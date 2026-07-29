"""Figure - what a timecode tick looks like, and how long it is held, in each era."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
BH,BW,BX,BY=120,620,590,895
def band(v): return np.fromfile('analysis/timecode-ticks/band_%s.raw'%v,dtype=np.uint8).reshape(-1,BH,BW)
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FM='/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'
def f(p,s): return ImageFont.truetype(p,s)
def tile(vid,a,b,x0,x1,pad=5,tw=700,th=50):
    A=band(vid)
    seg=A[a-1+pad:b-1-pad, 32:110, x0-BX:x1-BX].astype(np.float32)
    m=seg.mean(0); m=m-ndimage.gaussian_filter(m,5)
    s=m.std(); m=np.clip(m/(2.4*s)*118+130,0,255).astype('uint8')
    return Image.fromarray(m).resize((tw,th),Image.LANCZOS)
R11=[('ZB788PtqQvg',186,233,'00:08:43',47),('ZB788PtqQvg',233,277,'00:08:44',44),
     ('ZB788PtqQvg',277,325,'00:08:45',48),('ZB788PtqQvg',325,371,'00:08:46',46)]
R26=[('l9RAhmPHM_A',3150,3195,'02:23:45',45),('l9RAhmPHM_A',3195,3240,'02:23:46',45),
     ('l9RAhmPHM_A',3240,3285,'02:23:47',45),('l9RAhmPHM_A',3285,3330,'02:23:48',45),
     ('l9RAhmPHM_A',3330,3374,'02:23:49',44),('l9RAhmPHM_A',3374,3420,'02:23:50',46)]
X11=(660,1040); X26=(612,990)
W=1360; TW=680; LX=250
IMG=Image.new('RGB',(W,1150),(255,255,255)); d=ImageDraw.Draw(IMG)
INK=(22,22,26); MUT=(112,114,122); AC1=(176,68,36); AC2=(34,90,156); RULE=(214,214,220)
d.text((36,24),'The burned-in timecode counts whole seconds of source time',font=f(FB,31),fill=INK)
d.text((36,64),'Each value is held for a fixed number of video frames. That frame count is the whole argument.',font=f(FR,21),fill=MUT)
def block(y0,title,rows,xr,col):
    d.text((36,y0),title,font=f(FB,25),fill=col)
    y=y0+36
    d.text((38,y),'reads',font=f(FR,15),fill=MUT)
    d.text((LX,y),'the timecode strip, averaged over every frame it is held',font=f(FR,15),fill=MUT)
    d.text((LX+TW+22,y),'held for',font=f(FR,15),fill=MUT)
    y+=22
    for vid,a,b,txt,n in rows:
        IMG.paste(tile(vid,a,b,xr[0],xr[1],tw=TW,th=50),(LX,y+1))
        d.rectangle([LX-1,y,LX+TW,y+51],outline=RULE)
        d.text((38,y+15),txt,font=f(FM,20),fill=INK)
        d.text((LX+TW+22,y+13),'%d'%n,font=f(FB,24),fill=col)
        d.text((LX+TW+60,y+18),'frames',font=f(FR,17),fill=MUT)
        y+=55
    return y
y=block(112,'2011 uploads  —  25 fps',R11,X11,AC2)
d.text((LX,y+4),'four consecutive seconds — 47, 44, 48, 46 frames',font=f(FR,18),fill=MUT)
d.text((LX,y+27),'185 frames / 4 ticks  =  46.3 frames per source second',font=f(FB,18),fill=AC2)
y=block(y+66,'2026 uploads  —  29.97 fps',R26,X26,AC1)
d.text((LX,y+4),'ten consecutive seconds were read; six shown',font=f(FR,18),fill=MUT)
d.text((LX,y+27),'450 frames / 10 ticks  =  45.0 frames per source second',font=f(FB,18),fill=AC1)
yb=y+64
d.rectangle([36,yb,W-36,yb+168],fill=(245,245,248))
d.text((58,yb+16),'Nearly the same frame count — at a different frame rate.',font=f(FB,26),fill=INK)
d.text((58,yb+56),'2011:   46.3 frames ÷ 25 fps       =  1.85 s of video per source second   →   0.54× speed',font=f(FM,19),fill=AC2)
d.text((58,yb+90),'2026:   45.0 frames ÷ 29.97 fps  =  1.50 s of video per source second   →   0.67× speed',font=f(FM,19),fill=AC1)
d.text((58,yb+128),'A shared editing template would have carried the speed across. What carried across was the frame count.',font=f(FR,19),fill=MUT)
IMG=IMG.crop((0,0,W,yb+186)).save('figs/technical/fig_timecode_ticks.png')
print('ok')
