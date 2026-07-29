import numpy as np, sys
from PIL import Image, ImageDraw, ImageFilter
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
def enh(f,box):
    im=Image.open(F.format(f)).convert('L').crop(box)
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(9))).astype(np.float32)
    d=a-bg; d=np.clip((d+12)/24*255,0,255)
    return Image.fromarray(d.astype(np.uint8))
def montage(frames,out,box,scale=1.6):
    w=box[2]-box[0]; h=box[3]-box[1]
    tw=int(w*scale); th=int(h*scale)
    canvas=Image.new('L',(tw+80,th*len(frames)),0); d=ImageDraw.Draw(canvas)
    for i,f in enumerate(frames):
        canvas.paste(enh(f,box).resize((tw,th),Image.LANCZOS),(80,i*th))
        d.text((4,i*th+th//2-4),str(f),fill=255)
    canvas.save(out); print(out,canvas.size)
if __name__=='__main__':
    fr=eval(sys.argv[1]); out=sys.argv[2]; box=eval(sys.argv[3])
    sc=float(sys.argv[4]) if len(sys.argv)>4 else 1.6
    montage(fr,out,box,sc)
