"""agent_cyr4 core: native-resolution per-frame stack + estimators.
Ink is POSITIVE in all estimator outputs."""
import numpy as np, os, json
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter as gf

D  = '/home/user/new-skinny-bob/frames/OpSTlDJWFFI/'
P  = '/home/user/new-skinny-bob/analysis/cyrillic/'
FIG= '/home/user/new-skinny-bob/figs/cyrillic/'
os.makedirs(P, exist_ok=True); os.makedirs(FIG, exist_ok=True)

Y0, Y1 = 900, 1080
X0, X1 = 300, 1750
FRAMES = list(range(910, 1050))
NORMBOX = (15, 1045, 290, 1610)
CAP = list(range(970, 990))
BG  = [f for f in FRAMES if not (966 <= f <= 993)]

# measured geometry (agent_cyr3, corrected)
L1_BASE, L1_SIZE = 985, 104          # line 1 baseline / RobotoM-equivalent size
L2_BASE, L2_SIZE = 1056, 90
L1_ROWS = (925, 1000)
L2_ROWS = (995, 1075)
L1_X    = (445, 1600)
L2_X    = (445, 1560)
L1_TEXT = 'Предыдущее сообщение'

_cache = P + 'stack4.npz'

def _load(f):
    a = np.asarray(Image.open(D + 'f%05d.png' % f).convert('L'), dtype=np.float64)
    m = a[NORMBOX[0]:NORMBOX[1], NORMBOX[2]:NORMBOX[3]].mean()
    return (a / m)[Y0:Y1, X0:X1]

if os.path.exists(_cache):
    _d = np.load(_cache); S = _d['S'].astype(np.float64); FR = list(_d['fr'])
else:
    S = np.stack([_load(f) for f in FRAMES]).astype(np.float32)
    np.savez_compressed(_cache, S=S, fr=np.array(FRAMES))
    S = S.astype(np.float64); FR = list(FRAMES)

H, W = S.shape[1], S.shape[2]
_bgm = S[[FR.index(f) for f in BG]].mean(0)
RES  = S - _bgm                      # ink NEGATIVE here

def flat(X):  return X - np.median(X, axis=1, keepdims=True)
def hp(X, s=20.0): return X - gf(X, (0, s))
def pp(X, s=20.0): return hp(flat(X), s)

def sl(rows, xs):
    return (slice(rows[0]-Y0, rows[1]-Y0), slice(xs[0]-X0, xs[1]-X0))

def render_ink(text, fp, size, h, w, xref, bref, spacing=0.0):
    im = Image.new('L', (w, h), 255); d = ImageDraw.Draw(im)
    fnt = ImageFont.truetype(fp, size)
    if spacing == 0.0:
        d.text((xref, bref), text, font=fnt, fill=0, anchor='ls')
    else:
        x = float(xref)
        for ch in text:
            d.text((x, bref), ch, font=fnt, fill=0, anchor='ls')
            x += fnt.getlength(ch) + spacing
    return 1.0 - np.asarray(im, dtype=np.float64) / 255.0

def ncc(a, b):
    a = a - a.mean(); b = b - b.mean()
    n = np.sqrt((a*a).sum() * (b*b).sum())
    return float((a*b).sum()/n) if n > 1e-12 else 0.0
