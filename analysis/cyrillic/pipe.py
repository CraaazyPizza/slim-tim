"""Final display + measurement pipeline. Ink POSITIVE, no ringing."""
import numpy as np, sys
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from PIL import Image
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
OFFC=np.r_[np.arange(300-X0,430-X0), np.arange(1630-X0,1750-X0)]
def _clean(X):
    Y=-X; return Y - Y[:,OFFC].mean(1,keepdims=True)
NULLF=list(range(1005,1050))
NUL=_clean(RESL[[FR.index(f) for f in NULLF]].mean(0))
def sig(fs):
    """caption layer, ink positive, systematic y/x drift removed via caption-free frames"""
    return _clean(RESL[[FR.index(f) for f in fs]].mean(0)) - NUL
BEST=983
BEST5=[983,973,974,984,981]
def save(X, rows, xs, fn, sc=1, resample=Image.NEAREST, lo=1.0, hi=99.0, gamma=1.0):
    b=X[(rows[0]-Y0):(rows[1]-Y0),(xs[0]-X0):(xs[1]-X0)]
    a,q=np.percentile(b,[lo,hi]); Q=np.clip((b-a)/(q-a),0,1)**gamma
    im=Image.fromarray(((1-Q)*255).astype(np.uint8))
    if sc!=1: im=im.resize((int(im.width*sc),int(im.height*sc)),resample)
    im.save(fn); return im
