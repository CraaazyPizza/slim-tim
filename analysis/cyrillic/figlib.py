"""Figure helpers: contrast-stretched crops, labelled row stacks, burned-in captions."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR_='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def strip(X, lo=1.0, hi=99.0, invert=True):
    a,q=np.percentile(X,[lo,hi]); Q=np.clip((X-a)/(q-a+1e-12),0,1)
    if invert: Q=1-Q
    return (Q*255).astype(np.uint8)
def up(arr, sc, mode='L', nn=False):
    im=Image.fromarray(arr, mode)
    return im.resize((int(im.width*sc),int(im.height*sc)),
                     Image.NEAREST if nn else Image.LANCZOS)
def canvas(w,h,bg=255): return Image.new('RGB',(w,h),(bg,bg,bg))
def text(im,xy,s,size=22,bold=True,fill=(20,20,20),anchor='la'):
    d=ImageDraw.Draw(im); d.text(xy,s,font=ImageFont.truetype(FB if bold else FR_,size),fill=fill,anchor=anchor)
def measure(s,size=22,bold=True):
    f=ImageFont.truetype(FB if bold else FR_,size); b=f.getbbox(s); return b[2]-b[0], b[3]-b[1]
def rule(im,xy0,xy1,fill=(190,60,60),w=2):
    ImageDraw.Draw(im).line([xy0,xy1],fill=fill,width=w)
def rect(im,box,outline=(190,60,60),w=2):
    ImageDraw.Draw(im).rectangle(box,outline=outline,width=w)

def wrap(im, xy, s, maxw, size=20, bold=True, fill=(20,20,20), lh=None):
    """word-wrap `s` into lines no wider than maxw px; returns the y after the block."""
    from PIL import ImageFont
    f=ImageFont.truetype(FB if bold else FR_,size)
    words=s.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if f.getbbox(t)[2]-f.getbbox(t)[0] <= maxw or not cur: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    lh = lh or int(size*1.35)
    x,y=xy
    for ln in lines:
        text(im,(x,y),ln,size=size,bold=bold,fill=fill); y+=lh
    return y
