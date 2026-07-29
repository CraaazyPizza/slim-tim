import sys,os,numpy as np
from PIL import Image
fd=sys.argv[1]; label=sys.argv[2]; f0=int(sys.argv[3]); f1=int(sys.argv[4])
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
def load(i):
    return np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)
# mean frame to locate the matte
acc=None;n=0
for i in range(f0,f1+1,max(1,(f1-f0)//60)):
    a=load(i); acc=a if acc is None else acc+a; n+=1
M=acc/n
H,W=M.shape
print('=== %s frames %d-%d  (%dx%d), mean of %d frames'%(label,f0,f1,W,H,n))
cm=M.mean(0); rm=M.mean(1)
def edges(prof,name):
    g=np.gradient(prof)
    L=int(np.argmax(g[:len(g)//2])); Rr=int(np.argmin(g[len(g)//2:]))+len(g)//2
    return L,Rr
Lx,Rx=edges(cm,'x'); Ty,By=edges(rm,'y')
print('   matte edges from mean frame: x %d..%d (w=%d)   y %d..%d (h=%d)  aspect=%.4f'%(Lx,Rx,Rx-Lx,Ty,By,By-Ty,(Rx-Lx)/(By-Ty)))
# per-frame subpixel edge tracking using the gradient centroid in a window around each edge
def subpix(prof,c,half=14,sign=+1):
    a=max(0,c-half); b=min(len(prof),c+half+1)
    g=np.gradient(prof[a:b])*sign
    g=np.clip(g,0,None)
    if g.sum()<=0: return np.nan
    xs=np.arange(a,b)
    return float((g*xs).sum()/g.sum())
recs=[]
for i in range(f0,f1+1):
    a=load(i)
    cmi=a.mean(0); rmi=a.mean(1)
    recs.append((subpix(cmi,Lx,14,+1),subpix(cmi,Rx,14,-1),subpix(rmi,Ty,14,+1),subpix(rmi,By,14,-1)))
Rr=np.array(recs)
nm=['left','right','top','bottom']
print('   per-frame subpixel matte-edge position over %d frames:'%len(Rr))
for j in range(4):
    v=Rr[:,j]; v=v[~np.isnan(v)]
    print('     %-6s mean=%8.3f  sd=%.4f px  p2p=%.3f px'%(nm[j],v.mean(),v.std(),v.max()-v.min()))
wj=Rr[:,1]-Rr[:,0]; hj=Rr[:,3]-Rr[:,2]
print('     width  mean=%.3f sd=%.4f    height mean=%.3f sd=%.4f'%(np.nanmean(wj),np.nanstd(wj),np.nanmean(hj),np.nanstd(hj)))
cx=(Rr[:,0]+Rr[:,1])/2; cy=(Rr[:,2]+Rr[:,3])/2
print('     centre-x sd=%.4f px   centre-y sd=%.4f px   (this is the gate WEAVE)'%(np.nanstd(cx),np.nanstd(cy)))
np.save('analysis/compare-eras/gate_%s.npy'%label,Rr)
