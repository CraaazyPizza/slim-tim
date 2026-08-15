"""Shared primitives for the star-question rerun (Arm 1).

numpy + PIL only, by design decision D6 -- no scipy, no cv2. Every operation the
detector depends on is implemented here in full so it can be audited line by line.

Paths resolve relative to this file (D4). The older scripts under analysis/ hardcode
/home/user/new-skinny-bob; this deliberately does not.

Three things here were got wrong in a first draft and are called out so they are not
re-introduced:

  * blur() uses pad -> convolve 'valid' -> exact-shape output. np.convolve(x, k, 'same')
    returns max(len(x), len(k)), so a kernel wider than the array silently grows it. That
    is reachable inside the approved grid: the 40 px cell at half resolution is a 22 px
    array meeting a 43-tap kernel at the measured PSF. See selftest.test_blur_shape.
  * xcorr() rolls by +(th//2, tw//2). The correlation identity is
    IFFT(FFT(img).conj(FFT(tpl)))[m] = sum_n img[n] tpl[n-m], which peaks at m = i - t,
    so centre-alignment needs out[x] = full[x - tw//2]. Cropping at +th//2 instead --
    the first draft -- offsets every peak by the template centre and would have failed
    D9's location requirement in a way that still looks like a working detector. See
    selftest.test_xcorr_alignment.
  * placement clearance comes from the template's own support, not a fixed erosion.
    See template_support() and D23.
"""
import os
import numpy as np
from PIL import Image, ImageDraw

# ---------------------------------------------------------------- corpus constants

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))

VIDEO = 'OpSTlDJWFFI'
SEGMENT = (2571, 2917)          # Mk.5 colour segment, agent_mk5_claims.md:240
CODECS = {'av1': 'frames', 'avc': 'frames-avc'}

# Film matte: union active box over 8 frames spanning the segment (measured, not assumed).
MATTE = dict(x0=280, y0=40, x1=1625, y1=1045)

# Captions in this segment are transient, not burned in -- a temporal-invariance probe
# over 14 frames spanning f2571-2917 found no static bright overlay at all. The one known
# caption frame (f2655, cf. analysis/cyrillic/mk5-captions/) puts caption ink at y>=900.
CAPTION_Y0 = 880

# ---------------------------------------------------------------- frame access


def frame_path(codec, n):
    return os.path.join(ROOT, CODECS[codec], VIDEO, 'f%05d.png' % n)


def load_luma(codec, n):
    """Flat mean of RGB, matching mkfigs.py's `d5.mean(2)` so numbers here stay
    comparable to the published figure."""
    a = np.asarray(Image.open(frame_path(codec, n)).convert('RGB'), dtype=np.float64)
    return a.mean(2)


def load_stack(codec, frames):
    """Mean stack over the given frame numbers (Amendment A1).

    The two prior injections are not comparable as they stand: mkfigs.py's 120 px / 35 DN
    miss was single-frame, agent_mk5_claims.md:88's 'clearly visible' 70 px / 35 DN was a
    50-frame mean stack. Every number produced downstream is tagged single-frame or
    stacked so the comparison resolves instead of repeating.
    """
    acc = None
    for n in frames:
        g = load_luma(codec, n)
        acc = g if acc is None else acc + g
    return acc / float(len(frames))


def halve(a):
    """2x2 box downsample to the half resolution the published survey ran at
    (agent_mk5_claims.md:59). Requires even dimensions; 1920x1080 qualifies."""
    h, w = a.shape
    return a[:h - h % 2, :w - w % 2].reshape(h // 2, 2, w // 2, 2).mean((1, 3))


# ---------------------------------------------------------------- blur


def gauss_kernel(sigma):
    radius = max(1, int(np.ceil(5.0 * sigma)))
    x = np.arange(-radius, radius + 1, dtype=np.float64)
    k = np.exp(-0.5 * (x / sigma) ** 2)
    return k / k.sum()


def blur_radius(sigma):
    return max(1, int(np.ceil(5.0 * sigma)))


def _conv1d(a, k, axis, mode):
    """Pad -> convolve 'valid' -> exact input shape, for any kernel/array size ratio."""
    r = (len(k) - 1) // 2
    width = [(0, 0)] * a.ndim
    width[axis] = (r, len(k) - 1 - r)
    ap = np.pad(a, width, mode=mode)
    return np.apply_along_axis(lambda v: np.convolve(v, k, 'valid'), axis, ap)


def blur(a, sigma, mode='constant'):
    """Separable Gaussian, shape-preserving by construction.

    mode='constant' (zero pad) is correct for a rendered shape sitting on empty
    background; mode='edge' is correct for image data.
    """
    k = gauss_kernel(sigma)
    return _conv1d(_conv1d(a, k, 0, mode), k, 1, mode)


# ---------------------------------------------------------------- box statistics
# Integral-image box filters, so local normalisation needs no scipy.


def _integral(a):
    return np.pad(a, ((1, 0), (1, 0)), mode='constant').cumsum(0).cumsum(1)


def box_mean(a, half):
    ii = _integral(a)
    h, w = a.shape
    y0 = np.clip(np.arange(h) - half, 0, h)
    y1 = np.clip(np.arange(h) + half + 1, 0, h)
    x0 = np.clip(np.arange(w) - half, 0, w)
    x1 = np.clip(np.arange(w) + half + 1, 0, w)
    tot = (ii[np.ix_(y1, x1)] - ii[np.ix_(y0, x1)]
           - ii[np.ix_(y1, x0)] + ii[np.ix_(y0, x0)])
    cnt = np.outer(y1 - y0, x1 - x0).astype(np.float64)
    return tot / cnt


def local_normalize(a, half):
    """Zero-mean, unit-variance in a local window -- the 'locally-normalized'
    preprocessing of agent_mk5_claims.md:59."""
    m = box_mean(a, half)
    v = box_mean(a * a, half) - m * m
    return (a - m) / np.sqrt(np.maximum(v, 1e-6))


# ---------------------------------------------------------------- masks


def matte_mask(shape=(1080, 1920)):
    m = np.zeros(shape, dtype=bool)
    m[MATTE['y0']:MATTE['y1'], MATTE['x0']:MATTE['x1']] = True
    m[CAPTION_Y0:, :] = False
    return m


def erode(m, r):
    """Binary erosion by a (2r+1) square. The mask is padded False first, so a pixel
    within r of the frame border can never survive on a clipped window."""
    if r <= 0:
        return m.copy()
    p = np.pad(m.astype(np.float64), ((r, r), (r, r)), mode='constant')
    s = box_mean(p, r)[r:-r, r:-r]
    return s > 1.0 - 1e-9


def hull_mask(luma, thr=140.0):
    """D10 option (ii), the primary search domain: per-frame luma threshold.

    Returns the *unclearanced* mask. Placement clearance is not applied here because it
    depends on the template being injected -- see template_support() and D23. The craft
    translates a long way through this segment (centroid x 1066->1312, bright area
    20k-268k px), which is why a fixed region would be wrong.
    """
    return (luma >= thr) & matte_mask(luma.shape)


# D10 option (i), sanity overlay only: a fixed box around the craft's union footprint
# across the segment. Never the search domain. A collapse in agreement flags a frame
# where the threshold has failed.
HULL_POLY = [(940, 90), (1600, 90), (1600, 700), (940, 700)]


def poly_mask(shape, poly):
    im = Image.new('L', (shape[1], shape[0]), 0)
    ImageDraw.Draw(im).polygon(poly, fill=255)
    return np.asarray(im) > 127


def hull_agreement(mask):
    ref = poly_mask(mask.shape, HULL_POLY)
    inter = int((mask & ref).sum())
    union = int((mask | ref).sum())
    return dict(iou=inter / union if union else 0.0,
                covered=inter / int(mask.sum()) if mask.sum() else 0.0)


# ---------------------------------------------------------------- shapes and support


def template_support(size, sigma):
    """Half-width of the canvas a star of `size` blurred at `sigma` needs, in px.

    This is the D23 clearance: size/2 + blur radius. The injector samples sites only
    from `erode(hull_mask(...), template_support(size, sigma))`, so no injected star can
    overhang the hull edge or the matte -- it is enforced by rejecting the *site*, via an
    eroded placement mask, rather than by a fixed global erosion. The first draft used a
    fixed erode=8, which would have let the 140 px cell hang off the hull.
    """
    return int(np.ceil(size / 2.0)) + blur_radius(sigma)


def _canvas_odd(half_width):
    """Odd canvas size, so the shape centre is exactly index n//2 and the injector,
    the template builder and xcorr all share one unambiguous centre convention."""
    return 2 * int(half_width) + 1


def _poly_points(c, R, points, rot_deg, inner):
    out = []
    rot = np.deg2rad(rot_deg)
    for k in range(2 * points):
        ang = -np.pi / 2 + rot + k * np.pi / points
        r = R if k % 2 == 0 else R * inner
        out.append((c + r * np.cos(ang), c + r * np.sin(ang)))
    return out


def star_shape(size, half_width, points=5, rot_deg=0.0, inner=0.40, ss=4):
    """Filled star, unit amplitude, on an odd canvas, supersampled then box-downsampled.
    `size` is outer diameter in px. inner=0.40 matches mkfigs.py:207."""
    n = _canvas_odd(half_width)
    c = n * ss / 2.0
    big = Image.new('L', (n * ss, n * ss), 0)
    ImageDraw.Draw(big).polygon(_poly_points(c, (size / 2.0) * ss, points, rot_deg, inner),
                                fill=255)
    return np.asarray(big, dtype=np.float64).reshape(n, ss, n, ss).mean((1, 3)) / 255.0


def disc_shape(size, half_width, ss=4):
    n = _canvas_odd(half_width)
    c = n * ss / 2.0
    R = (size / 2.0) * ss
    big = Image.new('L', (n * ss, n * ss), 0)
    ImageDraw.Draw(big).ellipse([c - R, c - R, c + R, c + R], fill=255)
    return np.asarray(big, dtype=np.float64).reshape(n, ss, n, ss).mean((1, 3)) / 255.0


def render_blurred(kind, size, sigma, rot_deg=0.0, half_width=None):
    """A blurred shape on its own odd canvas, amplitude in [0, 1]. Used both to inject
    (scaled to a DN contrast) and, after zero-meaning, as a matched-filter template."""
    if half_width is None:
        half_width = template_support(size, sigma)
    if kind == 'star5':
        a = star_shape(size, half_width, 5, rot_deg)
    elif kind == 'star6':
        a = star_shape(size, half_width, 6, rot_deg)
    elif kind == 'disc':
        a = disc_shape(size, half_width)
    else:
        raise ValueError(kind)
    return blur(a, sigma, mode='constant')


def make_template(kind, size, sigma, rot_deg=0.0):
    """Zero-mean, unit-norm matched-filter template.

    star6 and disc are the controls: per agent_mk5_claims.md:59-61 the statistic is
    star5 measured *against* them, because a bare star5 response fires on any bright blob
    and that is what produced the published top-ranked 'candidates'.

    The canvas is trimmed to 3 sigma of blur rather than the injector's 5 sigma, so the
    template is not mostly zeros -- a large sparse template survives zero-meaning but
    wastes correlation area.
    """
    hw = int(np.ceil(size / 2.0)) + int(np.ceil(3.0 * sigma))
    a = render_blurred(kind, size, sigma, rot_deg, half_width=hw)
    a = a - a.mean()
    nrm = float(np.sqrt((a * a).sum()))
    return a / nrm if nrm > 0 else a


# ---------------------------------------------------------------- matched filter


def xcorr(img, tpl):
    """Cross-correlation via numpy FFT, centre-aligned.

    Returns an array the shape of `img` where out[y, x] is the response with the
    template's centre pixel (th//2, tw//2) sitting on img pixel (y, x).

    Derivation: IFFT(FFT(img) * conj(FFT(tpl)))[m] = sum_n img[n] tpl[n - m], which for
    an impulse pair peaks at m = i - t. Centre alignment therefore needs
    out[x] = full[x - tw//2], i.e. a roll by +tw//2. Verified for odd and even template
    sizes in selftest.test_xcorr_alignment.
    """
    ih, iw = img.shape
    th, tw = tpl.shape
    fh, fw = ih + th - 1, iw + tw - 1
    F = np.fft.rfft2(img, (fh, fw)) * np.conj(np.fft.rfft2(tpl, (fh, fw)))
    full = np.fft.irfft2(F, (fh, fw))
    full = np.roll(full, (th // 2, tw // 2), axis=(0, 1))
    return full[:ih, :iw]


# ---------------------------------------------------------------- injection


def inject(luma, cx, cy, size, sigma, contrast_dn, rot_deg=0.0, polarity=-1):
    """Add one blurred star to a full-resolution frame, in place on a copy.

    polarity=-1 subtracts (dark star), matching mkfigs.py:216-217 and the headline grid
    of D24; polarity=+1 is the bright replicate. Injection happens at full resolution and
    at the full-resolution PSF; the detector's half-resolution templates use sigma/2.

    D34 applies and is not fixed here: this is a post-decode injection, so the added mark
    takes no codec damage while the frame around it already has. Arm 1b re-encodes three
    cells to bound that bias.
    """
    hw = template_support(size, sigma)
    a = render_blurred('star5', size, sigma, rot_deg, half_width=hw)
    n = a.shape[0]
    y0, x0 = int(cy) - n // 2, int(cx) - n // 2
    if y0 < 0 or x0 < 0 or y0 + n > luma.shape[0] or x0 + n > luma.shape[1]:
        raise ValueError('injection canvas leaves the frame: site clearance not applied')
    out = luma.copy()
    out[y0:y0 + n, x0:x0 + n] += polarity * contrast_dn * a
    return out


def placement_mask(luma, size, sigma, thr=140.0):
    """The D23 site domain: hull mask eroded by the template's own support."""
    return erode(hull_mask(luma, thr), template_support(size, sigma))
