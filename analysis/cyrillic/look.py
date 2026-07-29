import numpy as np, sys
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from PIL import Image
ci=[FR.index(f) for f in CAP]
def out(X, rows, xs, fn, lo=1, hi=99, sc=1, inv=True, resample=Image.NEAREST):
    b=X[(rows[0]-Y0):(rows[1]-Y0),(xs[0]-X0):(xs[1]-X0)]
    a,bq=np.percentile(b,[lo,hi]); Q=np.clip((b-a)/(bq-a),0,1)
    if inv: Q=1-Q
    im=Image.fromarray((Q*255).astype(np.uint8))
    if sc!=1: im=im.resize((im.width*sc,im.height*sc),resample)
    im.save(fn); return fn
STK=-pp(RES[ci].mean(0)); F983=-pp(RES[FR.index(983)])
for tag,X in [('stack',STK),('f983',F983)]:
    out(X,(905,1000),(430,1620),'L1_%s.png'%tag)
    out(X,(995,1080),(430,1620),'L2_%s.png'%tag)
    out(X,(905,1080),(430,1620),'BOTH_%s.png'%tag, sc=1)
# amplitude in 8-bit levels
print('ink depth (stack, line1 band, 99th pct of ink):', np.percentile(STK[(925-Y0):(1000-Y0),(445-X0):(1600-X0)],99.5)*255*  (1.0))
print('ink depth f983:', np.percentile(F983[(925-Y0):(1000-Y0),(445-X0):(1600-X0)],99.5)*255)
print('noise sd (stack):', STK[(900-Y0):(920-Y0),(445-X0):(1600-X0)].std()*255)
print('noise sd (f983):', F983[(900-Y0):(920-Y0),(445-X0):(1600-X0)].std()*255)
