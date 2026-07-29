"""
agent_mk5cap core: load native-resolution frames for the Mk.5 colour-clip caption,
build a robust (median, not mean) template of the STATIC caption layer for
SCORING purposes only, and provide per-frame metrics.

Caption band (measured on f2650, gradient-energy row scan):
  rows 915-998 (text ink), control rows 860-900 (no text, same column range,
  same general scene-brightness regime).
Caption x-extent (measured on f2650, gradient-energy column scan): ink from
  x~260 to x~1610. Full sweep range 2560-2705 (covers onset->plateau->fade
  per FINDINGS.md refinement: onset f2603, plateau to ~2664, fade to ~2698).

IMPORTANT: the template built here (median over many frames) is used ONLY to
score/rank individual frames (Tenengrad, RMS-vs-control, leave-one-out NCC).
The evidentiary figures always show a SINGLE unstacked frame, per instructions
to not rely on averaged/stacked composites as primary evidence.
"""
import numpy as np, os
from PIL import Image

D = '/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f%05d.png'
OUT = '/home/user/new-skinny-bob/analysis/cyrillic/mk5-captions/'
FIG = '/home/user/new-skinny-bob/figs/cyrillic/'
os.makedirs(OUT, exist_ok=True); os.makedirs(FIG, exist_ok=True)

ROWS = (915, 998)          # text ink band, full frame y
CTRL_ROWS = (860, 900)     # text-free control band, same x-range
XRANGE = (200, 1700)       # generous; actual ink measured ~260-1610
FRAMES = list(range(2560, 2706))   # sweep range; caption present ~2599-2698

_cache = OUT + 'stack_L.npz'

def _load_gray(f):
    return np.asarray(Image.open(D % f).convert('L'), dtype=np.float64)

def get_stack():
    if os.path.exists(_cache):
        d = np.load(_cache)
        return d['S'], list(d['fr'])
    ims = []
    for f in FRAMES:
        a = _load_gray(f)
        ims.append(a[CTRL_ROWS[0]:ROWS[1], XRANGE[0]:XRANGE[1]])
    S = np.stack(ims).astype(np.float32)
    np.savez_compressed(_cache, S=S, fr=np.array(FRAMES))
    return S, FRAMES

# offsets into the cropped stack coordinate frame
Y0 = CTRL_ROWS[0]
X0 = XRANGE[0]

def sl(rows, xs=XRANGE):
    return (slice(rows[0]-Y0, rows[1]-Y0), slice(xs[0]-X0, xs[1]-X0))

def ncc(a, b):
    a = a - a.mean(); b = b - b.mean()
    n = np.sqrt((a*a).sum() * (b*b).sum())
    return float((a*b).sum()/n) if n > 1e-12 else 0.0
