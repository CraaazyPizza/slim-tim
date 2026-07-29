import numpy as np
from scipy import ndimage as ndi

def find_caps(img, box, capthr, minarea=120, maxarea=2200):
    y0,y1,x0,x1=box
    sub=ndi.gaussian_filter(img[y0:y1,x0:x1].astype(float),1.0)
    m=sub<capthr
    m=ndi.binary_opening(m,np.ones((3,3)))
    lab,n=ndi.label(m)
    out=[]
    for k in range(1,n+1):
        c=(lab==k); a=c.sum()
        if not (minarea<=a<=maxarea): continue
        ys,xs=np.nonzero(c)
        h=ys.max()-ys.min()+1; w=xs.max()-xs.min()+1
        if max(h,w)/max(1,min(h,w))>3.2: continue
        out.append(dict(area=int(a), cx=float(xs.mean()+x0), cy=float(ys.mean()+y0),
                        pix=(xs+x0, ys+y0), h=int(h), w=int(w)))
    return out

def cap_tip(cap, axis):
    """extreme point of the cap along `axis` (unit vector pointing distally)"""
    xs,ys=cap['pix']
    p=np.stack([xs,ys],1).astype(float)
    s=p@np.array(axis,float)
    k=int(np.argmax(s))
    # average of the top few for stability
    o=np.argsort(-s)[:max(3,len(s)//12)]
    return p[o].mean(0)
