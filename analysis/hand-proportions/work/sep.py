import numpy as np
from scipy import ndimage as ndi

def bilin(img,x,y):
    return ndi.map_coordinates(img,[np.asarray(y,float),np.asarray(x,float)],order=1,mode='nearest')

def profile(img, c, n, hw, smooth=1.5):
    ts=np.arange(-hw,hw+1e-9,0.5)
    v=bilin(img, c[0]+ts*n[0], c[1]+ts*n[1])
    return ts, ndi.gaussian_filter1d(v,smooth)

def sep_amplitude(img, c, n, sign, hw, search=0.45):
    """amplitude of the separation feature at station c, transverse dir n.
    sign=+1: feature is BRIGHT (paper wedge). sign=-1: feature is DARK (groove)."""
    ts,v = profile(img,c,n,hw)
    w=v*sign
    m0=int(len(w)*(0.5-search)); m1=int(len(w)*(0.5+search))
    j=m0+int(np.argmax(w[m0:m1]))
    # flanking digit extrema = minima of w on each side, searched outward from j
    li=np.argmin(w[:j]) if j>2 else 0
    ri=j+ (np.argmin(w[j:]) if j<len(w)-3 else 0)
    base=0.5*(w[li]+w[ri])
    return ts[j], w[j]-base, (ts[li],ts[ri])

def measure_sep(img, p0, direction, sign, hw, step=2.0, nsteps=200, refit=True):
    d=np.array(direction,float); d/=np.linalg.norm(d)
    n=np.array([-d[1],d[0]])
    p0=np.array(p0,float)
    cs=[];amps=[];pts=[]
    for k in range(nsteps):
        c=p0+k*step*d
        try: t,a,_=sep_amplitude(img,c,n,sign,hw)
        except Exception: break
        cs.append(t);amps.append(a);pts.append(c+t*n)
    amps=np.array(amps); pts=np.array(pts); S=np.arange(len(amps))*step
    if refit and len(amps)>20:
        Aref=np.percentile(amps,80)
        good=amps>0.7*Aref
        if good.sum()>=8:
            P=pts[good]
            # total least squares line through the good separation centres
            m=P.mean(0); u,s,vt=np.linalg.svd(P-m); dd=vt[0]
            if np.dot(dd,d)<0: dd=-dd
            # restart at the most distal good point projected on the line
            proj=(P-m)@dd
            start=m+proj.min()*dd
            return measure_sep(img,start,dd,sign,hw,step,nsteps,refit=False)
    return S,pts,amps,d,n

def cleft(S,amps,frac=0.5,hold=12):
    A=ndi.uniform_filter1d(amps.astype(float),5)
    Aref=float(np.percentile(A,80)); thr=frac*Aref
    i0=0
    for i in range(len(A)):
        if A[i]>0.85*Aref: i0=i;break
    idx=None
    for i in range(i0,len(A)):
        if A[i]<thr and A[i:i+hold].max()<thr: idx=i;break
    if idx is None: idx=len(A)-1
    if idx>0 and A[idx-1]!=A[idx]:
        f=(A[idx-1]-thr)/(A[idx-1]-A[idx]); s=S[idx-1]+f*(S[idx]-S[idx-1])
    else: s=S[idx]
    return s, idx, Aref, A
