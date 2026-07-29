import numpy as np
from PIL import Image
D='frames/Oqw96jCOP7A'; N=2503
res={k:np.zeros(N) for k in ['mean','fd','fdmax','fdn','L','R','T','B','area']}
prev=None
for i in range(1,N+1):
    a=np.asarray(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(float)
    res['mean'][i-1]=a.mean()
    if prev is not None:
        d=np.abs(a-prev)
        res['fd'][i-1]=d.mean(); res['fdmax'][i-1]=d.max(); res['fdn'][i-1]=(d>4).sum()
    prev=a
    # gate detection: threshold relative to frame's own dynamic range
    thr=max(a.max()*0.18, 6.0)
    m=a>thr
    cs=m.sum(0); rs=m.sum(1)
    ci=np.where(cs>m.shape[0]*0.25)[0]; ri=np.where(rs>m.shape[1]*0.25)[0]
    if len(ci)>10 and len(ri)>10:
        res['L'][i-1],res['R'][i-1]=ci[0],ci[-1]; res['T'][i-1],res['B'][i-1]=ri[0],ri[-1]
        res['area'][i-1]=m.sum()
    else:
        res['L'][i-1]=res['R'][i-1]=res['T'][i-1]=res['B'][i-1]=np.nan
np.savez('analysis/teardown-video2/big.npz',**res)
print('done')
