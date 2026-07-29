import cv2, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
def raw(f): return cv2.imread(FD%f, cv2.IMREAD_GRAYSCALE)
def prep(f):
    im=raw(f).astype(np.float32)
    m=cv2.GaussianBlur(im,(0,0),41); s=np.sqrt(cv2.GaussianBlur((im-m)**2,(0,0),41))+1.5
    return np.clip((im-m)/s*40+128,0,255).astype(np.uint8)
def flow(a,b):
    return cv2.calcOpticalFlowFarneback(prep(a),prep(b),None,0.5,6,61,5,7,1.5,cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
pairs=[(1625,1695),(1695,1765),(1765,1832),(1625,1832)]
Y,X=np.mgrid[0:1080,0:1920]
ap=np.zeros((1080,1920),bool); ap[70:1010,360:1580]=True
for a,b in pairs:
    F=flow(a,b)
    u,v=F[...,0],F[...,1]
    # figure mask: dark blob near centre. build from raw luma of frame a
    im=raw(a).astype(float)
    fig=(im<np.percentile(im[ap],22))&ap&(X>500)&(X<1050)&(Y>380)
    fig=cv2.dilate(fig.astype(np.uint8),np.ones((25,25),np.uint8)).astype(bool)
    bg=ap&~fig
    # robust affine fit on bg
    pts=np.c_[X[bg],Y[bg],np.ones(bg.sum())]
    du,dv=u[bg],v[bg]
    for it in range(4):
        cu=np.linalg.lstsq(pts,du,rcond=None)[0]; cv_=np.linalg.lstsq(pts,dv,rcond=None)[0]
        ru=du-pts@cu; rv=dv-pts@cv_
        r=np.hypot(ru,rv); keep=r<max(2.0,3*np.median(r))
        pts,du,dv=pts[keep],du[keep],dv[keep]
    A=np.array([[cu[0],cu[1]],[cv_[0],cv_[1]]])
    print(f'--- f{a}->f{b}  ({(b-a)} frames) ---')
    print('  affine gradient matrix (I+A):\n   ', np.round(np.eye(2)+A,5).tolist())
    print('  translation: (%.2f, %.2f) px ; mean |flow| bg = %.2f px'%(cu[2],cv_[2],np.hypot(u[bg],v[bg]).mean()))
    ev=np.linalg.eigvals(np.eye(2)+A)
    print('  scale eigenvalues:',np.round(ev.real,5), ' => zoom %.4f'%np.sqrt(abs(np.linalg.det(np.eye(2)+A))))
    Pall=np.c_[X[ap],Y[ap],np.ones(ap.sum())]
    RU=(u[ap]-Pall@cu); RV=(v[ap]-Pall@cv_)
    R=np.zeros((1080,1920)); R[ap]=np.hypot(RU,RV)
    bgres=np.hypot(u[bg]-np.c_[X[bg],Y[bg],np.ones(bg.sum())]@cu, v[bg]-np.c_[X[bg],Y[bg],np.ones(bg.sum())]@cv_)
    print('  bg residual after affine: median %.2f px, p90 %.2f px'%(np.median(bgres),np.percentile(bgres,90)))
    np.save(f'flow_{a}_{b}.npy',F)
    fig2,axs=plt.subplots(1,3,figsize=(21,5))
    axs[0].imshow(raw(a),cmap='gray'); axs[0].set_title(f'f{a}')
    s=24
    axs[1].imshow(raw(a),cmap='gray')
    axs[1].quiver(X[::s,::s][ap[::s,::s]],Y[::s,::s][ap[::s,::s]],u[::s,::s][ap[::s,::s]],-v[::s,::s][ap[::s,::s]],
                  color='lime',angles='xy',scale_units='xy',scale=0.5,width=0.002)
    axs[1].set_title(f'flow f{a}->f{b} (x2)')
    im3=axs[2].imshow(np.where(ap,R,np.nan),cmap='inferno',vmin=0,vmax=max(3,np.percentile(R[ap],98)))
    axs[2].set_title('residual after global affine (px)'); plt.colorbar(im3,ax=axs[2])
    for ax in axs: ax.set_xlim(340,1600); ax.set_ylim(1030,50)
    plt.tight_layout(); plt.savefig(f'walk_flow_{a}_{b}.png',dpi=100); plt.close()
