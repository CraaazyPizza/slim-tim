from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
def L(f): return np.asarray(Image.open(FD%f).convert('L'),dtype=np.float64)
A0,A1,B0,B1 = 330,1600, 40,1040   # aperture-ish
f0,f1=1625,1832
I0=gaussian_filter(L(f0),1.2); I1=gaussian_filter(L(f1),1.2)
P=48  # half patch
step=60
res=[]
def ncc_track(I0,I1,cx,cy,P,srch):
    T=I0[cy-P:cy+P,cx-P:cx+P]
    if T.std()<2.0: return None
    T0=T-T.mean(); n0=np.sqrt((T0*T0).sum())
    best=(-2,0,0)
    for dy in range(-srch,srch+1,2):
        for dx in range(-srch,srch+1,2):
            y,x=cy+dy,cx+dx
            if y-P<0 or x-P<0 or y+P>1080 or x+P>1920: continue
            W=I1[y-P:y+P,x-P:x+P]; W=W-W.mean()
            d=np.sqrt((W*W).sum())
            if d<1e-6: continue
            v=(T0*W).sum()/(n0*d)
            if v>best[0]: best=(v,dy,dx)
    v,dy,dx=best
    for ddy in range(dy-2,dy+3):
        for ddx in range(dx-2,dx+3):
            y,x=cy+ddy,cx+ddx
            if y-P<0 or x-P<0 or y+P>1080 or x+P>1920: continue
            W=I1[y-P:y+P,x-P:x+P]; W=W-W.mean(); d=np.sqrt((W*W).sum())
            if d<1e-6: continue
            vv=(T0*W).sum()/(n0*d)
            if vv>v: v,dy,dx=vv,ddy,ddx
    return v,dy,dx,T.std()
for cy in range(B0+P,B1-P,step):
    for cx in range(A0+P,A1-P,step):
        r=ncc_track(I0,I1,cx,cy,P,70)
        if r is None: continue
        v,dy,dx,sd=r
        res.append((cx,cy,dx,dy,v,sd))
res=np.array(res)
np.save('walk_track_1625_1832.npy',res)
print('patches',len(res),' good(v>0.8):',(res[:,4]>0.8).sum())
g=res[res[:,4]>0.85]
print('median dx %.1f dy %.1f'%(np.median(g[:,2]),np.median(g[:,3])))
