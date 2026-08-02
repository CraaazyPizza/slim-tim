#!/usr/bin/env python3.12
"""Rebuild figs/qtecqot/counter.png.

The original said of slot 8 only "not yet — the finale, unreleased as of 2026-07-29".
On 2026-08-02 he described its contents unprompted, replying on X:

    "I can confirm that the next release will contain content from Tape 7 and will be
     in color. Some may find it slightly more disturbing than previous footage."
    -- 2083903785219551469, 13:12:34 UTC

and seven minutes earlier gave the numbering the whole counter sits inside:

    "They advance sequentially across 7 tapes, beginning at tape 01, case 01 and ending
     at tape 07, case 40. Of note is a minor indexing error in 2011."
    -- 2083902015831511168, 13:05:32 UTC

So slot 8 stops being blank. It now carries a claim he made before the thing that would
test it, which is the only reason it is worth drawing: tape 7 and colour are both
falsifiable on release, and `agent_colour_duplicate_count.md` already has the measurement
to run against a colour release the day it lands.

No script made the original. Like make_dossier_clock.py this is a reconstruction of its
design from the image. The original is kept under figs/qtecqot/withdrawn/.

Run from anywhere: python3.12 analysis/dossier-figs/make_counter.py
"""
import os
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from acts import ROOT  # noqa: E402

OUT = os.path.join(ROOT, "figs/qtecqot/counter.png")

FG, DIM = "#1a1a1a", "#6b6b6b"
BROWN, RED, GREY = "#8a6244", "#c0392b", "#9a9a9a"
GREEN, GREENBG = "#1a7f5a", "#f0f7f4"

SLOTS = [
    (1, BROWN, "2011-04-14", "ZB788PtqQvg", "tape 01 material"),
    (2, BROWN, "2011-05-02", "RsQCXN4o4Ps", "the “skinny bob” video"),
    (3, BROWN, "2011-05-09", "Xju_CY5ZESA", "text-only reply video"),
    (4, BROWN, "2011-05-18", "a6TLGkrfNKI", "“tape 06 — family vacation”"),
    (5, RED,   "2026-05-25", "OpSTlDJWFFI", "tapes 02, 05, 06 — no number on the card"),
    (6, RED,   "2026-06-15", "Oqw96jCOP7A", "“Continuation release 6 / 8”"),
    (7, RED,   "2026-07-24", "l9RAhmPHM_A", "“Continuation release 7 / 8”"),
    (8, GREY,  "not yet",    "—",       "he says tape 7, and in colour"),
]

fig = plt.figure(figsize=(15.2, 8.2), dpi=140, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)

ax.text(.048, .955, "The “N of 8” counter, decoded", fontsize=25, weight="bold",
        color=FG, va="top")
ax.text(.048, .905, "His own numbering treats ivan0135's 2011 uploads as releases 1–4 "
                    "of the same series.", fontsize=13, color=DIM, va="top")

# era brackets
ax.plot([.048, .468], [.815, .815], color=BROWN, lw=2)
ax.text(.048, .838, "ivan0135, 2011  —  four uploads in 34 days, then silence", fontsize=13.5, weight="bold", color=BROWN, va="baseline")
ax.plot([.492, .806], [.815, .815], color=RED, lw=2)
ax.text(.492, .838, "qtecqot, 2026  —  three uploads in nine weeks", fontsize=13.5,
        weight="bold", color=RED, va="baseline")
ax.text(.828, .838, "announced", fontsize=13.5, weight="bold", color=GREY,
        va="baseline")

X0, W, GAP = .048, .096, .0175
BOX_TOP, BOX_H = .785, .175
for i, (n, colour, date, vid, note) in enumerate(SLOTS):
    x = X0 + i * (W + GAP)
    pending = (n == 8)
    ax.add_patch(FancyBboxPatch((x, BOX_TOP - BOX_H), W, BOX_H,
                                boxstyle="round,pad=0,rounding_size=.012",
                                fc=("white" if pending else colour),
                                ec=(GREY if pending else "none"),
                                ls=("--" if pending else "-"), lw=1.6, zorder=2))
    ax.text(x + W / 2, BOX_TOP - BOX_H * .40, str(n), fontsize=34, weight="bold",
            color=(GREY if pending else "white"), ha="center", va="center", zorder=3)
    ax.text(x + W / 2, BOX_TOP - BOX_H * .80, "of 8", fontsize=12,
            color=(GREY if pending else "#f0e6e0"), ha="center", va="center", zorder=3)
    ax.text(x + W / 2, .578, date, fontsize=11.5, weight="bold", color=FG, ha="center")
    ax.text(x + W / 2, .548, vid, fontsize=10.5, color=DIM, ha="center",
            family="DejaVu Sans Mono")
    # Hand-placed line breaks collided with the neighbouring column at three
    # slots. Wrap to the box width instead.
    ax.text(x + W / 2, .512, textwrap.fill(note, 20), fontsize=10, color=DIM,
            ha="center", va="top", linespacing=1.5)

# the "5 of 8 completed" anchor, unchanged from the original reading
ax.plot([X0 + 4 * (W + GAP) + W / 2] * 2, [.450, .345], color=GREEN, lw=1.4,
        ls=(0, (4, 4)), zorder=1)
ax.add_patch(FancyBboxPatch((.115, .215), .77, .115,
                            boxstyle="round,pad=0,rounding_size=.012",
                            fc=GREENBG, ec=GREEN, lw=1.4, zorder=2))
ax.text(.138, .295, "“5 of 8 completed.”   — written in a YouTube comment "
                    "two to four days after video 1 went up,", fontsize=13, color=FG,
        va="center", zorder=3)
ax.text(.138, .253, "when exactly one qtecqot video existed.  4 (ivan, 2011) + 1 (video 1) "
                    "= 5.  That fixes the counter, and makes slot 8 the last one.",
        fontsize=12, color=FG, va="center", zorder=3)

# what he has since said about slot 8
ax.add_patch(Rectangle((.115, .045), .77, .135, fc="#fafafa", ec="#e0e0e0", lw=1, zorder=2))
ax.text(.138, .150, "What he has since said about slot 8, unprompted, on 2026-08-02:",
        fontsize=12, weight="bold", color=FG, va="center", zorder=3)
ax.text(.138, .110, "“the next release will contain content from Tape 7 and will be "
                    "in color. Some may find it slightly more disturbing.”",
        fontsize=12, color=FG, va="center", style="italic", zorder=3)
ax.text(.138, .073, "Registered before release, so it is falsifiable. Tape 07 has never "
                    "been shown by either era, and the colour notation is a 2026 invention "
                    "with no 2011 precedent.",
        fontsize=10.5, color=DIM, va="center", zorder=3)

fig.savefig(OUT, facecolor="white")
plt.close(fig)
print("wrote", OUT)
