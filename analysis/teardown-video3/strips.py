import numpy as np, json, sys
from PIL import Image, ImageDraw
D='/home/user/new-skinny-bob/frames/l9RAhmPHM_A'
X0,X1,Y0,Y1=462,975,936,1002
def strip(i):
    a=np.array(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(np.float32)
    s=a[Y0:Y1,X0:X1]
    lo=np.percentile(s,25); hi=np.percentile(s,99.0)
    q=np.clip((s-lo)/max(hi-lo,1.0),0,1)
    return (q*255).astype('uint8')
start,end,step,tag=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
fs=list(range(start,end,step))
W=513; H=66; SC=0.78
w=int(W*SC); h=int(H*SC)
cols=4
rows=(len(fs)+cols-1)//cols
LBL=90
out=Image.new('L',(cols*(w+LBL), rows*(h+4)),40)
d=ImageDraw.Draw(out)
for n,i in enumerate(fs):
    r,c=divmod(n,cols)
    t=Image.fromarray(strip(i)).resize((w,h),Image.LANCZOS)
    out.paste(t,(c*(w+LBL)+LBL, r*(h+4)))
    d.text((c*(w+LBL)+3, r*(h+4)+h//2-6), f'{i}', fill=255)
out.save(f'/home/user/new-skinny-bob/analysis/teardown-video3/strips_{tag}.png')
print(out.size, len(fs))
