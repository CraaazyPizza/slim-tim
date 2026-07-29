import numpy as np
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
v=[]
for f in range(1,2999):
    a=np.asarray(Image.open(F.format(f)).convert('L').resize((160,90),Image.BILINEAR)).astype(np.float32)
    v.append(a.mean())
v=np.array(v); np.save('luma.npy',v)
