import numpy as np
from scipy import ndimage as ndi

def row_track(img, y0, y1, x_start, sign, halfwin=45, follow=20, smooth=1.5):
    """Row-wise tracker for an inter-digital separation feature.
    sign=+1 : feature is BRIGHT relative to the digits (paper wedge in an ink print)
    sign=-1 : feature is DARK  relative to the digits (shadow groove in a photo)
    Returns y, x_sep, v_sep, v_flank (all in the image's own units, sign-corrected so
    that larger v_sep = more open)."""
    ys=[];xs=[];vs=[];vf=[]
    x=float(x_start); step=1 if y1>y0 else -1
    for y in range(int(y0),int(y1)+step,step):
        row=ndi.gaussian_filter1d(img[y].astype(float),smooth)
        w=row*sign
        lo=int(max(0,x-follow)); hi=int(min(len(row)-1,x+follow))
        j=lo+int(np.argmax(w[lo:hi+1]))
        L=max(0,j-halfwin); R=min(len(row)-1,j+halfwin)
        if j-L<5 or R-j<5: break
        jl=L+int(np.argmin(w[L:j])); jr=j+int(np.argmin(w[j:R+1]))
        ys.append(y); xs.append(j); vs.append(w[j]); vf.append(0.5*(w[jl]+w[jr]))
        x=0.55*x+0.45*j
    return (np.array(ys),np.array(xs,float),np.array(vs,float),np.array(vf,float))

def cleft_level(y,vs,vf,frac=0.5,plateau=0.40,hold=8):
    """Cleft = where the separation feature's level has moved `frac` of the way from its
    fully-open value g0 (median over the distal plateau) to the flanking digit level."""
    V=ndi.uniform_filter1d(vs,7); F=ndi.uniform_filter1d(vf,15)
    npl=max(6,int(len(V)*plateau)); g0=float(np.median(V[:npl]))
    thr=F+frac*(g0-F)
    idx=None
    for i in range(npl//2,len(V)):
        if V[i]<thr[i] and (V[i:i+hold]<thr[i:i+hold]).all(): idx=i;break
    if idx is None: idx=len(V)-1
    if idx>0:
        a=V[idx-1]-thr[idx-1]; b=V[idx]-thr[idx]
        f=a/(a-b) if a!=b else 0.0
        yy=y[idx-1]+f*(y[idx]-y[idx-1])
    else: yy=y[idx]
    return yy, idx, g0, V, thr
