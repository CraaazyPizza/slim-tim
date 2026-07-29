import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from pipe import *
from figlib import *
from PIL import Image
FIG='/home/user/new-skinny-bob/figs/cyrillic/'
F=sig([983]); ST=sig(CAP)
R=(906,1080); Xc=(438,1612)
def crop(X): return X[(R[0]-Y0):(R[1]-Y0),(Xc[0]-X0):(Xc[1]-X0)]
n=strip(crop(F),1.0,99.0)
h,w=n.shape
SC=3
im_l=up(n,SC); im_n=up(n,SC,nn=True)
st=strip(crop(ST),1.0,99.0); im_s=up(st,SC)
PAD=26; LH=46
W=im_l.width+2*PAD
Hc=70 + (h+LH) + (im_l.height+LH) + (im_n.height+LH) + (im_s.height+LH) + 90
c=canvas(W,Hc)
text(c,(PAD,18),'THE SINGLE SHARPEST FRAME — hidden Cyrillic caption, video 1 (OpSTlDJWFFI), frame 983',size=30)
text(c,(PAD,52),'No frame averaging. Background = mean of caption-free frames 950-1009; row-mean flatten; percentile stretch; inverted.',size=19,bold=False,fill=(90,90,90))
y=92
def row(im,label,y):
    x=PAD+(im_l.width-im.width)//2
    c.paste(im.convert('RGB'),(x,y))
    text(c,(PAD,y+im.height+8),label,size=20)
    return y+im.height+LH
y=row(Image.fromarray(n),'A   frame 983, NATIVE resolution, 1 screen pixel = 1 video pixel   (1174 x 174 px)',y)
y=row(im_l,'B   frame 983, %d x Lanczos'%SC,y)
y=row(im_n,'C   frame 983, %d x NEAREST-NEIGHBOUR (no interpolation — every value is a real measured pixel)'%SC,y)
y=row(im_s,'D   for comparison: the 20-frame average f970-989, same %d x Lanczos, same stretch'%SC,y)
text(c,(PAD,y+4),'Line 1 = "Предыдущее сообщение".   Line 2 ends "... об АА" + one further glyph.   Panel D is the stack the earlier reports used: it is NOT sharper than the single frame.',size=19,bold=False,fill=(90,90,90))
c.save(FIG+'FIG1_best_frame.png')
print(FIG+'FIG1_best_frame.png', c.size)
