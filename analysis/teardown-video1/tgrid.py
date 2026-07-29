import numpy as np, sys
from PIL import Image, ImageDraw, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
def enh(f,box):
    im=Image.open(F.format(f)).convert('L').crop(box)
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(9))).astype(np.float32)
    d=a-bg; d=np.clip((d+12)/24*255,0,255)
    return Image.fromarray(d.astype(np.uint8))
def go(frames,out,box,cols=8,scale=2.2):
    w=int((box[2]-box[0])*scale); h=int((box[3]-box[1])*scale)+16
    rows=(len(frames)+cols-1)//cols
    c=Image.new('L',(cols*w,rows*h),40); d=ImageDraw.Draw(c)
    for i,f in enumerate(frames):
        x=(i%cols)*w; y=(i//cols)*h
        c.paste(enh(f,box).resize((w,h-16),Image.LANCZOS),(x,y+16))
        d.text((x+2,y+3),str(f),fill=255)
    c.save(out); print(out,c.size)
if __name__=='__main__':
    go(eval(sys.argv[1]),sys.argv[2],eval(sys.argv[3]),int(sys.argv[4]) if len(sys.argv)>4 else 8, float(sys.argv[5]) if len(sys.argv)>5 else 2.2)
