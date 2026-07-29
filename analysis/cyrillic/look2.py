import numpy as np, sys
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from PIL import Image
from scipy.ndimage import gaussian_filter as gf
ci=[FR.index(f) for f in CAP]
def img(X, rows, xs, fn, lo=1, hi=99, sc=1, resample=Image.LANCZOS, sig=0.0):
    b=X[(rows[0]-Y0):(rows[1]-Y0),(xs[0]-X0):(xs[1]-X0)]
    if sig: b=gf(b,sig)
    a,bq=np.percentile(b,[lo,hi]); Q=1-np.clip((b-a)/(bq-a),0,1)
    im=Image.fromarray((Q*255).astype(np.uint8))
    if sc!=1: im=im.resize((int(im.width*sc),int(im.height*sc)),resample)
    im.save(fn); return fn
F=-pp(RES[FR.index(983)])
STK=-pp(RES[ci].mean(0))
img(F,(998,1078),(1150,1580),'z_l2_tail_f983_x6.png',sc=6)
img(F,(998,1078),(430,1200),'z_l2_head_f983_x3.png',sc=3)
img(F,(905,1000),(430,1620),'z_l1_f983_x3.png',sc=3)
img(STK,(998,1078),(1150,1580),'z_l2_tail_stack_x6.png',sc=6)
img(F,(998,1078),(430,1580),'z_l2_full_f983_x2.png',sc=2)
print('ok')
