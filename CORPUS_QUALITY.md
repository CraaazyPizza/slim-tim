# There are two copies of every video, and the analysis used the worse one

**Read this before trusting any result phrased as a limit.**

## What happened

YouTube serves the same video at several bitrates. It offers this footage at
1920×1080 in both AV1 and AVC, and at that identical frame size the AV1 version is
compressed far harder. The download tool prefers AV1 by default because it is
normally the better codec, so it took the thin one without saying anything.

The result: everything in this repo was measured on 310–489 kbps video when
1187–2059 kbps was available at the same resolution.

| video | `videos/2026/`, `videos/2011/` (AV1) | `videos/2026-avc/`, `videos/2011-avc/` (AVC) | ratio |
|---|---:|---:|---:|
| `ZB788PtqQvg` | 2.77 MB | 12.40 MB | 4.5× |
| `RsQCXN4o4Ps` | 2.64 MB | 10.08 MB | 3.8× |
| `Xju_CY5ZESA` | 1.74 MB | 3.37 MB | 1.9× |
| `a6TLGkrfNKI` | 0.60 MB | 2.75 MB | 4.6× |
| `OpSTlDJWFFI` | 5.23 MB | 16.99 MB | 3.2× |
| `Oqw96jCOP7A` | 4.36 MB | 12.87 MB | 3.0× |
| `l9RAhmPHM_A` | 5.42 MB | 16.31 MB | 3.0× |
| **total** | **22.8 MB** | **74.8 MB** | **3.3×** |

**Both copies are now in the repo.** The AVC set has been verified to be the same
seven videos: identical frame counts (1188 / 1500 / 2598 / 2337 / 2998 / 2503 /
4395) and identical resolutions, differing only in codec and bitrate.

`videos/2026/` and `videos/2011/` are deliberately **not** replaced. Every number in this repo
was computed on those files and has to stay reproducible. `bin/frames` and
`frames/README.md` read from them, so extracted frames stay byte-comparable to the
published ones unless you point them elsewhere on purpose.

## What this means for the findings

**Nothing here is known to be wrong because of it.** But the distinction that
matters is:

- **Positive findings — something *is* there — are safe.** If a thing is visible in
  a degraded copy it is visible in a better one. The sample-level audio copy, the
  time-base disagreement, the 26% digit-proportion difference, the four-frame
  insert existing at all: none of these get weaker with more bitrate.
- **Negative findings — something *isn't* there — are the problem.** Anywhere this
  repo says "too soft to resolve", "below the noise floor", or gives a detection
  floor, that number is partly a property of *this download* and not only of the
  footage. Read those as pessimistic, and rerun them on the AVC copy.

Audio is unaffected. Every track came from format 251 (Opus), the only audio rung
offered, in both fetches.

## The first thing the better copy settled

One result was **codec-specific by construction**, and having both copies turns it
from an accident into a controlled test.

FINDINGS §17 and §22 conclude that the fixed dark dots in the corners of the black
frames are an AV1 tile-corner artefact, not a mark placed in the picture. That
originally rested on luck: a third party's AVC frames happened to lack the stamp
ours carried. The prediction, stated properly, is that an authorial mark survives a
change of codec and an encoder artefact does not.

Frame 2 of `OpSTlDJWFFI`, same video, both codecs:

| | AV1 | AVC |
|---|---|---|
| luma histogram | 2,071,552 px at Y=16, **2,048 px at Y=17** | **2,073,600 px at Y=16**, nothing else |
| marked pixels | 2,048 | **0** |
| where | rows 0–31, cols 0–31 and 960–991 | — |
| all inside the two predicted 32×32 blocks | 2,048 of 2,048 | — |

Exactly the predicted count, in exactly the predicted places, and **completely
absent** from the AVC decode. Reproduce with
`analysis/corner-dots/controls/codec_control.py`.

This also explains the one-bit discrepancy that started the whole thread: the
outside analyst had the better copy all along.

## Still worth rerunning on the AVC copy

1. **The five-pointed star.** The null was already flagged as underpowered — a real
   star injected at 120 px and 35 DN was invisible to an independent observer too.
   On 3× the bitrate that test deserves rerunning, and the question may simply be
   answerable now.
2. **The four-frame insert** at `OpSTlDJWFFI` 2971–2974. Still unidentified. The
   most interesting object in the corpus and the best candidate to resolve.
3. **Anything phrased as a limit of the picture** — grain statistics, edge
   sharpness, the typeface fit, the hand-proportion measurement. Ratios between
   videos should survive. Absolute thresholds may not.

Report anything re-derived on the AVC copy **next to** the AV1 number, not in place
of it. The disagreement is the interesting part.

## Getting the files yourself

```bash
yt-dlp -f 'bestvideo[vcodec^=avc1]+bestaudio' --merge-output-format mkv \
       -o 'videos/2026-avc/%(id)s.mkv' <url>
```

The higher-bitrate formats need an authenticated session; without one YouTube
serves only a reduced ladder and then refuses the fragments. If you get 403s or a
"format is not available", that is an access problem, not evidence the formats are
gone.

A caution if you re-derive the corner-dot numbers by hand: plain `-pix_fmt gray`
rescales limited-range luma onto 0–255, which collapses the Y=16 / Y=17 distinction
the test depends on into 0 / 1. Force full range in and out to keep the codeword
values quoted above.
