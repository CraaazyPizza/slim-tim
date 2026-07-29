import sys,numpy as np
from PIL import Image
def blur(a,k):
    o=a.astype(np.float32).copy()
    for _ in range(k): o=(o+np.roll(o,1,0)+np.roll(o,-1,0)+np.roll(o,1,1)+np.roll(o,-1,1))*np.float32(0.2)
    return o
pre,label,NR=sys.argv[1],sys.argv[2],int(sys.argv[3])
B=np.load(pre+'_band.npy'); idx=np.load(pre+'_idx.npy'); runs=np.load(pre+'_runs.npy')
lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
imgs=[];names=[]
for o in order:
    a,b=runs[o]
    if b-a<8: continue
    m=B[a:b].astype(np.float32).mean(0)
    h=(m-blur(m,20))[4:-4,4:-4]
    if h.std()<1e-6: continue
    imgs.append(h/h.std()); names.append('f%d-%d(n%d)'%(idx[a],idx[b-1],b-a))
    if len(imgs)>=NR: break
A=np.stack(imgs); print(label,'runs used',len(A))
P=np.clip(A,0,None).mean(0)
cp=P.mean(0)
# best pitch by FFT over text region
c=np.nonzero(cp>cp.max()*0.25)[0]; s=cp[c.min():c.max()+1]
n=len(s); w=np.hanning(n); F=np.fft.rfft((s-s.mean())*w); fr=np.fft.rfftfreq(n)
cand=[(i,1/fr[i],abs(F[i])) for i in range(1,len(fr)) if 40<=1/fr[i]<=52]
i,p,_=max(cand,key=lambda t:t[2])
ph=np.angle(F[i])
# cell centers: maxima of cos(2pi x/p - ph)
xs=np.arange(c.min(),c.max()+1)
k0=np.round((ph)/(2*np.pi)*0+0)
centers=[]
x=c.min()+((ph/(2*np.pi))*p)%p
while x< c.max()+p*0.4:
    centers.append(x); x+=p
print('  pitch=%.3f  ncells=%d  centers[0:6]=%s'%(p,len(centers),[round(v,1) for v in centers[:6]]))
np.save(pre+'_A.npy',A); np.save(pre+'_grid.npy',np.array([p]+centers))
open(pre+'_names.txt','w').write('\n'.join(names))
# montage with cell lines
lo,hi=np.percentile(P,0.5),np.percentile(P,99.8)
vis=np.clip((P-lo)/(hi-lo),0,1)
vis3=np.stack([vis]*3,-1)
for cx in centers:
    xi=int(round(cx-p/2))
    if 0<=xi<vis3.shape[1]: vis3[:,xi]=[1,0,0]
Image.fromarray((vis3*255).astype(np.uint8)).resize((vis.shape[1]*5,vis.shape[0]*5),Image.NEAREST).save(pre+'_gridvis.png')
print('  saved',pre+'_gridvis.png')
