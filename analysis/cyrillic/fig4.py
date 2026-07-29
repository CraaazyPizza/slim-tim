import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
import pipe
from pipe import sig, BEST5
from fast import base_render, place, capsize, _font
from figlib import *
from figlib import wrap
from enh import localnorm
from scipy.ndimage import gaussian_filter as gf
from PIL import Image, ImageDraw
FIG='/home/user/new-skinny-bob/figs/cyrillic/'
ALL=json.load(open('fonts.json')); G=json.load(open('l2geo.json')); LAST=json.load(open('l2last.json'))
F=sig([983]); B5=sig(BEST5); NUL1=sig([1020])
R2=(998,1080)
def crop(X,xs,rows=R2,s=45): return localnorm(X[(rows[0]-Y0):(rows[1]-Y0),(xs[0]-X0):(xs[1]-X0)],s)
def render_pinned(fp,text,size,kx,H,W,xleft,baseline):
    f=_font(fp,size); bb=f.getbbox(text)
    w=max(2,bb[2]-bb[0]+8); h=max(2,bb[3]-bb[1]+8)
    im=Image.new('L',(w,h),255); ImageDraw.Draw(im).text((4-bb[0],4-bb[1]),text,font=f,fill=0)
    A=np.asarray(im,dtype=np.uint8); nw=max(2,int(round(w*kx)))
    T=1.0-np.asarray(Image.fromarray(A).resize((nw,h),Image.LANCZOS),dtype=np.float64)/255.0
    asc,_=f.getmetrics(); by=4-bb[1]+asc
    out=np.zeros((H,W)); y0=int(round(baseline-by)); x0=int(round(xleft-4*kx))
    a,b2=max(0,y0),min(H,y0+h); c,d=max(0,x0),min(W,x0+nw)
    if b2<=a or d<=c: return out
    out[a:b2,c:d]=T[a-y0:b2-y0,c-x0:d-x0]; return out
XSF=(436,1600); H=R2[1]-R2[0]; Wf=XSF[1]-XSF[0]
fp=ALL[G['font']]
tmpl=render_pinned(fp,'предупреждало об АА',G['size'],G['kx'],H,Wf,439-XSF[0],1058-R2[0])
tmpl=gf(tmpl,1.0)
SC=1
a_real=up(strip(crop(F,XSF),1,99),SC)
a_stk =up(strip(crop(B5,XSF),1,99),SC)
a_tmp =up((255-(tmpl/max(tmpl.max(),1e-9)*255)).astype(np.uint8),SC)
a_nul =up(strip(crop(NUL1,XSF),1,99),SC)
# tail zoom
XT=(1370,1600)
t_real=up(strip(crop(F,XT,s=35),1,99),4)
t_stk =up(strip(crop(B5,XT,s=35),1,99),4)
tt=render_pinned(fp,'предупреждало об АА',G['size'],G['kx'],H,XSF[1]-XSF[0],439-XSF[0],1058-R2[0])
tt=tt[:,(XT[0]-XSF[0]):(XT[1]-XSF[0])]
t_tmp=up((255-(gf(tt,1.0)*255).clip(0,255)).astype(np.uint8),4)
tt3=render_pinned(fp,'предупреждало об ААГ',G['size'],G['kx'],H,XSF[1]-XSF[0],439-XSF[0],1058-R2[0])
tt3=tt3[:,(XT[0]-XSF[0]):(XT[1]-XSF[0])]
t_tmp3=up((255-(gf(tt3,1.0)*255).clip(0,255)).astype(np.uint8),4)
PAD=30; LH=42
Wc=max(a_real.width,t_real.width)+2*PAD
Hc=120+4*(a_real.height+LH)+40+4*(t_real.height+LH)+430
c=canvas(Wc,Hc)
text(c,(PAD,18),'LINE 2 — "предупреждало об АА" + one more capital-height glyph',size=28)
wrap(c,(PAD,56),'Template pinned to the MEASURED left edge of the ink (x=439), free to slide only +-8 px. Fitted geometry cap 48 px, kx 1.41, baseline y 1058. Whole-line score against 22 same-length Russian and nonsense phrases: z = +10.7 (frame 983), +10.3 (5-frame). Best null +1.9; best the same test reaches on caption-free frames +3.8.',Wc-2*PAD,size=17,bold=False,fill=(70,70,70))
y=150
for lab,im,col in [('REAL PIXELS — frame 983 (one frame)',a_real,(170,20,20)),
                   ('REAL PIXELS — 5-frame average',a_stk,(170,20,20)),
                   ('TEMPLATE  "предупреждало об АА"  at the fitted geometry, same scale, same position',a_tmp,(20,20,20)),
                   ('CONTROL — caption-free frame f1020, same band, same pipeline',a_nul,(120,120,120))]:
    c.paste(im.convert('RGB'),(PAD,y)); rect(c,(PAD-2,y-2,PAD+im.width+1,y+im.height+1),outline=col,w=2)
    text(c,(PAD,y+im.height+8),lab,size=19,fill=col); y+=im.height+LH
y+=26
text(c,(PAD,y),'THE TAIL, 4x  (x = 1370 - 1600).  Two capital A, then one more capital-height glyph; nothing after x = 1570.',size=19); y+=40
for lab,im,col in [('REAL — frame 983',t_real,(170,20,20)),('REAL — 5-frame average',t_stk,(170,20,20)),
                   ('TEMPLATE "...об АА" only, two glyphs: its ink ends at x = 1540',t_tmp,(20,20,20)),
                   ('TEMPLATE "...об ААГ", three glyphs — this is what the pixels look like',t_tmp3,(20,20,20))]:
    c.paste(im.convert('RGB'),(PAD,y)); rect(c,(PAD-2,y-2,PAD+im.width+1,y+im.height+1),outline=col,w=2)
    text(c,(PAD,y+im.height+8),lab,size=19,fill=col); y+=im.height+LH
y+=14
y=wrap(c,(PAD,y),'RANKED CANDIDATES for the third glyph, scored on a window covering ONLY that cell (x 1526-1617) so the rest of the line cannot pay for it:',Wc-2*PAD,size=19)
rows=LAST['best5'][:12]
lst=' '.join('%s %.2f (z%+.1f)'%(r[0].strip("'"),r[1],r[2]) for r in rows)
y=wrap(c,(PAD,y+4),lst,Wc-2*PAD,size=19)+6
wrap(c,(PAD,y),'The same test on caption-free frames reaches z = +2.06 and +3.36, and the best real candidate is z = +2.07 — so the glyph EXISTS (its cap-band ink is about 4x the caption-free level) but its IDENTITY is UNDETERMINED: a capital-height stem-with-top-arm form, the Г / П / Б / В / Р / С / Е class. "Р" is 5th (z +1.4), so "об ААР" is live but not established. A FOURTH capital would need x 1607-1678, and there is no ink there.',Wc-2*PAD,size=18,bold=True)
c.save(FIG+'FIG4_line2.png'); print('FIG4',c.size)
