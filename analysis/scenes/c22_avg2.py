from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter, shift as ndshift

FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
def L(f): return np.asarray(Image.open(FD%f).convert('L'),dtype=np.float64)
x0,x1,y0,y1 = 980,1620,45,470
ref=1430
full={f:L(f) for f in range(1416,1445)}
Rb=gaussian_filter(full[ref],1.5)[y0:y1,x0:x1]
Rb=Rb-Rb.mean()
def best(a):
    ab=gaussian_filter(a,1.5)
    bs=None;bv=-2
    for dy in range(-12,13):
        for dx in range(-12,13):
            p=ab[y0+dy:y1+dy, x0+dx:x1+dx]
            p=p-p.mean()
            v=(p*Rb).sum()/np.sqrt((p*p).sum()*(Rb*Rb).sum())
            if v>bv: bv=v; bs=(dy,dx)
    return bs,bv
acc=np.zeros((y1-y0,x1-x0)); n=0
for f in sorted(full):
    (dy,dx),v=best(full[f])
    print(f,dy,dx,round(v,4))
    acc+=full[f][y0+dy:y1+dy, x0+dx:x1+dx]; n+=1
avg=acc/n
np.save('c22_head_avg2.npy',avg)
def stretch(a,lo,hi):
    p1,p2=np.percentile(a,[lo,hi]); return np.clip((a-p1)/(p2-p1),0,1)
for s,(lo,hi) in [('s1',(0.5,99.5)),('s2',(3,97)),('s3',(15,88))]:
    im=Image.fromarray((stretch(avg,lo,hi)*255).astype(np.uint8))
    im=im.resize((im.width*2,im.height*2),Image.LANCZOS); im.save(f'c22_head_mcavg_{s}.png')
# unsharp on avg
u=avg+1.2*(avg-gaussian_filter(avg,3))
im=Image.fromarray((stretch(u,1,99)*255).astype(np.uint8)); im=im.resize((im.width*2,im.height*2),Image.LANCZOS); im.save('c22_head_mcavg_sharp.png')
