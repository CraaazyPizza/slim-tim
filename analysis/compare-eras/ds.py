import sys,os,numpy as np
from PIL import Image
fd,label=sys.argv[1],sys.argv[2]; f0,f1=int(sys.argv[3]),int(sys.argv[4])
y0,y1,x0,x1=map(int,sys.argv[5:9]); ds=int(sys.argv[9]); out=sys.argv[10]
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
acc=None;n=0
for i in range(f0,f1+1):
    a=np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)[y0:y1,x0:x1]
    acc=a if acc is None else acc+a; n+=1
M=acc/n
H,W=M.shape
A=np.asarray(Image.fromarray(M,mode='F').resize((W//ds,H//ds),Image.BOX),dtype=np.float32)
def gb(a,k):
    o=a.copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
print('%s n=%d  downscaled to %s'%(label,n,A.shape))
for k in (3,6,10):
    hp=A-gb(A,k)
    for pct,tag in [((2,98),'p2'),((6,94),'p6'),((15,85),'p15')]:
        lo,hi=np.percentile(hp,pct[0]),np.percentile(hp,pct[1])
        v=np.clip((hp-lo)/(hi-lo+1e-9),0,1)
        im=Image.fromarray(((1-v)*255).astype(np.uint8)).resize((W,H*2),Image.LANCZOS)
        im.save('%s_k%d_%s.png'%(out,k,tag))
