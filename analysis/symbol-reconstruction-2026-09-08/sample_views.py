#!/usr/bin/env python3.12
"""Reproduce temporally separate, unmodified AVC frame sampling overview."""
from pathlib import Path
import subprocess
from PIL import Image,ImageDraw
p=Path(__file__).resolve().parent
source=p.parents[1]/'videos/2026-avc/l9RAhmPHM_A.mkv'
assert subprocess.check_output(['ffmpeg','-version'],text=True).startswith('ffmpeg version 4.4.2-')
subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',"select='eq(n,1209)+eq(n,1349)+eq(n,1499)+eq(n,1599)+eq(n,1709)'",'-vsync','0',str(p/'raw/sample-%02d.png')],check=True)
canvas=Image.new('RGB',(960,5*565),'white')
for i,n in enumerate([1210,1350,1500,1600,1710]):
 im=Image.open(p/'raw'/f'sample-{i+1:02}.png');canvas.paste(im.resize((960,540)),(0,i*565+25));ImageDraw.Draw(canvas).text((5,i*565+5),f'Raw AVC frame {n}; downscaled overview',fill='black')
canvas.save(p/'temporal-samples-overview.jpg')
