import numpy as np
from PIL import Image
from scipy import ndimage
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
fr=list(range(950,1040))
S=np.array([np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float32)[120:930,330:1600] for f in fr])
med=np.median(S,axis=0)
print('stack',S.shape,'median range',med.min(),med.max())
# per-frame residual
res=S-med[None]
print('residual rms per frame (min/med/max): %.2f %.2f %.2f'%(res.reshape(len(fr),-1).std(1).min(),np.median(res.reshape(len(fr),-1).std(1)),res.reshape(len(fr),-1).std(1).max()))
# detect dark marks per frame: pixels < med - 8
mask=(res<-7)
print('dark-mark pixel count per frame:')
for i,f in enumerate(fr):
    if i%3==0: print(f,int(mask[i].sum()), end='   ')
print()
# persistence: for each pixel, longest run of mask
def longest_run(v):
    best=cur=0
    for x in v:
        cur=cur+1 if x else 0
        best=max(best,cur)
    return best
# subsample pixels that are ever masked
ys,xs=np.where(mask.any(0))
print('n pixels ever dark:',len(ys))
runs=[]
for y,x in zip(ys[::7],xs[::7]):
    runs.append(longest_run(mask[:,y,x]))
runs=np.array(runs)
print('longest-run histogram (frames):',np.bincount(runs,minlength=20)[:20], 'max',runs.max())
np.save('leader_med.npy',med)
