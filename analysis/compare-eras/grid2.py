import sys,numpy as np
from PIL import Image
pre=sys.argv[1]; NR=int(sys.argv[2]) if len(sys.argv)>2 else 30
B=np.load(pre+'_band.npy'); idx=np.load(pre+'_idx.npy'); runs=np.load(pre+'_runs.npy')
lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
def blur(a,k):
    o=a.astype(np.float64).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))/5.0
    return o
acc=[];names=[]
for o in order[:NR]:
    a,b=runs[o]
    if b-a<4: continue
    m=B[a:b].mean(0)
    hp=m-blur(m,30)              # remove illumination
    sd=hp.std()
    acc.append(hp/ (sd+1e-9)); names.append((idx[a],idx[b-1],b-a))
A=np.stack(acc); print('runs used',len(acc))
mx=A.max(0); mean=A.mean(0)
np.save(pre+'_hpruns.npy',A); np.save(pre+'_hpnames.npy',np.array(names))
def sv(arr,fn,s=4):
    lo,hi=np.percentile(arr,0.5),np.percentile(arr,99.8)
    t=np.clip((arr-lo)/(hi-lo+1e-9),0,1)
    Image.fromarray((t*255).astype(np.uint8)).resize((arr.shape[1]*s,arr.shape[0]*s),Image.LANCZOS).save(fn)
sv(mx,pre+'_union.png'); sv(mean,pre+'_mean.png')
cp=np.clip(mx,0,None).mean(0)
# find glyph cell boundaries: local minima of column profile
print('column profile of union (x from band start):')
for i in range(0,len(cp),40):
    print(' x%4d:'%i,' '.join('%2d'%min(99,round(v*10)) for v in cp[i:i+40]))
