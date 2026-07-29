import cv2, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
def L(f): return cv2.imread(FD%f,cv2.IMREAD_GRAYSCALE).astype(np.float32)
# background sub-windows well away from the figure
wins={'building_R':(1150,1560,300,880),'terrain_TL':(380,700,90,330),'ground_BL':(380,620,760,980),'skyline_T':(700,1150,80,300)}
ref=1625
out={k:[] for k in wins}
for f in range(1621,1836,3):
    for k,(x0,x1,y0,y1) in wins.items():
        a=L(ref)[y0:y1,x0:x1]; b=L(f)[y0:y1,x0:x1]
        (dx,dy),resp=cv2.phaseCorrelate(np.ascontiguousarray(a.astype(np.float64)),
                                        np.ascontiguousarray(b.astype(np.float64)),
                                        cv2.createHanningWindow((x1-x0,y1-y0),cv2.CV_64F))
        out[k].append((f,dx,dy,resp))
plt.figure(figsize=(14,8))
for i,k in enumerate(wins):
    A=np.array(out[k])
    print('%-12s over shot: dx range %+.2f..%+.2f (sd %.2f), dy range %+.2f..%+.2f (sd %.2f), mean resp %.3f'%(
        k,A[:,1].min(),A[:,1].max(),A[:,1].std(),A[:,2].min(),A[:,2].max(),A[:,2].std(),A[:,3].mean()))
    plt.subplot(2,1,1); plt.plot(A[:,0],A[:,1],label=k); plt.ylabel('dx px'); plt.grid(alpha=.3)
    plt.subplot(2,1,2); plt.plot(A[:,0],A[:,2],label=k); plt.ylabel('dy px'); plt.grid(alpha=.3)
plt.subplot(2,1,1); plt.legend(fontsize=8); plt.title('Phase-correlation displacement of four background windows vs f1625')
plt.subplot(2,1,2); plt.xlabel('frame')
plt.tight_layout(); plt.savefig('walk_bg_registration.png',dpi=110); plt.close()
# differential parallax between windows
import itertools
ks=list(wins)
for a,b in itertools.combinations(ks,2):
    A=np.array(out[a]); B=np.array(out[b])
    d=np.hypot(A[:,1]-B[:,1],A[:,2]-B[:,2])
    print('differential motion %s vs %s: median %.2f px, max %.2f px'%(a,b,np.median(d),d.max()))
