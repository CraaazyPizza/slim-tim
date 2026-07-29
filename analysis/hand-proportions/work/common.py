import numpy as np
from scipy import ndimage as ndi

def bilin(img, x, y):
    x=np.asarray(x,float); y=np.asarray(y,float)
    return ndi.map_coordinates(img, [y,x], order=1, mode='nearest')

def track_separation(img, start, direction, sign, halfwidth=32, step=1.5, nsteps=400,
                     flank=None, smooth=2.0):
    """March from `start` along `direction` (unit, pointing PROXIMALLY).
    At each step sample a transverse profile; find the separation-feature extremum
    (sign=+1 -> bright feature e.g. paper wedge; sign=-1 -> dark feature e.g. groove).
    Returns arrays: s (arclength), pts (x,y of feature centre), amp (feature amplitude
    relative to the two flanking digit levels)."""
    if flank is None: flank = halfwidth
    d = np.array(direction,float); d/= np.linalg.norm(d)
    p = np.array(start,float)
    n = np.array([-d[1], d[0]])
    ts = np.arange(-halfwidth, halfwidth+1e-9, 0.5)
    S,P,A,Wd = [],[],[],[]
    for k in range(nsteps):
        prof = bilin(img, p[0]+ts*n[0], p[1]+ts*n[1])
        prof = ndi.gaussian_filter1d(prof, smooth)
        v = prof*sign
        m0 = int(len(v)*0.30); m1=int(len(v)*0.70)
        j = m0 + int(np.argmax(v[m0:m1]))
        # flanking digit levels: max of the opposite sign outside the feature
        left  = v[:max(j-6,1)]; right = v[min(j+6,len(v)-1):]
        if len(left)<3 or len(right)<3: break
        if abs(ts[j])>0.55*halfwidth: break
        base = 0.5*(left.min()+right.min())
        amp = v[j]-base
        cen = ts[j]
        # sub-pixel by parabola
        if 0<j<len(v)-1:
            y0,y1,y2=v[j-1],v[j],v[j+1]
            den=(y0-2*y1+y2)
            if den < -1e-9:
                dd = 0.5*(y0-y2)/den
                if abs(dd) <= 1.0: cen = ts[j] + dd*0.5
        q = p + cen*n
        S.append(k*step); P.append(q.copy()); A.append(amp)
        # keep the march direction fixed; only the transverse centre is re-estimated
        p = np.array([q[0], q[1]])
        # width of the feature at half amplitude
        half=base+0.5*amp
        li=j
        while li>0 and v[li]>half: li-=1
        ri=j
        while ri<len(v)-1 and v[ri]>half: ri+=1
        Wd.append((ri-li)*0.5)
        p = q + step*d
    return np.array(S), np.array(P), np.array(A), np.array(Wd)

def cleft_from_track(S,A,frac=0.5,hold=20):
    """Cleft = the arclength at which the separation feature's amplitude has decayed
    to `frac` of its plateau value and stays there for `hold` steps."""
    As=ndi.uniform_filter1d(np.asarray(A,float),9)
    Aref=float(np.percentile(As,80))
    thr=frac*Aref
    n=len(As)
    i0=0
    for i in range(n):
        if As[i]>0.7*Aref: i0=i; break
    idx=None
    for i in range(i0,n):
        if As[i]<thr and As[i:min(i+hold,n)].max()<thr: idx=i; break
    if idx is None: idx=n-1
    if idx>0 and As[idx-1]!=As[idx]:
        f=(As[idx-1]-thr)/(As[idx-1]-As[idx]); s=S[idx-1]+f*(S[idx]-S[idx-1])
    else: s=S[idx]
    return s, idx, Aref
