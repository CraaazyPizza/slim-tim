import sys,os,numpy as np
from PIL import Image
fd=sys.argv[1]; label=sys.argv[2]; f0=int(sys.argv[3]); f1=int(sys.argv[4])
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
def load(i): return np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)
F=[load(i) for i in range(f0,f1+1)]
MX=np.maximum.reduce(F); H,W=MX.shape
mask=MX>np.percentile(MX,40)
xs=np.nonzero(mask.mean(0)>0.5)[0]; ys=np.nonzero(mask.mean(1)>0.5)[0]
Lx,Rx,Ty,By=xs.min(),xs.max(),ys.min(),ys.max()
r0=Ty+int(0.30*(By-Ty)); r1=Ty+int(0.70*(By-Ty))
c0=Lx+int(0.30*(Rx-Lx)); c1=Lx+int(0.70*(Rx-Lx))
def cross(prof,c,half,rising):
    a=max(0,c-half); b=min(len(prof),c+half+1)
    seg=prof[a:b]
    lo,hi=np.percentile(seg,5),np.percentile(seg,95)
    if hi-lo<3: return np.nan
    t=(lo+hi)/2
    for k in range(1,len(seg)):
        if rising and seg[k-1]<t<=seg[k]:
            return a+k-1+(t-seg[k-1])/(seg[k]-seg[k-1])
        if (not rising) and seg[k-1]>t>=seg[k]:
            return a+k-1+(seg[k-1]-t)/(seg[k-1]-seg[k])
    return np.nan
rec=[]
for f in F:
    hp=f[r0:r1].mean(0); vp=f[:,c0:c1].mean(1)
    rec.append((cross(hp,Lx,22,True),cross(hp,Rx,22,False),cross(vp,Ty,22,True),cross(vp,By,22,False)))
Rr=np.array(rec)
print('=== %s frames %d-%d  picture x %d-%d y %d-%d'%(label,f0,f1,Lx,Rx,Ty,By))
for j,nm in enumerate(['left','right','top','bottom']):
    v=Rr[:,j]; v=v[~np.isnan(v)]
    if len(v)<10: print('   %-6s insufficient (%d)'%(nm,len(v))); continue
    print('   %-6s n=%3d mean=%8.3f  sd=%.4f px  p2p=%.3f'%(nm,len(v),v.mean(),v.std(),v.max()-v.min()))
cx=(Rr[:,0]+Rr[:,1])/2; cy=(Rr[:,2]+Rr[:,3])/2
print('   GATE WEAVE: centre-x sd=%.4f px   centre-y sd=%.4f px'%(np.nanstd(cx),np.nanstd(cy)))
print('   GATE BREATHE: width sd=%.4f px  height sd=%.4f px'%(np.nanstd(Rr[:,1]-Rr[:,0]),np.nanstd(Rr[:,3]-Rr[:,2])))
# phase correlation of consecutive frames, whole frame, integer+subpixel
def pc(a,b):
    A=np.fft.rfft2(a-a.mean()); B=np.fft.rfft2(b-b.mean())
    Rp=A*np.conj(B); m=np.abs(Rp); m[m==0]=1
    c=np.fft.irfft2(Rp/m,s=a.shape)
    k=np.unravel_index(np.argmax(c),c.shape)
    dy=k[0]-(a.shape[0] if k[0]>a.shape[0]//2 else 0); dx=k[1]-(a.shape[1] if k[1]>a.shape[1]//2 else 0)
    return dy,dx,float(c[k])
sh=[pc(F[i],F[i+1]) for i in range(len(F)-1)]
nz=sum(1 for dy,dx,_ in sh if (dy,dx)!=(0,0))
print('   phase-corr consecutive-frame integer shift: %d/%d frames nonzero; shifts=%s'%(nz,len(sh),sorted(set((dy,dx) for dy,dx,_ in sh))[:8]))
