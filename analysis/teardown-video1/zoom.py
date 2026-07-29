import sys,numpy as np
from PIL import Image, ImageDraw
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
def go(frames,box,out,cols,scale,eq=True):
    w=int((box[2]-box[0])*scale); h=int((box[3]-box[1])*scale)
    rows=(len(frames)+cols-1)//cols
    c=Image.new('L',(cols*w,rows*(h+16)),0); d=ImageDraw.Draw(c)
    for i,f in enumerate(frames):
        im=Image.open(F.format(f)).convert('L').crop(box)
        a=np.asarray(im).astype(np.float32)
        if eq:
            lo,hi=np.percentile(a,[1,99]); a=np.clip((a-lo)/(hi-lo+1e-6)*255,0,255)
        im=Image.fromarray(a.astype(np.uint8)).resize((w,h),Image.LANCZOS)
        x=(i%cols)*w; y=(i//cols)*(h+16)
        c.paste(im,(x,y+16)); d.text((x+3,y+3),str(f),fill=255)
    c.save(out); print(out,c.size)
if __name__=='__main__':
    go(eval(sys.argv[1]),eval(sys.argv[2]),sys.argv[3],int(sys.argv[4]),float(sys.argv[5]), (len(sys.argv)<7 or sys.argv[6]!='noeq'))
