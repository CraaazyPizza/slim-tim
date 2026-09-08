#!/usr/bin/env python3.12
"""Reproduce original AVC crops, registration, diagnostic images, and contour SVGs.
Run: uv run --project /home/user/tools/devpc-python python3.12 analysis/symbol-reconstruction-2026-09-08/reconstruct.py
"""
from pathlib import Path
import subprocess, json, hashlib
import numpy as np
import cv2
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter
from skimage.measure import find_contours

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parents[1]/'videos/2026-avc/l9RAhmPHM_A.mkv'
BOX=(680,570,950,850)
FRAMES=list(range(1689,1700))
version=subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0]
assert version.startswith('ffmpeg version 4.4.2-'), version
(ROOT/'raw').mkdir(exist_ok=True)
if not all((ROOT/'raw'/f'frame-{f:04d}.png').exists() for f in FRAMES):
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(SOURCE),'-vf',"select='between(n,1688,1698)'",'-vsync','0','-start_number','1689',str(ROOT/'raw/frame-%04d.png')],check=True)
crops=[]
for f in FRAMES:
    im=Image.open(ROOT/'raw'/f'frame-{f:04d}.png').crop(BOX)
    im.save(ROOT/f'raw-crop-{f}.png')
    crops.append(np.asarray(im).astype(np.float32))
gray=[cv2.cvtColor(c,cv2.COLOR_RGB2GRAY) for c in crops]
ref=gray[FRAMES.index(1694)]
registered=[]; metadata=[]
for f,g in zip(FRAMES,gray):
    warp=np.eye(2,3,dtype=np.float32)
    cc,warp=cv2.findTransformECC(ref,g,warp,cv2.MOTION_TRANSLATION,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,150,1e-7),None,5)
    reg=cv2.warpAffine(g,warp,(g.shape[1],g.shape[0]),flags=cv2.INTER_LINEAR|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REFLECT)
    registered.append(reg)
    metadata.append({'frame_1based':f,'ecc':float(cc),'warp_inverse_map':warp.tolist()})
stack=np.array(registered)
med=np.median(stack,axis=0)
# Local subtraction reduces broad panel shading; it does not recover lost detail.
contrast=med-gaussian_filter(med,20)
sm=gaussian_filter(contrast,1.2)
Image.fromarray(np.clip(med,0,255).astype('uint8')).save(ROOT/'processed-registered-median.png')
Image.fromarray(np.clip((contrast+3)*8,0,255).astype('uint8')).save(ROOT/'processed-local-contrast-x8.png')
Image.fromarray(np.clip(stack.std(axis=0)*20,0,255).astype('uint8')).save(ROOT/'processed-temporal-sd-x20.png')
print('range',float(sm.min()),float(sm.max()),'percentiles',np.percentile(sm,[50,75,90,95,99]))

# Cubic Bezier paths follow isocontour vertices. The small simplification tolerance
# and tangent interpolation make an illustrative smooth boundary, not a measured edge.
def path_from_contour(contour):
    xy=contour[:,::-1].astype(np.float32)
    xy=cv2.approxPolyDP(xy.reshape(-1,1,2),0.8,True).reshape(-1,2)
    if len(xy)<4:return ''
    parts=[f'M {xy[0,0]:.2f},{xy[0,1]:.2f}']
    for i,p in enumerate(xy):
        q=xy[(i+1)%len(xy)]; prev=xy[(i-1)%len(xy)]; nxt=xy[(i+2)%len(xy)]
        a=p+(q-prev)/6; b=q-(nxt-p)/6
        parts.append(f'C {a[0]:.2f},{a[1]:.2f} {b[0]:.2f},{b[1]:.2f} {q[0]:.2f},{q[1]:.2f}')
    return ' '.join(parts)+' Z'

def contours(level):
    # No closing/dilation and no joining separate components. Reject tiny islands.
    result=[]
    for c in find_contours(sm,level):
        if len(c)>25 and abs(cv2.contourArea(c[:,::-1].astype(np.float32)))>=20:result.append(c)
    return result

def svg(levels,filename):
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="810" height="840" viewBox="0 0 270 280">', '<title>Data-derived smooth contour illustration; source AVC frame 1694 and registered frames 1689–1699</title>', '<rect width="270" height="280" fill="#faf8f2"/>']
    for level,color,opacity in levels:
        ds=' '.join(path_from_contour(c) for c in contours(level))
        out.append(f'<path d="{ds}" fill="{color}" fill-rule="evenodd" opacity="{opacity}"/>')
    out.append('</svg>')
    (ROOT/filename).write_text('\n'.join(out))
for level in [4,6,8,10,12,16]:
    svg([(level,'#222222',1)],f'contour-{level:02d}DN.svg')
svg([(4,'#b9bbbd',.55),(8,'#4d5358',.7),(12,'#10171c',1)],'reconstruction-with-uncertainty.svg')
svg([(8,'#222222',1)],'reconstruction-smooth.svg')
# Diagnostic panels use source pixel values and explicitly labelled displays.
panels=[]
def panel(a,label,scale=2):
    im=Image.fromarray(np.uint8(np.clip(a,0,255))).convert('RGB').resize((540,560),Image.Resampling.NEAREST)
    canvas=Image.new('RGB',(540,590),'white');canvas.paste(im,(0,30));ImageDraw.Draw(canvas).text((8,8),label,fill='black');return canvas
panels.append(panel(crops[5],'RAW AVC frame 1694; nearest-neighbour x2'))
panels.append(panel(med,'PROCESSED: 11-frame registered median'))
panels.append(panel((contrast+3)*8,'PROCESSED: local contrast (residual+3) x8'))
for level in [4,8,12]:
    im=np.repeat(np.clip(med*3,0,255)[:,:,None],3,axis=2).astype('uint8')
    for c in contours(level):cv2.polylines(im,[np.round(c[:,::-1]).astype('int32')],True,(255,85,30),1)
    panels.append(panel(im,f'PROCESSED: {level} DN contour / median x3'))
canvas=Image.new('RGB',(1620,1180),'white')
for i,im in enumerate(panels):canvas.paste(im,((i%3)*540,(i//3)*590))
canvas.save(ROOT/'diagnostic-contact-sheet.png')
# Source-gradient correspondence and per-frame threshold stability.
grad=np.hypot(cv2.Sobel(med,cv2.CV_32F,1,0,ksize=3),cv2.Sobel(med,cv2.CV_32F,0,1,ksize=3))
Image.fromarray(np.uint8(np.clip(grad*3,0,255))).save(ROOT/'processed-gradient-x3.png')
individual=np.array([gaussian_filter(g-gaussian_filter(g,20),1.2) for g in registered])
support=(individual>=8).mean(axis=0)
Image.fromarray(np.uint8(support*255)).save(ROOT/'processed-8DN-temporal-support.png')
(ROOT/'registration.json').write_text(json.dumps({'source':str(SOURCE),'decoder':version,'crop_xyxy':BOX,'reference_frame_1based':1694,'frames':metadata,'contrast_gaussian_sigma':20,'contour_gaussian_sigma':1.2,'simplification_tolerance_px':.8},indent=2))
# Single-frame and five-frame sensitivity checks retain the same filtering and level.
full_sm=sm.copy()
for label,base in [('single-frame-1694',ref),('five-frames-1692-1696',np.median(stack[3:8],axis=0))]:
    sm=gaussian_filter(base-gaussian_filter(base,20),1.2)
    svg([(8,'#222222',1)],f'sensitivity-{label}.svg')
sm=full_sm
# Comparison of source gradients and per-frame persistence, both diagnostic only.
canvas=Image.new('RGB',(1620,590),'white')
for i,im in enumerate([panel(ref,'RAW: frame 1694'),panel(grad*3,'PROCESSED: median Sobel gradient x3'),panel(support*255,'PROCESSED: fraction of 11 frames >=8 DN')]):canvas.paste(im,(i*540,0))
canvas.save(ROOT/'gradient-and-support.png')
import pymupdf
for f in ['reconstruction-smooth','reconstruction-with-uncertainty','sensitivity-single-frame-1694','sensitivity-five-frames-1692-1696']:
    d=pymupdf.open(ROOT/(f+'.svg'));d[0].get_pixmap().save(ROOT/(f+'.png'))
