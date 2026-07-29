import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from scipy.signal import fftconvolve
FR='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f%05d.png'
def hp2(n):
    a=np.asarray(Image.open(FR%n).convert('L')).astype(np.float32)
    a=a[::2,::2]
    return a-gaussian_filter(a,8)
t=hp2(1043)[478:502, 355:402]   # y 956-1004, x 710-804 at half res
t=t-t.mean()
tn=np.sqrt((t*t).sum())
res=[]
for n in range(1,2999):
    I=hp2(n)
    num=fftconvolve(I, t[::-1,::-1], mode='valid')
    # local norm
    ones=np.ones_like(t)
    s1=fftconvolve(I,ones,mode='valid'); s2=fftconvolve(I*I,ones,mode='valid')
    cnt=t.size
    den=np.sqrt(np.maximum(s2-s1*s1/cnt,1e-6))*tn
    ncc=num/den
    i=np.unravel_index(np.argmax(ncc),ncc.shape)
    res.append((n,float(ncc[i]),int(i[1]*2),int(i[0]*2)))
np.save('tmatch_r.npy',np.array(res))
r=np.array(res)
o=np.argsort(-r[:,1])[:40]
for k in o: print(int(r[k,0]), round(r[k,1],3), int(r[k,2]), int(r[k,3]))
