"""FIG2b refresh (free kx, all candidates incl. the newly installed faces) and
FIG6 (the stem-constrained comparison: every face forced to the kx its own
stroke weight predicts)."""
import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
import fastvar
from c4 import *
from fast import base_render, place, capsize
from figlib import *
from figlib import wrap
from enh import localnorm
from scipy.ndimage import gaussian_filter as gf
from PIL import Image
FIG='/home/user/new-skinny-bob/figs/cyrillic/'
R=json.load(open('sweep3.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
RB=(902,1002); XB=(430,1615); TXT='Предыдущее сообщение'
H=RB[1]-RB[0]; W=XB[1]-XB[0]
def obsw(fs): return (-RESL[[FR.index(f) for f in fs]].mean(0))[(RB[0]-Y0):(RB[1]-Y0),(XB[0]-X0):(XB[1]-X0)]
REAL=obsw([983]); REAL5=obsw([983,973,974,984,981]); CARRIER=obsw([1020])
DEPTH=11.9/255.0; SIG=0.9
def synth(spec,cap,kx,dx=0,dy=0):
    A=base_render(spec,TXT,capsize(spec,cap))
    ink=place(A,kx,H,W)
    ink=np.roll(np.roll(ink,int(dy),axis=0),int(dx),axis=1)
    return CARRIER+gf(ink,SIG)*DEPTH
def strip_of(X,SX,sc):
    a=SX[0]-XB[0]; b=SX[1]-XB[0]
    return up(strip(localnorm(X[:,a:b],45),1.0,99.0),sc)
D={r['font']:r for r in R['best5']}
# ---------------- FIG2b refresh: free kx, close-up on "едыдущ"
SX=(560,1120); SC=2
ORDER=[d['font'] for d in R['best5']][:6]
for m in ['Roboto Medium','PT Sans Bold','Fira Sans Bold','Inter w600 opsz14','Golos Text w500',
          'Rubik w500','Montserrat w575','Nimbus Sans Bold','Arimo Bold','Liberation Sans Bold','Go Bold']:
    if m in D and m not in ORDER: ORDER.append(m)
rows=[('REAL PIXELS — frame 983, one frame',strip_of(REAL,SX,SC),True),
      ('REAL PIXELS — 5-frame average',strip_of(REAL5,SX,SC),True)]
for n in ORDER:
    d=D[n]
    rows.append(('%-24s cap %.0f  kx %.2f (free)   r = %.4f'%(n,d['cap_free'],d['kx_free'],d['r_free']),
                 strip_of(synth(d['spec'],d['cap_free'],d['kx_free']),SX,SC),False))
def build(rows,fn,title,sub,foot):
    PAD=28; LH=40
    Wc=max(im.width for _,im,_ in rows)+2*PAD
    c0=canvas(Wc,10)
    yh=18
    Hc=140+sum(im.height+LH for _,im,_ in rows)+230
    c=canvas(Wc,Hc)
    text(c,(PAD,18),title,size=29)
    y=wrap(c,(PAD,54),sub,Wc-2*PAD,size=18,bold=False,fill=(70,70,70))
    y+=8
    for lab,im,isreal in rows:
        c.paste(im.convert('RGB'),(PAD,y))
        rect(c,(PAD-2,y-2,PAD+im.width+1,y+im.height+1),outline=(170,20,20) if isreal else (200,200,200),w=2 if isreal else 1)
        text(c,(PAD,y+im.height+6),lab,size=23,fill=(170,20,20) if isreal else (20,20,20))
        y+=im.height+LH
    wrap(c,(PAD,y+6),foot,Wc-2*PAD,size=21)
    c=c.crop((0,0,Wc,min(Hc,y+240)))
    c.save(FIG+fn); print(fn,c.size)
build(rows,'FIG2b_typeface_closeup.png',
 'TYPEFACE TEST, close-up on "едыдущ" — now with PT Sans, Fira Sans, Inter, Golos Text, Rubik and Montserrat',
 'PSF held at the independently measured sigma = 0.9 px. Cap height and horizontal stretch kx are free. Same ink depth, same real caption-free noise carrier (f1020), same contrast stretch, 2x Lanczos. 361 faces and variable-font instances were tested; these are the leaders plus the six newly installed faces.',
 'With kx free the field is still degenerate: the leaders span r = 0.68-0.76 across unrelated designs, exactly as before the new fonts were installed. None of the six new faces wins. What breaks the tie is the stroke-weight constraint — see the next figure.')
# ---------------- FIG6: stem-constrained
SX2=(438,1612); SC2=1
ORD2=['Roboto Medium','Inter w600 opsz14','Arimo Bold','Liberation Sans Bold','Nimbus Sans Bold',
      'Go Bold','Carlito Bold','PT Sans Bold','Fira Sans Bold','DejaVu Sans Bold']
rows2=[('REAL PIXELS — frame 983, one frame',strip_of(REAL,SX2,SC2),True),
       ('REAL PIXELS — 5-frame average',strip_of(REAL5,SX2,SC2),True)]
for n in ORD2:
    if n not in D: continue
    d=D[n]
    ok='  <-- PASSES' if d['dkx']<=0.08 else ''
    rows2.append(('%-22s stem/cap %.3f -> kx must be %.2f   r = %.4f%s'%(n,d['sf'],d['kx_pred'],d['r_con'],ok),
                  strip_of(synth(d['spec'],d['cap_con'],d['kx_con']),SX2,SC2),False))
build(rows2,'FIG6_stem_constrained.png',
 'THE STROKE-WEIGHT CONSTRAINT BREAKS THE TIE',
 'The measured stem is 11.6 px at a cap height of 52.5 px, so the stretched stem/cap ratio is 0.2217. The stretch acts on x only: cap height is untouched and stem width is multiplied by kx. So every candidate face PREDICTS its own kx from its own stroke weight, kx = 0.2217 / (its intrinsic stem/cap) — and the image fit then has to work at that kx. No free stretch parameter any more.',
 'Two candidates survive. Roboto Medium keeps its correlation when kx is forced to what its own stroke weight demands (0.740 free -> 0.727 constrained), and Inter at weight 600 does the same at 0.702. Every bold face fails: the Arial, Helvetica, Calibri, PT Sans and Fira Sans bolds need kx = 0.94-1.13 to explain their stems, and at that stretch their text no longer reaches the measured right-hand edge of the ink - visible above - and r collapses to 0.12-0.22, against 0.089 - the best ANY of the 361 candidates reaches on a caption-free frame. Roboto Medium beats Inter by 0.026, which is INSIDE the grid and frame-set jitter of 0.03-0.05, so those two are not separated from each other.')
