import numpy as np
from PIL import Image, ImageFilter
D='frames/Oqw96jCOP7A'
def blur(f,s=5):
    im=Image.open(f'{D}/f{f:05d}.png').convert('L').filter(ImageFilter.GaussianBlur(s))
    return np.asarray(im).astype(float)[60:1000:2,350:1590:2]
def acf(lo,hi,label):
    prev=blur(lo); v=[]
    for f in range(lo+1,hi+1):
        a=blur(f); v.append(np.abs(a-prev).mean()); prev=a
    v=np.array(v); v=v-v.mean(); n=len(v)
    r=[np.corrcoef(v[:n-l],v[l:])[0,1] for l in range(1,13)]
    best=int(np.argmax(r[1:]))+2
    print(f'{label:32s} '+' '.join(f'{l}:{x:+.2f}' for l,x in zip(range(1,13),r))+f'   PEAK lag={best}')
for a,b,l in [(1990,2100,'/25 SlimTim 40:19-40:22'),(2270,2420,'/25 SlimTim 40:36-40:40'),
              (1630,1830,'/25 Walkabout 02:07-02:12'),(1210,1410,'/21 Triage 15:01-15:06'),
              (1445,1610,'/22 Exit 30:31-31:14'),(760,1000,'/20 Brown 03:12-03:56'),
              (1020,1200,'/20 Brown 04:02-04:11'),(460,700,'/11 TinBird 36:02-36:07'),
              (2424,2458,'TAIL dirt-only')]:
    acf(a,b,l)
