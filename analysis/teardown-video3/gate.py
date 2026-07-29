import numpy as np, json
from PIL import Image
D='/home/user/new-skinny-bob/frames/l9RAhmPHM_A'
res={}
for i in range(457,4262):
    a=np.array(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(np.float32)
    # matte = flat value in [26,31]
    m=((a>=26)&(a<=31))
    colf=m[200:900,:].mean(axis=0)   # fraction matte per column
    rowf=m[:,400:1400].mean(axis=1)
    def edge(prof, rng, rising):
        # find subpixel crossing of 0.5
        idx=list(rng)
        for j in range(len(idx)-1):
            a0,b0=prof[idx[j]],prof[idx[j+1]]
            if rising and a0<0.5<=b0: return idx[j]+(0.5-a0)/(b0-a0)
            if (not rising) and a0>=0.5>b0: return idx[j]+(a0-0.5)/(a0-b0)
        return None
    L=edge(colf,range(400,100,-1),False)  # scanning leftwards from inside: matte frac goes 0->1
    R=edge(colf,range(1300,1900),True)
    T=edge(rowf,range(300,0,-1),False)
    B=edge(rowf,range(800,1080),True)
    res[i]=(L,R,T,B)
json.dump(res,open('/home/user/new-skinny-bob/analysis/teardown-video3/gate.json','w'))
print('ok')
