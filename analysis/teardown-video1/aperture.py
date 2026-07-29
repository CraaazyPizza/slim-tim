import numpy as np
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
segs={'leader':(950,1040),'s11':(1060,1200),'taxi':(1252,1296),'pace':(1400,1500),'pace2':(2100,2200),'s26':(2506,2540),'color':(2700,2800)}
means={}
for k,(a,b) in segs.items():
    acc=None;n=0
    for f in range(a,b+1):
        x=np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float64)
        acc=x if acc is None else acc+x; n+=1
    means[k]=acc/n
    Image.fromarray(np.clip(means[k],0,255).astype(np.uint8)).save('mean_%s.png'%k)
np.save('means.npy',means,allow_pickle=True)
# find aperture edges: for each mean image, normalise then locate 50% crossing along middle row/col
for k,m in means.items():
    row=m[480:600,:].mean(0); col=m[:,760:1000].mean(1)
    def cross(p,rng,rising):
        lo=np.percentile(p,5); hi=np.percentile(p,95); thr=(lo+hi)/2
        idx=list(rng)
        for i in range(len(idx)-1):
            a1,b1=p[idx[i]],p[idx[i+1]]
            if (rising and a1<thr<=b1) or ((not rising) and a1<thr<=b1):
                return idx[i]+ (thr-a1)/(b1-a1+1e-9)*(idx[i+1]-idx[i])
        return float('nan')
    L=cross(row,range(0,500),True); R=cross(row,range(1919,1400,-1),True)
    T=cross(col,range(0,300),True); B=cross(col,range(1079,800,-1),True)
    print('%-7s L %7.2f  R %7.2f  T %7.2f  B %7.2f   W %7.2f H %7.2f'%(k,L,R,T,B,R-L,B-T))
