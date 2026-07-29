import sys,os,numpy as np
fd=sys.argv[1]; label=sys.argv[2]; f0=int(sys.argv[3]); f1=int(sys.argv[4])
from PIL import Image
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
def load(i): return np.asarray(Image.open(os.path.join(fd,files[i-1])).convert('L'),dtype=np.float32)
F=[load(i) for i in range(f0,f1+1)]
MX=np.maximum.reduce(F); H,W=MX.shape
mask=MX>np.percentile(MX,40)
xs=np.nonzero(mask.mean(0)>0.5)[0]; ys=np.nonzero(mask.mean(1)>0.5)[0]
Lx,Rx,Ty,By=int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max())
r0,r1=Ty+int(0.25*(By-Ty)),Ty+int(0.75*(By-Ty))
print('=== %s f%d-%d  picture x%d-%d y%d-%d'%(label,f0,f1,Lx,Rx,Ty,By))
# 1D subpixel shift of the LEFT matte edge profile vs the temporal-mean profile
def prof(f): return f[r0:r1, max(0,Lx-30):Lx+30].mean(0)
P=[prof(f) for f in F]
ref=np.mean(P,0); ref=ref-ref.mean()
contrast=[float(np.percentile(p,95)-np.percentile(p,5)) for p in P]
def subshift(a,b,maxs=6):
    a=a-a.mean(); b=b-b.mean()
    best=None
    cc=[]
    for d in range(-maxs,maxs+1):
        bb=np.roll(b,d)
        den=np.sqrt((a*a).sum()*(bb*bb).sum())
        cc.append(float((a*bb).sum()/den) if den>0 else -9)
    k=int(np.argmax(cc))
    if 0<k<len(cc)-1:
        y0,y1,y2=cc[k-1],cc[k],cc[k+1]
        den=(y0-2*y1+y2)
        off=0.5*(y0-y2)/den if den!=0 else 0
    else: off=0
    return (k-maxs)+off, cc[k]
ok=[i for i,c in enumerate(contrast) if c>12]
sh=[subshift(ref,P[i])[0] for i in ok]
if len(sh)>20:
    sh=np.array(sh)
    print('   LEFT MATTE EDGE subpixel shift: n=%d  sd=%.4f px  p2p=%.3f px  (usable frames w/ edge contrast>12)'%(len(sh),sh.std(),sh.max()-sh.min()))
else:
    print('   LEFT MATTE EDGE: only %d frames with usable contrast - INDETERMINATE'%len(sh))
# interior-only subpixel phase correlation between consecutive frames
pad=40
def interior(f):
    g=f[Ty+pad:By-pad, Lx+pad:Rx-pad].astype(np.float64)
    g=g-g.mean()
    wy=np.hanning(g.shape[0])[:,None]; wx=np.hanning(g.shape[1])[None,:]
    return g*wy*wx
def pcsub(a,b):
    A=np.fft.rfft2(a); B=np.fft.rfft2(b)
    Rp=A*np.conj(B); m=np.abs(Rp); m[m==0]=1
    c=np.fft.irfft2(Rp/m,s=a.shape)
    k=np.unravel_index(np.argmax(c),c.shape)
    def par(v0,v1,v2):
        den=v0-2*v1+v2
        return 0.5*(v0-v2)/den if den!=0 else 0.0
    y,x=k
    yp=par(c[(y-1)%c.shape[0],x],c[y,x],c[(y+1)%c.shape[0],x])
    xp=par(c[y,(x-1)%c.shape[1]],c[y,x],c[y,(x+1)%c.shape[1]])
    dy=y-(c.shape[0] if y>c.shape[0]//2 else 0)+yp
    dx=x-(c.shape[1] if x>c.shape[1]//2 else 0)+xp
    return dy,dx,float(c[k])
I=[interior(f) for f in F]
d=[pcsub(I[i],I[i+1]) for i in range(len(I)-1)]
dy=np.array([t[0] for t in d]); dx=np.array([t[1] for t in d]); pk=np.array([t[2] for t in d])
sel=(np.abs(dy)<8)&(np.abs(dx)<8)
print('   INTERIOR content frame-to-frame subpixel shift: n=%d/%d  dx sd=%.4f px  dy sd=%.4f px  |dx|med=%.4f |dy|med=%.4f  peak med=%.3f'%(
    sel.sum(),len(dy),dx[sel].std(),dy[sel].std(),np.median(np.abs(dx[sel])),np.median(np.abs(dy[sel])),np.median(pk)))
# cumulative drift of interior (integrated) -> is there wander?
cum_x=np.cumsum(np.where(sel,dx,0)); cum_y=np.cumsum(np.where(sel,dy,0))
print('   INTERIOR cumulative wander over %d frames: x range %.2f px, y range %.2f px'%(len(dx),cum_x.max()-cum_x.min(),cum_y.max()-cum_y.min()))
