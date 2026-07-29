# The complete corpus — seven videos, verified

Two YouTube channels, seven uploads, fifteen years apart. This document tabulates every
video as a digital artifact: identifiers, exact timestamps, encoding, on-screen text, and
the burned-in catalog each one carries. It does not argue about what the footage shows —
that's covered elsewhere. Every field below was verified directly against the media files
(`ffprobe`, SHA-256, frame-by-frame decode) rather than taken on trust from metadata, and
every place where a source disagreed with the pixels, or where a number can drift (views,
comments), is flagged with its provenance and its capture date.

**The corpus:**

| # | Channel | Year | Video ID | Title |
|---|---|---|---|---|
| 1 | ivan0135 (`UCC5AjFfZHRvILhJfWw5UcDw`) | 2011 | `ZB788PtqQvg` | Disclosure leaked ufo alien case video confidential documents old footage |
| 2 | ivan0135 | 2011 | `RsQCXN4o4Ps` | alien grey  extraterrestrial zeta reticuli ufo leaked  footage |
| 3 | ivan0135 | 2011 | `Xju_CY5ZESA` | Ivan0135 about ALIEN and UFO documents |
| 4 | ivan0135 | 2011 | `a6TLGkrfNKI` | alien grey extraterrestrial zeta reticuli tape 06 - family vacation |
| 5 | qtecqot (`UCw1EA-KJud9OmMA5p7_MWgw`) | 2026 | `OpSTlDJWFFI` | Confidential leaked ufo-ebe footage continuation of disclosure |
| 6 | qtecqot | 2026 | `Oqw96jCOP7A` | ET crew recovery site D, survival of EBL Tim +2, skinny Bob |
| 7 | qtecqot | 2026 | `l9RAhmPHM_A` | interior walkthru and examination 8mm disclosure footage ufo |

Titles are copied verbatim, including double spaces and inconsistent capitalization present
in the source.

---

## 1. Master corpus table

### 1.1 Identity and timestamps

| Video ID | Channel | Published (UTC, exact) | Category | Category ID |
|---|---|---|---|---|
| `ZB788PtqQvg` | ivan0135 | **2011-04-14 02:04:26** | News & Politics | 25 |
| `RsQCXN4o4Ps` | ivan0135 | **2011-05-02 05:21:51** | News & Politics | 25 |
| `Xju_CY5ZESA` | ivan0135 | **2011-05-09 05:09:51** | News & Politics | 25 |
| `a6TLGkrfNKI` | ivan0135 | **2011-05-18 00:35:43** | News & Politics | 25 |
| `OpSTlDJWFFI` | qtecqot | **2026-05-25 09:39:42** | News & Politics | 25 |
| `Oqw96jCOP7A` | qtecqot | **2026-06-15 04:23:35** | News & Politics | 25 |
| `l9RAhmPHM_A` | qtecqot | **2026-07-24 09:14:05** | News & Politics | 25 |

All seven are catalogued identically: "News & Politics" (`categoryId 25`).

### 1.2 Duration, frames, frame rate — measured, not trusted

Every figure below comes from a full decode-count of the delivered video stream
(`ffprobe -count_frames`), cross-checked against the frame rate declared by the container.
**All seven agree exactly** — decode-counted frames divided by the container's declared fps
reproduces the file's own runtime to within ~0.02–0.04 s in every case (a small, fixed
positive offset present across all seven; see note below), so there is no fps disagreement
to report anywhere in this corpus.

| Video ID | Frames (decode-counted) | Frame rate (container) | Frame-exact duration | Container-reported duration | Δ |
|---|---|---|---|---|---|
| `ZB788PtqQvg` | 1,188 | 25/1 fps | 47.520 s | 47.541 s | +0.021 s |
| `RsQCXN4o4Ps` | 1,500 | 25/1 fps | 60.000 s | 60.021 s | +0.021 s |
| `Xju_CY5ZESA` | 2,598 | 25/1 fps | 103.920 s | 103.941 s | +0.021 s |
| `a6TLGkrfNKI` | 2,337 | 25/1 fps | 93.480 s | 93.501 s | +0.021 s |
| `OpSTlDJWFFI` | 2,998 | 30000/1001 (29.970 fps) | 100.033 s | 100.061 s | +0.028 s |
| `Oqw96jCOP7A` | 2,503 | 30000/1001 (29.970 fps) | 83.517 s | 83.541 s | +0.024 s |
| `l9RAhmPHM_A` | 4,395 | 30000/1001 (29.970 fps) | 146.647 s | 146.681 s | +0.035 s |

The container duration is consistently ~21–35 ms longer than frame-count × frame-length in
**every one of the seven files** — a fixed muxing artifact of this delivery pipeline, not a
per-video anomaly, and too small to represent a missing or extra frame.

### 1.3 Video stream

| Video ID | Resolution | Aspect ratio | Codec | Profile / level | Pixel format | Colour |
|---|---|---|---|---|---|---|
| `ZB788PtqQvg` | 1920×1080 † | 16:9 | AV1 | Main, level 8 (AV1 4.0) | yuv420p | bt709, tv range |
| `RsQCXN4o4Ps` | 1920×1080 † | 16:9 | AV1 | Main, level 8 (AV1 4.0) | yuv420p | bt709, tv range |
| `Xju_CY5ZESA` | 1920×1080 † | 16:9 | AV1 | Main, level 8 (AV1 4.0) | yuv420p | bt709, tv range |
| `a6TLGkrfNKI` | 640×480 | 4:3 | AV1 | Main, level 4 (AV1 3.0) | yuv420p | smpte170m primaries, bt709 transfer, tv range |
| `OpSTlDJWFFI` | 1920×1080 | 16:9 | AV1 | Main, level 8 (AV1 4.0) | yuv420p | bt709, tv range |
| `Oqw96jCOP7A` | 1920×1080 | 16:9 | AV1 | Main, level 8 (AV1 4.0) | yuv420p | bt709, tv range |
| `l9RAhmPHM_A` | 1920×1080 | 16:9 | AV1 | Main, level 8 (AV1 4.0) | yuv420p | bt709, tv range |

**† Flagged — provenance of the resolution figure.** Three of the four 2011 files
(`ZB788PtqQvg`, `RsQCXN4o4Ps`, `Xju_CY5ZESA`) are delivered today at 1920×1080 (yt-dlp
format `399+251`, i.e. YouTube's current AV1 1080p re-encode). This is the resolution of
the file **as currently served**, not necessarily the resolution of the original 2011
camera/upload — YouTube re-transcodes its back-catalogue over time, and 2011-era consumer
uploads were not commonly 1080p. The fourth 2011 file, `a6TLGkrfNKI`, is capped at 640×480
(format `397+251`) — the only member of the corpus where a sub-1080p ceiling is directly
observable, which is at least consistent with (though not proof of) a lower-resolution
original master. **The original camera/tape resolution of any 2011 video is not
established** from what is held here; only the current delivered-file resolution is a
verified fact. All three 2026 files were captured at the same `399+251` format ladder and
show no such ceiling.

`ZB788PtqQvg`'s `smpte170m`/`bt709` colour mismatch (primaries vs. transfer function) is
copied straight from the container as delivered; not adjusted here.

### 1.4 Audio stream and container

| Video ID | Audio codec | Sample rate | Channels | Container |
|---|---|---|---|---|
| `ZB788PtqQvg` | Opus | 48,000 Hz | 2 (stereo) | Matroska (`.mkv`) |
| `RsQCXN4o4Ps` | Opus | 48,000 Hz | 2 (stereo) | Matroska (`.mkv`) |
| `Xju_CY5ZESA` | Opus | 48,000 Hz | 2 (stereo) | Matroska (`.mkv`) |
| `a6TLGkrfNKI` | Opus | 48,000 Hz | 2 (stereo) | Matroska (`.mkv`) |
| `OpSTlDJWFFI` | Opus | 48,000 Hz | 2 (stereo) | Matroska (`.mkv`) |
| `Oqw96jCOP7A` | Opus | 48,000 Hz | 2 (stereo) | Matroska (`.mkv`) |
| `l9RAhmPHM_A` | Opus | 48,000 Hz | 2 (stereo) | Matroska (`.mkv`) |

All seven are identical on this axis: Opus/48 kHz/stereo audio muxed into Matroska. (The
four 2011 files' own metadata records their extraction format as `webm`/format-id
`399+251` or `397+251` — a labelling artifact of the download tool's merge step, not a
property of the file on disk, which is Matroska in all seven cases per direct container
inspection.)

### 1.5 File size and bitrate (measured from the file, not metadata)

| Video ID | File size | Overall bitrate (measured) | SHA-256 |
|---|---|---|---|
| `ZB788PtqQvg` | 2,908,146 B (2.77 MiB) | 489.4 kbps | `280acf4bf51eac40c6d4de92db99ddb4d58b046c6de8144a6c0b5da47a0f2d78` |
| `RsQCXN4o4Ps` | 2,767,153 B (2.64 MiB) | 368.8 kbps | `fc9e28d39249fed830996f902a2be5ad1522c281a89f8aa3da9826a9dfb331da` |
| `Xju_CY5ZESA` | 1,821,387 B (1.74 MiB) | 140.2 kbps | `1b4dff802c8d6e0a0ba2342e7f232cc07032db658f8718eb0a69d64647faf94e` |
| `a6TLGkrfNKI` | 631,655 B (601 KiB) | 54.0 kbps | `bc46cfea5ee37bc17608b02e11dd34cdb37619a8d32edaece0fb59ed5595b408` |
| `OpSTlDJWFFI` | 5,488,011 B (5.23 MiB) | 438.8 kbps | `9bc73d66971d32664acad7a5cc508c4ef3048cac05c14aaaaa079bcbdbdd82a4` |
| `Oqw96jCOP7A` | 4,576,802 B (4.36 MiB) | 438.3 kbps | `d9076cf9283a068e14e0bd4f109fa2ebb7c2c50d815fc703a5d71e967a955cfb` |
| `l9RAhmPHM_A` | 5,687,336 B (5.42 MiB) | 310.2 kbps | `65dfa3fd1c61f541151532c5703b3c7397043a3395b28d82d04c5fbdf40e7e80` |

SHA-256 is computed directly over the delivered `.mkv` file, pinning exactly the artifact
this whole document describes. Note that "file size" and "bitrate" here are measured from
disk/`ffprobe`, not read from `info.json` — the metadata's own `filesize` field is `null`
for all seven; it only ever populated an *approximate* size at fetch time (`filesize_approx`),
which is consistently a few hundred bytes to a few KB off the true size and is not quoted
here.

### 1.6 Language fields — a real, documented drift

The three 2026 videos were captured against the YouTube Data API, which exposes both
`defaultLanguage` and `defaultAudioLanguage`. All three carry `defaultLanguage: "en"`, but
**`defaultAudioLanguage` is not uniform**:

| Video ID | `defaultLanguage` | `defaultAudioLanguage` |
|---|---|---|
| `OpSTlDJWFFI` | en | **en** |
| `Oqw96jCOP7A` | en | **en-US** |
| `l9RAhmPHM_A` | en | **en** |

This is a genuine, small metadata inconsistency across three videos otherwise produced on
the same template — flagged as an observation, not an interpretation.

For the 2011 videos, the equivalent Data-API language fields were not captured in this
corpus; only the download tool's own `language` tag is available, and it is populated on
just one of the four (`ZB788PtqQvg: "en"`) and absent (not merely empty) on the other three.
**`defaultAudioLanguage` for the 2011 videos is not established** here.

### 1.7 Tags (verbatim, as delivered)

```text
ZB788PtqQvg:
ufo, crash accident, alien, extraterrestrial, life, et, zeta, reticuli, grey,
desclassified, top, secret, cosmic, sighting, leaked, disclosure, confidential,
autopsy, intelligence, service, rosswel, incident, new, mexico, South, Africa,
Kalahari, Desert, army, navy, air, force, defense, agency, department, abduction,
old, footage, 1947, space, aliens, flying, military, video, airplanes, interview

RsQCXN4o4Ps:
ufo, crash accident, alien, extraterrestrial, life, et, zeta, reticuli, grey,
desclassified, top, secret, cosmic, sighting, leaked, disclosure, confidential,
autopsy, intelligence, service, rosswel, incident, new, mexico, South, Africa,
Kalahari, Desert, army, navy, air, force, defense, agency, department, abduction,
old, footage, 1947, space, aliens, flying, military, video, airplanes, interview,
planet, earth, moon, exclusive, science, predator

Xju_CY5ZESA:
reply, Ivan0135, ufo, crash accident, alien, extraterrestrial, life, et, zeta,
reticuli, grey, desclassified, top, secret, cosmic, sighting, leaked, disclosure,
confidential, autopsy, intelligence, service, rosswel, incident, new, mexico,
South, Africa, Kalahari, Desert, army, navy, air, force, defense, agency,
department, abduction, old, footage, 1947, space, aliens, flying, military, video,
airplanes, interview, planet, earth, moon, exclusive, science, universe, outer,
galaxy

a6TLGkrfNKI:
ufo, crash accident, alien, extraterrestrial, life, et, zeta, reticuli, grey,
desclassified, top, secret, cosmic, sighting, leaked, disclosure, confidential,
autopsy, intelligence, service, rosswel, incident, new, mexico, South, Africa,
Kalahari, Desert, army, navy, air, force, defense, agency, department, abduction,
old, footage, 1947, space, aliens, flying, military, video, airplanes, interview,
planet, earth, moon, exclusive, science, predator, shuttle, universe, area, outer,
galaxy, invasion, astronomy, planets

OpSTlDJWFFI:
ufo, crash accident, alien, extraterrestrial, life, et, zeta, reticuli, grey, top,
secret, cosmic, sighting, leaked, disclosure, confidential, autopsy, intelligence,
service, incident, new, mexico, South, Africa, Kalahari, Desert, army, navy, air,
force, defense, agency, department, abduction, old, footage, 1947, space, aliens,
flying, military, video, airplanes, interview, declassified, roswell, ivan0135,
pentagon, kgb

Oqw96jCOP7A:
ufo, crash accident, alien, extraterrestrial, life, et, zeta, reticuli, grey, top,
secret, cosmic, sighting, leaked, disclosure, confidential, autopsy, intelligence,
service, incident, new, mexico, Desert, army, navy, air, force, defense, agency,
department, abduction, old, footage, 1947, space, aliens, flying, military, video,
airplanes, interview, planet, earth, moon, exclusive, science, predator, false
cape, crash

l9RAhmPHM_A:
reply, Ivan0135, ufo, crash accident, alien, extraterrestrial, life, et, zeta,
reticuli, grey, desclassified, top, secret, cosmic, sighting, leaked, disclosure,
confidential, autopsy, intelligence, service, rosswel, incident, new, abduction,
old, footage, 1947, space, aliens, flying, military, video, airplanes, interview,
planet, earth, moon, exclusive, science, universe, outer, galaxy
```

Misspellings (`desclassified`, `rosswel`) are in the source and reproduced as-is. Note the
2026 tags carry both a **corrected** spelling (`declassified`, `roswell` on `OpSTlDJWFFI`)
and, on the other two 2026 videos, the same misspellings the 2011 videos use
(`desclassified`, `rosswel`) — the corpus is not internally consistent on this point.

### 1.8 Thumbnail sets

All seven videos expose the standard YouTube thumbnail ladder (numbered `0`–`3`, `default`,
`mqdefault`, `hqdefault`, `sddefault`, `hq720`, plus `_webp` variants and storyboard `sqp=`
crops). The high-resolution `maxresdefault` (1920×1080) is **confirmed present** for five of
the seven:

| Video ID | `maxresdefault` (1920×1080) |
|---|---|
| `OpSTlDJWFFI` | present |
| `Oqw96jCOP7A` | present |
| `l9RAhmPHM_A` | present |
| `RsQCXN4o4Ps` | present |
| `Xju_CY5ZESA` | present |
| `ZB788PtqQvg` | **not confirmed** — listed with no returned dimensions |
| `a6TLGkrfNKI` | **not confirmed** — listed with no returned dimensions |

The two "not confirmed" cases are consistent with those uploads never having a 1080p-or-better
source to generate a maxres thumbnail from — notably including `a6TLGkrfNKI`, the one video
in the corpus whose delivered video resolution is itself capped at 640×480. This is
suggestive, not conclusive: a missing maxres record could also just be a stale thumbnail
cache.

### 1.9 View and comment counts — two captures, dated

Two full metadata captures exist for this corpus: **2026-07-26** (the original pull) and
**2026-07-29** (`comments/capture_2026-07-29/`, a dedicated fresh capture). Every count below
carries its capture date; treat the 07-29 column as current as of this document.

| Video ID | Views (07-26) | Views (07-29) | Comments (07-26) | Comments (07-29) | Likes (07-26) | Likes (07-29) |
|---|---|---|---|---|---|---|
| `ZB788PtqQvg` | 677,241 | **678,223** | 1,258 | **1,262** | 7,584 | 7,600 |
| `RsQCXN4o4Ps` | 1,485,704 | **1,487,236** | 5,126 | **5,134** | 16,408 | 16,451 |
| `Xju_CY5ZESA` | 346,184 | **346,779** | 867 | **867** | 4,597 | 4,611 |
| `a6TLGkrfNKI` | 702,381 | **703,136** | 2,152 | **2,153** | 8,719 | 8,734 |
| `OpSTlDJWFFI` | 2,260 | **4,271** | 16 | **29** | 81 | 182 |
| `Oqw96jCOP7A` | 2,379 | **4,578** | 13 | **52** | 80 | 181 |
| `l9RAhmPHM_A` | 6,153 | **10,720** | 40 | **96** | 149 | 294 |

The three qtecqot videos roughly doubled their view/comment/like counts in the three days
between captures; the four ivan0135 videos moved by well under 1%, consistent with a
fifteen-year-old, no-longer-promoted upload versus an actively circulating one.

### 1.10 Verbatim descriptions

Descriptions are quoted exactly as delivered, including all original spacing, punctuation
and grammar.

**`ZB788PtqQvg`:**
> Leaked air force ufo footage. Confidential. Classified document.1942-1969.
>
> Relevant information:
>
> The video contains a sample edited fragments of tapes 01, 03 and 04
>
> Tape duration: 180 min
> Total recorded duration: 1.260 min
>
> Tape 01:
> Case 07/Tin bird 00:08:41 - 00:08:47
> Tape 03:
> Case 15/Flying twin 00:27:11 - 00:27:13
> Case 15/Flying twin 00:27:34 - 00:27:39
> Tape 04:
> Case 23/Blue boys 00:42:50 - 00:42:51
> Case 23/Blue boys 00:48:09 - 00:48:16
> Case 24/Blue boys meeting 00:47:30 - 00:47:32
> Case 24/Blue boys meeting 00:56:12 - 00:56:14
> Case 24/Blue boys meeting 00:58:26 - 00:58:28

**`RsQCXN4o4Ps`:** description field is **empty** (verified empty in both the 2026-07-26 and
2026-07-29 captures). This video's entire catalog text exists only as on-screen title
cards — see §2.

**`Xju_CY5ZESA`:**
> Ivan0135:
>
> In  response to posts about the Documents:
>
> http://www.youtube.com/watch?v=RsQCXN4o4Ps&feature=channel_video_title
> http://www.youtube.com/watch?v=ZB788PtqQvg&feature=channel_video_title

(The double space in "In  response" is in the source.)

**`a6TLGkrfNKI`:**
> Tape 06
> Family vacation
>
> From the first contact in 1942, a series of diplomatic visits to discuss matters of mutual concern were planned.
>
> Under the treaty 23/04, these meetings would take place in secrecy, a limited number of special agents would escort visitors and they would only meet high ranking officers.
>
> According to the document 072 / E, at the meeting of 1961 there was an incident involving 3 subjects due to the violation of the agreement by the officers at the military base when they discovered that their arrival was been filmed with a hidden device without their consent.
>
> Under the treaty 23/04, the meetings would be confidential and filming or taking photographs would not be allowed.
>
> After the incident, the treaty was revised.

**`OpSTlDJWFFI`:**
> Leaked ufo/uap/ebe footage. Confidential. Classified documents.1942-1969.
>
> Relevant information:
>
> 0135 location and status unclear as of
> 2026/04/21.  Incapacitation presumed.
>
> Per provision with network, continuity
> releases are triggered.
>
> 7 video tapes with material recorded
> between 1942-1969.
>
> Material containing UFO incidents,
> recovery and study of extraterrestrial
> life forms.  Full disclosure pending.
>
> Source anonymity is maintained.
> Failsafe contract is preserved.
>
> The video contains sample edited fragments of tapes 02, 05, 06.
>
> Tape duration: 180 min
> Total recorded duration: 1.260 min
>
> Tape 02:
> Case 11/Tin bird unauth 00:33:30 - 00:33:34
> Case 12/Mk.4 taxi 01:08:21 - 01:08:22
> Case 12/Mk.4 pace lap 01:10:55 - 01:11:21
> Tape 05:
> Case 26/Tim's show &tell 01:01:18 - 01:01:19
> Tape 06:
> Case 31/Mk.5 virgin (col/s) 00:57:56 - 00:58:04

**`Oqw96jCOP7A`:**
> Relevant information:
>
> Continuation release 6 / 8.
>
> Source anonymity is maintained.
> Failsafe contract is preserved.
>
> The video contains sample edited fragments of tapes 02, 04, 05.
>
> Tape 02:
> Case 11/Tin bird primer 00:36:02 - 00:36:07
>
> Tape 04:
> Case 20/Brown boys 00:03:11 - 00:03:18
> Case 20/Brown boys 00:03:55 - 00:04:05
> Case 20/Brown boys 00:04:10 - 00:04:11
> Case 21/Triage 00:15:01 - 00:15:06
> Case 22/Exit EBL04 00:30:26 - 00:31:14
>
> Tape 05:
> Case 25/Bob's walkabout 00:02:07 - 00:02:12
> Case 25/Slim Tim 00:40:12 - 00:40:40

**`l9RAhmPHM_A`** — **this description was edited after initial capture**; both versions are
given. As of 2026-07-26:
> Relevant information:
>
> Continuation release 7 / 8.
>
> Source anonymity is maintained.
> Failsafe contract is preserved.
>
> The video contains sample edited fragments of tapes 03, 05.
>
> Tape 03:
> Case 18 / Mk.4 early boarding 02:13:18 ~ 02:23:57
>
> Tape 05:
> Case 28 / False Cape study 02:51:01 ~ 02:51:32

As of 2026-07-29, the same text with a block appended at the end:
> [… identical text as above, then:]
>
>
>
> Official venue for dissemination of facts and clarification of misinformation/misinterpretation.
>   - false claims of ownership/production
>   - false allegations re: intent or motive
>   - other dubious claims which fall within my limited range of authority to address
> https://x.com/qtecqot

This is the only one of the seven descriptions confirmed to have changed between captures.

---

## 2. The in-video text — verbatim, with frame numbers

Every card below was read directly from the delivered video frames (full decode, not
metadata, not a thumbnail sample), and frame ranges are measured from the actual file. Where
this corrects or sharpens an earlier reading based on lower-fidelity sources, that's flagged.

### 2.1 `OpSTlDJWFFI` (2026)

Three sequential title cards, monospaced white text on near-black, cross-dissolving into one
another, frames 1–882 (0.00–29.4 s of the file):

- **Card A**, f1–~310: *"0135 location and status unclear as of 2026/04/21. Incapacitation
  presumed. / Per provision with network, continuity releases are triggered. / 7 video tapes
  with material recorded between 1942-1969. / Material containing UFO incidents, recovery
  and study of extraterrestrial life forms. Full disclosure pending."*
- **Card B**, f~330–555: *"Source anonymity is maintained. / Failsafe contract is preserved."*
- **Card C**, f~570–882: the fragment list (identical to the description, §1.10, including
  the `&tell` typo).

Fade to black f883–917. Then a blank bright leader section f918–1044, inside which a
**translucent Cyrillic caption**, two lines, appears at f≈969–990 (≈32.3–33.0 s):
line 1 reads **«Предыдущее сообщение»** ("Previous message") in a modern sans-serif face,
not a period typeface. A second, smaller line sits beneath it; it is real ink (confirmed by
split-half correlation against blank controls) but **remains unread** — extensive
measurement narrows it to ≈22 characters ending in a run of three capital-height glyphs, with
several plausible endings tested and rejected, and none confirmed. **Flagged as contested:**
do not treat any specific reading of line 2 as established.

Footage (Case 11, "Tin bird unauth") begins at f1049.

### 2.2 `Oqw96jCOP7A` (2026)

One static title card, white monospace on black, **f11–389 (0.33–12.9 s)**, reproducing the
video's own description verbatim (§1.10) — the fragment table for tapes 02, 04, 05. Fades
f390–414, pure black f415–456, footage begins f457. No other text card exists in this file.

### 2.3 `l9RAhmPHM_A` (2026)

One static title card, **f11–393 (0.37–14.3 s)**, full brightness, fading f394–427, true
black f428–456. Read at full resolution:

```
The video contains sample edited
fragments of video tapes 03, 05.

Tape 03 edited fragments:
Case 18/Mk.4 early boarding 02:13:18 ~ 02:23:57

Tape 05 edited fragments:
Case 28/False Cape study 02:51:01 ~ 02:51:32
```

No other text card exists anywhere in the file, and there is no end card: frames 4255–4394
are a flat grey field, and f4395 alone is true black.

### 2.4 `ZB788PtqQvg` (2011)

One opening card, **f1–~125 (0.00–5.00 s)**: a sword-and-shield emblem (Soviet/KGB-style
crest) centred between two solid black bars above and below it. **No legible text is visible
in the bars in this copy** — they carry no ink at any contrast stretch. (An external source
match — not derived from this file's own pixels — has previously identified the crest as
lifted from the 1998 commercial documentary *The Secret KGB UFO Files*, whose own card reads
«СОВЕРШЕННО СЕКРЕТНО / АРХИВ КГБ»; that text is not present in our copy and should not be
quoted as if it were.) Footage (Case 07, "Tin bird") begins f133 (5.28 s). This is the only
title card in the file; the rest of its runtime is footage with no further text cards,
consistent with its catalog being carried entirely by the YouTube description (§1.10).

### 2.5 `RsQCXN4o4Ps` (2011)

Four sequential title cards, white monospace text over a faint blurred grayscale background,
measured directly from the file:

- **Card 1**, f51–201 (2.0–8.0 s): *"Filtrate for declassification and dissemination through
  the Internet and media. / 7 video tapes with material recorded between 1942-1969. /
  Material containing UFO incidents, recovery and study of extraterrestrial life forms."*
- **Card 2**, f246–336 (9.8–13.4 s): *"Due to the importance of these documents, maintain the
  anonymity of the sources."*
- **Card 3**, f366–476 (14.6–19.0 s): *"The video contains a sample edited fragments of video
  tape 05. / Tape duration: 180 min. / Total recorded duration: 1.260 min."*
- **Card 4**, f501–575 (20.0–23.0 s):
  ```
  Tape 05 edited fragments:
  Case 25/skinny Bob 00:08:42 - 00:08:50

  Case 25/skinny Bob 00:27:36 - 00:27:45

  Case 26/How to drive 00:55:07 - 00:55:12
  ```

True black f596–606 (23.8–24.2 s); footage (Case 25, first fragment) begins f611 (24.4 s).

**Correction to a widely repeated caveat.** An earlier reconstruction of this video's
on-screen text (done from third-party thumbnail captures rather than the primary file) could
only confirm the case *numbers* 25 and 26 on screen, and explicitly flagged the labels
"skinny Bob" and "How to drive" as fan-applied, not independently confirmed as on-screen
text. Read directly from the file, **Card 4 is plainly legible at ordinary contrast** — it is
sparse text on a black field, not faint or hidden — and it names both cases with exactly
those labels, in the same `Case NN/label HH:MM:SS - HH:MM:SS` format the 2026 videos later
adopt. The full names are on-screen text, not fan cataloguing.

### 2.6 `Xju_CY5ZESA` (2011)

This entire 103.9 s video is on-screen text over one static background image — a splayed
handprint pressed onto a light surface — held for essentially the whole runtime. **There is
no footage anywhere in this file.**

True black f1–121 (0.0–4.8 s), fading in f129–505 (5.2–20.2 s). During the fade, a header is
briefly legible (confirmed at f200, ≈8.0 s): *"Ivan0135: / In  response to posts about the
Documents:"* (double space as in the source). By f513 the fade completes onto the first full
page of reply text, and the following 13-paragraph statement is displayed across several
sequential cards (confirmed directly at f300, f700, f1500, f1700, f1900 and f2200) between
roughly f513 and f2400 (20.5–96 s), before fading to black f2409–2544 and holding black to the
end (f2598, 103.9 s):

> Ivan0135:
>
> In response to posts about the Documents:
>
> The material is an edited compilation of the documents that we have.
>
> Your opinion and the conclusion you draw from this material do not depend on us.
>
> Maybe you are looking in the wrong direction.
>
> You are the ones who reject this material.
>
> Sources will not be revealed.
>
> Information that may involve any agency or people will not be disclosed.
>
> There is not any reference which may link the material to any organization that is working today in the material exposed.
>
> However, you are speculating and making conjectures about its origins.
>
> The material does not belong to any film, video game, television series or other commercial products that have been revealed to date or which are currently in production.
>
> No one who is out of this may prove to be the owner of this material.
>
> No one who is out of this can prove he has in his possession the original material.
>
> The revelation of further material will depend on the events and people.
>
> You are the ones who create your own misinformation.

Every paragraph above was confirmed directly against the primary video frames; **the exact
frame boundary between each individual paragraph card was not resolved** (some transitions
are gradual dissolves rather than hard cuts) — only the outer envelope and several
intermediate anchor points are given with precision above. This does not affect the text
itself, which is fully confirmed.

### 2.7 `a6TLGkrfNKI` (2011)

Six sequential title cards over a persistent, heavily blurred grayscale background
photograph (reads as a blurred silhouette/portrait), interrupted once by the only actual
footage in the file:

- **Card 1**, f1–204 (0.0–8.2 s): *"Tape 06 / Family vacation"*
- **Card 2**, f211–477 (8.4–19.1 s): *"From the first contact in 1942, a series of diplomatic
  visits to discuss matters of mutual concern were planned."*
- **Card 3**, f554–806 (22.2–32.2 s): *"Under the treaty 23/04, these meetings would take
  place in secrecy, a limited number of special agents would escort visitors and they would
  only meet high ranking officers."*
- **Card 4**, f890–1268 (35.6–50.7 s) — the longest card: *"According to the document 072/E,
  at the meeting of 1961 there was an incident involving 3 subjects due to the violation of
  the agreement by the officers at the military base when they discovered that their arrival
  was been filmed with a hidden device without their consent."* ("was been filmed" is
  reproduced exactly as it appears on screen.)
- **Card 5**, f1359–1674 (54.4–67.0 s): *"Under the treaty 23/04, the meetings would be
  confidential and filming or taking photographs would not be allowed."*
- **[Footage, f1821–2045, 72.8–81.8 s]** — the only photographed-looking content anywhere in
  this file: pale, low-contrast, varying imagery, consistent with the "family vacation" label.
  **No burned-in timecode or case number appears anywhere in this shot**, nor anywhere else in
  the file.
- **Card 6**, f2059–2192 (82.4–87.7 s): *"After the incident, the treaty was revised."*

Fades to black by f2241 (89.6 s); true black to the end (f2337, 93.5 s). This video is the
only one in the corpus with no burned-in tape/case overlay anywhere, confirmed by direct
inspection at full stretch across the entire file.

---

## 3. The burned-in source-timecode ledger (2026 videos)

Each 2026 video carries an on-screen catalog naming tape, case, a short label, and a claimed
source-timecode span, matching its own description field exactly (§1.10, §2.1–2.3). Presented
here cleanly, without re-deriving or re-litigating the underlying provenance analysis.

### 3.1 `OpSTlDJWFFI` — separator: `-`

| Tape | Case | Label | Claimed span |
|---|---|---|---|
| 02 | 11 | Tin bird unauth | 00:33:30 – 00:33:34 |
| 02 | 12 | Mk.4 taxi | 01:08:21 – 01:08:22 |
| 02 | 12 | Mk.4 pace lap | 01:10:55 – 01:11:21 |
| 05 | 26 | Tim's show &tell | 01:01:18 – 01:01:19 |
| 06 | 31 | Mk.5 virgin (col/s) | 00:57:56 – 00:58:04 |

### 3.2 `Oqw96jCOP7A` — separator: `-`

| Tape | Case | Label | Claimed span |
|---|---|---|---|
| 02 | 11 | Tin bird primer | 00:36:02 – 00:36:07 |
| 04 | 20 | Brown boys | 00:03:11 – 00:03:18 |
| 04 | 20 | Brown boys | 00:03:55 – 00:04:05 |
| 04 | 20 | Brown boys | 00:04:10 – 00:04:11 |
| 04 | 21 | Triage | 00:15:01 – 00:15:06 |
| 04 | 22 | Exit EBL04 | 00:30:26 – 00:31:14 |
| 05 | 25 | Bob's walkabout | 00:02:07 – 00:02:12 |
| 05 | 25 | Slim Tim | 00:40:12 – 00:40:40 |

### 3.3 `l9RAhmPHM_A` — separator: `~`

| Tape | Case | Label | Claimed span |
|---|---|---|---|
| 03 | 18 | Mk.4 early boarding | 02:13:18 ~ 02:23:57 |
| 05 | 28 | False Cape study | 02:51:01 ~ 02:51:32 |

**On the separator switch.** The first two 2026 videos use `-` for every fragment; the third
switches to `~` for both of its fragments, and only there. This is a meaningful change, not a
typo: `l9RAhmPHM_A`'s Case 18 claims a 640-second span (02:13:18 to 02:23:57) but the case is
only actually on screen for a small fraction of that — consistent with `~` denoting a
*range that fragments were sampled from*, rather than one continuous clip, as `-` does. The
video's own on-screen card (§2.3) uses `~` in exactly the same two places as the description.

**Case-number reuse across eras.** Cases 25 and 26 (both Tape 05) appear in both the 2011 and
2026 catalogs — 2011's `RsQCXN4o4Ps` names Case 25 "skinny Bob" and Case 26 "How to drive"
(§2.5); 2026 renames the same two case numbers "Bob's walkabout"/"Slim Tim" (Case 25) and
"Tim's show &tell" (Case 26). No other case numbers are shared between the two eras. This
reuse-with-renaming pattern, along with the full cross-era timecode ledger and its
consistency checks, is catalogued in full in `reports/agent_catalog_ledger.md`; it is not
re-derived here.

---

## 4. Figures

Two figures for embedding, in `figs/corpus/`:

- **`timeline_2011_2026.png`** — all seven publish timestamps on two aligned mini-timelines
  (2011 / 2026), each video labelled with its ID, exact date, and duration.
- **`corpus_table.png`** — the seven-row spec table (ID, published, duration, decode-counted
  frames, fps, resolution, current view count) as a standalone image.

---

## 5. Summary of flagged/uncertain items

For a document meant to be lifted into a public post with minimal editing, everything above
is either a direct measurement or a verbatim quote. The following is the complete list of
places where provenance is genuinely uncertain, so none of it gets silently smoothed over:

1. **2011 delivered resolution.** Three of four 2011 files are served today at 1920×1080 AV1;
   this is YouTube's current re-encode, not a confirmed original camera/upload resolution.
2. **`OpSTlDJWFFI` Cyrillic line 2** (§2.1) — real ink, extensively measured, **not read**.
   Any specific transcription offered elsewhere should be treated as unconfirmed.
3. **`ZB788PtqQvg`'s crest text** — the specific phrase «СОВЕРШЕННО СЕКРЕТНО / АРХИВ КГБ»
   associated with this card in some secondary sources is not visible in our copy's pixels;
   it comes from an external match to a 1998 documentary, not from this file.
4. **2011 `defaultAudioLanguage`** — not established; the Data-API language fields available
   for the 2026 videos were never captured for the four 2011 uploads.
5. **`maxresdefault` thumbnails for `ZB788PtqQvg` and `a6TLGkrfNKI`** — listed with no
   confirmed dimensions; likely absent, not conclusively confirmed either way.
6. **`Xju_CY5ZESA` internal card boundaries** — the 13-paragraph text is fully confirmed
   verbatim; the exact frame at which each individual paragraph card dissolves into the next
   was not resolved past several confirmed anchor points.
7. **Original 2011 camera/tape resolution** — not established at all; only the resolution of
   the currently delivered file is known.

Everything else in this document — every timestamp, hash, frame count, description, on-screen
card, and timecode span — is a direct, reproducible measurement or verbatim quote from the
files as they exist now.
