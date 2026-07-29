import cv2, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
rows=[]
for f in range(1621,1836):
    im=cv2.imread(FD%f,cv2.IMREAD_GRAYSCALE).astype(np.float32)
    roi=im[200:750,500:1100]
    # head = bright dome; use a high percentile threshold inside roi
    thr=np.percentile(roi,97.0)
    m=(roi>thr).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((9,9),np.uint8))
    n,lab,stats,cent=cv2.connectedComponentsWithStats(m)
    if n<2: rows.append((f,np.nan,np.nan,np.nan,np.nan)); continue
    k=1+np.argmax(stats[1:,4])
    x,y,w,h,a=stats[k]
    rows.append((f,x+500,y+200,w,h))
R=np.array(rows,float)
np.save('walk_head_bbox.npy',R)
import numpy.polynomial.polynomial as npp
f=R[:,0]; w=R[:,3]; h=R[:,4]; cx=R[:,1]+w/2; cy=R[:,2]+h/2
def sm(a,k=15):
    return np.convolve(a,np.ones(k)/k,mode='same')
print('head cap width: f1621 %.0f -> f1835 %.0f  (ratio %.3f)'%(sm(w)[8],sm(w)[-9],sm(w)[-9]/sm(w)[8]))
print('head cap centre y: %.0f -> %.0f'%(sm(cy)[8],sm(cy)[-9]))
print('head cap centre x: %.0f -> %.0f'%(sm(cx)[8],sm(cx)[-9]))
plt.figure(figsize=(13,7))
plt.subplot(3,1,1); plt.plot(f,w,'.',ms=2); plt.plot(f,sm(w)); plt.ylabel('head-cap width px'); plt.grid(alpha=.3)
plt.subplot(3,1,2); plt.plot(f,cy,'.',ms=2); plt.plot(f,sm(cy)); plt.ylabel('head cap centre y'); plt.gca().invert_yaxis(); plt.grid(alpha=.3)
plt.subplot(3,1,3); plt.plot(f,cx,'.',ms=2); plt.plot(f,sm(cx)); plt.ylabel('head cap centre x'); plt.xlabel('frame'); plt.grid(alpha=.3)
plt.suptitle('Walkabout: bright head-cap blob metrics, f1621-1835')
plt.tight_layout(); plt.savefig('walk_head_metrics.png',dpi=110); plt.close()
