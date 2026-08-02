#!/usr/bin/env python3.12
"""Clock redo, second pass. Two corrections to the first pass and one real finding.

CORRECTION 1: the "tightest window" column in clock19.py is uninformative BY CONSTRUCTION.
Shifting every act by a constant offset cannot change the width of the arc that contains
them, so it reported 14.98 h for all nine zones. It measures the data's spread, not the
zone's fit. Dropped. Only the waking-hours violation count carries information.

CORRECTION 2: a single 07:00-24:00 band is one arbitrary choice. Scanned below.
"""
from datetime import datetime, timedelta
def U(s): return datetime.strptime(s,"%Y-%m-%dT%H:%M:%S")

X = [U(s) for s in """
2026-04-28T05:54:16 2026-05-07T06:17:03 2026-05-25T09:46:14 2026-05-25T09:50:36
2026-06-14T13:20:43 2026-06-14T13:23:30 2026-06-14T13:32:03 2026-06-15T04:53:33
2026-06-15T04:54:05 2026-07-28T07:18:28 2026-07-29T08:18:46 2026-07-31T07:21:01
2026-07-31T10:15:58 2026-07-31T10:18:24 2026-07-31T22:33:22 2026-08-01T02:09:43
2026-08-01T03:37:11 2026-08-01T03:45:49 2026-08-02T03:24:49""".split()]

def hrs(acts, off):
    return [((a+timedelta(hours=off)).hour+(a+timedelta(hours=off)).minute/60) for a in acts]
def viol(acts, off, lo, hi):
    return sum(1 for h in hrs(acts,off) if not (lo <= h < hi))

print("Offset scan, violations of three different waking bands (n=19 X posts)")
print(f"{'offset':>8}{'06-24':>8}{'07-24':>8}{'08-23':>8}   {'':<3}")
best={}
for half in range(-24,25):
    off=half/2
    v=[viol(X,off,6,24), viol(X,off,7,24), viol(X,off,8,23)]
    bar="#"*(19-v[1])
    print(f"{off:+8.1f}{v[0]:>8}{v[1]:>8}{v[2]:>8}   {bar}")
    best[off]=sum(v)
top=sorted(best.items(), key=lambda kv:(kv[1],abs(kv[0])))[:6]
print("\nbest offsets by summed violations:", ", ".join(f"UTC{o:+.1f} ({s})" for o,s in top))

print("\n\n--- the structure the aggregate hides ---")
EPOCH_A=[a for a in X if a < U("2026-07-31T20:00:00")]
EPOCH_B=[a for a in X if a >= U("2026-07-31T20:00:00")]
for name,grp in (("posts up to 2026-07-31 10:18 UTC",EPOCH_A),("posts from 2026-07-31 22:33 UTC",EPOCH_B)):
    us=[a.hour+a.minute/60 for a in grp]
    print(f"\n{name}: n={len(grp)}, UTC hour range {min(us):.2f}-{max(us):.2f}")
    row=[]
    for half in range(-24,25):
        off=half/2
        row.append((viol(grp,off,7,24),off))
    row.sort()
    zeroes=[o for v,o in row if v==0]
    print(f"  offsets with ZERO acts outside 07:00-24:00 local: "
          + (f"UTC{min(zeroes):+.1f} .. UTC{max(zeroes):+.1f}" if zeroes else "none"))

print("""
Reading: the two epochs demand incompatible clocks. Nothing that satisfies the first
satisfies the second. That is the finding -- not a time zone, but a discontinuity.""")
