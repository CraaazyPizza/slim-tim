# AGENTS.md

Facts about this repo you can't infer from reading it. Long versions, with the specific
failures behind each, in [`docs/PITFALLS.md`](docs/PITFALLS.md).

Seven videos: four from `ivan0135` (2011), three from `qtecqot` (2026) claiming to continue
them. **Provenance is undetermined and stays that way** — findings constrain how the videos
were assembled, not whether the footage is genuine. `FINDINGS.md` is what we think is true,
`CORRECTIONS.md` what we got wrong.

## The footage will make you hallucinate

Not a generic caution. Subject resolution of a few hundred pixels, point-spread width
5–6.6 px: enough structure to look interpretable, not enough to constrain it. Five documented
failures here, and **confidence was inversely correlated with correctness** — Apollo 11 at
95% and a military UAP video at 99%, both wrong, both about the same four frames, disagreeing
with each other.

So: ask neutrally ("what do you see?" not "do you see a face?"), ask twice in separate
contexts, put the null on the table explicitly or it won't get picked, and work from
unmodified frames — the enhanced and averaged ones are in here and labelled.

## Never state an absence without a detection floor

Inject a synthetic version at graded amplitudes and report where detection fails. A real star
at 120 px and 35 DN was invisible to an independent observer, so five negative frames proved
nothing.

**Every floor here is pessimistic**, measured on the thin AV1 copy in `videos/2026/` when
`videos/2026-avc/` carries ~3× more. Check which copy you're on before calling something
unresolvable — `CORPUS_QUALITY.md`.

## Second opinions need a clean room

`gemini` is the strongest of the three CLIs at vision here. But **running it inside this repo
poisons the answer** — it reads our own findings and hands them back as independent. That
happened, and the "independent confirmation" was worthless.

```bash
mkdir -p /tmp/vq && cp <frame>.png /tmp/vq/image_01.png   # neutral filename
cd /tmp/vq && env -u GEMINI_CLI_IDE_WORKSPACE_PATH -u GEMINI_CLI_IDE_SERVER_PORT \
  gemini --skip-trust -p "@image_01.png What do you see? If nothing is identifiable, say so."
```

Two traps in that command: a filename like `case22_bearded_face.png` supplies the answer, and
without `-p` it prints help and exits **0**, which looks like success.

## The decoder is part of the method

**ffmpeg 4.4.2.** Across versions the same decode differs by 16 bytes a frame; across codecs
by up to 1 in 255 — and that one-bit delta *is* a finding, it's how the corner dots were
identified as AV1 tile artefacts. `bin/frames` makes frames; `frames/README.md` has the rest.

## Local facts

- **`python3.12`**, not `python3`.
- `analysis/` is one-off scripts with absolute paths, not a pipeline — nothing reruns end to
  end. `analysis/README.md` maps it and explains why a referenced file may be missing.
- The work went through generations; only the last is right. Before trusting an old figure,
  check `FINDINGS.md` still cites it.

## Before publishing anything

- **Build by inclusion, never redaction.** A grep pass here missed an email rendered *inside
  an image*, then a real name in a screenshot's comment-box placeholder. Text search sees
  neither. Enumerate what goes in.
- **Never name a private individual.** Two public creators who published under their own
  names are the whole exception, public output only.
- Not used here: *proves, debunked, case closed, confirms it's fake, confirms it's real,
  hoax*. "AI-generated" is a hypothesis, not a conclusion.
