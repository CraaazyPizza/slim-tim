import numpy as np, sys
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from PIL import Image
from scipy.ndimage import gaussian_filter as gf
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
def prep_disp(X):
    Y=X-np.median(X,axis=1,keepdims=True)
    return -gf(Y-gf(Y,12),(1.5,0.8))
F=prep_disp(RESL[FR.index(983)])
def img(rows,xs,fn,sc,lo=1.5,hi=98.5,X=None):
    X=F if X is None else X
    b=X[(rows[0]-Y0):(rows[1]-Y0),(xs[0]-X0):(xs[1]-X0)]
    a,q=np.percentile(b,[lo,hi]); Q=1-np.clip((b-a)/(q-a),0,1)
    im=Image.fromarray((Q*255).astype(np.uint8))
    im=im.resize((int(im.width*sc),int(im.height*sc)),Image.LANCZOS); im.save(fn)
img((995,1080),(435,820),'q_l2_a.png',5)
img((995,1080),(800,1180),'q_l2_b.png',5)
img((995,1080),(1160,1580),'q_l2_c.png',5)
img((905,1005),(435,1030),'q_l1_a.png',4)
img((905,1005),(1010,1620),'q_l1_b.png',4)
