import numpy as np, json, sys
from PIL import Image
D='/home/user/new-skinny-bob/frames/l9RAhmPHM_A'
def onset(prof, idxs, plateau, thr=1.2):
    # idxs ordered from inside-matte outward->inward; find first crossing of plateau+thr
    for j in range(len(idxs)-1):
        a0,b0=prof[idxs[j]],prof[idxs[j+1]]
        if a0 < plateau+thr <= b0:
            return idxs[j]+(plateau+thr-a0)/(b0-a0)*(idxs[j+1]-idxs[j])
    return None
res={}
lo,hi=int(sys.argv[1]),int(sys.argv[2])
for i in range(lo,hi):
    a=np.array(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(np.float32)
    rowp=a[380:720,:].mean(axis=0)
    colp=a[:,560:1240].mean(axis=1)
    plL=rowp[150:230].mean(); plR=rowp[1700:1800].mean()
    plT=colp[0:22].mean();    plB=colp[1064:1079].mean()
    L=onset(rowp, list(range(240,340)), plL)
    R=onset(rowp, list(range(1620,1500,-1)), plR)
    T=onset(colp, list(range(24,140)), plT)
    B=onset(colp, list(range(1075,970,-1)), plB)
    res[i]=[None if v is None else round(float(v),3) for v in (L,R,T,B)]+[round(float(plL),3),round(float(plT),3)]
json.dump(res,open(f'/home/user/new-skinny-bob/analysis/teardown-video3/gate2_{lo}.json','w'))
print('ok',lo,hi)
