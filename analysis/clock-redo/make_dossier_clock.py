#!/usr/bin/env python3.12
"""Rebuild figs/qtecqot/clock.png against all 19 posts.

The script that made the original does not exist. `figs/qtecqot/clock.png` arrived in
the initial commit and nothing in the repo generates it, which is the `analysis/README.md`
caveat in action. This is a reconstruction of that figure's design, not a recovery of its
code, and the data underneath it has changed:

  2026 half  was 7 machine-read acts (3 uploads, 2 registrations, 2 posts).
             Now 19 X posts and nothing else. Uploads and registrations are dropped
             because uploads can be scheduled, which is what made the old panel
             mix schedulable with non-schedulable acts. See clock19c.py.
  2011 half  unchanged, 5 acts. Reproduced here from archive/ivan/*.info.json rather
             than copied from the dossier table, and it lands on the same US Pacific
             17:35-22:21 span the dossier reported, which is the check that the
             reconstruction is faithful.

The visible difference is the point: the old 2026 panel carried a green "best fit" box
on Central European. There is no best fit any more. Under all 19 posts every one of the
four candidate zones puts posts in the local small hours.

The original is kept at figs/qtecqot/withdrawn/clock_7acts_2026-07-29_WITHDRAWN.png.

Run from the repo root: python3.12 analysis/clock-redo/make_dossier_clock.py
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from datetime import datetime, timedelta

OUT = "figs/qtecqot/clock.png"

FG, DIM, GRID = "#1a1a1a", "#666666", "#e8eaf2"
BLUE, BLUE_L = "#2f6fc4", "#a9c4e8"
RED,  RED_L = "#c0392b", "#e8b3ad"
WARN = "#c0392b"


def U(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")


# 19 X posts. Authored, non-schedulable. Same list as clock19c.py.
Q2026 = [U(s) for s in """
2026-04-28T05:54:16 2026-05-07T06:17:03 2026-05-25T09:46:14 2026-05-25T09:50:36
2026-06-14T13:20:43 2026-06-14T13:23:30 2026-06-14T13:32:03 2026-06-15T04:53:33
2026-06-15T04:54:05 2026-07-28T07:18:28 2026-07-29T08:18:46 2026-07-31T07:21:01
2026-07-31T10:15:58 2026-07-31T10:18:24 2026-07-31T22:33:22 2026-08-01T02:09:43
2026-08-01T03:37:11 2026-08-01T03:45:49 2026-08-02T03:24:49""".split()]

# 5 ivan0135 acts. Channel creation from YouTube's RSS feed (docs/SKINNY_BOB_DOSSIER.md
# section F); the four uploads decoded from the `timestamp` field of the archived
# info.json for each video, not retyped from the dossier table.
I2011 = [U(s) for s in """
2011-04-14T01:08:36 2011-04-14T02:04:26 2011-05-02T05:21:51
2011-05-09T05:09:51 2011-05-18T00:35:43""".split()]

# 2011 used UTC+4 for Moscow (permanent DST that year), 2026 uses +3.
ZONES_2026 = [("Central European", "CEST, UTC+2", 2), ("Moscow", "UTC+3", 3),
              ("US Eastern", "EDT, UTC−4", -4), ("US Pacific", "PDT, UTC−7", -7)]
ZONES_2011 = [("Central European", "CEST, UTC+2", 2), ("Moscow", "2011: UTC+4", 4),
              ("US Eastern", "EDT, UTC−4", -4), ("US Pacific", "PDT, UTC−7", -7)]

# The original figure shaded 23:00-07:00. Everything in the correction uses a
# 07:00-24:00 waking band instead (clock19c.py, 3_clock.png, and the withdrawal note in
# the dossier), so the small hours are 00:00-07:00 here. Keeping the old 23:00 edge would
# have printed US Eastern 14 and US Pacific 11 against the 11 and 10 reported everywhere
# else, which is two numbers for one measurement. clock19b.py scans three bands and the
# answer is stable across them, so the choice does not change the conclusion.
NIGHT_LO, NIGHT_HI = 24.0, 7.0


def local_hours(acts, off):
    return sorted(((a + timedelta(hours=off)).hour
                   + (a + timedelta(hours=off)).minute / 60) for a in acts)


def in_night(h):
    return h < NIGHT_HI or h >= NIGHT_LO


def panel(ax, acts, zones, dot, line, show_span):
    """One block of zone rows. Returns the per-zone violation counts."""
    ax.set_xlim(-0.4, 24.4)
    ax.set_ylim(len(zones) - 0.4, -0.75)
    ax.set_yticks([])
    ax.set_xticks(range(0, 25, 3))
    ax.set_xticklabels([f"{h:02d}" for h in range(0, 25, 3)], fontsize=10.5, color=DIM)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#cccccc")
    ax.tick_params(length=0)

    viols = []
    for i, (name, sub, off) in enumerate(zones):
        hrs = local_hours(acts, off)
        v = sum(1 for h in hrs if in_night(h))
        viols.append(v)
        # the row bed, with the small hours shaded
        ax.add_patch(Rectangle((0, i - 0.30), 24, 0.60, fc="#f4f5f9", ec="none", zorder=1))
        ax.add_patch(Rectangle((0, i - 0.30), NIGHT_HI, 0.60, fc=GRID, ec="none", zorder=1))
        ax.add_patch(Rectangle((NIGHT_LO, i - 0.30), 24 - NIGHT_LO, 0.60,
                               fc=GRID, ec="none", zorder=1))
        if len(hrs) > 1:
            ax.plot([hrs[0], hrs[-1]], [i, i], color=line, lw=2.4, zorder=2,
                    solid_capstyle="round")
        for h in hrs:
            ax.plot([h], [i], "o", ms=7.5, color=dot, mec="white", mew=.9, zorder=3)

        ax.text(-0.9, i - 0.10, name, fontsize=11.5, color=FG, ha="right", va="center")
        ax.text(-0.9, i + 0.19, f"({sub})", fontsize=9.5, color=DIM, ha="right", va="center")
        # count of acts landing in the shaded band. This is the number the old figure
        # never showed, and the reason its best-fit box was wrong.
        lab = "none in the small hours" if v == 0 else \
              f"{v} of {len(hrs)} in the small hours"
        ax.text(24.9, i, lab, fontsize=10.5, va="center",
                color=(DIM if v == 0 else WARN), weight=("normal" if v == 0 else "bold"))
        if show_span and v == 0:
            ax.add_patch(Rectangle((-0.25, i - 0.42), 24.5, 0.84, fc="none",
                                   ec="#1a7f5a", lw=1.6, zorder=4))
    # In axes fraction, not data. At data y it landed on top of the last row's
    # "(PDT, UTC-7)" sub-label.
    ax.text(-0.012, -0.115, "local hour", transform=ax.transAxes, fontsize=9.5,
            color=DIM, ha="right", va="center", family="DejaVu Sans Mono")
    return viols


fig = plt.figure(figsize=(13.2, 9.2), dpi=140, facecolor="white")
fig.text(.045, .965, "The clock: every authored act against four candidate time zones",
         fontsize=19, weight="bold", color=FG, va="top")
fig.text(.045, .930, "Nothing here is a geolocation. It is a working-hours pattern, "
                     "and shaded means midnight to 07:00 local.",
         fontsize=11.5, color=DIM, va="top")

ax1 = fig.add_axes([.175, .585, .55, .265])
fig.text(.045, .895, "qtecqot, 2026 — all 19 X posts", fontsize=14.5,
         weight="bold", color=FG, va="top")
fig.text(.045, .873, "Uploads and registrations are excluded because uploads can be "
                     "scheduled. Posts cannot.", fontsize=10.5, color=DIM, va="top")
v26 = panel(ax1, Q2026, ZONES_2026, BLUE, BLUE_L, show_span=True)

ax2 = fig.add_axes([.175, .185, .55, .265])
fig.text(.045, .490, "ivan0135, 2011 — five machine-read acts", fontsize=14.5,
         weight="bold", color=FG, va="top")
fig.text(.045, .468, "Four uploads plus the channel creation, in the same four zones.",
         fontsize=10.5, color=DIM, va="top")
v11 = panel(ax2, I2011, ZONES_2011, RED, RED_L, show_span=True)

# The withdrawal notice belongs on the figure, because figures travel without their captions.
fig.text(.045, .095,
         "Supersedes the 7-act version of 2026-07-29, which showed a clean Central "
         "European morning band and a green best-fit box on it.\n"
         "The recovery of 11 deleted posts took the 2026 count from 7 to 19 and that "
         "reading did not survive. None of the four zones is clean now.\n"
         "The only offsets where no post lands in the small hours run from UTC+8.5 to "
         "+10. A zero is a gap in the data, not an address.",
         fontsize=10, color=DIM, va="top", linespacing=1.65)

fig.savefig(OUT, facecolor="white")
plt.close(fig)

print(f"wrote {OUT}")
print(f"  2026, n=19: " + ", ".join(f"{z[0]} {v}" for z, v in zip(ZONES_2026, v26)))
print(f"  2011, n=5 : " + ", ".join(f"{z[0]} {v}" for z, v in zip(ZONES_2011, v11)))
