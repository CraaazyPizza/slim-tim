#!/usr/bin/env python3.12
"""Discriminators: AV1 tile-corner artifact, block-grid energy, duplicate-beat, detail level."""
import os, hashlib, json
import numpy as np
from PIL import Image

BASE = "/home/user/new-skinny-bob/analysis/third-party-toolkit/extracted/2026-05-25_Confidential leaked ufo-ebe footage continuation of disclosure"
OURS = "/home/user/new-skinny-bob/frames/OpSTlDJWFFI"

def lc_map():
    d = {}
    for dirp in sorted(os.listdir(BASE)):
        fp = os.path.join(BASE, dirp)
        if not os.path.isdir(fp): continue
        for f in sorted(os.listdir(fp)):
            if f.endswith(".png"): d[int(f.split("_")[1].split(".")[0])] = os.path.join(fp, f)
    return d
LC = lc_map()
def A(p): return np.asarray(Image.open(p).convert("RGB"), dtype=np.uint8)
def O(n): return A(os.path.join(OURS, f"f{n:05d}.png"))

print("="*78)
print("TEST 1 — AV1 tile-corner artifact on near-black frames")
print("="*78)
print("FINDINGS 13: our AV1 v1 black frames are flat Y=16 except 2048 px at Y=17,")
print("two solid 32x32 blocks at (0,0) and (960,0) (the 2-tile-column AV1 grid).")
for n in [1, 3, 5, 8, 10, 910, 913, 915, 916]:
    if n not in LC: continue
    a, b = A(LC[n]), O(n)
    for tag, im in (("LC  ", a), ("ours", b)):
        vals, cnt = np.unique(im, return_counts=True)
        blkA = im[0:32, 0:32]; blkB = im[0:32, 960:992]
        rest = im.copy(); rest[0:32, 0:32] = 0; rest[0:32, 960:992] = 0
        nz = np.count_nonzero(im != np.bincount(im.ravel()).argmax())
        print(f" f{n:5d} {tag}: uniq={dict(zip(vals.tolist(),cnt.tolist())) if len(vals)<=6 else str(len(vals))+' vals'}"
              f" blk(0,0)uniq={np.unique(blkA).tolist()[:4]} blk(0,960)uniq={np.unique(blkB).tolist()[:4]} npx!=mode={nz}")
    d = a.astype(np.int16) - b.astype(np.int16)
    ys, xs = np.where(np.abs(d).max(axis=2) > 0)
    if len(xs):
        print(f"        diff pixels: {len(xs)}  x[{xs.min()}..{xs.max()}] y[{ys.min()}..{ys.max()}]"
              f"  in blk(0,0)={np.sum((xs<32)&(ys<32))} in blk(960)={np.sum((xs>=960)&(xs<992)&(ys<32))}"
              f"  elsewhere={np.sum(~(((xs<32)|((xs>=960)&(xs<992)))&(ys<32)))}")
    print()

print("="*78)
print("TEST 2 — block-grid energy of each image (codec transform-block signature)")
print("="*78)
def gridenergy(im, period):
    g = np.asarray(Image.fromarray(im).convert("L"), dtype=np.float32)
    dh = np.abs(np.diff(g, axis=1))          # horizontal gradient, column j = |g[:,j+1]-g[:,j]|
    cols = np.arange(dh.shape[1])
    on = dh[:, (cols + 1) % period == 0].mean()
    off = dh[:, (cols + 1) % period != 0].mean()
    return on / off if off else float('nan')
print("ratio = mean|grad| ON block boundary / OFF boundary  (>1 = blocking at that period)")
print(f"{'frame':>7} {'src':>5} " + " ".join(f"p={p:<3d}" for p in (4,8,16,32,64,128)))
for n in [400, 700, 1000, 1200, 1400]:
    for tag, im in (("LC", A(LC[n])), ("ours", O(n))):
        print(f"{n:7d} {tag:>5} " + " ".join(f"{gridenergy(im,p):5.3f}" for p in (4,8,16,32,64,128)))

print()
print("="*78)
print("TEST 3 — the 12-frame duplicate beat (FINDINGS 11) in each set")
print("="*78)
for lo, hi in [(200, 260), (1000, 1060), (1350, 1410)]:
    for tag, get in (("LC  ", lambda n: A(LC[n])), ("ours", O)):
        hs = [hashlib.md5(get(n).tobytes()).hexdigest()[:8] for n in range(lo, hi)]
        dup = [n for i, n in enumerate(range(lo, hi)) if i and hs[i] == hs[i-1]]
        # group run lengths
        runs = []
        cur = 1
        for i in range(1, len(hs)):
            if hs[i] == hs[i-1]: cur += 1
            else: runs.append(cur); cur = 1
        runs.append(cur)
        print(f" {lo}-{hi} {tag}: n_distinct={len(set(hs))}/{len(hs)} runlens={runs}")
    print()

print("="*78)
print("TEST 4 — detail / noise level: which set is 'cleaner'?")
print("="*78)
print("If LC had a pre-YouTube master, LC would carry detail ours lost.")
print("laplacian variance (detail+noise), and local high-freq energy:")
K = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]], dtype=np.float32)
def lapvar(im):
    g = np.asarray(Image.fromarray(im).convert("L"), dtype=np.float32)
    out = (4*g[1:-1,1:-1] - g[:-2,1:-1] - g[2:,1:-1] - g[1:-1,:-2] - g[1:-1,2:])
    return float(out.var()), float(np.abs(out).mean())
print(f"{'frame':>7} {'LC lapvar':>12} {'ours lapvar':>12} {'LC |lap|':>10} {'ours |lap|':>11}  {'ratio(LC/ours) var':>18}")
for n in [100, 300, 500, 700, 900, 1000, 1100, 1200, 1300, 1400]:
    lv, lm = lapvar(A(LC[n])); ov, om = lapvar(O(n))
    print(f"{n:7d} {lv:12.3f} {ov:12.3f} {lm:10.4f} {om:11.4f}  {lv/ov if ov else 0:18.4f}")

print()
print("="*78)
print("TEST 5 — is 'ours' = 'LC' + noise, or symmetric? (third-party reference test)")
print("="*78)
print("Compare each to a strongly-blurred common estimate; whichever is closer to")
print("a *shared* low-frequency core is not informative, so instead: check whether the")
print("LC-ours difference correlates with local image activity (codec-noise signature).")
for n in [400, 1000, 1200, 1400]:
    a, b = A(LC[n]).astype(np.float32), O(n).astype(np.float32)
    d = np.abs(a - b).mean(axis=2)
    g = np.asarray(Image.fromarray(O(n)).convert("L"), dtype=np.float32)
    act = np.abs(np.gradient(g)[0]) + np.abs(np.gradient(g)[1])
    # blockwise 16x16 means
    H, W = 1080//16*16, 1920//16*16
    db = d[:H,:W].reshape(H//16,16,W//16,16).mean(axis=(1,3)).ravel()
    ab = act[:H,:W].reshape(H//16,16,W//16,16).mean(axis=(1,3)).ravel()
    r = np.corrcoef(db, ab)[0,1]
    print(f" f{n}: corr(|LC-ours| , local activity) = {r:+.4f}   "
          f"flat-region mean|d| = {db[ab<np.percentile(ab,10)].mean():.4f}  "
          f"busy-region mean|d| = {db[ab>np.percentile(ab,90)].mean():.4f}")
