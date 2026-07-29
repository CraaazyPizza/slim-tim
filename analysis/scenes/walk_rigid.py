import cv2, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
def prep(f):
    im=cv2.imread(FD%f,cv2.IMREAD_GRAYSCALE).astype(np.float32)
    m=cv2.GaussianBlur(im,(0,0),31); s=np.sqrt(cv2.GaussianBlur((im-m)**2,(0,0),31))+1.0
    return np.clip((im-m)/s*40+128,0,255).astype(np.uint8)
regs={'A far terrain top-L':(400,760,100,320),
      'B skyline top-R':(1150,1520,90,250),
      'C building right':(1180,1540,330,860),
      'D ground low-L':(390,640,700,900),
      'E left mid terrain':(390,560,380,690)}
fs=list(range(1621,1836))
I=prep(fs[0]); series={k:[] for k in regs}
for f in fs[1:]:
    J=prep(f)
    F=cv2.calcOpticalFlowFarneback(I,J,None,0.5,5,45,5,7,1.5,cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
    for k,(x0,x1,y0,y1) in regs.items():
        u=F[y0:y1,x0:x1,0]; v=F[y0:y1,x0:x1,1]
        series[k].append((np.median(u),np.median(v)))
    I=J
S={k:np.array(v) for k,v in series.items()}
np.save('walk_rigid_series.npy',np.array([S[k] for k in regs]))
ks=list(regs)
print('per-frame median flow, magnitude summary:')
for k in ks:
    print('  %-22s rms|du|=%.3f rms|dv|=%.3f  cumulative net (%.1f, %.1f) px  cumulative pathlength %.0f px'%(
        k,S[k][:,0].std(),S[k][:,1].std(),S[k][:,0].sum(),S[k][:,1].sum(),np.hypot(S[k][:,0],S[k][:,1]).sum()))
print('\npairwise correlation of the per-frame motion series (u,v jointly):')
import itertools
for a,b in itertools.combinations(ks,2):
    cu=np.corrcoef(S[a][:,0],S[b][:,0])[0,1]; cv_=np.corrcoef(S[a][:,1],S[b][:,1])[0,1]
    ratio=np.std(np.hypot(*S[a].T))/np.std(np.hypot(*S[b].T))
    print('  %-22s vs %-22s  corr_u %.3f  corr_v %.3f   amp ratio %.2f'%(a,b,cu,cv_,ratio))
plt.figure(figsize=(15,8))
for i,ax in enumerate(['u (horizontal)','v (vertical)']):
    plt.subplot(2,1,i+1)
    for k in ks: plt.plot(fs[1:],np.cumsum(S[k][:,i]),label=k,lw=1)
    plt.ylabel('cumulative '+ax+' (px)'); plt.grid(alpha=.3); plt.legend(fontsize=8)
plt.xlabel('frame'); plt.suptitle('Walkabout: cumulative background motion of five widely separated regions (adjacent-frame flow, integrated)')
plt.tight_layout(); plt.savefig('walk_rigidity.png',dpi=110); plt.close()
