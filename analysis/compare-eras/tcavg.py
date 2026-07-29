import sys,numpy as np
from PIL import Image
pre=sys.argv[1]; out=sys.argv[2]; scale=int(sys.argv[3]) if len(sys.argv)>3 else 6
B=np.load(pre+'_band.npy'); idx=np.load(pre+'_idx.npy'); runs=np.load(pre+'_runs.npy')
lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
tiles=[]
print('top runs:')
for o in order[:8]:
    a,b=runs[o]; m=B[a:b].mean(0)
    print('  frames %d-%d n=%d'%(idx[a],idx[b-1],b-a))
    # local contrast stretch
    lo,hi=np.percentile(m,1),np.percentile(m,99.7)
    t=np.clip((m-lo)/(hi-lo+1e-9),0,1)
    tiles.append((t,'%d-%d n%d'%(idx[a],idx[b-1],b-a)))
H=tiles[0][0].shape[0]; W=tiles[0][0].shape[1]
canvas=np.zeros((len(tiles)*(H+4),W))
for i,(t,_) in enumerate(tiles): canvas[i*(H+4):i*(H+4)+H,:]=t
im=Image.fromarray((canvas*255).astype(np.uint8)).resize((W*scale,canvas.shape[0]*scale),Image.LANCZOS)
im.save(out); print('saved',out,im.size)
