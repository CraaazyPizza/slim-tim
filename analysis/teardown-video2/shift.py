import numpy as np
from PIL import Image
D='frames/Oqw96jCOP7A'
def reg(f,box): 
    return np.asarray(Image.open(f'{D}/f{f:05d}.png').convert('L')).astype(float)[box[1]:box[3],box[0]:box[2]]
def pc(a,b):
    w=np.outer(np.hanning(a.shape[0]),np.hanning(a.shape[1]))
    A=np.fft.fft2((a-a.mean())*w); B=np.fft.fft2((b-b.mean())*w)
    R=A*np.conj(B); R/=np.abs(R)+1e-9
    c=np.fft.fftshift(np.fft.ifft2(R).real)
    p=np.unravel_index(np.argmax(c),c.shape); cy,cx=a.shape[0]//2,a.shape[1]//2
    def par(v0,v1,v2): return (v0-v2)/(2*(v0-2*v1+v2)+1e-12)
    dy=par(c[p[0]-1,p[1]],c[p[0],p[1]],c[p[0]+1,p[1]]) if 0<p[0]<c.shape[0]-1 else 0
    dx=par(c[p[0],p[1]-1],c[p[0],p[1]],c[p[0],p[1]+1]) if 0<p[1]<c.shape[1]-1 else 0
    return p[0]+dy-cy, p[1]+dx-cx
BOX=(400,120,1550,960)
def run(lo,hi,label):
    prev=reg(lo,BOX); s=[]
    for f in range(lo+1,hi+1):
        a=reg(f,BOX); s.append((f,)+pc(prev,a)); prev=a
    mag=np.array([np.hypot(dy,dx) for f,dy,dx in s])
    z=(mag<0.05).mean()
    print(f'--- {label} f{lo}-{hi}: {z*100:.1f}% of frame pairs have |global shift| < 0.05 px; median={np.median(mag):.3f}px  max={mag.max():.2f}px')
    nz=[(f,round(dy,2),round(dx,2)) for f,dy,dx in s if np.hypot(dy,dx)>=0.25]
    print('    non-trivial shifts:', nz[:34])
    if len(nz)>1:
        g=np.diff([x[0] for x in nz]); print('    gaps between them:', g.tolist()[:33])
for a,b,l in [(2270,2420,'/25 SlimTim end'),(1630,1830,'/25 Walkabout'),(1445,1610,'/22 Exit'),(1210,1410,'/21 Triage'),(760,960,'/20 Brown')]:
    run(a,b,l)
