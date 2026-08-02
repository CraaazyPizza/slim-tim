#!/usr/bin/env python3.12
"""Consecutive-frame similarity scan of the colour Mk.5 segment, OpSTlDJWFFI f2571-2917.

Two reports disagree about how many frame duplicates this segment contains.
`reports/agent_video1_OpSTlDJWFFI.md` §"Underlying temporal structure" lists a
period-12 series f2578, 2590, 2602 ... 2878 (26 frames). `reports/agent_mk5_claims.md`
item 5e re-measures the same segment and finds "3 near-identical consecutive pairs in
346 frames", calling the period-12 conform "only weakly expressed here". The count
matters because FINDINGS §20 multiplies frames-per-tick by 11/12 to get the colour
clip's distinct-images-per-source-second figure, and that factor is only valid if the
conform really is fully expressed in this segment.

This scans every consecutive pair with no period-12 prior of any kind. Phase is
recorded but never used to select, threshold or weight anything -- phase purity is a
result of the scan, not an input to it. Classification lives in `classify.py`, which
derives its threshold from the distribution this script writes.

Usage:
    python3.12 analysis/colour-duplicate-count/dupdetect.py            # AV1 copy
    python3.12 analysis/colour-duplicate-count/dupdetect.py --copy avc # AVC copy

Requires frames extracted first, which is what the hashes in the output pin down:
    bin/frames OpSTlDJWFFI 2570 2918
    bin/frames --avc OpSTlDJWFFI 2570 2918
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import PIL
from PIL import Image

# Repo root, located from this file rather than hardcoded. analysis/<dir>/<script>.
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

VIDEO = "OpSTlDJWFFI"
SEG_LO, SEG_HI = 2571, 2917  # colour Mk.5 segment, CORRECTIONS.md entry 9
MARGIN = 1                   # one frame either side so the edge pairs are real pairs

COPIES = {"av1": ("frames", "videos/2026"), "avc": ("frames-avc", "videos/2026-avc")}


def tool_versions() -> dict:
    """Record the decode and compute environment. The decoder is part of the method
    here -- see docs/PITFALLS.md -- so a rerun that disagrees should be able to tell
    whether it was looking at different pixels or running different arithmetic."""
    try:
        ff = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True,
                            check=True).stdout.splitlines()[0]
    except (OSError, subprocess.CalledProcessError):
        ff = "unavailable"
    return {
        "ffmpeg": ff,
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "pillow": PIL.__version__,
    }


def luma(rgb: np.ndarray) -> np.ndarray:
    """Rec.709 luma. Float64 throughout so the result does not depend on the order
    numpy happens to reduce in."""
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def scan(framedir: Path, lo: int, hi: int) -> tuple[list[dict], dict[str, str]]:
    """Every consecutive pair in [lo, hi], plus the SHA-256 of each input PNG."""
    hashes: dict[str, str] = {}

    def load(n: int) -> np.ndarray:
        p = framedir / f"f{n:05d}.png"
        raw = p.read_bytes()
        hashes[p.name] = hashlib.sha256(raw).hexdigest()
        return np.asarray(Image.open(p).convert("RGB"))

    rows: list[dict] = []
    prev = load(lo)
    prev_y = luma(prev.astype(np.float64))

    for n in range(lo + 1, hi + 1):
        cur = load(n)
        cur_y = luma(cur.astype(np.float64))
        d = np.abs(cur.astype(np.int16) - prev.astype(np.int16))
        dy = np.abs(cur_y - prev_y)

        rows.append({
            "a": n - 1,
            "b": n,
            "exact": bool(hashes[f"f{n:05d}.png"] == hashes[f"f{n - 1:05d}.png"]),
            "mad_y": float(dy.mean()),
            "mad_rgb": float(d.mean()),
            "max_y": float(dy.max()),
            "max_rgb": int(d.max()),
            "frac_gt4": float((d > 4).any(axis=2).mean()),
            "phase": (n - 1) % 12,
        })
        prev, prev_y = cur, cur_y

    return rows, hashes


def add_local_norm(rows: list[dict], half: int = 6) -> None:
    """Each pair's mad_y against the median of its neighbours, excluding itself.

    A raw threshold cannot work across this segment: local motion varies by more than
    an order of magnitude between the static interior shots and the flare-swept tail,
    so an absolute cut calibrated anywhere is wrong everywhere else. That is precisely
    the failure this scan exists to check for."""
    mad = np.array([r["mad_y"] for r in rows])
    for i, r in enumerate(rows):
        lo, hi = max(0, i - half), min(len(rows), i + half + 1)
        win = np.concatenate([mad[lo:i], mad[i + 1:hi]])
        med = float(np.median(win))
        r["local_med"] = med
        r["norm"] = float(r["mad_y"] / med) if med > 0 else float("nan")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--copy", choices=sorted(COPIES), default="av1",
                    help="which of the two corpus copies to measure (CORPUS_QUALITY.md)")
    args = ap.parse_args()

    framedir = ROOT / COPIES[args.copy][0] / VIDEO
    if not framedir.is_dir():
        sys.exit(f"no {framedir.relative_to(ROOT)} -- run: bin/frames "
                 f"{'--avc ' if args.copy == 'avc' else ''}{VIDEO} "
                 f"{SEG_LO - MARGIN} {SEG_HI + MARGIN}")

    rows, hashes = scan(framedir, SEG_LO - MARGIN, SEG_HI + MARGIN)
    add_local_norm(rows)
    seg = [r for r in rows if SEG_LO <= r["a"] and r["b"] <= SEG_HI]

    out = {
        "video": VIDEO,
        "copy": args.copy,
        "source_video": COPIES[args.copy][1] + f"/{VIDEO}.mkv",
        "frame_dir": COPIES[args.copy][0] + f"/{VIDEO}",
        "segment": [SEG_LO, SEG_HI],
        "loaded": [SEG_LO - MARGIN, SEG_HI + MARGIN],
        "n_pairs_segment": len(seg),
        "tool_versions": tool_versions(),
        "frame_sha256": hashes,
        "pairs": rows,
    }
    dest = HERE / f"pairs_{args.copy}.json"
    dest.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")

    print(f"{args.copy}: {len(seg)} pairs in f{SEG_LO}-{SEG_HI}, "
          f"{len(hashes)} frames hashed -> {dest.relative_to(ROOT)}")
    print(f"  ffmpeg: {out['tool_versions']['ffmpeg']}")


if __name__ == "__main__":
    main()
