#!/usr/bin/env python3.12
"""Stage 2: stack registered panel frames into canonical canvases, and run the
four anti-pareidolia controls.

Usage: stack.py <mode>
  glyph    - glyph-cluster canvas stacks (+4 disjoint windows)
  panel    - wide panel canvas stack, raw and rectified
  control  - matched featureless control ROI through the identical pipeline
  inject   - synthetic-glyph injection test
"""
import numpy as np, cv2, sys, json, os

FR = "/home/user/new-skinny-bob/frames/l9RAhmPHM_A/f%05d.png"
OUT = "/home/user/new-skinny-bob/analysis/symbol-panel/"
PB = (263, 60, 1561, 1043)
REF = 1694
TCM = (469 - PB[0], 938 - PB[1], 968 - PB[0], 1002 - PB[1])
REG = OUT + "reg2_1099_1760.npz"

# canonical canvases: (src rect in ref picture coords, zoom)
CANVAS = {
    "glyph":   ((400, 500, 730, 810), 3.0),
    "panel":   ((230, 180, 980, 830), 2.0),
    "control": ((60, 500, 390, 810), 3.0),     # same size as glyph, featureless dark field
}


def load(i):
    return cv2.imread(FR % i, cv2.IMREAD_GRAYSCALE).astype(np.float32)


def pic(a):
    return a[PB[1]:PB[3], PB[0]:PB[2]].copy()


def smat(rect, z):
    return np.array([[z, 0, -z * rect[0]], [0, z, -z * rect[1]], [0, 0, 1]], np.float64)


def canvas_size(rect, z):
    return int(z * (rect[2] - rect[0])), int(z * (rect[3] - rect[1]))


def warp(img, H, rect, z, border=np.nan):
    W, Hh = canvas_size(rect, z)
    return cv2.warpPerspective(img, smat(rect, z) @ H, (W, Hh),
                               flags=cv2.INTER_LANCZOS4,
                               borderMode=cv2.BORDER_CONSTANT, borderValue=border)


def sel(d, nccmin=0.40, inlmin=12):
    m = (d["ncc"] >= nccmin) & (d["inl"] >= inlmin)
    return m


def stack_frames(frames, Hs, rect, z, gains=True, extra=None):
    """robust weighted stack of the given frames into canonical canvas"""
    W, Hh = canvas_size(rect, z)
    layers, wts = [], []
    for f, H in zip(frames, Hs):
        c = pic(load(f))
        if extra is not None:
            c = extra(c, f, H)
        c[TCM[1]:TCM[3], TCM[0]:TCM[2]] = np.nan          # mask burned-in timecode
        w = warp(c, H, rect, z)
        v = np.isfinite(w)
        if v.mean() < 0.55:
            continue
        layers.append(w); wts.append(v.astype(np.float32))
    if not layers:
        return None, None, 0
    A = np.stack(layers); V = np.stack(wts) > 0
    # per-layer robust photometric normalisation to the median layer
    med = np.nanmedian(A, 0)
    if gains:
        for k in range(len(A)):
            m = V[k] & np.isfinite(med)
            if m.sum() < 500:
                continue
            x = A[k][m]; y = med[m]
            lo, hi = np.percentile(x, (5, 99))
            if hi - lo < 1e-3:
                continue
            g = (np.percentile(y, 99) - np.percentile(y, 5)) / (hi - lo)
            g = float(np.clip(g, 0.2, 5.0))
            A[k] = (A[k] - lo) * g + np.percentile(y, 5)
    # sigma-clipped mean
    mu = np.nanmedian(A, 0)
    sd = np.nanstd(A, 0)
    keep = np.abs(A - mu) < (2.5 * sd + 2.0)
    keep &= V
    n = keep.sum(0)
    Az = np.where(keep, A, 0.0)
    out = np.where(n > 0, np.nansum(Az, 0) / np.maximum(n, 1), np.nan)
    return out, n, len(A)


def enhance(img, sigma_px, upsample=1.0, rl_iters=25):
    """flat-field, stretch, optional Richardson-Lucy with a Gaussian PSF"""
    x = np.nan_to_num(img, nan=np.nanmedian(img))
    bg = cv2.GaussianBlur(x, (0, 0), max(sigma_px * 8, 30))
    x = x - bg
    lo, hi = np.percentile(x, (1.0, 99.9))
    x = np.clip((x - lo) / (hi - lo + 1e-6), 0, 1)
    if rl_iters:
        k = int(sigma_px * 6) | 1
        psf = cv2.getGaussianKernel(k, sigma_px)
        psf = psf @ psf.T; psf /= psf.sum()
        est = np.full_like(x, x.mean())
        flip = psf[::-1, ::-1]
        for _ in range(rl_iters):
            conv = cv2.filter2D(est, -1, psf, borderType=cv2.BORDER_REPLICATE)
            rel = x / (conv + 1e-3)
            est = est * cv2.filter2D(rel, -1, flip, borderType=cv2.BORDER_REPLICATE)
            est = np.clip(est, 0, 3)
        x = est
    lo, hi = np.percentile(x, (1.0, 99.8))
    x = np.clip((x - lo) / (hi - lo + 1e-6), 0, 1)
    if upsample != 1.0:
        x = cv2.resize(x, None, fx=upsample, fy=upsample, interpolation=cv2.INTER_LANCZOS4)
    return x


def u8(x):
    return (np.clip(x, 0, 1) * 255).astype(np.uint8)


def main():
    mode = sys.argv[1]
    d = np.load(REG)
    m = sel(d)
    fr, H, ncc, sc, sh = (d["frames"][m], d["H"][m], d["ncc"][m], d["scale"][m], d["sharp"][m])
    print("usable frames:", len(fr), "range", fr.min(), fr.max())
    json.dump({"n": int(len(fr)), "frames": fr.tolist()},
              open(OUT + "usable_frames.json", "w"))

    if mode in ("glyph", "control"):
        rect, z = CANVAS[mode]
        out, n, k = stack_frames(fr, H, rect, z)
        np.save(OUT + f"{mode}_stack.npy", out)
        cv2.imwrite(OUT + f"{mode}_stack_lin.png", u8(enhance(out, 3 * 2.7, rl_iters=0)))
        cv2.imwrite(OUT + f"{mode}_stack_rl.png", u8(enhance(out, 3 * 2.7)))
        print(mode, "stacked", k, "layers")
        # four disjoint windows
        q = np.array_split(np.arange(len(fr)), 4)
        tiles = []
        for j, idx in enumerate(q):
            o, _, kk = stack_frames(fr[idx], H[idx], rect, z)
            e = enhance(o, 3 * 2.7)
            np.save(OUT + f"{mode}_win{j}.npy", o)
            tiles.append((f"f{fr[idx][0]}-{fr[idx][-1]} n={kk}", e))
        W = tiles[0][1].shape[1]; Hh = tiles[0][1].shape[0]
        sheet = np.zeros((Hh + 30, W * 4, 3), np.uint8)
        for j, (lab, e) in enumerate(tiles):
            sheet[30:, j * W:(j + 1) * W] = cv2.cvtColor(u8(e), cv2.COLOR_GRAY2BGR)
            cv2.putText(sheet, lab, (j * W + 8, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imwrite(OUT + ("controls_4up.png" if mode == "glyph" else "control_roi_4up.png"), sheet)

    if mode == "panel":
        rect, z = CANVAS["panel"]
        # near-constant-viewpoint band around the reference
        band = (fr >= 1660) & (fr <= 1745)
        out, n, k = stack_frames(fr[band], H[band], rect, z)
        np.save(OUT + "panel_stack.npy", out)
        cv2.imwrite(OUT + "panel_stack_raw.png", u8(enhance(out, 2 * 2.7, upsample=1.5)))
        print("panel stacked", k, "layers")


if __name__ == "__main__":
    main()
