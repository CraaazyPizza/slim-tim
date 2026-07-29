import numpy as np
from PIL import Image, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
box=(400,180,700,420)
fr=list(range(1310,1560))
S=[]
for f in fr:
    im=Image.open(F.format(f)).convert('L').crop(box)
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(12))).astype(np.float32)
    S.append(a-bg)
S=np.array(S)
print('flatness: hp std overall %.3f  min pixel %.1f  max %.1f'%(S.std(),S.min(),S.max()))
for thr in [-6,-9,-15,-25]:
    m=S<thr
    c=m.reshape(len(fr),-1).sum(1)
    print('thr %d: frames with >20 px: '%thr, [(fr[i],int(x)) for i,x in enumerate(c) if x>20][:25])
m=S<-9
def runs_at(v):
    out=[];cur=0
    for x in v:
        if x: cur+=1
        else:
            if cur: out.append(cur); cur=0
    if cur: out.append(cur)
    return out
ys,xs=np.where(m.any(0))
allr=[]
for y,x in zip(ys,xs): allr+=runs_at(m[:,y,x])
allr=np.array(allr) if len(allr) else np.array([0])
print('n dark px ever:',len(ys),' run hist:',np.bincount(allr,minlength=8)[:8],'mean %.2f'%allr.mean())
