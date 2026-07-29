import numpy as np, json, sys
from PIL import Image, ImageDraw
D='frames/Oqw96jCOP7A'
runs=json.load(open('analysis/teardown-video2/runs_SEC.json'))
# representative frame = middle of run
reps=[(a,b,(a+b)//2) for a,b in runs]
BOX=(300,930,1060,1000)  # includes bar + full text
rows=[]
for a,b,m in reps:
    im=Image.open(f'{D}/f{m:05d}.png').convert('L').crop(BOX)
    x=np.asarray(im).astype(float)
    lo,hi=np.percentile(x,[2,99]); x=np.clip((x-lo)/(hi-lo+1e-9)*255,0,255)
    rows.append((a,b,m,Image.fromarray(x.astype(np.uint8))))
W=BOX[2]-BOX[0]; H=BOX[3]-BOX[1]
per=22
for k in range(0,len(rows),per):
    ch=rows[k:k+per]
    canvas=Image.new('L',(W+220,H*len(ch)),0)
    d=ImageDraw.Draw(canvas)
    for j,(a,b,m,im) in enumerate(ch):
        canvas.paste(im,(220,j*H))
        d.text((6,j*H+H//2-6), f'f{a}-{b} n={b-a+1} @{m}', fill=255)
    canvas=canvas.resize(((W+220)*2,H*len(ch)*2),Image.LANCZOS)
    canvas.save(f'analysis/teardown-video2/tc_{k//per:02d}.png')
print('made', (len(rows)+per-1)//per, 'montages;', len(rows),'runs')
