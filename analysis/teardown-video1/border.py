import numpy as np, sys
from PIL import Image
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
a,b=int(sys.argv[1]),int(sys.argv[2])
res=[]
for f in range(a,b+1):
    im=np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float32)
    col=im[300:800,:].mean(0)      # avoid top/bottom
    row=im[:,700:1100].mean(1)
    def edge(p,lo,hi,rising):
        # subpixel crossing of half-max
        thr=(p.min()+p.max())/2
        idx=range(lo,hi) if rising else range(hi,lo,-1)
        prev=None
        for i in idx:
            if prev is not None:
                if (p[prev]<thr<=p[i]):
                    return prev+(thr-p[prev])/(p[i]-p[prev]+1e-9)*(i-prev)
            prev=i
        return float('nan')
    L=edge(col,0,600,True); R=edge(col,1919,1300,False)
    T=edge(row,0,400,True); B=edge(row,1079,700,False)
    res.append((f,L,R,T,B))
arr=np.array(res); np.save('border_%d_%d.npy'%(a,b),arr)
for r in res: print(r[0],*['%.2f'%x for x in r[1:]])
