"""THE TYPEFACE PROOF FIGURE.
Each candidate face is rendered at its own best-fit geometry, degraded through the
MEASURED pipeline (horizontal stretch kx, Gaussian PSF sigma, measured ink depth),
added to a REAL caption-free noise carrier from the same video, and then put through
exactly the same display pipeline as the real pixels. Glyph-aligned, same stretch."""
import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import base_render, place, capsize
from figlib import *
from enh import localnorm
from scipy.ndimage import gaussian_filter as gf
from PIL import Image
FIG='/home/user/new-skinny-bob/figs/cyrillic/'
ALL=json.load(open('fonts.json'))
B=json.load(open('sweepB.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
ROWS=(904,1000); XS=(438,1612); TXT='Предыдущее сообщение'
H=ROWS[1]-ROWS[0]; W=XS[1]-XS[0]
def obsw(fs):
    return (-RESL[[FR.index(f) for f in fs]].mean(0))[(ROWS[0]-Y0):(ROWS[1]-Y0),(XS[0]-X0):(XS[1]-X0)]
REAL=obsw([983]); REAL5=obsw([983,973,974,984,981])
CARRIER=obsw([1020])                    # caption-free single frame, same band
DEPTH=11.9/255.0
def synth(font, cap, kx, sig, dx, dy, noisy=True):
    fp=ALL[font]; s=capsize(fp,cap)
    ink=place(base_render(fp,TXT,s),kx,H,W)
    ink=np.roll(np.roll(ink,int(round(dy)),axis=0),int(round(dx)),axis=1)
    lay=gf(ink,sig)*DEPTH
    return (CARRIER+lay) if noisy else lay
def show(X, sc=2, sig=45):
    return up(strip(localnorm(X,sig),1.0,99.0), sc)
def build(tag, order, fn, title, noisy=True, sc=2):
    rows=[]
    im0=show(REAL,sc); rows.append(('REAL PIXELS  —  video 1, frame 983 (single frame, no averaging)',im0,None))
    rows.append(('REAL PIXELS  —  5-frame average f983/973/974/981/984 (corroboration only)',show(REAL5,sc),None))
    d={x['font']:x for x in B[tag]}
    for f in order:
        if f not in d: continue
        e=d[f]
        X=synth(f,e['cap'],e['kx'],e['blur'],e['dx'],e['dy'],noisy)
        lab='%s   —   cap %.0f px, horizontal stretch %.2f, PSF sigma %.1f px%s   |   r = %.4f'%(
            f,e['cap'],e['kx'],e['blur'],'' if noisy else ' (clean render)',e['r'])
        rows.append((lab,show(X,sc) if noisy else up(strip(-localnorm(-X,sig),1,99),sc),e['r']))
    PAD=28; LH=40; GAP=10
    Wc=rows[0][1].width+2*PAD
    Hc=96+sum(r[1].height+LH+GAP for r in rows)+40
    c=canvas(Wc,Hc)
    text(c,(PAD,20),title,size=32)
    text(c,(PAD,60),'Every synthetic row: rendered -> stretched horizontally by kx -> blurred by the measured PSF -> scaled to the measured ink depth -> added to a REAL caption-free frame of the same video -> identical display pipeline.',size=17,bold=False,fill=(90,90,90))
    y=98
    for i,(lab,im,r) in enumerate(rows):
        c.paste(im.convert('RGB'),(PAD,y))
        col=(150,20,20) if i<2 else (20,20,20)
        text(c,(PAD,y+im.height+6),lab,size=21,fill=col)
        rect(c,(PAD-2,y-2,PAD+im.width+1,y+im.height+1),outline=(150,20,20) if i<2 else (200,200,200),w=2)
        y+=im.height+LH+GAP
    c.save(FIG+fn); print(FIG+fn,c.size)
if __name__=='__main__':
    tag='f983'
    ranked=[x['font'] for x in B[tag]]
    order=ranked[:6]
    for must in ['Roboto Medium','DejaVu Sans Bold','Liberation Sans Bold','Open Sans Semibold','Nimbus Sans Bold']:
        if must not in order and must in [x['font'] for x in B[tag]]: order.append(must)
    build(tag,order,'FIG2_typeface_proof.png',
      'TYPEFACE TEST — the known line 1 "Предыдущее сообщение", real pixels vs candidate faces put through the measured degradation')
