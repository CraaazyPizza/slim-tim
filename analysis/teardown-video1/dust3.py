import numpy as np
from PIL import Image, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
fr=list(range(2150,2330))
# bright flat sky region of pace lap
box=(700,150,1500,600)
S=[]
for f in fr:
    im=Image.open(F.format(f)).convert('L').crop(box)
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(12))).astype(np.float32)
    S.append(a-bg)
S=np.array(S)
mask=S<-9
print('specks per frame (nonzero only):')
cnt=mask.reshape(len(fr),-1).sum(1)
print([ (fr[i],int(c)) for i,c in enumerate(cnt) if c>30][:40])
def runs_at(v):
    out=[];cur=0
    for x in v:
        if x: cur+=1
        else:
            if cur: out.append(cur); cur=0
    if cur: out.append(cur)
    return out
ys,xs=np.where(mask.any(0))
allr=[]
for y,x in zip(ys,xs): allr+=runs_at(mask[:,y,x])
allr=np.array(allr)
print('run-length hist:',np.bincount(allr,minlength=12)[:12],'mean %.2f'%allr.mean())
# locate biggest specks and print their frames + centroid to test motion locking
from scipy import ndimage
lab,n=ndimage.label(mask)
sizes=ndimage.sum(mask,lab,range(1,n+1))
order=np.argsort(-sizes)[:12]
for o in order:
    sl=ndimage.find_objects(lab)[o]
    print('speck size %d  frames %d-%d  y %d-%d x %d-%d'%(sizes[o],fr[sl[0].start],fr[sl[0].stop-1],box[1]+sl[1].start,box[1]+sl[1].stop,box[0]+sl[2].start,box[0]+sl[2].stop))
