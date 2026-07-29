#!/usr/bin/env python3.12
"""Decode burned-in overlay strings for the 2011 videos, window by window."""
import os, sys, glob, json
import numpy as np
from PIL import Image, ImageDraw

os.chdir(os.path.dirname(os.path.abspath(__file__)))

BANDS = {
    'ZB788PtqQvg': (930, 995, 260, 1240),
    'RsQCXN4o4Ps': (930, 995, 260, 1240),
}
WIN = 6
GH, GW = 40, 26


def stretch(a, lo=3, hi=99.7):
    a = a.astype(float)
    l, h = np.percentile(a, [lo, hi])
    if h - l < 6:
        return None
    return np.clip((a - l) / (h - l), 0, 1)


def segment(st):
    m = st > 0.72
    if m.sum() < 40:
        return []
    rows = m.sum(axis=1)
    rr = np.where(rows >= 3)[0]
    if len(rr) == 0:
        return []
    # main text band: rows 0..len; take the contiguous block with most ink
    cols = m.sum(axis=0)
    on = cols >= 2
    runs = []
    i, n = 0, len(on)
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]:
                j += 1
            if 5 <= j - i <= 70:
                runs.append((i, j))
            i = j
        else:
            i += 1
    out = []
    for a, b in runs:
        sub = m[:, a:b]
        r = np.where(sub.sum(axis=1) > 0)[0]
        if len(r) < 5:
            continue
        ra, rb = r[0], r[-1] + 1
        patch = st[ra:rb, a:b]
        g = np.array(Image.fromarray((patch * 255).astype('uint8')).resize((GW, GH), Image.BILINEAR)) / 255.0
        out.append(dict(a=a, b=b, ra=int(ra), rb=int(rb), g=g.astype(np.float32)))
    return out


def build(v):
    y0, y1, x0, x1 = BANDS[v]
    fs = sorted(glob.glob(f'frames2011/{v}/*.png'))
    arr = np.stack([np.array(Image.open(f).convert('L'))[y0:y1, x0:x1] for f in fs]).astype(np.float32)
    wins = []
    for s in range(0, len(arr), WIN):
        w = arr[s:s + WIN]
        if len(w) < 3:
            continue
        st = stretch(np.median(w, axis=0))
        if st is None:
            continue
        gs = segment(st)
        if len(gs) < 5:
            continue
        wins.append(dict(f0=s + 1, f1=s + len(w), st=st.astype(np.float32), gs=gs))
    print(v, 'windows with text:', len(wins))
    return wins


def ncc(a, b):
    a = a - a.mean(); b = b - b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 1e-9 else 0.0


def cluster_all(wins, thr=0.93):
    allg = [(wi, gi, g['g']) for wi, w in enumerate(wins) for gi, g in enumerate(w['gs'])]
    cents, cnts, asg = [], [], []
    for wi, gi, g in allg:
        best, bi = -2, -1
        for k in range(len(cents)):
            s = ncc(g, cents[k] / cnts[k])
            if s > best:
                best, bi = s, k
        if best >= thr:
            cents[bi] += g; cnts[bi] += 1; asg.append(bi)
        else:
            cents.append(g.copy()); cnts.append(1); asg.append(len(cents) - 1)
    C = [c / n for c, n in zip(cents, cnts)]
    return allg, np.array(asg), C, np.array(cnts)


if __name__ == '__main__':
    v = sys.argv[1]
    wins = build(v)
    allg, asg, C, cnts = cluster_all(wins)
    print('clusters', len(C))
    order = np.argsort(-cnts)
    cols = 12
    rows = (len(C) + cols - 1) // cols
    CW, CH = 56, 86
    sh = Image.new('L', (cols * CW, rows * CH), 0)
    dr = ImageDraw.Draw(sh)
    for j, k in enumerate(order):
        im = Image.fromarray((np.clip(C[k], 0, 1) * 255).astype('uint8')).resize((36, 55), Image.LANCZOS)
        x, y = (j % cols) * CW, (j // cols) * CH
        sh.paste(im, (x + 10, y + 26))
        dr.text((x + 3, y + 5), f'{k}/{cnts[k]}', fill=255)
    sh.resize((cols * CW * 2, rows * CH * 2), Image.LANCZOS).save(f'sheets/dec_clusters_{v}.png')
    np.save(f'dec_{v}_asg.npy', asg)
    with open(f'dec_{v}_wins.json', 'w') as fh:
        json.dump([dict(f0=w['f0'], f1=w['f1'], boxes=[[g['a'], g['b'], g['ra'], g['rb']] for g in w['gs']]) for w in wins], fh)
    np.savez_compressed(f'dec_{v}_cent.npz', C=np.array(C), cnts=cnts,
                        idx=np.array([[a, b] for a, b, _ in allg]))
    print('order', list(order))
