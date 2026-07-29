import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

norm=np.load('work/xju_norm.npy')
res={}
for tname in ['t55','t64']:
    m=np.load(f'work/xju_mask_{tname}.npy')
    # contour by marching around the boundary
    b = m & ~ndi.binary_erosion(m)
    ys,xs=np.nonzero(b); pts=np.stack([xs,ys],1).astype(float)
    # order the boundary: nearest-neighbour walk
    from scipy.spatial import cKDTree
    tree=cKDTree(pts); n=len(pts)
    order=[0]; used=np.zeros(n,bool); used[0]=True
    cur=0
    for _ in range(n-1):
        d,idx=tree.query(pts[cur],k=12)
        nxt=None
        for dd,ii in zip(d,idx):
            if not used[ii]: nxt=ii; break
        if nxt is None: break
        used[nxt]=True; order.append(nxt); cur=nxt
    C=pts[order]
    # palm reference: centroid of the mask's lower 40%
    ys2,xs2=np.nonzero(m)
    ycut=np.percentile(ys2,60)
    cx=xs2[ys2>ycut].mean(); cy=ys2[ys2>ycut].mean()
    r=np.hypot(C[:,0]-cx, C[:,1]-cy)
    res[tname]=dict(C=C, centre=(cx,cy), r=r, mask=m)
    print(tname,'contour pts',len(C),'palm centre',round(cx,1),round(cy,1))
np.save('work/xju_contour_t64.npy', res['t64']['C'])
np.save('work/xju_contour_t55.npy', res['t55']['C'])
print('centre t64', res['t64']['centre'])
