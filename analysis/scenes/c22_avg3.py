from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter, zoom
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
def L(f): return np.asarray(Image.open(FD%f).convert('L'),dtype=np.float64)
x0,x1,y0,y1 = 1000,1600,45,440
ref=1430
full={f:L(f) for f in range(1416,1445)}
def ncc(p,R):
    p=p-p.mean(); return (p*R).sum()/np.sqrt((p*p).sum()*(R*R).sum()+1e-12)
Rf=gaussian_filter(full[ref],1.5)
R=Rf[y0:y1,x0:x1]; R=R-R.mean()
res=[]
for f in sorted(full):
    ab=gaussian_filter(full[f],1.5)
    bv=-2;bs=(0,0)
    for dy in range(-60,61,3):
        for dx in range(-60,61,3):
            if y0+dy<0 or x0+dx<0 or y1+dy>1080 or x1+dx>1920: continue
            v=ncc(ab[y0+dy:y1+dy,x0+dx:x1+dx],R)
            if v>bv: bv=v;bs=(dy,dx)
    # refine
    for dy in range(bs[0]-3,bs[0]+4):
        for dx in range(bs[1]-3,bs[1]+4):
            if y0+dy<0 or x0+dx<0 or y1+dy>1080 or x1+dx>1920: continue
            v=ncc(ab[y0+dy:y1+dy,x0+dx:x1+dx],R)
            if v>bv: bv=v;bs=(dy,dx)
    res.append((f,bs[0],bs[1],bv)); print(f,bs,round(bv,4))
acc=np.zeros((y1-y0,x1-x0));n=0;w=0
for f,dy,dx,v in res:
    if v<0.85: continue
    acc+=full[f][y0+dy:y1+dy,x0+dx:x1+dx]; n+=1
avg=acc/n; print('n used',n)
np.save('c22_head_mc3.npy',avg)
def st(a,lo,hi):
    p1,p2=np.percentile(a,[lo,hi]);return np.clip((a-p1)/(p2-p1),0,1)
for s,(lo,hi) in [('s1',(0.5,99.5)),('s2',(3,97))]:
    im=Image.fromarray((st(avg,lo,hi)*255).astype(np.uint8)); im=im.resize((im.width*2,im.height*2),Image.LANCZOS); im.save(f'c22_head_mc3_{s}.png')
u=avg+1.0*(avg-gaussian_filter(avg,3.0))
im=Image.fromarray((st(u,1,99)*255).astype(np.uint8)); im=im.resize((im.width*2,im.height*2),Image.LANCZOS); im.save('c22_head_mc3_sharp.png')
