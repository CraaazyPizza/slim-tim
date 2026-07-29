"""Fit the line-2 prefix «предупреждало об АА» with free geometry; write l2geo.json."""
import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
from fast import _font
ALL=json.load(open('fonts.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
R2=(998,1078); XS=(432,1560)
def win(fs):
    o=(-RESL[[FR.index(f) for f in fs]].mean(0))[(R2[0]-Y0):(R2[1]-Y0),(XS[0]-X0):(XS[1]-X0)]
    return Field(o,*o.shape)
TXT='предупреждало об АА'
FS=[f for f in ['Lato Bold','Carlito Bold','Nimbus Sans Bold','Open Sans Semibold','Roboto Medium',
                'Liberation Sans Bold','DejaVu Sans Bold','Noto Sans Regular','Cantarell Bold','Arimo Bold'] if f in ALL]
CAPS=[40,42,44,46,48,50,52]; KX=np.round(np.arange(1.20,1.60,0.03),2); BL=[0.4,0.7,1.1,1.6,2.3,3.2]
best=None
for tag,fs in [('f983',[983]),('best5',[983,973,974,984,981])]:
    fl=win(fs)
    for fn in FS:
        fp=ALL[fn]
        for cap in CAPS:
            s=capsize(fp,cap); A=base_render(fp,TXT,s)
            for kx in KX:
                ink=place(A,kx,fl.H,fl.W)
                for r,bl,dx,dy in fl.match(ink,BL,dxr=40,dyr=16):
                    if best is None or r>best[0]: best=(r,fn,cap,s,float(kx),bl,dx,dy,tag)
    print('%-7s best so far: r=%.4f %s cap %.0f kx %.2f blur %.1f dx %d dy %d'%(tag,best[0],best[1],best[2],best[4],best[5],best[6],best[7]))
r,fn,cap,size,kx,bl,dx,dy,tag=best
# recover the absolute ink-left and baseline of the fitted template
from PIL import ImageFont
f=_font(ALL[fn],size); b=f.getbbox(TXT)
w=max(2,b[2]-b[0]+8); h=max(2,b[3]-b[1]+8); nw=int(round(w*kx))
Hw=R2[1]-R2[0]; Ww=XS[1]-XS[0]
y0=(Hw-h)//2+dy; x0=(Ww-nw)//2+dx
xleft = XS[0]+x0+4*kx
baseline = R2[0]+y0+(4-b[1])
# where the next glyph cell sits: after the last А
adv = f.getlength(TXT)*kx
inkw = (b[2]-b[0])*kx
cell_x0 = xleft + inkw + 4
cell_x1 = cell_x0 + f.getlength('А')*kx
geo=dict(font=fn,cap=cap,size=size,kx=kx,blur=bl,r=r,xleft=float(xleft),baseline=float(baseline),
         cell_x0=float(cell_x0),cell_x1=float(cell_x1),inkw=float(inkw),src=tag)
json.dump(geo,open('l2geo.json','w'),indent=1,ensure_ascii=False)
print(json.dumps(geo,ensure_ascii=False,indent=1))
