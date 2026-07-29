import numpy as np
from PIL import Image, ImageFilter
D='frames/Oqw96jCOP7A'
N=2503
# text region full line, and seconds-only region
def hp(a):
    im=Image.fromarray(a)
    b=np.asarray(im.filter(ImageFilter.GaussianBlur(3))).astype(float)
    return a.astype(float)-b
sec=[]; line=[]
for i in range(1,N+1):
    a=np.asarray(Image.open(f'{D}/f{i:05d}.png').convert('L'))
    sec.append(hp(a[920:1005,900:1015]))
    line.append(hp(a[920:1005,500:1015]))
sec=np.array(sec); line=np.array(line)
np.save('analysis/teardown-video2/sec.npy',sec)
ds=np.array([0]+[np.abs(sec[i]-sec[i-1]).mean() for i in range(1,N)])
dl=np.array([0]+[np.abs(line[i]-line[i-1]).mean() for i in range(1,N)])
np.save('analysis/teardown-video2/ds.npy',ds); np.save('analysis/teardown-video2/dl.npy',dl)
for i in range(400,2450):
    if ds[i]>2.0:
        print(i+1, round(ds[i],2), round(dl[i],2))
