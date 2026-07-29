import numpy as np, os, sys
from PIL import Image
from multiprocessing import Pool
V={'OpSTlDJWFFI':'/home/user/new-skinny-bob/frames/OpSTlDJWFFI',
'Oqw96jCOP7A':'/home/user/new-skinny-bob/frames/Oqw96jCOP7A',
'l9RAhmPHM_A':'/home/user/new-skinny-bob/frames/l9RAhmPHM_A',
'ZB788PtqQvg':'/home/user/new-skinny-bob/frames/ZB788PtqQvg',
'RsQCXN4o4Ps':'/home/user/new-skinny-bob/frames/RsQCXN4o4Ps',
'Xju_CY5ZESA':'/home/user/new-skinny-bob/frames/Xju_CY5ZESA',
'a6TLGkrfNKI':'/home/user/new-skinny-bob/frames/a6TLGkrfNKI'}
def load(p):
    im=Image.open(p).convert('L')
    return np.asarray(im.reduce(4),dtype=np.float32)
def job(args):
    d,i=args
    return i,load(os.path.join(d,'f%05d.png'%i))
for k,d in V.items():
    out='thumb_%s.npy'%k
    if os.path.exists(out): print('skip',k); continue
    n=len(os.listdir(d))
    with Pool(12) as p:
        r=p.map(job,[(d,i) for i in range(1,n+1)],chunksize=20)
    r.sort()
    arr=np.stack([x[1] for x in r])
    np.save(out,arr.astype(np.float32))
    print(k,arr.shape,flush=True)
