#!/usr/bin/env python3.12
"""Figures for the colour-segment duplicate count.

Two panels:

`contact_sheet.png` -- representative pairs with the difference amplified, chosen by
rank within the measured distribution rather than by frame number, so the sheet
follows the data if the data changes. This carries the qualitative discriminator,
which is stronger than any threshold: a conform duplicate differs from its neighbour
only by blocky codec quantisation noise, while a genuinely advancing pair differs
along object edges. Per docs/PITFALLS.md the frames themselves are shown unmodified;
only the third column, explicitly labelled, is amplified.

`phase_signature.png` -- every pair in the segment plotted against phase, which is
where the result is visible without any statistics at all.

Usage:
    python3.12 analysis/colour-duplicate-count/sheet.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GAIN = 24  # difference amplification, labelled on the figure


def main() -> None:
    doc = json.loads((HERE / "pairs_av1.json").read_text())
    res = json.loads((HERE / "classification.json").read_text())["av1"]
    lo, hi = doc["segment"]
    seg = [r for r in doc["pairs"] if lo <= r["a"] and r["b"] <= hi]
    framedir = ROOT / doc["frame_dir"]

    dom = res["dominant_phase_a"]
    onph = sorted([r for r in seg if r["phase"] == dom], key=lambda r: r["mad_y"])
    offph = sorted([r for r in seg if r["phase"] != dom], key=lambda r: r["mad_y"])

    picks = [
        (onph[0], "duplicate, strongest"),
        (onph[1], "duplicate"),
        (onph[len(onph) // 2], "duplicate, median"),
        (onph[-2], "duplicate, 2nd-weakest"),
        (onph[-1], "duplicate, weakest"),
        (offph[0], "control, closest non-duplicate"),
        (offph[1], "control"),
        (offph[len(offph) // 2], "control, median"),
    ]

    def load(n: int) -> np.ndarray:
        return np.asarray(Image.open(framedir / f"f{n:05d}.png")
                          .convert("RGB")).astype(np.float64)

    fig, axes = plt.subplots(len(picks), 3, figsize=(13.6, 2.05 * len(picks)))
    for row, (r, tag) in enumerate(picks):
        a, b = load(r["a"]), load(r["b"])
        d = np.abs(a - b).mean(axis=2)
        for col, (img, cmap) in enumerate([(a / 255, None), (b / 255, None),
                                           (np.clip(d * GAIN / 255, 0, 1), "inferno")]):
            ax = axes[row, col]
            ax.imshow(img, cmap=cmap, vmin=0, vmax=1)
            ax.set_xticks([]), ax.set_yticks([])
        axes[row, 0].set_ylabel(f"f{r['a']}→f{r['b']}\nphase {r['phase']}",
                                fontsize=8, rotation=0, ha="right", va="center",
                                labelpad=34)
        axes[row, 0].set_title(f"f{r['a']} (unmodified)", fontsize=8)
        axes[row, 1].set_title(f"f{r['b']} (unmodified)", fontsize=8)
        axes[row, 2].set_title(f"|difference| ×{GAIN}    mad_y={r['mad_y']:.4f}  "
                               f"norm={r['norm']:.3f}    {tag}", fontsize=8)

    fig.suptitle(f"{doc['video']} f{lo}-{hi} ({doc['copy'].upper()} copy) — "
                 f"consecutive-pair duplicate check\n"
                 f"duplicates differ by block noise only; controls differ along edges. "
                 f"phase = frame index mod 12", fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.965])
    fig.savefig(HERE / "contact_sheet.png", dpi=95)
    print(f"wrote {(HERE / 'contact_sheet.png').relative_to(ROOT)}")

    fig2, ax = plt.subplots(figsize=(13.6, 4.2))
    for p in range(12):
        v = [r["mad_y"] for r in seg if r["phase"] == p]
        ax.scatter([p] * len(v), v, s=14, alpha=0.65,
                   color="crimson" if p == dom else "steelblue")
    ax.set_yscale("log")
    ax.set_xticks(range(12))
    ax.set_xlabel("phase (frame index a mod 12)")
    ax.set_ylabel("mean absolute luma difference to next frame")
    ax.axhline(res["max_mad_y_on_phase"], ls="--", lw=0.9, color="crimson",
               label=f"highest phase-{dom} pair ({res['max_mad_y_on_phase']:.3f})")
    ax.axhline(res["min_mad_y_off_phase"], ls="--", lw=0.9, color="steelblue",
               label=f"lowest other pair ({res['min_mad_y_off_phase']:.3f})")
    ax.set_title(f"Every consecutive pair in f{lo}-{hi} by phase — the two "
                 f"populations do not overlap ({doc['copy'].upper()} copy)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.25)
    fig2.tight_layout()
    fig2.savefig(HERE / "phase_signature.png", dpi=95)
    print(f"wrote {(HERE / 'phase_signature.png').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
