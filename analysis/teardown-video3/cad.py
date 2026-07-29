import numpy as np, json, sys
from PIL import Image
D='/home/user/new-skinny-bob/frames/l9RAhmPHM_A'
PITCH=42.667; X0C=475.5; Y0,Y1=938,1000
def cell(a,k):
    c=X0C+PITCH*k; x0=int(round(c-16)); x1=x0+32
    p=a[Y0:Y1,x0:x1]
    lo=np.percentile(p,15); hi=np.percentile(p,97)
    return np.clip((p-lo)/max(hi-lo,1.0),0,1)
def load(i):
    return np.array(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(np.float32)
TR={0:[2257,1777],1:[2302,3727],2:[637,1282],3:[682,2392],4:[727,2437],
    5:[772,2497],6:[997,2557],7:[1657,3697],8:[1687,2857],9:[1732,2242]}
T={}
for d,fs in TR.items():
    T[d]=[cell(load(f),11) for f in fs]
def clas(q):
    best=None;bd=1e9
    for d,ts in T.items():
        for t in ts:
            e=((q-t)**2).mean()
            if e<bd: bd=e;best=d
    return best,bd
out={}
for lo,hi in [(457,805),(1100,1405),(2255,2575),(3125,3705),(3830,4200)]:
    for i in range(lo,hi):
        a=load(i)
        q=cell(a,11); d,e=clas(q)
        out[i]=(d,round(float(e),4))
json.dump(out,open('/home/user/new-skinny-bob/analysis/teardown-video3/cad.json','w'))
print('ok',len(out))
