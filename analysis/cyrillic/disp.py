"""Display pipeline experiments for the single best frame."""
import numpy as np, sys
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from PIL import Image
from scipy.ndimage import gaussian_filter as gf, median_filter as mf
ci=[FR.index(f) for f in CAP]
# local background: frames adjacent to the caption block only
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg = S[[FR.index(f) for f in LOC]].mean(0)
RESL = S - _lbg
def var(X, mode):
    Y = X - np.median(X,axis=1,keepdims=True)
    if mode=='hp20':      Z = Y - gf(Y,(0,20))
    elif mode=='iso20':   Z = Y - gf(Y,20)
    elif mode=='iso20s1': Z = gf(Y - gf(Y,20), 1.0)
    elif mode=='iso12s15':Z = gf(Y - gf(Y,12), (1.5,0.8))
    elif mode=='hp20s':   Z = gf(Y - gf(Y,(0,20)), (1.6,0.6))
    elif mode=='bp':      Z = gf(Y,(1.2,0.8)) - gf(Y,(14,14))
    return Z
def img(X,rows,xs,fn,sc,lo=1.5,hi=98.5):
    b=X[(rows[0]-Y0):(rows[1]-Y0),(xs[0]-X0):(xs[1]-X0)]
    a,q=np.percentile(b,[lo,hi]); Q=1-np.clip((b-a)/(q-a),0,1)
    im=Image.fromarray((Q*255).astype(np.uint8))
    im=im.resize((int(im.width*sc),int(im.height*sc)),Image.LANCZOS); im.save(fn)
for m in ['hp20','iso20','iso20s1','iso12s15','hp20s','bp']:
    X=-var(RESL[FR.index(983)],m)
    img(X,(995,1080),(430,1580),'v_%s_l2.png'%m,2)
    img(X,(905,1005),(430,1620),'v_%s_l1.png'%m,2)
print('done')
