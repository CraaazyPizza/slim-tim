import numpy as np
from lib import *
from scipy.ndimage import gaussian_filter
PROBE={'OpSTlDJWFFI':[930,1100,1330,1650,1850,2200,2450,2700,2850],
'Oqw96jCOP7A':[470,650,800,1250,1500,1700,1900,2150,2350],
'l9RAhmPHM_A':[900,1098,1500,2000,2500,3000,3296,3800,4200],
'ZB788PtqQvg':[178,297,534,600,772,891,1009,1128],
'RsQCXN4o4Ps':[675,825,975,1125,1275,1425],
'a6TLGkrfNKI':[350,700,1000,1400,1752,1986,2200],
'Xju_CY5ZESA':[389,909,1428,1948,2208]}
edges=np.array([0,15,25,35,50,70,90,110,140,175,210,256])
print('noise std (high-pass sigma=2.0) vs local luminance, picture area only')
print('%-12s'%'video'+''.join('%8s'%('%d-%d'%(edges[i],edges[i+1])) for i in range(len(edges)-1)))
for k in V:
    y0,y1,x0,x1=PIC[k]
    num=np.zeros(len(edges)-1); den=np.zeros(len(edges)-1)
    for i in PROBE[k]:
        a=F(k,i)[y0:y1,x0:x1]
        lo=gaussian_filter(a,2.0); n=a-lo
        # exclude near strong edges
        g=np.abs(gaussian_filter(a,1.0,order=(0,1)))+np.abs(gaussian_filter(a,1.0,order=(1,0)))
        m=g<np.percentile(g,40)
        b=np.digitize(lo[m],edges)-1
        v=n[m]**2
        for j in range(len(edges)-1):
            s=b==j
            if s.sum()>500: num[j]+=v[s].sum(); den[j]+=s.sum()
    out=np.where(den>0,np.sqrt(num/np.maximum(den,1)),np.nan)
    print('%-12s'%k+''.join(('%8.3f'%o if np.isfinite(o) else '%8s'%'-') for o in out), ' era',ERA[k])
