#!/usr/bin/env python3.12
"""Pass 3: per-frame U and V row-mean profiles inside the picture rect
(chroma-plane resolution, W/2 x H/2), for chroma-banding analysis."""
import subprocess, sys, numpy as np
sys.path.insert(0, "/home/user/new-skinny-bob/analysis/compare-eras/band")
from pass2 import VIDS
OUT = "/home/user/new-skinny-bob/analysis/compare-eras/band"

def run(key):
    path, W, H, C0, C1, R0, R1 = VIDS[key]
    C0 &= ~1; C1 &= ~1
    cw, ch = W//2, H//2
    ysz, csz = W*H, cw*ch
    fsz = ysz+2*csz
    cc0, cc1 = C0//2, C1//2
    nw = cc1-cc0
    p = subprocess.Popen(["ffmpeg","-v","error","-i",path,"-f","rawvideo",
                          "-pix_fmt","yuv420p","-"], stdout=subprocess.PIPE, bufsize=fsz*8)
    up = []; vp = []
    rd = p.stdout.read
    while True:
        b = rd(fsz)
        if len(b) < fsz: break
        a = np.frombuffer(b, np.uint8)
        U = a[ysz:ysz+csz].reshape(ch, cw)[:, cc0:cc1]
        V = a[ysz+csz:].reshape(ch, cw)[:, cc0:cc1]
        up.append(np.add.reduce(U, axis=1, dtype=np.int32)/nw)
        vp.append(np.add.reduce(V, axis=1, dtype=np.int32)/nw)
    p.stdout.close(); p.wait()
    np.savez_compressed(f"{OUT}/{key}_p3.npz",
        uprof=np.array(up, np.float32), vprof=np.array(vp, np.float32),
        rect=np.array([C0,C1,R0,R1]), W=W, H=H)
    print(key, len(up), flush=True)

for k in sys.argv[1:] or VIDS:
    run(k)
