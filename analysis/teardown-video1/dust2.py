import numpy as np
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
fr=list(range(950,1040))
S=[]
for f in fr:
    a=np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float32)[150:900,360:1570]
    a=a-np.median(a)     # remove per-frame level
    S.append(a)
S=np.array(S)
med=np.median(S,axis=0)
res=S-med[None]
print('res rms per frame:',np.round(res.reshape(len(fr),-1).std(1),2))
mask=res<-6
print('dark px/frame:',[int(x) for x in mask.reshape(len(fr),-1).sum(1)])
def runs_at(v):
    out=[];cur=0
    for x in v:
        if x: cur+=1
        else:
            if cur: out.append(cur); cur=0
    if cur: out.append(cur)
    return out
ys,xs=np.where(mask.any(0))
print('n pixels ever dark:',len(ys))
allr=[]
for y,x in zip(ys,xs):
    allr+= runs_at(mask[:,y,x])
allr=np.array(allr)
print('run-length hist:',np.bincount(allr,minlength=25)[:25])
print('mean run %.2f, 90th %.0f, max %d'%(allr.mean(),np.percentile(allr,90),allr.max()))
# also: how much of the "median" image has persistent dark marks
print('median-image dark pixels (<-6):',int((med<-6).sum()))
