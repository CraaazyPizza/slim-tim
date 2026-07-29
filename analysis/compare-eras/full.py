import sys,os,numpy as np
from PIL import Image
fd=sys.argv[1]; f0=int(sys.argv[2]); f1=int(sys.argv[3]); out=sys.argv[4]
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
def blur(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
acc=None;n=0
for i in range(f0,f1+1):
    a=np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)
    acc=a if acc is None else acc+a; n+=1
M=acc/n
hp=M-blur(M,10)
np.save(out+'_M.npy',M); np.save(out+'_hp.npy',hp)
# row-wise local contrast: text rows have elevated high-pass energy
e=np.abs(hp).mean(1)
print('averaged %d frames. |hp| per row, rows with elevated energy:'%n)
med=np.median(e)
for y in range(0,len(e),4):
    if e[y]>med*1.6: print('   y=%4d  |hp|=%.3f (x%.2f median)'%(y,e[y],e[y]/med))
lo,hi=np.percentile(hp,2),np.percentile(hp,98)
v=np.clip((hp-lo)/(hi-lo),0,1)
Image.fromarray(((1-v)*255).astype(np.uint8)).save(out+'_fullinv.png')
print('saved',out+'_fullinv.png', M.shape)
