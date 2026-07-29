import sys,os,numpy as np
from PIL import Image
fd=sys.argv[1]; y0,y1,x0,x1=map(int,sys.argv[2:6]); s,e=int(sys.argv[6]),int(sys.argv[7]); out=sys.argv[8]
thr=float(sys.argv[9]) if len(sys.argv)>9 else 0.97
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])[s-1:e]
def blur(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
B=np.empty((len(files),y1-y0,x1-x0),dtype=np.uint8)
for k,f in enumerate(files):
    B[k]=np.asarray(Image.open(os.path.join(fd,f)).convert('L'))[y0:y1,x0:x1]
idx=np.arange(s,s+len(files))
print('band',B.shape,flush=True)
prev=None; cc=np.full(len(files)-1,np.nan,dtype=np.float32)
for k in range(len(files)):
    cur=blur(B[k],2); cur=cur-cur.mean()
    if prev is not None:
        na,nb=float(prev.ravel()@prev.ravel()),float(cur.ravel()@cur.ravel())
        if na>1e-6 and nb>1e-6: cc[k-1]=float(prev.ravel()@cur.ravel())/np.sqrt(na*nb)
    prev=cur
v=cc[~np.isnan(cc)]
print('cc pct',np.percentile(v,[1,5,10,20,50,90]).round(4),flush=True)
n=len(files)
bnd=[0]+[i+1 for i in range(n-1) if (np.isnan(cc[i]) or cc[i]<thr)]+[n]
runs=[(bnd[i],bnd[i+1]) for i in range(len(bnd)-1) if bnd[i+1]-bnd[i]>=3]
lens=np.array([b-a for a,b in runs])
print('nruns',len(runs),'lens',lens[:80].tolist(),flush=True)
if len(lens): print('mean %.2f median %.1f'%(lens.mean(),np.median(lens)))
np.save(out+'_band.npy',B); np.save(out+'_idx.npy',idx); np.save(out+'_runs.npy',np.array(runs)); np.save(out+'_cc.npy',cc)
