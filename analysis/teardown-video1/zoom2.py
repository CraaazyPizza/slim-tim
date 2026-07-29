import sys,numpy as np
from PIL import Image, ImageDraw, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
def clahe_ish(a,tile=32,clip=2.0):
    # simple local contrast: (a - local mean)/local std normalized
    im=Image.fromarray(a.astype(np.uint8))
    m=np.asarray(im.filter(ImageFilter.GaussianBlur(tile))).astype(np.float32)
    d=a-m
    s=np.sqrt(np.asarray(Image.fromarray(np.clip(d*d,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(tile))).astype(np.float32))+3
    out=128+d/s*40
    return np.clip(out,0,255)
frames=eval(sys.argv[1]); box=eval(sys.argv[2]); out=sys.argv[3]; cols=int(sys.argv[4]); sc=float(sys.argv[5])
mode=sys.argv[6] if len(sys.argv)>6 else 'pct'
w=int((box[2]-box[0])*sc); h=int((box[3]-box[1])*sc)
rows=(len(frames)+cols-1)//cols
c=Image.new('L',(cols*w,rows*(h+16)),0); d=ImageDraw.Draw(c)
for i,f in enumerate(frames):
    a=np.asarray(Image.open(F.format(f)).convert('L').crop(box)).astype(np.float32)
    if mode=='pct':
        lo,hi=np.percentile(a,[2,98]); a=np.clip((a-lo)/(hi-lo+1e-6)*255,0,255)
    elif mode=='loc':
        a=clahe_ish(a)
    im=Image.fromarray(a.astype(np.uint8)).resize((w,h),Image.LANCZOS)
    x=(i%cols)*w; y=(i//cols)*(h+16)
    c.paste(im,(x,y+16)); d.text((x+3,y+3),str(f),fill=255)
c.save(out); print(out,c.size)
