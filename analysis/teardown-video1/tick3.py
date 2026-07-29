import numpy as np, sys
from PIL import Image, ImageFilter
from numpy.fft import fft2, ifft2
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
BIG=(300,915,1060,1010)     # whole overlay strip for alignment
def load(f):
    im=Image.open(F.format(f)).convert('L')
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(6))).astype(np.float32)
    return a-bg
def align_shift(A,B,R=6):
    # brute force integer shift maximizing ncc on strip
    h,w=A.shape; best=(-2,0,0)
    Ac=A[R:h-R,R:w-R]; Ac=Ac-Ac.mean(); an=np.sqrt((Ac*Ac).sum())
    for dy in range(-R,R+1):
        for dx in range(-R,R+1):
            P=B[R+dy:h-R+dy,R+dx:w-R+dx]; P=P-P.mean()
            v=float((Ac*P).sum()/(an*np.sqrt((P*P).sum())+1e-9))
            if v>best[0]: best=(v,dy,dx)
    return best[1],best[2]
a,b=int(sys.argv[1]),int(sys.argv[2])
DIG=(930,928,1040,1006)
E={}
for f in range(a,b+1):
    E[f]=load(f)
ref=E[a][BIG[1]:BIG[3],BIG[0]:BIG[2]]
out=[]
prevpatch=None
for f in range(a,b+1):
    dy,dx=align_shift(ref,E[f][BIG[1]-6:BIG[3]+6,BIG[0]-6:BIG[2]+6][6:-6+0 or None,:][0:ref.shape[0],0:ref.shape[1]]) if False else (0,0)
    out.append(f)
# simpler: align each frame to previous using the big strip via brute force on the strip itself
res=[]
prev=None
for f in range(a,b+1):
    cur=E[f]
    if prev is not None:
        A=prev[BIG[1]:BIG[3],BIG[0]:BIG[2]]
        Bfull=cur
        # find shift minimizing diff on the strip
        best=(1e18,0,0)
        for dy in range(-4,5):
            for dx in range(-4,5):
                P=Bfull[BIG[1]+dy:BIG[3]+dy,BIG[0]+dx:BIG[2]+dx]
                v=float(np.abs(A-P).mean())
                if v<best[0]: best=(v,dy,dx)
        _,dy,dx=best
        Ad=prev[DIG[1]:DIG[3],DIG[0]:DIG[2]]
        Bd=cur[DIG[1]+dy:DIG[3]+dy,DIG[0]+dx:DIG[2]+dx]
        res.append((f,float(np.abs(Ad-Bd).mean()),dy,dx))
    prev=cur
arr=np.array([(r[0],r[1]) for r in res])
np.save('tick3_%d_%d.npy'%(a,b),arr)
for f,v,dy,dx in res: print(f,'%.3f  dy%+d dx%+d'%(v,dy,dx))
