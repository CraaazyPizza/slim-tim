#!/usr/bin/env python3.12
import os, sys, struct, glob, collections, hashlib

def chunks(path, maxread=None):
    out = []
    with open(path, "rb") as f:
        sig = f.read(8)
        assert sig == b"\x89PNG\r\n\x1a\n", (path, sig[:8])
        while True:
            hdr = f.read(8)
            if len(hdr) < 8: break
            ln, typ = struct.unpack(">I4s", hdr)
            data = f.read(ln) if (ln < 200 or typ in (b"IHDR", b"tEXt", b"iTXt", b"zTXt", b"pHYs", b"tIME", b"gAMA", b"cHRM", b"sRGB", b"iCCP", b"bKGD", b"sBIT")) else None
            if data is None:
                f.seek(ln, 1)
            f.read(4)
            out.append((typ.decode("latin1"), ln, data))
            if typ == b"IEND": break
    return out

def describe(path):
    cs = chunks(path)
    ihdr = [c for c in cs if c[0] == "IHDR"][0][2]
    w, h, bd, ct, comp, filt, il = struct.unpack(">IIBBBBB", ihdr)
    idats = [c for c in cs if c[0] == "IDAT"]
    order = [c[0] for c in cs]
    # collapse repeated IDAT
    coll = []
    for t in order:
        if coll and coll[-1][0] == t: coll[-1][1] += 1
        else: coll.append([t, 1])
    anc = {}
    for t, ln, d in cs:
        if t in ("tEXt", "iTXt", "zTXt", "pHYs", "tIME", "gAMA", "cHRM", "sRGB", "sBIT", "bKGD", "iCCP"):
            anc[t] = d
    return dict(path=path, w=w, h=h, bitdepth=bd, colortype=ct, compression=comp,
                filter=filt, interlace=il, n_idat=len(idats),
                idat_sizes=[c[1] for c in idats][:6],
                idat_total=sum(c[1] for c in idats),
                order="+".join(f"{t}x{n}" if n > 1 else t for t, n in coll),
                ancillary={k: (v[:80] if v else None) for k, v in anc.items()},
                filesize=os.path.getsize(path))

if __name__ == "__main__":
    for p in sys.argv[1:]:
        d = describe(p)
        print(f"--- {os.path.basename(p)} ({os.path.dirname(p).split('/')[-1]})")
        for k, v in d.items():
            if k != "path": print(f"    {k}: {v}")
