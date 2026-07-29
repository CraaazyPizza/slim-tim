import numpy as np
from PIL import Image
D='frames/Oqw96jCOP7A'; N=2503
fd=np.zeros(N); prev=None
for i in range(1,N+1):
    a=np.asarray(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(np.int16)
    if prev is not None: fd[i-1]=np.abs(a-prev).mean()
    prev=a
np.save('analysis/teardown-video2/fd.npy',fd)
dups=[i+1 for i in range(1,N) if fd[i]<0.25]
print('strict near-dups:',dups)
