import numpy as np,sys
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
def get(f,box):
    a=np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float32)[box[1]:box[3],box[0]:box[2]]
    return a-a.mean()
def pc(A,B):
    w=np.outer(np.hanning(A.shape[0]),np.hanning(A.shape[1]))
    Fa=np.fft.fft2(A*w); Fb=np.fft.fft2(B*w)
    R=Fa*np.conj(Fb); R/= (np.abs(R)+1e-9)
    r=np.fft.fftshift(np.real(np.fft.ifft2(R)))
    cy,cx=np.array(r.shape)//2
    i,j=np.unravel_index(np.argmax(r),r.shape)
    def sub(a,b,c):
        d=a-2*b+c
        return 0.0 if abs(d)<1e-12 else 0.5*(a-c)/d
    sy=sub(r[i-1,j],r[i,j],r[i+1,j]); sx=sub(r[i,j-1],r[i,j],r[i,j+1])
    return (j+sx-cx),(i+sy-cy),r[i,j]
a,b=int(sys.argv[1]),int(sys.argv[2]); box=eval(sys.argv[3])
prev=get(a,box); tot=[0.0,0.0]
for f in range(a+1,b+1):
    cur=get(f,box)
    dx,dy,pk=pc(cur,prev)
    tot[0]+=dx; tot[1]+=dy
    print('%d  dx %+.3f dy %+.3f  cum %+.2f %+.2f  pk %.3f'%(f,dx,dy,tot[0],tot[1],pk))
    prev=cur
