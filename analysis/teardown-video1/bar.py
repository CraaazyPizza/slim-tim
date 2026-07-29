import numpy as np
from PIL import Image, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
out=[]
for f in range(1049,2980):
    im=Image.open(F.format(f)).convert('L')
    a=np.asarray(im).astype(np.float32)
    hp=a-np.asarray(im.filter(ImageFilter.GaussianBlur(6))).astype(np.float32)
    prof=hp[60:1000,500:1300].mean(1)
    i=int(np.argmin(prof))
    out.append((f,float(prof[i]),60+i,float(prof.max())))
np.save('bar.npy',np.array(out))
print('done')
