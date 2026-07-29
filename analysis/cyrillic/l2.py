"""LINE 2: whole-phrase test at anisotropic geometry, and the last-glyph ranking."""
import numpy as np, sys, json, time, random
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter as gf
ALL=json.load(open('fonts.json'))
FSET=[f for f in ['Roboto Medium','Open Sans Semibold','Liberation Sans Bold','DejaVu Sans Book',
                  'Noto Sans Regular','Lato Bold','Carlito Bold','Nimbus Sans Bold','Arimo Bold'] if f in ALL]
ROWS=(996,1080); XS=(432,1590)
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
ci=[FR.index(f) for f in CAP]
def prep(X):
    Y=X-np.median(X,axis=1,keepdims=True); return Y-gf(Y,12.0,truncate=3.0)
OBS={'f983':-prep(RESL[FR.index(983)]),
     'best5':-prep(RESL[[FR.index(f) for f in (983,973,974,984,981)]].mean(0)),
     'stack20':-prep(RESL[ci].mean(0)),
     'NULLa':-prep(RESL[[FR.index(f) for f in range(1010,1030)]].mean(0)),
     'NULLb':-prep(RESL[[FR.index(f) for f in range(915,935)]].mean(0)),
     'NULLc':-prep(RESL[FR.index(1020)])}
class Wn:
    def __init__(s,obs):
        o=obs[(ROWS[0]-Y0):(ROWS[1]-Y0),(XS[0]-X0):(XS[1]-X0)].astype(float)
        s.H,s.W=o.shape; s.ob=o-o.mean(); s.F=np.fft.rfft2(s.ob); s.n=np.sqrt((s.ob**2).sum())
_RC={}
def rend(fp,text,size):
    k=(fp,text,size)
    if k not in _RC:
        f=ImageFont.truetype(fp,size); b=f.getbbox(text)
        w=max(2,b[2]-b[0]+8); h=max(2,b[3]-b[1]+8)
        im=Image.new('L',(w,h),255); ImageDraw.Draw(im).text((4-b[0],4-b[1]),text,font=f,fill=0)
        _RC[k]=np.asarray(im,dtype=np.uint8)
    return _RC[k]
def place(A,kx,H,W):
    h,w=A.shape; nw=max(2,int(round(w*kx)))
    T=1.0-np.asarray(Image.fromarray(A).resize((nw,h),Image.LANCZOS),dtype=np.float64)/255.0
    out=np.zeros((H,W)); y0=(H-h)//2; x0=(W-nw)//2
    a,b=max(0,y0),min(H,y0+h); c,d=max(0,x0),min(W,x0+nw)
    out[a:b,c:d]=T[a-y0:b-y0,c-x0:d-x0]; return out
def score(win,fp,text,sizes,kxs,blurs,dyr=18,dxr=45):
    best=None
    dys=np.r_[np.arange(0,dyr+1),np.arange(win.H-dyr,win.H)]
    dxs=np.r_[np.arange(0,dxr+1),np.arange(win.W-dxr,win.W)]
    for s in sizes:
        A=rend(fp,text,s)
        for kx in kxs:
            ink=place(A,kx,win.H,win.W)
            for bl in blurs:
                tm=prep(gf(ink,bl,truncate=3.0)); tm-=tm.mean()
                nn=np.sqrt((tm**2).sum())
                if nn<1e-9: continue
                cc=np.fft.irfft2(np.fft.rfft2(tm).conj()*win.F,(win.H,win.W))/(nn*win.n)
                sub=cc[np.ix_(dys,dxs)]; k=np.unravel_index(np.argmax(sub),sub.shape)
                dy,dx=dys[k[0]],dxs[k[1]]
                sdy=dy-win.H if dy>win.H//2 else dy; sdx=dx-win.W if dx>win.W//2 else dx
                r=float(sub[k])
                if best is None or r>best[0]: best=(r,s,kx,bl,sdx,sdy)
    return best
if __name__=='__main__':
    geo=json.load(open('l2geo.json')) if False else None
    SZ=json.load(open('l1geo.json'))
    print('geometry carried over from line 1:',SZ)
