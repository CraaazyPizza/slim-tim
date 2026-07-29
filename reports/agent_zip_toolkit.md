> **REDACTION NOTE (added by the coordinator, 2026-07-28).** This report is archived
> verbatim EXCEPT that a real personal name — the Office "registered user" string that
> LC inadvertently published inside their own toolkit ZIP, in the `~$....pptx` owner file —
> has been replaced with `[PERSONAL NAME REDACTED]` (2 occurrences). The name has zero
> investigative value: it concerns a third-party analyst assessed at ~95% independent of
> qtecqot, and it says nothing about the footage's provenance. It is recoverable from the
> original archive if it ever genuinely matters. It must never appear in anything public.

Analysis complete. Full report follows.

---

# Forensic report — LC's "toolkit" ZIP for qtecqot video 1 (`OpSTlDJWFFI`)

**Target:** `/home/user/new-skinny-bob/community/2026-05-25_Confidential leaked ufo-ebe footage continuation of disclosure.zip`
**Analysis date:** 2026-07-28. **Analyst artifacts:** `/home/user/new-skinny-bob/analysis/third-party-toolkit/`

**Status change during the run:** the file was still transferring when I began (397,410,304 B). It finished at **1,612,769,090 B** at 23:39 local and was stable for 5 consecutive 25 s polls. The completed archive has a valid end-of-central-directory record and passes `unzip -t` with no errors, so the "partial upload" caveat in the tasking **no longer applies** — everything below is measured on the complete archive.

- SHA-256: `82eafff2d8e5b6098ecf66ac61ce9cbdf45bf3a1bf594f0211fd9c9d5c1d4b3d`
- Compression method is **DEFLATE (8)**, not STORE as the tasking assumed (one exception, noted below). My carver handles both; it walks local file headers and never needs the central directory.

---

## 1. Archive structure and manifest summary

**3,351 local file headers: 3,329 files + 22 directory entries.** Uncompressed 1,692,547,957 B; compressed 1,611,551,974 B (95.2% — essentially no compression, since the payload is PNG/MP4/WAV). All entries CRC-verified: **3,329/3,329 OK**. Extracted to `/home/user/new-skinny-bob/analysis/third-party-toolkit/extracted/` (1.6 GB on disk); full manifest with every path, size, method, CRC and DOS stamp in `/home/user/new-skinny-bob/analysis/third-party-toolkit/manifest.json`.

By extension: 3,304 PNG, 14 MP4, 7 WAV, 2 TXT, 1 PDF, 1 PPTX-ownerfile.

### Directory scheme

```
2026-05-25_Confidential leaked ufo-ebe footage continuation of disclosure/
├── 00 - 01 - Intro/                                    916 frames   (f1–916)
├── 00 - 02 - Message/                                  132 frames   (f917–1048)
├── 01 - Tape 02 - Case 11 - Tin bird unauth/           212 frames   (f1049–1260)
├── 02 - Tape 02 - Case 12 - Mk.4 taxi/                  43 frames   (f1261–1303)
├── 03 - Tape 02 - Case 12 - Mk.4 pace lap/            1198 frames   (f1304–2501)
├── 04 - Tape 05 - Case 26 - Tim's show &tell/           69 frames   (f2502–2570)
├── 05 - Tape 06 - Case 31 - Mk.5 virgin (col_s)/       420 frames   (f2571–2990)
├── 06 - End - fill/                                      8 frames   (f2991–2998)
├── SOURCE/   ← LC's actual downloaded YouTube file (18,380,973 B MP4)
├── SPLIT/    ← 7 per-segment MP4 re-renders
├── TIME REFACTOR/ ← 6 de-duplicated / retimed MP4 re-renders
├── SOUND/    ← 1 full-length WAV + 6 segment/processed WAVs
├── EXTRACT/  ← 6 sub-folders, 284 files (all byte-identical duplicates of frames above)
├── BREAKOUT/ ← the 22-page PDF + 22 PNG slide exports
├── 2026-05-25_...disclosure.txt   (1,001 B — copy of the YouTube description)
├── 2026-05-25_info.txt            (574 B — the segment table, tab-separated)
└── ~$2026-05-25_...disclosure.pptx (165 B — Microsoft Office owner/lock file)
```

Frames are named globally `qtecqot01_NNNN.png`, 1-indexed, continuous 1…2998 across folder boundaries — **the folders are a partition of one flat extraction, not eight separate extractions.** The segmentation exactly matches the table printed on page 2 of LC's PDF and in `2026-05-25_info.txt`.

**ZIP writer fingerprint:** every entry has general-purpose flags `0x0000`, extra-field length `0`, no data descriptors, and no ZIP64. That combination (no `UT`/`NTFS`/`Zip64` extra fields at all) is characteristic of the **Windows Explorer built-in "Compressed (zipped) folder"** writer rather than 7-Zip or Info-ZIP, both of which normally emit timestamp extra fields. I treat this as suggestive, not proven. One entry — `SPLIT/03 - Tape 02 - Case 12 - Mk.4 pace lap.mp4` — is STORE rather than DEFLATE, which is the normal "incompressible, don't bother" fallback.

---

## 2. Timestamp / timezone analysis

### The offset is measured, not assumed

DOS stamps carry no timezone. But the archive contains its own calibration: `BREAKOUT/...disclosure.pdf` has a DOS local-header stamp of **2026-07-28 23:04:44**, and the PDF's own internal metadata declares `CreationDate(D:20260728230442+02'00')` and XMP `<xmp:CreateDate>2026-07-28T23:04:42+02:00`. Same wall-clock reading, two seconds apart, from two independent recorders. **The DOS stamps are therefore in a UTC+02:00 local clock**, and the given UTC anchor (PDF created 21:04:42 UTC) is confirmed.

### Distribution

Timestamps fall into five discrete work sessions, not a smear:

| Local (UTC+2) | UTC | Session content |
|---|---|---|
| **Jul 25, 00:55:10** | Jul 24, 22:55:10 | `SOURCE/...(1080p).mp4` written — the download |
| **Jul 25, 01:06:20 – 01:06:42** | Jul 24, 23:06:20–23:06:42 | **All 2,998 PNG frames**, one continuous 22-second burst |
| **Jul 26, 18:41:04** | Jul 26, 16:41:04 | the description `.txt` |
| **Jul 27, 15:29:00 – 15:32:22** | Jul 27, 13:29:00–13:32:22 | 6 TIME REFACTOR MP4s, then 5 SPLIT MP4s |
| **Jul 27, 15:41:44 – 15:54:40** | Jul 27, 13:41:44–13:54:40 | full WAV, then segment WAV, then 5 processed variants |
| **Jul 28, 12:45:36 – 12:45:42** | Jul 28, 10:45:36–10:45:42 | SPLIT Intro + Message re-rendered |
| **Jul 28, 23:03:02 – 23:21:30** | Jul 28, 21:03:02–21:21:30 | PPTX open → PDF export → 22 slide PNGs → folders → ZIP |

Within the frame burst the per-2-second bucket counts are 207, 271, 368, 318, 296, 397, 251, 252, 239, 247, 298, 138 — a continuous write at **≈130 files/s**, strictly monotonic in frame number across all eight folders.

### What that implies about workflow

The 2,998 frame files carry Jul 25 01:06 mtimes while their **containing folders** carry Jul 28 23:10 mtimes. On Windows, a same-volume move preserves file mtime and sets the destination folder's mtime to the move time. So: LC extracted all 2,998 frames into one flat directory on Jul 25, and **sorted them into the eight segment folders on Jul 28 at 23:10**, minutes before zipping. The `EXTRACT/` sub-folders behave the same way — their 284 files retain Jul 25 mtimes and are byte-identical duplicates, i.e. copies, not crops.

Key deltas:

| From → to | Elapsed |
|---|---|
| Video published (2026-05-25 09:39:42 UTC) → LC downloads source | **60 d 13:15:28** |
| Download → frame extraction begins | **11 min 10 s** |
| Frames → PDF export | 3 d 21:58:22 |
| PDF export → ZIP root folder stamp | 16 min 48 s |

### Timezone / location

**Measured:** machine clock at UTC+02:00 on 2026-07-28. PDF `Producer`/`Creator` = `Microsoft® PowerPoint® pour Microsoft 365` (French-localized UI); all 22 slide `/Title` entries read `Diapositive N`. PDF `/Author` = `LC`. The Office owner file `~$...pptx` contains the registered Office user name **`[PERSONAL NAME REDACTED]`** (offset 0x00: length byte `0x10`, then the ANSI string; repeated as UTF-16 at 0x33).

**Inference (stated as inference):** UTC+2 in late July is CEST — continental Western/Central Europe — or one of the year-round UTC+2 zones. Combined with a French-language Office install, the French administrative `SURNAME Firstname` capitalisation, and heavy francophone calquing in the PDF's English ("**argentic** film" ← *film argentique*, "shooted from a Chinook", "there is two other sequences", "Sovietic", "the maintain of anonymity"), the strong reading is a **French-speaking user in a CEST country (France most likely)**. The initials match the self-applied "LC" byline in reverse order.

*Caveat:* an Office user name is self-declared and trivially editable; it is evidence about the machine's configuration, not verified identity. It appears here only because LC published it themselves inside their own public archive. I could not determine the timezone from working-hours patterns alone — sessions at local 00:55, 18:41, 15:29, 12:45 and 23:03 are consistent with UTC+2 but would also be consistent with several other offsets; the +02:00 declaration is the actual evidence.

**No timestamp in the archive predates 2026-07-24 22:55:10 UTC.** Nothing in it is contemporaneous with the video's May publication.

---

## 3. Frame source comparison — the central question

### Answer

**LC's frames come from the same public YouTube upload we analysed, decoded from a *different YouTube rendition*: YouTube's 1080p H.264/AVC stream (itag 137) plus AAC audio (itag 140). Ours came from the AV1 stream (itag 399) plus Opus. This is not different source material, not a higher-quality master, and not a pre-YouTube file.**

The question is settled by direct evidence rather than inference, because **LC shipped their own download in the archive.**

### The decisive test

`SOURCE/Confidential leaked ufo-ebe footage continuation of disclosure (1080p).mp4`, 18,380,973 B:

```
video: h264, High profile, avc1, 1920x1080, yuv420p, level 40,
       30000/1001 fps, nb_frames=2998, bit_rate=1,334,303
audio: aac LC, 44100 Hz, stereo, bit_rate=127,999
tags : handler_name = "ISO Media file produced by Google Inc."  (both streams)
       encoder = Lavf58.27.103      (muxed by libavformat 58.27 = FFmpeg 4.2)
```

Compare `OpSTlDJWFFI.info.json`: itag 137 = 1920×1080 avc1, tbr 1337.425, 16,723,334 B; itag 140 = m4a AAC, abr 129.54, asr 44100, 1,620,894 B. Sum = 18,344,228 B; LC's muxed file is 18,380,973 B (36,745 B of container overhead). Exact match. LC's PDF independently states "Sound: yes - 128 Kbits/s - 44.1kHz - Stereo" — Opus, which is what the AV1/WebM route delivers, is 48 kHz and would never read 44.1.

I then decoded LC's own MP4 with ffmpeg 4.4.2 and compared to LC's shipped PNGs:

> **LC's decoded pixels are identical to my re-decode of LC's SOURCE.mp4 for 2,998 / 2,998 frames. Zero mismatches.**

The provenance chain is closed end to end: *YouTube upload `OpSTlDJWFFI` → itag 137 + 140 → LC's `SOURCE.mp4` → ffmpeg PNG extraction → LC's 2,998 frames.*

### LC vs. our AV1 extraction — the numbers

Alignment first. A pixel-hash offset sweep over −5…+5 found **no** identical frames at any offset (my first pass's "offset −5" was a tie-break artifact of an all-zero hit table, not a result). An RMS-minimising sweep over −40…+40 gives **offset = 0**: LC's frame *N* is our frame *N*.

Full-set comparison, all 2,998 frames, LC[n] vs ours[n]:

| Metric | Result |
|---|---|
| PNG files byte-identical | **0 / 2998** |
| Decoded images pixel-identical | **0 / 2998** |
| max abs diff — min / p25 / median / p75 / p95 / max | 1 / 19 / 23 / 36 / 65 / **91** |
| frames with maxabs ≤ 2 / ≤ 8 / ≤ 32 / ≤ 64 | 24 / 46 / 2089 / 2803 |

Per-frame difference statistics on a 512-frame sample spread across the whole video (every 5th frame, n = 1…2561):

| Statistic | min | p5 | p25 | median | p75 | p95 | max |
|---|---|---|---|---|---|---|---|
| RMS | 0.0314 | 0.5747 | 1.2211 | **1.9303** | 2.1010 | 2.2210 | **2.7253** |
| mean abs diff | 0.0010 | 0.0911 | 0.4426 | 1.3560 | 1.4876 | 1.5883 | 1.8886 |
| % pixels differing | 0.099 | 4.119 | 24.867 | 68.050 | 70.723 | 73.099 | 78.313 |
| % with abs diff > 8 | 0.0000 | 0.0205 | 0.0634 | 0.1309 | 0.2157 | 0.5893 | 3.0302 |
| % with abs diff > 16 | 0.0000 | 0.0000 | 0.0002 | 0.0008 | 0.0045 | 0.0799 | 0.3745 |

Global signed-difference histogram over 3.185 G pixel-channels:

| \|d\| | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | ≥40 |
|---|---|---|---|---|---|---|---|---|---|---|
| share | 49.54% | 22.57% | 15.87% | 5.85% | 3.32% | 1.48% | 0.68% | 0.34% | 0.15% | 0.000044% |
| cumulative | 49.5% | 72.1% | 88.0% | 93.8% | 97.2% | 98.6% | 99.3% | 99.7% | 99.8% | — |

Mean **signed** difference (LC − ours) = **+0.0346**; P(d>0) = 25.64%, P(d<0) = 24.82%. The difference is symmetric and essentially zero-mean — there is no gain, gamma, level-range or colour-matrix offset between the two sets. 99.8% of all pixel-channels agree within ±8.

### Scale reference — how small "RMS 2" is

| frame | LC[n] vs ours[n] | ours[n] vs ours[n+1] | LC[n] vs ours[n+15] |
|---|---|---|---|
| 400 | 1.444 | 0.301 | 4.507 |
| 1100 | 1.973 | 1.371 | 11.702 |
| 1400 | 2.043 | 6.635 | 31.867 |
| 1700 | 1.981 | 14.934 | 22.103 |
| 2000 | 1.976 | 3.331 | 30.862 |
| 2300 | 1.828 | 2.101 | 14.019 |
| 2500 | 2.590 | 2.351 | 59.423 |

At f1700 two *genuinely adjacent* frames of the same video differ 7.5× more than LC's frame differs from ours. At f2500 the same-index agreement is 23× tighter than a 15-frame displacement. Same content, same timeline, same frame indices.

### Ruling out the alternatives

**(a) Not the AV1 stream — a binary discriminator.** FINDINGS §13 established that YouTube's 1080p AV1 encode writes exactly 2,048 pixels at Y=17 on otherwise-flat black frames, in two solid 32×32 blocks at (0,0) and (960,0) — the first superblock of each of the two AV1 tile columns. Across **all 16 strictly-black frame pairs** in the video (f1–10, f911–916):

- ours: tile blocks entirely ==1 (artifact present) — **16/16**
- LC: tile blocks entirely ==0 (artifact absent) — **16/16**
- and the *entire* frame difference is confined to those 2,048 pixels — **15/16** (f10 has 13 extra pixels from a faint fade tail)

LC's black frames are perfectly flat: all 6,220,800 values are 0. Our two control transcodes (libx264 and libvpx-vp9 re-encoded *from* our AV1 decode) both inherit the 6,144 nonzero values, which confirms the test detects the artifact rather than the codec.

**(b) Not a pre-YouTube master.** Three independent measurements:

*Block-grid signature.* Exclusive boundary strength (mean |∂x| at columns that are multiples of *p* but not of 2*p*, normalised to non-multiples-of-4), averaged over 9 frames:

| source | ×4 | ×8 | ×16 | ×32 | ×64 | ×128 |
|---|---|---|---|---|---|---|
| **LC** | 0.899 | 1.433 | **2.843** | 2.715 | 2.877 | 2.919 |
| ours (YouTube AV1) | 0.997 | 1.024 | 1.108 | 1.672 | 2.396 | 2.287 |
| ctrl libx264 | 0.972 | 1.415 | 1.887 | 2.202 | 2.951 | 2.975 |
| ctrl libvpx-vp9 | 1.022 | 0.993 | 0.986 | 1.524 | 1.998 | 2.212 |

LC's profile jumps at 16 and then **plateaus flat out to 128** — every multiple of 16 is equally discontinuous. That is a uniform 16×16 macroblock grid, i.e. H.264. Ours rises monotonically to 128 (AV1 superblocks); VP9 shows almost no 16-px grid at all. A master would carry no such grid.

*The difference image carries LC's grid, not ours.* Exclusive profile of |LC − ours|:

| frame | ×4 | ×8 | ×16 | ×32 | ×64 | ×128 |
|---|---|---|---|---|---|---|
| 1000 | 1.041 | 1.821 | 3.600 | 3.756 | 4.499 | 5.055 |
| 1100 | 0.978 | 1.390 | 3.773 | 4.012 | 4.216 | 4.459 |
| 1200 | 0.981 | 1.431 | 4.008 | 4.075 | 4.779 | 4.658 |
| 1400 | 0.979 | 1.489 | 3.850 | 4.007 | 4.466 | 4.326 |

If LC held a master and ours were YouTube's encode of it, the residual would carry *AV1's* structure (weak at 16, peaking at 64/128). Instead the residual is dominated by a 16-px grid absent from our frames — contributed by LC's own encoder.

*Detail level.* Laplacian variance, LC ÷ ours, across 10 frames: 0.989, 0.995, 0.995, 0.994, 0.973, 0.904, 0.858, 0.902, 0.902 — LC is **smoother in 9 of 10** (the exception, f1300, is a near-flat frame at the noise floor). A higher-quality master would be *sharper*, not softer.

**(c) Not a rescale from a lower resolution.** Both sets are exactly 1920×1080; blocking appears at exactly 4/8/16 (integer, not the 24-px grid a 720p→1080p upscale would produce); detail ratio ≈0.99 rather than the large drop an upscale imposes.

**(d) The residual behaves like codec noise, not content difference.** corr(|LC − ours|, local image activity) = +0.85 / +0.45 / +0.43 / +0.42 at f400/1000/1200/1400, with essentially zero difference in flat regions. Both files are lossy siblings of one common master; the disagreement lives exactly where quantisation error lives.

### Corroboration for FINDINGS §2c

The hidden 4-frame insert at f2971–2974 is present in LC's AVC-derived frames with the same blue cast (channel means R 28.3 / G 34.4 / B 49.5 at f2971 rising to 32.2 / 38.5 / 54.6 at f2973–74, against a ~8.3 grey neighbourhood). Since this now reproduces through a completely independent codec path, **the insert is content in the upload, not an AV1 decode artifact.** LC filed those frames inside segment 05 and never mentions them in the PDF — LC did not notice the insert. LC's `06 - End - fill` (f2991–2998) is genuinely eight frames of pure black (all values 0), correctly labelled.

---

## 4. PNG / tooling forensics

All 3,304 frame PNGs: **1920×1080, bit depth 8, colour type 2 (truecolour RGB), compression 0, filter 0, non-interlaced.** No `tEXt`, `iTXt`, `zTXt`, `tIME`, `iCCP` or `sBIT` chunks anywhere — no embedded authoring metadata of any kind.

Chunk order, LC vs ours:

```
LC   : IHDR + pHYs + cICP + cHRM + gAMA + IDAT×N + IEND
ours : IHDR + pHYs +        cHRM + gAMA + IDAT×N + IEND
```

`pHYs` = 1×1 px/unit, unit 0 (unspecified); `cHRM` and `gAMA` = the bt709/sRGB values ffmpeg writes when tagging from bt709 source; `cICP` = `[1, 1, 0, 1]`. **IDAT chunks are exactly 4096 bytes each** — the hard-coded chunk size of libavcodec's PNG encoder, and the single strongest tool signature here. Photoshop, VirtualDub, ImageMagick and libpng-default writers all chunk differently.

**Identification: both sets were produced by ffmpeg's PNG encoder at default settings.** The tightest demonstration: for frame 500, LC's PNG and my own ffmpeg-4.4.2 re-encode from LC's MP4 have **identical IDAT chunk count (43) and identical total IDAT bytes (175,400)** — the zlib streams are byte-for-byte the same. The files differ by exactly 16 bytes (176,058 vs 176,042), which is precisely one `cICP` chunk (4 length + 4 type + 4 payload + 4 CRC). LC's ffmpeg is therefore a **newer build that emits `cICP`** (PNG cICP writing is a recent FFmpeg addition, 7.x era); mine at 4.4.2 does not. That is the *only* structural difference between LC's frame files and a stock ffmpeg extraction.

Note the version tension worth recording: LC's *muxer* stamped `Lavf58.27.103` (FFmpeg 4.2) into `SOURCE.mp4`, while LC's *PNG encoder* emits `cICP` (FFmpeg 7.x). Most likely the MP4 was muxed by a downloader bundling its own old ffmpeg (yt-dlp/youtube-dl ship or call one), and the frame extraction was done with a separately installed modern ffmpeg. I could not determine the downloader's identity.

The 22 `BREAKOUT/*.PNG` files are different: **1280×720**, chunk order `IHDR + sRGB + gAMA + pHYs + IDAT + IEND`, `pHYs` = 3780 px/m (96 DPI), non-4096 IDAT chunking. That is a **PowerPoint "Save as Picture / Export slides" output** — the 22 slides of the PDF exported as images.

---

## 5. Non-frame contents

### `SOURCE/` — the single highest-value item

LC's actual downloaded YouTube file (specs in §3). This is what makes the provenance question answerable rather than merely inferable. Its DOS stamp (2026-07-24 22:55:10 UTC) is the earliest timestamp in the archive.

### `SOUND/` — 7 WAVs

`Confidential leaked ufo-ebe footage continuation of disclosure (1080p).wav` — 35,297,656 B, **pcm_f32le, 44100 Hz, stereo, 100.0333 s** (4,411,467 samples). Note 44.1 kHz float, matching the AAC track, not our 48 kHz Opus.

*Is it processed?* Against my own decode of `SOURCE.mp4`'s AAC track: best lag **−1024 samples** (23.2 ms — standard AAC priming-delay handling difference), optimal scalar gain **0.999974 (−0.0002 dB)**, Pearson **r = 0.99997379**, residual RMS 0.72% of signal. LC's peak is 0.999969 where my decode reaches 1.011886 — i.e. **hard-clipped to ±1.0 on export, otherwise unprocessed.** It is a straight decode.

*Against our Opus track* (resampled to 44.1 kHz): best lag +576 samples (+13.06 ms), r = 0.713 after lag correction. Consistent with two different lossy codecs of one master plus a resample — same content, as expected.

`SOUND/05 - Tape 06 - Case 31 - Mk.5 virgin/` — six files, all 11.8169 s (521,126 samples):

- `05 - Tape 06 - Case 31 - Mk.5 virgin.wav` (pcm_f32le) — cross-correlation places it at **sample 3,778,891 = 85.6891 s = video frames 2568–2922**, with **r = 1.000000, max|diff| = 0, 521,126/521,126 samples bit-identical**. A bit-exact cut from the full WAV. (Note the audio cut 2568–2922 does not match LC's own video segment bounds 2571–2990 — LC cut by ear.)
- `A_voice.wav`, `B_radio.wav`, `C_highpass.wav`, `D_lowpass.wav`, `voice_filtered.wav` — all **pcm_s32le** (different sample format from the f32 parent, so a different tool), all normalised to **exactly peak 0.988553 (−0.10 dBFS) with exactly 1 clipped sample each** — the signature of a normaliser targeting −0.1 dBFS.

Octave-band energy relative to the raw cut (dB):

| file | 0–150 | 150–300 | 300–600 | 600–1.2k | 1.2–2.4k | 2.4–4.8k | 4.8–9.6k | 9.6–22k |
|---|---|---|---|---|---|---|---|---|
| A_voice | −7.08 | +0.32 | +3.13 | +4.11 | +3.30 | +1.24 | −2.91 | −7.27 |
| B_radio | −10.07 | −1.89 | +2.16 | +4.14 | +3.61 | +1.35 | −3.07 | −7.54 |
| C_highpass | −17.27 | −8.60 | −3.28 | +0.80 | +3.36 | +4.14 | +4.43 | +4.51 |
| D_lowpass | +2.05 | +1.99 | +1.78 | +1.07 | −1.21 | −4.42 | −9.41 | −14.06 |
| voice_filtered | −12.40 | −5.00 | −2.19 | −1.21 | −2.02 | −4.08 | −8.23 | −12.59 |

These are **simple EQ / band filters, not AI stem separation** — smooth monotone spectral tilts with no phase or transient restructuring. Two exact relationships: `voice_filtered = A_voice × 0.54199537` (residual RMS 3.25e-09, **r = 1.000000000** — a pure level change, despite the different name), and `B_radio ≈ A_voice × 0.848` with r = 0.977 (a related but genuinely distinct EQ). So the five "variants" are really **three** distinct filter results.

### `SPLIT/` and `TIME REFACTOR/` — 14 MP4s, all LC re-renders

`SPLIT/` = the seven segments cut out losslessly-in-timeline but **re-encoded** (H.264 at 2.6–10.0 Mbps, audio AAC resampled to 48 kHz at ~317 kbps — both far above the 1.33 Mbps / 128 kbps source). Frame counts match the segment table exactly (916, 132, 212, 43, 1198, 69, 420).

`TIME REFACTOR/` is the most interesting non-frame item. Frame counts are reduced:

| segment | SPLIT frames | TR frames | ratio |
|---|---|---|---|
| 01 Tin bird unauth | 212 | 139 | 0.6557 |
| 02 Mk.4 taxi | 43 | 28 | 0.6512 |
| 03 Mk.4 pace lap | 1198 | 793 | 0.6619 |
| 04 Tim's show &tell | 69 | 49 | 0.7101 |
| 05 Mk.5 virgin (col/s) | 420 | 280 | 0.6667 |
| **full TR** | — | **1289** | = 139+28+793+49+280 exactly |

LC de-duplicated the held frames to recover the underlying cadence, landing on ratios clustered around **≈2/3**. This is an independent reconstruction of the same phenomenon recorded in FINDINGS §11 ("about 2/3 speed"; 0.6515× for the b/w fragments, 0.6735× for the colour Mk.5 clip). LC's per-segment numbers (0.651–0.662 for the b/w clips, 0.6667 for the colour clip) are close to ours but not identical, and LC's full TR concatenation **omits the Intro, Message and End-fill** segments — it is a footage-only cut.

### `EXTRACT/` — 284 files, zero new content

Six thematic sub-folders (`FRAMES`, `Human face…`, `Letter01…`, `Letter02…`, `Message…`, `Military…`). Every one of the 284 files is **byte-identical (SHA-256) to a frame already present in the main segment folders**; 0 differing, 0 not-in-main. These are LC's selection copies for the PDF, not crops or enhancements.

### `BREAKOUT/` — the PDF plus 22 slide PNGs

PDF metadata: Creator/Producer `Microsoft® PowerPoint® pour Microsoft 365`, Author `LC`, CreationDate = ModDate = `2026-07-28T23:04:42+02:00`, DocumentID `uuid:E5B2C069-A006-493C-9CC5-26462A017507`.

### Unexpected items worth flagging prominently

1. **`SOURCE/…mp4` — LC shipped their own download.** Almost certainly unintentional from a forensic standpoint, and it is what converts the central question from an inference into a measurement.
2. **`~$2026-05-25_….pptx`** — a Microsoft Office owner/lock file, 165 B, left behind because the PowerPoint deck was still open when LC zipped the folder (its stamp, 21:03:02 UTC, is 100 s before the PDF export). It contains the Office registered user name **`[PERSONAL NAME REDACTED]`**. This is personal information; it is in the archive because LC published it, and I report it because it is materially probative of the timezone/locale conclusion. It is self-declared configuration data, not verified identity. The source `.pptx` itself is **not** in the archive.
3. The PDF's analytical passages credit **"Google Gemini 3.1pro/3.6"** for the Russian transcription and translation work — LC's readings of the in-frame Cyrillic are AI output, not independent linguistic analysis.

---

## 6. What this tells us, and what it does not

### Established by measurement

1. **LC's frames are not a new source.** All 2,998 are pixel-identical to a stock ffmpeg decode of LC's own shipped `SOURCE.mp4`, which is YouTube's itag 137 (H.264 1080p) + itag 140 (AAC 128k/44.1k) for `OpSTlDJWFFI`, muxed by Lavf58.27.103, Google handler tags intact. There is no pre-YouTube material, no master, no alternate cut, no extra frames, no missing frames anywhere in this archive.
2. **The 0/2998 non-identity against our extraction is fully explained by codec choice.** Median RMS 1.93, max 2.73; 99.8% of pixel-channels within ±8; zero-mean symmetric residual; alignment exactly offset 0. The AV1 tile-corner artifact is present in 16/16 of our black frames and absent in 16/16 of LC's, and on those frames the difference is *exactly* the 2,048 artifact pixels. The residual carries a 16-px macroblock grid that exists in LC's frames and not in ours. Every one of these points to "sibling YouTube renditions", and each independently contradicts "master".
3. **LC's work post-dates the video by two months** and is entirely derivative of the public upload. The earliest artifact in the archive is the download at 2026-07-24 22:55:10 UTC — 60 days after publication.
4. **The machine clock is UTC+02:00**, calibrated against the PDF's own declared offset with a 2-second cross-check, not assumed.
5. **The audio is unprocessed** at the toolkit level: the full WAV is a straight decode (r = 0.99997) and the segment cut is bit-exact. Only the five small variants are filtered, and two of the five are the same file at different gain.
6. **The 4-frame hidden insert (FINDINGS §2c) reproduces through an independent codec path**, which retires any residual worry that it was an AV1 decode artifact.
7. **LC's ≈2/3 retiming reconstruction independently converges with FINDINGS §11**, from a different toolchain and without contact.

### What this does not tell us

- **Nothing about the footage's provenance.** This archive is a downstream derivative work. It contains zero information about where qtecqot's material came from, and it cannot — every byte in it descends from the same public upload we already had.
- **It does not corroborate or undermine qtecqot.** LC is a third-party analyst, not a source. Their conclusions in the PDF (Chinook reflection, Soviet shoulder boards, Cyrillic readings) rest on the same 2,998 frames we hold, several of them mediated through Gemini. They should be evaluated on their own merits, not credited as independent evidence.
- **I could not determine LC's downloader.** The Lavf58.27.103 mux stamp narrows it to something bundling FFmpeg 4.2, which covers a large family of yt-dlp/youtube-dl-derived tools and GUI wrappers.
- **I could not determine why the PNG encoder (FFmpeg 7.x, emits cICP) and the muxer (FFmpeg 4.2) differ in version.** Two separate tools on one machine is the ordinary explanation, but I did not verify it.
- **I could not distinguish H.264 from VP9 by pixel signature alone with certainty** before finding `SOURCE.mp4` — the block-grid evidence pointed firmly at H.264 (LC's flat ×16→×128 plateau vs. VP9's near-absent 16-px grid), and the container then confirmed it. Recording this because the grid method reached the right answer unaided and is reusable.
- **The Office user name is configuration data, not an identification.** I make no claim that it corresponds to a real person of that name.

### Methodological note for the file

Two traps were live in this analysis and both nearly bit. First, an offset search that scores by hash equality returns a meaningless argmax when *nothing* matches — my first pass silently reported "offset −5" from an all-zero table and produced a page of garbage statistics. Continuous-metric alignment (RMS) is the correct tool when exact matches may not exist. Second, control transcodes made *from* our own AV1 decode inherit that decode's artifacts, so they cannot be used to test for the presence of those artifacts in a third file — useful for block-grid shape, useless for the tile-corner test. Both are worth remembering the next time a cross-rendition comparison comes up.

### Scripts and artifacts

All under `/home/user/new-skinny-bob/analysis/third-party-toolkit/`: `carve.py` (header-walking carver, tolerates truncation, streaming entries and ZIP64), `manifest.json` (3,351 entries with path, offsets, sizes, CRC, method, DOS stamp), `png_forensics.py`, `align.py`, `compare.py`, `compare2.py` (+ `compare2.json`, `diffhist.npy`), `codec_test.py`, `ctrl_test.py`, `grid2.py`, `scale.py`, `audio.py`, and `extracted/` (1.6 GB, complete).