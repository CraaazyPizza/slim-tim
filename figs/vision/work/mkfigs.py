#!/usr/bin/env python3.12
"""Reader-facing figures for the vision re-adjudication.
House rule (the owner's method complaint): every enhanced panel is shown beside the
UNMODIFIED single frame it came from, and both are labelled. No stacking, no
frame averaging anywhere in this file -- single frames only.
"""
import numpy as np, os
from PIL import Image, ImageDraw, ImageFont

ROOT = '/home/user/new-skinny-bob'
OUT  = f'{ROOT}/figs/vision'
FB   = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR   = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BG   = (18, 18, 20)
FG   = (238, 238, 238)
DIM  = (158, 158, 165)
ACC  = (255, 196, 60)

def f(sz, bold=True):
    return ImageFont.truetype(FB if bold else FR, sz)

def frame(vid, n):
    return np.asarray(Image.open(f'{ROOT}/frames/{vid}/f{n:05d}.png').convert('RGB'), dtype=np.float64)

def stretch(a, lo=1.0, hi=99.5, box=None):
    """Single-frame linear tone stretch. box=(x0,y0,x1,y1) picks the percentile source."""
    g = a.mean(2)
    if box:
        x0, y0, x1, y1 = box
        g = g[y0:y1, x0:x1]
    l, h = np.percentile(g, lo), np.percentile(g, hi)
    return np.clip((a - l) * 255.0 / (h - l), 0, 255).astype(np.uint8)

def crop(arr, box, zoom=1):
    im = Image.fromarray(arr.astype(np.uint8)) if isinstance(arr, np.ndarray) else arr
    im = im.crop(box)
    if zoom != 1:
        im = im.resize((int(im.width * zoom), int(im.height * zoom)), Image.LANCZOS)
    return im

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def panelgrid(panels, cols, title, subtitle, outname, pw=560, gap=14,
              cap_h=54, head_h=96, foot=None, layout=None):
    """panels = list of (PIL image, label, sublabel).
    layout = optional list of panels-per-row; each row is width-fitted to the canvas."""
    W = cols * pw + (cols + 1) * gap
    if layout is None:
        layout = [cols] * ((len(panels) + cols - 1) // cols)
    groups, i = [], 0
    for k in layout:
        groups.append(panels[i:i+k]); i += k
    scaled_rows = []
    for grp in groups:
        n = len(grp)
        rpw = (W - (n + 1) * gap) // n
        scaled_rows.append([(im.resize((rpw, int(im.height * rpw / im.width)), Image.LANCZOS), lab, sub)
                            for im, lab, sub in grp])
    scaled = [p for r in scaled_rows for p in r]
    rows = len(scaled_rows)
    rh = [max(s[0].height for s in r) + cap_h for r in scaled_rows]
    probe = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    sub_lines = wrap(probe, subtitle, f(19, False), W - 2*gap)
    head_h = 52 + 25*len(sub_lines) + 16
    foot_lines = wrap(probe, foot, f(16, False), W - 2*gap) if foot else []
    foot_h = (12 + 22*len(foot_lines)) if foot else 0
    H = head_h + sum(rh) + rows * gap + gap + foot_h
    cv = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(cv)
    d.text((gap, 16), title, font=f(30), fill=FG)
    for i, ln in enumerate(sub_lines):
        d.text((gap, 56 + 25*i), ln, font=f(19, False), fill=DIM)
    y = head_h
    for r in range(rows):
        x = gap
        for im, lab, sub in scaled_rows[r]:
            cv.paste(im, (x, y))
            d.rectangle([x-1, y-1, x+im.width, y+im.height], outline=(64, 64, 70))
            d.text((x, y + im.height + 7), lab, font=f(20), fill=ACC)
            if sub:
                d.text((x, y + im.height + 31), sub, font=f(16, False), fill=DIM)
            x += im.width + gap
        y += rh[r] + gap
    for i, ln in enumerate(foot_lines):
        d.text((gap, H - foot_h + 6 + 22*i), ln, font=f(16, False), fill=DIM)
    p = f'{OUT}/{outname}'
    cv.save(p)
    print('wrote', p, cv.size)

# ---------------------------------------------------------------- FIG 1
# Case 22 disputed head: raw single frame vs same frame stretched
V2 = 'Oqw96jCOP7A'
BOX22 = (1130, 0, 1660, 430)
a = frame(V2, 1435)
panelgrid(
    [(crop(a, BOX22, 1.6), 'UNMODIFIED single frame', 'video 2 f1435, exactly as decoded'),
     (crop(stretch(a), BOX22, 1.6), 'ENHANCED (same single frame)', 'linear tone stretch only - no stacking, no averaging')],
    2,
    'Fig 1  Video 2, Case 22 head - the disputed "bearded human face"',
    'Overlay reads BL04 /22 00:30:26.  Sharpest frame of the 29-frame shot f1416-1444 (Laplacian variance peak at f1435).',
    '01_case22_raw_vs_enhanced.png', pw=620,
    foot='Independent read (Gemini 3 Pro, no project notes in context): "no high-frequency detail ... cannot confirm the presence of a beard and moustache because there is no visible hair texture".')

# ---------------------------------------------------------------- FIG 2
# identity control: disputed head vs the known grey 35 frames later, same scale
b = frame(V2, 1470)
A = crop(stretch(a), (1150, 0, 1650, 400), 1.0)
B = crop(stretch(b), (880, 20, 1480, 560), 1.0)
h = 470
A = A.resize((int(A.width * h / A.height), h), Image.LANCZOS)
B = B.resize((int(B.width * h / B.height), h), Image.LANCZOS)
panelgrid(
    [(A, 'f1435  -  the disputed head', 'tc BL04 /22 00:30:26  (single frame, stretched)'),
     (B, 'f1470  -  the grey, 35 frames later', 'tc BL04 /22 00:30:31  (single frame, stretched)')],
    2,
    'Fig 2  Identity control - same bed, same bedding, 35 output frames apart',
    'Both panels are single frames at the same pixel scale with the same processing. Same shot sequence, one hard cut between them.',
    '02_case22_vs_grey.png', pw=600,
    foot='The record calls the left panel a second, human casualty. The owner reads it as the same non-human subject looking upward. Neither is settled by these pixels.')

# ---------------------------------------------------------------- FIG 3
# mouth-motion sequence, single frames, NCC-aligned by translation only
def ncc_align(n, ref_g, ty, tx, th, tw, step=4, rng=(64, 88)):
    g = frame(V2, n).mean(2)
    t = ref_g[ty:ty+th, tx:tx+tw]
    tc = t - t.mean(); tn = np.sqrt((tc*tc).sum())
    best = (-9, 0, 0)
    for dy in range(-rng[0], rng[0]+1, step):
        for dx in range(-rng[1], rng[1]+1, step):
            p = g[ty+dy:ty+dy+th, tx+dx:tx+dx+tw]
            if p.shape != t.shape:
                continue
            pc = p - p.mean(); dn = np.sqrt((pc*pc).sum()) * tn
            v = (pc*tc).sum()/dn if dn > 0 else 0
            if v > best[0]:
                best = (v, dx, dy)
    return best

ref_g = frame(V2, 1435).mean(2)
seq = [1422, 1427, 1432, 1435, 1439, 1443]
# gemini's openness rank recovered from the SHUFFLED strip (most open -> least)
rank = {1432: 1, 1435: 2, 1427: 3, 1439: 4, 1443: 5, 1422: 6}
tiles = []
for n in seq:
    v, dx, dy = ncc_align(n, ref_g, 80, 1200, 240, 400)
    im = crop(stretch(frame(V2, n)), (1200+dx, 80+dy, 1600+dx, 320+dy), 2.0)
    tiles.append((im, f'f{n}', f'openness rank {rank[n]} of 6   (NCC {v:.2f})'))
panelgrid(tiles, 6,
    'Fig 3  Case 22 - does the mouth move?  Six single frames in time order',
    'Each panel is one unaveraged frame, aligned to f1435 by whole-pixel translation only. Openness ranks come from an independent observer shown these same six panels SHUFFLED.',
    '03_case22_mouth_sequence.png', pw=330,
    foot='Ranks read 6,3,1,2,4,5 across time = closed -> opening -> most open -> closing -> closed. The ranking was stable when the panels were re-presented out of order, so it tracks an image property, not the left-to-right story.')

# ---------------------------------------------------------------- FIG 4
# video 1 profile, raw
V1 = 'OpSTlDJWFFI'
c = frame(V1, 1532)
BOXV1 = (1230, 60, 1720, 1010)
panelgrid(
    [(crop(c, (300, 30, 1820, 1050), 1.0), 'UNMODIFIED full frame - nothing done to it at all',
      'video 1 f1532, tc /12 01:10:59.  This is the frame the independent read below was given.')],
    1,
    'Fig 4a  Video 1, Case 12 - the near-profile figure at f1437-1570',
    'No crop of the subject, no tone change, no stacking. Straight decode.',
    '04a_v1_profile_fullframe.png', pw=1240,
    foot='Independent read of this exact frame, no context, open question, unprompted: "a human figure in profile ... the bridge of the nose, the tip of the nose, the upper lip, mouth, and chin ... a stiff, high collar ... an epaulette or shoulder board. Attached to this shoulder board are two distinct, small, circular metallic objects". Replicated on a second model.')

HEADV1 = (1180, 60, 1740, 700)
BOARDV1 = (1270, 690, 1660, 920)
panelgrid(
    [(crop(c, HEADV1, 1.0), 'Head - UNMODIFIED, cropped only', 'no tone change at all'),
     (crop(stretch(c, box=HEADV1), HEADV1, 1.0), 'Head - ENHANCED, same single frame', 'linear stretch only'),
     (crop(stretch(c, box=BOARDV1), BOARDV1, 1.0), 'Shoulder board - ENHANCED, same frame', 'the "star" candidate of §31.2')],
    3,
    'Fig 4b  Same single frame, closer',
    'Left is the untouched decode. Middle and right are the same one frame tone-mapped - still no stacking, no averaging.',
    '04b_v1_profile_detail.png', pw=470,
    foot='Asked to describe the right-hand object and count its points or lobes, with no mention of stars, the independent model returned "an irregular, blurry blob ... roughly 3 vague lobes ... its exact shape cannot be definitively determined due to the lack of focus".')

# ---------------------------------------------------------------- FIG 5
# star: negative and injected positive control on the Mk.5 hull
import math
d5 = frame(V1, 2683)
CB = (980, 380, 1620, 780)
g = d5.mean(2)
lo, hi = np.percentile(g[380:780, 980:1620], 1), np.percentile(g[380:780, 980:1620], 99.8)
def rend(arr):
    return crop(np.clip((arr-lo)*255/(hi-lo), 0, 255), CB, 1.6)
inj = d5.copy()
mask = Image.new('L', (1920, 1080), 0)
dr = ImageDraw.Draw(mask)
cx, cy, R = 1290, 550, 60   # brightest 120 px window on the hull (mean 185 DN) = best case
pts = []
for k in range(10):
    ang = -math.pi/2 + k*math.pi/5
    r = R if k % 2 == 0 else R*0.40
    pts.append((cx + r*math.cos(ang), cy + r*math.sin(ang)))
dr.polygon(pts, fill=255)
m = np.asarray(mask, dtype=np.float64)/255.0
ky = np.exp(-0.5*(np.arange(-40, 41)/8.0)**2); ky /= ky.sum()
mb = np.apply_along_axis(lambda r: np.convolve(r, ky, 'same'), 0, m)
mb = np.apply_along_axis(lambda r: np.convolve(r, ky, 'same'), 1, mb)
for ch in range(3):
    inj[:, :, ch] -= mb*35.0
panelgrid(
    [(rend(d5), 'The footage as it is', 'video 1 f2683, colour Mk.5 segment, single frame'),
     (rend(inj), 'SAME frame + a REAL 5-pointed star', '120 px across, 35 DN contrast, blurred to the measured 19 px PSF')],
    2,
    'Fig 5  Star detection limit on the Mk.5 hull',
    'Left: what is actually there. Right: the same single frame with a genuine five-pointed star pasted on and blurred to this footage\'s own sharpness.',
    '05_star_controls.png', pw=620,
    foot='The injected star renders as a formless dark smudge with no points. An independent observer asked to list every marking on the object missed it entirely - so this material cannot resolve a star of this size either way.')

# ---------------------------------------------------------------- FIG 6
# ghost disc, raw frame only + raw zoom
e = frame(V1, 150)
panelgrid(
    [(crop(e, (0, 0, 1920, 1080), 0.60), 'UNMODIFIED single frame', 'video 1 f150 - no stretch, no stacking, no text suppression'),
     (crop(e, (330, 400, 1180, 880), 1.0), 'UNMODIFIED, cropped only', 'same pixels, closer - the silhouette sits under lines 3-4')],
    2,
    'Fig 6  The disc behind the opening title card',
    'Both panels are the raw decode of one frame. The record said this needed 260 frames averaged and the text median-suppressed; it does not.',
    '06_ghost_disc_raw.png', pw=620,
    foot='Independent read of this raw frame, unprompted: "a dark, blurry silhouette of a classic flying saucer (UFO) visible behind the text". A five-frame sweep with "nothing distinct" offered as an explicit answer returned a positive 5 times out of 5. Rated only 2 of 5 for visibility, so subtle rather than obvious - but no processing was needed. Note the LABEL is not stable across readers (saucer / alien head / fedora / eye); only the presence of a dome-over-ellipse silhouette is.')

# ---------------------------------------------------------------- FIG 7
# blink candidate
EB = (600, 360, 1000, 660)
ref = frame(V2, 1212)[360:660, 600:1000].mean(2)
l2, h2 = np.percentile(ref, 2), np.percentile(ref, 99.5)
def eyep(n):
    a = frame(V2, n)
    return crop(np.clip((a-l2)*255/(h2-l2), 0, 255), EB, 1.7)
panelgrid(
    [(eyep(1213), 'f1213  before', 'interior max 96 DN'),
     (eyep(1215), 'f1215  onset', 'interior max 130 DN'),
     (eyep(1217), 'f1217  held', 'interior max 129 DN'),
     (eyep(1221), 'f1221  reverted', 'interior max 94 DN')],
    4,
    'Fig 7  Video 2, Case 21 "Triage" - an eye-localised 5-frame event at f1215-1219',
    'Four single frames, identical tone mapping across all four so the brightness change is real and not a per-panel rescale.',
    '07_blink_sequence.png', pw=420,
    foot='Frame-to-frame change at f1214->f1215: eye 7.62 DN vs nose/mouth 0.96, crown 0.47, cheek 1.05, background 0.02. Reverts at f1219->f1220. No global exposure step and no scanline artifact in the same rows outside the eye.')

# ---------------------------------------------------------------- FIG 8
# jumpscare, both states
def jw(n):
    a = frame(V1, n)
    wb = a.copy()
    for ch in range(3):
        c0 = a[:, :, ch]
        l, hh = np.percentile(c0, 1), np.percentile(c0, 99.8)
        wb[:, :, ch] = np.clip((c0-l)*255/(hh-l), 0, 255)
    return a, wb
a1, w1 = jw(2971)
a2, w2 = jw(2973)
BJ = (240, 10, 1680, 1075)
panelgrid(
    [(crop(a1, BJ, 0.5), 'State A  f2971 - UNMODIFIED', 'held 2 frames (f2971 = f2972)'),
     (crop(w1, BJ, 0.5), 'State A - per-channel white balance', 'same single frame'),
     (crop(a2, BJ, 0.5), 'State B  f2973 - UNMODIFIED', 'held 2 frames (f2973 = f2974)'),
     (crop(w2, BJ, 0.5), 'State B - per-channel white balance', 'same single frame')],
    2,
    'Fig 8  The hidden 4-frame insert that closes video 1 (t 99.10-99.20 s, ~133 ms)',
    'Two image states, each held for two output frames. Left column untouched, right column the same frame with each colour channel stretched independently.',
    '08_jumpscare_poses.png', pw=600,
    foot='Content remains unidentified. An independent observer, given each state separately with no context, could not name any real-world subject in either; for State B it offered only "a vertical, possibly bipedal figure standing on a dark mass". Treat the Apollo reading as withdrawn.')

print('\nall figures written to', OUT)
