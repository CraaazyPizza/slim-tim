import numpy as np, sys
from PIL import Image, ImageDraw
D='/home/user/new-skinny-bob/frames/l9RAhmPHM_A'
fs=[int(x) for x in sys.argv[1].split(',')]
tag=sys.argv[2]; boost=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
W,H=470,352
cols=4; rows=(len(fs)+cols-1)//cols
out=Image.new('L',(cols*W, rows*(H+16)),0)
d=ImageDraw.Draw(out)
for n,i in enumerate(fs):
    a=np.array(Image.open(f'{D}/f{i:05d}.png').convert('L')).astype(np.float32)
    a=a[40:1060,250:1610]
    if boost!=1.0:
        a=np.clip((a/255.0)**(1/boost)*255,0,255)
    t=Image.fromarray(a.astype('uint8')).resize((W,H),Image.LANCZOS)
    r,c=divmod(n,cols)
    out.paste(t,(c*W,r*(H+16)+16))
    d.text((c*W+4, r*(H+16)+3), f'f{i}', fill=255)
out.save(f'/home/user/new-skinny-bob/analysis/teardown-video3/mont_{tag}.png')
print(out.size)
