import numpy as np, sys, json
from lib import *
from scipy.ndimage import gaussian_filter
from multiprocessing import Pool
SPAN={'OpSTlDJWFFI':(1040,2900),'Oqw96jCOP7A':(460,2400),'l9RAhmPHM_A':(900,2700),
'ZB788PtqQvg':(60,1150),'RsQCXN4o4Ps':(400,1490),'Xju_CY5ZESA':(150,1350),'a6TLGkrfNKI':(150,1350)}
B = 192
def rect(k):
    y0,y1,x0,x1=PIC[k]; cy=(y0+y1)//2; cx=(x0+x1)//2
    b=B if (y1-y0)>=B and (x1-x0)>=B else 160
    return (cy-b//2,cy+b//2,cx-b//2,cx+b//2)
def job(a):
    k,i,r=a; y0,y1,x0,x1=r
    p=F(k,i)[y0:y1,x0:x1]
    return i,(p-gaussian_filter(p,2.0)).astype(np.float32),p.astype(np.float32)
def unit(A):
    X=A.reshape(len(A),-1).astype(np.float32)
    X-=X.mean(1,keepdims=True)
    X/=np.maximum(np.linalg.norm(X,axis=1,keepdims=True),1e-9)
    return X
def lagstats(X,nm,res,maxlag=900):
    G=X@X.T; N=len(X)
    L=[];mn=[];md=[];p99=[];mx=[]
    for lag in range(1,min(N-2,maxlag+1)):
        d=np.diagonal(G,lag)
        L.append(lag);mn.append(d.mean());md.append(np.median(d));p99.append(np.percentile(d,99));mx.append(d.max())
    L=np.array(L);mn=np.array(mn);md=np.array(md);p99=np.array(p99);mx=np.array(mx)
    res[nm]=dict(lag=L.tolist(),mean=mn.tolist(),median=md.tolist(),p99=p99.tolist(),max=mx.tolist())
    far=L>30
    base=np.median(mn[far]); mad=1.4826*np.median(np.abs(mn[far]-base))
    z=(mn-base)/max(mad,1e-9)
    print('  [%s] N=%d  mean-NCC lag1..10: %s'%(nm,N,np.round(mn[:10],4)))
    print('       baseline mean-NCC(lag>30)=%+.5f  MAD=%.5f  ; max|z| over lags>30 = %.1f at k=%d'%(
        base,mad,np.abs(z[far]).max(),L[far][np.argmax(np.abs(z[far]))]))
    o=np.argsort(-mn[far])[:8]
    print('       top-8 lags>30 by mean-NCC: '+' '.join('k=%d:%+.4f(z%+.1f)'%(L[far][i],mn[far][i],z[far][i]) for i in o))
    o2=np.argsort(-mx[far])[:5]
    print('       top-5 lags>30 by MAX single-pair NCC: '+' '.join('k=%d:%.3f'%(L[far][i],mx[far][i]) for i in o2))
    print('       p99 of single-pair NCC across all lags>30: median=%.4f  max=%.4f'%(np.median(p99[far]),p99[far].max()))
if __name__=='__main__':
    k=sys.argv[1]
    s,e=SPAN[k]; s=max(2,s); e=min(e,nframes(k)-2); r=rect(k)
    with Pool(5) as p:
        out=p.map(job,[(k,i,r) for i in range(s,e+1)],chunksize=16)
    out.sort()
    HP2=np.stack([o[1] for o in out]); RAW=np.stack([o[2] for o in out]); del out
    TR=(RAW[1:-1]-0.5*(RAW[:-2]+RAW[2:]))
    TR=np.stack([t-gaussian_filter(t,8.0) for t in TR]).astype(np.float32); del RAW
    print('==== %s era%d span %d-%d rect y[%d:%d] x[%d:%d] N=%d'%(k,ERA[k],s,e,r[0],r[1],r[2],r[3],len(HP2)),flush=True)
    res={'video':k,'era':ERA[k],'span':[s,e],'rect':list(r)}
    lagstats(unit(HP2),'HP2 (spatial high-pass, sigma2)',res)
    sys.stdout.flush()
    lagstats(unit(TR),'TRES (content-free temporal residual)',res)
    json.dump(res,open('taskBf_%s.json'%k,'w'))
