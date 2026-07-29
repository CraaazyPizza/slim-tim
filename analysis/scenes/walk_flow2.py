import cv2, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
def raw(f): return cv2.imread(FD%f,cv2.IMREAD_GRAYSCALE)
def prep(f):
    im=raw(f).astype(np.float32)
    m=cv2.GaussianBlur(im,(0,0),41); s=np.sqrt(cv2.GaussianBlur((im-m)**2,(0,0),41))+1.5
    return np.clip((im-m)/s*40+128,0,255).astype(np.uint8)
Y,X=np.mgrid[0:1080,0:1920]
ap=np.zeros((1080,1920),bool); ap[75:1000,365:1575]=True
tc=np.zeros((1080,1920),bool); tc[900:1000,360:1100]=True   # burned-in timecode band
def texmask(f,q=70):
    im=cv2.GaussianBlur(raw(f).astype(np.float32),(0,0),1.5)
    gx=cv2.Sobel(im,cv2.CV_32F,1,0,ksize=5); gy=cv2.Sobel(im,cv2.CV_32F,0,1,ksize=5)
    g=cv2.GaussianBlur(np.hypot(gx,gy),(0,0),9)
    return g>np.percentile(g[ap],q), g
def figmask(f):
    im=raw(f).astype(float)
    m=(im<np.percentile(im[ap],20))&ap&(X>480)&(X<1120)&(Y>330)
    return cv2.dilate(m.astype(np.uint8),np.ones((41,41),np.uint8)).astype(bool)
def fit(a,b,label):
    F=cv2.calcOpticalFlowFarneback(prep(a),prep(b),None,0.5,6,61,5,7,1.5,cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
    u,v=F[...,0],F[...,1]
    tx,g=texmask(a); bg=ap&tx&~figmask(a)&~tc
    P=np.c_[X[bg],Y[bg],np.ones(bg.sum())]; du,dv=u[bg],v[bg]
    keep=np.ones(len(P),bool)
    for _ in range(5):
        cu=np.linalg.lstsq(P[keep],du[keep],rcond=None)[0]; cvv=np.linalg.lstsq(P[keep],dv[keep],rcond=None)[0]
        r=np.hypot(du-P@cu,dv-P@cvv); keep=r<max(1.5,2.5*np.median(r[keep]))
    r=np.hypot(du-P@cu,dv-P@cvv)
    print('%s: n_tex=%d  translation(%.2f,%.2f) zoom %.4f | bg residual med %.2f p90 %.2f p99 %.2f px | mean|flow| %.2f'%(
        label,bg.sum(),cu[2],cvv[2],np.sqrt(abs(np.linalg.det([[1+cu[0],cu[1]],[cvv[0],1+cvv[1]]]))),
        np.median(r),np.percentile(r,90),np.percentile(r,99),np.hypot(du,dv).mean()))
    R=np.full((1080,1920),np.nan); R[bg]=r
    return R,bg,u,v,cu,cvv
pairs=[(1625,1832,'f1625->1832 (full)'),(1625,1730,'f1625->1730'),(1730,1832,'f1730->1832'),
       (1625,1655,'f1625->1655 (30f)'),(1800,1830,'f1800->1830 (30f)')]
outs={}
for a,b,lab in pairs:
    outs[(a,b)]=fit(a,b,lab)
# control: same estimator on a static-camera pair? use two adjacent frames
fit(1700,1703,'f1700->1703 (3f, noise floor)')
R,bg,u,v,cu,cvv=outs[(1625,1832)]
fig,axs=plt.subplots(1,2,figsize=(17,6))
axs[0].imshow(raw(1625),cmap='gray'); axs[0].set_title('f1625')
im=axs[1].imshow(R,cmap='inferno',vmin=0,vmax=15); axs[1].set_title('homography(affine) residual on textured bg, f1625->f1832')
plt.colorbar(im,ax=axs[1])
for ax in axs: ax.set_xlim(350,1590); ax.set_ylim(1010,60)
plt.tight_layout(); plt.savefig('walk_resid_textured.png',dpi=110); plt.close()
