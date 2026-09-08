# qtecqot presence archive: September 8 audit and checks

The watcher held real evidence, but its Git activity overstated its usefulness.
At inspection, the live local timeline contained 54 entries and about 358 MB of X
media. The reviewed public timeline contained 42 entries and stopped at its August
15 review. Numerous later commits only changed observation timestamps. The YouTube
watcher recorded an August 25 upload but had never archived its description or video.

Continuous capture lives in `../new-skinny-bob-capture` on `local/capture`.
The local viewer is **http://127.0.0.1:8765/timeline/**. Public `main` and the static
website are reviewed publications, not live replicas of that private capture tree.

## Repair and verified coverage

- A September 8 full official X timeline enumeration returned **39 current items**.
  The local timeline retains **54 entries**, including deleted/recovered and manual
  entries. These totals describe different sets; neither demonstrates historical
  completeness.
- Delta enumeration previously stopped at one page, risking skipped posts after a
  backlog exceeding 100. It now drains every page, preserves each response as it
  arrives, and advances its cursor only after the run succeeds. Hourly full sweeps
  now re-enumerate the official timeline. The procedure follows X's documented
  [pagination behavior](https://docs.x.com/x-api/fundamentals/pagination).
- Media filenames previously depended on URL enumeration order. New manifests bind
  each URL to retrieval time, byte count and SHA-256; source bytes are verified before
  reuse. Edited media cannot silently inherit a different attachment's old filename.
  Direct and reply/quote-context attachments have separate ownership. Five historical
  source URLs returned 404 during the live sweep; transient failures remain retryable.
  Legacy bytes remain held but their old filenames alone cannot establish attribution.
- Profile responses, avatar/banner bytes and revisions are retained. Public following
  snapshots use the [official following endpoint](https://docs.x.com/x-api/users/get-following).
  Private likes and DMs are outside observable coverage.
- The viewer now exposes context, source links, archive freshness, YouTube descriptions,
  held video links and readable comment snapshots. Its public edition displays the
  review date and excludes new local context/YouTube records from implicit publication.
- **All four qtecqot YouTube watch pages/descriptions are now held.** The first three
  have their existing AVC corpus copies indexed and **1,334 comments** archived:
  612 for `l9RAhmPHM_A`, 352 for `Oqw96jCOP7A`, and 370 for `OpSTlDJWFFI`.
  These counts equal the extractor's reported counts in this run, but deleted or
  filtered comments remain outside that measurement. The fourth upload's media and
  comments are blocked by YouTube's age check. Existing exports and the local Chrome
  session were tested; a current age-verified login is required to complete that leg.

Raw API/page captures and comment authors stay in the local capture tree. No private
individual is identified in this report. Provenance of the footage remains undetermined.

## Research checks refreshed from the archive

| Lead | Current status | What would resolve the remaining question |
|---|---|---|
| August 22 announcement pointing to August 25 | A new upload was published August 25 at 03:14:43 UTC according to the channel RSS. The dated release happened. [X announcement](https://x.com/qtecqot/status/2090997307349315801), [upload](https://www.youtube.com/watch?v=bg1BmaF6AJA). | This scores release timing only; a creator controls their own schedule. |
| August 2 promise of Tape 7 and colour | The new description lists Tape 07, Cases 38 and 40. The catalogue portion matches the earlier claim. Colour in the full release remains unscored here because its bytes have not yet been downloaded. [Earlier post](https://x.com/qtecqot/status/2083903785219551469). | Download the actual fourth release, map its fragments, then measure colour and frame repetition on that source. Do not substitute an enhancement or teaser. |
| September 6 claim of a background mantis body part in “release #2” | A localized visual test has **not** been registered: no timestamp or region is supplied, and the release numbering needs disambiguation. [Post](https://x.com/qtecqot/status/2096497751463002292). | Specify the intended upload and region before inspection. Use raw AVC frames, neutral independent reads and graded positive controls before interpreting a negative search. |
| August 25 endorsement of an enhanced ship still | This is an endorsement of a derivative image. It does not turn the reconstruction into source detail. [Post](https://x.com/qtecqot/status/2092183709256696250). | Compare held original frames with the explicitly identified derivative; retain separate provenance. |
| Claimed minor catalogue error in the 2011 material | The earlier local worksheet predicted Tape 04's Case 23/24 ordering. The account's separate discussion about Case 28 belonging to Tape 05 concerns a different table correction; it does not automatically score that prediction. [Indexing post](https://x.com/qtecqot/status/2083902015831511168). | An explicit, identifiable correction to the 2011 catalogue, then a frame-level check against the original ledger. |
| New description's red-pill block | The 96-byte decoded payload and unsuccessful bounded cipher checks are already recorded in [the handle investigation](qtecqot-handle-2026-09-08.md). | A specified cipher, key derivation or independently constrained clue. More arbitrary guesses would not be a smoking gun. |
| Same-handle Gmail no longer bouncing | Reported to the investigation on September 8. No delivery-status message, sending date or observation interval was supplied. This is an unverified change in apparent delivery behavior, not an ownership link. No email was sent by this audit. | Compare the old nondelivery report with the newer sent-message timestamp and elapsed observation window. A reply or public linkage would be separate evidence of ownership. |
| Other online accounts | The archive records the uploader's claim of using Instagram, but no independently linked Instagram handle is configured. | Establish a public cross-link before attributing or monitoring a same-name account. |

## Validation

All 21 offline regression tests passed. The suite covers pagination/backlog and partial failure, semantic
revisions, media reordering and corruption, retryable failures, context attribution,
invalid mirror responses, RSS failure recovery, and local route confinement. Live
verification included full X enumeration/media retry, YouTube extraction, browser
rendering/search, local description routes, and the reviewed public-site build.
Raw captures and health files in the capture checkout provide the run-specific details.

Adding requested API fields during this repair generated record revisions even when
post text was unchanged. A record revision is not automatically an authored edit.
