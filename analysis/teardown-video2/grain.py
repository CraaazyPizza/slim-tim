import numpy as np
from PIL import Image, ImageFilter
D='frames/Oqw96jCOP7A'
BOX=(520,300,1000,900)   # flat bright wall panel, Slim Tim segment
def resid(i):
    im=Image.open(f'{D}/f{i:05d}.png').convert('L').crop(BOX)
    a=np.asarray(im).astype(float)
    b=np.asarray(im.filter(ImageFilter.GaussianBlur(2.5))).astype(float)
    r=(a-b); r-=r.mean(); return r
fr=list(range(2000,2400))
R=np.array([resid(i) for i in fr])
V=R.reshape(len(fr),-1); V/= (np.linalg.norm(V,axis=1,keepdims=True)+1e-9)
print('grain residual std (mean over frames): %.3f'%np.std(R,axis=(1,2)).mean())
C=V@V.T
print('\nautocorrelation of grain residual vs lag (mean over frames):')
for lag in list(range(1,16))+[18,20,24,25,30,36,40,45,48,50,60,72,75,90,96,100,120,144,150,180,200]:
    d=np.array([C[i,i+lag] for i in range(len(fr)-lag)])
    print(f'  lag {lag:4d}: mean r={d.mean():+.4f}  max r={d.max():+.4f}')
np.save('analysis/teardown-video2/C_grain.npy',C)
