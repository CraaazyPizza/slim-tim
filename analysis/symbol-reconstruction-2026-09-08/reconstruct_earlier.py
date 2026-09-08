#!/usr/bin/env python3.12
"""Separate view: execute after reconstruct.py, same locked shared environment."""
import reconstruct as m
import subprocess,json
import numpy as np
import cv2,pymupdf
from PIL import Image,ImageDraw
from scipy.ndimage import gaussian_filter
from skimage.measure import find_contours
p=m.ROOT
frames=list(range(1598,1603)); box=(680,350,980,680)
if not all((p/'raw'/f'frame-{f}.png').exists() for f in frames):
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(m.SOURCE),'-vf',"select='between(n,1597,1601)'",'-vsync','0','-start_number','1598',str(p/'raw/frame-%04d.png')],check=True)
a=[]
for f in frames:
 im=Image.open(p/'raw'/f'frame-{f}.png').crop(box);im.save(p/f'raw-crop-{f}.png');a.append(cv2.cvtColor(np.array(im),cv2.COLOR_RGB2GRAY).astype('float32'))
ref=a[2];regs=[];meta=[]
for f,g in zip(frames,a):
 w=np.eye(2,3,dtype=np.float32)
 cc,w=cv2.findTransformECC(ref,g,w,cv2.MOTION_TRANSLATION,(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,150,1e-7),None,5)
 regs.append(cv2.warpAffine(g,w,(300,330),flags=cv2.INTER_LINEAR|cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REFLECT));meta.append({'frame':f,'ecc':cc,'warp':w.tolist()})
med=np.median(regs,axis=0);res=med-gaussian_filter(med,20);m.sm=gaussian_filter(res,1.2)
for name,levels in [('earlier-view-reconstruction',[(8,'#222222',1)]),('earlier-view-with-threshold-sensitivity',[(4,'#b9bbbd',.55),(8,'#4d5358',.7),(12,'#10171c',1)])]:
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="600" height="660" viewBox="0 0 300 330">','<title>Separate earlier view, AVC frames 1598-1602 registered to 1600; threshold-derived illustration</title>','<rect width="300" height="330" fill="#faf8f2"/>']
 for level,col,op in levels:
  ds=' '.join(m.path_from_contour(c) for c in m.contours(level));out.append(f'<path d="{ds}" fill="{col}" fill-rule="evenodd" opacity="{op}"/>')
 out.append('</svg>');(p/(name+'.svg')).write_text('\n'.join(out));d=pymupdf.open(p/(name+'.svg'));d[0].get_pixmap().save(p/(name+'.png'))
canvas=Image.new('RGB',(1800,690),'white')
for i,(data,label) in enumerate([(ref,'RAW original AVC frame 1600; nearest-neighbour x2'),(med,'PROCESSED registered median 1598-1602'),(res*8+24,'PROCESSED local contrast (residual+3) x8')]):
 im=Image.fromarray(np.uint8(np.clip(data,0,255))).convert('RGB').resize((600,660),Image.Resampling.NEAREST);canvas.paste(im,(i*600,30));ImageDraw.Draw(canvas).text((i*600+5,8),label,fill='black')
canvas.save(p/'earlier-view-diagnostic.png')
(p/'earlier-registration.json').write_text(json.dumps({'frames_1based':frames,'crop_xyxy':box,'transforms':meta},indent=2))
print(meta)
