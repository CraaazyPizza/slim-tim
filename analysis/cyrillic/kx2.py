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
fl=field([983]); fn_=field(list(range(1010,1030)))
FACES=['Arimo Bold','Roboto Medium','Carlito Bold','DejaVu Sans Bold','Lato Bold']
KX=np.round(np.arange(0.95,1.66,0.03),2); BL=[1.0,1.8,2.8,4.0]; CAPS=[52,54]
out={'kx':[float(k) for k in KX]}
for n in FACES:
    fp=ALL[n]; ys=[]; yn=[]
    for kx in KX:
        b=-1; bn=-1
        for cap in CAPS:
            A=base_render(fp,TXT,capsize(fp,cap))
            ink=place(A,kx,fl.H,fl.W)
            b=max(b,max(x[0] for x in fl.match(ink,BL,dxr=40)))
            bn=max(bn,max(x[0] for x in fn_.match(ink,BL,dxr=40)))
        ys.append(b); yn.append(bn)
    out[n]={'f983':ys,'null':yn}
    i=int(np.argmax(ys))
    print('%-20s peak r %.4f at kx %.2f | r at kx=1.00 %.4f | null peak %.4f'%(n,ys[i],KX[i],ys[list(KX).index(1.01) if 1.01 in list(KX) else 2],max(yn)))
json.dump(out,open('kx2.json','w'),indent=1,ensure_ascii=False)
