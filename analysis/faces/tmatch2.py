import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from scipy.signal import fftconvolve
FR='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f%05d.png'
def hp2(n):
    a=np.asarray(Image.open(FR%n).convert('L')).astype(np.float32)[::2,::2]
    return a-gaussian_filter(a,8)
t=hp2(1043)[478:502, 355:402]; t=t-t.mean(); tn=np.sqrt((t*t).sum())
o=np.ones_like(t); cnt=t.size
VARFLOOR = 2.0   # DN^2 per pixel in high-pass
res=[]
for n in range(1,2999):
    I=hp2(n).astype(np.float64)
    num=fftconvolve(I,t[::-1,::-1],'valid')
    s1=fftconvolve(I,o,'valid'); s2=fftconvolve(I*I,o,'valid')
    var=np.maximum(s2-s1*s1/cnt, VARFLOOR*cnt)
    ncc=num/(np.sqrt(var)*tn)
    i=np.unravel_index(np.argmax(ncc),ncc.shape)
    res.append((n,float(ncc[i]),int(i[1]*2),int(i[0]*2)))
r=np.array(res); np.save('tmatch_r2.npy',r)
for k in np.argsort(-r[:,1])[:30]: print(int(r[k,0]), round(r[k,1],3), int(r[k,2]), int(r[k,3]))
