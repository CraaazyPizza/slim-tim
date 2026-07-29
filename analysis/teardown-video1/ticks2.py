import numpy as np, sys
from PIL import Image, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
def enh(f,box):
    im=Image.open(F.format(f)).convert('L').crop(box)
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(7))).astype(np.float32)
    d=a-bg
    return (d>6).astype(np.float32)   # binary map of bright thin structures
def iou(A,B):
    i=(A*B).sum(); u=((A+B)>0).sum()
    return float(i/(u+1e-9))
def bestiou(A,B,r=3):
    h,w=A.shape; core=A[r:h-r,r:w-r]; bv=0
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            bv=max(bv,iou(core,B[r+dy:h-r+dy,r+dx:w-r+dx]))
    return bv
a,b=int(sys.argv[1]),int(sys.argv[2]); box=eval(sys.argv[3]); lag=int(sys.argv[4]) if len(sys.argv)>4 else 2
E={f:enh(f,box) for f in range(a,b+1)}
vals=[]
for f in range(a+lag,b+1):
    vals.append((f,bestiou(E[f-lag],E[f])))
np.save('iou_%d_%d.npy'%(a,b),np.array(vals))
for f,v in vals: print(f,round(v,3))
