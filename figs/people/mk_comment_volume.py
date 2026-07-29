import json, glob, datetime
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

BLUE = "#2a78d6"
ORANGE = "#eb6834"
GRAY_TEXT = "#52514e"
GRAY_GRID = "#d8d6d0"
INK = "#0b0b0b"

all_comments = []
for f in sorted(glob.glob('/home/user/new-skinny-bob/comments/capture_2026-07-29/*.info.json')):
    d = json.load(open(f))
    for c in d.get('comments', []):
        all_comments.append(c)

# Panel A: per-year totals 2011-2024 (year-level relative strings are reliable to the year)
year_counts = Counter()
for c in all_comments:
    ts = c.get('timestamp')
    if ts is None:
        continue
    dt = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
    year_counts[dt.year] += 1

years_a = list(range(2011, 2025))
vals_a = [year_counts.get(y, 0) for y in years_a]

# Panel B: per-month Aug 2025 - Jul 2026, using ONLY comments whose relative string
# is month-or-finer (day/hour/minute) -- excluding "N years ago" strings, which all
# collapse onto the scrape month (2026-07) and would fake a spike there.
month_counts = Counter()
for c in all_comments:
    ts = c.get('timestamp')
    tt = c.get('_time_text') or ''
    if ts is None or 'year' in tt:
        continue
    dt = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
    if (dt.year, dt.month) >= (2025, 8):
        month_counts[(dt.year, dt.month)] += 1

months_b = [(2025, m) for m in range(8, 13)] + [(2026, m) for m in range(1, 8)]
vals_b = [month_counts.get(k, 0) for k in months_b]
month_labels = [datetime.date(y, m, 1).strftime("%b\n%Y") if m == 1 else datetime.date(y, m, 1).strftime("%b")
                for (y, m) in months_b]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3), gridspec_kw={"width_ratios": [1.25, 1]})
fig.patch.set_facecolor("#fcfcfb")

# --- Panel A ---
ax1.set_facecolor("#fcfcfb")
bars = ax1.bar(years_a, vals_a, color=BLUE, width=0.68, zorder=3)
ax1.set_yscale("log")
ax1.set_ylim(20, 1600)
ax1.set_title("Comments per year, 2011–2024", fontsize=12, color=INK, fontweight="bold", loc="left", pad=10)
ax1.set_xticks(years_a)
ax1.set_xticklabels([str(y)[2:] for y in years_a], fontsize=8.5, color=GRAY_TEXT)
ax1.tick_params(axis="y", labelsize=8.5, colors=GRAY_TEXT)
for spine in ["top", "right", "left"]:
    ax1.spines[spine].set_visible(False)
ax1.spines["bottom"].set_color(GRAY_GRID)
ax1.grid(axis="y", color=GRAY_GRID, linewidth=0.7, zorder=0)
ax1.set_axisbelow(True)
ax1.annotate("video 1 uploaded,\nMay 2011", xy=(2011, vals_a[0]), xytext=(2011.3, 900),
             fontsize=8, color=GRAY_TEXT, ha="left",
             arrowprops=dict(arrowstyle="-", color=GRAY_TEXT, lw=0.7))
# find local peak ~2022
peak_y = years_a[vals_a.index(max(vals_a[8:]))] if len(vals_a) > 8 else years_a[-1]
ax1.annotate("periodic\nresurfacing", xy=(peak_y, year_counts.get(peak_y, 0)), xytext=(2018.6, 1400),
             fontsize=8, color=GRAY_TEXT, ha="left",
             arrowprops=dict(arrowstyle="-", color=GRAY_TEXT, lw=0.7))
ax1.text(0.0, -0.24, "log scale — note the axis. Year-level bucketing only (YouTube's\n"
                       "“N years ago” strings resolve to the year, not finer).",
         transform=ax1.transAxes, fontsize=7.5, color=GRAY_TEXT, va="top")

# --- Panel B ---
ax2.set_facecolor("#fcfcfb")
x = range(len(months_b))
bars2 = ax2.bar(x, vals_b, color=BLUE, width=0.68, zorder=3)
ax2.set_title("Comments per month, Aug 2025–Jul 2026", fontsize=12, color=INK, fontweight="bold", loc="left", pad=10)
ax2.set_xticks(list(x))
ax2.set_xticklabels(month_labels, fontsize=8, color=GRAY_TEXT)
ax2.tick_params(axis="y", labelsize=8.5, colors=GRAY_TEXT)
for spine in ["top", "right", "left"]:
    ax2.spines[spine].set_visible(False)
ax2.spines["bottom"].set_color(GRAY_GRID)
ax2.grid(axis="y", color=GRAY_GRID, linewidth=0.7, zorder=0)
ax2.set_axisbelow(True)

# mark qtecqot video upload months + the m21-b5q plea/reply window
def idx_of(y, m):
    return months_b.index((y, m))

v1 = idx_of(2026, 5)
v2 = idx_of(2026, 6)
v3 = idx_of(2026, 7)
for ix, label in [(v1, "v1"), (v2, "v2"), (v3, "v3")]:
    ax2.plot([ix, ix], [0, vals_b[ix] + 60], color=ORANGE, lw=1.4, zorder=4)
    ax2.text(ix, vals_b[ix] + 75, label, color=ORANGE, fontsize=8, fontweight="bold", ha="center")

ax2.annotate("qtecqot uploads\nvideo 1 (05-25);\nm21-b5q plea +\nreply both land\nin this bar",
             xy=(v1, vals_b[v1]), xytext=(v1 - 3.9, 560),
             fontsize=7.6, color=GRAY_TEXT, ha="left",
             arrowprops=dict(arrowstyle="-", color=GRAY_TEXT, lw=0.7))

fig.suptitle("Comment volume across all seven videos (9,593 comments, capture 2026-07-29)",
             fontsize=13, color=INK, fontweight="bold", x=0.015, ha="left", y=0.995)
fig.text(0.015, 0.012,
         "Dates are estimated from YouTube's relative-time strings (“N weeks/months/years ago”), fuzzed by\n"
         "construction — see FINDINGS.md / TIMELINE.md for the bracketing method. Source: comments/capture_2026-07-29/.",
         fontsize=7.6, color=GRAY_TEXT, ha="left")

plt.tight_layout(rect=[0.01, 0.10, 0.99, 0.88])
plt.savefig("/home/user/new-skinny-bob/figs/people/comment_volume_over_time.png", dpi=200, facecolor="#fcfcfb")
print("saved")
print("years:", list(zip(years_a, vals_a)))
print("months:", list(zip(months_b, vals_b)))
