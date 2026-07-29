#!/usr/bin/env python3.12
"""Stage 3: deliverables + remaining controls.

  lineart   - window-agreement binarisation -> panel_lineart / glyph line art
  crops     - individual glyph crops, Lanczos-upscaled
  rect      - plane-normal estimate and rectified stack
  rot       - rotation control (0/90/180/270)
  inject    - synthetic-glyph injection control
  control2  - a genuinely empty control ROI
  best      - single least-degraded raw frame
  panel2    - wide panel stack re-registered on the panel region itself
"""
import numpy as np, cv2, sys, json

FR = "/home/user/new-skinny-bob/frames/l9RAhmPHM_A/f%05d.png"
O = "/home/user/new-skinny-bob/analysis/symbol-panel/"
PB = (263, 60, 1561, 1043)
REF = 1694
TCM = (469 - PB[0], 938 - PB[1], 968 - PB[0], 1002 - PB[1])
GL, Z = (400, 500, 730, 810), 3.0
sys.path.insert(0, O)
from stack import (load, pic, warp, smat, canvas_size, stack_frames, enhance, u8, sel, CANVAS)


def norm(x):
    x = np.nan_to_num(x, nan=np.nanmedian(x))
    bg = cv2.GaussianBlur(x, (0, 0), 60)
    x = x - bg
    lo, hi = np.percentile(x, (1, 99.8))
    return np.clip((x - lo) / (hi - lo + 1e-9), 0, 1)


# ---------------------------------------------------------------- line art
def lineart():
    full = norm(np.load(O + "glyph_stack.npy"))
    wins = [norm(np.load(O + f"glyph_win{j}.npy")) for j in range(4)]
    # per-window threshold at a fixed area fraction, so a dimmer window is not
    # penalised for being dim -- what must agree is WHERE the ink is.
    frac = 0.055
    ths = [np.percentile(w, 100 * (1 - frac)) for w in wins]
    votes = np.sum([w > t for w, t in zip(wins, ths)], 0)
    th = np.percentile(full, 100 * (1 - frac))
    solid = (votes >= 3) & (full > th)
    unc = (votes >= 2) & (full > np.percentile(full, 100 * (1 - frac * 1.8))) & ~solid
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    solid = cv2.morphologyEx(solid.astype(np.uint8), cv2.MORPH_OPEN, k)
    solid = cv2.morphologyEx(solid, cv2.MORPH_CLOSE, k)
    unc = cv2.morphologyEx(unc.astype(np.uint8), cv2.MORPH_OPEN, k)
    # drop specks
    for m in (solid, unc):
        n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
        for i in range(1, n):
            if st[i, cv2.CC_STAT_AREA] < 250:
                m[lab == i] = 0
    up = 2
    S_ = lambda a: cv2.resize(a, None, fx=up, fy=up, interpolation=cv2.INTER_CUBIC)
    ss, uu = S_(solid.astype(np.float32)) > 0.5, S_(unc.astype(np.float32)) > 0.5
    art = np.full(ss.shape, 255, np.uint8)
    art[ss] = 0
    cv2.imwrite(O + "glyph_lineart.png", art)
    art2 = np.full(ss.shape + (3,), 255, np.uint8)
    art2[uu] = (170, 170, 170)
    art2[ss] = (0, 0, 0)
    cv2.imwrite(O + "glyph_lineart_uncertain.png", art2)
    print("line art: solid px %d  uncertain px %d" % (ss.sum(), uu.sum()))
    # same treatment for the wide panel
    p = norm(np.load(O + "panel_stack.npy"))
    pm = (p > 0.66).astype(np.uint8)
    pm = cv2.morphologyEx(pm, cv2.MORPH_OPEN, k)
    n, lab, st, _ = cv2.connectedComponentsWithStats(pm, 8)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] < 200:
            pm[lab == i] = 0
    pa = np.full(pm.shape, 255, np.uint8); pa[pm > 0] = 0
    cv2.imwrite(O + "panel_lineart.png",
                cv2.resize(pa, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC))


# ------------------------------------------------------------------- crops
GLYPHS = {   # name: bbox in glyph-canvas coords (990x930)
    "01_full_cluster":   (120, 90, 900, 880),
    "02_left_crescent":  (140, 130, 400, 860),
    "03_double_minim":   (330, 100, 640, 880),
    "04_flag_and_bar":   (520, 100, 900, 830),
}


def crops():
    g = norm(np.load(O + "glyph_stack.npy"))
    rl = cv2.imread(O + "glyph_stack_rl.png", cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
    for nm, (x0, y0, x1, y1) in GLYPHS.items():
        for tag, src in (("", g), ("_sharp", rl)):
            m = 60
            c = src[max(y0 - m, 0):y1 + m, max(x0 - m, 0):x1 + m]
            c = (c - c.min()) / (np.ptp(c) + 1e-9)
            out = cv2.resize(c, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LANCZOS4)
            cv2.imwrite(O + f"glyph_{nm}{tag}.png", u8(out))
    print("crops written")


# --------------------------------------------------------- plane / rectify
def rect():
    d = np.load(O + "reg2_1099_1760.npz")
    m = sel(d)
    H = d["H"][m]; fr = d["frames"][m]
    W = PB[2] - PB[0]; Hh = PB[3] - PB[1]
    res = {}
    for fmul in (0.9, 1.2, 1.6):
        f = fmul * W
        K = np.array([[f, 0, W / 2], [0, f, Hh / 2], [0, 0, 1]])
        ns = []
        for h, fnum in zip(H, fr):
            if abs(fnum - REF) < 25:
                continue
            try:
                _, R, T, N = cv2.decomposeHomographyMat(np.linalg.inv(h), K)
            except cv2.error:
                continue
            for n in N:
                n = n.ravel()
                if n[2] < 0:
                    n = -n
                ns.append(n)
        if not ns:
            continue
        ns = np.array(ns)
        # cluster: keep normals within 35 deg of the modal direction
        best, bn = 0, None
        for c in ns[::7]:
            k = (ns @ c > np.cos(np.deg2rad(35))).sum()
            if k > best:
                best, bn = k, c
        nn = ns[ns @ bn > np.cos(np.deg2rad(35))].mean(0)
        nn /= np.linalg.norm(nn)
        tilt = np.degrees(np.arccos(abs(nn[2])))
        res[fmul] = (nn.tolist(), float(tilt), int(best), len(ns))
        print("f=%.1f*W  plane normal %s  tilt from fronto-parallel %.1f deg  (%d/%d)"
              % (fmul, np.round(nn, 3), tilt, best, len(ns)))
    json.dump(res, open(O + "plane_estimate.json", "w"), indent=1)
    # rectify the glyph stack with the median tilt
    tilts = [v[1] for v in res.values()]
    tilt = float(np.median(tilts)) if tilts else 0.0
    nn = np.array(res[1.2][0]) if 1.2 in res else np.array([0, 0, 1.0])
    g = np.load(O + "glyph_stack.npy")
    cw, ch = canvas_size(GL, Z)
    f = 1.2 * (PB[2] - PB[0]) * Z
    K = np.array([[f, 0, cw / 2], [0, f, ch / 2], [0, 0, 1]])
    z = np.array([0, 0, 1.0])
    v = np.cross(nn, z); s = np.linalg.norm(v)
    if s > 1e-6:
        vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        R = np.eye(3) + vx + vx @ vx * ((1 - nn @ z) / s ** 2)
    else:
        R = np.eye(3)
    Hr = K @ R @ np.linalg.inv(K)
    out = cv2.warpPerspective(np.nan_to_num(g, nan=float(np.nanmedian(g))), Hr, (cw, ch),
                              flags=cv2.INTER_LANCZOS4)
    cv2.imwrite(O + "panel_rectified_stack.png",
                u8(enhance(out, 3 * 2.7, upsample=1.6)))
    cv2.imwrite(O + "glyph_stack_upscaled.png",
                u8(enhance(g, 3 * 2.7, upsample=1.6)))
    print("median tilt estimate %.1f deg" % tilt)


# ------------------------------------------------------------- rotation
def rot():
    a = cv2.imread(O + "glyph_lineart.png", cv2.IMREAD_GRAYSCALE)
    a = cv2.resize(a, (a.shape[1] // 2, a.shape[0] // 2))
    t = [a, cv2.rotate(a, cv2.ROTATE_90_CLOCKWISE), cv2.rotate(a, cv2.ROTATE_180),
         cv2.rotate(a, cv2.ROTATE_90_COUNTERCLOCKWISE)]
    s = max(max(x.shape) for x in t)
    sheet = np.full((s + 34, 4 * s, 3), 255, np.uint8)
    for i, x in enumerate(t):
        h, w = x.shape
        sheet[34:34 + h, i * s:i * s + w] = cv2.cvtColor(x, cv2.COLOR_GRAY2BGR)
        cv2.putText(sheet, ["0", "90", "180", "270"][i] + " deg", (i * s + 8, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.imwrite(O + "rotation_test.png", sheet)
    print("rotation_test.png")


# ------------------------------------------------------------ injection
def synth(h, w):
    """known target: bars of 3/6/10 px stroke width, a ring, a diagonal, a hook"""
    m = np.zeros((h, w), np.float32)
    y0, y1 = int(0.18 * h), int(0.82 * h)
    for i, t in enumerate((3, 6, 10)):
        x = int((0.14 + 0.11 * i) * w)
        cv2.line(m, (x, y0), (x, y1), 1.0, t)
    cv2.circle(m, (int(0.62 * w), int(0.34 * h)), int(0.14 * h), 1.0, 6)
    cv2.line(m, (int(0.50 * w), int(0.80 * h)), (int(0.80 * w), int(0.52 * h)), 1.0, 6)
    cv2.ellipse(m, (int(0.76 * w), int(0.74 * h)), (int(0.09 * w), int(0.11 * h)),
                0, 180, 360, 1.0, 4)
    return cv2.GaussianBlur(m, (0, 0), 1.0)


def inject():
    d = np.load(O + "reg2_1099_1760.npz")
    m = sel(d)
    fr, H = d["frames"][m], d["H"][m]
    rectp = (760, 520, 950, 760)          # empty panel area in ref picture coords
    W = rectp[2] - rectp[0]; Hh = rectp[3] - rectp[1]
    tgt = synth(Hh, W)
    big = np.zeros((PB[3] - PB[1], PB[2] - PB[0]), np.float32)
    big[rectp[1]:rectp[3], rectp[0]:rectp[2]] = tgt
    for amp in (40.0, 12.0, 4.0):
        def add(c, f, h, amp=amp):
            w = cv2.warpPerspective(big, np.linalg.inv(h), (c.shape[1], c.shape[0]),
                                    flags=cv2.INTER_LANCZOS4)
            return c + amp * w
        cv = ((rectp[0] - 60, rectp[1] - 60, rectp[2] + 60, rectp[3] + 60), 3.0)
        out, n, k = stack_frames(fr, H, cv[0], cv[1], extra=add)
        cv2.imwrite(O + f"injection_amp{int(amp)}.png", u8(enhance(out, 3 * 2.7, upsample=1.2)))
        print("injection amp", amp, "layers", k)
    # ground truth render
    cv2.imwrite(O + "injection_truth.png",
                u8(cv2.resize(tgt, None, fx=3.6, fy=3.6, interpolation=cv2.INTER_LANCZOS4)))
    # assemble
    ims = [cv2.imread(O + "injection_truth.png"),
           *[cv2.imread(O + f"injection_amp{a}.png") for a in (40, 12, 4)]]
    hh = min(i.shape[0] for i in ims)
    ims = [cv2.resize(i, (int(i.shape[1] * hh / i.shape[0]), hh)) for i in ims]
    lab = ["injected target", "amp 40 (~real stroke)", "amp 12", "amp 4"]
    sheet = np.zeros((hh + 34, sum(i.shape[1] for i in ims), 3), np.uint8)
    x = 0
    for i, l in zip(ims, lab):
        sheet[34:34 + hh, x:x + i.shape[1]] = i
        cv2.putText(sheet, l, (x + 8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        x += i.shape[1]
    cv2.imwrite(O + "injection_test.png", sheet)


def control2():
    d = np.load(O + "reg2_1099_1760.npz")
    m = sel(d)
    fr, H = d["frames"][m], d["H"][m]
    for tag, rectp in (("a", (760, 500, 1090, 810)), ("b", (400, 130, 730, 440))):
        out, n, k = stack_frames(fr, H, rectp, 3.0)
        if out is None:
            print("control", tag, "empty"); continue
        cv2.imwrite(O + f"control_roi_{tag}.png", u8(enhance(out, 3 * 2.7)))
        g = norm(np.load(O + "glyph_stack.npy")); c = norm(out)
        print("control", tag, "layers", k,
              "p99.5 %.3f (glyph %.3f)" % (np.percentile(c, 99.5), np.percentile(g, 99.5)),
              "frac>0.62 %.4f (glyph %.4f)" % ((c > .62).mean(), (g > .62).mean()))
    a = cv2.imread(O + "control_roi_a.png"); b = cv2.imread(O + "control_roi_b.png")
    g = cv2.imread(O + "glyph_stack_lin.png")
    s = np.hstack([cv2.resize(x, (g.shape[1], g.shape[0])) for x in (g, a, b)])
    for i, l in enumerate(["glyph ROI", "control ROI a", "control ROI b"]):
        cv2.putText(s, l, (i * g.shape[1] + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0, 255, 255), 2)
    cv2.imwrite(O + "control_roi.png", s)


def best():
    i = 1694
    a = pic(load(i))
    c = a[430:800, 330:720]
    lo, hi = np.percentile(c, (1, 99.7))
    c = np.clip((c - lo) / (hi - lo), 0, 1)
    cv2.imwrite(O + "single_best_frame.png",
                u8(cv2.resize(c, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_LANCZOS4)))
    w = a[200:800, 250:1000]
    lo, hi = np.percentile(w, (1, 99.7))
    w = np.clip((w - lo) / (hi - lo), 0, 1)
    cv2.imwrite(O + "single_best_frame_wide.png",
                u8(cv2.resize(w, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LANCZOS4)))
    print("single best frame f%05d" % i)


def panel2():
    """re-register on the upper panel (dials/ticks) instead of the glyph"""
    import cv2 as C
    d = np.load(O + "reg2_1099_1760.npz")
    m = sel(d)
    fr, H = d["frames"][m], d["H"][m]
    band = (fr >= 1668) & (fr <= 1716)
    fr, H = fr[band], H[band]
    rectp, z = (450, 200, 1000, 620), 2.0
    ra = pic(load(REF))
    ref = warp(ra, np.eye(3), rectp, z, border=0)
    crit = (C.TERM_CRITERIA_EPS | C.TERM_CRITERIA_COUNT, 120, 1e-7)
    S_ = smat(rectp, z)
    Hs = []
    for f, h in zip(fr, H):
        c = pic(load(f))
        w = warp(c, h, rectp, z, border=0)
        rn = ((ref - ref.mean()) / (ref.std() + 1e-6)).astype(np.float32)
        wn = ((w - w.mean()) / (w.std() + 1e-6)).astype(np.float32)
        try:
            W = np.eye(3, dtype=np.float32)
            _, W = C.findTransformECC(rn, wn, W, C.MOTION_HOMOGRAPHY, crit, None, 5)
            hh = np.linalg.inv(S_) @ np.linalg.inv(W.astype(np.float64)) @ S_ @ h
            hh /= hh[2, 2]
            Hs.append(hh if np.isfinite(hh).all() else h)
        except C.error:
            Hs.append(h)
    out, n, k = stack_frames(fr, np.array(Hs), rectp, z)
    np.save(O + "panel2_stack.npy", out)
    cv2.imwrite(O + "panel_stack_panelreg.png", u8(enhance(out, 2 * 2.7, upsample=1.5)))
    print("panel2 stacked", k)


for a in sys.argv[1:]:
    globals()[a]()
