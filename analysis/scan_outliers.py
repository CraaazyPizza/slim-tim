"""Sweep all extracted frames for subliminal-flash outliers.

For each video's frame dir: load every PNG downscaled, compute mean luma,
mean saturation (max(RGB)-min(RGB)), and abs diff vs previous frame.
Flag frames whose luma or saturation jumps >5 sigma from a rolling context,
i.e. single/few-frame inserts that differ hugely from neighbours.
"""
import numpy as np, os, sys
from PIL import Image

dirs = {
    'OpSTlDJWFFI': 'frames/OpSTlDJWFFI',
    'Oqw96jCOP7A': 'frames/Oqw96jCOP7A',
    'l9RAhmPHM_A': 'frames/l9RAhmPHM_A',
}

for vid, d in dirs.items():
    files = sorted(os.listdir(d))
    luma = np.zeros(len(files)); sat = np.zeros(len(files))
    prev = None; diff = np.zeros(len(files))
    for i, fn in enumerate(files):
        a = np.asarray(Image.open(os.path.join(d, fn)).convert('RGB').resize((96, 54)), float)
        luma[i] = (0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]).mean()
        sat[i] = (a.max(2)-a.min(2)).mean()
        diff[i] = 0.0 if prev is None else np.abs(a-prev).mean()
        prev = a
    np.save(f'analysis/stats_{vid}.npy', np.stack([luma, sat, diff]))
    # rolling-median outlier detection, window 91
    win = 45
    flags = []
    for i in range(len(files)):
        lo, hi = max(0, i-win), min(len(files), i+win+1)
        ctx = np.concatenate([luma[lo:i], luma[i+1:hi]])
        ctxs = np.concatenate([sat[lo:i], sat[i+1:hi]])
        ml, sl = np.median(ctx), np.median(np.abs(ctx-np.median(ctx))) + 1e-6
        ms, ss = np.median(ctxs), np.median(np.abs(ctxs-np.median(ctxs))) + 1e-6
        zl = abs(luma[i]-ml)/(1.4826*sl); zs = abs(sat[i]-ms)/(1.4826*ss)
        if zl > 8 or zs > 8:
            flags.append((i+1, round(zl,1), round(zs,1), round(luma[i],1), round(sat[i],1)))
    print(f'== {vid}: {len(files)} frames, {len(flags)} outliers (frame#, z_luma, z_sat, luma, sat)')
    # merge consecutive runs
    runs = []
    for f in flags:
        if runs and f[0] == runs[-1][-1][0]+1: runs[-1].append(f)
        else: runs.append([f])
    for r in runs:
        t0, t1 = (r[0][0]-1)/29.97, (r[-1][0]-1)/29.97
        print(f'  frames {r[0][0]}-{r[-1][0]}  t={t0:.2f}-{t1:.2f}s  peak z_luma={max(x[1] for x in r)} z_sat={max(x[2] for x in r)}')
    sys.stdout.flush()
