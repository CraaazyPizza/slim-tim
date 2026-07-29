import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
ALL=json.load(open('fonts.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
ROWS=(902,1002); XS=(430,1615); TXT='Предыдущее сообщение'
def win(fs):
    o=(-RESL[[FR.index(f) for f in fs]].mean(0))[(ROWS[0]-Y0):(ROWS[1]-Y0),(XS[0]-X0):(XS[1]-X0)]
    return Field(o,*o.shape)
fl=win([983]); flb=win([983,973,974,984,981]); fln=win(list(range(1010,1030)))
FACES=['Roboto Medium','Lato Bold','Carlito Bold','Nimbus Sans Bold','Open Sans Semibold',
       'DejaVu Sans Bold','Liberation Sans Bold','Noto Sans Regular','Cantarell Bold','DejaVu Sans Book']
KX=np.round(np.arange(0.95,1.75,0.025),3)
CAPS=[49,51,53,55,57]; BL=[0.4,0.7,1.0,1.4,1.9,2.6,3.5,4.6]
out={}
for nm in FACES:
    fp=ALL[nm]; cur={'kx':[k for k in KX],'f983':[],'best5':[],'null':[]}
    for kx in KX:
        for key,F in (('f983',fl),('best5',flb),('null',fln)):
            b=None
            for cap in CAPS:
                A=base_render(fp,TXT,capsize(fp,cap))
                ink=place(A,kx,F.H,F.W)
                for r,bl,dx,dy in F.match(ink,BL):
                    if b is None or r>b: b=r
            cur[key].append(b)
    out[nm]=cur
    i=int(np.argmax(cur['f983']))
    print('%-24s peak r=%.4f at kx=%.3f  (kx=1.00 -> %.4f, gain x%.1f) | null peak %.4f'
          %(nm,cur['f983'][i],KX[i],cur['f983'][list(KX).index(1.0)] if 1.0 in list(KX) else float('nan'),
            cur['f983'][i]/max(cur['f983'][0],1e-9), max(cur['null'])))
json.dump(out,open('kxcurve.json','w'),indent=1,ensure_ascii=False)
