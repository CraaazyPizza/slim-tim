import numpy as np,sys
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
a,b=int(sys.argv[1]),int(sys.argv[2]); tag=sys.argv[3]
box=eval(sys.argv[4]) if len(sys.argv)>4 else (380,140,1580,980)
step=3
out=[]
prev=None
for f in range(a-1,b+1):
    cur=np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float64)
    if prev is not None:
        T=prev
        gy,gx=np.gradient(T)
        sl=(slice(box[1],box[3],step),slice(box[0],box[2],step))
        A=np.stack([T[sl].ravel(),gx[sl].ravel(),gy[sl].ravel(),np.ones(T[sl].size)],1)
        y=cur[sl].ravel()
        sol,*_=np.linalg.lstsq(A,y,rcond=None)
        r=float(np.sqrt(((y-A@sol)**2).mean()))
        out.append((f,r,sol[1]/sol[0],sol[2]/sol[0]))
    prev=cur
np.save('rep_%s.npy'%tag,np.array(out))
print('done',len(out))
