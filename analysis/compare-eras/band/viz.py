#!/usr/bin/env python3.12
"""Render, for chosen frames: original RGB | chroma amplified x10 about neutral.
Decodes a single frame straight from the mkv at yuv444p so no RGB round-trip
hides the chroma."""
import subprocess, numpy as np, sys, os
from PIL import Image
O = "/home/user/new-skinny-bob/analysis/compare-eras/band/viz"
os.makedirs(O, exist_ok=True)
V = {
 "OpSTlDJWFFI": ("/home/user/new-skinny-bob/videos/2026/OpSTlDJWFFI.mkv", 1920, 1080, 30000/1001),
 "Oqw96jCOP7A": ("/home/user/new-skinny-bob/videos/2026/Oqw96jCOP7A.mkv", 1920, 1080, 30000/1001),
 "l9RAhmPHM_A": ("/home/user/new-skinny-bob/videos/2026/l9RAhmPHM_A.mkv", 1920, 1080, 30000/1001),
 "ZB788PtqQvg": ("/home/user/new-skinny-bob/videos/2011/ZB788PtqQvg.mkv", 1920, 1080, 25.),
 "RsQCXN4o4Ps": ("/home/user/new-skinny-bob/videos/2011/RsQCXN4o4Ps.mkv", 1920, 1080, 25.),
 "Xju_CY5ZESA": ("/home/user/new-skinny-bob/videos/2011/Xju_CY5ZESA.mkv", 1920, 1080, 25.),
 "a6TLGkrfNKI": ("/home/user/new-skinny-bob/videos/2011/a6TLGkrfNKI.mkv", 640, 480, 25.),
}
JOBS = [("OpSTlDJWFFI", [1041, 2600, 2700, 2800, 2900]),
        ("Oqw96jCOP7A", [2265, 1900]),
        ("l9RAhmPHM_A", [3885]),
        ("ZB788PtqQvg", [382, 200]),
        ("RsQCXN4o4Ps", [1140]),
        ("Xju_CY5ZESA", [484]),
        ("a6TLGkrfNKI", [2009, 1500])]
AMP = 10.0

def grab(path, W, H, fps, fno):
    t = (fno-1)/fps
    p = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.4f}","-i",path,"-frames:v","1",
                        "-f","rawvideo","-pix_fmt","yuv444p","-"], capture_output=True)
    a = np.frombuffer(p.stdout[:3*W*H], np.uint8).reshape(3, H, W).astype(np.float32)
    return a

def yuv2rgb(Y, U, V):
    y = (Y-16)/219.0; u = (U-128)/224.0; v = (V-128)/224.0
    r = y + 1.5748*v; g = y - 0.1873*u - 0.4681*v; b = y + 1.8556*u
    return np.clip(np.stack([r, g, b], -1)*255, 0, 255).astype(np.uint8)

for key, frames in JOBS:
    path, W, H, fps = V[key]
    tiles = []
    for fno in frames:
        a = grab(path, W, H, fps, fno)
        Y, U, Vv = a[0], a[1], a[2]
        rgb = yuv2rgb(Y, U, Vv)
        amp = yuv2rgb(np.full_like(Y, 128.0), 128+(U-128)*AMP, 128+(Vv-128)*AMP)
        for im in (rgb, amp):
            t = Image.fromarray(im)
            t = t.resize((int(t.width*260/t.height), 260))
            tiles.append(t)
        print(key, fno, "meanU=%.2f meanV=%.2f sdU=%.2f sdV=%.2f max|U-128|=%.0f" % (
            U.mean(), Vv.mean(), U.std(), Vv.std(), np.abs(U-128).max()))
    w = sum(t.width for t in tiles)
    out = Image.new("RGB", (w, 260)); x = 0
    for t in tiles:
        out.paste(t, (x, 0)); x += t.width
    out.save(f"{O}/{key}.png")
