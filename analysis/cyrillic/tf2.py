"""ANISOTROPIC typeface fit: free cap-height AND free horizontal scale.
Motivated by the measured letterform aspect (glyphs are ~30% wider than any
installed face at the measured cap height), i.e. the caption layer looks
horizontally stretched.  Everything else identical to tf.py."""
import numpy as np, sys, json, time
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter as gf

TEXT=L1_TEXT; ROWS=(902,1002); XS=(430,1620)
FONTS=json.load(open('fonts.json'))
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
def render_scaled(fp, text, size, kx, H, W):
    """render text at font `size` then stretch horizontally by kx; centred."""
    key=(fp,text,size)
    if key not in _RC:
        f=ImageFont.truetype(fp,size)
        b=f.getbbox(text)
        w=b[2]-b[0]+8; h=b[3]-b[1]+8
        im=Image.new('L',(w,h),255); ImageDraw.Draw(im).text((4-b[0],4-b[1]),text,font=f,fill=0)
        _RC[key]=(np.asarray(im,dtype=np.float64), f)
    A,f=_RC[key]
    h,w=A.shape
    nw=max(2,int(round(w*kx)))
    im=Image.fromarray(A.astype(np.uint8)).resize((nw,h),Image.LANCZOS)
    T=1.0-np.asarray(im,dtype=np.float64)/255.0
    out=np.zeros((H,W))
    y0=(H-h)//2; x0=(W-nw)//2
    ys=slice(max(0,y0),min(H,y0+h)); xs=slice(max(0,x0),min(W,x0+nw))
    out[ys,xs]=T[max(0,-y0):max(0,-y0)+(ys.stop-ys.start), max(0,-x0):max(0,-x0)+(xs.stop-xs.start)]
    return out

def capsize(fp,target):
    """font size whose cap height (П) equals target px"""
    best=None
    for s in range(20,260):
        try: b=ImageFont.truetype(fp,s).getbbox('П')
        except Exception: return None
        c=b[3]-b[1]
        d=abs(c-target)
        if best is None or d<best[1]: best=(s,d)
        if c>target*1.5: break
    return best[0] if best else None

def fit(win,fp,sizes,kxs,blurs,dyr=20,dxr=40):
    dys=np.r_[np.arange(0,dyr+1),np.arange(win.H-dyr,win.H)]
    dxs=np.r_[np.arange(0,dxr+1),np.arange(win.W-dxr,win.W)]
    best=None
    for size in sizes:
        for kx in kxs:
            try: ink=render_scaled(fp,TEXT,size,kx,win.H,win.W)
            except Exception: return None
            for bl in blurs:
                tm=prep(gf(ink,bl,truncate=3.0)); tm-=tm.mean()
                nn=np.sqrt((tm**2).sum())
                if nn<1e-9: continue
                cc=np.fft.irfft2(np.fft.rfft2(tm).conj()*win.F,(win.H,win.W))/(nn*win.n)
                sub=cc[np.ix_(dys,dxs)]
                k=np.unravel_index(np.argmax(sub),sub.shape)
                r=float(sub[k])
                if best is None or r>best[0]: best=(r,size,kx,bl)
    return best

t0=time.time()
win=Wn(OBS['f983'])
KX=[1.00,1.10,1.18,1.24,1.30,1.36,1.44]
BL=[0.6,1.0,1.5,2.2,3.0]
S1=[]
for name,fp in FONTS.items():
    s0=capsize(fp,53.5)
    if s0 is None: continue
    b=fit(win,fp,[s0],KX,BL)
    if b: S1.append(dict(font=name,file=fp,r=b[0],size=b[1],kx=b[2],blur=b[3],cap_size=s0))
S1.sort(key=lambda d:-d['r'])
print('ANISOTROPIC stage1: %d faces, %.0fs'%(len(S1),time.time()-t0))
print('%-40s %7s %5s %5s %5s'%('face','r','size','kx','blur'))
for d in S1[:45]: print('%-40s %7.4f %5d %5.2f %5.1f'%(d['font'],d['r'],d['size'],d['kx'],d['blur']))
json.dump(S1,open('tf2_stage1.json','w'),indent=1,ensure_ascii=False)
