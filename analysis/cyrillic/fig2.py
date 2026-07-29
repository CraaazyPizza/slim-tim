import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import base_render, place, capsize
from figlib import *
from enh import localnorm
from scipy.ndimage import gaussian_filter as gf
from PIL import Image
FIG='/home/user/new-skinny-bob/figs/cyrillic/'
ALL=json.load(open('fonts.json')); B=json.load(open('sweepB2.json'))['best5']
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
RB=(902,1002); XB=(430,1615); TXT='Предыдущее сообщение'
H=RB[1]-RB[0]; W=XB[1]-XB[0]
def obsw(fs): return (-RESL[[FR.index(f) for f in fs]].mean(0))[(RB[0]-Y0):(RB[1]-Y0),(XB[0]-X0):(XB[1]-X0)]
REAL=obsw([983]); REAL5=obsw([983,973,974,984,981]); CARRIER=obsw([1020])
DEPTH=11.9/255.0
SHOWX=(438,1612); sx0=SHOWX[0]-XB[0]; sx1=SHOWX[1]-XB[0]
def disp(X,sc=1):
    return up(strip(localnorm(X[:,sx0:sx1],45),1.0,99.0),sc)
def synth(d,noisy=True):
    fp=ALL[d['font']]; A=base_render(fp,TXT,capsize(fp,d['cap']))
    ink=place(A,d['kx'],H,W)
    ink=np.roll(np.roll(ink,int(d['dy']),axis=0),int(d['dx']),axis=1)
    lay=gf(ink,d['blur'])*DEPTH
    return CARRIER+lay if noisy else lay
ORDER=['Arimo Bold','Roboto Medium','Go Bold','Carlito Bold','Liberation Sans Bold','Lato Bold',
       'DejaVu Sans Bold','Nimbus Sans Bold','Open Sans Semibold','Noto Sans Regular','Nimbus Mono PS Bold']
d={x['font']:x for x in B}
rows=[('REAL PIXELS — frame 983 (one frame, no averaging)',disp(REAL),None,True),
      ('REAL PIXELS — 5-frame average f973/974/981/983/984 (corroboration)',disp(REAL5),None,True)]
for f in ORDER:
    if f not in d: continue
    e=d[f]
    rows.append(('%s  —  cap %.0f px, horizontal stretch kx=%.2f, PSF sigma %.1f px   |   r = %.4f'%(f,e['cap'],e['kx'],e['blur'],e['r']),
                 disp(synth(e)), e['r'], False))
PAD=30; LH=44
Wc=max(im.width for _,im,_,_ in rows)+2*PAD
Hc=118+sum(im.height+LH for _,im,_,_ in rows)+170
c=canvas(Wc,Hc)
text(c,(PAD,18),'TYPEFACE TEST — line 1, known text',size=30)
text(c,(PAD,54),'Real pixels vs candidate faces put through the MEASURED degradation:',size=17,bold=False,fill=(70,70,70))
text(c,(PAD,76),'render -> stretch horizontally by kx -> blur by the fitted PSF -> scale to the measured ink',size=17,bold=False,fill=(70,70,70))
text(c,(PAD,98),'depth (11.9/255) -> ADD A REAL CAPTION-FREE FRAME of the same video -> same display pipeline.',size=17,bold=False,fill=(70,70,70))
y=128
for lab,im,r,isreal in rows:
    c.paste(im.convert('RGB'),(PAD,y))
    rect(c,(PAD-2,y-2,PAD+im.width+1,y+im.height+1),outline=(170,20,20) if isreal else (200,200,200),w=2 if isreal else 1)
    text(c,(PAD,y+im.height+8),lab,size=19,fill=(170,20,20) if isreal else (20,20,20))
    y+=im.height+LH
text(c,(PAD,y+4),'Top four (Arimo Bold = Arial Bold clone, Roboto Medium, Go Bold, Carlito Bold = Calibri',size=19)
text(c,(PAD,y+30),'Bold clone) span r = 0.751-0.814: an 8% spread across four unrelated designs. Roboto',size=19)
text(c,(PAD,y+56),'Medium is 2nd, not 1st; on frame f983 with one extra cap-height grid point Nimbus Sans',size=19)
text(c,(PAD,y+82),'Bold (Helvetica Bold clone) wins instead. THE TYPEFACE IS UNDETERMINED.',size=19)
text(c,(PAD,y+112),'Nimbus Mono PS Bold is a negative control: it should lose, and does (r = 0.249).',size=18,fill=(90,90,90))
c.save(FIG+'FIG2_typeface_proof.png'); print('FIG2',c.size)
