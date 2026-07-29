import numpy as np
from lib import *
from scipy.ndimage import gaussian_filter, grey_closing, grey_opening, label, center_of_mass, maximum_filter
def marks(a, size=9, k=4.0):
    """return (dark_mask, bright_mask, resid) using morphological top-hats on high-passed image"""
    lo=gaussian_filter(a,6.0)
    hp=a-lo
    bh=grey_closing(hp,size=size)-hp      # dark specks positive
    wh=hp-grey_opening(hp,size=size)      # bright specks positive
    s=np.median(np.abs(hp-np.median(hp)))*1.4826+1e-6
    return bh>k*s, wh>k*s, hp, s
FR={'OpSTlDJWFFI':[1650,2200,2450,2700,2850],'Oqw96jCOP7A':[650,800,1250,1500,1900],
'l9RAhmPHM_A':[900,1098,2000,3296,4200],'ZB788PtqQvg':[297,534,772,1009,1128],
'RsQCXN4o4Ps':[675,975,1275,1425],'Xju_CY5ZESA':[389,1428,2208],'a6TLGkrfNKI':[350,1000,1752,1986]}
for k in V:
    y0,y1,x0,x1=PIC[k]
    print('== %s era%d pic y[%d:%d] x[%d:%d]'%(k,ERA[k],y0,y1,x0,x1))
    for f in FR[k]:
        a=F(k,f)[y0:y1,x0:x1]
        dm,wm,hp,s=marks(a)
        nd,_=label(dm); nw,_=label(wm)
        # size distribution
        szd=np.bincount(nd.ravel())[1:]; szw=np.bincount(nw.ravel())[1:]
        print('   f%05d  hp_sigma=%.3f  dark blobs=%4d (med size %s) bright blobs=%4d (med size %s)  maxdark=%.2f maxbright=%.2f'%(
          f,s,len(szd),int(np.median(szd)) if len(szd) else 0,len(szw),int(np.median(szw)) if len(szw) else 0,
          (a-gaussian_filter(a,6.0)).min(),(a-gaussian_filter(a,6.0)).max()))
