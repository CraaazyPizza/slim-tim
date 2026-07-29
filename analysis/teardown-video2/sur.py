import numpy as np
from PIL import Image
D='frames/Oqw96jCOP7A'
vals=[]
for i in range(1,2504):
    a=np.asarray(Image.open(f'{D}/f{i:05d}.png').convert('L'))
    vals.append((a[0:40,1750:1900].mean(), a[0:40,1750:1900].std()))
vals=np.array(vals); np.save('analysis/teardown-video2/surround.npy',vals)
prev=None
for i,(m,s) in enumerate(vals,1):
    r=round(float(m),2)
    if r!=prev:
        print(f'frame {i}: surround {r} (std {s:.3f})'); prev=r
