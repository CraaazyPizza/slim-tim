import numpy as np
from lib import *
from scipy.ndimage import gaussian_filter
SEGS={ # (frame list to probe) chosen from content segments
'OpSTlDJWFFI':[930,1100,1330,1650,1850,2200,2450,2700,2850],
'Oqw96jCOP7A':[470,650,800,1250,1500,1700,1900,2150,2350],
'l9RAhmPHM_A':None,
'ZB788PtqQvg':None,'RsQCXN4o4Ps':None,'Xju_CY5ZESA':None,'a6TLGkrfNKI':None}
B=96
for k in V:
    n=nframes(k)
    fl=SEGS.get(k) or [int(n*x) for x in (0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95)]
    rows=[]
    for i in fl:
        a=F(k,i)
        H,W=a.shape
        lo=gaussian_filter(a,3.0)
        for y in range(0,H-B+1,B):
            for x in range(0,W-B+1,B):
                p=lo[y:y+B,x:x+B]
                rows.append((float(p.std()),float(p.mean()),i,y,x))
    rows.sort()
    print('==',k,'n=%d'%n)
    for lab,lo_,hi_ in [('DARK',12,55),('MID',55,100),('BRIGHT',100,255)]:
        sel=[r for r in rows if lo_<=r[1]<hi_][:6]
        for s in sel:
            print('  %-6s struct=%5.2f mean=%6.1f  f%05d  y[%d:%d] x[%d:%d]'%(lab,s[0],s[1],s[2],s[3],s[3]+B,s[4],s[4]+B))
