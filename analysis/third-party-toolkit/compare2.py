#!/usr/bin/env python3.12
import os, sys, hashlib, json
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
ns = sorted(LC)

rows = []
hist = np.zeros(512, dtype=np.int64)   # signed diff histogram, index = d+255
nbyte = npix = 0
for n in ns:
    if n % 5: continue
    o = os.path.join(OURS, f"f{n:05d}.png")
    if not os.path.exists(o): continue
    pa, pb = LC[n], o
    ba, bb = open(pa, "rb").read(), open(pb, "rb").read()
    a, b = arr(pa), arr(pb)
    if a.shape != b.shape: continue
    fi = hashlib.sha256(ba).digest() == hashlib.sha256(bb).digest()
    d = a.astype(np.int16) - b.astype(np.int16)
    mx = int(np.abs(d).max()); pi = (mx == 0)
    nbyte += fi; npix += pi
    hist += np.bincount((d.ravel() + 255).astype(np.int32), minlength=512)
    rows.append(dict(n=n, file_ident=bool(fi), pix_ident=bool(pi), maxabs=mx,
                     rms=float(np.sqrt((d.astype(np.float64)**2).mean())),
                     mad=float(np.abs(d).mean()),
                     p999=float(np.percentile(np.abs(d), 99.9)),
                     pct_diff=float((np.abs(d) > 0).mean()*100),
                     pct_gt2=float((np.abs(d) > 2).mean()*100),
                     pct_gt8=float((np.abs(d) > 8).mean()*100),
                     pct_gt16=float((np.abs(d) > 16).mean()*100),
                     lc_bytes=len(ba), our_bytes=len(bb)))

print(f"compared {len(rows)} frames (every 5th, n=1..{ns[-1]}), offset 0")
print(f"byte-identical PNG files : {nbyte}/{len(rows)}")
print(f"pixel-identical images   : {npix}/{len(rows)}")
mx = np.array([r['maxabs'] for r in rows]); rm = np.array([r['rms'] for r in rows])
md = np.array([r['mad'] for r in rows]); pd = np.array([r['pct_diff'] for r in rows])
p8 = np.array([r['pct_gt8'] for r in rows]); p16 = np.array([r['pct_gt16'] for r in rows])
def st(name, v, f="%.4f"):
    q = np.percentile(v, [0,5,25,50,75,95,100])
    print(f"{name:12s} " + "  ".join(f"{x:{f[1:]}}" for x in q))
print("\nstat          min      p5      p25     med     p75     p95     max")
st("maxabs", mx, "%8.1f"); st("rms", rm, "%8.4f"); st("mean|d|", md, "%8.4f")
st("%px !=", pd, "%8.3f"); st("%|d|>8", p8, "%8.4f"); st("%|d|>16", p16, "%8.4f")

tot = hist.sum()
print(f"\n=== global signed-diff histogram over {len(rows)} frames, {tot/1e9:.3f} Gpx-channels ===")
cum = 0
for d in range(0, 40):
    c = hist[255+d] + (hist[255-d] if d else 0)
    cum += c
    if d < 12 or d % 5 == 0:
        print(f"  |d|={d:3d}: {c:14d}  {100*c/tot:8.4f}%   cum {100*cum/tot:8.4f}%")
print(f"  |d|>=40: {tot-cum:14d}  {100*(tot-cum)/tot:8.4f}%")
nz = np.arange(512)-255
mean_signed = float((hist*nz).sum()/tot)
print(f"  mean signed diff (LC - ours) = {mean_signed:+.6f}")
print(f"  P(d>0)={100*hist[256:].sum()/tot:.3f}%  P(d<0)={100*hist[:255].sum()/tot:.3f}%  P(d=0)={100*hist[255]/tot:.3f}%")

json.dump(rows, open("/home/user/new-skinny-bob/analysis/third-party-toolkit/compare2.json","w"))
np.save("/home/user/new-skinny-bob/analysis/third-party-toolkit/diffhist.npy", hist)

print("\n=== worst 12 by RMS ===")
for r in sorted(rows, key=lambda r:-r['rms'])[:12]:
    print(f"  f{r['n']:5d} maxabs={r['maxabs']:3d} rms={r['rms']:8.4f} mad={r['mad']:7.4f} %diff={r['pct_diff']:6.2f} %>16={r['pct_gt16']:6.3f}")
print("=== best 12 by RMS ===")
for r in sorted(rows, key=lambda r:r['rms'])[:12]:
    print(f"  f{r['n']:5d} maxabs={r['maxabs']:3d} rms={r['rms']:8.4f} mad={r['mad']:7.4f} %diff={r['pct_diff']:6.2f}")
print("\n=== PNG size ratio (LC/ours) ===")
rat = np.array([r['lc_bytes']/r['our_bytes'] for r in rows])
print(f"  min {rat.min():.4f} med {np.median(rat):.4f} mean {rat.mean():.4f} max {rat.max():.4f}")
print(f"  LC total {sum(r['lc_bytes'] for r in rows)}  ours total {sum(r['our_bytes'] for r in rows)}")
