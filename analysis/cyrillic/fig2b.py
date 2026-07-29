import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import base_render, place, capsize
from figlib import *
from figlib import wrap
from enh import localnorm
from scipy.ndimage import gaussian_filter as gf
from PIL import Image
FIG='/home/user/new-skinny-bob/figs/cyrillic/'
ALL=json.load(open('fonts.json')); B=json.load(open('fixpsf.json'))['best5']
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
RB=(902,1002); XB=(430,1615); TXT='Предыдущее сообщение'
H=RB[1]-RB[0]; W=XB[1]-XB[0]
def obsw(fs): return (-RESL[[FR.index(f) for f in fs]].mean(0))[(RB[0]-Y0):(RB[1]-Y0),(XB[0]-X0):(XB[1]-X0)]
REAL=obsw([983]); REAL5=obsw([983,973,974,984,981]); CARRIER=obsw([1020])
DEPTH=11.9/255.0
SX=(560,1120)                    # zoom on "едыдущ" so glyph shape is visible at Reddit size
sx0=SX[0]-XB[0]; sx1=SX[1]-XB[0]
def disp(X,sc=2):
    return up(strip(localnorm(X[:,sx0:sx1],45),1.0,99.0),sc)
def synth(d):
    fp=ALL[d['font']]; A=base_render(fp,TXT,capsize(fp,d['cap']))
    ink=place(A,d['kx'],H,W)
    ink=np.roll(np.roll(ink,int(d['dy']),axis=0),int(d['dx']),axis=1)
    return CARRIER+gf(ink,d['blur'])*DEPTH
rows=[('REAL PIXELS — frame 983, one frame',disp(REAL),True),
      ('REAL PIXELS — 5-frame average',disp(REAL5),True)]
for d in B[:8]:
    rows.append(('%-22s cap %.0f  kx %.2f   r = %.4f'%(d['font'],d['cap'],d['kx'],d['r']),disp(synth(d)),False))
PAD=28; LH=40
Wc=max(im.width for _,im,_ in rows)+2*PAD
Hc=124+sum(im.height+LH for _,im,_ in rows)+190
c=canvas(Wc,Hc)
text(c,(PAD,18),'TYPEFACE TEST, close-up: the letters "едыдущ" of line 1',size=30)
wrap(c,(PAD,54),'PSF held at the INDEPENDENTLY MEASURED value, sigma = 0.9 px, from an edge-spread fit on the leading stem of "П". Only cap height and horizontal stretch are fitted. Same ink depth, same real caption-free noise carrier, same contrast stretch.',Wc-2*PAD,size=18,bold=False,fill=(70,70,70))
y=126
for lab,im,isreal in rows:
    c.paste(im.convert('RGB'),(PAD,y))
    rect(c,(PAD-2,y-2,PAD+im.width+1,y+im.height+1),outline=(170,20,20) if isreal else (200,200,200),w=2 if isreal else 1)
    text(c,(PAD,y+im.height+6),lab,size=24,fill=(170,20,20) if isreal else (20,20,20))
    y+=im.height+LH
wrap(c,(PAD,y+2),'Top five faces span r = 0.732 - 0.765, a 4% spread. Caption-free control frames give r = 0.065 - 0.076 for EVERY face, so the fit is real (about 10x the null) but it does not choose between the faces. Nimbus Sans Bold (Helvetica Bold clone), Arimo Bold (Arial Bold clone), Go Bold and Roboto Medium are statistically interchangeable here.',Wc-2*PAD,size=21)
c.save(FIG+'FIG2b_typeface_closeup.png'); print('FIG2b',c.size)
