#!/usr/bin/env python3.12
"""Is the glyph attached to the scene, or an independent layer?

For each frame: estimate a homography to the reference using ONLY features
OUTSIDE the glyph region ("scene"), and separately using only features INSIDE
it ("glyph"). If the mark lies on the photographed surface the two must agree.
"""
import numpy as np, cv2, json

FR = "/home/user/new-skinny-bob/frames/l9RAhmPHM_A/f%05d.png"
OUT = "/home/user/new-skinny-bob/analysis/symbol-panel/"
PB = (263, 60, 1561, 1043)
REF = 1694
GBOX = (425, 505, 615, 740)            # glyph bbox in ref picture coords
TCM = (469 - PB[0], 938 - PB[1], 968 - PB[0], 1002 - PB[1])
PAD = 40


def load(i):
    a = cv2.imread(FR % i, cv2.IMREAD_GRAYSCALE).astype(np.float32)
    return a[PB[1]:PB[3], PB[0]:PB[2]]


def prep(c):
    bg = cv2.GaussianBlur(c, (0, 0), 25)
    d = np.clip((c - bg) / (4 * np.std(c - bg) + 1e-6) + 0.5, 0, 1)
    u = (d * 255).astype(np.uint8)
    u[TCM[1]:TCM[3], TCM[0]:TCM[2]] = 128
    return u


def inbox(pts, box, pad=0):
    x0, y0, x1, y1 = box
    return ((pts[:, 0] > x0 - pad) & (pts[:, 0] < x1 + pad) &
            (pts[:, 1] > y0 - pad) & (pts[:, 1] < y1 + pad))


def main():
    d = np.load(OUT + "reg2_1099_1760.npz")
    keep = (d["ncc"] > 0.4) & (d["inl"] >= 12)
    frames, Hg0 = d["frames"][keep], d["H"][keep]
    sift = cv2.SIFT_create(nfeatures=6000)
    bf = cv2.BFMatcher()
    ra = prep(load(REF))
    kr, dr = sift.detectAndCompute(ra, None)
    pr = np.array([k.pt for k in kr])
    gm_r = inbox(pr, GBOX, PAD)
    print("ref kp %d  in-glyph %d  scene %d" % (len(kr), gm_r.sum(), (~gm_r).sum()))
    ctr = np.array([[[(GBOX[0] + GBOX[2]) / 2, (GBOX[1] + GBOX[3]) / 2]]], np.float32)
    rows = []
    for f, Hg in zip(frames, Hg0):
        a = prep(load(f))
        k, dd = sift.detectAndCompute(a, None)
        if dd is None:
            continue
        p = np.array([x.pt for x in k])
        # where is the glyph in this frame?
        gb = cv2.perspectiveTransform(np.float32(
            [[[GBOX[0], GBOX[1]]], [[GBOX[2], GBOX[1]]],
             [[GBOX[2], GBOX[3]]], [[GBOX[0], GBOX[3]]]]), np.linalg.inv(Hg))[:, 0, :]
        bb = (gb[:, 0].min(), gb[:, 1].min(), gb[:, 0].max(), gb[:, 1].max())
        gm = inbox(p, bb, PAD)
        mt = bf.knnMatch(dd, dr, k=2)
        good = [x for x, y in mt if x.distance < 0.8 * y.distance]
        res = {}
        for tag, want in (("scene", False), ("glyph", True)):
            sel = [g for g in good
                   if bool(gm[g.queryIdx]) == want and bool(gm_r[g.trainIdx]) == want]
            if len(sel) < 8:
                res[tag] = (None, len(sel)); continue
            src = np.float32([k[g.queryIdx].pt for g in sel]).reshape(-1, 1, 2)
            dst = np.float32([kr[g.trainIdx].pt for g in sel]).reshape(-1, 1, 2)
            H, msk = cv2.findHomography(src, dst, cv2.RANSAC, 3.0, maxIters=10000)
            res[tag] = ((H, int(msk.sum())) if H is not None and msk is not None
                        and msk.sum() >= 6 else (None, len(sel)))
        Hs = res["scene"][0]; Hgl = res["glyph"][0]
        if Hs is None or Hgl is None:
            rows.append(dict(f=int(f), scene_inl=res["scene"][1], glyph_inl=res["glyph"][1],
                             disp=None))
            continue
        cs = cv2.perspectiveTransform(
            cv2.perspectiveTransform(ctr, np.linalg.inv(Hgl)), Hs)[0, 0]
        disp = float(np.hypot(cs[0] - ctr[0, 0, 0], cs[1] - ctr[0, 0, 1]))
        rows.append(dict(f=int(f), scene_inl=res["scene"][1], glyph_inl=res["glyph"][1],
                         disp=disp))
        print(f, "scene_inl", res["scene"][1], "glyph_inl", res["glyph"][1],
              "disagreement px %.1f" % disp, flush=True)
    json.dump(rows, open(OUT + "motion_test.json", "w"), indent=1)
    dd = [r["disp"] for r in rows if r["disp"] is not None]
    if dd:
        print("\nN=%d  median disagreement %.1f px  p10 %.1f  p90 %.1f"
              % (len(dd), np.median(dd), np.percentile(dd, 10), np.percentile(dd, 90)))


main()
