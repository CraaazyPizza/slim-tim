import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
import pipe
from pipe import sig, BEST5, save
from fast import base_render, place, capsize, _font
from figlib import *
from figlib import wrap
from enh import localnorm
from scipy.ndimage import gaussian_filter as gf
from PIL import Image, ImageDraw
FIG='/home/user/new-skinny-bob/figs/cyrillic/'
ALL=json.load(open('fonts.json'))
F=sig([983]); B5=sig(BEST5); ST=sig(list(CAP))
NULLF=sig([1020])
def show(X,rows,xs,sc=1,sig_=45,nn=False,lo=1.0,hi=99.0):
    b=X[(rows[0]-Y0):(rows[1]-Y0),(xs[0]-X0):(xs[1]-X0)]
    return up(strip(localnorm(b,sig_),lo,hi),sc,nn=nn)

# ---------------- FIG 1 : best single frame
R1=(906,1000); R2=(998,1080); XA=(438,1615)
rows=[]
rows.append(('REAL, frame 983 — line 1, NATIVE resolution (1 screen px = 1 video px)',show(F,R1,XA,1)))
rows.append(('REAL, frame 983 — line 1, 2x nearest-neighbour (no interpolation)',show(F,R1,XA,2,nn=True)))
rows.append(('REAL, frame 983 — line 1, 2x Lanczos',show(F,R1,XA,2)))
rows.append(('REAL, frame 983 — line 2, NATIVE resolution',show(F,R2,XA,1)))
rows.append(('REAL, frame 983 — line 2, 2x nearest-neighbour',show(F,R2,XA,2,nn=True)))
rows.append(('REAL, frame 983 — line 2, 2x Lanczos',show(F,R2,XA,2)))
rows.append(('for comparison: the 20-frame average f970-989, line 2, 2x Lanczos (NOT sharper)',show(ST,R2,XA,2)))
rows.append(('CONTROL: a caption-free frame (f1020), same band, same pipeline, same stretch',show(NULLF,R2,XA,2)))
PAD=30; LH=56
W=max(im.width for _,im in rows)+2*PAD
H=140+sum(im.height+LH for _,im in rows)+150
c=canvas(W,H)
text(c,(PAD,22),'THE SINGLE SHARPEST FRAME — hidden Cyrillic caption, video 1 (OpSTlDJWFFI), frame 983',size=44)
wrap(c,(PAD,66),'Chosen by leave-one-out cross-correlation against the rest of the caption block: f983 r=0.865; next best f973 0.849; worst frame inside the block f976 0.349; best frame outside the block 0.10.',W-2*PAD,size=26,bold=False,fill=(70,70,70))
y=136
for lab,im in rows:
    c.paste(im.convert('RGB'),(PAD,y)); rect(c,(PAD-2,y-2,PAD+im.width+1,y+im.height+1),outline=(180,180,180),w=1)
    text(c,(PAD,y+im.height+8),lab,size=30,fill=(150,20,20) if 'CONTROL' in lab or 'comparison' in lab else (20,20,20))
    y+=im.height+LH
y=wrap(c,(PAD,y+2),'Line 1: "Предыдущее сообщени" — the final "е" of "сообщение" is NOT rendered. Ink stops at x=1615; a final "е" would need x 1612-1658.',W-2*PAD,size=28)
wrap(c,(PAD,y+6),'Line 2: "предупреждало об АА" plus one further capital-height glyph.',W-2*PAD,size=28)
c.save(FIG+'FIG1_best_frame.png'); print('FIG1', c.size)
