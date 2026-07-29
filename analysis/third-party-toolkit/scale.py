#!/usr/bin/env python3.12
"""Scale references + exhaustive tile-corner scan."""
import os, numpy as np
from PIL import Image
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
LC = lc_map(); ns = sorted(LC)
def A(p): return np.asarray(Image.open(p).convert("RGB"), dtype=np.uint8)
def O(n): return A(f"{OURS}/f{n:05d}.png")
def rms(a,b):
    d=a.astype(np.float32)-b.astype(np.float32); return float(np.sqrt((d*d).mean()))

print("="*80)
print("SCALE REFERENCE: how big is 'RMS 2' really?")
print("="*80)
print(f"{'frame':>6} {'LC[n] vs ours[n]':>18} {'ours[n] vs ours[n+1]':>22} {'LC[n] vs ours[n+1]':>20} {'LC[n] vs ours[n+15]':>21}")
for n in [400, 1100, 1400, 1700, 2000, 2300, 2500]:
    if n not in LC: continue
    a=A(LC[n]); b=O(n)
    try: b1=O(n+1); b15=O(n+15)
    except Exception: continue
    print(f"{n:6d} {rms(a,b):18.4f} {rms(b,b1):22.4f} {rms(a,b1):20.4f} {rms(a,b15):21.4f}")

print()
print("="*80)
print("EXHAUSTIVE AV1 TILE-CORNER SCAN over every LC frame carved")
print("="*80)
print("For each frame, does the 32x32 block at (0,0)/(960,0) sit ABOVE its local")
print("surroundings the way the AV1 artifact forces?  Reported: count of LC frames")
print("where LC's tile blocks differ from ours, and the total artifact accounting.")
nlc_flat = nours_art = both = 0
onlyours = []
for n in ns:
    if n % 7: continue
    a = A(LC[n]); b = O(n)
    ab = np.concatenate([a[0:32,0:32].ravel(), a[0:32,960:992].ravel()])
    bb = np.concatenate([b[0:32,0:32].ravel(), b[0:32,960:992].ravel()])
    # is the whole frame near-black?
    if b.max() <= 2 and a.max() <= 2:
        nours_art += int((bb == 1).all())
        nlc_flat += int((ab == 0).all())
        both += 1
print(f"near-black frames tested (both sets, every 7th): {both}")
print(f"  ours: tile blocks entirely ==1 (artifact present): {nours_art}/{both}")
print(f"  LC  : tile blocks entirely ==0 (artifact absent) : {nlc_flat}/{both}")

print()
print("For those frames, the FULL-FRAME difference is confined to the tile blocks:")
cnt = 0
for n in ns:
    if n % 7: continue
    a = A(LC[n]); b = O(n)
    if not (b.max() <= 2 and a.max() <= 2): continue
    d = (a.astype(np.int16) - b.astype(np.int16))
    ys, xs = np.where(np.abs(d).max(axis=2) > 0)
    inblk = np.sum(((xs < 32) | ((xs >= 960) & (xs < 992))) & (ys < 32))
    if cnt < 12:
        print(f"  f{n:5d}: {len(xs):6d} differing px, {inblk} inside tile corners, {len(xs)-inblk} outside")
    cnt += 1
print(f"  ({cnt} such frames total)")
