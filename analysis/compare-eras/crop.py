import sys, numpy as np
from PIL import Image
# usage: crop.py in.png out.png x0 y0 x1 y1 scale
f=sys.argv; im=Image.open(f[1]).convert('RGB')
x0,y0,x1,y1,s=int(f[3]),int(f[4]),int(f[5]),int(f[6]),int(f[7])
c=im.crop((x0,y0,x1,y1))
c=c.resize((c.width*s,c.height*s),Image.NEAREST)
c.save(f[2]); print(f[2], c.size)
