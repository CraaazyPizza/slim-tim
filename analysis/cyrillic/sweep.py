"""FULL typeface sweep, Fourier matched filter, free cap-height / kx / blur / position."""
import numpy as np, sys, json, time
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
TEXT=L1_TEXT; ROWS=(902,1002); XS=(430,1620)
ALL=json.load(open('fonts.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
ci=[FR.index(f) for f in CAP]
def win(fs):
    o=(-RESL[[FR.index(f) for f in fs]].mean(0))[(ROWS[0]-Y0):(ROWS[1]-Y0),(XS[0]-X0):(XS[1]-X0)]
    return Field(o,*o.shape)
OBS={'f983':win([983]),'best5':win([983,973,974,984,981]),'stack20':win(CAP),
     'NULL_1010_1029':win(list(range(1010,1030))),'NULL_f1020':win([1020])}
KX=np.round(np.arange(1.00,1.62,0.04),2)
BL=[0.4,0.6,0.8,1.1,1.4,1.8,2.3,2.9,3.6,4.4,5.4]
CAPS=[47,49,51,53,55,57,59]
t0=time.time(); res={}
for tag,fl in OBS.items():
    rows=[]
    for name,fp in ALL.items():
        best=None
        for cap in CAPS:
            s=capsize(fp,cap)
            A=base_render(fp,TEXT,s)
            for kx in KX:
                ink=place(A,kx,fl.H,fl.W)
                for r,bl,dx,dy in fl.match(ink,BL):
                    if best is None or r>best[0]: best=(r,cap,s,float(kx),bl,dx,dy)
        rows.append(dict(font=name,file=fp,r=best[0],cap=best[1],size=best[2],kx=best[3],
                         blur=best[4],dx=best[5],dy=best[6]))
    rows.sort(key=lambda d:-d['r']); res[tag]=rows
    rr=np.array([d['r'] for d in rows])
    print('\n===== %s  (%.0fs) =====   field: median r %.4f, sd %.4f'%(tag,time.time()-t0,np.median(rr),rr.std()))
    print('%-40s %7s %4s %5s %5s'%('face','r','cap','kx','blur'))
    for d in rows[:30]: print('%-40s %7.4f %4d %5.2f %5.1f'%(d['font'],d['r'],d['cap'],d['kx'],d['blur']))
    sys.stdout.flush()
json.dump(res,open('sweep.json','w'),indent=1,ensure_ascii=False)
print('\ntotal %.0fs'%(time.time()-t0))
