#!/usr/bin/env python3.12
"""
Do damage marks persist across frames?

A real scanned-film overlay clip carries hairs and scratches that last many frames
(Sapphire's Hairs group even has explicit Persistence and Wiggle controls). A layer
that is re-randomised every frame does not. This is a property of the ASSET, so it
can be measured on the newly-obtained stock clips and compared against both eras.

Retention(k) = fraction of a frame's thin-dark-curve pixels that are still curve
pixels k frames later, within a 1 px dilation, minus the chance level obtained by
pairing with a random distant frame.

If the stock clips show real persistence and the Skinny Bob videos do not, the SB
damage layer was not these clips composited frame-for-frame.
"""
import subprocess, json
import numpy as np
from scipy.ndimage import gaussian_filter, binary_dilation

W, H = 480, 270

VIDS = {
    "stock_getty104161830": "analysis/prior-work/gettyimages-104161830-640_adpp.mp4",
    "stock_getty160602429": "analysis/prior-work/gettyimages-160602429-640_adpp.mp4",
    "stock_istock146102427": "analysis/prior-work/istockphoto-146102427-640_adpp_is.mp4",
    "2011_ZB788": "videos/2011/ZB788PtqQvg.mkv",
    "2011_RsQCX": "videos/2011/RsQCXN4o4Ps.mkv",
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


def ridge(a, pct=99.2):
    r = gaussian_filter(a, 5) - gaussian_filter(a, 1.0)
    return r > max(np.percentile(r, pct), 1.0)


if __name__ == "__main__":
    out = {}
    rng = np.random.default_rng(0)
    for name, path in VIDS.items():
        f = decode(path)
        n = len(f)
        if n < 40:
            continue
        # sample up to 120 frames from the brighter half (marks are visible there)
        lum = f.reshape(n, -1).mean(axis=1)
        cand = np.argsort(lum)[-min(240, n):]
        cand = np.array(sorted(int(i) for i in cand if i + 3 < n))
        if len(cand) > 120:
            cand = cand[np.linspace(0, len(cand) - 1, 120).astype(int)]
        R = {int(i): ridge(f[i]) for i in cand}
        res = {}
        for k in (1, 2, 3):
            keep, chance = [], []
            for i in cand:
                if i + k not in R:
                    R[int(i + k)] = ridge(f[i + k])
                a, b = R[int(i)], R[int(i + k)]
                if a.sum() < 30:
                    continue
                bd = binary_dilation(b)
                keep.append((a & bd).sum() / a.sum())
                # chance: pair with a random far frame
                j = int(rng.choice(cand))
                while abs(j - i) < 15 and len(cand) > 30:
                    j = int(rng.choice(cand))
                cd = binary_dilation(R[j])
                chance.append((a & cd).sum() / a.sum())
            if keep:
                res[f"lag{k}"] = {
                    "retention": round(float(np.mean(keep)), 4),
                    "chance": round(float(np.mean(chance)), 4),
                    "excess": round(float(np.mean(keep) - np.mean(chance)), 4)}
        out[name] = res
        s = "  ".join(f"{k}: ret={v['retention']:.3f} chance={v['chance']:.3f} "
                      f"excess={v['excess']:+.3f}" for k, v in res.items())
        print(f"{name:24s} {s}", flush=True)
    json.dump(out, open("persistence.json", "w"), indent=1)
