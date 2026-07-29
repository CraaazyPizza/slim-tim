import numpy as np, sys
from PIL import Image, ImageDraw, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
def enh(f,box):
    im=Image.open(F.format(f)).convert('L').crop((box[0]-20,box[1]-20,box[2]+20,box[3]+20))
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(5))).astype(np.float32)
    d=a-bg
    s=np.sqrt(np.asarray(Image.fromarray(np.clip(np.abs(d)*8,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(20))).astype(np.float32)/8)+0.8
    d=d/s
    d=np.clip(d*70+128,0,255)
    out=Image.fromarray(d.astype(np.uint8)).crop((20,20,20+box[2]-box[0],20+box[3]-box[1]))
    return out
def go(frames,out,box,cols,scale):
    w=int((box[2]-box[0])*scale); h=int((box[3]-box[1])*scale)+14
    rows=(len(frames)+cols-1)//cols
    c=Image.new('L',(cols*w,rows*h),0); d=ImageDraw.Draw(c)
    for i,f in enumerate(frames):
        x=(i%cols)*w; y=(i//cols)*h
        c.paste(enh(f,box).resize((w,h-14),Image.LANCZOS),(x,y+14))
        d.text((x+2,y+2),str(f),fill=255)
    c.save(out); print(out,c.size)
go(eval(sys.argv[1]),sys.argv[2],eval(sys.argv[3]),int(sys.argv[4]),float(sys.argv[5]))
