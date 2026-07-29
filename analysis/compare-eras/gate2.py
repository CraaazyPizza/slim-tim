import sys,os,numpy as np
from PIL import Image
fd=sys.argv[1]; label=sys.argv[2]; f0=int(sys.argv[3]); f1=int(sys.argv[4])
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
def load(i): return np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)
step=max(1,(f1-f0)//120)
MX=None
for i in range(f0,f1+1,step):
    a=load(i); MX=a if MX is None else np.maximum(MX,a)
H,W=MX.shape
thr=(MX.max()+MX.min())/2*0.5+np.percentile(MX,55)*0.5
mask=MX>np.percentile(MX,40)
cm=mask.mean(0); rm=mask.mean(1)
xs=np.nonzero(cm>0.5)[0]; ys=np.nonzero(rm>0.5)[0]
print('=== %s frames %d-%d step %d'%(label,f0,f1,step))
if len(xs)==0 or len(ys)==0: print('   no matte found'); sys.exit()
Lx,Rx,Ty,By=xs.min(),xs.max(),ys.min(),ys.max()
print('   picture area (temporal-max mask): x %d..%d (w=%d)  y %d..%d (h=%d)  aspect=%.4f'%(Lx,Rx,Rx-Lx+1,Ty,By,By-Ty+1,(Rx-Lx+1)/(By-Ty+1)))
print('   matte covers %.1f%% of frame area'%(100*(1-((Rx-Lx+1)*(By-Ty+1))/(W*H))))
# corner radius: walk the mask boundary near the top-left corner
sub=mask[Ty:By+1,Lx:Rx+1]
h,w=sub.shape
rad=[]
for name,q in [('TL',sub),('TR',sub[:,::-1]),('BL',sub[::-1,:]),('BR',sub[::-1,::-1])]:
    r=None
    for k in range(1,min(120,h//2,w//2)):
        # if pixel (k,k) inside and (0,0) outside -> radius ~ where diagonal enters
        if q[k,k]: r=k; break
    rad.append((name,r))
print('   corner inset along diagonal (px):',rad)
# radius estimate: for each row near top, find first inside column
prof=[]
for r in range(0,min(90,h)):
    c=np.nonzero(q[r])[0] if False else np.nonzero(sub[r])[0]
    prof.append(int(c.min()) if len(c) else -1)
print('   top-left boundary inset per row (rows 0..%d): %s'%(min(89,h-1),prof[:60]))
np.save('analysis/compare-eras/mask_%s.npy'%label,mask)
Image.fromarray((mask*255).astype(np.uint8)).resize((W//2,H//2)).save('analysis/compare-eras/mask_%s.png'%label)
