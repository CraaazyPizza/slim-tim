"""Figure - the "#020202 hidden dots" resolved: two AV1 tile-corner blocks."""
import numpy as np, subprocess
from PIL import Image, ImageDraw, ImageFont
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FM='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
def f(p,s): return ImageFont.truetype(p,s)
subprocess.run(['ffmpeg','-v','error','-i','videos/2026/OpSTlDJWFFI.mkv','-vf','select=eq(n\\,2990)',
                '-vsync','0','-pix_fmt','yuv420p','-f','rawvideo','/tmp/vq7/one.yuv','-y'],check=True)
Y=np.fromfile('/tmp/vq7/one.yuv',dtype=np.uint8)[:1920*1080].reshape(1080,1920)
INK='#181820'; AC='#b04424'; MUT='#70727a'
# --- line profile panel via matplotlib
fig,ax=plt.subplots(figsize=(12.4,2.7),dpi=100)
ax.step(np.arange(1920),Y[8].astype(int),where='mid',lw=1.4,color=AC)
ax.set_xlim(-10,1930); ax.set_ylim(15.6,17.4)
ax.set_yticks([16,17]); ax.set_yticklabels(['Y = 16  (black)','Y = 17'],fontsize=15)
ax.set_xticks([0,240,480,720,960,1200,1440,1680,1920]); ax.tick_params(labelsize=14)
ax.set_xlabel('pixel column across the 1920-px-wide frame',fontsize=15,color=MUT)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.spines['left'].set_color('#c8c8ce'); ax.spines['bottom'].set_color('#c8c8ce')
ax.grid(axis='y',color='#e8e8ec'); ax.set_axisbelow(True)
ax.annotate('columns 0–31',xy=(16,17),xytext=(120,17.22),fontsize=15,color=INK,
            arrowprops=dict(arrowstyle='->',color=INK,lw=1.2))
ax.annotate('columns 960–991',xy=(975,17),xytext=(1080,17.22),fontsize=15,color=INK,
            arrowprops=dict(arrowstyle='->',color=INK,lw=1.2))
fig.tight_layout(pad=0.4); fig.savefig('/tmp/vq7/prof.png'); plt.close(fig)
prof=Image.open('/tmp/vq7/prof.png').convert('RGB')

W=1360
IMG=Image.new("RGB",(W,900),(255,255,255)); d=ImageDraw.Draw(IMG)
Ink=(24,24,32); Mut=(112,114,122); Ac=(176,68,36); RULE=(206,206,212)
d.text((36,22),'What the "hidden dots" in the black frames actually are',font=f(FB,31),fill=Ink)
d.text((36,62),'A fully black frame of 2026 video 1, decoded straight from YouTube\'s AV1 stream (frame 2990).',font=f(FR,20),fill=Mut)
# Panel A: top 48 rows of the difference map, stretched
mp=(Y>Y.min())[:48]
im=Image.fromarray((mp*255).astype('uint8')).resize((1288,96),Image.BOX)
IMG.paste(Image.merge('RGB',(im,im,im)),(36,116))
d.rectangle([36,116,36+1288,116+96],outline=RULE)
for bx in (0,960):
    x0=36+int(bx*1288/1920)-3; x1=36+int((bx+32)*1288/1920)+3
    d.rectangle([x0,113,x1,116+99],outline=(220,60,30),width=3)
d.text((36,220),'top 48 rows of the frame. White = any pixel that is not the frame minimum. 2,048 pixels out of 2,073,600.',font=f(FR,19),fill=Mut)
# Panel B: profile
IMG.paste(prof.resize((1288,int(prof.height*1288/prof.width))),(36,256))
h2=256+int(prof.height*1288/prof.width)
d.text((36,h2+4),'the luma value along row 8: two square pulses, one code value high, on the encoder\'s 960-px tile boundary.',font=f(FR,19),fill=Mut)
# Panel C: the three facts
y=h2+46
d.rectangle([36,y,W-36,y+206],fill=(246,246,249))
def bullet(yy,head,body):
    d.text((58,yy),head,font=f(FB,20),fill=Ac)
    d.text((58,yy+26),body,font=f(FR,18),fill=Ink)
bullet(y+16,'The two blocks are bit-identical.',
       'The right block is the left block translated by exactly +960 px — not mirrored. It tracks the codec, not the picture.')
bullet(y+78,'The same two blocks sit at the same coordinates in the 2011 files.',
       'Both eras are modern YouTube AV1 encodes, so the "cross-era pixel match" that looked like a file-lineage link is the encoder.')
bullet(y+140,'Confirmed independently, from a second codec.',
       'An outside analyst\'s AVC download of the same upload has these 2,048 pixels at 0 on all 16 black frames; ours has them at 1.')
IMG.crop((0,0,W,y+252)).save('figs/technical/fig_tile_corners.png')
print('ok')
