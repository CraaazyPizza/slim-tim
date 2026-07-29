import numpy as np, json
from lib import *
from scipy.ndimage import gaussian_filter
PROBE={'OpSTlDJWFFI':[930,1100,1330,1650,2000,2200,2450,2700,2850],
'Oqw96jCOP7A':[470,650,800,1250,1500,1700,1900,2150,2350],
'l9RAhmPHM_A':[900,1098,1700,2500,3000,3296,3800,4200],
'ZB788PtqQvg':[178,297,534,700,772,891,1009,1128],
'RsQCXN4o4Ps':[600,675,825,975,1125,1275,1425],
'a6TLGkrfNKI':[350,700,1000,1400,1752,1986,2200],
'Xju_CY5ZESA':[389,909,1428,1948,2208]}
out={}
for k in V:
    y0,y1,x0,x1=PIC[k]
    b=256 if (y1-y0)>=256 and (x1-x0)>=256 else 128
    rows=[]
    for i in PROBE[k]:
        a=F(k,i)
        lo=gaussian_filter(a,6.0); hfa=a-gaussian_filter(a,2.0)
        for y in range(y0,y1-b+1,64):
            for x in range(x0,x1-b+1,64):
                p=lo[y:y+b,x:x+b]
                rows.append((float(p.std()),float(p.mean()),float(hfa[y:y+b,x:x+b].std()),i,y,x))
    out[k]=dict(b=b,rows=[])
    print('== %s (patch %d)'%(k,b),flush=True)
    for lab,l,h in [('DARK',16,60),('BRIGHT',105,255)]:
        sel=sorted([r for r in rows if l<=r[1]<h])[:5]
        for s in sel:
            print('  %-6s struct=%5.2f mean=%6.1f hf=%5.3f  f%05d y[%d:%d] x[%d:%d]'%(lab,s[0],s[1],s[2],s[3],s[4],s[4]+b,s[5],s[5]+b))
            out[k]['rows'].append(dict(lab=lab,struct=s[0],mean=s[1],hf=s[2],f=s[3],y=s[4],x=s[5]))
json.dump(out,open('patches.json','w'),indent=1)
