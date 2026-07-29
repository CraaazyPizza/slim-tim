import numpy as np, json
from PIL import Image
D='/home/user/new-skinny-bob/frames/l9RAhmPHM_A'
Y0,Y1=938,1000
PITCH=42.667; X0C=475.5
def cellbox(k):
    c=X0C+PITCH*k
    return int(round(c-16)), int(round(c+16))
DIG=[1,2,4,5,7,8,10,11]
pats={}
frames=list(range(420,4310))
data={}
for i in frames:
    a=np.array(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(np.float32)
    row=[]
    for k in DIG:
        x0,x1=cellbox(k)
        p=a[Y0:Y1,x0:x1]
        lo=np.percentile(p,10); hi=np.percentile(p,97)
        q=np.clip((p-lo)/max(hi-lo,1e-3),0,1)
        row.append(q)
    data[i]=np.stack(row)
np.save('/home/user/new-skinny-bob/analysis/teardown-video3/cells.npy', np.stack([data[i] for i in frames]))
json.dump(frames,open('/home/user/new-skinny-bob/analysis/teardown-video3/cellframes.json','w'))
print('ok',len(frames))
