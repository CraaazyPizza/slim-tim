#!/usr/bin/env python3.12
"""Register panel frames of l9RAhmPHM_A onto a canonical reference view.

SIFT+RANSAC homography to reference, then ECC refinement on the panel ROI.
Writes H matrices + quality metrics to reg.npz
"""
import numpy as np, cv2, sys, json

FR = "/home/user/new-skinny-bob/frames/l9RAhmPHM_A/f%05d.png"
OUT = "/home/user/new-skinny-bob/analysis/symbol-panel/"
PB = (263, 60, 1561, 1043)          # picture area x0,y0,x1,y1 (measured)
REF = 1694
ROI_PANEL = (250, 200, 950, 800)    # in picture-area coords
TC_MASK = (469 - PB[0], 940 - PB[1], 965 - PB[0], 1000 - PB[1])  # timecode overlay


def load(i):
    return cv2.imread(FR % i, cv2.IMREAD_GRAYSCALE).astype(np.float32)


def pic(a):
    return a[PB[1]:PB[3], PB[0]:PB[2]].copy()


def prep(c):
    """local-contrast normalised uint8 for feature detection"""
    bg = cv2.GaussianBlur(c, (0, 0), 25)
    d = c - bg
    d = np.clip(d / (4 * np.std(d) + 1e-6) + 0.5, 0, 1)
    u = (d * 255).astype(np.uint8)
    u[TC_MASK[1]:TC_MASK[3], TC_MASK[0]:TC_MASK[2]] = 128   # kill timecode
    return u


def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    sift = cv2.SIFT_create(nfeatures=4000)
    bf = cv2.BFMatcher()
    rc = pic(load(REF)); ra = prep(rc)
    kr, dr = sift.detectAndCompute(ra, None)
    x0, y0, x1, y1 = ROI_PANEL
    m = np.zeros(ra.shape, np.uint8); m[y0:y1, x0:x1] = 255
    m[TC_MASK[1]:TC_MASK[3], TC_MASK[0]:TC_MASK[2]] = 0
    refroi = ra[y0:y1, x0:x1].astype(np.float32)
    refroi = (refroi - refroi.mean()) / (refroi.std() + 1e-6)

    Hs, ncc, inl, sharp = {}, {}, {}, {}
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-6)
    for i in range(lo, hi + 1):
        c = pic(load(i)); a = prep(c)
        k, d = sift.detectAndCompute(a, None)
        H = None
        if d is not None and len(k) >= 8:
            mt = bf.knnMatch(d, dr, k=2)
            good = [p for p, q in mt if p.distance < 0.78 * q.distance]
            if len(good) >= 10:
                src = np.float32([k[g.queryIdx].pt for g in good]).reshape(-1, 1, 2)
                dst = np.float32([kr[g.trainIdx].pt for g in good]).reshape(-1, 1, 2)
                H0, mask = cv2.findHomography(src, dst, cv2.RANSAC, 3.0, maxIters=8000)
                if H0 is not None and mask is not None and mask.sum() >= 15:
                    inl[i] = int(mask.sum())
                    # ECC refine (warp maps ref -> cur, so invert)
                    W = np.linalg.inv(H0); W /= W[2, 2]
                    try:
                        _, W = cv2.findTransformECC(ra, a, W.astype(np.float32),
                                                    cv2.MOTION_HOMOGRAPHY, crit, m, 5)
                        H = np.linalg.inv(W); H /= H[2, 2]
                    except cv2.error:
                        H = H0
        if H is None:
            continue
        w = cv2.warpPerspective(c, H, (ra.shape[1], ra.shape[0]),
                                flags=cv2.INTER_LANCZOS4, borderValue=np.nan)
        r = w[y0:y1, x0:x1]
        if np.isnan(r).mean() > 0.25:
            continue
        rr = np.nan_to_num(r, nan=np.nanmean(r))
        bg = cv2.GaussianBlur(rr, (0, 0), 25)
        rr = rr - bg
        rr = (rr - rr.mean()) / (rr.std() + 1e-6)
        ncc[i] = float((rr * refroi).mean())
        Hs[i] = H
        gx = cv2.Sobel(c[y0:y1, x0:x1], cv2.CV_32F, 1, 0)
        gy = cv2.Sobel(c[y0:y1, x0:x1], cv2.CV_32F, 0, 1)
        sharp[i] = float(np.mean(gx * gx + gy * gy))
        if i % 25 == 0:
            print(i, inl[i], round(ncc[i], 3), round(sharp[i], 1), flush=True)
    ks = sorted(Hs)
    np.savez(OUT + f"reg_{lo}_{hi}.npz", frames=np.array(ks),
             H=np.array([Hs[i] for i in ks]),
             ncc=np.array([ncc[i] for i in ks]),
             inl=np.array([inl[i] for i in ks]),
             sharp=np.array([sharp[i] for i in ks]))
    print("kept", len(ks), "of", hi - lo + 1)


main()
