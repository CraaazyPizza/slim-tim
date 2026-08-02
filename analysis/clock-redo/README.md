# The clock, redone against all 19 posts

Dossier §3 rendered **7** machine-read instants against four time zones and found a clean
Central European morning band. The 2026-08-02 recovery of 11 deleted posts took the count of
authored, non-schedulable acts from 2 to 19. This is the recompute.

Run: `python3.12 analysis/clock-redo/clock19c.py` (the one to trust). `clock19.py` and
`clock19b.py` are kept because each contains an error worth not repeating, documented in their
docstrings and in `CORRECTIONS.md` §6 of the 2026-08-02 entry.

## Method

Each act is rendered as a local time under a candidate UTC offset, and scored on how many fall
outside a waking band. Nothing is fitted. The band is a choice, so `clock19b.py` scans three
(06–24, 07–24, 08–23) and the answer is stable across them.

**Uploads are excluded.** YouTube uploads can be scheduled; posts and account registration
cannot. §3 mixed them. Using only the 19 X posts is the stricter test and is what is reported.

## Result

| zone | posts falling in the local small hours |
|---|---|
| CEST (+2) | **7 of 19** |
| Moscow (+3) | 5 of 19 |
| US Eastern (−4) | 11 of 19 |
| US Pacific (−7) | 10 of 19 |

Offsets under which **no** post lands in the small hours: **UTC+8.5, +9.0, +9.5, +10.0**. Every
other offset from −12 to +12 has at least one violation.

## What to conclude, and what not to

**Do not** conclude the operator is at UTC+9. The all-or-nothing waking-hours test is brittle:
one late-night post eliminates a candidate, and people post at 2 a.m. The honest statement is
that **the clock no longer identifies a zone**. It excludes Europe and the Americas as *clean*
fits, and the least-violating region has moved a long way east of where §3 put it.

**The discontinuity is the real structure.** The 14 posts up to 2026-07-31 10:18 UTC sit in a
UTC 04:53–13:32 band. The 5 posts from 2026-07-31 22:33 UTC sit in a UTC 22:33–03:45 band.
Taken separately the early epoch admits UTC+2.5 to +10 and the late epoch admits a much wider
range. **They are not incompatible** — the intersection is UTC+8.5 to +10, which is exactly the
all-19 answer — but a roughly 12-hour shift in posting window appearing overnight on 31 July is
the most conspicuous thing in the series and nothing here explains it. Travel, a schedule
change, and a second hand at the keyboard all fit.

## What survives from §3

The ivan0135 half is untouched: 5 acts in 2011, tightest in US Mountain and US Pacific evening,
zero violations there and 3 of 5 in the Central European night. The **contrast** between the two
accounts' clocks therefore survives in direction even though qtecqot's own best-fit zone moved.
The specific sentence "the two clocks do not overlap" needs restating against the new numbers
before it is used again.

`figs/qtecqot-2026-08-02/3_clock.png` is the figure. `figs/qtecqot/clock.png` is the old one and
should not be cited.

## The dossier figure

`figs/qtecqot/clock.png` was the dossier's §3 figure and showed the 7-act reading. It has been
regenerated against all 19 posts by `make_dossier_clock.py`. Two things to know before trusting
it:

- **It is a reconstruction, not a rerun.** No script in this repo ever generated the original;
  the PNG arrived in the initial commit. The rebuild matches the original's design from the
  image, so treat small styling differences as expected.
- **The band moved.** The original shaded 23:00–07:00. The rebuild uses 00:00–07:00 to agree
  with `clock19c.py` and `figs/qtecqot-2026-08-02/3_clock.png`. Under the old 23:00 edge the
  same data reads US Eastern 14 and US Pacific 11 instead of 11 and 10, which would have put
  two numbers on one measurement. `clock19b.py` scans three bands and the conclusion is stable
  across all of them.

The 7-act original is preserved at `figs/qtecqot/withdrawn/clock_7acts_2026-07-29_WITHDRAWN.png`.
