import numpy as np,sys
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
a,b=int(sys.argv[1]),int(sys.argv[2])
frames=list(range(a,b+1))
S=np.array([np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float64) for f in frames])
T=S.mean(0)
gy,gx=np.gradient(T)
# border band: where |grad| is large (the vignette roll-off)
g=np.hypot(gx,gy)
band=g>np.percentile(g,99.0)
print('band px',band.sum())
res=[]
for i,f in enumerate(frames):
    I=S[i]
    # solve for gain k and shift (dx,dy):  I = k*(T + dx*gx + dy*gy)
    A=np.stack([T[band],gx[band],gy[band]],1)
    y=I[band]
    sol,*_=np.linalg.lstsq(A,y,rcond=None)
    k,cx,cy=sol
    res.append((f,k,cx/k,cy/k))
r=np.array(res)
print('gain: mean %.3f std %.3f'%(r[:,1].mean(),r[:,1].std()))
print('dx: std %.3f  range %.3f'%(r[:,2].std(), r[:,2].max()-r[:,2].min()))
print('dy: std %.3f  range %.3f'%(r[:,3].std(), r[:,3].max()-r[:,3].min()))
for f,k,dx,dy in res[:40]: print('%d  gain %.3f dx %+.3f dy %+.3f'%(f,k,dx,dy))
np.save('lk_%d_%d.npy'%(a,b),r)
