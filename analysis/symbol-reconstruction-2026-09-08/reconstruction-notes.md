# Blind reconstruction of the lower-panel bright stroke cluster

The main deliverable is `reconstruction-with-uncertainty.svg` (and PNG preview). Dark regions are the 12-DN local-contrast contour; intermediate and pale regions add the 8- and 4-DN contours. These layers are **threshold sensitivity, not confidence intervals**. `reconstruction-smooth.svg` is the single 8-DN illustrative silhouette. Neither is an exact recovered original design.

## Source and reproducibility

- Source: `videos/2026-avc/l9RAhmPHM_A.mkv`, original AVC copy.
- Decoder verified: `ffmpeg version 4.4.2-0ubuntu0.22.04.1`.
- Full decoded frames: `raw/frame-1689.png` through `raw/frame-1699.png`, inclusive, **1-based**. ffmpeg selection is zero-based `between(n,1688,1698)`; frame 1694 is decoder index 1693.
- Crop: x=680…949, y=570…849, half-open Python bounds `(680,570,950,850)`. `raw-crop-1694.png` contains unmodified decoded RGB pixels. Other `raw-crop-*.png` files have the same source-coordinate bounds.
- Reproduce using `uv run --project /home/user/tools/devpc-python python3.12 analysis/symbol-reconstruction-2026-09-08/reconstruct.py`. The existing shared environment supplies the locked dependencies. No generative tools, external reference artwork, old reconstructions, or identity interpretations were used.

## Method and subjective choices

1. Estimate a translation for each crop relative to frame 1694 using OpenCV ECC, then resample with bilinear interpolation. Full transforms and correlations are in `registration.json`. ECC correlations range 0.91865–1.0; the largest shift is about 22.6 px horizontally and 8.6 px vertically. Translation-only alignment does not compensate for perspective or changing blur.
2. Compute the median of all eleven registered grayscale crops. Subtract a Gaussian-smoothed background with sigma=20 source pixels, then smooth the residual with sigma=1.2 px. This is shading removal and mild smoothing; it does not recover unseen detail.
3. Extract isocontours at 4, 6, 8, 10, 12 and 16 DN above the estimated local background. Discard contour islands smaller than 20 px² or with 25 or fewer vertices. There is no morphological closing, dilation, or manual joining of separate pieces.
4. Simplify contours with tolerance 0.8 source px and interpolate cubic Bézier segments from neighboring vertices. This creates a usable smooth vector boundary. Curves can deviate locally from the measurement contour and should be read as illustration. Width, tip roundness, exact endpoints, background scale, smoothing scale, thresholds, component filtering and curve tolerance are analyst choices.

The 8-DN level is a display choice, **not a calibrated detection floor**. No inference that a faint stroke is absent follows from it.

## What remains uncertain

The bright upper portions and the right-hand transverse stroke are comparatively stable across these choices. Lower ends change length/shape across thresholds and temporal windows. In particular, the left group's lowermost return and its inner descending stroke join at a lower contrast contour and separate at higher contours. The uncertainty illustration preserves that difference; selecting one contour cannot establish whether the original mark was open or closed there.

The single-frame silhouette has local narrowings and small irregularities that are subdued in the temporal median. A five-frame variant retains more of these than the eleven-frame rendering. Repeated video frames are correlated observations, not eleven independent measurements. Temporal persistence alone cannot establish fine geometry. The deliverables make no absence claim about further faint hooks or connections; testing one would require a specified synthetic feature and injection/recovery calibration.

## Review assets

- `diagnostic-contact-sheet.png`: raw frame 1694, registered median, local-contrast display, and 4/8/12-DN measurement contours over the median. All scaling is labelled.
- `gradient-and-support.png`: raw reference, source-gradient diagnostic, and the fraction of registered frames above the selected threshold. Gradients are computed from the registered source median; they are not an independent source.
- `sensitivity-single-frame-1694.svg` / PNG and `sensitivity-five-frames-1692-1696.svg` / PNG: same processing and threshold with narrower temporal windows.
- `contour-04DN.svg` through `contour-16DN.svg`: alternate thresholds, as enumerated above.
- `processed-*.png`: explicitly processed diagnostic images, not original frames.
- `inspection.png`: an initial enlarged crop for viewing, not a raw pixel reference.

The publication manifest lists the selected evidence files. Additional diagnostic outputs described here can be regenerated with the scripts; not every generated intermediate is committed.

## Separate earlier view: essential second deliverable

**Use both views.** `earlier-view-with-threshold-sensitivity.svg` / PNG and `earlier-view-reconstruction.svg` / PNG add a separately reconstructed view centered on **frame 1600**, using frames **1598–1602 inclusive**. `raw/frame-1600.png` is the unmodified full decoded frame; `raw-crop-1600.png` preserves its original pixels at bounds `(680,350,980,680)`. `earlier-view-diagnostic.png` places original, registered median, and local-contrast display together.

Run `uv run --project /home/user/tools/devpc-python python3.12 analysis/symbol-reconstruction-2026-09-08/reconstruct_earlier.py` to reproduce this separate reconstruction. It imports and reruns the first script, then applies the same filter, contour, and smoothing choices to the earlier five-frame window. `earlier-registration.json` records the translations; the first two earlier frames require about 23–24 px vertical translation, with ECC correlation 0.9823–0.9936 for non-reference frames. No spatial averaging or merging was performed between the two temporal windows.

Before choosing frame 1600, original AVC frames 1210, 1350, 1500, 1600 and 1710 were sampled. `raw/sample-01.png` through `sample-05.png` correspond to that ordered list. Reproduce this sampling and its labelled downscaled overview with `sample_views.py` using the same uv command prefix. A separate raw crop of frame 1210 was also inspected, at `(730,490,960,750)` (the enlarged `inspect-sample-1.png` is only a viewing aid). Frame 1500 provides no useful positive shape constraint in this inspection; this is not a calibrated absence result.

The earlier view materially changes what a useful comparison should preserve:

- At frame 1600, the two right-hand descending strokes curve leftward at their lower ends. These curves are supported by contiguous bright pixels in the raw frame and persist across the five-frame rendering. The lower curve of the inner one approaches/joins the central vertical at the displayed contour levels.
- The left group has a downward extension below its curved side's meeting region. In the 1694 rendering, the lower return and inner stroke have different relative extents and threshold-dependent closure.
- The upper cap on the far-right vertical is separated by a low-contrast interval in the 1600 rendering; the 1694 rendering has a broad continuous upper shape. The central vertical's top also differs. These threshold results do not establish whether an original physical mark had a gap.
- Frame 1210 supplies a further raw view consistent with leftward turns at the lower ends of the right group. It was not included in either median or vector contour.

These are **view-dependent pixel observations**, not exact original geometry. Projection, shading, blur, compression, and changes within the footage are not disentangled here. A single clean canonical silhouette would hide these differences. The two separate main deliverables therefore retain their respective lower ends and top-region uncertainty rather than imposing one design or inventing connections. No absence detection floor has been calibrated, and none of the threshold layers is a statistical confidence band.
