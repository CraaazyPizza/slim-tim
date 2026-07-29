import numpy as np, sys
from PIL import Image, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
box=(890,928,1025,1002)
def enh(f):
    im=Image.open(F.format(f)).convert('L').crop(box)
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(9))).astype(np.float32)
    return a-bg
a,b=int(sys.argv[1]),int(sys.argv[2])
E={f:enh(f) for f in range(a,b+1)}
v=[]
for f in range(a+1,b+1):
    v.append((f,float(np.abs(E[f]-E[f-1]).mean())))
v=np.array(v)
med=np.median(v[:,1])
print('median diff %.3f'%med)
# peaks
cand=[(int(f),round(float(x),2)) for f,x in v if x>3*med]
print(cand)
