import numpy as np, os, json
from PIL import Image
D='/home/user/new-skinny-bob/frames/l9RAhmPHM_A'
N=4395
rows=[]
prev=None
for i in range(1,N+1):
    a=np.array(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(np.float32)
    ov=a[930:1005,440:1000]
    m=a.mean(); mx=a.max()
    # gate mask: which pixels are "lit" at all
    lit=(a>12)
    ys,xs=np.where(lit)
    if len(xs)>500:
        bb=(int(xs.min()),int(xs.max()),int(ys.min()),int(ys.max()))
    else: bb=None
    d = float(np.abs(a-prev).mean()) if prev is not None else 0.0
    prev=a
    rows.append(dict(f=i,mean=float(m),mx=float(mx),ovmean=float(ov.mean()),ovmax=float(ov.max()),bb=bb,fd=d))
json.dump(rows,open('/home/user/new-skinny-bob/analysis/teardown-video3/scan.json','w'))
print('done')
