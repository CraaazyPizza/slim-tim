import sys,os,numpy as np
from PIL import Image
fd=sys.argv[1]; label=sys.argv[2]; f0=int(sys.argv[3]); f1=int(sys.argv[4])
y0,y1,x0,x1=map(int,sys.argv[5:9])
out=sys.argv[9]
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
def blur(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
acc=None;n=0
for i in range(f0,f1+1):
    a=np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)[y0:y1,x0:x1]
    acc=a if acc is None else acc+a; n+=1
M=acc/n
print('%s: averaged %d frames, region y%d-%d x%d-%d, mean=%.2f sd=%.3f min=%.1f max=%.1f'%(label,n,y0,y1,x0,x1,M.mean(),M.std(),M.min(),M.max()))
hp=M-blur(M,12)
print('   high-pass sd=%.4f  p1=%.3f p99=%.3f'%(hp.std(),np.percentile(hp,1),np.percentile(hp,99)))
for tag,img,pct in [('raw',M,(2,98)),('hp',hp,(1,99)),('hp_hard',hp,(5,95))]:
    lo,hi=np.percentile(img,pct[0]),np.percentile(img,pct[1])
    v=np.clip((img-lo)/(hi-lo+1e-9),0,1)
    Image.fromarray((v*255).astype(np.uint8)).resize(((x1-x0)*2,(y1-y0)*2),Image.LANCZOS).save('%s_%s.png'%(out,tag))
    Image.fromarray(((1-v)*255).astype(np.uint8)).resize(((x1-x0)*2,(y1-y0)*2),Image.LANCZOS).save('%s_%s_inv.png'%(out,tag))
np.save(out+'.npy',M)
print('   saved %s_{raw,hp,hp_hard}[_inv].png'%out)
