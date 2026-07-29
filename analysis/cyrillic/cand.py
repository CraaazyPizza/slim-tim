"""Head-to-head typeface test on a curated candidate list.
Mode ISO  : free size, free blur, isotropic  (what the prior record did)
Mode ANISO: free cap-height, free horizontal scale kx, free blur
Score = normalised cross-correlation of the KNOWN line-1 string against the pixels."""
import numpy as np, sys, json, time
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter as gf

TEXT=L1_TEXT; ROWS=(902,1002); XS=(430,1620)
ALL=json.load(open('fonts.json'))
CAND = ['Roboto Medium','Roboto Regular','Roboto Bold','Roboto Black','Roboto Light',
 'Roboto Condensed Medium','Roboto Condensed Bold',
 'DejaVu Sans Bold','DejaVu Sans Book','DejaVu Sans Condensed Bold','DejaVu Sans Condensed',
 'Liberation Sans Bold','Liberation Sans Regular','Liberation Sans Narrow Bold','Liberation Sans Narrow Regular',
 'Arimo Bold','Arimo Regular',
 'Open Sans Regular','Open Sans Semibold','Open Sans Bold','Open Sans Condensed Bold','Open Sans Light',
 'Noto Sans Regular','Noto Sans Bold','Noto Sans Display Regular','Noto Sans Display Bold',
 'Lato Regular','Lato Bold','Lato Semibold','Lato Medium','Lato Black','Lato Heavy',
 'Carlito Regular','Carlito Bold','Cantarell Regular','Cantarell Bold','Cantarell Extra Bold',
 'Nimbus Sans Regular','Nimbus Sans Bold','Nimbus Sans Narrow Bold','Nimbus Sans Narrow Regular',
 'FreeSans Regular','FreeSans Bold','URW Gothic Book','URW Gothic Demi','Comfortaa Bold','Comfortaa Regular',
 'Go Regular','Go Medium Regular','Go Bold',
 # negative controls (should lose)
 'DejaVu Serif Book','Liberation Serif Bold','Nimbus Mono PS Bold','Cousine Bold','Tinos Bold',
 'Linux Libertine O Regular','EB Garamond 12 Regular']
CAND=[c for c in CAND if c in ALL]
MISSING_NOTE=['PT Sans','PT Sans Caption','Segoe UI','Helvetica','Arial (real)','Inter','SF Pro',
 'Fira Sans','Source Sans Pro','Ubuntu','Museo Sans','Circe','Golos Text','YS Text','Manrope','Montserrat']

LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
ci=[FR.index(f) for f in CAP]
def prep(X):
    Y=X-np.median(X,axis=1,keepdims=True); return Y-gf(Y,12.0,truncate=3.0)
OBS={'f983':-prep(RESL[FR.index(983)]),
     'best5':-prep(RESL[[FR.index(f) for f in (983,973,974,984,981)]].mean(0)),
     'stack20':-prep(RESL[ci].mean(0))}
class Wn:
    def __init__(s,obs):
        o=obs[(ROWS[0]-Y0):(ROWS[1]-Y0),(XS[0]-X0):(XS[1]-X0)].astype(float)
        s.H,s.W=o.shape; s.ob=o-o.mean()
        s.F=np.fft.rfft2(s.ob); s.n=np.sqrt((s.ob**2).sum())
_RC={}
def base_render(fp,text,size):
    k=(fp,text,size)
    if k not in _RC:
        f=ImageFont.truetype(fp,size); b=f.getbbox(text)
        w=b[2]-b[0]+8; h=b[3]-b[1]+8
        im=Image.new('L',(w,h),255); ImageDraw.Draw(im).text((4-b[0],4-b[1]),text,font=f,fill=0)
        _RC[k]=np.asarray(im,dtype=np.uint8)
    return _RC[k]
def place(A,kx,H,W):
    h,w=A.shape; nw=max(2,int(round(w*kx)))
    T=1.0-np.asarray(Image.fromarray(A).resize((nw,h),Image.LANCZOS),dtype=np.float64)/255.0
    out=np.zeros((H,W)); y0=(H-h)//2; x0=(W-nw)//2
    ys0,ys1=max(0,y0),min(H,y0+h); xs0,xs1=max(0,x0),min(W,x0+nw)
    out[ys0:ys1,xs0:xs1]=T[ys0-y0:ys1-y0, xs0-x0:xs1-x0]
    return out
def corr(win,ink,bl,dyr=20,dxr=45):
    tm=prep(gf(ink,bl,truncate=3.0)); tm-=tm.mean()
    nn=np.sqrt((tm**2).sum())
    if nn<1e-9: return -1,0,0
    cc=np.fft.irfft2(np.fft.rfft2(tm).conj()*win.F,(win.H,win.W))/(nn*win.n)
    dys=np.r_[np.arange(0,dyr+1),np.arange(win.H-dyr,win.H)]
    dxs=np.r_[np.arange(0,dxr+1),np.arange(win.W-dxr,win.W)]
    sub=cc[np.ix_(dys,dxs)]; k=np.unravel_index(np.argmax(sub),sub.shape)
    dy,dx=dys[k[0]],dxs[k[1]]
    sdy=dy-win.H if dy>win.H//2 else dy; sdx=dx-win.W if dx>win.W//2 else dx
    return float(sub[k]),sdx,sdy
BL=[0.5,0.8,1.2,1.7,2.4,3.2,4.2,5.4]
SIZES=list(range(58,132,2))
KX=[1.00,1.06,1.12,1.18,1.22,1.26,1.30,1.34,1.38,1.44,1.50]
def capsize(fp,target):
    best=None
    for s in range(20,260):
        c=ImageFont.truetype(fp,s).getbbox('П'); c=c[3]-c[1]
        d=abs(c-target)
        if best is None or d<best[1]: best=(s,d)
        if c>target*1.6: break
    return best[0]
t0=time.time(); out={}
for tag in ('f983','best5','stack20'):
    win=Wn(OBS[tag]); rows=[]
    for n in CAND:
        fp=ALL[n]
        # ISO
        bi=None
        for s in SIZES:
            A=base_render(fp,TEXT,s)
            for bl in BL:
                r,dx,dy=corr(win,place(A,1.0,win.H,win.W),bl)
                if bi is None or r>bi[0]: bi=(r,s,1.0,bl,dx,dy)
        # ANISO
        ba=None
        c0=capsize(fp,53.5)
        for s in range(max(20,c0-8),c0+9,2):
            A=base_render(fp,TEXT,s)
            for kx in KX:
                ink=place(A,kx,win.H,win.W)
                for bl in BL:
                    r,dx,dy=corr(win,ink,bl)
                    if ba is None or r>ba[0]: ba=(r,s,kx,bl,dx,dy)
        rows.append(dict(font=n,iso_r=bi[0],iso_size=bi[1],iso_blur=bi[3],
                         ani_r=ba[0],ani_size=ba[1],ani_kx=ba[2],ani_blur=ba[3],
                         ani_dx=ba[4],ani_dy=ba[5],cap_size=c0))
    rows.sort(key=lambda d:-d['ani_r']); out[tag]=rows
    print('\n===== %s (%.0fs) ====='%(tag,time.time()-t0))
    print('%-30s | %7s %5s %5s | %7s %5s %5s %5s'%('face','ISO r','size','blur','ANI r','size','kx','blur'))
    for d in rows:
        print('%-30s | %7.4f %5d %5.1f | %7.4f %5d %5.2f %5.1f'%(d['font'],d['iso_r'],d['iso_size'],d['iso_blur'],
              d['ani_r'],d['ani_size'],d['ani_kx'],d['ani_blur']))
    sys.stdout.flush()
json.dump(dict(res=out,missing=MISSING_NOTE),open('cand.json','w'),indent=1,ensure_ascii=False)
