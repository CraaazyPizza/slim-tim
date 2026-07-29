"""
Task 3: typeface test for the legible portion of the Mk.5 caption, "Mark 5 (1961 год".
Method: render the string in every installed Cyrillic-capable font (fc-list :lang=ru),
allow a FREE horizontal scale kx independent of the vertical (cap) size, degrade through
the PSF measured from this caption's own glyph edges (edge-spread fit, see psf_fit.py /
this script's PSF_SIGMA constant), align by 2-D FFT cross-correlation search, and score
each candidate by normalised cross-correlation (NCC) against the observed ink.

Observed ink: analysis/cyrillic/mk5-captions/hp_2655_region.npy, a local-highpass (background
gaussian sigma=20) residual of the SINGLE frame f2655 (the task-1 best frame), covering
native (x=780-1660, y=900-1010). This is a single-frame measurement, not a stack.
"""
import numpy as np, json, sys, time
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter as gf

OUT = '/home/user/new-skinny-bob/analysis/cyrillic/mk5-captions/'
TEXT = 'Mark 5 (1961 год'   # the VERIFIED legible portion only
PSF_SIGMA_MEASURED = 2.55   # measured on this caption's own edges, sigma in px; std across 7 edges = 1.14
PSF_SIGMA_GRID = [1.5, 2.0, 2.5, 3.0, 3.5, 4.5]  # search a bit around the measured value

HP_BG_SIGMA = 20.0  # matches how OBS was built (gaussian_filter background, sigma 20)

OBS = np.load(OUT + 'hp_2655_region.npy')   # shape (110, 880), native crop (x780:1660, y900:1010)
H, W = OBS.shape
OBSc = OBS - OBS.mean()
OBS_NORM = np.sqrt((OBSc**2).sum())

FONTS = json.load(open(OUT + 'fonts_ru.json'))

def render_ink(fp, text, size):
    f = ImageFont.truetype(fp, size)
    b = f.getbbox(text)
    w = b[2]-b[0]+10; h = b[3]-b[1]+10
    im = Image.new('L', (w, h), 255)
    ImageDraw.Draw(im).text((5-b[0], 5-b[1]), text, font=f, fill=0)
    return 1.0 - np.asarray(im, dtype=np.float64)/255.0   # ink positive

_capheight_cache = {}
def _capheight(fp, s, probe='M6'):
    key = (fp, s)
    if key not in _capheight_cache:
        try:
            b = ImageFont.truetype(fp, s).getbbox(probe)
            _capheight_cache[key] = b[3]-b[1]
        except Exception:
            _capheight_cache[key] = None
    return _capheight_cache[key]

def capsize_for_target(fp, target_cap_px, probe='M6'):
    """font size (px) whose cap-height bbox equals target_cap_px. Most fonts scale
    linearly (cap_height ~ k*size), so probe twice and interpolate, then a couple of
    local refinement steps -- far cheaper than a full linear scan."""
    s1 = 100
    c1 = _capheight(fp, s1, probe)
    if c1 is None or c1 <= 0:
        return None
    s2 = max(10, int(round(s1*target_cap_px/c1)))
    c2 = _capheight(fp, s2, probe)
    if c2 is None:
        return s2
    best = (s2, abs(c2-target_cap_px))
    # one Newton-ish refinement using the two-point slope
    if c2 != c1 and s2 != s1:
        slope = (c2-c1)/(s2-s1)
        if abs(slope) > 1e-6:
            s3 = int(round(s2 + (target_cap_px-c2)/slope))
            s3 = max(6, min(400, s3))
            c3 = _capheight(fp, s3, probe)
            if c3 is not None and abs(c3-target_cap_px) < best[1]:
                best = (s3, abs(c3-target_cap_px))
    # local search +-3 around best
    for ds in (-3,-2,-1,1,2,3):
        s4 = best[0]+ds
        if s4 < 6: continue
        c4 = _capheight(fp, s4, probe)
        if c4 is not None and abs(c4-target_cap_px) < best[1]:
            best = (s4, abs(c4-target_cap_px))
    return best[0]

_stretch_cache = {}
def stretch(ink, kx):
    h, w = ink.shape
    nw = max(2, int(round(w*kx)))
    im = Image.fromarray((ink*255).astype(np.uint8))
    im = im.resize((nw, h), Image.LANCZOS)
    return np.asarray(im, dtype=np.float64)/255.0

def place(ink, H, W):
    h, w = ink.shape
    out = np.zeros((H, W))
    y0 = (H-h)//2; x0 = (W-w)//2
    ys = slice(max(0,y0), min(H, y0+h)); xs = slice(max(0,x0), min(W, x0+w))
    sy0 = max(0,-y0); sx0 = max(0,-x0)
    out[ys, xs] = ink[sy0:sy0+(ys.stop-ys.start), sx0:sx0+(xs.stop-xs.start)]
    return out

def prep(X):
    return X - gf(X, HP_BG_SIGMA, truncate=3.0)

def best_shift_ncc(template, obs=OBSc, obs_norm=OBS_NORM, rad=25):
    t = template - template.mean()
    n = np.sqrt((t*t).sum())
    if n < 1e-9:
        return 0.0, 0, 0
    F = np.fft.rfft2(obs)
    G = np.fft.rfft2(t)
    cc = np.fft.irfft2(F*np.conj(G), obs.shape)
    cc = np.fft.fftshift(cc)
    c0 = (obs.shape[0]//2, obs.shape[1]//2)
    sub = cc[max(0,c0[0]-rad):c0[0]+rad+1, max(0,c0[1]-rad):c0[1]+rad+1]
    k = np.unravel_index(np.argmax(sub), sub.shape)
    peak = sub[k] / (n*obs_norm)
    dy = k[0]-(sub.shape[0]//2); dx = k[1]-(sub.shape[1]//2)
    return float(peak), int(dy), int(dx)

def fit_font(fp, cap_sizes, kxs, sigmas):
    best = None
    for cap in cap_sizes:
        s0 = capsize_for_target(fp, cap)
        if s0 is None:
            continue
        try:
            ink0 = render_ink(fp, TEXT, s0)
        except Exception:
            continue
        for kx in kxs:
            ink = stretch(ink0, kx)
            for sig in sigmas:
                blurred = gf(ink, sig, truncate=3.0)
                templ = prep(place(blurred, H, W))
                r, dy, dx = best_shift_ncc(templ)
                if best is None or r > best[0]:
                    best = (r, cap, s0, kx, sig, dy, dx)
    return best

if __name__ == '__main__':
    t0 = time.time()
    CAP_SIZES = [60, 72, 84]     # candidate cap-heights in px, coarse stage 1
    KXS = [0.85, 0.95, 1.05, 1.15, 1.25, 1.35, 1.45]
    SIGMAS = [PSF_SIGMA_MEASURED]

    results = []
    items = list(FONTS.items())
    for i, (name, fp) in enumerate(items):
        b = fit_font(fp, CAP_SIZES, KXS, SIGMAS)
        if b is not None:
            r, cap, size, kx, sig, dy, dx = b
            results.append(dict(font=name, file=fp, r=r, cap=cap, size=size, kx=kx, sigma=sig, dy=dy, dx=dx))
        print('...', i+1, '/', len(items), name, 'elapsed', round(time.time()-t0,1), flush=True)
        if (i+1) % 20 == 0:
            json.dump(results, open(OUT+'typeface_stage1.json','w'), indent=1, ensure_ascii=False)
    results.sort(key=lambda d: -d['r'])
    print('STAGE1 done: %d fonts fit, %.0fs' % (len(results), time.time()-t0), flush=True)
    for d in results[:30]:
        print('%-40s r=%.4f cap=%3d size=%3d kx=%.2f sig=%.2f dy=%d dx=%d' % (
            d['font'], d['r'], d['cap'], d['size'], d['kx'], d['sigma'], d['dy'], d['dx']), flush=True)
    json.dump(results, open(OUT+'typeface_stage1.json','w'), indent=1, ensure_ascii=False)
