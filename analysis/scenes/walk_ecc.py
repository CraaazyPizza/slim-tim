import cv2, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
Y,X=np.mgrid[0:1080,0:1920]
def prep(f):
    im=cv2.imread(FD%f,cv2.IMREAD_GRAYSCALE).astype(np.float32)
    m=cv2.GaussianBlur(im,(0,0),51); s=np.sqrt(cv2.GaussianBlur((im-m)**2,(0,0),51))+1.0
    return ((im-m)/s).astype(np.float32)
base=np.zeros((1080,1920),np.uint8); base[80:990,370:1570]=255
base[900:1000,360:1120]=0     # timecode
def mask_for(f, fx0,fx1,fy0):
    m=base.copy(); m[fy0:,fx0:fx1]=0; return m
crit=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,60,1e-6)
ref=prep(1625)
rows=[]
for f in range(1621,1836,6):
    # exclude a generous figure box that grows with the shot
    t=(f-1621)/214.
    fx0=int(520-60*t); fx1=int(1080+60*t); fy0=int(400-140*t)
    M=mask_for(f,fx0,fx1,fy0)
    W=np.eye(2,3,dtype=np.float32)
    try:
        cc,W=cv2.findTransformECC(ref,prep(f),W,cv2.MOTION_AFFINE,crit,M,5)
    except cv2.error as e:
        rows.append((f,np.nan,np.nan,np.nan,np.nan)); continue
    A=W[:,:2]; t_=W[:,2]
    # displacement of image centre and of scale
    sc=np.sqrt(abs(np.linalg.det(A)))
    c=np.array([975,540]); d=A@c+t_-c
    rows.append((f,cc,d[0],d[1],sc))
R=np.array(rows,float)
np.save('walk_ecc.npy',R)
ok=~np.isnan(R[:,1])
print('ECC frames %d, mean cc %.3f'%(ok.sum(),np.nanmean(R[:,1])))
print('centre displacement dx: %.2f .. %.2f px (sd %.2f)'%(np.nanmin(R[:,2]),np.nanmax(R[:,2]),np.nanstd(R[:,2])))
print('centre displacement dy: %.2f .. %.2f px (sd %.2f)'%(np.nanmin(R[:,3]),np.nanmax(R[:,3]),np.nanstd(R[:,3])))
print('scale: %.4f .. %.4f'%(np.nanmin(R[:,4]),np.nanmax(R[:,4])))
plt.figure(figsize=(13,8))
plt.subplot(3,1,1); plt.plot(R[:,0],R[:,2],label='dx'); plt.plot(R[:,0],R[:,3],label='dy'); plt.legend(); plt.ylabel('bg centre shift px'); plt.grid(alpha=.3)
plt.subplot(3,1,2); plt.plot(R[:,0],R[:,4]); plt.ylabel('bg scale'); plt.grid(alpha=.3)
plt.subplot(3,1,3); plt.plot(R[:,0],R[:,1]); plt.ylabel('ECC correlation'); plt.xlabel('frame'); plt.grid(alpha=.3)
plt.suptitle('Walkabout: ECC affine registration of the BACKGROUND to f1625 (figure masked out)')
plt.tight_layout(); plt.savefig('walk_ecc.png',dpi=110); plt.close()
