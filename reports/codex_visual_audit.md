# Codex visual audit — 2026 corpus

*Independent review, 2026-07-27. Source frames were inspected at native
1920×1080 resolution, with contrast/luma lifts used only as viewing aids.*

## Executive result

The existing analysis is unusually thorough, but three interpretations have been
promoted beyond what the pixels or audio establish:

1. The four-frame end insert in video 1 is **not presently source-matched to Apollo
   11**. In particular, “Armstrong descending Eagle’s ladder” should not be reported
   as an identification.
2. Video 2 does **not establish a flying boat, aircraft nose, or lakeshore**. Those
   are plausible scene readings, not resolved objects.
3. The 99.907 Hz audio line supports a **50 Hz-mains hypothesis**, but does not prove
   mains pickup or geographic origin. The underlying agent report already states
   this caveat; the outreach draft had lost it.
4. The 2011 opening crest is not a newly identified physical provenance clue. The
   dossier already records that the entire card is lifted from the 1998 commercial
   documentary *The Secret KGB UFO Files*; later model-based “KGB crest” readings
   rediscovered the card’s intended meaning while overlooking its known source.

None of these corrections changes the strongest findings: the 2026 files use a
deliberately assembled modern presentation pipeline; their soundtrack and catalog
structure are publicly reproducible from the 2011 releases; and the 2026 pipeline is
measurably different from the 2011 pipeline.

## 1. Video 1’s four-frame insert

Native frames: `frames/OpSTlDJWFFI/f02971.png` through `f02974.png`.

What is directly observable:

- The insert occupies four output frames, about 133 ms.
- Frames 2971–2972 form one near-identical pair and 2973–2974 another.
- The two pairs are two distinct **image states**. Calling them “poses” or a
  two-frame motion excerpt assumes the cause of the change.
- The picture is strongly blue-weighted, low-information, vignetted and heavily
  posterized. A bright irregular mass occupies much of the left/centre and a dark
  wedge occupies much of the right.
- The soundtrack around it is deliberately arranged. That supports an authored
  end sting regardless of the image’s identity.

What is not established:

- A white pressure suit, PLSS backpack, ladder, lunar module, lunar terrain, or
  Armstrong cannot be resolved independently at this image quality.
- The prior “95%” value came from model agreement, not a source-frame match. Two
  models making the same semantic guess are not independent physical evidence.

Source check:

- Compared against NASA’s restored 292.56-second `Apollo 11 EVA 1` film, including a
  full MPEG-7 signature pass at 320×180 grayscale: **no match**.
- Compared visually against NASA’s restored ladder/first-step view, the Apollo Lunar
  Surface Journal 16 mm sequence-camera view, and coarse samples across the complete
  public moonwalk recording: **no geometric match found**.
- Heavy posterization could defeat an automated signature, so this is not proof that
  the source is non-Apollo. It is enough to reject a positive identification until an
  actual matching source frame is produced.

Recommended status: **unidentified four-frame insert; Apollo imagery is an
unverified candidate only.**

Audit images:

- `analysis/insert-identification/jump_insert_four_frames.png`
- `analysis/insert-identification/nasa_armstrong_descent_samples.jpg`

Reference sources:

- NASA, “Apollo 11 HD Videos”: https://www.nasa.gov/missions/apollo-11-hd-videos/
- NASA SVS, “Apollo 11 HD Videos”: https://svs.gsfc.nasa.gov/10453
- Apollo Lunar Surface Journal, video index:
  https://www.nasa.gov/wp-content/uploads/static/history/alsj/a11/video11.html

## 2. Video 2, Case 11 “Tin bird primer”

Native interval: approximately `f00457`–`f00707`.

What the sequence supports:

- A very large, smooth, pale curved surface fills the early frames.
- A dark, stylized bird-like mark remains attached to that surface across the pan.
- As the camera moves, the underside/edge of the pale form remains across the upper
  frame while a distant outdoor scene is exposed.
- The background contains wooded/rocky or snow-like terrain, two upright figures,
  and a pale ribbed or segmented structure at frame right.

What the sequence does not resolve:

- No cockpit, propeller, wing, engine, registration, waterline or other
  aircraft-specific feature is visible.
- The pale field need not be water, and the location need not be a lakeshore.
- The mark is bird-like, but “nose art,” “national insignia,” and “Soviet marking”
  are progressively stronger interpretations without readable detail.

Recommended wording: **“large pale curved object with a persistent bird-like
marking, overlooking an outdoor compound or terrain with two figures.”** Keep
aircraft/flying-boat identification as a search hypothesis.

Audit image: `analysis/insert-identification/v2_case11_sequence.jpg`.

## 3. Video 3’s circular “lens” shot

Native interval: approximately `f03117`–`f03700`.

The sharp portion shows a genuinely glossy, convex circular surface in a pale
surround. Several soft elliptical highlights and a thin rim reflection remain
coherent as focus and framing change. The later pan exposes pale, finger- or
slab-like forms to the right.

The pixels support “glass-like circular optical surface” more strongly than a
specific identity. They do not establish whether it is:

- an eye covering on a prop/being,
- a mask or helmet eyepiece,
- a camera/inspection lens, or
- another domed instrument.

The current report’s neutral label “the lens shot” is sound. “Mask-like face” should
remain descriptive shorthand, not an object identification. The highlight geometry
is a worthwhile future physical-rendering test because it is among the cleanest
specular information in the corpus.

Audit image: `analysis/insert-identification/v3_lens_sequence.png`.

## 4. Audio claim that escaped its own caveat

`reports/agent_scenes_content.md` is appropriately cautious:

- the strongest stationary line is 99.907 Hz;
- weak companions occur near 49.85 and 149.83 Hz;
- a 60 Hz series is unsupported;
- higher 50 Hz harmonics are mostly absent; and
- the six observed tones also fit a designed tonal cluster.

Therefore the defensible conclusion is:

> If the 99.907 Hz line is mains-related, it indicates a 50 Hz system and argues
> against ordinary North American 60 Hz pickup.

It does **not** prove that the sound is mains hum, that it was recorded in Russia or
Europe, or that the channel’s US setting is false. Upload hours and self-declared
account locations cannot upgrade that ambiguity into geolocation.

## 5. The 2011 opening crest: known borrowed footage

The contrast stack makes the crest easier to see, but does not create a new
identification. `docs/SKINNY_BOB_DOSSIER.md` §4.3 already records the stronger result:
the full still—including the crest and the Russian “TOP SECRET / KGB ARCHIVE”
wording hidden by Ivan’s black bars—comes from the 1998 documentary *The Secret KGB
UFO Files*. Skinnybob.info publishes the source comparison:
https://skinnybob.info/#kgb.

Consequences:

- The card is deliberate KGB-themed production design, not evidence that the
  underlying footage passed through a Soviet archive.
- A vision model calling the crest “KGB” is unsurprising because the uncropped source
  literally labels it KGB.
- The borrowed 1998 still is provenance-relevant in the opposite direction: it is
  modern material inserted ahead of footage presented as a 1942–1969 archive.
- Any Russian/geographic argument should rest on independently sourced evidence, not
  this card.

## 6. Evidence hierarchy for publication

Use three labels consistently:

- **Measured/observed:** exact frames, cadence, spectral peaks, pixel geometry,
  text that is independently legible.
- **Supported interpretation:** best explanation with explicit alternatives.
- **Open lead:** semantic object recognition, geographic attribution, or source
  identity without a direct match.

The Apollo and flying-boat readings belong in the third category. The 50 Hz reading
belongs in the second, with the designed-tone alternative attached.
