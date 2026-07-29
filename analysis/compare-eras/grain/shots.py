import numpy as np,sys,glob,os
for f in sorted(glob.glob('thumb_*.npy')):
    k=f[6:-4]
    a=np.load(f)
    d=np.abs(np.diff(a,axis=0)).mean(axis=(1,2))
    lum=a.mean(axis=(1,2))
    cuts=np.where(d>np.percentile(d,50)*4+2)[0]
    # group
    segs=[]; s=0
    for c in list(cuts)+[len(a)-1]:
        if c-s>15: segs.append((s+1,c+1))
        s=c+1
    print('==',k,'n=%d'%len(a),'nsegs',len(segs))
    for (s,e) in segs:
        sub=d[s-1:e-1]
        print('   seg %5d-%5d len %4d  lum %6.2f  meandiff %6.3f  min %6.3f  max %6.3f'%(s,e,e-s,lum[s-1:e].mean(),sub.mean() if len(sub) else -1, sub.min() if len(sub) else -1, sub.max() if len(sub) else -1))
