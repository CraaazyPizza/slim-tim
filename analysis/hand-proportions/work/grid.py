import numpy as np, sys
from PIL import Image, ImageDraw

def render(arr, x0, y0, scale, path, step=20, lo=None, hi=None, gamma=1.0, gridcol=(255,255,0)):
    a=arr.astype(float)
    if lo is None: lo,hi=np.percentile(a,[1,99])
    n=np.clip((a-lo)/(hi-lo),0,1)**gamma
    im=Image.fromarray((n*255).astype(np.uint8)).convert('RGB')
    im=im.resize((im.width*scale, im.height*scale), Image.LANCZOS)
    d=ImageDraw.Draw(im)
    for gx in range(0, arr.shape[1], step):
        X=gx*scale
        d.line([(X,0),(X,im.height)], fill=gridcol if (gx//step)%5 else (255,80,80), width=1)
        if (gx//step)%5==0: d.text((X+2,2), str(x0+gx), fill=(255,80,80))
    for gy in range(0, arr.shape[0], step):
        Y=gy*scale
        d.line([(0,Y),(im.width,Y)], fill=gridcol if (gy//step)%5 else (255,80,80), width=1)
        if (gy//step)%5==0: d.text((2,Y+2), str(y0+gy), fill=(255,80,80))
    im.save(path); return im.size
