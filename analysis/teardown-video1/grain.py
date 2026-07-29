import numpy as np, sys
from PIL import Image, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
box=eval(sys.argv[3]); a,b=int(sys.argv[1]),int(sys.argv[2])
R=[]
for f in range(a,b+1):
    im=Image.open(F.format(f)).convert('L').crop(box)
    x=np.asarray(im).astype(np.float32)
    hp=x-np.asarray(im.filter(ImageFilter.GaussianBlur(1.6))).astype(np.float32)
    R.append(hp)
R=np.array(R)
print('hp rms per frame (first 12):',np.round([r.std() for r in R[:12]],3))
print('mean hp rms %.3f'%np.mean([r.std() for r in R]))
def c(l):
    v=[]
    for i in range(len(R)-l):
        A=R[i]-R[i].mean(); B=R[i+l]-R[i+l].mean()
        v.append(float((A*B).sum()/(np.sqrt((A*A).sum()*(B*B).sum())+1e-9)))
    return np.mean(v),np.std(v)
for l in range(1,9):
    m,s=c(l); print('lag',l,'corr %.3f +-%.3f'%(m,s))
