"""Clean vertical metrics: residual only (no high-pass, no ringing).
Per-row offset taken from caption-free columns outside the text."""
import numpy as np, sys
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
OFFC=np.r_[np.arange(300-X0,430-X0), np.arange(1625-X0,1750-X0)]
def clean(X):
    Y=-X                             # ink positive
    return Y - Y[:,OFFC].mean(1,keepdims=True)
ci=[FR.index(f) for f in CAP]
OB={'f983':clean(RESL[FR.index(983)]),
    'best5':clean(RESL[[FR.index(f) for f in (983,973,974,984,981)]].mean(0)),
    'stack20':clean(RESL[ci].mean(0))}
NUL=clean(RESL[[FR.index(f) for f in range(1010,1030)]].mean(0))
def rp(X,xs,rows=(905,1000)):
    return np.arange(rows[0],rows[1]), X[(rows[0]-Y0):(rows[1]-Y0),(xs[0]-X0):(xs[1]-X0)].mean(1)
X=OB['best5']
ys,pP=rp(X,(452,504)); _,po=rp(X,(1176,1220)); _,poo=rp(X,(1238,1280))
_,pcc=rp(X,(1122,1158)); _,pnul=rp(NUL,(1176,1220))
print(' y     П      o1      o2      c    NULLo1   (units 1e3)')
for i,y in enumerate(ys):
    print('%4d %7.2f %7.2f %7.2f %7.2f %7.2f'%(y,pP[i]*1e3,po[i]*1e3,poo[i]*1e3,pcc[i]*1e3,pnul[i]*1e3))
