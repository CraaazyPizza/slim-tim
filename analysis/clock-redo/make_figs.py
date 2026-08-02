#!/usr/bin/env python3.12
"""Carousel figures for the 2026-08-02 recovery.

Square 1080x1080, because Reddit's gallery crops to square in the feed preview and
anything wider loses its edges. One accent colour (red = deleted), everything else white
or grey. No footers, no legend boxes, no callout borders, no emoji.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime, timedelta

OUT = "figs/qtecqot-2026-08-02/"
BG, FG, DIM, ACC = "#111111", "#f2f2f2", "#7d7d7d", "#e5484d"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "text.color": FG,
    "axes.labelcolor": FG, "xtick.color": DIM, "ytick.color": DIM,
    "axes.edgecolor": DIM, "font.family": "DejaVu Sans", "font.size": 13,
    "xtick.major.size": 0, "ytick.major.size": 0,
})
SQ = dict(figsize=(7.2, 7.2), dpi=150)


def U(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")


POSTS = [("2026-04-28T05:54:16", 0), ("2026-05-07T06:17:03", 0), ("2026-05-25T09:46:14", 0),
         ("2026-05-25T09:50:36", 0), ("2026-06-14T13:20:43", 0), ("2026-06-14T13:23:30", 0),
         ("2026-06-14T13:32:03", 0), ("2026-06-15T04:53:33", 0), ("2026-06-15T04:54:05", 0),
         ("2026-07-28T07:18:28", 1), ("2026-07-29T08:18:46", 1), ("2026-07-31T07:21:01", 0),
         ("2026-07-31T10:15:58", 0), ("2026-07-31T10:18:24", 1), ("2026-07-31T22:33:22", 1),
         ("2026-08-01T02:09:43", 1), ("2026-08-01T03:37:11", 1), ("2026-08-01T03:45:49", 1),
         ("2026-08-02T03:24:49", 1)]
VID = [("2026-05-25T09:39:42", "video 5 of 8"), ("2026-06-15T04:23:35", "video 6 of 8"),
       ("2026-07-24T09:14:05", "video 7 of 8")]


# ------------------------------------------------------------------ 1. the ledger
# A linear date axis wastes half the square on an empty July and then jams ten posts
# into the last week. An evenly spaced ledger keeps the order, prints the real dates,
# and makes "11 of 19" countable at a glance.
EVENTS = [
    ("28 Apr  05:54", "post", 0, "First post ever, names Project SERPO"),
    ("07 May  06:17", "post", 0, "Names Valerijs \u010cernohajev, with a photo"),
    ("25 May  09:39", "vid",  0, "Video 5 of 8 goes live"),
    ("25 May  09:46", "post", 0, "Upload No.1 complete"),
    ("25 May  09:50", "post", 0, "Reworded, and the first three are gone"),
    ("14 Jun  13:20", "post", 0, ""),
    ("14 Jun  13:23", "post", 0, ""),
    ("14 Jun  13:32", "post", 0, ""),
    ("15 Jun  04:23", "vid",  0, "Video 6 of 8 goes live"),
    ("15 Jun  04:53", "post", 0, ""),
    ("15 Jun  04:54", "post", 0, ""),
    ("24 Jul  09:14", "vid",  0, "Video 7 of 8 goes live"),
    ("28 Jul  07:18", "post", 1, "I am not Ivan0135"),
    ("29 Jul  08:18", "post", 1, "DMS = Deadman's Switch"),
    ("31 Jul  07:21", "post", 0, ""),
    ("31 Jul  10:15", "post", 0, ""),
    ("31 Jul  10:18", "post", 1, "Two AI-detector screenshots"),
    ("31 Jul  22:33", "post", 1, ""),
    ("01 Aug  02:09", "post", 1, ""),
    ("01 Aug  03:37", "post", 1, "Less than 2% of the cache"),
    ("01 Aug  03:45", "post", 1, ""),
    ("02 Aug  03:24", "post", 1, "Case 28 belongs to tape 5"),
]
fig, ax = plt.subplots(**SQ)
ax.axis("off")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
y, dy = .885, .0395
for ts, kind, live, note in EVENTS:
    if kind == "vid":
        ax.plot([0, 1], [y + .019, y + .019], color=DIM, lw=.7, ls=(0, (3, 3)))
        ax.text(.115, y, note, fontsize=12.5, color=DIM, va="center")
    else:
        c = FG if live else ACC
        ax.text(0, y, ts, fontsize=12, color=DIM, va="center", family="DejaVu Sans Mono")
        ax.plot([.245], [y], marker="s", ms=7.5, color=c)
        if note:
            ax.text(.295, y, note, fontsize=12.5, color=c, va="center")
    y -= dy
ax.text(0, .960, "He deleted 11 of his 19 posts", fontsize=27, weight="bold", va="baseline")
ax.text(0, .925, "@qtecqot on X. Red is deleted, white is still up.",
        fontsize=13.5, color=DIM, va="baseline")
fig.tight_layout(rect=[.05, .02, .97, .99])
fig.savefig(OUT + "1_deletions.png")
plt.close(fig)


# ------------------------------------------------------------------ 2. the counters
# Same construction as slide 1: everything placed by hand in axes coordinates. set_title
# plus tight_layout(rect=...) fought each other here and clipped the heading.
fig, ax = plt.subplots(**SQ)
ax.axis("off")
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.text(0, .945, "He wiped the thread 11 minutes", fontsize=26, weight="bold", va="baseline")
ax.text(0, .888, "after the first video went up", fontsize=26, weight="bold", va="baseline")
ax.text(0, .838, "The numbers X showed on his profile at each post",
        fontsize=13.5, color=DIM, va="baseline")
CX = {"Posts": .50, "Media": .655, "Follows": .82}
for k, x in CX.items():
    ax.text(x, .745, k, fontsize=13, color=DIM, ha="center", va="baseline")
ax.plot([0, .90], [.725, .725], color=DIM, lw=.8)
ROWS = [("28 Apr  05:54", "1", "0", "2", False),
        ("07 May  06:17", "2", "1", "4", False),
        ("25 May  09:46", "3", "1", "3", False),
        ("25 May  09:50", "1", "0", "3", True)]
y = .665
for ts, p_, m_, f_, hot in ROWS:
    ax.text(0, y, ts, fontsize=14.5, color=FG, va="center", family="DejaVu Sans Mono")
    for val, k in ((p_, "Posts"), (m_, "Media"), (f_, "Follows")):
        red = hot and k in ("Posts", "Media")
        ax.text(CX[k], y, val, fontsize=16, ha="center", va="center",
                color=(ACC if red else FG), weight=("bold" if red else "normal"))
    y -= .058
ax.plot([0, .90], [y + .022, y + .022], color=DIM, lw=.8)
ax.text(0, .365, "Video 5 of 8 went live at 09:39:42.", fontsize=16, va="baseline")
ax.text(0, .300, "He announced it at 09:46:14.", fontsize=16, va="baseline")
ax.text(0, .235, "By 09:50:36 he was back to 1 post and 0 media.", fontsize=16, va="baseline")
ax.text(0, .155, "The first three posts were gone, and so was a follow.",
        fontsize=16, va="baseline")
fig.tight_layout(rect=[.05, .02, .97, .99])
fig.savefig(OUT + "2_counters.png")
plt.close(fig)


# ------------------------------------------------------------------ 3. the clock
# Per-bar annotations collided with each other and with the bars at -4/-3.5 and +2/+3.
# The readings go in a block in the empty upper right instead, where nothing can clash.
X = [U(s) for s, _ in POSTS]
offs = np.arange(-12, 12.5, .5)
viol = [sum(1 for a in X if not (7.0 <= ((a + timedelta(hours=o)).hour
        + (a + timedelta(hours=o)).minute / 60) < 24.0)) for o in offs]
fig, ax = plt.subplots(**SQ)
ax.bar(offs, viol, width=.40, color=ACC, zorder=3)
READ = [("US Eastern", -4), ("US Pacific", -7), ("CEST", 2), ("Moscow", 3),
        ("UTC+8.5 to +10", 9)]
y = 16.4
for lab, o in READ:
    n = viol[int(round((o + 12) * 2))]
    ax.text(3.6, y, lab, fontsize=14, color=FG, va="center", ha="left")
    ax.text(12.9, y, str(n), fontsize=14, color=(FG if n == 0 else ACC), va="center",
            ha="right", weight="bold")
    y -= 1.45
ax.set_ylim(0, 18)
ax.set_xlim(-13.2, 13.6)
ax.set_xticks([-12, -8, -4, 0, 4, 8, 12])
ax.set_xticklabels(["-12", "-8", "-4", "UTC", "+4", "+8", "+12"])
ax.set_yticks([0, 5, 10])
ax.tick_params(labelsize=12.5)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.spines["left"].set_color(DIM)
ax.spines["bottom"].set_color(DIM)
ax.set_ylabel("Of his 19 posts, how many land in local 00:00 to 07:00",
              fontsize=13, color=DIM, labelpad=12)
ax.set_xlabel("UTC offset applied to every post", fontsize=13, color=DIM, labelpad=10)
# 28pt clipped the last word off the square. This heading is 31 characters and 23 is what fits.
ax.set_title("The clock stopped naming a zone", fontsize=23, weight="bold", loc="left", pad=32)
ax.text(0, 1.020, "Each of the 19 posts, read as a local time under every offset",
        transform=ax.transAxes, fontsize=13.5, color=DIM)
# The 0 in the readings block reads as "so he is at UTC+9" unless this says otherwise.
# It is the one number a viewer will take away, so the caveat goes next to it, not in a caption.
ax.text(3.6, 9.4, "A zero is a gap, not an address.", fontsize=12.5, color=DIM, va="center")
ax.text(3.6, 8.4, "One late night rules a zone out.", fontsize=12.5, color=DIM, va="center")
fig.tight_layout(rect=[.02, .02, .98, .95])
fig.savefig(OUT + "3_clock.png")
plt.close(fig)

print("wrote 3 square figures to", OUT)
