import sys,numpy as np
from PIL import Image
pre=sys.argv[1]
B=np.load(pre+'_band.npy'); idx=np.load(pre+'_idx.npy'); runs=np.load(pre+'_runs.npy')
lens=runs[:,1]-runs[:,0]; order=np.argsort(-lens)
# average of many runs, each contrast-normalised -> reveals stable glyph grid
acc=[]
for o in order[:25]:
    a,b=runs[o]; m=B[a:b].mean(0)
    lo,hi=np.percentile(m,1),np.percentile(m,99.7)
    acc.append(np.clip((m-lo)/(hi-lo+1e-9),0,1))
A=np.stack(acc)
mx=A.max(0)   # max over runs: union of all glyphs ever drawn
mn=A.min(0)
cp=mx.mean(0)
print('col profile (x offset from band x0), values*100:')
s=''.join('%3d'%round(v*100) for v in cp)
for i in range(0,len(cp),40):
    print(' x%4d:'%i, ' '.join('%2d'%round(v*100) for v in cp[i:i+40]))
# row profile
rp=mx.mean(1); print('row profile:', ' '.join('%2d'%round(v*100) for v in rp))
Image.fromarray((mx*255).astype(np.uint8)).resize((mx.shape[1]*3,mx.shape[0]*3),Image.LANCZOS).save(pre+'_union.png')
Image.fromarray((mn*255).astype(np.uint8)).resize((mn.shape[1]*3,mn.shape[0]*3),Image.LANCZOS).save(pre+'_inter.png')
print('saved',pre+'_union.png',pre+'_inter.png')
