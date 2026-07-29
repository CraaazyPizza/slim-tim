from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
sh={1416:(-28,-49),1417:(-32,-47),1418:(-37,-47),1419:(-23,-26),1420:(-29,-32),1421:(-36,-37),1422:(-37,-29),1423:(-38,-25),1424:(-37,-25),1425:(-26,2),1426:(-22,-6),1427:(-22,-6),1428:(-15,-16),1429:(-6,-22),1430:(0,0),1431:(4,-7),1432:(5,-12),1433:(1,-12),1434:(-4,-16),1435:(-8,-24),1436:(-18,-35),1437:(-25,-47),1438:(-28,-58),1439:(-28,-58),1440:(-26,-75),1441:(-23,-73),1442:(-23,-72),1443:(-21,-67),1444:(-19,-62)}
# mouth ROI in ref(f1430) coords
mx0,mx1,my0,my1=1240,1440,205,300
rows=[]
for f in sorted(sh):
    dy,dx=sh[f]
    a=np.asarray(Image.open(FD%f).convert('L'),dtype=float)
    p=a[my0+dy:my1+dy, mx0+dx:mx1+dx]
    # darkest horizontal band = mouth line; measure its thickness & row
    prof=p.mean(1)
    prof=(prof-prof.min())/(prof.max()-prof.min()+1e-9)
    i=np.argmin(prof)
    w=(prof<0.35).sum()
    rows.append((f,i,w,p.mean(),p.std()))
R=np.array(rows,float)
print('mouth-line row (px, in ROI):',R[:,1].astype(int).tolist())
print('dark-band thickness (px):   ',R[:,2].astype(int).tolist())
print('thickness: mean %.1f sd %.1f min %d max %d'%(R[:,2].mean(),R[:,2].std(),R[:,2].min(),R[:,2].max()))
plt.figure(figsize=(11,5))
plt.subplot(2,1,1); plt.plot(R[:,0],R[:,2],'o-'); plt.ylabel('dark mouth-band thickness (px)'); plt.grid(alpha=.3)
plt.subplot(2,1,2); plt.plot(R[:,0],R[:,1],'o-'); plt.ylabel('mouth-line row'); plt.xlabel('frame'); plt.grid(alpha=.3)
plt.suptitle('Case 22 bearded head: mouth-aperture metrics, f1416-1444 (motion-compensated ROI)')
plt.tight_layout(); plt.savefig('c22_mouth_metrics.png',dpi=110); plt.close()
