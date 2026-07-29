"""Stack all near-black frames per video, high gain, to reveal the faint ghost geometry."""
import numpy as np, os, subprocess, sys
from PIL import Image

OUT = "analysis/ghost-disc"
os.makedirs(OUT, exist_ok=True)

def save(acc, n, tag):
    if n == 0:
        print(tag, "no black frames"); return
    avg = acc / n
    g = np.clip(avg * 60, 0, 255).astype(np.uint8)
    Image.fromarray(g).save(f"{OUT}/stack_{tag}_n{n}.png")
    print(tag, "stacked", n, "frames; mean-of-avg %.4f" % avg.mean())

# 2026: pre-extracted PNG frames
for vid in ["OpSTlDJWFFI", "Oqw96jCOP7A", "l9RAhmPHM_A"]:
    d = f"frames/{vid}"
    acc = None; n = 0
    for fn in sorted(os.listdir(d)):
        a = np.asarray(Image.open(os.path.join(d, fn)).convert('L'), np.float64)
        if a.max() <= 6:
            acc = a if acc is None else acc + a
            n += 1
    save(acc if acc is not None else np.zeros((1080,1920)), n, vid)

# 2011: decode mkv, stream rawvideo gray
for vid in ["RsQCXN4o4Ps", "Xju_CY5ZESA", "ZB788PtqQvg", "a6TLGkrfNKI"]:
    f = f"videos/2011/{vid}.mkv"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", f, "-f", "rawvideo",
                          "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
    # probe dims
    import json
    pr = subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
                         "-show_entries","stream=width,height","-of","json",f],
                        capture_output=True, text=True)
    st = json.loads(pr.stdout)["streams"][0]
    w, h = st["width"], st["height"]
    fsz = w*h
    acc = np.zeros((h, w), np.float64); n = 0; total = 0
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz: break
        total += 1
        a = np.frombuffer(buf, np.uint8)
        if a.max() <= 6:
            acc += a.reshape(h, w); n += 1
    p.wait()
    print(vid, "total frames", total)
    save(acc, n, vid)
