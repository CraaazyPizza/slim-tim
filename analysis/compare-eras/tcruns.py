import sys, os, numpy as np
from PIL import Image
fd=sys.argv[1]; y0,y1,x0,x1=map(int,sys.argv[2:6]); s,e=int(sys.argv[6]),int(sys.argv[7]); out=sys.argv[8]
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])[s-1:e]
B=[];idx=[]
for k,f in enumerate(files):
    a=np.asarray(Image.open(os.path.join(fd,f)).convert('L'),dtype=np.float32)[y0:y1,x0:x1]
    B.append(a); idx.append(s+k)
B=np.stack(B); idx=np.array(idx)
def blur(a,k=2):
    o=a.copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))/5.0
    return o
Bb=np.stack([blur(b) for b in B]); Bb=Bb-Bb.mean(axis=(1,2),keepdims=True)
sd=Bb.std(axis=(1,2)); live=sd>1e-3
n=len(Bb); cc=np.full(n-1,np.nan)
for i in range(n-1):
    if live[i] and live[i+1]:
        a,b=Bb[i].ravel(),Bb[i+1].ravel(); cc[i]=(a@b)/np.sqrt((a@a)*(b@b))
v=cc[~np.isnan(cc)]
print('band',B.shape,'live',live.sum())
print('cc pct',np.percentile(v,[1,5,10,20,30,50,70,90,99]).round(4))
thr=float(sys.argv[9]) if len(sys.argv)>9 else float(np.percentile(v,25))
bnd=[0]+[i+1 for i in range(n-1) if (np.isnan(cc[i]) or cc[i]<thr)]+[n]
runs=[(bnd[i],bnd[i+1]) for i in range(len(bnd)-1) if bnd[i+1]-bnd[i]>=3 and live[bnd[i]]]
lens=np.array([b-a for a,b in runs])
print('thr',round(thr,4),'nruns',len(runs))
print('lens',lens[:80].tolist())
if len(lens): print('len mean %.2f median %.1f mode-ish'%(lens.mean(),np.median(lens)), np.bincount(lens).argmax())
np.save(out+'_band.npy',B); np.save(out+'_idx.npy',idx)
np.save(out+'_runs.npy',np.array(runs)); np.save(out+'_cc.npy',cc)
