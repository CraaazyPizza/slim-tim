# Pitfalls

The long version of [`AGENTS.md`](../AGENTS.md). Each of these is a mistake this project
actually made, usually confidently. Written for an AI working here, but the first section
is worth a human's time too — it is the reason the writeup hedges as much as it does.

---

## The five hallucinations

This footage sits in the worst possible regime for a vision model: low bitrate, subject
resolution of a few hundred pixels, measured point-spread width 5–6.6 px. Enough structure
to look interpretable, not enough to constrain the interpretation. What happened:

1. **Apollo 11 at ~95% confidence.** A model identified the four-frame insert at
   `OpSTlDJWFFI` 2971–2974 as a specific Apollo 11 frame. Wrong, withdrawn.
2. **A military UAP video at 99%.** A different model named a well-known piece of footage
   for the same insert. Also wrong. Note that these two confabulations *disagreed with each
   other* while both sounding certain.
3. **Mandarin numerals from silence.** Transcribed out of audio that contained no speech at
   all — synthetic babble plus projector noise.
4. **A five-pointed star that isn't there.** Produced purely by the question being leading.
   Asked neutrally, the same crop returns nothing.
5. **A typeface fitted without noticing a 1.3× horizontal stretch.** Gave a confidently
   wrong reading — one that two members of the public had already got right by eye.

The pattern in all five: **confidence was inversely related to correctness.** The most
emphatic answers were the wrong ones. That is why `AGENTS.md` says to distrust confidence
rather than calibrate against it.

The countermeasures, and why each exists:

- **Ask neutrally.** "Do you see a face here?" manufactures a face. The question is half
  the answer.
- **Ask twice in separate contexts.** Invented detail is not stable across sessions; real
  detail is. This is the cheapest test available and it caught several.
- **Offer the null explicitly.** "…or nothing identifiable" has to be on the table as a
  permitted answer or it will not be chosen. Models treat an open question as a demand for
  content.
- **Use unmodified frames.** Enhanced, stretched, averaged and annotated images are in this
  repo and labelled as such. Reasoning from those alone is how several claims died —
  enhancement turns noise into apparent structure, and the model cannot tell which it is
  looking at.

## Absence claims and detection floors

"I looked and saw nothing" is not a result. It is a statement about you, not the material.
A negative only carries information if you know what you *could* have seen.

The method: take a real frame, inject a synthetic version of the thing you are looking for
at graded amplitudes, and report the amplitude at which detection fails. That number is the
finding. The absence on its own is not.

The cautionary case, in full: five out of five candidate frames returned no five-pointed
star. Then a *real* star, 120 px across at 35 DN of contrast, was injected into an actual
frame — and an independent observer could not see it either. The null had no power. It was
reported as if it did.

The same discipline applies to audio. The measured speech floor is **−37.2 dBFS** on the
black-and-white bed and **−21.9 dBFS** on the colour segment. A voice 20 dB under the
projector is simply not recoverable, so "no speech" without that figure means nothing.

**And every floor here is pessimistic**, because they were measured on the thinner AV1 copy
in `videos/2026/` rather than the ~3× richer copy now in `videos/2026-avc/`. A floor from this repo is
an upper bound on how blind we were, not a property of the footage. See
[`CORPUS_QUALITY.md`](../CORPUS_QUALITY.md) — this is the single biggest caveat on the whole
record.

## Contaminating your own second opinion

`gemini` is noticeably the strongest of the three installed CLIs at actually looking at
these images, and getting a second opinion from a different model is part of the method
here — several findings were settled that way and several died that way.

But **running `gemini` from inside this repo poisons it.** The CLI injects
`GEMINI_CLI_IDE_WORKSPACE_PATH`, reads the surrounding documents, and returns our own
conclusions as though they were independent. It happened, and it was not subtle: one answer
opened *"Based on a factual analysis of the image and the surrounding workspace
documentation…"* and went on to cite our own audits back to us. Every vision result obtained
that way is void.

Clean room:

```bash
mkdir -p /tmp/vq && cp <frame>.png /tmp/vq/image_01.png   # neutral filename
cd /tmp/vq && env -u GEMINI_CLI_IDE_WORKSPACE_PATH -u GEMINI_CLI_IDE_SERVER_PORT \
  gemini --skip-trust -p "@image_01.png What do you see? If nothing is identifiable, say so."
```

Two separate traps in that one command:

- **Neutral filenames.** A crop called `case22_bearded_face.png` supplies the answer. Name
  them `image_01.png`.
- **The `-p` flag is required.** A bare positional path with no `-p` prints help and exits
  **0** — which looks exactly like success and returns no analysis.

## The decoder is part of the method

Two distinct effects, both measured:

- **Across ffmpeg versions:** 4.4.2 and 7.x decoding the same source produce PNGs differing
  by **16 bytes per frame** — a `cICP` colour-information chunk the newer build writes.
  Pixels identical, hashes not. So a hash mismatch across versions means nothing.
- **Across codecs:** AVC-decoded and AV1-decoded frames of the same content differ by up to
  **1 in 255**, mean 0.001.

That second one is not a nuisance, it is a result. Chasing it is how the fixed dark dots in
the corners of the black frames were identified as **AV1 tile-corner artefacts** rather than
a mark an author placed in the picture. With both copies of the videos now in the repo it is
a controlled test: exactly 2,048 marked pixels under AV1, **zero** under AVC, all inside the
two 32×32 blocks the tile grid predicts. Run
`analysis/corner-dots/controls/codec_control.py`.

One trap if you re-derive it by hand: plain `-pix_fmt gray` rescales limited-range luma onto
0–255, collapsing the Y=16 / Y=17 distinction the whole test depends on into 0 / 1. Force
full range in and out.

The corollary worth carrying: **pixel-level watermark hunting on YouTube re-encodes has to
control for codec behaviour.** At 1080p that means masking those two blocks before comparing
black frames at all. Not doing so produced a set of cross-era "constellation matches" — 88,
118 and 112 shared positions — that survived strict nulls at n≈200 and were entirely the
encoder's.

## Working in this codebase

- **`python3.12`**, not `python3`.
- `analysis/` is **one-off scripts, not a pipeline.** No Makefile, no DAG. Every script that
  reads a `.npy` is a pure consumer — none create their own arrays — so nothing reruns end to
  end. Paths are absolute for one machine. `analysis/README.md` explains the layout and the
  three different reasons a referenced file might be missing.
- The work went through **generations.** The Cyrillic analysis took four passes and only the
  last is correct. Before trusting an old figure, check that `FINDINGS.md` still cites it.
- **Never `nohup cmd &` inside a call that is already backgrounded.** It kills the child
  silently and the failure presents as the tool's fault. It isn't.
- `pkill -f '<pattern>'` **matches its own command line.** This killed a shell here and
  surfaced as an unexplained exit 144. Use a `pgrep` loop that excludes the current PID.

## Publishing anything

- **Build by inclusion, never by redaction.** A grep-based redaction pass on this repo
  missed an email address rendered *inside an image*, and later a screenshot containing a
  real full name in a comment-box placeholder — text search sees neither. If you are
  deciding what ships, enumerate what goes in. Never enumerate what comes out.
- **Never name a private individual.** Two public creators who published about this material
  under their own names may be named, public output only. Nobody else, including commenters,
  and including people accused of things in fifteen-year-old forum threads.
- **Check images, not just text**, for names, handles, avatars, browser tabs and
  notification text.
- Words that assert more than the evidence carries, and are not used here: *proves,
  debunked, case closed, confirms it's fake, confirms it's real, hoax*. "AI-generated" is a
  hypothesis here, not a conclusion.

## Verify before you pass something on

Agents and models in this project have overclaimed repeatedly. One case is worth the
warning on its own: a subagent reported a "correction" to a document that turned out to be
**already right**, and the correction was nearly propagated into the record.

Check a claim against the source before repeating it, and say plainly when you could not. If
you are wrong, say so in one line and fix it — no ceremony. The convention here is that
retractions stay visible with the reasoning intact. That is what `CORRECTIONS.md` is, and it
is the most credible thing in the repo.
