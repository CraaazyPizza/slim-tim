import cv2, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
Y,X=np.mgrid[0:1080,0:1920]
ap=np.zeros((1080,1920),bool); ap[80:995,375:1565]=True
tc=np.zeros((1080,1920),bool); tc[895:1005,355:1125]=True
def L(f): return cv2.imread(FD%f,cv2.IMREAD_GRAYSCALE).astype(np.float32)
def figmask(f):
    im=L(f)
    m=(im<np.percentile(im[ap],20))&ap&(X>480)&(X<1150)&(Y>330)
    m=cv2.morphologyEx(m.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((31,31),np.uint8))
    n,lab,st,cen=cv2.connectedComponentsWithStats(m)
    if n<2: return m.astype(bool)
    k=1+np.argmax(st[1:,4])
    return (lab==k)
D=15
bins=np.arange(0,241,20)
acc=np.zeros(len(bins)-1); accg=np.zeros(len(bins)-1); cnt=np.zeros(len(bins)-1)
for f in range(1625,1816,10):
    a=L(f); b=L(f+D)
    fm=figmask(f)|figmask(f+D)
    dist=cv2.distanceTransform((~fm).astype(np.uint8),cv2.DIST_L2,5)
    g=cv2.GaussianBlur(np.hypot(cv2.Sobel(a,cv2.CV_32F,1,0,5),cv2.Sobel(a,cv2.CV_32F,0,1,5)),(0,0),5)
    ch=np.abs(b-a)
    valid=ap&~fm&~tc&(dist>0)
    for i in range(len(bins)-1):
        m=valid&(dist>=bins[i])&(dist<bins[i+1])
        if m.sum()<200: continue
        acc[i]+=ch[m].sum(); accg[i]+=g[m].sum(); cnt[i]+=m.sum()
mch=acc/np.maximum(cnt,1); mg=accg/np.maximum(cnt,1)
print('distance from figure silhouette (px) | mean |ΔI| over %d frames | mean |grad| | ratio ΔI/grad'%D)
for i in range(len(bins)-1):
    if cnt[i]==0: continue
    print('  %4d-%4d   %7.3f DN   %8.3f   %8.5f   (n=%d)'%(bins[i],bins[i+1],mch[i],mg[i],mch[i]/max(mg[i],1e-6),cnt[i]))
r=mch/np.maximum(mg,1e-6)
ok=cnt>0
print('\nratio near (0-40 px): %.5f ; far (>=120 px): %.5f ; excess %+.1f%%'%(
    r[ok][:2].mean(), r[ok][6:].mean(), 100*(r[ok][:2].mean()/r[ok][6:].mean()-1)))
plt.figure(figsize=(11,4.5))
c=(bins[:-1]+bins[1:])/2
plt.subplot(1,2,1); plt.plot(c[ok],mch[ok],'o-'); plt.xlabel('distance outside figure silhouette (px)'); plt.ylabel('mean |I(f+15)-I(f)| (DN)'); plt.grid(alpha=.3)
plt.subplot(1,2,2); plt.plot(c[ok],r[ok],'o-'); plt.xlabel('distance outside silhouette (px)'); plt.ylabel('change / local gradient'); plt.grid(alpha=.3)
plt.suptitle('Occlusion-halo test: is background change elevated next to the moving figure?')
plt.tight_layout(); plt.savefig('walk_halo.png',dpi=110); plt.close()
