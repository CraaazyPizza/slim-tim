#!/usr/bin/env python3.12
import os, sys
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
            if f.endswith(".png"):
                d[int(f.split("_")[1].split(".")[0])] = os.path.join(fp, f)
    return d

def arr(p): return np.asarray(Image.open(p).convert("RGB"), dtype=np.uint8)

LC = lc_map()
cache = {}
def ours(n):
    p = os.path.join(OURS, f"f{n:05d}.png")
    if not os.path.exists(p): return None
    if p not in cache:
        if len(cache) > 120: cache.clear()
        cache[p] = arr(p)
    return cache[p]

def rms(a, b):
    d = a.astype(np.float32) - b.astype(np.float32)
    return float(np.sqrt((d * d).mean()))

# probe frames chosen in high-motion / content-rich regions
probes = [int(x) for x in sys.argv[1:]] or [300, 600, 918, 1000, 1100, 1200, 1300, 1400]
RANGE = range(-40, 41)
print("probe   best_off   best_rms   rms@0    2nd_best_off/rms")
for n in probes:
    if n not in LC: continue
    a = arr(LC[n])
    res = []
    for off in RANGE:
        b = ours(n + off)
        if b is None or b.shape != a.shape: continue
        res.append((rms(a, b), off))
    res.sort()
    r0 = [r for r in res if r[1] == 0]
    print(f"{n:5d}   {res[0][1]:+4d}   {res[0][0]:9.4f}   {r0[0][0] if r0 else float('nan'):8.4f}   {res[1][1]:+4d}/{res[1][0]:.4f}")
