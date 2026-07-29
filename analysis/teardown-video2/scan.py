import numpy as np, os
from PIL import Image
D='frames/Oqw96jCOP7A'
N=2503
means=np.zeros(N); diffs=np.zeros(N)
prev=None
small=[]
for i in range(1,N+1):
    a=np.asarray(Image.open(f'{D}/f{i:05d}.png').convert('L'))
    s=np.asarray(Image.fromarray(a).resize((96,54)),dtype=float)
    means[i-1]=a.mean()
    if prev is not None: diffs[i-1]=np.abs(s-prev).mean()
    prev=s
    small.append(s.astype(np.uint8))
np.save('analysis/teardown-video2/means.npy',means)
np.save('analysis/teardown-video2/diffs.npy',diffs)
np.save('analysis/teardown-video2/small.npy',np.array(small))
print('done')
cuts=[i+1 for i in range(N) if diffs[i]>12]
print('cuts(frame#):',cuts)
