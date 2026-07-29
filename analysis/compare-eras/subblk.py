import sys,os,numpy as np
from PIL import Image
fd=sys.argv[1]; f0=int(sys.argv[2]); f1=int(sys.argv[3])
y0,y1,x0,x1=map(int,sys.argv[4:8]); blk=int(sys.argv[8]); out=sys.argv[9]
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
def gb(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
B=[]
for i in range(f0,f1+1):
    B.append(np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)[y0:y1,x0:x1])
B=np.stack(B)
tiles=[];labs=[]
for s in range(0,len(B)-blk+1,blk):
    m=B[s:s+blk].mean(0)
    hp=m-gb(m,20)
    tiles.append(hp); labs.append(f0+s)
A=np.stack(tiles)
# static component = median across sub-blocks (kills anything that changes)
static=np.median(A,0)
print('sub-blocks: %d of %d frames each, starting frames %s'%(len(tiles),blk,labs))
H,W=static.shape
def sv(img,fn,pct=(2,98)):
    g=img-np.median(img,axis=1,keepdims=True)*0
    lo,hi=np.percentile(g,pct[0]),np.percentile(g,pct[1])
    v=np.clip((g-lo)/(hi-lo+1e-9),0,1)
    Image.fromarray(((1-v)*255).astype(np.uint8)).resize((W*2,img.shape[0]*2),Image.LANCZOS).save(fn)
sv(static,out+'_static.png',(3,97))
can=np.zeros(((H+4)*len(tiles),W))
for i,t in enumerate(tiles): can[i*(H+4):i*(H+4)+H]=t
sv(can,out+'_ladder.png',(3,97))
np.save(out+'_static.npy',static)
print('saved',out+'_static.png',out+'_ladder.png')
