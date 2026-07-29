import numpy as np, json
from PIL import Image, ImageFilter
D='frames/Oqw96jCOP7A'; N=2503
def vec(i,box):
    im=Image.open(f'{D}/f{i:05d}.png').convert('L').crop(box)
    a=np.asarray(im).astype(float)
    b=np.asarray(im.filter(ImageFilter.GaussianBlur(6))).astype(float)
    v=(a-b).ravel(); v=v-v.mean(); return v/(np.linalg.norm(v)+1e-9)
SEC=(905,938,1000,990)      # seconds pair
FULL=(500,938,1015,990)     # whole overlay line
V=np.array([vec(i,SEC) for i in range(1,N+1)])
W=np.array([vec(i,FULL) for i in range(1,N+1)])
np.save('analysis/teardown-video2/V.npy',V); np.save('analysis/teardown-video2/W.npy',W)
def seg(M,thr):
    runs=[]; s=1; ref=M[0]
    for i in range(2,N+1):
        c=float(ref@M[i-1])
        if c<thr:
            runs.append((s,i-1)); s=i; ref=M[i-1]
        else:
            ref=0.7*ref+0.3*M[i-1]; ref/=np.linalg.norm(ref)
    runs.append((s,N)); return runs
for name,M,thr in [('SEC',V,0.90),('FULL',W,0.90)]:
    r=seg(M,thr)
    r=[x for x in r if x[1]-x[0]>=2]
    print(f'--- {name} runs (len>=3) ---')
    for a,b in r: print(f'  f{a}-f{b}  len={b-a+1}')
    json.dump(r,open(f'analysis/teardown-video2/runs_{name}.json','w'))
