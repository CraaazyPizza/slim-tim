import numpy as np,sys
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
a,b=int(sys.argv[1]),int(sys.argv[2])
box=eval(sys.argv[3]) if len(sys.argv)>3 else (360,120,1600,1000)
S={f:np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float64) for f in range(a-1,b+2)}
def resid(f0,f1):
    T=S[f0]; I=S[f1]
    gy,gx=np.gradient(T)
    sl=(slice(box[1],box[3]),slice(box[0],box[2]))
    A=np.stack([T[sl].ravel(),gx[sl].ravel(),gy[sl].ravel(),np.ones(T[sl].size)],1)
    y=I[sl].ravel()
    sol,*_=np.linalg.lstsq(A,y,rcond=None)
    pred=A@sol
    return float(np.sqrt(((y-pred)**2).mean())), sol[1]/sol[0], sol[2]/sol[0]
for f in range(a,b+1):
    r,dx,dy=resid(f-1,f)
    print('%d  rms %6.3f  dx %+.3f dy %+.3f'%(f,r,dx,dy))
