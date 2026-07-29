import sys,numpy as np
from PIL import Image
pre=sys.argv[1]; out=sys.argv[2]; NR=int(sys.argv[3]); scale=int(sys.argv[4])
B=np.load(pre+'_band.npy'); idx=np.load(pre+'_idx.npy'); runs=np.load(pre+'_runs.npy')
lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
def blur(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
tiles=[];hp=[]
for o in order[:NR]:
    a,b=runs[o]
    m=B[a:b].astype(np.float32).mean(0)
    h=m-blur(m,25)
    if h.std()<1e-6: continue
    hp.append(h/h.std())
    lo,hi=np.percentile(h,0.5),np.percentile(h,99.7)
    tiles.append(np.clip((h-lo)/(hi-lo+1e-9),0,1))
    print('run f%d-f%d n=%d'%(idx[a],idx[b-1],b-a))
H,W=tiles[0].shape
canvas=np.zeros(((H+3)*len(tiles),W))
for i,t in enumerate(tiles): canvas[i*(H+3):i*(H+3)+H]=t
Image.fromarray((canvas*255).astype(np.uint8)).resize((W*scale,canvas.shape[0]*scale),Image.LANCZOS).save(out)
A=np.stack(hp); np.save(pre+'_hp.npy',A)
mx=A.max(0)
np.save(pre+'_union.npy',mx)
lo,hi=np.percentile(mx,0.5),np.percentile(mx,99.8)
Image.fromarray((np.clip((mx-lo)/(hi-lo),0,1)*255).astype(np.uint8)).resize((W*6,H*6),Image.LANCZOS).save(pre+'_UNION.png')
print('saved',out,'and',pre+'_UNION.png','nruns',len(hp))
