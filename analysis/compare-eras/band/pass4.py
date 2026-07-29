#!/usr/bin/env python3.12
"""Pass 4: per-frame cross-moments of (Y,U,V) inside the picture rect, at chroma
resolution, so a tint (chroma = linear function of luma) can be separated from
genuine independent colour.

For each frame store: n, sY, sYY, sU, sV, sYU, sYV, sUU, sVV, sUV
-> a_u,b_u = LS fit of (U-128) on Y ; R^2 ; residual sd of U after removing the
   luma-linear part = the part of the chroma that is NOT explainable as a tint.
"""
import subprocess, sys, numpy as np
sys.path.insert(0, "/home/user/new-skinny-bob/analysis/compare-eras/band")
from pass2 import VIDS, blockmean
OUT = "/home/user/new-skinny-bob/analysis/compare-eras/band"


def run(key):
    path, W, H, C0, C1, R0, R1 = VIDS[key]
    C0 &= ~1; C1 &= ~1; R0 &= ~1; R1 &= ~1
    cw, ch = W//2, H//2
    ysz, csz = W*H, cw*ch
    fsz = ysz+2*csz
    cc0, cc1, cr0, cr1 = C0//2, C1//2, R0//2, R1//2
    p = subprocess.Popen(["ffmpeg","-v","error","-i",path,"-f","rawvideo",
                          "-pix_fmt","yuv420p","-"], stdout=subprocess.PIPE, bufsize=fsz*8)
    rows = []
    rd = p.stdout.read
    while True:
        b = rd(fsz)
        if len(b) < fsz: break
        a = np.frombuffer(b, np.uint8)
        Y = a[:ysz].reshape(H, W)[R0:R1, C0:C1]
        U = a[ysz:ysz+csz].reshape(ch, cw)[cr0:cr1, cc0:cc1].astype(np.float32)-128.0
        V = a[ysz+csz:].reshape(ch, cw)[cr0:cr1, cc0:cc1].astype(np.float32)-128.0
        Yq = blockmean(Y.astype(np.float32), 2)
        hh = min(Yq.shape[0], U.shape[0]); ww = min(Yq.shape[1], U.shape[1])
        y = Yq[:hh, :ww].ravel(); u = U[:hh, :ww].ravel(); v = V[:hh, :ww].ravel()
        rows.append((y.size, y.sum(), (y*y).sum(), u.sum(), v.sum(),
                     (y*u).sum(), (y*v).sum(), (u*u).sum(), (v*v).sum(), (u*v).sum()))
    p.stdout.close(); p.wait()
    np.savez_compressed(f"{OUT}/{key}_p4.npz", mom=np.array(rows, np.float64),
                        rect=np.array([C0,C1,R0,R1]))
    print(key, len(rows), flush=True)


for k in sys.argv[1:] or VIDS:
    run(k)
