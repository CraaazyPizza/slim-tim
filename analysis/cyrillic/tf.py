"""TYPEFACE TEST. Fit the KNOWN line-1 string in every installed Cyrillic-capable
face, free size / blur / position, matched preprocessing on obs and template."""
import numpy as np, sys, json, os, time
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from PIL import ImageFont
from scipy.ndimage import gaussian_filter as gf

TEXT = L1_TEXT
ROWS = (902, 1002); XS = (430, 1620)
INKW = 1152.7
FONTS = json.load(open('fonts.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
ci=[FR.index(f) for f in CAP]
def prep(X):
    Y = X - np.median(X, axis=1, keepdims=True)
    return Y - gf(Y, 12.0, truncate=3.0)
OBS = {
  'f983'   : -prep(RESL[FR.index(983)]),
  'stack20': -prep(RESL[ci].mean(0)),
  'best5'  : -prep(RESL[[FR.index(f) for f in (983,973,974,984,981)]].mean(0)),
}
class Wn:
    def __init__(s, obs):
        o = obs[(ROWS[0]-Y0):(ROWS[1]-Y0), (XS[0]-X0):(XS[1]-X0)].astype(float)
        s.H,s.W = o.shape; s.ob = o-o.mean()
        s.F = np.fft.rfft2(s.ob); s.n = np.sqrt((s.ob**2).sum())
def size_for(fp, text, target):
    best=None
    for s in range(20,400):
        try:
            b=ImageFont.truetype(fp,s).getbbox(text); w=b[2]-b[0]
        except Exception: return None
        d=abs(w-target)
        if best is None or d<best[1]: best=(s,d)
        if w>target*1.6: break
    return best[0] if best else None
def fit(win, fp, sizes, blurs, dyr=18, dxr=26, text=None):
    text = TEXT if text is None else text
    best=None
    dys = np.r_[np.arange(0,dyr+1), np.arange(win.H-dyr, win.H)]
    dxs = np.r_[np.arange(0,dxr+1), np.arange(win.W-dxr, win.W)]
    for size in sizes:
        try: ink0 = render_ink(text, fp, size, win.H, win.W, win.W//2, win.H//2)
        except Exception: return None
        for bl in blurs:
            tm = prep(gf(ink0, bl, truncate=3.0)); tm -= tm.mean()
            nn = np.sqrt((tm**2).sum())
            if nn<1e-9: continue
            cc = np.fft.irfft2(np.fft.rfft2(tm).conj()*win.F,(win.H,win.W))/(nn*win.n)
            sub = cc[np.ix_(dys,dxs)]
            k = np.unravel_index(np.argmax(sub),sub.shape)
            dy,dx = dys[k[0]],dxs[k[1]]
            sdy = dy-win.H if dy>win.H//2 else dy
            sdx = dx-win.W if dx>win.W//2 else dx
            r=float(sub[k])
            if best is None or r>best[0]: best=(r,size,bl,XS[0]+win.W//2+sdx,ROWS[0]+win.H//2+sdy)
    return best

t0=time.time()
# ---------- stage 1: coarse sweep, all faces, single best frame
win = Wn(OBS['f983'])
S1=[]
for name,fp in FONTS.items():
    s0=size_for(fp,TEXT,INKW)
    if s0 is None: continue
    b=fit(win,fp,[s0],[0.7,1.3,2.0,3.0,4.5,6.0])
    if b: S1.append(dict(font=name,file=fp,r=b[0],size=b[1],blur=b[2],s0=s0))
S1.sort(key=lambda d:-d['r'])
print('stage1 %d faces in %.0fs'%(len(S1),time.time()-t0)); sys.stdout.flush()
print('%-40s %7s %5s %5s'%('face','r','size','blur'))
for d in S1[:40]: print('%-40s %7.4f %5d %5.1f'%(d['font'],d['r'],d['size'],d['blur']))
json.dump(S1,open('tf_stage1.json','w'),indent=1,ensure_ascii=False)

# ---------- stage 2: fine grid on the top 45, on all three observations
TOP=[d['font'] for d in S1[:45]]
BL=[0.4,0.7,1.0,1.3,1.6,2.0,2.5,3.0,3.5,4.0,5.0,6.0,7.0]
res={}
for tag,obs in OBS.items():
    w=Wn(obs); rows=[]
    for name in TOP:
        fp=FONTS[name]; s0=size_for(fp,TEXT,INKW)
        b=fit(w,fp,[s0-4,s0-2,s0,s0+2,s0+4],BL)
        if b: rows.append(dict(font=name,file=fp,r=b[0],size=b[1],blur=b[2],x=b[3],base=b[4]))
    rows.sort(key=lambda d:-d['r']); res[tag]=rows
    print('\n===== %s : fine grid, top 45 faces ====='%tag)
    print('%-40s %7s %5s %5s %6s %6s'%('face','r','size','blur','x','base'))
    for d in rows[:20]: print('%-40s %7.4f %5d %5.1f %6d %6d'%(d['font'],d['r'],d['size'],d['blur'],d['x'],d['base']))
    sys.stdout.flush()
json.dump(res,open('tf.json','w'),indent=1,ensure_ascii=False)
print('total %.0fs'%(time.time()-t0))
