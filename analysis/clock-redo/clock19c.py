#!/usr/bin/env python3.12
"""Clock redo, third pass. Fixes a wrong claim made in the second pass.

clock19b.py printed "offsets with ZERO violations: UTC-12.0 .. UTC+12.0" for the late
epoch and I read that as the two epochs being incompatible. That was wrong twice over:
the printout collapsed a set to its min and max (so it looked contiguous when it need not
be), and 5 acts spanning a ~5 h arc inside a 17 h waking band are satisfied by MOST
offsets, not none. The epochs are not incompatible. Set intersection below, done properly.
"""
from datetime import datetime, timedelta
def U(s): return datetime.strptime(s,"%Y-%m-%dT%H:%M:%S")
X = [U(s) for s in """
2026-04-28T05:54:16 2026-05-07T06:17:03 2026-05-25T09:46:14 2026-05-25T09:50:36
2026-06-14T13:20:43 2026-06-14T13:23:30 2026-06-14T13:32:03 2026-06-15T04:53:33
2026-06-15T04:54:05 2026-07-28T07:18:28 2026-07-29T08:18:46 2026-07-31T07:21:01
2026-07-31T10:15:58 2026-07-31T10:18:24 2026-07-31T22:33:22 2026-08-01T02:09:43
2026-08-01T03:37:11 2026-08-01T03:45:49 2026-08-02T03:24:49""".split()]
OFFS=[h/2 for h in range(-24,25)]
def ok(acts,off,lo=7.0,hi=24.0):
    return all(lo <= ((a+timedelta(hours=off)).hour+(a+timedelta(hours=off)).minute/60) < hi
               for a in acts)
def fmt(s): return ", ".join(f"{o:+.1f}" for o in sorted(s)) if s else "(none)"

A=[a for a in X if a < U("2026-07-31T20:00:00")]   # 14 posts, Apr 28 - Jul 31 10:18
B=[a for a in X if a >= U("2026-07-31T20:00:00")]  # 5 posts, Jul 31 22:33 - Aug 2 03:24
sA={o for o in OFFS if ok(A,o)}; sB={o for o in OFFS if ok(B,o)}; sX={o for o in OFFS if ok(X,o)}
print(f"early epoch (n={len(A)}) admits : {fmt(sA)}")
print(f"late  epoch (n={len(B)}) admits : {fmt(sB)}")
print(f"intersection                    : {fmt(sA&sB)}")
print(f"all 19 together                 : {fmt(sX)}")
print(f"\nCEST (+2.0) in the all-19 set?   {2.0 in sX}")
print(f"Moscow (+3.0) in the all-19 set? {3.0 in sX}")
print("\nviolations under a 07:00-24:00 band, the zones the dossier tabulated:")
for z,o in (("CEST (+2)",2),("Moscow (+3)",3),("US Eastern (-4)",-4),("US Pacific (-7)",-7)):
    v=sum(1 for a in X if not ok([a],o))
    print(f"  {z:<18} {v:>2} of 19 acts in the local small hours")
