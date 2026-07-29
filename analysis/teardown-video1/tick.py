import numpy as np, sys
from PIL import Image, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
def enh(f,box):
    im=Image.open(F.format(f)).convert('L').crop(box)
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(9))).astype(np.float32)
    return a-bg
box=(940,925,1020,1005)  # seconds-units digit
a,b=int(sys.argv[1]),int(sys.argv[2])
prev=None
for f in range(a,b+1):
    cur=enh(f,box)
    if prev is not None:
        print(f, round(float(np.abs(cur-prev).mean()),3))
    prev=cur
