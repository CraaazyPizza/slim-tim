# frames/ — not stored, regenerated

The extracted frames are not in this repository. They are 5.0 GB, and they are a
lossless expansion of 29 MB of source video — one ffmpeg command each.

## Just get me some frames

```bash
bin/frames OpSTlDJWFFI 2971 2974    # a range          ~10 s
bin/frames OpSTlDJWFFI              # one whole video   ~60 s, 1.1 GB
bin/frames                          # all seven         ~6 min, 5 GB
```

A range costs about the same as a single frame — the decoder walks the file from
the start either way — so ask for 200 frames as readily as for one. Output lands in
`frames/<video-id>/fNNNNN.png`, numbered from 1, which is the numbering the
writeups use.

If your Codespace came from a prebuild, all seven videos are already extracted and
you can ignore this. The greeting on attach tells you which case you are in.

## The command underneath

```bash
ffmpeg -i <source>.mkv -vsync 0 -pix_fmt rgb24 -start_number 1 f%05d.png
```

Run it inside the container, or with **ffmpeg 4.4.2** if you are on your own
machine. This has been verified rather than assumed: re-running it on three
videos spanning every container shape in the corpus and comparing with
`sha256sum` reproduced the original PNGs **byte for byte**.

```bash
# all seven, into the layout the scripts expect
for f in videos/2026/*.mkv videos/2011/*.mkv; do
  id=$(basename "$f" .mkv)
  mkdir -p "frames/$id" && (cd "frames/$id" && \
    ffmpeg -i "../../$f" -vsync 0 -pix_fmt rgb24 -start_number 1 f%05d.png)
done
```

## Expected output

| video | frames | era |
|---|---:|---|
| `ZB788PtqQvg` | 1,188 | ivan0135, 2011 |
| `RsQCXN4o4Ps` | 1,500 | ivan0135, 2011 |
| `Xju_CY5ZESA` | 2,598 | ivan0135, 2011 |
| `a6TLGkrfNKI` | 2,337 | ivan0135, 2011 |
| `OpSTlDJWFFI` | 2,998 | qtecqot, 2026 |
| `Oqw96jCOP7A` | 2,503 | qtecqot, 2026 |
| `l9RAhmPHM_A` | 4,395 | qtecqot, 2026 |

If your counts differ, stop and say so in an issue — that would be a real finding
rather than a setup problem.

## Why the version pin is not fussiness

ffmpeg 4.4.2 and ffmpeg 7.x produce a **16-byte-per-frame difference** on this
same source: a `cICP` colour-information chunk that the newer build writes into
the PNG. The pixels are the same; the files are not, so hashes will not match
across versions.

Separately, and more interesting: frames decoded from AVC differ from frames
decoded from AV1 by up to 1 in 255 on the same content — measured here at a mean
of 0.001, with our values in {0,1} and an outside analyst's in {0}. That
single-bit delta is how the fixed dark corner dots were identified as AV1
tile-corner artefacts rather than something the author put in the picture.

In a project where a one-bit difference carried a finding, the decoder is part of
the method. Use the container and your frames are comparable to the published
ones.

## Frames that ARE in the repo

Seven are kept because documents cite them directly:

```
frames/OpSTlDJWFFI/f00001.png    frames/OpSTlDJWFFI/f02972.png
frames/OpSTlDJWFFI/f00983.png    frames/OpSTlDJWFFI/f02973.png
frames/OpSTlDJWFFI/f02971.png    frames/OpSTlDJWFFI/f02974.png
frames/l9RAhmPHM_A/f03866.png
```

`f00983` is the Cyrillic caption frame. The four consecutive `f0297x` frames are
the hidden insert at the climax of the May 2026 release — the thing nobody noticed
for two months and nobody has identified.

## Thumbnails

`frames/ytimg/` held 48 yt-dlp thumbnail images. Not extractions, not needed, and
regenerable only while the source videos stay online.
