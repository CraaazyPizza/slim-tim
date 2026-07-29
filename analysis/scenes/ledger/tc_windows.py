#!/usr/bin/env python3.12
"""Temporal-median the overlay band in short windows, dedupe, emit readable sheets."""
import os, sys, glob
import numpy as np
from PIL import Image, ImageDraw

os.chdir(os.path.dirname(os.path.abspath(__file__)))

BANDS = {
    'ZB788PtqQvg': (930, 995, 260, 1240),
    'RsQCXN4o4Ps': (930, 995, 260, 1240),
}
WIN = 12


def stretch(a, lo=3, hi=99.7):
    a = a.astype(float)
    l, h = np.percentile(a, [lo, hi])
    if h - l < 6:
        return None
    return np.clip((a - l) / (h - l), 0, 1)


def run(v):
    y0, y1, x0, x1 = BANDS[v]
    fs = sorted(glob.glob(f'frames2011/{v}/*.png'))
    n = len(fs)
    arr = np.stack([np.array(Image.open(f).convert('L'))[y0:y1, x0:x1] for f in fs]).astype(np.float32)
    outs = []
    for s in range(0, n, WIN):
        w = arr[s:s + WIN]
        if len(w) < 4:
            continue
        med = np.median(w, axis=0)
        st = stretch(med)
        if st is None:
            continue
        # text presence: fraction of very bright pixels
        if (st > 0.85).sum() < 60:
            continue
        outs.append((s + 1, s + len(w), st))
    # dedupe consecutive
    keep = []
    for rec in outs:
        if keep:
            a = keep[-1][2]; b = rec[2]
            am = a - a.mean(); bm = b - b.mean()
            r = (am * bm).sum() / (np.sqrt((am ** 2).sum() * (bm ** 2).sum()) + 1e-9)
            if r > 0.965 and rec[0] - keep[-1][1] <= WIN:
                # merge: extend range
                keep[-1] = (keep[-1][0], rec[1], keep[-1][2])
                continue
        keep.append(list(rec))
        keep[-1] = tuple(keep[-1])
        keep[-1] = (rec[0], rec[1], rec[2])
    print(v, 'windows', len(outs), '-> deduped', len(keep))
    # sheets
    CW, CH = x1 - x0, y1 - y0
    per = 12
    for si in range(0, len(keep), per):
        chunk = keep[si:si + per]
        sh = Image.new('L', (CW + 190, CH * len(chunk)), 0)
        dr = ImageDraw.Draw(sh)
        for j, (a, b, st) in enumerate(chunk):
            sh.paste(Image.fromarray((st * 255).astype('uint8')), (190, j * CH))
            dr.text((6, j * CH + CH // 2 - 6), f'f{a}-{b}', fill=255)
        sh = sh.resize(((CW + 190) * 2, CH * len(chunk) * 2), Image.LANCZOS)
        sh.save(f'sheets/tcwin_{v}_{si//per:02d}.png')
    with open(f'tcwin_{v}.txt', 'w') as fh:
        for a, b, _ in keep:
            fh.write(f'{a} {b}\n')


for v in (sys.argv[1:] or list(BANDS)):
    run(v)
