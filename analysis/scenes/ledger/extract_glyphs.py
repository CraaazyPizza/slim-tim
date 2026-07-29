#!/usr/bin/env python3.12
"""Extract burned-in timecode glyphs from 2011 ivan0135 frames.

Stage 1: for every frame, crop the overlay band, contrast-stretch, binarize,
find glyph bounding boxes, save normalized glyph patches + geometry to npz.
"""
import sys, glob, os
import numpy as np
from PIL import Image

BANDS = {  # video -> (y0,y1,x0,x1) generous crop of overlay band
    'ZB788PtqQvg': (925, 1000, 250, 1250),
    'RsQCXN4o4Ps': (925, 1000, 250, 1250),
    'Xju_CY5ZESA': (925, 1000, 250, 1250),
    'a6TLGkrfNKI': (410, 455, 100, 560),
}

GH, GW = 40, 28  # normalized glyph size


def stretch(a):
    a = a.astype(float)
    lo, hi = np.percentile(a, [3, 99.7])
    if hi - lo < 8:
        return None
    return np.clip((a - lo) / (hi - lo), 0, 1)


def frame_glyphs(path, band):
    y0, y1, x0, x1 = band
    im = np.array(Image.open(path).convert('L'))
    c = im[y0:y1, x0:x1]
    s = stretch(c)
    if s is None:
        return None
    # text is the brightest thing in the band
    thr = 0.72
    m = s > thr
    # require a plausible text row block
    rows = m.sum(axis=1)
    if rows.max() < 4:
        return None
    # column runs
    cols = m.sum(axis=0)
    on = cols >= 2
    runs = []
    i = 0
    n = len(on)
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]:
                j += 1
            if 4 <= j - i <= 60:
                runs.append((i, j))
            i = j
        else:
            i += 1
    out = []
    for (a, b) in runs:
        sub = m[:, a:b]
        r = np.where(sub.sum(axis=1) > 0)[0]
        if len(r) == 0:
            continue
        ra, rb = r[0], r[-1] + 1
        if rb - ra < 4:
            continue
        patch = s[ra:rb, a:b]
        g = np.array(Image.fromarray((patch * 255).astype('uint8')).resize((GW, GH), Image.BILINEAR)) / 255.0
        out.append(dict(x0=a + x0, x1=b + x0, y0=ra + y0, y1=rb + y0, g=g))
    return out


def main(video):
    band = BANDS[video]
    fs = sorted(glob.glob(f'frames2011/{video}/*.png'))
    recs = []
    for k, f in enumerate(fs):
        idx = int(os.path.basename(f)[1:6])
        gl = frame_glyphs(f, band)
        if gl:
            recs.append((idx, gl))
    print(video, 'frames with glyphs:', len(recs), '/', len(fs))
    glyphs = []
    meta = []
    for idx, gl in recs:
        for g in gl:
            glyphs.append(g['g'])
            meta.append((idx, g['x0'], g['x1'], g['y0'], g['y1']))
    np.savez_compressed(f'glyphs_{video}.npz', g=np.array(glyphs, dtype=np.float32),
                        m=np.array(meta, dtype=np.int32))
    print('  glyphs:', len(glyphs))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for v in (sys.argv[1:] or list(BANDS)):
        main(v)
