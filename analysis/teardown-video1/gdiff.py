import numpy as np
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
prev=None; out=[]
for f in range(1,2999):
    a=np.asarray(Image.open(F.format(f)).convert('L').resize((240,135),Image.BILINEAR)).astype(np.float32)
    if prev is not None:
        out.append((f,float(np.abs(a-prev).mean())))
    prev=a
np.save('gdiff.npy',np.array(out))
print('done',len(out))
