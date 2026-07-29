#!/usr/bin/env python3.12
"""Exclusive block-boundary analysis: isolate which grid period each source really carries."""
import os, numpy as np
from PIL import Image
SCR = "/tmp/claude-1001/-home-user-new-skinny-bob/6c2508df-43ca-4f35-aaa6-0d27ef73c55d/scratchpad/ctrl"
BASE = "/home/user/new-skinny-bob/analysis/third-party-toolkit/extracted/2026-05-25_Confidential leaked ufo-ebe footage continuation of disclosure"
OURS = "/home/user/new-skinny-bob/frames/OpSTlDJWFFI"
def lc_map():
    d = {}
    for dp in sorted(os.listdir(BASE)):
        fp = os.path.join(BASE, dp)
        if not os.path.isdir(fp): continue
        for f in sorted(os.listdir(fp)):
            if f.endswith(".png"): d[int(f.split("_")[1].split(".")[0])] = os.path.join(fp, f)
    return d
LC = lc_map()
def A(p): return np.asarray(Image.open(p).convert("RGB"), dtype=np.uint8)
def L(im): return np.asarray(Image.fromarray(im).convert("L"), dtype=np.float32)

FR = [400, 1000, 1100, 1200, 1400, 1050, 1150, 1250, 1350]
srcs = [("LC", lambda n: A(LC[n])),
        ("ours(YT AV1)", lambda n: A(f"{OURS}/f{n:05d}.png")),
        ("ctrl h264", lambda n: A(f"{SCR}/h264_frames/f{n:05d}.png")),
        ("ctrl vp9", lambda n: A(f"{SCR}/vp9_frames/f{n:05d}.png"))]

def excl_profile(im):
    """mean |dx| at columns whose boundary class is exactly p (multiple of p, not of 2p),
       normalised by the mean at non-multiples-of-4 columns."""
    g = L(im); dh = np.abs(np.diff(g, axis=1)); c = np.arange(dh.shape[1]) + 1
    base = dh[:, c % 4 != 0].mean()
    out = {}
    for p in (4, 8, 16, 32, 64, 128):
        m = (c % p == 0) & (c % (2*p) != 0) if p < 128 else (c % 128 == 0)
        out[p] = dh[:, m].mean() / base if base else np.nan
    return out

print("EXCLUSIVE boundary strength, normalised to non-4-multiple columns")
print("(value at p counts columns that are multiples of p but NOT of 2p)")
print(f"{'source':>13} " + " ".join(f"{'x'+str(p):>8}" for p in (4,8,16,32,64,128)))
agg = {t: [] for t, _ in srcs}
for n in FR:
    for t, g in srcs:
        pr = excl_profile(g(n)); agg[t].append([pr[p] for p in (4,8,16,32,64,128)])
print(" -- per-frame --")
for i, n in enumerate(FR):
    print(f" frame {n}")
    for t, _ in srcs:
        print(f"{t:>13} " + " ".join(f"{x:8.3f}" for x in agg[t][i]))
print("\n -- MEAN over all %d frames --" % len(FR))
for t, _ in srcs:
    m = np.mean(agg[t], axis=0)
    print(f"{t:>13} " + " ".join(f"{x:8.3f}" for x in m))
print("\nInterpretation key:")
print("  H.264  : 16x16 macroblocks -> plateau, all multiples of 16 roughly EQUAL")
print("  VP9    : 64x64 superblocks -> rises to 64")
print("  AV1    : 128x128 superblocks -> rises to 128")

print("\n" + "="*90)
print("GRID SIGNATURE OF THE DIFFERENCE IMAGE (LC - X)")
print("="*90)
print("If LC were a *master* and ours a YouTube encode of it, the difference would carry")
print("only OUR codec's grid. If both are sibling YouTube renditions, the difference")
print("carries BOTH grids -- notably LC's 16px one.")
print(f"{'frame':>6} {'pair':>22} " + " ".join(f"{'x'+str(p):>8}" for p in (4,8,16,32,64,128)))
for n in [1000, 1100, 1200, 1400]:
    a = A(LC[n]).astype(np.float32)
    for t, g in srcs[1:]:
        d = np.abs(a - g(n).astype(np.float32)).mean(axis=2).astype(np.float32)
        dh = np.abs(np.diff(d, axis=1)); c = np.arange(dh.shape[1]) + 1
        base = dh[:, c % 4 != 0].mean()
        row = []
        for p in (4,8,16,32,64,128):
            m = (c % p == 0) & (c % (2*p) != 0) if p < 128 else (c % 128 == 0)
            row.append(dh[:, m].mean()/base)
        print(f"{n:6d} {'LC-'+t:>22} " + " ".join(f"{x:8.3f}" for x in row))
    print()
