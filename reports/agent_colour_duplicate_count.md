# Colour Mk.5 segment — independent duplicate count (`OpSTlDJWFFI` f2571–2917)

Scripts: `analysis/colour-duplicate-count/`. All frame numbers are 1-indexed PNGs in
`frames/OpSTlDJWFFI/` and `frames-avc/OpSTlDJWFFI/`, 1920×1080, 29.97 fps. Everything
below separates **measurement** from **interpretation** (labelled as such).

Decoded with ffmpeg 4.4.2, python 3.12.13, numpy 2.4.6, pillow 12.3.0. The SHA-256 of
every input frame is recorded in `pairs_av1.json` / `pairs_avc.json`, so a rerun that
disagrees can tell whether it was looking at different pixels or running different
arithmetic. Reruns are byte-identical.

---

## 0. Why this was measured

Two reports in this repo disagree about the same 346 frame pairs.

- `agent_video1_OpSTlDJWFFI.md` §"Underlying temporal structure" lists a strict
  period-12 duplicate series **f2578, 2590, 2602 … 2878** — 26 frames.
- `agent_mk5_claims.md` item 5e re-measures the same segment and reports **3
  near-identical consecutive pairs in 346 frames**, describing the period-12 conform as
  "only weakly expressed here".

The count is load-bearing. FINDINGS §20 states the colour clip's distinct-image rate as
`frames-per-tick × 11/12`, and that factor is only valid if the conform is fully
expressed in this segment. At 26 duplicates the multiplication is right; at 3 it is
wrong by a factor of ten, and the published figure would have to be rebuilt from a
directly measured unique-image count instead.

Neither prior classification was reused. The scan was written without a period-12
prior: phase is recorded but never used to select, threshold or weight anything, so
phase concentration is a **result** of the scan rather than an input to it.

---

## 1. Method

`dupdetect.py` computes six independent quantities for every consecutive pair in
f2571–2917 (346 pairs, the same range both prior reports used), loading one frame of
margin either side so the edge pairs are real pairs:

| quantity | what it is |
|---|---|
| `exact` | SHA-256 of the two PNGs identical |
| `mad_y` | mean absolute Rec.709 luma difference |
| `mad_rgb` | mean absolute difference over all three channels |
| `max_y` | largest single-pixel luma difference |
| `frac_gt4` | fraction of pixels differing by more than 4 in any channel |
| `norm` | `mad_y` against the median of a ±6-frame window, excluding itself |

The local normalisation exists because a raw threshold cannot work across this segment:
local motion varies by more than an order of magnitude between the static interior shots
and the flare-swept tail, so an absolute cut calibrated anywhere is wrong everywhere
else. **That is precisely the failure mode this scan was built to check for**, and §5
shows it is what happened.

`classify.py` places the threshold at the largest relative jump in the lower half of the
sorted distribution — the lower half only, to keep the cut away from the long upper tail
of ordinary motion where the biggest absolute jumps live and mean nothing. It asserts no
count, no phase and no cut; every figure below is derived from the JSON.

---

## 2. Result

**29 duplicate pairs.**

### 2.1 The deciding criterion: the two populations are disjoint

The count does not rest on a threshold at all. Sorted on raw `mad_y`, the segment
separates into two populations with clear air between them:

| | n | median `mad_y` | extreme |
|---|---|---|---|
| duplicates | 29 | 0.1128 | max **0.3885** |
| everything else | 317 | 1.6971 | min **0.5195** |

**Any cut placed anywhere in the gap 0.3885–0.5195 returns exactly the same 29 pairs.**
There is no borderline case, so the count is insensitive to where in that range a cut is
put — which is the property that makes it worth reporting. The absolute-threshold sweep
in §5 shows the same thing from the other side: 29 at both 0.40 and 0.50.

**Phase is never used to select, threshold or weight anything.** It is computed after
classification and reported as a property of the resulting set. That the 29 pairs turn
out to share one phase is a result, not a construction.

### 2.2 The initial classifier, and the three pairs it gets wrong

`classify.py` derives its cut from the largest relative jump in the sorted `norm`
distribution, giving `norm < 0.1726` and **28** pairs — 27 duplicates plus one
misclassification, and two duplicates missed. All three disagreements are resolved by
the disjointness criterion in §2.1, and all three are instructive:

| pair | phase | `mad_y` | `norm` | `local_med` | `max_y` | `frac>4` | AVC `mad_y` |
|---|---|---|---|---|---|---|---|
| f2601→f2602 | 9 | 0.3885 | 0.2532 | 1.5343 | 7.0 | 1.15% | **0.0004** |
| f2889→f2890 | 9 | 0.2944 | 0.2843 | 1.0356 | 11.0 | 0.46% | 0.2152 |
| f2912→f2913 | **8** | **0.5478** | 0.1199 | **4.5684** | **47.35** | **4.33%** | 0.5514 |

**The two missed duplicates** are the two noisiest members of the set in AV1, and they
sit in *quieter*-than-average neighbourhoods — local medians 1.53 and 1.04 against a
segment median of 1.68 — so the normalisation divides by a small denominator and works
against them. They fail the `norm` cut for that reason alone; both are comfortably inside
the duplicate population on raw `mad_y`.

They are not confirmed the same way, and the difference is worth recording. f2601→f2602
**collapses under AVC**, 0.3885 → 0.0004, a factor of about 970: its AV1 elevation was
entirely re-quantisation noise. f2889→f2890 **does not collapse**, 0.2944 → 0.2152. It
carries a small genuine residual and is the least clean member of the set — still far
below the AVC non-duplicate floor of 0.4736, so it stays cleanly in the duplicate
population under both codecs, but it is the one pair here that a stricter observer could
reasonably want re-examined.

**The one misclassification, f2912→f2913, is the mirror image** and shows exactly why an
unnormalised criterion has to be the final word. It sits in the terminal white-out at the
end of the segment, where its neighbours are changing violently — f2911→f2912 has
`mad_y` 1.96 with 23.8% of pixels moving, f2914→f2915 has 0.98 with 10.4%. Its local
median of 4.57 is nearly 3× the segment median, so dividing by it flatters a pair that is
in absolute terms a large picture change: `mad_y` 0.5478, a single-pixel excursion of 47
DN, and 4.33% of pixels differing by more than 4. It is a real advance that merely looks
quiet next to its neighbours. The disjointness criterion excludes it — 0.5478 is above
the 0.5195 non-duplicate floor — and it does not collapse under AVC either (0.5514),
confirming genuine picture change rather than codec noise.

### 2.3 Phase

Pairs are indexed by their first frame, so a duplicate pair is `a ≡ 9 (mod 12)` and the
duplicated frame itself is `b ≡ 10 (mod 12)`. This is the same structure
`agent_mk5_claims.md` records as "all at phase 10 mod 12" and the same series
`agent_video1` lists by duplicate-frame number. **The three measurements agree on phase
and disagree only on count.**

Mean normalised score by phase, AV1 copy:

| phase | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | **9** | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mean `norm` | 1.21 | 1.18 | 1.34 | 1.18 | 1.15 | 1.13 | 1.13 | 1.12 | 0.91 | **0.079** | 1.01 | 1.08 |

### 2.4 The full set

Every one of the 29 pairs, AV1 alongside AVC:

| pair | AV1 `mad_y` | AVC `mad_y` | `norm` (AV1) | `max_y` | `frac>4` |
|---|---|---|---|---|---|
| f2577→f2578 | 0.0489 | 0.0009 | 0.024 | 7.0 | 0.02% |
| f2589→f2590 | 0.1389 | 0.0012 | 0.056 | 9.0 | 0.52% |
| f2601→f2602 | 0.3885 | 0.0004 | 0.253 | 7.0 | 1.15% |
| f2613→f2614 | 0.1611 | 0.0017 | 0.094 | 8.0 | 0.20% |
| f2625→f2626 | 0.1050 | 0.0008 | 0.064 | 10.3 | 0.18% |
| f2637→f2638 | 0.1162 | 0.0001 | 0.053 | 12.3 | 0.12% |
| f2649→f2650 | 0.0681 | 0.2513 | 0.034 | 7.0 | 0.02% |
| f2661→f2662 | 0.0596 | 0.0000 | 0.027 | 6.0 | 0.10% |
| f2673→f2674 | 0.0340 | 0.0004 | 0.014 | 7.0 | 0.04% |
| f2685→f2686 | 0.0861 | 0.0256 | 0.038 | 7.1 | 0.20% |
| f2697→f2698 | 0.1256 | 0.0035 | 0.063 | 7.1 | 0.24% |
| f2709→f2710 | 0.1220 | 0.0011 | 0.090 | 12.7 | 0.24% |
| f2721→f2722 | 0.0689 | 0.0009 | 0.051 | 7.0 | 0.12% |
| f2733→f2734 | 0.1479 | 0.0003 | 0.088 | 9.0 | 0.22% |
| f2745→f2746 | 0.1298 | 0.0004 | 0.089 | 15.0 | 0.14% |
| f2757→f2758 | 0.1919 | 0.1062 | 0.096 | 11.2 | 0.41% |
| f2769→f2770 | 0.1609 | 0.2884 | 0.104 | 8.0 | 0.26% |
| f2781→f2782 | 0.1910 | 0.0001 | 0.130 | 7.9 | 0.27% |
| f2793→f2794 | 0.0723 | 0.0018 | 0.029 | 7.0 | 0.02% |
| f2805→f2806 | 0.1122 | 0.0041 | 0.065 | 6.0 | 0.14% |
| f2817→f2818 | 0.1128 | 0.0058 | 0.067 | 7.9 | 0.25% |
| f2829→f2830 | 0.0625 | 0.0007 | 0.047 | 5.9 | 0.05% |
| f2841→f2842 | 0.0515 | 0.0001 | 0.036 | 5.7 | 0.02% |
| f2853→f2854 | 0.0779 | 0.0007 | 0.067 | 5.2 | 0.20% |
| f2865→f2866 | 0.1357 | 0.0006 | 0.106 | 19.0 | 0.14% |
| f2877→f2878 | 0.1085 | 0.0005 | 0.090 | 7.0 | 0.15% |
| f2889→f2890 | 0.2944 | 0.2152 | 0.284 | 11.0 | 0.46% |
| f2901→f2902 | 0.1285 | 0.0000 | 0.104 | 7.0 | 0.12% |
| f2913→f2914 | 0.0672 | 0.0216 | 0.014 | 7.7 | 0.07% |

Figures: `contact_sheet.png`, `phase_signature.png` in the same directory.

The contact sheet carries the qualitative discriminator, which is stronger than any
threshold and needs no statistics: **a conform duplicate differs from its neighbour only
by blocky codec quantisation noise; a genuinely advancing pair differs along object
edges** — the craft rim, the doorframe, the caption glyphs. Even the weakest duplicate,
f2601→f2602, shows no edge structure whatsoever. Per `docs/PITFALLS.md` the frames
themselves are shown unmodified; only the third column, explicitly labelled, is
amplified.

---

## 3. Codec cross-check

The same scan on `videos/2026-avc/` returns **the same 29 pairs, in the same order, at
the same phase**. `classify.py` compares the two sets directly and reports identity.

| | AV1 | AVC |
|---|---|---|
| duplicate pairs | 29 | 29 |
| dominant phase | 9 | 9 |
| median `mad_y`, duplicates | 0.1128 | **0.0009** |
| median `mad_y`, all others | 1.6971 | 1.6244 |
| bit-identical pairs | 0 | **1** |

This is the decisive control. Under the ~3× richer copy the duplicate population
collapses by two orders of magnitude — most pairs fall below `mad_y` 0.002 and one is
bit-identical — while the non-duplicate population barely moves. **A true duplicate
loses its residual under a better encoder; real motion does not.** The AV1 residual of
0.03–0.39 is therefore AV1 re-quantisation of identical source frames, not picture
change.

It also settles a wording dispute. `agent_video1` calls these pairs "bit-identical";
`agent_triage_technical.md` §9.3 flags that v2 and v3 call the same phenomenon
"near-identical, *not* bit-identical" and recommends the latter. Both are right about
their own copy: zero pairs are bit-identical under AV1, one is under AVC. "Near-identical"
remains the defensible word for the corpus the writeups were measured on.

---

## 4. Derived cadence

All computed from the measured set, not assumed:

```
duplicate pairs    29 / 346  = 0.08382      (1/12 = 0.08333)
implied period     346 / 29  = 11.931 frames
unique fraction    317 / 346 = 0.91618      (11/12 = 0.91667)   agreement 0.053%
```

**The 11/12 conform factor is confirmed for this segment by direct measurement**, to
five parts in ten thousand. It was previously carried into the colour clip on the
strength of the global result, and `agent_mk5_claims.md` had called that into question.

*Interpretation, bounded:* this establishes the delivered frame cadence of this segment.
It says nothing about where the imagery came from.

---

## 5. Why the two prior reports diverged

**`agent_mk5_claims.md`'s 3 is a threshold-transfer artefact, and it reproduces
exactly.** The v2 and v3 reports defined "near-identical" by the absolute band
`mad 0.02–0.07`, calibrated on their own footage. Applying an absolute cut to this
segment, which has a higher AV1 noise floor:

| cut on `mad_y` | pairs | at phase 9 |
|---|---|---|
| 0.05 | 2 | 2 |
| 0.06 | 4 | 4 |
| 0.07 | 8 | 8 |
| 0.10 | 11 | 11 |
| 0.15 | 23 | 23 |
| 0.20 | 27 | 27 |
| 0.30 | 28 | 28 |
| **0.40** | **29** | **29** |
| 0.50 | 29 | 29 |

A cut near 0.05–0.06 yields two to four pairs. The series is not weakly expressed; an
absolute threshold truncates it. Note there are **zero false positives at any cut** —
every detection at every threshold lands on phase 9, which is itself strong evidence
that the structure is fully present and merely being clipped.

The report's own observation that all three of its hits sat at one phase should have
been the tell. Three hits landing on the same phase out of twelve is p ≈ 0.7% by chance;
that is the signature of a real periodic structure being under-detected, not of a weak
one.

**`agent_video1`'s 26 is correct but truncated.** Its series f2578 … f2878 is exactly 26
frames and every member is in the measured set. The series does not stop at f2878 — it
continues to f2890, f2902, f2914, giving 29 across the full segment. Its "bit-identical"
wording is wrong for the AV1 copy; see §3.

---

## 6. Consequence for the record

FINDINGS §20 currently reads "about 40.8 distinct images per source second". That figure
was `44.5 × 11/12`, and 44.5 is the frames-per-tick value retracted in FINDINGS §10.5.
`agent_triage_technical.md` §4.6 item 3 proposes recomputing it as `45.55 × 11/12 = 41.7`,
but 45.55 is the pooled **b/w Case 12** cadence, and this is a claim about the **colour**
clip — the same cross-segment substitution the §4 reconciliation removed. That document's
own §0 and §4.5 give the colour Mk.5 fragment as 45.0.

With the conform factor now measured rather than assumed:

```
45.0 frames/tick × 0.91618 unique/frame = 41.23 unique images per source second
```

| | |
|---|---|
| published 40.8 | wrong — inherits the retracted 44.5 |
| triage's 41.7 | wrong — b/w cadence applied to a colour-clip claim |
| **measured 41.2** | 45.0 × 0.91618; 41.25 using exact 11/12 |

Two caveats on quoting it. 45 and 12 are incommensurate (gcd 3, realigning every 180
frames), so any single tick contains 3 or 4 duplicates and 41.2 is a long-run average,
not a per-second count. And `agent_video2` measured the period as ~12.09 rather than 12,
which would give 41.28 — immaterial, but it means 11/12 is itself a rounding.

The direction of FINDINGS §20's conclusion is unaffected: 41.2 is still far above any
plausible 1961 amateur cine rate, so "synthesized intermediates or a high-rate source"
stands. Only the number changes.

*Still not measured:* the b/w "16 ± 1 distinct images per burned-in second" was counted
inside windows assumed to be **46** frames long — the same retracted value — across 24
intervals, of which only 11 fall inside the digit-verified Case 12 run. That inheritance
is untested and is not addressed here.

---

## 7. Reproducing

```bash
bin/frames OpSTlDJWFFI 2570 2918
bin/frames --avc OpSTlDJWFFI 2570 2918
python3.12 analysis/colour-duplicate-count/dupdetect.py
python3.12 analysis/colour-duplicate-count/dupdetect.py --copy avc
python3.12 analysis/colour-duplicate-count/classify.py
python3.12 analysis/colour-duplicate-count/sheet.py
```

About four minutes, most of it the two frame extractions. The scripts use paths relative
to the repo root and hardcode no counts, so a rerun on different frames yields different
numbers rather than these ones.
