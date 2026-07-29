import numpy as np, sys
sys.path.insert(0,'.')
from util import rd
from scipy.signal import fftconvolve
def nccmap(I,t,floor=1.0):
    t=t-t.mean(); tn=np.sqrt((t*t).sum())+1e-9
    o=np.ones_like(t); c=t.size
    num=fftconvolve(I,t[::-1,::-1],'valid')
    s1=fftconvolve(I,o,'valid'); s2=fftconvolve(I*I,o,'valid')
    var=np.maximum(s2-s1*s1/c, floor*c)
    return num/(np.sqrt(var)*tn)
def track(anchor, box, frames, search=90):
    """chain-track template from anchor frame across frames (ordered outward)."""
    y0,y1,x0,x1=box
    ref=rd(anchor); tmpl=ref[y0:y1,x0:x1].astype(np.float64)
    pos={anchor:(0.0,0.0,1.0)}
    for direction in (1,-1):
        cx,cy=0.0,0.0; t=tmpl.copy()
        seq=[f for f in frames if (f-anchor)*direction>0]
        seq.sort(key=lambda f:(f-anchor)*direction)
        for f in seq:
            img=rd(f).astype(np.float64)
            Y0=int(max(0,y0+cy-search)); Y1=int(min(img.shape[0],y1+cy+search))
            X0=int(max(0,x0+cx-search)); X1=int(min(img.shape[1],x1+cx+search))
            n=nccmap(img[Y0:Y1,X0:X1], t)
            i=np.unravel_index(np.argmax(n),n.shape)
            def sp(v,k):
                if 0<k<len(v)-1:
                    den=(v[k-1]-2*v[k]+v[k+1])
                    return k+((v[k-1]-v[k+1])/(2*den) if abs(den)>1e-9 else 0)
                return k
            yy=sp(n[:,i[1]],i[0]); xx=sp(n[i[0],:],i[1])
            cx=(X0+xx)-x0; cy=(Y0+yy)-y0
            pos[f]=(cx,cy,float(n[i]))
            # refresh template from this frame (adaptive)
            ny0=int(round(y0+cy)); nx0=int(round(x0+cx))
            t=img[ny0:ny0+(y1-y0), nx0:nx0+(x1-x0)].copy()
    return pos
