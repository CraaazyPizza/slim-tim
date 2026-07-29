import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BLUE = "#2a78d6"
ORANGE = "#eb6834"
GRAY_TEXT = "#52514e"
GRAY_GRID = "#d8d6d0"
GRAY_LIGHT = "#f0efec"
INK = "#0b0b0b"
VIOLET = "#4a3aa7"

fig = plt.figure(figsize=(11, 5.6))
fig.patch.set_facecolor("#fcfcfb")

# ---------- Left: stat tile ("who is this account") ----------
ax0 = fig.add_axes([0.03, 0.10, 0.24, 0.72])
ax0.set_facecolor("#fcfcfb")
ax0.axis("off")
ax0.set_title("Account @m21-b5q\n(“M21”)", fontsize=13, fontweight="bold", color=INK, loc="left", pad=6)

stats = [
    ("Created", "2015-10-02", "RSS feed, second-precision"),
    ("Subscribers", "3", "yt-dlp, 2026-07-29"),
    ("Uploads", "0", "no videos tab exists"),
    ("Comments found", "9", "across all 7 videos, full corpus"),
    ("Videos commented on", "2 of 7", "RsQ (2011) + both 2026\ncontinuation videos so far"),
    ("Silent on", "video 3", "uploaded 2026-07-24,\nno comment as of capture"),
]
y0 = 0.90
for label, val, note in stats:
    ax0.text(0.0, y0, label, fontsize=9.5, color=GRAY_TEXT, transform=ax0.transAxes, va="top")
    ax0.text(1.0, y0, val, fontsize=13, color=BLUE, fontweight="bold", ha="right",
             transform=ax0.transAxes, va="top")
    y0 -= 0.075
    ax0.text(0.0, y0, note, fontsize=7.6, color="#8a8880", transform=ax0.transAxes, va="top", style="italic")
    y0 -= 0.10

ax0.plot([0, 1], [y0 + 0.03, y0 + 0.03], color=GRAY_GRID, lw=0.8, transform=ax0.transAxes)
ax0.text(0.0, y0 - 0.02, "An 11-year-old lurker profile — not a\nfreshly created sock puppet.",
         fontsize=8.6, color=INK, transform=ax0.transAxes, va="top", fontweight="bold")

# ---------- Right: 2026 event timeline ----------
ax1 = fig.add_axes([0.34, 0.14, 0.63, 0.68])
ax1.set_facecolor("#fcfcfb")

t0 = datetime.date(2026, 4, 15)
t1 = datetime.date(2026, 7, 30)


def to_x(d):
    return (d - t0).days

ax1.set_xlim(0, to_x(t1))
ax1.set_ylim(-2.15, 1.9)
ax1.axhline(0, color=GRAY_GRID, lw=1.4, zorder=1)
ax1.axis("off")

# month ticks
months = [datetime.date(2026, m, 1) for m in range(4, 8)] + [datetime.date(2026, 7, 29)]
for md in [datetime.date(2026, m, 1) for m in range(5, 8)]:
    x = to_x(md)
    ax1.text(x, -1.5, md.strftime("%b"), fontsize=8.5, color=GRAY_TEXT, ha="center")
    ax1.plot([x, x], [-0.08, 0.08], color=GRAY_GRID, lw=1, zorder=1)

events = [
    (datetime.date(2026, 4, 22), "qtecqot channel\ncreated", 1, BLUE, "point"),
    (datetime.date(2026, 5, 25), "Video 1 uploaded", 1, BLUE, "point"),
    (datetime.date(2026, 5, 26), datetime.date(2026, 5, 29), "m21-b5q's plea\n(root comment,\nRsQ thread)", -1, ORANGE, "band"),
    (datetime.date(2026, 5, 27), datetime.date(2026, 5, 29), "qtecqot's ONLY\nreply anywhere —\nto this plea", 1.55, VIOLET, "band2"),
    (datetime.date(2026, 6, 15), "Video 2 uploaded", 1, BLUE, "point"),
    (datetime.date(2026, 7, 1), datetime.date(2026, 7, 6), "long reply cross-posted to\nboth continuation videos +\nthank-you on RsQ (edited)", -1, ORANGE, "band"),
    (datetime.date(2026, 7, 8), datetime.date(2026, 7, 13), "reply re: finger count\n(“can't see 5 fingers”)", -1.85, ORANGE, "band2"),
    (datetime.date(2026, 7, 24), "Video 3 uploaded —\nm21-b5q silent", 1, "#8a8880", "point"),
]

for ev in events:
    if ev[-1] == "point":
        d, label, yoff, color, _ = ev
        x = to_x(d)
        ax1.plot([x], [0], "o", color=color, markersize=7, zorder=5, markeredgecolor="white", markeredgewidth=1)
        ax1.plot([x, x], [0, yoff * 0.55], color=color, lw=1.2, zorder=3)
        va = "bottom" if yoff > 0 else "top"
        ax1.text(x, yoff * 0.62, label, fontsize=8.3, color=INK, ha="center", va=va)
    else:
        d0, d1_, label, yoff, color, kind = ev
        x0, x1_ = to_x(d0), to_x(d1_)
        xm = (x0 + x1_) / 2
        height = 0.30
        rect_y = 0 if yoff > 0 else -height
        # draw band directly on the spine region
        band_bottom = min(0, yoff * 0.42)
        band_top = max(0, yoff * 0.42) if False else None
        ax1.add_patch(mpatches.Rectangle((x0, -0.09), x1_ - x0, 0.18, color=color, alpha=0.85, zorder=4, lw=0))
        ax1.plot([xm, xm], [0, yoff * 0.55], color=color, lw=1.2, zorder=3, alpha=0.9)
        va = "bottom" if yoff > 0 else "top"
        ax1.text(xm, yoff * 0.62, label, fontsize=8.0, color=INK, ha="center", va=va)

ax1.set_title("What m21-b5q actually did, April–July 2026", fontsize=13, fontweight="bold",
              color=INK, loc="left", pad=14)
ax1.text(to_x(datetime.date(2026, 7, 29)), -1.45, "capture\n07-29", fontsize=7.2, color="#8a8880", ha="center")
ax1.plot([to_x(datetime.date(2026, 7, 29))] * 2, [-0.06, 0.06], color="#8a8880", lw=1)

fig.text(0.34, 0.045,
         "Orange bands = date windows bracketed from two yt-dlp comment captures taken 3 days apart\n"
         "(TIMELINE.md §row 5 method) — not exact dates. All other markers are second-precision.",
         fontsize=7.6, color=GRAY_TEXT, ha="left")

fig.suptitle("@m21-b5q — account profile and 2026 timeline", fontsize=14.5, fontweight="bold",
             color=INK, x=0.03, ha="left", y=0.985)

plt.savefig("/home/user/new-skinny-bob/figs/people/m21_timeline.png", dpi=200, facecolor="#fcfcfb")
print("saved")
