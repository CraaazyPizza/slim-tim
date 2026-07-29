import sys,os,numpy as np
from PIL import Image
fd=sys.argv[1]; label=sys.argv[2]
files=sorted([f for f in os.listdir(fd) if f.endswith('.png')])
ms=[]
for i,f in enumerate(files):
    a=np.asarray(Image.open(os.path.join(fd,f)).convert('L'))
    ms.append(a.mean())
ms=np.array(ms)
np.save('analysis/compare-eras/mean_%s.npy'%label,ms)
thr=np.percentile(ms,88)
runs=[];cur=None
for i,v in enumerate(ms):
    if v>thr: cur=[i+1,i+1] if cur is None else [cur[0],i+1]
    else:
        if cur and cur[1]-cur[0]>=8: runs.append(tuple(cur))
        cur=None
if cur and cur[1]-cur[0]>=8: runs.append(tuple(cur))
print('%s: frames=%d meanluma p50=%.1f p88=%.1f max=%.1f'%(label,len(ms),np.percentile(ms,50),thr,ms.max()))
print('   bright runs (>p88, >=8 frames):',runs)
