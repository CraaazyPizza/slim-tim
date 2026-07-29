"""§3.2 RE-RUN with the six newly installed faces, plus a stem-constrained fit.

Two tests:
  UNCONSTRAINED  free cap height + free kx, PSF fixed at the measured 0.9 px.
  STEM-CONSTRAINED  kx is not free: the measured stretched stem/cap = 0.2217 and the
      stretch acts on x only, so the intrinsic stem/cap of the true face must equal
      0.2217/kx.  Each candidate therefore PREDICTS its own kx, and the image fit has
      to work at that kx.  Agreement between the predicted and the fitted kx is an
      independent test that costs the candidate a degree of freedom.
"""
import numpy as np, sys, json, os, time
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
import fastvar
from c4 import *
from fast import Field, base_render, place, capsize
from vfonts import stem_cap
from fast import _font

R_STRETCHED = 0.2217           # measured stretched stem/cap (realstem.py)
R_ERR       = 0.009            # 1 sigma on that ratio (~4%)
SIG_PSF     = 0.9
RB=(902,1002); XB=(430,1615); TXT='Предыдущее сообщение'
ALL=json.load(open('fonts2.json'))
VD=os.path.expanduser('~/.local/share/fonts/cyr_test/')
VAR={'Inter':(VD+'Inter.ttf',[('opsz',14.0),('opsz',32.0)],range(300,901,25)),
     'Golos Text':(VD+'GolosText.ttf',[(None,None)],range(400,901,25)),
     'Rubik':(VD+'Rubik.ttf',[(None,None)],range(300,901,25)),
     'Montserrat':(VD+'Montserrat.ttf',[(None,None)],range(200,901,25))}
CAND={}
for n,fp in ALL.items():
    if fp.startswith(VD) and os.path.basename(fp) in ('Inter.ttf','GolosText.ttf','Rubik.ttf','Montserrat.ttf'):
        continue                                    # handled as instances below
    CAND[n]=fp
for fam,(fp,opsl,wl) in VAR.items():
    for tag,ov in opsl:
        for w in wl:
            spec=fp+'#wght=%d'%w + (',opsz=%d'%ov if tag=='opsz' else '')
            nm='%s w%d'%(fam,w) + (' opsz%d'%ov if tag=='opsz' else '')
            CAND[nm]=spec
print('candidates:',len(CAND),' (of which variable instances: %d)'%sum(1 for v in CAND.values() if '#' in v))

# ---- intrinsic stem/cap and the kx it predicts, per candidate
def sf(spec):
    try:
        sc=stem_cap(_font(spec,400))
        if sc is None or sc[0]<=0: return None
        return sc[1]/sc[0]
    except Exception: return None
META={}
for n,spec in CAND.items():
    s=sf(spec)
    if s is None or s<=0.02: continue
    META[n]=dict(spec=spec, sf=s, kx_pred=R_STRETCHED/s,
                 kx_lo=(R_STRETCHED-R_ERR)/s, kx_hi=(R_STRETCHED+R_ERR)/s)
print('measurable:',len(META))

LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
def field(fs):
    o=(-RESL[[FR.index(f) for f in fs]].mean(0))[(RB[0]-Y0):(RB[1]-Y0),(XB[0]-X0):(XB[1]-X0)]
    return Field(o,*o.shape)
OBS={'f983':field([983]),'best5':field([983,973,974,984,981]),
     'NULL20':field(list(range(1010,1030))),'NULL1':field([1020])}
CAPS=[50,51.5,53,54.5,56]
KXFREE=np.round(np.arange(1.06,1.63,0.03),2)

def fit(fl,spec,kxs,caps=CAPS):
    best=None
    for cap in caps:
        sz=capsize(spec,cap); A=base_render(spec,TXT,sz)
        for kx in kxs:
            if kx<=0.4 or kx>2.2: continue
            ink=place(A,kx,fl.H,fl.W)
            for r,bl,dx,dy in fl.match(ink,[SIG_PSF],dxr=40):
                if best is None or r>best[0]: best=(r,cap,float(kx),int(dx),int(dy))
    return best

t0=time.time(); RES={}
for tag,fl in OBS.items():
    rows=[]
    for n,m in META.items():
        a=fit(fl,m['spec'],KXFREE)
        kxs=[k for k in (m['kx_lo'],m['kx_pred'],m['kx_hi']) if 0.5<=k<=2.2]
        b=fit(fl,m['spec'],kxs) if kxs else None
        rows.append(dict(font=n,spec=m['spec'],sf=m['sf'],kx_pred=m['kx_pred'],
                         r_free=a[0],cap_free=a[1],kx_free=a[2],
                         r_con=(b[0] if b else float('nan')),
                         cap_con=(b[1] if b else float('nan')),
                         kx_con=(b[2] if b else float('nan')),
                         dkx=abs(a[2]-m['kx_pred'])))
    rows.sort(key=lambda d:-d['r_free']); RES[tag]=rows
    print('\n===== %s  (%.0fs) ====='%(tag,time.time()-t0))
    print('%-30s %8s %5s %5s | %8s %5s | %6s %6s'%('face','r_free','cap','kx','r_stem','kx*','stem/cap','dkx'))
    for d in rows[:28]:
        print('%-30s %8.4f %5.1f %5.2f | %8.4f %5.2f | %8.4f %6.2f'%(
            d['font'],d['r_free'],d['cap_free'],d['kx_free'],d['r_con'],d['kx_con'],d['sf'],d['dkx']))
    sys.stdout.flush()
    json.dump(RES,open('sweep3.json','w'),indent=1,ensure_ascii=False)
print('\ntotal %.0fs'%(time.time()-t0))
