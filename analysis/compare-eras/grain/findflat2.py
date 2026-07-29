import numpy as np
from lib import *
from scipy.ndimage import gaussian_filter
PROBE={'OpSTlDJWFFI':[930,1000,1100,1160,1330,1650,1850,2200,2300,2450,2700,2850],
'Oqw96jCOP7A':[470,500,650,800,1250,1300,1500,1700,1900,2150,2350],
'l9RAhmPHM_A':[900,1098,1500,2000,2500,3000,3296,3800,4200],
'ZB788PtqQvg':[178,297,534,600,772,891,1009,1128],
'RsQCXN4o4Ps':[675,825,975,1125,1275,1425],
'a6TLGkrfNKI':[350,700,1000,1400,1752,1986,2200],
'Xju_CY5ZESA':[389,909,1428,1948,2208]}
B=128
for k in V:
    y0,y1,x0,x1=PIC[k]
    rows=[]
    for i in PROBE[k]:
        a=F(k,i); lo=gaussian_filter(a,4.0)
        for y in range(y0,y1-B+1,B//2):
            for x in range(x0,x1-B+1,B//2):
                p=lo[y:y+B,x:x+B]
                rows.append((float(p.std()),float(p.mean()),i,y,x))
    print('==',k)
    for lab,l,h in [('DARK',18,62),('BRIGHT',110,250)]:
        sel=sorted([r for r in rows if l<=r[1]<h])[:4]
        for s in sel: print('  %-6s struct=%5.2f mean=%6.1f f%05d y[%d:%d] x[%d:%d]'%(lab,s[0],s[1],s[2],s[3],s[3]+B,s[4],s[4]+B))
