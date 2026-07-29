import numpy as np,sys
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
a,b=int(sys.argv[1]),int(sys.argv[2])
frames=list(range(a,b+1))
S=np.array([np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float64) for f in frames])
T=S.mean(0); gy,gx=np.gradient(T)
H,W=T.shape
yy,xx=np.mgrid[0:H,0:W].astype(np.float64); yy/=H; xx/=W
mx=(np.abs(gx)>np.percentile(np.abs(gx),99.3)) & (np.abs(gx)>3*np.abs(gy))
my=(np.abs(gy)>np.percentile(np.abs(gy),99.3)) & (np.abs(gy)>3*np.abs(gx))
print('mx',mx.sum(),'my',my.sum())
def solve(mask,grad):
    A=np.stack([T[mask],grad[mask],np.ones(mask.sum()),xx[mask],yy[mask]],1)
    out=[]
    for i in range(len(frames)):
        sol,*_=np.linalg.lstsq(A,S[i][mask],rcond=None)
        out.append(sol[1]/sol[0])
    return np.array(out)
dx=solve(mx,gx); dy=solve(my,gy)
print('dx std %.3f range %.3f'%(dx.std(),dx.max()-dx.min()))
print('dy std %.3f range %.3f'%(dy.std(),dy.max()-dy.min()))
for i,f in enumerate(frames):
    if i<45: print('%d dx %+.3f dy %+.3f'%(f,dx[i],dy[i]))
np.save('lk2_%d_%d.npy'%(a,b),np.stack([np.array(frames),dx,dy],1))
