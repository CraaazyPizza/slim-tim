from PIL import Image
import numpy as np
from numpy.fft import fft2, ifft2

FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
def L(f): return np.asarray(Image.open(FD%f).convert('L'),dtype=np.float64)

# head ROI in full-frame coords
x0,x1,y0,y1 = 980,1620,45,470
ref=1430
R=L(ref)[y0:y1,x0:x1]
win=np.hanning(R.shape[0])[:,None]*np.hanning(R.shape[1])[None,:]
def pc(a,b):
    A=fft2((a-a.mean())*win); B=fft2((b-b.mean())*win)
    X=A*np.conj(B); X/= (np.abs(X)+1e-9)
    c=np.real(ifft2(X))
    i=np.unravel_index(np.argmax(c),c.shape)
    dy=i[0]-(c.shape[0] if i[0]>c.shape[0]//2 else 0)
    dx=i[1]-(c.shape[1] if i[1]>c.shape[1]//2 else 0)
    return dy,dx,c.max()

frames=list(range(1416,1445))
shifts={}
for f in frames:
    a=L(f)[y0:y1,x0:x1]
    dy,dx,p=pc(a,R)
    shifts[f]=(dy,dx,p)
    print(f,dy,dx,round(p,4))

acc=np.zeros_like(R); n=0
for f in frames:
    dy,dx,p=shifts[f]
    a=L(f)
    yy0,yy1=y0+dy,y1+dy; xx0,xx1=x0+dx,x1+dx
    if yy0<0 or xx0<0 or yy1>a.shape[0] or xx1>a.shape[1]: continue
    acc+=a[yy0:yy1,xx0:xx1]; n+=1
avg=acc/n
print('n',n)
np.save('c22_head_avg.npy',avg)

def stretch(a,lo=0.5,hi=99.5):
    p1,p2=np.percentile(a,[lo,hi])
    return np.clip((a-p1)/(p2-p1),0,1)

for name,arr in [('raw',R),('avg',avg)]:
    for s,(lo,hi) in [('s1',(0.5,99.5)),('s2',(2,98)),('s3',(10,90))]:
        im=Image.fromarray((stretch(arr,lo,hi)*255).astype(np.uint8))
        im=im.resize((im.width*2,im.height*2),Image.LANCZOS)
        im.save(f'c22_head_{name}_{s}.png')
