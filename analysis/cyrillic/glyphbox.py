import sys, numpy as np; sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from pipe import *
def cross(v,c,frac,plateau,rev=False):
    t=frac*plateau
    idx=range(len(v)-1) if not rev else range(len(v)-1,0,-1)
    for i in idx:
        j=i+1 if not rev else i-1
        if (v[i]<t<=v[j]): return c[i]+(t-v[i])/(v[j]-v[i])*(c[j]-c[i])
    return np.nan
def box(X,xr,yr,label):
    sub=X[(yr[0]-Y0):(yr[1]-Y0),(xr[0]-X0):(xr[1]-X0)]
    xs=np.arange(xr[0],xr[1]); ys=np.arange(yr[0],yr[1])
    px=sub.max(0); py=sub.max(1)
    pl=max(px.max(),py.max())
    xl=cross(px,xs,0.5,pl); xh=cross(px,xs,0.5,pl,rev=True)
    yt=cross(py,ys,0.5,pl); yb=cross(py,ys,0.5,pl,rev=True)
    print('  %-5s w %6.2f  h %6.2f  aspect %6.3f   [x %.1f..%.1f  y %.1f..%.1f]'
          %(label,xh-xl,yb-yt,(xh-xl)/(yb-yt),xl,xh,yt,yb))
    return xh-xl, yb-yt
for tag,fs in [('f983',[983]),('best5',BEST5),('stack20',CAP)]:
    X=sig(fs); print('=== %s ==='%tag)
    box(X,(438,516),(908,986),'П')
    box(X,(1166,1230),(928,988),'о(1)')
    box(X,(1228,1292),(928,988),'о(2)')
    box(X,(1112,1168),(928,988),'с')
    box(X,(1286,1348),(908,988),'б')
