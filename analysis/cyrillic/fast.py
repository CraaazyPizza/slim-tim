"""Fast Fourier-domain matched filter. The whole preprocessing chain
(row-mean removal + Gaussian high-pass) and the PSF blur are linear, so they are
applied as transfer functions and the blur sweep costs almost nothing."""
import numpy as np, json
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter as gf

class Field:
    """Holds an observation window, preprocessed, plus filter masks."""
    def __init__(s, obs, H, W, hpsig=12.0):
        s.H, s.W = H, W
        Y = obs - obs.mean(axis=1, keepdims=True)
        Y = Y - gf(Y, hpsig, truncate=3.0)
        s.ob = Y - Y.mean()
        s.O = np.fft.rfft2(s.ob)
        s.nob = np.sqrt((s.ob**2).sum())
        fy = np.fft.fftfreq(H)[:,None]; fx = np.fft.rfftfreq(W)[None,:]
        s.f2 = fy**2 + fx**2
        s.HP = 1.0 - np.exp(-2*np.pi**2*hpsig**2*s.f2)   # Gaussian high-pass
        s.HP[:,0] = 0.0                                  # row-mean removal
        s._bl = {}
    def blur_mask(s, sig):
        if sig not in s._bl:
            s._bl[sig] = np.exp(-2*np.pi**2*sig**2*s.f2)
        return s._bl[sig]
    def match(s, ink, blurs, dyr=20, dxr=45):
        """ink: (H,W) float in [0,1]. Returns list of (r, blur, dx, dy)."""
        T = np.fft.rfft2(ink)
        dys = np.r_[np.arange(0,dyr+1), np.arange(s.H-dyr, s.H)]
        dxs = np.r_[np.arange(0,dxr+1), np.arange(s.W-dxr, s.W)]
        out=[]
        for bl in blurs:
            G = T*s.HP*s.blur_mask(bl)
            n2 = (np.abs(G[:,0])**2).sum() + 2*(np.abs(G[:,1:])**2).sum()
            n2 = n2/(s.H*s.W)
            if s.W%2==0: n2 -= (np.abs(G[:,-1])**2).sum()/(s.H*s.W)
            if n2 <= 1e-18: continue
            cc = np.fft.irfft2(np.conj(G)*s.O, (s.H,s.W))/(np.sqrt(n2)*s.nob)
            sub = cc[np.ix_(dys,dxs)]
            k = np.unravel_index(np.argmax(sub), sub.shape)
            dy,dx = dys[k[0]], dxs[k[1]]
            sdy = dy-s.H if dy>s.H//2 else dy
            sdx = dx-s.W if dx>s.W//2 else dx
            out.append((float(sub[k]), bl, sdx, sdy))
        return out

_RC={}
def base_render(fp, text, size):
    k=(fp,text,size)
    if k not in _RC:
        f=_font(fp,size); b=f.getbbox(text)
        w=max(2,b[2]-b[0]+8); h=max(2,b[3]-b[1]+8)
        im=Image.new('L',(w,h),255); ImageDraw.Draw(im).text((4-b[0],4-b[1]),text,font=f,fill=0)
        _RC[k]=np.asarray(im,dtype=np.uint8)
    return _RC[k]
def place(A, kx, H, W):
    h,w=A.shape; nw=max(2,int(round(w*kx)))
    T=1.0-np.asarray(Image.fromarray(A).resize((nw,h),Image.LANCZOS),dtype=np.float64)/255.0
    out=np.zeros((H,W)); y0=(H-h)//2; x0=(W-nw)//2
    a,b=max(0,y0),min(H,y0+h); c,d=max(0,x0),min(W,x0+nw)
    if b<=a or d<=c: return out
    out[a:b,c:d]=T[a-y0:b-y0,c-x0:d-x0]; return out
_FC={}
def _font(fp,size):
    k=(fp,size)
    if k not in _FC: _FC[k]=ImageFont.truetype(fp,size)
    return _FC[k]
_CS={}
def capsize(fp,target,ch='П'):
    """Font size whose cap height equals `target` px. Cap height is linear in the
    nominal size, so calibrate the ratio once at size 200 and invert, then refine +-2."""
    k=(fp,ch)
    if k not in _CS:
        b=_font(fp,200).getbbox(ch); _CS[k]=(b[3]-b[1])/200.0
    s=max(6,int(round(target/max(_CS[k],1e-6))))
    best=None
    for t in range(max(6,s-2),s+3):
        b=_font(fp,t).getbbox(ch); c=b[3]-b[1]; d=abs(c-target)
        if best is None or d<best[1]: best=(t,d)
    return best[0]
