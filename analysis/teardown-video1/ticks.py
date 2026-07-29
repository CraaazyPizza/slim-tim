import numpy as np, sys
from PIL import Image, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
def enh(f,box):
    im=Image.open(F.format(f)).convert('L').crop(box)
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(9))).astype(np.float32)
    return a-bg
def ncc(A,B):
    A=A-A.mean(); B=B-B.mean()
    return float((A*B).sum()/(np.sqrt((A*A).sum()*(B*B).sum())+1e-9))
def best(A,B,r=4):
    h,w=A.shape; bestv=-2
    core=A[r:h-r,r:w-r]
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            bestv=max(bestv,ncc(core,B[r+dy:h-r+dy,r+dx:w-r+dx]))
    return bestv
a,b=int(sys.argv[1]),int(sys.argv[2]); box=eval(sys.argv[3])
th=float(sys.argv[4]) if len(sys.argv)>4 else 0.85
prev=None; res=[]
for f in range(a,b+1):
    cur=enh(f,box)
    if prev is not None:
        v=best(prev,cur)
        res.append((f,v))
    prev=cur
for f,v in res:
    if v<th: print(f, round(v,3), '  t=%.3f'%((f-1)/29.97))
