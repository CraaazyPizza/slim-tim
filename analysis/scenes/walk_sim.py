import cv2, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
S=4  # downsample factor
def prep(f):
    im=cv2.imread(FD%f,cv2.IMREAD_GRAYSCALE).astype(np.float32)
    im=cv2.GaussianBlur(im,(0,0),S/2.0)
    im=cv2.resize(im,(1920//S,1080//S),interpolation=cv2.INTER_AREA)
    m=cv2.GaussianBlur(im,(0,0),12); s=np.sqrt(cv2.GaussianBlur((im-m)**2,(0,0),12))+0.5
    return (im-m)/s
H,W=1080//S,1920//S
Yg,Xg=np.mgrid[0:H,0:W].astype(np.float32)
ref=prep(1621).astype(np.float32)
def mask(f):
    t=(f-1621)/214.
    m=np.zeros((H,W),bool); m[80//S:1000//S,375//S:1565//S]=True
    m[895//S:1005//S,355//S:1125//S]=False       # timecode band
    fx0=int((500-70*t)/S); fx1=int((1100+70*t)/S); fy0=int((390-150*t)/S)
    m[fy0:,fx0:fx1]=False                        # figure
    return m
def score(img,M,dx,dy,sc):
    mx=((Xg-W/2)/sc+W/2+dx).astype(np.float32); my=((Yg-H/2)/sc+H/2+dy).astype(np.float32)
    w=cv2.remap(img.astype(np.float32),mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=float('nan'))
    ok=M&np.isfinite(w)
    a=ref[ok]; b=w[ok]
    if len(a)<500: return -2
    a=a-a.mean(); b=b-b.mean()
    return float((a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum()+1e-9))
rows=[]
for f in range(1621,1836,2):
    img=prep(f).astype(np.float32); M=mask(f)
    best=(-2,0,0,1.0)
    for sc in np.arange(0.94,1.065,0.01):
        for dy in np.arange(-14,14.1,1.0):
            for dx in np.arange(-14,14.1,1.0):
                v=score(img,M,dx,dy,sc)
                if v>best[0]: best=(v,dx,dy,sc)
    v,dx,dy,sc=best
    # refine
    for sc2 in np.arange(sc-0.01,sc+0.011,0.0025):
        for dy2 in np.arange(dy-1,dy+1.01,0.25):
            for dx2 in np.arange(dx-1,dx+1.01,0.25):
                vv=score(img,M,dx2,dy2,sc2)
                if vv>v: v,dx,dy,sc=vv,dx2,dy2,sc2
    rows.append((f,v,dx*S,dy*S,sc))
R=np.array(rows); np.save('walk_sim.npy',R)
print('mean NCC after best similarity: %.3f (min %.3f)'%(R[:,1].mean(),R[:,1].min()))
print('bg dx: %+.1f .. %+.1f px ; dy: %+.1f .. %+.1f px ; scale %.3f .. %.3f'%(
    R[:,2].min(),R[:,2].max(),R[:,3].min(),R[:,3].max(),R[:,4].min(),R[:,4].max()))
print('end-to-end (f1835 vs f1621): dx %+.1f dy %+.1f scale %.3f ncc %.3f'%(R[-1,2],R[-1,3],R[-1,4],R[-1,1]))
plt.figure(figsize=(13,8))
plt.subplot(3,1,1); plt.plot(R[:,0],R[:,2],label='dx'); plt.plot(R[:,0],R[:,3],label='dy'); plt.legend(); plt.ylabel('bg shift (px @1080p)'); plt.grid(alpha=.3)
plt.subplot(3,1,2); plt.plot(R[:,0],R[:,4]); plt.ylabel('bg scale'); plt.grid(alpha=.3)
plt.subplot(3,1,3); plt.plot(R[:,0],R[:,1]); plt.ylabel('NCC to f1621'); plt.xlabel('frame'); plt.grid(alpha=.3)
plt.suptitle('Walkabout background: best global similarity (translation+zoom) vs f1621, figure masked')
plt.tight_layout(); plt.savefig('walk_bg_similarity.png',dpi=110); plt.close()
