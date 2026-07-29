# analysis/

One directory per line of enquiry. This is a record of what was actually run, not a
tidy library: no packaging, no tests, varying quality, and some of it superseded by
later passes. Where a directory is superseded, the matching report in `reports/` says
so. `reports/` is the readable layer over all of this.

| directory | what it was for |
|---|---|
| `compare-eras/` | 2011 against 2026: timecode fonts, playback rate, grain, banding |
| `corner-dots/` | the fixed dark dots in the black frames — and the codec control that settled them |
| `cyrillic/` | the hidden caption. `gen1/`, `gen3/`, `mk5-captions/`, `second-opinion/` are successive passes |
| `faces/` | the human-face sweeps in video 1 |
| `ghost-disc/` | the object behind title card A |
| `hand-proportions/` | digit ratios, the strongest single discriminator in the corpus |
| `insert-identification/` | the four-frame insert at `OpSTlDJWFFI` 2971–2974 |
| `mk4/`, `mk5-colour-segment/` | the colour segment |
| `audio-colour-segment/` | audio of that segment |
| `prior-work/` | material from earlier public analyses, for comparison |
| `scenes/` | shot-by-shot content pass |
| `symbol-panel/` | the interior symbol in video 3 |
| `teardown-video1/`, `-video2/`, `-video3/` | per-video teardowns |
| `third-party-toolkit/` | measurement of an outside analyst's released toolkit |
| `timecode-ticks/` | tick cadence, gate weave, border drift |
| `contact-sheets/` | overview sheets for eyeballing |

## Scripts that reference files you don't have

Three different reasons, and only the first is a problem:

**1. Frames.** Scripts read `frames/<video-id>/fNNNNN.png`, which isn't stored — it's
5 GB of lossless expansion from 23 MB of video. Make what you need first:

```bash
bin/frames OpSTlDJWFFI        # one video, ~60 s
bin/frames                    # all seven, ~6 min
```

**2. Outputs, not inputs.** A lot of the paths in these scripts are things the script
*writes* — `np.save('.../occ.npy')`, `out.save('.../mont_x.png')`. Those are absent
because the intermediate results weren't published, not because anything is missing.
Run the script and it makes them.

**3. Deliberately not shipped.** `third-party-toolkit/extracted/` is the unpacked
contents of a 1.6 GB third-party archive. It is not in this repo and will not be:
it contains a real personal name inside an Office lock file, and re-hosting somebody
else's release is not ours to do. Those scripts are kept as a record of the method and
the numbers they produced are in `reports/agent_zip_toolkit.md`. They are not runnable
here.

A handful of reports also name a working directory that no longer exists
(`analysis/agent_pdf/`, `analysis/scenes/morpho/`). Those held scratch artefacts that
weren't worth 15 GB of repo; the results are in the report text.

## Paths are absolute in a lot of these scripts

Written for one machine, `/home/user/new-skinny-bob/...`. In a Codespace the repo lives
somewhere else, so either run them with the repo at that path or fix the constant at the
top — usually one line. Not elegant. It is what it looked like when it was being used.
