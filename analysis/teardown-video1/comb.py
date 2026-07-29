import numpy as np
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
vals=[]
for f in range(1050,2990):
    a=np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float32)[100:1000,300:1600]
    v=np.abs(a[2:,:]-2*a[1:-1,:]+a[:-2,:]).mean()
    h=np.abs(a[:,2:]-2*a[:,1:-1]+a[:,:-2]).mean()
    vals.append((f,v,h,v/(h+1e-6)))
np.save('comb.npy',np.array(vals))
print('done')
