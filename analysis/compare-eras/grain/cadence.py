import numpy as np
from lib import *
from multiprocessing import Pool
SPAN={'OpSTlDJWFFI':(1600,2000),'Oqw96jCOP7A':(600,1000),'l9RAhmPHM_A':(1000,1400),
'ZB788PtqQvg':(600,1000),'RsQCXN4o4Ps':(600,1000),'Xju_CY5ZESA':(600,1000),'a6TLGkrfNKI':(600,1000)}
def sub(k):
    y0,y1,x0,x1=PIC[k]
    cy=(y0+y1)//2; cx=(x0+x1)//2; h=min(200,(y1-y0)//2); w=min(256,(x1-x0)//2)
    return (cy-h,cy+h,cx-w,cx+w)
def job(a):
    k,i,r=a
    y0,y1,x0,x1=r
    return i,F(k,i)[y0:y1,x0:x1].astype(np.float32)
for k in V:
    s,e=SPAN[k]; r=sub(k)
    with Pool(6) as p:
        out=p.map(job,[(k,i,r) for i in range(s,e+1)],chunksize=8)
    out.sort(); st=np.stack([o[1] for o in out]); del out
    d=np.abs(np.diff(st,axis=0)).mean(axis=(1,2))
    exact=np.mean([float(np.array_equal(st[i],st[i+1])) for i in range(len(st)-1)])
    dd=d-d.mean(); ac=np.correlate(dd,dd,'full')[len(dd)-1:]/(dd@dd)
    print('== %s era%d span %d-%d rect y[%d:%d] x[%d:%d]'%(k,ERA[k],s,e,*r))
    print('   meandiff=%.4f exact-dup frac=%.3f  frac d<0.02=%.3f  p5/25/50/75/95=%s'%(
      d.mean(),exact,(d<0.02).mean(),np.round(np.percentile(d,[5,25,50,75,95]),4)),flush=True)
    print('   diffsig autocorr lag1..12: %s'%np.round(ac[1:13],3))
    np.save('diffsig_%s.npy'%k,d); del st
