#!/usr/bin/env python3.12
"""Direct codec control for the corner-dot artefact.

FINDINGS.md §17 and §22 conclude that the fixed dark dots in the corners of the
black frames are an AV1 tile-corner artefact rather than a mark placed in the
picture. That conclusion originally rested on a lucky comparison: a third party's
AVC-decoded frames lacked the stamp our AV1-decoded frames carried.

This runs the comparison deliberately, on the same YouTube video fetched twice in
two codecs. It is the falsifiable form of the claim: if the dots are authorial they
survive a change of codec, and if they are the encoder's tile grid they vanish.

Usage:
    python3.12 analysis/corner-dots/controls/codec_control.py

Requires videos/2026-avc/OpSTlDJWFFI.mkv — see CORPUS_QUALITY.md for how to fetch it.
"""
import io
import subprocess
import sys

import numpy as np
from PIL import Image

FRAME = 2  # a pure-black frame near the head of the May release
BLOCKS = [(0, 0), (0, 960)]  # (row, col) of the two 32x32 tile-column corners
SIZE = 32


def grab(src: str, n: int) -> np.ndarray:
    """One frame as luma, without range rescaling.

    Plain `-pix_fmt gray` maps limited-range Y (16..235) onto 0..255, which turns
    the Y=16/Y=17 distinction this test depends on into 0/1. Forcing full range in
    and out keeps the codeword values that FINDINGS quotes.
    """
    p = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", src,
         "-vf", rf"select=eq(n\,{n - 1}),scale=in_range=full:out_range=full",
         "-vsync", "0", "-pix_fmt", "gray", "-frames:v", "1",
         "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True, check=True,
    )
    return np.array(Image.open(io.BytesIO(p.stdout)))


def report(label: str, src: str) -> int:
    a = grab(src, FRAME)
    floor = a.min()
    hi = a > floor
    total = int(hi.sum())
    vals, cnts = np.unique(a, return_counts=True)

    print(f"\n=== {label}  ({src}) ===")
    print(f"  luma histogram      : {dict(zip(vals.tolist(), cnts.tolist()))}")
    print(f"  pixels above floor  : {total}")

    if not total:
        print("  no artefact present")
        return 0

    ys, xs = np.nonzero(hi)
    print(f"  bounding box        : rows {ys.min()}-{ys.max()}, cols {xs.min()}-{xs.max()}")

    inblock = sum(int((a[r:r + SIZE, c:c + SIZE] > floor).sum()) for r, c in BLOCKS)
    print(f"  inside the two 32x32 tile corners: {inblock} of {total}")

    left = a[0:SIZE, 0:SIZE]
    right = a[0:SIZE, 960:960 + SIZE]
    print(f"  left block == right block under +960 translation: "
          f"{np.array_equal(left, right)}")
    return total


def main() -> int:
    av1, avc = "videos/2026/OpSTlDJWFFI.mkv", "videos/2026-avc/OpSTlDJWFFI.mkv"
    n_av1 = report("AV1  (videos/2026/, the copy everything was measured on)", av1)
    try:
        n_avc = report("AVC  (videos/2026-avc/, the higher-bitrate copy)", avc)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"\n{avc} not present — see CORPUS_QUALITY.md for the fetch command.")
        return 2

    print("\n--- verdict ---")
    if n_av1 == 2048 and n_avc == 0:
        print("  Artefact present in AV1 at exactly 2048 px and absent in AVC.")
        print("  The dots are the encoder's tile grid. Not authorial. §17/§22 hold.")
        return 0
    print(f"  Unexpected: AV1={n_av1} (expected 2048), AVC={n_avc} (expected 0).")
    print("  This would be a real finding. Say so rather than assuming a setup error.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
