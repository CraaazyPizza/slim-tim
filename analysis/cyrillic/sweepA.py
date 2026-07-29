"""STAGE A of the typeface sweep: every installed Cyrillic-capable face, coarse grid,
scored on the word «Предыдущее» of the best single frame. Fourier matched filter."""
import numpy as np, sys, json, time
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
ALL=json.load(open('fonts.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
WA='Предыдущее'; RA=(906,996); XA=(438,1120)
o=(-RESL[FR.index(983)])[(RA[0]-Y0):(RA[1]-Y0),(XA[0]-X0):(XA[1]-X0)]
fl=Field(o,*o.shape)
KX=[1.16,1.25,1.34,1.43,1.52]; BL=[0.7,1.4,2.6]; CAPS=[52,55]
t0=time.time(); A=[]
for n,fp in ALL.items():
    best=None
    for cap in CAPS:
        s=capsize(fp,cap); Aa=base_render(fp,WA,s)
        for kx in KX:
            ink=place(Aa,kx,fl.H,fl.W)
            for r,bl,dx,dy in fl.match(ink,BL,dxr=30):
                if best is None or r>best[0]: best=(r,cap,float(kx),bl)
    A.append(dict(font=n,file=fp,r=best[0],cap=best[1],kx=best[2],blur=best[3]))
A.sort(key=lambda d:-d['r']); rr=np.array([d['r'] for d in A])
print('STAGE A  %d faces  %.0fs | field median %.4f sd %.4f'%(len(A),time.time()-t0,np.median(rr),rr.std()))
print('%-40s %7s %6s %5s %5s'%('face','r','cap','kx','blur'))
for d in A[:50]: print('%-40s %7.4f %6.1f %5.2f %5.1f'%(d['font'],d['r'],d['cap'],d['kx'],d['blur']))
json.dump(A,open('sweepA.json','w'),indent=1,ensure_ascii=False)
