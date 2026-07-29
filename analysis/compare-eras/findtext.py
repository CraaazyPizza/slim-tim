import sys, numpy as np
from PIL import Image
p=sys.argv[1]
a=np.asarray(Image.open(p).convert('L')).astype(float)
H,W=a.shape
# bright text on dark: find bounding box of pixels above threshold in bottom region
for y0 in [880]:
    sub=a[y0:,:]
    thr=sub.max()*0.6
    m=sub>thr
    ys,xs=np.nonzero(m)
    if len(ys): print(p,'bbox y',y0+ys.min(),y0+ys.max(),'x',xs.min(),xs.max(),'max',sub.max(),'thr',round(thr,1),'npix',len(ys))
    # row profile
    rp=(sub>thr).sum(1)
    nz=[(y0+i,v) for i,v in enumerate(rp) if v>0]
    print('  rows w/ bright:', nz[:60])
