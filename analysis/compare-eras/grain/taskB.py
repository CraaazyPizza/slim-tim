import numpy as np, sys, json
from lib import *
from scipy.ndimage import gaussian_filter
from multiprocessing import Pool
SPAN={'OpSTlDJWFFI':(1500,2400),'Oqw96jCOP7A':(600,1500),'l9RAhmPHM_A':(1000,1900),
'ZB788PtqQvg':(200,1100),'RsQCXN4o4Ps':(600,1450),'Xju_CY5ZESA':(200,1100),'a6TLGkrfNKI':(200,1100)}
B=256
def rect(k):
    y0,y1,x0,x1=PIC[k]; cy=(y0+y1)//2; cx=(x0+x1)//2
    b=B if (y1-y0)>=B and (x1-x0)>=B else 160
    return (cy-b//2,cy+b//2,cx-b//2,cx+b//2)
def job(a):
    k,i,r=a; y0,y1,x0,x1=r
    p=F(k,i)[y0:y1,x0:x1]
    return i,(p-gaussian_filter(p,2.0)).astype(np.float32),(p-gaussian_filter(p,8.0)).astype(np.float32),p.astype(np.float32)
def ncc(A,B_):
    a=A-A.mean(axis=(1,2),keepdims=True); b=B_-B_.mean(axis=(1,2),keepdims=True)
    num=(a*b).sum(axis=(1,2)); den=np.sqrt((a*a).sum(axis=(1,2))*(b*b).sum(axis=(1,2)))
    return num/np.maximum(den,1e-12)
k=sys.argv[1]
s,e=SPAN[k]; r=rect(k)
with Pool(6) as p:
    out=p.map(job,[(k,i,r) for i in range(s,e+1)],chunksize=8)
out.sort()
HP2=np.stack([o[1] for o in out]); HP8=np.stack([o[2] for o in out]); RAW=np.stack([o[3] for o in out]); del out
N=len(HP2)
# content-free temporal residual
TR=RAW[1:-1]-0.5*(RAW[:-2]+RAW[2:])
TR=np.stack([t-gaussian_filter(t,8.0) for t in TR]).astype(np.float32)
del RAW
LAGS=list(range(1,301))+[320,350,375,400,425,450,500,550,600,625,650,700,750,800]
res={'video':k,'era':ERA[k],'span':[s,e],'rect':list(r),'N':N}
for nm,ARR in [('HP2',HP2),('HP8',HP8),('TRES',TR)]:
    c={}
    for L in LAGS:
        if L>=len(ARR)-2: continue
        v=ncc(ARR[:-L],ARR[L:])
        c[L]=(float(np.mean(v)),float(np.median(v)),float(np.percentile(v,99)),float(np.max(v)))
    res[nm]=c
    ks=sorted(c); mn=np.array([c[i][0] for i in ks]); md=np.array([c[i][1] for i in ks])
    base=np.median(md[20:]) if len(md)>20 else np.median(md)
    print('-- %s %s  mean-NCC lag1..12: %s'%(k,nm,np.round([c[i][0] for i in ks[:12]],4)))
    print('   median-NCC baseline(lag>20)=%.4f ; top-10 lags by median-NCC:'%base)
    o=np.argsort(-md)[:10]
    print('   '+' '.join('k=%d:%.4f'%(ks[i],md[i]) for i in o))
    print('   max over lags of 99th pct: %s'%' '.join('k=%d:%.3f'%(ks[i],c[ks[i]][2]) for i in np.argsort(-np.array([c[i][2] for i in ks]))[:6]))
json.dump(res,open('taskB_%s.json'%k,'w'))
