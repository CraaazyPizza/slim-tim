import numpy as np, os
from PIL import Image
FR='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f%05d.png'
def rd(n, gray=True):
    im=Image.open(FR%n)
    a=np.asarray(im).astype(np.float32)
    if gray:
        if a.ndim==3: a=0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]
        return a
    return a
def save(a,p,lo=None,hi=None):
    a=np.asarray(a,dtype=np.float32)
    if lo is None: lo=np.percentile(a,0.5)
    if hi is None: hi=np.percentile(a,99.5)
    if hi<=lo: hi=lo+1
    b=np.clip((a-lo)/(hi-lo)*255,0,255).astype(np.uint8)
    Image.fromarray(b).save(p); return p
