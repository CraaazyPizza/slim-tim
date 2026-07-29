#!/usr/bin/env python3.12
"""Render a labelled vertical strip of per-frame timecode crops."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw

os.chdir(os.path.dirname(os.path.abspath(__file__)))
BANDS = {
    'ZB788PtqQvg': (930, 995, 600, 1240),
    'RsQCXN4o4Ps': (930, 995, 600, 1240),
}


def main(v, a, b, step, tag, smooth=3):
    y0, y1, x0, x1 = BANDS[v]
    idxs = list(range(a, b + 1, step))
    CW, CH = x1 - x0, y1 - y0
    sh = Image.new('L', (CW + 150, CH * len(idxs)), 0)
    dr = ImageDraw.Draw(sh)
    for j, i in enumerate(idxs):
        stack = []
        for k in range(i, min(i + smooth, b + 1)):
            try:
                stack.append(np.array(Image.open(f'frames2011/{v}/f{k:05d}.png').convert('L'))[y0:y1, x0:x1])
            except FileNotFoundError:
                pass
        if not stack:
            continue
        c = np.median(np.stack(stack).astype(float), axis=0)
        lo, hi = np.percentile(c, [3, 99.7])
        c = np.clip((c - lo) / max(hi - lo, 1), 0, 1) * 255
        sh.paste(Image.fromarray(c.astype('uint8')), (150, j * CH))
        dr.text((6, j * CH + CH // 2 - 6), f'f{i}', fill=255)
    sh.resize(((CW + 150) * 2, CH * len(idxs) * 2), Image.LANCZOS).save(f'sheets/strip_{tag}.png')
    print('sheets/strip_%s.png' % tag, sh.size, idxs[0], idxs[-1])


if __name__ == '__main__':
    v, a, b, step, tag = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    sm = int(sys.argv[6]) if len(sys.argv) > 6 else 3
    main(v, a, b, step, tag, sm)
