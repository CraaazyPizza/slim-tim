#!/usr/bin/env python3.12
"""Quick visual: row-mean profile of a single frame, detrended and stretched,
rendered as a tall thin image replicated horizontally, for visual banding check."""
import numpy as np, sys, os
from PIL import Image
B = "/home/user/new-skinny-bob"
O = B + "/analysis/compare-eras/band/peek"
os.makedirs(O, exist_ok=True)
SPEC = [
 ("frames/OpSTlDJWFFI", 1500), ("frames/Oqw96jCOP7A", 1250), ("frames/l9RAhmPHM_A", 2000),
 ("frames/ZB788PtqQvg", 350),
 ("frames/RsQCXN4o4Ps", 720),
 ("frames/Xju_CY5ZESA", 700),
 ("frames/a6TLGkrfNKI", 700),
]
for d, n in SPEC:
    p = f"{B}/{d}/f{n:05d}.png"
    im = np.asarray(Image.open(p).convert("L")).astype(np.float32)
    H, W = im.shape
    # central 50% columns
    c0, c1 = int(W*0.30), int(W*0.70)
    prof = im[:, c0:c1].mean(axis=1)
    # detrend with 31-tap moving average
    k = 31
    pad = np.pad(prof, k//2, mode="reflect")
    tr = np.convolve(pad, np.ones(k)/k, mode="valid")
    det = prof - tr
    print(f"{os.path.basename(d)} f{n} H={H} W={W} prof[400:420]="
          + " ".join(f"{v:.2f}" for v in prof[400:420]))
    print(f"   detrended std={det.std():.4f} ptp={np.ptp(det):.3f} "
          f"first20=" + " ".join(f"{v:+.2f}" for v in det[400:420]))
    # image: 12x amplified detrended profile
    vis = np.clip(128 + det[:, None]*16, 0, 255).astype(np.uint8)
    Image.fromarray(np.repeat(vis, 60, axis=1)).save(f"{O}/{os.path.basename(d)}_prof.png")
