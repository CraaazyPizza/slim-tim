import numpy as np, sys
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/faces')
from util import rd
from scipy.ndimage import shift as ndshift, gaussian_filter
from PIL import Image
def mcavg(pos, frames, box, pad=0):
    y0,y1,x0,x1=box
    acc=None; k=0
    for f in frames:
        if f not in pos: continue
        cx,cy,q=pos[f]
        img=np.pad(rd(f),600,mode='edge')
        Y0=y0+cy-pad+600; X0=x0+cx-pad+600
        H=(y1-y0)+2*pad; W=(x1-x0)+2*pad
        iy=int(np.floor(Y0)); ix=int(np.floor(X0))
        fy=Y0-iy; fx=X0-ix
        sub=img[iy:iy+H+2, ix:ix+W+2].astype(np.float64)
        sub=ndshift(sub, (-fy,-fx), order=3, mode='nearest')[:H,:W]
        acc = sub if acc is None else acc+sub
        k+=1
    return acc/k, k
def enhance(a, sharp_sigma=4, amount=1.2, lo=0.5, hi=99.5):
    b = a + amount*(a - gaussian_filter(a, sharp_sigma))
    l,h=np.percentile(b,lo),np.percentile(b,hi)
    return np.clip((b-l)/(h-l)*255,0,255).astype(np.uint8)
def save(a,p,scale=1):
    im=Image.fromarray(a)
    if scale!=1: im=im.resize((int(im.width*scale),int(im.height*scale)),Image.LANCZOS)
    im.save(p); return p
