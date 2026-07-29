import numpy as np
from PIL import Image
from scipy import ndimage as nd
D='frames/Oqw96jCOP7A'
def reg(f): return np.asarray(Image.open(f'{D}/f{f:05d}.png').convert('L')).astype(float)[200:840,500:1140]
def pc(a,b):
    w=np.outer(np.hanning(a.shape[0]),np.hanning(a.shape[1]))
    A=np.fft.fft2((a-a.mean())*w); B=np.fft.fft2((b-b.mean())*w)
    R=A*np.conj(B); R/=np.abs(R)+1e-9
    c=np.fft.fftshift(np.fft.ifft2(R).real)
    p=np.unravel_index(np.argmax(c),c.shape); cy,cx=a.shape[0]//2,a.shape[1]//2
    def par(v0,v1,v2): return (v0-v2)/(2*(v0-2*v1+v2)+1e-12)
    return p[0]+par(c[p[0]-1,p[1]],c[p[0],p[1]],c[p[0]+1,p[1]])-cy, p[1]+par(c[p[0],p[1]-1],c[p[0],p[1]],c[p[0],p[1]+1])-cx
print('CONTROL: known sub-pixel shifts applied to a real frame (f2200)')
a=reg(2200)
for true in [0.0,0.15,0.3,0.5,0.7,1.35,3.4,7.62]:
    dy,dx=pc(a,nd.shift(a,(0,-true),order=3,mode='nearest'))
    print(f'   true dx={true:6.2f}  measured={dx:+7.3f}  err={dx-true:+.3f}')
fr=[]
for lo,hi in [(1445,1610),(1630,1830),(2270,2420)]:
    prev=reg(lo)
    for f in range(lo+1,hi+1):
        cur=reg(f); dy,dx=pc(prev,cur); prev=cur
        for v in (dy,dx):
            if 0.8<=abs(v)<50: fr.append(abs(abs(v)-round(abs(v))))
fr=np.array(fr)
print(f'\nfractional parts of measured shifts: n={len(fr)} mean={fr.mean():.4f} median={np.median(fr):.4f}')
h,_=np.histogram(fr,bins=np.arange(0,0.55,0.05))
print('  |frac| hist 0..0.5 step .05:',h.tolist(),' uniform expectation:',round(len(fr)/10))
