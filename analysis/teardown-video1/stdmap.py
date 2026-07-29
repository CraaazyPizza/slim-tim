import numpy as np, sys
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
a,b,st,tag=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
acc=None; acc2=None; n=0
for f in range(a,b+1,st):
    x=np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float64)
    acc=x if acc is None else acc+x
    acc2=x*x if acc2 is None else acc2+x*x
    n+=1
m=acc/n; v=np.sqrt(np.maximum(acc2/n-m*m,0))
np.save('mean_%s.npy'%tag,m); np.save('std_%s.npy'%tag,v)
def sv(arr,fn,lo=None,hi=None):
    lo=arr.min() if lo is None else lo; hi=arr.max() if hi is None else hi
    Image.fromarray(np.clip((arr-lo)/(hi-lo)*255,0,255).astype(np.uint8)).save(fn)
sv(m,'mean_%s.png'%tag,0,255); sv(v,'std_%s.png'%tag,0,40)
print(tag,n,'std range',v.min(),v.max(),'mean of std',v.mean())
# horizontal profile of std in border zone
print('std col profile x=250..380 (y 300..800):', np.round(v[300:800,250:380].mean(0),1))
