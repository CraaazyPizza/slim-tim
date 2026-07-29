#!/usr/bin/env python3.12
import os, sys, glob, hashlib, json
import numpy as np
from PIL import Image

BASE = "/home/user/new-skinny-bob/analysis/third-party-toolkit/extracted/2026-05-25_Confidential leaked ufo-ebe footage continuation of disclosure"
OURS = "/home/user/new-skinny-bob/frames/OpSTlDJWFFI"

def lc_frames():
    d = {}
    for dirp in sorted(os.listdir(BASE)):
        fp = os.path.join(BASE, dirp)
        if not os.path.isdir(fp): continue
        for f in sorted(os.listdir(fp)):
            if f.endswith(".png"):
                n = int(f.split("_")[1].split(".")[0])
                d[n] = os.path.join(fp, f)
    return d

def arr(p):
    return np.asarray(Image.open(p).convert("RGB"), dtype=np.uint8)

def fhash(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def phash(p):  # hash of decoded pixels
    return hashlib.sha256(arr(p).tobytes()).hexdigest()

def main():
    lc = lc_frames()
    ns = sorted(lc)
    print(f"LC frames present: {len(ns)}  range {ns[0]}..{ns[-1]}  contiguous={ns==list(range(ns[0],ns[-1]+1))}")

    # ---- offset search using pixel hashes on a probe set
    probes = [n for n in ns if n % 97 == 3][:20]
    ourhash = {}
    print("\n=== offset search (pixel-hash) ===")
    best = None
    for off in range(-5, 6):
        hit = 0
        for n in probes:
            o = os.path.join(OURS, f"f{n+off:05d}.png")
            if not os.path.exists(o): continue
            if o not in ourhash: ourhash[o] = phash(o)
            if ourhash[o] == phash(lc[n]): hit += 1
        print(f"  offset {off:+d}: {hit}/{len(probes)} pixel-identical")
        if best is None or hit > best[1]: best = (off, hit)
    off = best[0]
    print(f"best offset = {off:+d} ({best[1]}/{len(probes)})")

    # ---- full sweep: every 10th frame across the whole carved range + all in first/last
    sample = sorted(set([n for n in ns if n % 10 == 1] + ns[:15] + ns[-15:]
                        + [n for n in ns if 910 <= n <= 925]))
    rows = []
    n_fileident = n_pixident = 0
    for n in sample:
        o = os.path.join(OURS, f"f{n+off:05d}.png")
        if not os.path.exists(o): continue
        a = arr(lc[n]); b = arr(o)
        if a.shape != b.shape:
            rows.append(dict(n=n, note=f"shape {a.shape} vs {b.shape}")); continue
        fi = fhash(lc[n]) == fhash(o)
        d = a.astype(np.int16) - b.astype(np.int16)
        mx = int(np.abs(d).max())
        pi = mx == 0
        n_fileident += fi; n_pixident += pi
        rows.append(dict(n=n, ours=n+off, file_ident=bool(fi), pix_ident=bool(pi),
                         maxabs=mx, rms=float(np.sqrt((d.astype(np.float64)**2).mean())),
                         mad=float(np.abs(d).mean()),
                         pct_diff=float((np.abs(d) > 0).mean() * 100),
                         pct_gt1=float((np.abs(d) > 1).mean() * 100),
                         pct_gt2=float((np.abs(d) > 2).mean() * 100)))
    print(f"\n=== compared {len(rows)} frames ===")
    print(f"byte-identical files : {n_fileident}/{len(rows)}")
    print(f"pixel-identical      : {n_pixident}/{len(rows)}")
    ok = [r for r in rows if "maxabs" in r]
    mxs = np.array([r["maxabs"] for r in ok])
    rmss = np.array([r["rms"] for r in ok])
    pds = np.array([r["pct_diff"] for r in ok])
    print(f"maxabs   : min {mxs.min()} med {np.median(mxs)} mean {mxs.mean():.2f} max {mxs.max()}")
    print(f"rms      : min {rmss.min():.4f} med {np.median(rmss):.4f} mean {rmss.mean():.4f} max {rmss.max():.4f}")
    print(f"%px diff : min {pds.min():.3f} med {np.median(pds):.3f} mean {pds.mean():.3f} max {pds.max():.3f}")
    print(f"frames with maxabs<=1: {(mxs<=1).sum()}  <=2: {(mxs<=2).sum()}  <=4: {(mxs<=4).sum()}  <=8: {(mxs<=8).sum()}")

    print("\n n     ours  fileid pixid  maxabs      rms    %diff   %>1    %>2")
    for r in ok[::max(1, len(ok)//60)]:
        print(f"{r['n']:5d} {r['ours']:6d}  {str(r['file_ident'])[0]}      {str(r['pix_ident'])[0]}"
              f"    {r['maxabs']:4d}  {r['rms']:8.4f} {r['pct_diff']:7.3f} {r['pct_gt1']:6.3f} {r['pct_gt2']:6.3f}")

    json.dump(dict(offset=off, rows=rows), open("/home/user/new-skinny-bob/analysis/third-party-toolkit/compare.json", "w"), indent=1)

    # ---- worst frames detail
    ok.sort(key=lambda r: -r["rms"])
    print("\n=== 10 worst frames by RMS ===")
    for r in ok[:10]:
        print(f"  f{r['n']} maxabs={r['maxabs']} rms={r['rms']:.4f} %diff={r['pct_diff']:.2f}")
    print("\n=== 10 best (non-identical) ===")
    nz = [r for r in ok if r["maxabs"] > 0]
    nz.sort(key=lambda r: r["rms"])
    for r in nz[:10]:
        print(f"  f{r['n']} maxabs={r['maxabs']} rms={r['rms']:.4f} %diff={r['pct_diff']:.2f}")

if __name__ == "__main__":
    main()
