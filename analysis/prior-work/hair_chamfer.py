#!/usr/bin/env python3.12
"""
Chamfer search for the stock-overlay hook hair.

NCC failed because the template is >95% empty background, so the correlation
scored background similarity rather than the curve. Chamfer matching scores only
the curve: take the template's curve pixels as a point set, and for each candidate
offset measure the mean distance from those points to the nearest thin-dark-curve
pixel in the target frame. Present -> ~1-2 px. Absent -> much larger.

  chamfer(offset) = (curve_mask (*) distance_transform(target_curves)) / |curve_mask|

which is a single FFT convolution per frame per scale.

POSITIVE CONTROL: the 2011 videos, where the hair is demonstrated present
(analysis/prior-work/dYfOF60.png, Ivan0135 Shot 07). If the control does not separate
from the null, the test is uninformative and is reported as such.
NULL: same template flipped on both axes.
"""
import subprocess, json
import numpy as np
from PIL import Image
from scipy.signal import fftconvolve
from scipy.ndimage import gaussian_filter, distance_transform_edt

W, H = 480, 270
MAXF = 150

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


def ridge(a, sig=1.0, pct=99.0):
    """Binary map of thin dark curve pixels."""
    r = gaussian_filter(a, 5) - gaussian_filter(a, sig)   # dark thin -> positive
    thr = np.percentile(r, pct)
    return (r > max(thr, 1.0))


def tpl_points(scale):
    im = np.asarray(Image.open("analysis/prior-work/dYfOF60.png").convert("L"), np.float32)
    t = im[40:370, 1640:2040]
    w = int(400 * scale)
    h = int(330 * scale)
    t = np.asarray(Image.fromarray(t).resize((w, h), Image.BILINEAR), np.float32)
    m = ridge(t, pct=97.0)
    return m


def chamfer_min(target_ridge, mask):
    if mask.sum() < 30:
        return None
    if mask.shape[0] >= target_ridge.shape[0] or mask.shape[1] >= target_ridge.shape[1]:
        return None
    dt = distance_transform_edt(~target_ridge)
    # correlate: flip mask so fftconvolve gives correlation
    c = fftconvolve(dt, mask[::-1, ::-1].astype(np.float64), mode="valid")
    return float(c.min() / mask.sum())


def scan(frames, masks):
    lum = frames.reshape(len(frames), -1).mean(axis=1)
    keep = np.argsort(lum)[-min(MAXF, len(frames)):]
    best = (1e9, None)
    for i in keep:
        tr = ridge(frames[i])
        if tr.sum() < 50:
            continue
        for m in masks:
            v = chamfer_min(tr, m)
            if v is not None and v < best[0]:
                best = (v, int(i))
    return best


if __name__ == "__main__":
    scales = (0.24, 0.33, 0.44)
    sig = [tpl_points(s) for s in scales]
    nul = [m[::-1, ::-1].copy() for m in sig]
    print("template curve pixels per scale:", [int(m.sum()) for m in sig], flush=True)

    out = {}
    for name, path in VIDS.items():
        f = decode(path)
        if len(f) == 0:
            continue
        s, si = scan(f, sig)
        n, _ = scan(f, nul)
        out[name] = {"chamfer_px": round(s, 3), "at_frame": si,
                     "null_px": round(n, 3), "null_minus_sig": round(n - s, 3)}
        print(f"{name:24s} chamfer={s:7.3f} px @f{si}   null={n:7.3f}   "
              f"null-sig={n-s:+.3f}", flush=True)
    json.dump(out, open("hair_chamfer.json", "w"), indent=1)
