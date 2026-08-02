#!/usr/bin/env python3.12
"""Redo of dossier section 3 against every machine-read instant, not the seven we had.

The old section used 7 acts and reported a clean CEST 06:23-11:39 band, "eight for eight".
The deleted-post recovery of 2026-08-02 added 17 more authored instants. This recomputes
from scratch. Nothing is tuned: each act is rendered as local time under a candidate UTC
offset and scored on how many fall outside a plausible waking band.
"""
from datetime import datetime, timedelta

def U(s): return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")

# --- qtecqot: authored on X (cannot be scheduled). 19 posts, 11 of them recovered from deletion.
X_POSTS = [U(s) for s in """
2026-04-28T05:54:16 2026-05-07T06:17:03 2026-05-25T09:46:14 2026-05-25T09:50:36
2026-06-14T13:20:43 2026-06-14T13:23:30 2026-06-14T13:32:03 2026-06-15T04:53:33
2026-06-15T04:54:05 2026-07-28T07:18:28 2026-07-29T08:18:46 2026-07-31T07:21:01
2026-07-31T10:15:58 2026-07-31T10:18:24 2026-07-31T22:33:22 2026-08-01T02:09:43
2026-08-01T03:37:11 2026-08-01T03:45:49 2026-08-02T03:24:49""".split()]
# --- account/channel creation: authored, not schedulable
CREATE = [U("2026-04-22T05:27:55"), U("2026-04-28T05:24:54")]
# --- uploads: SCHEDULABLE, so weaker evidence. Kept separate on purpose.
UPLOADS = [U("2026-05-25T09:39:42"), U("2026-06-15T04:23:35"), U("2026-07-24T09:14:05")]

IVAN = [U(s) for s in """2011-04-14T01:08:36 2011-04-14T02:04:26 2011-05-02T05:21:51
2011-05-09T05:09:51 2011-05-18T00:35:43""".split()]

ZONES = {"UTC+0 (UK win)":0, "CEST (+2)":2, "Moscow (+3)":3, "UTC+4":4, "India (+5.5)":5.5,
         "US Eastern (-4)":-4, "US Central (-5)":-5, "US Mountain (-6)":-6, "US Pacific (-7)":-7}

def local_hours(acts, off):
    return [((a + timedelta(hours=off)).hour + (a + timedelta(hours=off)).minute/60) for a in acts]

def outside(hours, lo=7.0, hi=24.0):
    """Acts outside a plausible waking band. 07:00-24:00 local is generous to every zone."""
    return sum(1 for h in hours if not (lo <= h < hi))

def tightest_window(hours):
    """Smallest circular arc (in hours) containing every act."""
    hs = sorted(hours); n = len(hs)
    best = 24.0; start = None
    for i in range(n):
        span = (hs[(i-1) % n] - hs[i]) % 24
        if span < best: best, start = span, hs[i]
    return best, start

def report(label, acts):
    print(f"\n{'='*74}\n{label}  (n={len(acts)})\n{'='*74}")
    print(f"{'zone':<18}{'outside 07-24':>14}{'tightest window':>32}")
    rows = []
    for z, off in ZONES.items():
        h = local_hours(acts, off)
        span, start = tightest_window(h)
        rows.append((outside(h), span, z, start))
        print(f"{z:<18}{outside(h):>10} / {len(acts):<3}"
              f"{f'{span:5.2f} h  from {int(start):02d}:{int(start%1*60):02d}':>32}")
    rows.sort()
    print(f"\n  best by waking-hours violations: {rows[0][2]}  ({rows[0][0]} outside)")
    rows.sort(key=lambda r: r[1])
    print(f"  best by tightest window:         {rows[0][2]}  ({rows[0][1]:.2f} h wide)")
    return rows

print("### qtecqot -- X posts only (authored, non-schedulable). This is the real test.")
report("qtecqot X posts", X_POSTS)
print("\n### qtecqot -- every authored act (posts + account creations)")
report("qtecqot authored", X_POSTS + CREATE)
print("\n### qtecqot -- the OLD seven (2 creations + 3 uploads + 2 of the July posts)")
report("old seven", CREATE + UPLOADS + [U("2026-07-28T07:07:01"), U("2026-07-28T07:18:28")])
print("\n### ivan0135 2011, unchanged for comparison")
report("ivan0135", IVAN)

print("\n\n--- raw local times of the 19 X posts, per zone ---")
print(f"{'UTC':<20}" + "".join(f"{z:>16}" for z in ("CEST (+2)","Moscow (+3)","US Eastern (-4)","US Pacific (-7)")))
for a in X_POSTS:
    row = f"{a.strftime('%m-%d %H:%M'):<20}"
    for z in ("CEST (+2)","Moscow (+3)","US Eastern (-4)","US Pacific (-7)"):
        loc = a + timedelta(hours=ZONES[z])
        h = loc.hour + loc.minute/60
        mark = "*" if not (7.0 <= h < 24.0) else " "
        row += f"{loc.strftime('%H:%M')+mark:>16}"
    print(row)
print("\n(* = outside 07:00-24:00 local, i.e. the act happened in that zone's small hours)")
