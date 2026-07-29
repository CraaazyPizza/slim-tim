import numpy as np, sys
from PIL import Image, ImageDraw, ImageFilter

BOX=(470,925,1040,1005)   # timecode text strip
def enh(f):
    im=Image.open(f'/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{f:05d}.png').convert('L').crop(BOX)
    a=np.asarray(im).astype(np.float32)
    bg=np.asarray(im.filter(ImageFilter.GaussianBlur(9))).astype(np.float32)
    d=a-bg
    d=(d-d.min())/(d.max()-d.min()+1e-6)*255
    return Image.fromarray(d.astype(np.uint8))

def montage(frames,out,scale=2):
    w=BOX[2]-BOX[0]; h=BOX[3]-BOX[1]
    W=int(w*scale)+90; H=int(h*scale)*len(frames)
    canvas=Image.new('L',(W,H),0); d=ImageDraw.Draw(canvas)
    for i,f in enumerate(frames):
        canvas.paste(enh(f).resize((int(w*scale),int(h*scale)),Image.LANCZOS),(90,i*int(h*scale)))
        d.text((4,i*int(h*scale)+int(h*scale)//2-4),str(f),fill=255)
    canvas.save(out)
    print(out,canvas.size)

if __name__=='__main__':
    a,b,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
    montage(list(range(a,b+1)),out)
