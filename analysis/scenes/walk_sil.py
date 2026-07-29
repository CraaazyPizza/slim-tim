import cv2, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
Y,X=np.mgrid[0:1080,0:1920]
ap=np.zeros((1080,1920),bool); ap[80:995,375:1565]=True
rows=[]
for f in range(1621,1836):
    im=cv2.imread(FD%f,cv2.IMREAD_GRAYSCALE).astype(np.float32)
    m=(im<np.percentile(im[ap],20))&ap&(X>460)&(X<1180)&(Y>330)
    m=cv2.morphologyEx(m.astype(np.uint8),cv2.MORPH_CLOSE,np.ones((31,31),np.uint8))
    n,lab,st,cen=cv2.connectedComponentsWithStats(m)
    if n<2: rows.append((f,np.nan,np.nan,np.nan,np.nan)); continue
    k=1+np.argmax(st[1:,4]); x,y,w,h,a=st[k]
    rows.append((f,x,x+w,y,a))
R=np.array(rows,float); np.save('walk_sil.npy',R)
def sm(a,k=21):
    return np.convolve(np.pad(a,(k//2,k//2),mode='edge'),np.ones(k)/k,mode='valid')
L=sm(R[:,1]); Rt=sm(R[:,2]); A=sm(R[:,4])
print('silhouette left  edge: %.0f -> %.0f  (min %.0f)'%(L[0],L[-1],L.min()))
print('silhouette right edge: %.0f -> %.0f  (max %.0f)'%(Rt[0],Rt[-1],Rt.max()))
print('silhouette area: %.0f -> %.0f  (ratio %.2f, sqrt %.2f)'%(A[0],A[-1],A[-1]/A[0],np.sqrt(A[-1]/A[0])))
print('does the silhouette ever retreat, uncovering background?')
print('  left edge moves right by more than 20 px from its running minimum on %d of %d frames'%(
    (L-np.minimum.accumulate(L)>20).sum(),len(L)))
print('  right edge moves left by more than 20 px from its running maximum on %d of %d frames'%(
    (np.maximum.accumulate(Rt)-Rt>20).sum(),len(Rt)))
plt.figure(figsize=(12,5))
plt.plot(R[:,0],L,label='silhouette left edge x'); plt.plot(R[:,0],Rt,label='silhouette right edge x')
plt.plot(R[:,0],np.minimum.accumulate(L),'--',label='running min of left'); plt.plot(R[:,0],np.maximum.accumulate(Rt),'--',label='running max of right')
plt.xlabel('frame'); plt.ylabel('x px'); plt.legend(fontsize=8); plt.grid(alpha=.3)
plt.title('Walkabout: figure silhouette horizontal extent — how much background is uncovered')
plt.tight_layout(); plt.savefig('walk_silhouette.png',dpi=110); plt.close()
