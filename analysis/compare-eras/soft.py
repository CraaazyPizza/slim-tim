import sys,numpy as np
from PIL import Image
M=np.load(sys.argv[1]); out=sys.argv[2]
ds=int(sys.argv[3]) if len(sys.argv)>3 else 2
H,W=M.shape
im=Image.fromarray(M.astype(np.float32),mode='F').resize((W//ds,H//ds),Image.BOX)
A=np.asarray(im,dtype=np.float32)
def gb(a,k):
    o=a.copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
for k in (6,12,25,50):
    hp=A-gb(A,k)
    for pct,tag in [((1,99),'p1'),((3,97),'p3'),((10,90),'p10')]:
        lo,hi=np.percentile(hp,pct[0]),np.percentile(hp,pct[1])
        v=np.clip((hp-lo)/(hi-lo+1e-9),0,1)
        Image.fromarray(((1-v)*255).astype(np.uint8)).resize((W,H),Image.LANCZOS).save('%s_k%d_%s.png'%(out,k,tag))
print('saved variants for k=6,12,25,50 x p1,p3,p10  (downscale %d)'%ds)
