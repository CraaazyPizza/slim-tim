# Unfinished business

**This is the to-do list. If you want something to work on, it's in here.**

Everything below is either a measurement nobody has made, a claim in the documents that
needs fixing, or something that was worked out and never written down. Priorities are
`[H]`/`[M]/[L]` — high items are ones where the current record is either wrong or missing
something load-bearing.

I'm not working on these right now. Take any of them.

---

## Start here: rerun the soft calls on the better copy

**`[H]`** Everything in this repo was measured on the thinner of two available copies of the
videos. YouTube serves the same 1920×1080 picture at several bitrates and the download tool
quietly took the thinnest, so every measurement was made on ~3× less information than was
available. One page on it: [`CORPUS_QUALITY.md`](CORPUS_QUALITY.md).

The better copy is in the repo as `videos/2026-avc/` and `videos/2011-avc/` (74.8 MB against
22.8 MB), verified frame-for-frame identical in content. `videos/2026/` and `videos/2011/` are
unchanged on purpose so the existing numbers stay reproducible. `bin/frames --avc` extracts
from the better set into `frames-avc/`.

Nothing is known to be *wrong* because of this. But anything phrased as a limit — "too soft to
see X", "below the noise floor", any stated detection floor — is partly a limit of the
download, not the footage. Worth rerunning, highest value first:

1. **`[H]` The five-pointed star.** The null was already underpowered: a real star injected at
   120 px and 35 DN was invisible to an independent observer too. It may simply be answerable
   now.
2. **`[H]` The four-frame insert**, `OpSTlDJWFFI` 2971–2974. Still unidentified, and the best
   candidate to resolve with 3× the bitrate. Two models have confidently misidentified it;
   see [`docs/PITFALLS.md`](docs/PITFALLS.md) before trusting a third.
3. **`[M]` Anything phrased as a limit of the picture** — grain, edge sharpness, the typeface
   fit, the hand proportions. Ratios between videos should survive; absolute thresholds may
   not.

Report AVC results *next to* the AV1 numbers, not instead of them. The disagreement is the
interesting part.

**Already settled by having both copies:** the corner dots. §17/§22 predicted the artefact
would vanish under a different codec, and it does — exactly 2,048 marked pixels under AV1,
zero under AVC, all inside the two predicted 32×32 blocks.
`analysis/corner-dots/controls/codec_control.py`.

---

## Analysis nobody has run

The best place to find real work. Effort estimates are rough.

| # | Target | Why it matters | Effort |
|---|---|---|---|
| 1 | **Video 3 face sweep** | 4,395 frames, **44% of the 2026 corpus** — more than either other video — and the most-watched of the three. Never swept. Only two ledger rows, with no observed frame ranges. A corpus-wide "only one human face" claim already had to be retracted once because of this gap | 2–3 h |
| 2 | **The Mk.4 pace-lap sequence**, video 1 f1290–1900 | Best-resolved craft material in the corpus. Started, not finished — 186 frames tracked in `analysis/mk4/`. Three open tests: whether the specular highlight is locked to the hull or **migrates** across it (preliminary says it migrates, u −0.16→+0.08 over f1596–1645); a surface-of-revolution fit, then the same fit on the Mk.5 to ask **one hull or two**; and the structured f1442–1494 object that shares frames with the §31 human figure | in flight |
| 3 | **Fix `analysis/symbol-panel/tilt_test.py` and redo the foreshortening result** | The symbol mark appears to show **no measurable foreshortening** (anisotropy median 1.04) while translating 380 px across a shot whose composition changes completely. That would be a strong tell. It does **not** currently hold: only 145 of 662 frames registered, so selection bias, and the ASIFT tilt control failed because pooled descriptors defeated the ratio test. The fix is to match per affine simulation rather than against a pooled descriptor database. Until then it's a lead, not a result | 2–3 h |
| 4 | **Reconcile frames-per-tick: 44.5 vs 46.0** (§11.2 vs §30.4) | **The linchpin.** §12's headline rests on both eras holding ~45–46 frames per tick at *different* frame rates. The two measurements disagree and nobody has reconciled them. Two of seven tick boundaries sit behind flares | 1–2 h |
| 5 | **A five-digit human-hand control for §28** | §28 is the strongest positive result in the repo and it has no human-hand control | 2–4 h |
| 6 | **Frame-precise segment maps for videos 2 and 3** | One exists for video 1 only. Folds into #1 | 2 h |
| 7 | **Redo the 2011 Cyrillic sweep with timecode masking** | The current sweep is invalid without it | 3–4 h |
| 8 | **A Sapphire trial render, plus preset version history** | The strongest available *confirmatory* test of the post-processing thread, described in `docs/PIPELINE.md`. Never started | ? |
| 9 | **Reconcile the palm-width figures** | §21's 1.38/1.37 against the newer 2.01/1.40. One has a definitional problem, and §21's is the one carrying a claim that was retracted | 1 h |