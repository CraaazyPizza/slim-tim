import numpy as np, os, json
from PIL import Image
V={'OpSTlDJWFFI':'/home/user/new-skinny-bob/frames/OpSTlDJWFFI',
'Oqw96jCOP7A':'/home/user/new-skinny-bob/frames/Oqw96jCOP7A',
'l9RAhmPHM_A':'/home/user/new-skinny-bob/frames/l9RAhmPHM_A',
'ZB788PtqQvg':'/home/user/new-skinny-bob/frames/ZB788PtqQvg',
'RsQCXN4o4Ps':'/home/user/new-skinny-bob/frames/RsQCXN4o4Ps',
'Xju_CY5ZESA':'/home/user/new-skinny-bob/frames/Xju_CY5ZESA',
'a6TLGkrfNKI':'/home/user/new-skinny-bob/frames/a6TLGkrfNKI'}
res={}
for k,d in V.items():
    n=len(os.listdir(d))
    idx=np.linspace(1,n,60).astype(int)
    acc=None
    for i in idx:
        a=np.asarray(Image.open(os.path.join(d,'f%05d.png'%i)).convert('L'),dtype=np.float64)
        acc=a if acc is None else acc+a
    m=acc/len(idx)
    np.save('meanmax_%s.npy'%k,m)
    rows=m.mean(1); cols=m.mean(0)
    # find bounding box where profile > 5% of max
    def bounds(p):
        t=p.max()*0.10
        w=np.where(p>t)[0]
        return int(w[0]),int(w[-1])
    r0,r1=bounds(rows); c0,c1=bounds(cols)
    res[k]=dict(n=n,shape=m.shape,rows=[r0,r1],cols=[c0,c1],gmax=float(m.max()),gmean=float(m.mean()))
    print(k,n,m.shape,'rows',r0,r1,'cols',c0,c1,'max %.1f mean %.1f'%(m.max(),m.mean()))
json.dump(res,open('geom.json','w'),indent=1)
