import cv2, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
fs=list(range(1621,1836))
st=np.stack([cv2.imread(FD%f,cv2.IMREAD_GRAYSCALE).astype(np.float32) for f in fs])
def norm(a):
    p1,p2=np.percentile(a,[1,99]); return np.clip((a-p1)/(p2-p1),0,1)
lines=[('horizontal y=200 (far terrain/skyline)',('h',200)),
       ('horizontal y=430 (building top / pole)',('h',430)),
       ('horizontal y=700 (building body + figure)',('h',700)),
       ('horizontal y=880 (near ground)',('h',880)),
       ('vertical x=1300 (through building)',('v',1300)),
       ('vertical x=480  (left terrain)',('v',480))]
fig,axs=plt.subplots(len(lines),1,figsize=(15,3.0*len(lines)))
for ax,(lab,(o,k)) in zip(axs,lines):
    K = st[:,k,370:1570] if o=='h' else st[:,80:1000,k]
    ax.imshow(norm(K).T,aspect='auto',cmap='gray',
              extent=[fs[0],fs[-1], (1570 if o=='h' else 1000), (370 if o=='h' else 80)])
    ax.set_title('kymograph — '+lab); ax.set_ylabel('x px' if o=='h' else 'y px')
axs[-1].set_xlabel('frame')
plt.tight_layout(); plt.savefig('walk_kymographs.png',dpi=110); plt.close()

# quantify edge trajectories: strongest gradient location along each line vs frame
print('edge tracking (strongest |d/dx| feature per line):')
for lab,(o,k) in lines:
    K = st[:,k,370:1570] if o=='h' else st[:,80:1000,k]
    Ks=cv2.GaussianBlur(K,(0,0),3)
    g=np.abs(np.diff(Ks,axis=1))
    idx=np.argmax(g,axis=1)
    print('  %-42s  pos %4d..%4d (range %3d px), sd %.1f, median |frame-to-frame step| %.2f px'%(
        lab,idx.min(),idx.max(),idx.max()-idx.min(),idx.std(),np.median(np.abs(np.diff(idx)))))
