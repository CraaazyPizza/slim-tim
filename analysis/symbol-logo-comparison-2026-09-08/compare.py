#!/usr/bin/env python3.12
"""Compare existing raster representations; no source-attribution classifier.
Run: uv run --project /home/user/tools/devpc-python python analysis/symbol-logo-comparison-2026-09-08/compare.py
"""
from pathlib import Path
import hashlib,json
import cv2
import numpy as np
from scipy.optimize import least_squares
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
web=cv2.imread(str(ROOT/'analysis/domain-qtecqot/2026-09-08/logo.png'),0)
raw=cv2.imread(str(ROOT/'analysis/domain-qtecqot/2026-09-08/interior-avc-f01694.png'),0)
stack=cv2.imread(str(ROOT/'analysis/symbol-panel/glyph_stack_lin.png'),0)
art=cv2.imread(str(ROOT/'analysis/symbol-panel/glyph_lineart_uncertain.png'),0)
crop=raw[580:880,680:960]
# Raw grayscale source is displayed with original pixel values in panel 1.
fig,ax=plt.subplots(1,4,figsize=(15,5),layout='constrained')
for a,im,title in zip(ax,[crop,stack,art,web],['Original AVC frame 1694\nUnmodified crop, 1-based frame','Older 145-frame stack\nProcessed AV1 footage','Older agreement line art\nThresholded; gray = less agreement','Website PNG\n343 × 270 pixels']):
 a.imshow(im,cmap='gray',vmin=0,vmax=255,interpolation='nearest');a.set_title(title,fontsize=11);a.axis('off')
fig.savefig(OUT/'source-comparison.png',dpi=150);plt.close(fig)
# Align the website mark to the raw crop via bounded affine warp and blur.
# Contrast is fitted with a gain, offset, and low-order background plane.
# This is a conditional shape fit, not evidence of derivation or exact identity.
yy,xx=np.mgrid[:crop.shape[0],:crop.shape[1]]
xx=(xx-crop.shape[1]/2)/crop.shape[1];yy=(yy-crop.shape[0]/2)/crop.shape[0]
y,x=np.where(web>80);bbox=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
t=web[bbox[1]:bbox[3],bbox[0]:bbox[2]].astype(float)/255
# Resize initial template to expected native-source extent. Fit only within ROI.
t=cv2.resize(t,(195,220),interpolation=cv2.INTER_AREA).astype(np.float32)
target=crop.astype(float)
# x,y location and 2x2 affine, Gaussian blur; background/gain fitted internally.
p0=np.array([1.,0.,0.,1.,35.,30.,2.5])
bounds=([.7,-.25,-.25,.65,0.,0.,.4],[1.3,.25,.25,1.3,90.,90.,7.])
mask=np.ones(crop.shape,bool);mask[:10]=False;mask[-10:]=False;mask[:,:10]=False;mask[:,-10:]=False
# Exclude upper-right neighboring panel object; same mask used for all fitted residuals.
mask[:70,225:]=False

def render(p):
 M=np.array([[p[0],p[1],p[4]],[p[2],p[3],p[5]]],np.float32)
 w=cv2.warpAffine(t,M,(crop.shape[1],crop.shape[0]),flags=cv2.INTER_LINEAR)
 return cv2.GaussianBlur(w,(0,0),float(p[6]))

def fit(p,ret=False):
 w=render(p);A=np.column_stack([w[mask],np.ones(mask.sum()),xx[mask],yy[mask]])
 coef=np.linalg.lstsq(A,target[mask],rcond=None)[0]
 pred=coef[0]*w+coef[1]+coef[2]*xx+coef[3]*yy
 return (pred,coef,w) if ret else (pred-target)[mask]
res=least_squares(fit,p0,bounds=bounds,diff_step=.002,loss='soft_l1',f_scale=5,max_nfev=150)
pred,coef,w=fit(res.x,True)
# Error metrics are conditional upon selected ROI, mask, warp family, and brightness model.
older_paths=sorted((ROOT/'analysis/symbol-panel').glob('*.png'))
web_hash=hashlib.sha256((ROOT/'analysis/domain-qtecqot/2026-09-08/logo.png').read_bytes()).hexdigest()
metrics={'method':'Website silhouette fitted to raw AVC crop with affine warp, Gaussian blur, gain and background plane; no origin classification.', 'source_crop_xyxy':[680,580,960,880],'website_foreground_bbox_threshold80':bbox,'affine_parameters':res.x.tolist(),'gain_background_coefficients':coef.tolist(),'rmse_dn_masked':float(np.sqrt(np.mean((pred-target)[mask]**2))),'median_abs_error_dn_masked':float(np.median(np.abs((pred-target)[mask]))),'fit_converged':bool(res.success),'website_sha256':hashlib.sha256((ROOT/'analysis/domain-qtecqot/2026-09-08/logo.png').read_bytes()).hexdigest(),'older_pngs_compared_for_exact_hash':len(older_paths),'older_png_exact_hash_matches':[p.name for p in older_paths if hashlib.sha256(p.read_bytes()).hexdigest()==web_hash]}
# Display stretch is explicitly labeled; outlines are not measurements of native sharp edges.
fig,ax=plt.subplots(1,3,figsize=(11,4.5),layout='constrained')
ax[0].imshow(target,cmap='gray',vmin=25,vmax=130);ax[0].set_title('Original crop, display stretch\n25–130 DN')
ax[1].imshow(pred,cmap='gray',vmin=25,vmax=130);ax[1].set_title('Fitted website template\nBlurred + affine-transformed')
ax[2].imshow(target,cmap='gray',vmin=25,vmax=130);ax[2].contour(w,levels=[.35],colors=['#ff6040'],linewidths=.8);ax[2].set_title('Template contour on source\nConditional alignment, not identity')
for a in ax:a.axis('off')
fig.savefig(OUT/'website-fit-to-frame.png',dpi=150);plt.close(fig)
(OUT/'comparison-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n')
print(json.dumps(metrics,indent=2))

# Display both independently reconstructed temporal windows alongside their raw crops.
recon=ROOT/'analysis/symbol-reconstruction-2026-09-08'
fig,axs=plt.subplots(2,3,figsize=(12,10),layout='constrained')
panels=[
 (recon/'raw-crop-1600.png','Original AVC frame 1600\nUnmodified RGB crop'),
 (recon/'earlier-view-with-threshold-sensitivity.png','Blind reconstruction, frames 1598–1602\nProcessed; shades = threshold sensitivity'),
 (ROOT/'analysis/domain-qtecqot/2026-09-08/logo.png','Website PNG\n343 × 270 pixels'),
 (recon/'raw-crop-1694.png','Original AVC frame 1694\nUnmodified RGB crop'),
 (recon/'reconstruction-with-uncertainty.png','Blind reconstruction, frames 1689–1699\nProcessed; shades = threshold sensitivity'),
 (ROOT/'analysis/symbol-panel/glyph_stack_lin.png','Older 145-frame extraction\nProcessed AV1 footage')]
for a,(path,title) in zip(axs.flat,panels):
 im=cv2.cvtColor(cv2.imread(str(path)),cv2.COLOR_BGR2RGB)
 a.imshow(im,interpolation='nearest');a.set_title(title,fontsize=11);a.axis('off')
fig.savefig(OUT/'two-view-comparison.png',dpi=150);plt.close(fig)
