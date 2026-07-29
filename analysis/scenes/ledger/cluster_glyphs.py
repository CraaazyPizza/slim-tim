#!/usr/bin/env python3.12
import sys, os
import numpy as np
from PIL import Image, ImageDraw

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def load(v):
    d = np.load(f'glyphs_{v}.npz')
    return d['g'], d['m']


def ncc(a, b):
    a = a - a.mean(); b = b - b.mean()
    da = np.sqrt((a * a).sum()); db = np.sqrt((b * b).sum())
    if da < 1e-6 or db < 1e-6:
        return 0.0
    return float((a * b).sum() / (da * db))


def cluster(G, thr=0.90):
    cents = []
    counts = []
    assign = np.zeros(len(G), dtype=int)
    for i, g in enumerate(G):
        best, bi = -2, -1
        for k, c in enumerate(cents):
            s = ncc(g, c / counts[k])
            if s > best:
                best, bi = s, k
        if best >= thr:
            cents[bi] += g
            counts[bi] += 1
            assign[i] = bi
        else:
            cents.append(g.copy())
            counts.append(1)
            assign[i] = len(cents) - 1
    C = np.array([c / n for c, n in zip(cents, counts)])
    return C, np.array(counts), assign


if __name__ == '__main__':
    v = sys.argv[1]
    G, M = load(v)
    C, N, A = cluster(G, float(sys.argv[2]) if len(sys.argv) > 2 else 0.90)
    order = np.argsort(-N)
    print(v, 'clusters:', len(C))
    for k in order:
        print(f'  c{k}: n={N[k]}  meanwidth={np.mean([M[i,2]-M[i,1] for i in range(len(A)) if A[i]==k]):.1f}')
    # render sheet
    cols = 10
    rows = (len(C) + cols - 1) // cols
    CW, CH = 60, 90
    sh = Image.new('L', (cols * CW, rows * CH), 0)
    dr = ImageDraw.Draw(sh)
    for j, k in enumerate(order):
        im = Image.fromarray((np.clip(C[k], 0, 1) * 255).astype('uint8')).resize((40, 58), Image.LANCZOS)
        x, y = (j % cols) * CW, (j // cols) * CH
        sh.paste(im, (x + 10, y + 26))
        dr.text((x + 4, y + 4), f'{k}:{N[k]}', fill=255)
    sh.resize((cols * CW * 2, rows * CH * 2), Image.LANCZOS).save(f'sheets/clusters_{v}.png')
    np.savez_compressed(f'clusters_{v}.npz', C=C, N=N, A=A, M=M)
