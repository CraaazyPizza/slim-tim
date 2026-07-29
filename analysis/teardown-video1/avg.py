import numpy as np,sys
from PIL import Image, ImageDraw
F='/home/user/new-skinny-bob/frames/OpSTlDJWFFI/f{:05d}.png'
groups=eval(sys.argv[1]); box=eval(sys.argv[2]); out=sys.argv[3]; sc=float(sys.argv[4])
w=int((box[2]-box[0])*sc); h=int((box[3]-box[1])*sc)
c=Image.new('L',(len(groups)*w,h+16),0); d=ImageDraw.Draw(c)
for i,gr in enumerate(groups):
    A=np.mean([np.asarray(Image.open(F.format(f)).convert('L')).astype(np.float64)[box[1]:box[3],box[0]:box[2]] for f in gr],0)
    lo,hi=np.percentile(A,[1.5,98.5]); A=np.clip((A-lo)/(hi-lo)*255,0,255)
    c.paste(Image.fromarray(A.astype(np.uint8)).resize((w,h),Image.LANCZOS),(i*w,16))
    d.text((i*w+3,3),'%d-%d (n=%d)'%(gr[0],gr[-1],len(gr)),fill=255)
c.save(out); print(out,c.size)
