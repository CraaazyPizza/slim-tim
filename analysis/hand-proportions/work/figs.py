import numpy as np, json, os, sys
os.chdir('/home/user/new-skinny-bob/analysis/hand-proportions'); sys.path.insert(0,'work')
from PIL import Image, ImageDraw, ImageFont
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run_2026 import measure

def dot(dr,p,c,r,lab=None,off=(8,-8)):
    dr.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r],outline=c,width=3)
    if lab: dr.text((p[0]+off[0],p[1]+off[1]),lab,fill=c)

# ---------- FIG 1 : side-by-side landmarks, scaled to equal D3 cleft-to-tip length ----
norm=np.load('work/xju_norm.npy')
tips11=[t[:2] for t in json.load(open('work/xju_tips.json'))['t64']['tips']]
d11=json.load(open('work/xju_land_t64_f70.json'))
A=Image.fromarray(np.stack([np.clip(norm*230,0,255).astype(np.uint8)]*3,-1))
dr=ImageDraw.Draw(A)
for n,p in zip(['TH','D2','D3','D4'],tips11): dot(dr,p,(0,255,0),10,n)
for k in ['C23','C34']: dot(dr,d11[k],(255,60,60),11,k)
dr.line([tuple(tips11[2]),tuple(d11['C34'])],fill=(255,215,0),width=5)
dr.line([tuple(tips11[3]),tuple(d11['C34'])],fill=(255,0,255),width=5)
A=A.crop((120,0,790,1042))

r26=measure(3866,0.7)
img=np.asarray(Image.open('/home/user/new-skinny-bob/frames/l9RAhmPHM_A/f03866.png').convert('L')).astype(float)
lo,hi=np.percentile(img[330:900,540:1020],[1,99])
B=Image.fromarray(np.stack([np.clip((img-lo)/(hi-lo)*255,0,255).astype(np.uint8)]*3,-1))
dr=ImageDraw.Draw(B)
for n,k in [('D2','T2'),('D3','T3'),('D4','T4')]: dot(dr,r26['tips'][k],(0,255,0),10,n)
for k in ['C23','C34']: dot(dr,r26[k],(255,60,60),11,k)
dr.line([tuple(r26['tips']['T3']),tuple(r26['C34'])],fill=(255,215,0),width=5)
dr.line([tuple(r26['tips']['T4']),tuple(r26['C34'])],fill=(255,0,255),width=5)
B=B.crop((540,320,1030,900))
# scale B so that D3 cleft-to-tip matches A's
L11=np.linalg.norm(np.array(tips11[2])-np.array(d11['C34']))
L26=np.linalg.norm(np.array(r26['tips']['T3'])-np.array(r26['C34']))
s=L11/L26
B=B.resize((int(B.width*s),int(B.height*s)),Image.LANCZOS)
H=max(A.height,B.height)
F=Image.new('RGB',(A.width+B.width+40,H+46),(20,20,20))
F.paste(A,(0,46)); F.paste(B,(A.width+40,46))
dr=ImageDraw.Draw(F)
dr.text((10,14),'2011  ivan0135  Xju_CY5ZESA  hand-print plate (median of 97 text-free frames)',fill=(255,255,255))
dr.text((A.width+50,14),'2026  qtecqot  l9RAhmPHM_A  f03866  (scaled to equal D3 cleft-to-tip length)',fill=(255,255,255))
F.save('out/FIG1_landmarks_sidebyside.png')
print('FIG1', F.size, 'scale', round(s,3))

# ---------- FIG 2 : separation-closure profiles -------------------------------------
full=json.load(open('work/xju_land_full.json'))
fig,ax=plt.subplots(1,2,figsize=(11,4.2))
for k,c in [('C23','tab:blue'),('C34','tab:red')]:
    p=full[k+'_prof']; y=np.array(p['y']); V=np.array(p['V']); T=np.array(p['thr'])
    ax[0].plot(y,V,c,label=f'{k} gap level'); ax[0].plot(y,T,c,ls='--',lw=1,label=f'{k} 70% threshold')
    ax[0].axvline(d11[k][1],color=c,lw=1,alpha=.5)
ax[0].set_title('2011 print: paper-wedge level vs row\n(1.0 = paper, 0.28 = ink)')
ax[0].set_xlabel('image row y (crop coords)'); ax[0].set_ylabel('normalised level'); ax[0].legend(fontsize=7)
for k,c in [('C23','tab:blue'),('C34','tab:red')]:
    p=r26[k+'_prof']; y=np.array(p['y']); V=np.array(p['V']); T=np.array(p['thr'])
    ax[1].plot(y,V,c,label=f'{k} groove floor'); ax[1].plot(y,T,c,ls='--',lw=1,label=f'{k} 70% threshold')
    ax[1].axvline(r26[k][1],color=c,lw=1,alpha=.5)
ax[1].set_title('2026 f03866: inter-digital groove floor vs row\n(luma DN; skin ~150, groove ~40)')
ax[1].set_xlabel('image row y'); ax[1].set_ylabel('luma DN'); ax[1].legend(fontsize=7)
plt.tight_layout(); plt.savefig('out/FIG2_cleft_closure_profiles.png',dpi=130); plt.close()
print('FIG2 ok')

# ---------- FIG 3 : R per frame ------------------------------------------------------
rows=json.load(open('work/v3_sweep2.json'))
fig,ax=plt.subplots(figsize=(10,4.2))
cols={0.5:'tab:green',0.7:'tab:blue',0.85:'tab:orange'}
for fr in [0.5,0.7,0.85]:
    s=sorted([r for r in rows if r['frac']==fr],key=lambda r:r['frame'])
    ax.plot([r['frame'] for r in s],[r['R_shared'] for r in s],'o',ms=4,color=cols[fr],label=f'2026, closure frac={fr}')
ax.axhspan(0.666,0.686,color='crimson',alpha=.25)
ax.axhline(0.676,color='crimson',lw=2,label='2011 print  R = 0.676 (0.666-0.686)')
for a,b,lab in [(3724,3830,'B'),(3831,3878,'A'),(3879,3935,'C'),(3936,4100,'D'),(4101,4260,'E')]:
    ax.axvline(b,color='0.8',lw=.8); ax.text((a+b)/2,1.08,lab,ha='center',color='0.4')
ax.set_xlabel('video-3 frame'); ax.set_ylabel(r'$R_{shared}=|T_4-C_{34}| / |T_3-C_{34}|$')
ax.set_ylim(0.6,1.13); ax.legend(fontsize=8,loc='lower right')
ax.set_title('Little-digit / middle-digit length from the shared D3|D4 cleft')
plt.tight_layout(); plt.savefig('out/FIG3_R_per_frame.png',dpi=130); plt.close()
print('FIG3 ok')

# ---------- FIG 4 : systematic sensitivity ------------------------------------------
L4a,L3a=393.278,573.375
s26=[r for r in rows if r['frac']==0.7 and 3831<=r['frame']<=3935]
L4b=np.mean([r['L4'] for r in s26]); L3bb=np.mean([r['L3b'] for r in s26])
d=np.linspace(0,0.62,200)
fig,ax=plt.subplots(figsize=(7,4.4))
ax.plot(100*d,(L4b-d*L3bb)/(L3bb-d*L3bb),'tab:blue',label='2026, cleft moved DISTALLY by d')
ax.plot(100*d,(L4a+d*L3a)/(L3a+d*L3a),'crimson',label='2011, cleft moved PROXIMALLY by d')
ax.axhline(0.676,color='crimson',ls=':',lw=1); ax.axhline(0.870,color='tab:blue',ls=':',lw=1)
ax.axvline(58,color='k',ls='--',lw=1); ax.text(58.5,0.78,'d needed to null\nthe difference\n(58% of D3 length)',fontsize=8)
ax.set_xlabel('cleft displacement d, as % of the D3 cleft-to-tip length')
ax.set_ylabel(r'$R_{shared}$'); ax.legend(fontsize=8)
ax.set_title('Sensitivity of the result to the palmar-print vs dorsal-photo cleft offset')
plt.tight_layout(); plt.savefig('out/FIG4_cleft_sensitivity.png',dpi=130); plt.close()
print('FIG4 ok')
