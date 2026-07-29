#!/usr/bin/env python3.12
"""Two figures for PIPELINE.md. Palette validated via dataviz validate_palette.js."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#dedcd6"
BLUE = "#2a78d6"     # categorical slot 1
ORANGE = "#eb6834"   # categorical slot 2

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "font.size": 10, "text.color": INK,
    "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.edgecolor": GRID, "axes.linewidth": 0.8,
})

# ---------------------------------------------------------------- figure 1
# h5/h1 of the amplitude-envelope spectrum, per quarter-clip. Speed-invariant.
tracks = [
    ("Getty 104161830", [0.443, 0.474, 0.624, 0.503], ORANGE, "stock clip"),
    ("2011 ZB788",      [0.180, 0.150, 0.138, 0.114], BLUE, "Skinny Bob"),
    ("2011 RsQCX",      [0.157, 0.116, 0.082],        BLUE, "Skinny Bob"),
    ("2026 v1",         [0.151, 0.149],               BLUE, "Skinny Bob"),
    ("2026 v2",         [0.101, 0.112, 0.138, 0.120], BLUE, "Skinny Bob"),
]
fig, ax = plt.subplots(figsize=(7.6, 3.0))
seen = set()
for i, (name, vals, c, grp) in enumerate(tracks):
    y = len(tracks) - 1 - i
    lbl = grp if grp not in seen else None
    seen.add(grp)
    ax.scatter(vals, [y] * len(vals), s=58, color=c, zorder=3,
               edgecolors=SURFACE, linewidths=1.6, label=lbl)
ax.axvspan(0.08, 0.18, color=BLUE, alpha=0.07, zorder=0)
ax.axvspan(0.44, 0.63, color=ORANGE, alpha=0.07, zorder=0)
ax.set_yticks(range(len(tracks)))
ax.set_yticklabels([t[0] for t in tracks][::-1])
ax.set_xlim(0, 0.70)
ax.set_xlabel("h5 / h1 of the amplitude-envelope spectrum  (speed-invariant)")
ax.set_title("Projector-tick shape: stock clip and Skinny Bob tracks do not overlap",
             color=INK, fontsize=11, pad=10, loc="left")
ax.grid(axis="x", color=GRID, linewidth=0.7, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.text(0.13, 3.62, "Skinny Bob band 0.08–0.18", color=BLUE, fontsize=8.5, ha="center")
ax.text(0.535, 3.62, "Getty 0.44–0.62", color=ORANGE, fontsize=8.5, ha="center")
ax.legend(frameon=False, loc="lower right", fontsize=9, labelcolor=INK2)
fig.tight_layout()
fig.savefig("analysis/prior-work/sheets/fig_tick_h5.png", dpi=170)
print("wrote fig_tick_h5.png")

# ---------------------------------------------------------------- figure 2
# Vignette depth, one number per video: luma at r=0.85 divided by luma at frame centre.
# 1.0 = flat (no vignette); lower = deeper corners.
vig = [
    ("2011 a6TL",  0.953, ORANGE, "static-text video"),
    ("2011 Xju",   0.828, ORANGE, "static-text video"),
    ("2026 v2",    0.626, BLUE,   ""),
    ("2011 ZB788", 0.604, ORANGE, ""),
    ("2026 v1",    0.595, BLUE,   ""),
    ("2026 v3",    0.515, BLUE,   ""),
    ("2011 RsQCX", 0.503, ORANGE, ""),
]
fig, ax = plt.subplots(figsize=(7.6, 3.5))
seen = set()
for i, (name, v, c, note) in enumerate(vig):
    y = len(vig) - 1 - i
    era = "2026 (qtecqot)" if name.startswith("2026") else "2011 (ivan0135)"
    lbl = era if era not in seen else None
    seen.add(era)
    ax.hlines(y, v, 1.0, color=c, linewidth=2.0, alpha=0.45, zorder=2)
    ax.scatter([v], [y], s=64, color=c, zorder=3, edgecolors=SURFACE,
               linewidths=1.6, label=lbl)
    ax.text(v - 0.012, y, f"{v:.3f}", va="center", ha="right",
            fontsize=9, color=INK2)
    if note:
        ax.text(1.015, y, note, va="center", ha="left", fontsize=8.5, color=INK2)
ax.axvline(1.0, color=GRID, linewidth=1.0, zorder=1)
ax.set_yticks(range(len(vig)))
ax.set_yticklabels([t[0] for t in vig][::-1])
ax.set_xlim(0.36, 1.26)
ax.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax.set_xlabel("edge luma \u00f7 centre luma   (1.0 = flat, lower = deeper vignette)")
ax.set_title("Vignette depth is comparable across eras", color=INK,
             fontsize=11, pad=10, loc="left")
ax.grid(axis="x", color=GRID, linewidth=0.7, zorder=0)
ax.set_axisbelow(True)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.legend(frameon=False, fontsize=9, labelcolor=INK2, ncol=2,
          loc="upper center", bbox_to_anchor=(0.5, -0.28))
fig.tight_layout()
fig.savefig("analysis/prior-work/sheets/fig_vignette.png", dpi=170)
print("wrote fig_vignette.png")
