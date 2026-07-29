"""Stage 2: refine the top stage-1 candidates with a finer (cap, kx, sigma) grid,
then compute per-glyph NCC scores for the winner."""
import numpy as np, json, sys, time
sys.path.insert(0, '/home/user/new-skinny-bob/analysis/cyrillic/mk5-captions')
from typeface_fit import (OUT, TEXT, OBS, OBSc, OBS_NORM, H, W, FONTS,
                           render_ink, capsize_for_target, stretch, place, prep,
                           best_shift_ncc, PSF_SIGMA_MEASURED)

stage1 = json.load(open(OUT+'typeface_stage1.json'))
stage1.sort(key=lambda d: -d['r'])
TOP = stage1[:15]

CAP_SIZES = list(range(72, 96, 3))          # finer cap-height grid around 84
KXS = [round(x,2) for x in np.arange(0.75, 1.35, 0.05)]
SIGMAS = [1.8, 2.2, 2.55, 3.0, 3.5]

def fit_font_fine(fp):
    best = None
    for cap in CAP_SIZES:
        s0 = capsize_for_target(fp, cap)
        if s0 is None:
            continue
        try:
            ink0 = render_ink(fp, TEXT, s0)
        except Exception:
            continue
        for kx in KXS:
            ink = stretch(ink0, kx)
            for sig in SIGMAS:
                from scipy.ndimage import gaussian_filter as gf
                blurred = gf(ink, sig, truncate=3.0)
                templ = prep(place(blurred, H, W))
                r, dy, dx = best_shift_ncc(templ)
                if best is None or r > best[0]:
                    best = (r, cap, s0, kx, sig, dy, dx)
    return best

t0 = time.time()
results2 = []
for d in TOP:
    b = fit_font_fine(d['file'])
    if b is None:
        continue
    r, cap, size, kx, sig, dy, dx = b
    results2.append(dict(font=d['font'], file=d['file'], r=r, cap=cap, size=size, kx=kx, sigma=sig, dy=dy, dx=dx))
    print('%-40s r=%.4f cap=%3d size=%3d kx=%.2f sig=%.2f' % (d['font'], r, cap, size, kx, sig), flush=True)

results2.sort(key=lambda x: -x['r'])
json.dump(results2, open(OUT+'typeface_stage2.json','w'), indent=1, ensure_ascii=False)
print('STAGE2 done, %.0fs' % (time.time()-t0), flush=True)

# kx spread across top-5 stage2 candidates -> report as "kx with uncertainty"
kxs_top = np.array([d['kx'] for d in results2[:5]])
print('top-5 stage2 kx: mean=%.3f std=%.3f  values=%s' % (kxs_top.mean(), kxs_top.std(), kxs_top.tolist()))

# ---- per-glyph scores for the winner ----
winner = results2[0]
fp = winner['file']; size = winner['size']; kx = winner['kx']; sig = winner['sigma']
ink0 = render_ink(fp, TEXT, size)
ink = stretch(ink0, kx)
from scipy.ndimage import gaussian_filter as gf
blurred = gf(ink, sig, truncate=3.0)
templ_full = place(blurred, H, W)
templ = prep(templ_full)
r, dy, dx = best_shift_ncc(templ)
# shift template by (dy,dx) using np.roll (circular, acceptable given zero-padding margins)
templ_shifted = np.roll(np.roll(templ, dy, axis=0), dx, axis=1)

# glyph x-window boundaries in native coords -> convert to OBS-local (X0=780)
X0 = 780
glyph_windows = [
    ('M', 795, 855), ('a', 855, 895), ('r', 895, 920), ('k', 920, 960),
    ('5', 980, 1030), ('(', 1130, 1160), ('1a', 1160, 1180), ('9', 1180, 1230),
    ('6', 1230, 1280), ('1b', 1280, 1310), ('g', 1450, 1490), ('o', 1490, 1545), ('d', 1545, 1605),
]
print('\nper-glyph NCC for winner: %s (size=%d kx=%.2f sigma=%.2f)' % (winner['font'], size, kx, sig))
for name, xa, xb in glyph_windows:
    ca = max(0, xa-X0); cb = min(W, xb-X0)
    if cb <= ca:
        continue
    o = OBSc[:, ca:cb]; t = templ_shifted[:, ca:cb]
    o0 = o - o.mean(); t0v = t - t.mean()
    n = np.sqrt((o0**2).sum()*(t0v**2).sum())
    ncc = float((o0*t0v).sum()/n) if n > 1e-9 else float('nan')
    print('  %-4s x=%4d-%4d  ncc=%.3f' % (name, xa, xb, ncc))
