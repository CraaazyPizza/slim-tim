import numpy as np
from PIL import Image
D='/home/user/new-skinny-bob/frames/l9RAhmPHM_A'
# Build a per-frame binary glyph map of the overlay strip using top-hat vs local median
X0,X1,Y0,Y1=455,985,938,1000
def strip(i):
    a=np.array(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(np.float32)
    return a[Y0:Y1,X0:X1]
# occupancy map over segment A frames to get glyph mask
acc=np.zeros((Y1-Y0,X1-X0))
n=0
for i in range(440,3720,11):
    s=strip(i)
    thr=np.percentile(s,88)
    acc+= (s>max(thr,120)); n+=1
p=acc/n
np.save('/home/user/new-skinny-bob/analysis/teardown-video3/occ.npy',p)
im=(p/p.max()*255).astype('uint8')
Image.fromarray(im).resize(((X1-X0)*3,(Y1-Y0)*3),Image.NEAREST).save('/home/user/new-skinny-bob/analysis/teardown-video3/occ.png')
col=p.mean(axis=0)
print(' '.join(f'{i+X0}:{v:.2f}' for i,v in enumerate(col) if v>0.02))
