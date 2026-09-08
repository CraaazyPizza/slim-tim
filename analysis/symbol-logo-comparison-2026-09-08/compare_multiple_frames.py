#!/usr/bin/env python3.12
"""Independent per-frame global affine fits; local differences are not attribution tests.
Run with uv run --project /home/user/tools/devpc-python python3.12 <this file>.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import cv2
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
SOURCE = ROOT/'videos/2026-avc/l9RAhmPHM_A.mkv'
assert subprocess.check_output(['ffmpeg', '-version'], text=True).startswith('ffmpeg version 4.4.2-')
web = cv2.imread(str(ROOT/'analysis/domain-qtecqot/2026-09-08/logo.png'), 0)
y, x = np.where(web > 80)
bbox = [int(x.min()), int(y.min()), int(x.max()+1), int(y.max()+1)]
# Include background around the logo so foreground curves never meet a template boundary.
template = web.astype(np.float32)/255
# Coordinates below were chosen from raw frames, not by matching local strokes.
views = [(1210, (700,470,1000,800)),
         (1600, (680,320,980,680)),
         (1694, (680,570,980,900))]
fig, axes = plt.subplots(3, 4, figsize=(16,13), layout='constrained')
records = []
for row, (frame, box) in enumerate(views):
    data = subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(SOURCE),
      '-vf',f'select=eq(n\\,{frame-1})','-frames:v','1','-f','image2pipe','-vcodec','png','pipe:1'])
    full = cv2.imdecode(np.frombuffer(data,np.uint8),cv2.IMREAD_COLOR)
    rgbcrop = full[box[1]:box[3],box[0]:box[2]]
    cv2.imwrite(str(OUT/f'raw-crop-f{frame:05d}.png'),rgbcrop)
    target = cv2.cvtColor(rgbcrop,cv2.COLOR_BGR2GRAY).astype(np.float64)
    h,w = target.shape
    yy,xx = np.mgrid[:h,:w]; xx=(xx-w/2)/w; yy=(yy-h/2)/h
    mask = np.zeros((h,w),bool);mask[15:h-40,20:260]=True
    # Frame 1210 has an adjacent panel feature in the upper right.
    if frame == 1210: mask[:90,230:]=False
    # A single global affine warp, blur, and intensity model; no local warping.
    # Coarse normalized correlation initialization prevents a fit to unrelated background.
    candidates=[]
    foreground=template[bbox[1]:bbox[3],bbox[0]:bbox[2]]
    for sx in (.70,.80,.90,1.):
        for sy in (.75,.85,.95,1.05):
            small=cv2.resize(foreground,None,fx=sx,fy=sy)
            small=cv2.GaussianBlur(small,(0,0),2.)
            score=cv2.matchTemplate(target.astype(np.float32),small,cv2.TM_CCOEFF_NORMED)
            _,peak,_,loc=cv2.minMaxLoc(score)
            candidates.append((peak,[sx,0.,0.,sy,loc[0]-bbox[0]*sx,loc[1]-bbox[1]*sy,2.5]))
    p0=max(candidates,key=lambda item:item[0])[1]
    bounds = ([.55,-.30,-.30,.55,-65.,-45.,.5], [1.2,.30,.30,1.3,65.,60.,7.])
    def render(p):
        mat=np.array([[p[0],p[1],p[4]],[p[2],p[3],p[5]]],np.float32)
        sharp=cv2.warpAffine(template,mat,(w,h),flags=cv2.INTER_LINEAR)
        return sharp,cv2.GaussianBlur(sharp,(0,0),float(p[6]))
    def residual(p, details=False):
        sharp,blur=render(p)
        # Same gain + sloping background family as the earlier single-frame fit.
        design=np.column_stack([blur[mask],np.ones(mask.sum()),xx[mask],yy[mask]])
        coef=np.linalg.lstsq(design,target[mask],rcond=None)[0]
        pred=coef[0]*blur+coef[1]+coef[2]*xx+coef[3]*yy
        return (sharp,blur,pred,coef) if details else (pred-target)[mask]
    def jacobian(p):
        # Absolute steps avoid zero-shear / float32 warp quantization freezing a parameter.
        columns=[]
        for j,step in enumerate([.002,.002,.002,.002,.15,.15,.04]):
            plus=np.array(p,copy=True);minus=plus.copy()
            plus[j]+=step;minus[j]-=step
            columns.append((residual(plus)-residual(minus))/(2*step))
        return np.column_stack(columns)
    fit=least_squares(residual,p0,bounds=bounds,jac=jacobian,loss='soft_l1',f_scale=5,max_nfev=180)
    sharp,blur,pred,coef=residual(fit.x,True)
    assert coef[0] > 0, 'Reject physically inappropriate inverted-contrast fit'
    # Lower background cutoff than the old 25-DN display: preserve faint source signal.
    low,high=10,120
    a=axes[row]
    for col,arr in [(0,target),(1,pred),(2,target),(3,target)]:
        a[col].imshow(arr,cmap='gray',vmin=low,vmax=high,interpolation='nearest')
        a[col].axis('off')
    # 50% boundary of the unblurred warped raster, not a threshold on source data.
    for col in (2,3): a[col].contour(sharp,levels=[.5],colors=['#ff8058'],linewidths=.7,alpha=.9)
    # Website left group's lower bend and tail, transformed into the source coordinates.
    corners=np.array([[60,140,1],[130,140,1],[130,245,1],[60,245,1]],float)
    mat=np.array([[fit.x[0],fit.x[1],fit.x[4]],[fit.x[2],fit.x[3],fit.x[5]]])
    points=corners@mat.T
    x0,y0=points.min(axis=0)-10; x1,y1=points.max(axis=0)+10
    a[2].add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fill=False,edgecolor='#6ee7ef',lw=.8))
    a[3].set_xlim(x0,x1);a[3].set_ylim(y1,y0)
    for col in (0,1,2):a[col].set_xlim(-8,w+8);a[col].set_ylim(h+8,-8)
    for col,title in enumerate(['Source frame '+str(frame)+'\nDisplay stretch 10–120 DN',
           'Website fitted to this frame\nGlobal affine transform + blur',
           'Website boundary on source\nBox marks enlarged region',
           'Left lower bend and tail\nSame fit, enlarged; no local adjustment']):
        a[col].set_title(title,fontsize=10)
    records.append({'frame_1based':frame,'crop_xyxy':box,'raw_crop_sha256':hashlib.sha256((OUT/f'raw-crop-f{frame:05d}.png').read_bytes()).hexdigest(),
      'affine_and_blur_parameters':fit.x.tolist(),'gain_and_background':coef.tolist(),
      'converged':bool(fit.success),'rmse_dn_masked':float(np.sqrt(np.mean(residual(fit.x)**2))),
      'detail_box_xyxy':[float(x0),float(y0),float(x1),float(y1)]})
fig.savefig(OUT/'website-fit-multiple-frames.png',dpi=170)
plt.close(fig)
(OUT/'multiple-frame-metrics.json').write_text(json.dumps({'method':'Separate global affine + Gaussian blur fits; constant gain and planar background; soft-L1 residual; no local deformation or origin classification.',
 'display_stretch_dn':[10,120],'overlay':'50% contour of unblurred warped website raster; not a source edge measurement',
 'website_foreground_bbox_threshold80':bbox,'views':records},indent=2)+'\n')
print(json.dumps(records,indent=2))
