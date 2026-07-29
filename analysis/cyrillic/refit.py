"""Re-run the PSF-fixed typeface fit with the newly installed Russian-market faces."""
import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
ALL=json.load(open('fonts.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
RB=(902,1002); XB=(430,1615); TXT='Предыдущее сообщение'
def field(fs):
    o=(-RESL[[FR.index(f) for f in fs]].mean(0))[(RB[0]-Y0):(RB[1]-Y0),(XB[0]-X0):(XB[1]-X0)]
    return Field(o,*o.shape)
OLD=['Arimo Bold','Roboto Medium','Go Bold','Liberation Sans Bold','Nimbus Sans Bold','DejaVu Sans Bold']
NEW=['PT Sans Bold','Fira Sans Bold','GolosText w625 Regular','Inter w750 Regular',
     'Montserrat w675 Regular','Rubik w575 Regular']
FACES=[f for f in OLD+NEW if f in ALL]
missing=[f for f in OLD+NEW if f not in ALL]
if missing: print("NOT REGISTERED:",missing)
CAPS=[50,52,54,56]; KX=np.round(np.arange(1.12,1.57,0.03),2)
out={}
for tag,fs in [('f983',[983]),('best5',[983,973,974,984,981]),('NULL1',[1020])]:
    fl=field(fs); rows=[]
    for n in FACES:
        fp=ALL[n]; best=None
        for cap in CAPS:
            A=base_render(fp,TXT,capsize(fp,cap))
            for kx in KX:
                ink=place(A,kx,fl.H,fl.W)
                for r,bl,dx,dy in fl.match(ink,[0.9],dxr=40):
                    if best is None or r>best[0]: best=(r,cap,float(kx),int(dx),int(dy))
        rows.append(dict(font=n,r=best[0],cap=best[1],kx=best[2],new=(n in NEW)))
    rows.sort(key=lambda d:-d['r']); out[tag]=rows
    print('\n=== PSF fixed sigma=0.9, %s ==='%tag)
    print('%-26s %7s %5s %5s  %s'%('face','r','cap','kx','')); 
    for d in rows: print('%-26s %7.4f %5.0f %5.2f  %s'%(d['font'],d['r'],d['cap'],d['kx'],'NEW' if d['new'] else ''))
json.dump(out,open('refit.json','w'),indent=1,ensure_ascii=False)
