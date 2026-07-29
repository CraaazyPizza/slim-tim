import numpy as np, json
from skimage import measure
from scipy import ndimage as ndi
from PIL import Image, ImageDraw

def analyse(maskfile, tag):
    m=np.load(maskfile)
    cs=measure.find_contours(m.astype(float),0.5)
    C=max(cs,key=len)[:, ::-1]   # (x,y)
    ys,xs=np.nonzero(m); ycut=np.percentile(ys,60)
    cx=xs[ys>ycut].mean(); cy=ys[ys>ycut].mean()
    r=np.hypot(C[:,0]-cx,C[:,1]-cy)
    rs=ndi.uniform_filter1d(r,21,mode='wrap')
    N=len(rs)
    peaks=[]
    for i in range(N):
        w=[rs[(i+k)%N] for k in range(-60,61)]
        if rs[i]>=max(w): peaks.append(i)
    grp=[]
    for i in peaks:
        if grp and (i-grp[-1][-1])<=80: grp[-1].append(i)
        else: grp.append([i])
    if len(grp)>1 and (grp[0][0]+N-grp[-1][-1])<=80:
        grp[0]=grp[-1]+grp[0]; grp.pop()
    cands=[(int(np.mean([g[len(g)//2]])), C[g[len(g)//2]], rs[g[len(g)//2]]) for g in grp]
    cands.sort(key=lambda t:-t[2])
    print(tag,'contour',N,'centre',round(cx,1),round(cy,1))
    for i,p,rr in cands[:8]:
        print('   peak idx',i,'pt',np.round(p,1),'r',round(rr,1))
    return C,(cx,cy),rs,cands,m

C,ctr,rs,cands,m = analyse('work/xju_mask_t64.npy','t64')
np.save('work/xju_C.npy',C); np.save('work/xju_rs.npy',rs)
json.dump({'centre':list(ctr)}, open('work/xju_ctr.json','w'))
