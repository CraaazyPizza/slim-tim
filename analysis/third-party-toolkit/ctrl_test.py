#!/usr/bin/env python3.12
"""Which YouTube format did LC decode? Compare LC against controls re-encoded from our AV1."""
import os, subprocess, numpy as np
from PIL import Image

SCR = "/tmp/claude-1001/-home-user-new-skinny-bob/6c2508df-43ca-4f35-aaa6-0d27ef73c55d/scratchpad/ctrl"
BASE = "/home/user/new-skinny-bob/analysis/third-party-toolkit/extracted/2026-05-25_Confidential leaked ufo-ebe footage continuation of disclosure"
OURS = "/home/user/new-skinny-bob/frames/OpSTlDJWFFI"
FR = [400, 700, 1000, 1100, 1200, 1300, 1400]

def lc_map():
    d = {}
    for dp in sorted(os.listdir(BASE)):
        fp = os.path.join(BASE, dp)
        if not os.path.isdir(fp): continue
        for f in sorted(os.listdir(fp)):
            if f.endswith(".png"): d[int(f.split("_")[1].split(".")[0])] = os.path.join(fp, f)
    return d
LC = lc_map()

for src, tag in ((f"{SCR}/h264.mp4", "h264"), (f"{SCR}/vp9.webm", "vp9")):
    od = f"{SCR}/{tag}_frames"
    if not os.path.isdir(od):
        os.makedirs(od)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
                        "-vsync", "0", "-start_number", "1", f"{od}/f%05d.png"], check=True)

def A(p): return np.asarray(Image.open(p).convert("RGB"), dtype=np.uint8)
def grid(im, period):
    g = np.asarray(Image.fromarray(im).convert("L"), dtype=np.float32)
    dh = np.abs(np.diff(g, axis=1)); c = np.arange(dh.shape[1])
    return dh[:, (c+1) % period == 0].mean() / dh[:, (c+1) % period != 0].mean()

print("="*96)
print("BLOCK-GRID SIGNATURE  (mean|dx| on boundary / off boundary)")
print("="*96)
print(f"{'frame':>6} {'source':>14} " + " ".join(f"{'p='+str(p):>7}" for p in (4,8,16,32,64,128)) + "   shape16 = p16/p4")
srcs = [("LC", lambda n: A(LC[n])),
        ("ours(AV1-yt)", lambda n: A(f"{OURS}/f{n:05d}.png")),
        ("ctrl h264", lambda n: A(f"{SCR}/h264_frames/f{n:05d}.png")),
        ("ctrl vp9", lambda n: A(f"{SCR}/vp9_frames/f{n:05d}.png"))]
acc = {t: [] for t, _ in srcs}
for n in FR:
    for t, g in srcs:
        im = g(n); r = [grid(im, p) for p in (4,8,16,32,64,128)]
        acc[t].append(r)
        print(f"{n:6d} {t:>14} " + " ".join(f"{x:7.3f}" for x in r) + f"   {r[2]/r[0]:7.3f}")
    print()
print("MEANS over frames:")
for t, _ in srcs:
    m = np.mean(acc[t], axis=0)
    print(f"  {t:>14} " + " ".join(f"{x:7.3f}" for x in m) + f"   {m[2]/m[0]:7.3f}")

print()
print("="*96)
print("BLACK-FRAME BEHAVIOUR (AV1 tile-corner artifact present?)")
print("="*96)
for n in [1, 5, 913, 915]:
    line = f" f{n:5d}: "
    for t, g in srcs:
        try:
            im = g(n)
            blk = int(np.count_nonzero(im[0:32, 0:32]) + np.count_nonzero(im[0:32, 960:992]))
            line += f"{t}: max={im.max()} nz_in_tilecorners={blk} nz_total={int(np.count_nonzero(im))} | "
        except Exception as e: line += f"{t}: ERR | "
    print(line)

print()
print("="*96)
print("DISTANCE OF EACH CANDIDATE TO LC  (RMS vs LC frames)")
print("="*96)
print("If LC == a YouTube AVC decode, ctrl-h264 (same codec family, similar bitrate)")
print("should not necessarily be closest -- but the *block signature* should match.")
print(f"{'frame':>6} " + " ".join(f"{t:>16}" for t, _ in srcs[1:]))
for n in FR:
    a = A(LC[n]).astype(np.float32)
    row = []
    for t, g in srcs[1:]:
        b = g(n).astype(np.float32)
        row.append(float(np.sqrt(((a-b)**2).mean())))
    print(f"{n:6d} " + " ".join(f"{x:16.4f}" for x in row))

print()
print("="*96)
print("DETAIL LEVEL (laplacian variance) -- lower = smoother/more compressed")
print("="*96)
print(f"{'frame':>6} " + " ".join(f"{t:>16}" for t, _ in srcs))
for n in FR:
    row = []
    for t, g in srcs:
        gg = np.asarray(Image.fromarray(g(n)).convert("L"), dtype=np.float32)
        lap = 4*gg[1:-1,1:-1]-gg[:-2,1:-1]-gg[2:,1:-1]-gg[1:-1,:-2]-gg[1:-1,2:]
        row.append(float(lap.var()))
    print(f"{n:6d} " + " ".join(f"{x:16.3f}" for x in row))
