import cv2, numpy as np, itertools
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
def prep(f):
    im=cv2.imread(FD%f,cv2.IMREAD_GRAYSCALE).astype(np.float64)
    m=cv2.GaussianBlur(im,(0,0),25); s=np.sqrt(cv2.GaussianBlur((im-m)**2,(0,0),25))+0.8
    return (im-m)/s
regs={'A far terrain top-L':(400,780,95,330),
      'B skyline/ridge top-R':(1140,1540,80,270),
      'C building right':(1170,1550,320,870),
      'D ground low-L':(385,660,690,900),
      'E left mid terrain':(385,580,360,700)}
wins={k:cv2.createHanningWindow((v[1]-v[0],v[3]-v[2]),cv2.CV_64F) for k,v in regs.items()}
fs=list(range(1621,1836))
I=prep(fs[0]); S={k:[] for k in regs}; RSP={k:[] for k in regs}
for f in fs[1:]:
    J=prep(f)
    for k,(x0,x1,y0,y1) in regs.items():
        a=np.ascontiguousarray(I[y0:y1,x0:x1]); b=np.ascontiguousarray(J[y0:y1,x0:x1])
        (dx,dy),r=cv2.phaseCorrelate(a,b,wins[k])
        S[k].append((dx,dy)); RSP[k].append(r)
    I=J
S={k:np.array(v) for k,v in S.items()}
np.save('walk_pc_series.npy',np.array([S[k] for k in regs]))
print('adjacent-frame phase correlation, per region:')
for k in regs:
    print('  %-22s mean resp %.3f | per-frame rms (%.3f, %.3f) px | cumulative net (%.1f, %.1f) px'%(
        k,np.mean(RSP[k]),S[k][:,0].std(),S[k][:,1].std(),S[k][:,0].sum(),S[k][:,1].sum()))
print('\npairwise correlation of per-frame displacement series:')
for a,b in itertools.combinations(regs,2):
    print('  %-22s vs %-22s corr_dx %+.3f  corr_dy %+.3f'%(a,b,
        np.corrcoef(S[a][:,0],S[b][:,0])[0,1],np.corrcoef(S[a][:,1],S[b][:,1])[0,1]))
plt.figure(figsize=(15,8))
for i,lab in enumerate(['cumulative dx (px)','cumulative dy (px)']):
    plt.subplot(2,1,i+1)
    for k in regs: plt.plot(fs[1:],np.cumsum(S[k][:,i]),lw=1,label=k)
    plt.ylabel(lab); plt.grid(alpha=.3); plt.legend(fontsize=8)
plt.xlabel('frame'); plt.suptitle('Walkabout background rigidity: integrated adjacent-frame phase correlation, five separated regions')
plt.tight_layout(); plt.savefig('walk_rigidity_pc.png',dpi=110); plt.close()
