"""Figure - the film-damage layer is a separate overlay: it keeps playing after the
picture and the burned-in timecode have both cut to black."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def f(p,s): return ImageFont.truetype(p,s)
FD='frames/Oqw96jCOP7A'
def fr(i): return np.asarray(Image.open('%s/f%05d.png'%(FD,i)).convert('L')).astype(np.float32)
# plate segmentation at threshold 40
ks=list(range(2423,2459))
plates=[[2423]] if False else None
groups=[[ks[0]]]
for a,b in zip(ks[:-1],ks[1:]):
    if float(np.abs(fr(a)-fr(b)).max())<=40: groups[-1].append(b)
    else: groups.append([b])
lens=[len(g) for g in groups]
print('plate lengths',lens)
W=1360
IMG=Image.new("RGB",(W,1200),(255,255,255)); d=ImageDraw.Draw(IMG)
Ink=(24,24,32); Mut=(112,114,122); Ac=(176,68,36); Ac2=(34,90,156); RULE=(206,206,212)
d.text((36,22),'The film damage is a separate layer, laid on afterwards',font=f(FB,31),fill=Ink)
d.text((36,62),'2026 video 2. At frame 2423 the picture and the burned-in timecode both vanish in a single frame. The dirt does not.',font=f(FR,20),fill=Mut)
# Row 1: before/after the cut
y=116
def th(i,gain,w=300):
    a=np.clip(fr(i)*gain,0,255).astype('uint8')
    return Image.fromarray(a).resize((w,int(w*1080/1920)),Image.LANCZOS).convert('RGB')
labs=[(2421,1.0,'f2421  — picture + timecode'),(2422,1.0,'f2422  — last normal frame'),
      (2423,1.0,'f2423  — one frame later'),(2423,4.5,'f2423  at 4.5× gain')]
for k,(i,g,lab) in enumerate(labs):
    x=36+k*332
    IMG.paste(th(i,g),(x,y)); d.rectangle([x,y,x+300,y+169],outline=RULE)
    d.text((x,y+176),lab,font=f(FR,17),fill=Ac if k==3 else Ink)
d.text((36,y+206),'The frame is black — mean luma 0.04 of 255 — yet several thousand pixels still carry dirt, up to value 80.',font=f(FR,19),fill=Mut)
# Row 2: the 36 black frames, dirt only, at high gain
y2=y+248
d.text((36,y2),'The first twelve of those black frames — every pixel above value 8, shown white',font=f(FB,23),fill=Ink)
y2+=36
def binmap(i,w=204,thr=8):
    a=np.asarray(Image.open('%s/f%05d.png'%(FD,i)).convert('L'))
    m=(a>thr).astype(np.uint8)*255
    from scipy import ndimage
    m=ndimage.maximum_filter(m,4)
    return Image.fromarray(m).resize((w,int(w*1080/1920)),Image.LANCZOS).convert('RGB')
tw=204; th2=int(tw*1080/1920)
for k,i in enumerate(range(2423,2435)):
    col=k%6; row=k//6
    x=36+col*216; yy=y2+row*(th2+30)
    IMG.paste(binmap(i),(x,yy)); d.rectangle([x,yy,x+tw,yy+th2],outline=RULE)
    d.text((x+2,yy+th2+4),'f%d'%i,font=f(FR,19),fill=Mut)
y3=y2+2*(th2+30)+6
d.text((36,y3),'A new dirt plate every few frames, for 36 frames. At frame 2459 the dirt stops and the frame goes to true black (no pixel above 2).',font=f(FR,19),fill=Mut)
# Row 3: plate-length plot
fig,ax=plt.subplots(figsize=(12.4,2.0),dpi=100)
xs=[];ys=[]
for g in groups:
    for j,i in enumerate(g): xs.append(i); ys.append(len(g))
ax.step(xs,ys,where='mid',color='#b04424',lw=1.8)
ax.set_ylim(0,4.4); ax.set_yticks([1,2,3]); ax.set_xlim(2422,2459)
ax.set_ylabel('frames per\ndirt plate',fontsize=14,color='#70727a')
ax.set_xlabel('frame number',fontsize=14,color='#70727a')
ax.tick_params(labelsize=13)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.grid(axis='y',color='#e8e8ec'); ax.set_axisbelow(True)
ax.text(2424.5,3.6,'3, 2, 2   3, 2, 2   3, 2, 2   3, 2, 2   3, 2, 2      — period 7 frames',fontsize=13,color='#181820')
fig.tight_layout(pad=0.4); fig.savefig('/tmp/vq7/plate.png'); plt.close(fig)
p=Image.open('/tmp/vq7/plate.png').convert('RGB')
IMG.paste(p.resize((1288,int(p.height*1288/p.width))),(36,y3+30))
y4=y3+30+int(p.height*1288/p.width)+10
d.rectangle([36,y4,W-36,y4+104],fill=(246,246,249))
d.text((58,y4+14),'A 7-frame cycle is not a whole fraction of the 45-frame timecode tick.',font=f(FB,21),fill=Ac)
d.text((58,y4+46),'So the dirt cannot be dirt on the film that the timecode is counting. It was added after the fact.',font=f(FR,19),fill=Ink)
d.text((58,y4+70),'This says the film LOOK is manufactured. It says nothing either way about the picture underneath.',font=f(FR,19),fill=Mut)
IMG.crop((0,0,W,y4+120)).save('figs/technical/fig_dirt_layer.png')
print('ok')
