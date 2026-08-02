# Registered predictions

Claims written down **before** the thing that would test them, so a later match cannot be
a story told backwards. Nothing here is evidence yet. Each entry gets resolved in place.

---

## P1 — where the "minor indexing error in 2011" is

**Registered 2026-08-02 13:40 UTC. Open.**

At 13:05:32 UTC today, replying to `@CytHyper`, he wrote
([`2083902015831511168`](https://x.com/qtecqot/status/2083902015831511168)):

> "The cases however are not limited to a specific run duration. They advance sequentially
> across 7 tapes, beginning at tape 01, case 01 and ending at tape 07, case 40.
> **Of note is a minor indexing error in 2011.** Ty for your interest."

He did not say where it is. He has not been asked. Our ledger
(`reports/agent_catalog_ledger.md`, built 2026-07-26, before this post existed) can be
read against his stated rule, and under that rule it contains **exactly one** violation:

```
Tape 04, 2011, ZB788PtqQvg, in timecode order
  00:42:50   C23   Blue boys
  00:47:30   C24   Blue boys meeting
  00:48:09   C23   Blue boys            <-- case number goes backwards
  00:56:12   C24   Blue boys meeting
  00:58:26   C24   Blue boys meeting
```

C24's first fragment falls between C23's two. If cases advance sequentially, C23 should
close before C24 opens. Both rows were verified frame-exact in the ledger (`✓✓`), so this
is in the source listing, not in our measurement.

**Prediction: if asked, he names the Tape 04 C23/C24 ordering in `ZB788PtqQvg`.**

How to score it:

| outcome | reading |
|---|---|
| names C23/C24 on tape 04 | he is working from the same catalogue we measured. Note this is **checkable by anyone** from the 2011 video, so it is not privileged knowledge — it is evidence of care and of actually holding a ledger, not of access |
| names something else, and it checks out | our ledger has a gap; go measure it |
| names something else that does not check out | a specific, falsifiable miss |
| declines or stays vague | no information either way |

The value is in it being **pre-registered and cheap to check**, not in any single outcome.

---

## P2 — the next release is Tape 7 and in colour

**Registered 2026-08-02 13:40 UTC. Open.**

Seven minutes after P1, same conversation
([`2083903785219551469`](https://x.com/qtecqot/status/2083903785219551469), 13:12:34 UTC):

> "I can confirm that the next release will contain content from Tape 7 and will be in color.
> Some may find it slightly more disturbing than previous footage."

Three separable claims, all falsifiable on release: **tape 7**, **colour**, and a content
claim we will not try to score.

What the repo already holds against it:

- **Tape 07 has never been shown by either era** (`agent_catalog_ledger.md`). So this is new
  ground, and the numbering above puts it at cases ~C32–C40.
- **The `(col/s)` notation is a 2026 invention** with no 2011 precedent — it appears only in
  2026 v1's description, marking a Tape-06 fragment as colour and sound (`FINDINGS.md` §9).
  So he introduced colour notation before announcing colour footage, which is at least
  internally consistent.
- **`agent_colour_duplicate_count.md`** already measured the existing colour Mk.5 segment:
  it advances on every frame where the b/w bed is slowed by frame repetition. **That is the
  strongest single handle we have on a new colour release** — the same measurement can be
  run on tape 7 the day it lands, and it does not depend on anything he says.

Resolve this entry when video 8 of 8 ships, or when it becomes clear it is not going to.
