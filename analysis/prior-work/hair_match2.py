#!/usr/bin/env python3.12
"""
Faster rerun of the hook-hair search. Same logic, bounded cost:
480x270 working res, 3 template scales, at most 200 of the brightest frames per video.

Positive control: the 2011 videos, where BrooklynRobot demonstrated the hair is present.
Null: the same template flipped on both axes, searched identically.
"""
import subprocess, json, sys
import numpy as np
from PIL import Image
from skimage.feature import match_template
from scipy.ndimage import gaussian_filter

W, H = 480, 270
MAXF = 200

VIDS = {
    "stock_getty104161830": "analysis/prior-work/gettyimages-104161830-640_adpp.mp4",
    "stock_getty160602429": "analysis/prior-work/gettyimages-160602429-640_adpp.mp4",
    "stock_istock146102427": "analysis/prior-work/istockphoto-146102427-640_adpp_is.mp4",
    "2011_ZB788": "videos/2011/ZB788PtqQvg.mkv",
    "2011_RsQCX": "videos/2011/RsQCXN4o4Ps.mkv",
    "2011_Xju":   "videos/2011/Xju_CY5ZESA.mkv",
    "2011_a6TL":  "videos/2011/a6TLGkrfNKI.mkv",
    "2026_v1":    "videos/2026/OpSTlDJWFFI.mkv",
    "2026_v2":    "videos/2026/Oqw96jCOP7A.mkv",
    "2026_v3":    "videos/2026/l9RAhmPHM_A.mkv",
}


def decode(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-vf", f"scale={W}:{H}",
         "-pix_fmt", "gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (W * H)
    return np.frombuffer(raw[:n * W * H], np.uint8).reshape(n, H, W).astype(np.float32)


def darkness(a, sig=1.0):
    return gaussian_filter(a, 6) - gaussian_filter(a, sig)


def scaled(T, widths):
    out = []
    for w in widths:
        h = max(8, int(T.shape[0] * w / T.shape[1]))
        out.append(np.asarray(Image.fromarray(T).resize((w, h), Image.BILINEAR)))
    return out


def scan(frames, tpls):
    lum = frames.reshape(len(frames), -1).mean(axis=1)
    keep = np.argsort(lum)[-min(MAXF, len(frames)):]
    scores = []
    for i in keep:
        d = darkness(frames[i])
        best = -1.0
        for t in tpls:
            if t.shape[0] >= d.shape[0] or t.shape[1] >= d.shape[1]:
                continue
            best = max(best, float(match_template(d, t).max()))
        scores.append((best, int(i)))
    scores.sort(reverse=True)
    return scores


if __name__ == "__main__":
    im = np.asarray(Image.open("analysis/prior-work/dYfOF60.png").convert("L"), np.float32)
    T = darkness(im[40:370, 1640:2040])
    widths = (95, 130, 175)
    sig = scaled(T, widths)
    nul = scaled(T[::-1, ::-1].copy(), widths)
    print(f"template {T.shape} -> widths {widths}", flush=True)

    out = {}
    for name, path in VIDS.items():
        f = decode(path)
        if len(f) == 0:
            print(f"{name}: no frames", flush=True); continue
        s = scan(f, sig)
        n = scan(f, nul)
        out[name] = {"best": round(s[0][0], 4), "best_frame": s[0][1],
                     "top3": [round(x[0], 4) for x in s[:3]],
                     "null_best": round(n[0][0], 4),
                     "margin": round(s[0][0] - n[0][0], 4)}
        print(f"{name:24s} best={s[0][0]:.4f} @f{s[0][1]:<5d} "
              f"top3={[round(x[0],3) for x in s[:3]]}  null={n[0][0]:.4f}  "
              f"margin={s[0][0]-n[0][0]:+.4f}", flush=True)
    json.dump(out, open("hair_match.json", "w"), indent=1)
