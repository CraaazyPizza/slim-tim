import numpy as np
from PIL import Image
from scipy import ndimage as nd
D='frames/Oqw96jCOP7A'; N=2503
K=np.array([[0,-1,0],[-1,4,-1],[0,-1,0]],float)
L=[]
for i in range(1,N+1):
    a=np.asarray(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(float)
    L.append(nd.convolve(a[915:1010,495:1020],K))
L=np.array(L); np.save('analysis/teardown-video2/lap.npy',L)
print(L.shape, np.abs(L).mean())
