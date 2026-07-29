#!/usr/bin/env python3.12
from PIL import Image
import os
B = "/home/user/new-skinny-bob"
O = B + "/analysis/compare-eras/band/mont"
os.makedirs(O, exist_ok=True)
SPEC = [
 ("frames/OpSTlDJWFFI", [300,900,1500,2100,2700]),
 ("frames/Oqw96jCOP7A", [250,750,1250,1750,2250]),
 ("frames/l9RAhmPHM_A", [400,1200,2000,2800,3600]),
 ("frames/ZB788PtqQvg", [100,350,600,850,1100]),
 ("frames/RsQCXN4o4Ps", [120,420,720,1020,1380]),
 ("frames/Xju_CY5ZESA", [200,700,1200,1700,2400]),
 ("frames/a6TLGkrfNKI", [200,700,1200,1700,2200]),
]
for d, ns in SPEC:
    ims = []
    for n in ns:
        p = f"{B}/{d}/f{n:05d}.png"
        im = Image.open(p).convert("RGB")
        r = 300 / im.height
        ims.append(im.resize((int(im.width*r), 300)))
    w = sum(i.width for i in ims)
    out = Image.new("RGB", (w, 300)); x = 0
    for i in ims:
        out.paste(i, (x, 0)); x += i.width
    out.save(f"{O}/{os.path.basename(d)}.png")
    print(os.path.basename(d), out.size)
