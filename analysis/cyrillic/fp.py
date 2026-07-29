"""Scale-free letterform FINGERPRINT test: three dimensionless ratios measured off
the pixels, compared against every installed Cyrillic-capable face."""
import numpy as np, json, sys
from PIL import Image, ImageDraw, ImageFont
FONTS=json.load(open('/home/user/new-skinny-bob/analysis/cyrillic/fonts.json'))
TEXT='Предыдущее сообщение'
SZ=200      # render big, measure, ratios are scale-free

def measure(fp):
    try: f=ImageFont.truetype(fp,SZ)
    except Exception: return None
    def ink(txt):
        b=f.getbbox(txt)
        if b[2]<=b[0]: return None
        W=b[2]-b[0]+20; H=b[3]-b[1]+20
        im=Image.new('L',(W+40,H+40),255); d=ImageDraw.Draw(im)
        d.text((20-b[0],20-b[1]),txt,font=f,fill=0)
        a=255-np.asarray(im,dtype=float)
        cols=np.where(a.sum(0)>0)[0]; rows=np.where(a.sum(1)>0)[0]
        return a,cols,rows
    r=ink('П');  rП=r
    if r is None: return None
    aП,cП,rП2=r
    cap = rП2.max()-rП2.min()+1
    ro=ink('о')
    if ro is None: return None
    ao,co,rowso=ro
    xh = rowso.max()-rowso.min()+1
    rt=ink(TEXT)
    if rt is None: return None
    at,ct,rt2=rt
    width = ct.max()-ct.min()+1
    # stem width: mid-height row of 'П' left stem, run length
    mid=(rП2.min()+rП2.max())//2
    row=aП[mid]>127
    idx=np.where(row)[0]
    if len(idx)==0: return None
    a0=idx[0]; e=a0
    while e+1<len(row) and row[e+1]: e+=1
    stem = e-a0+1
    # 'о' bowl stroke width, horizontal at mid
    rowo=ao[(rowso.min()+rowso.max())//2]>127
    io=np.where(rowo)[0]
    if len(io): 
        a1=io[0]; e1=a1
        while e1+1<len(rowo) and rowo[e1+1]: e1+=1
        obow=e1-a1+1
    else: obow=np.nan
    return dict(cap=cap, xh=xh, width=width, stem=stem, obow=obow,
                xh_cap=xh/cap, w_cap=width/cap, stem_cap=stem/cap, obow_cap=obow/cap)

# measured targets (metrics2.py, f983 / best5 average; PSF sigma ~1.0 px deconvolved)
M = dict(cap=68.3, xh=40.05, width=1152.7, stem=11.4, obow=None)
T = dict(xh_cap=40.05/68.3, w_cap=1152.7/68.3, stem_cap=11.4/68.3)
E = dict(xh_cap=0.020, w_cap=0.40, stem_cap=0.012)     # 1-sigma uncertainties
print('MEASURED  x-height/cap = %.3f   width/cap = %.2f   stem/cap = %.3f'%(T['xh_cap'],T['w_cap'],T['stem_cap']))
print('(cap=%.1f px, xh=%.1f px, ink width=%.1f px, stem FWHM=%.1f px)\n'%(M['cap'],M['xh'],M['width'],M['stem']))
rows=[]
for n,fp in FONTS.items():
    m=measure(fp)
    if m is None: continue
    chi = sum(((m[k]-T[k])/E[k])**2 for k in T)
    rows.append(dict(font=n,file=fp,chi2=chi,**{k:m[k] for k in ('xh_cap','w_cap','stem_cap','obow_cap')}))
rows.sort(key=lambda d:d['chi2'])
print('%-40s %9s %9s %9s %9s'%('face','chi2','xh/cap','w/cap','stem/cap'))
for d in rows[:30]:
    print('%-40s %9.1f %9.3f %9.2f %9.3f'%(d['font'],d['chi2'],d['xh_cap'],d['w_cap'],d['stem_cap']))
print('\n--- where the named candidates land ---')
NAMED=['Roboto Medium','Roboto Regular','Roboto Bold','DejaVu Sans Bold','DejaVu Sans Book',
 'Liberation Sans Bold','Liberation Sans Regular','Arimo Bold','Arimo Regular','Open Sans Regular',
 'Open Sans Semibold','Open Sans Bold','Noto Sans Regular','Noto Sans Bold','Lato Bold','Lato Regular',
 'Carlito Bold','Cantarell Bold','Comfortaa Bold','URW Gothic Demi','Nimbus Sans Bold','FreeSans Bold']
idx={d['font']:i for i,d in enumerate(rows)}
for n in NAMED:
    if n in idx:
        d=rows[idx[n]]
        print('  #%-4d %-32s chi2=%9.1f  xh/cap %.3f  w/cap %.2f  stem/cap %.3f'%(idx[n]+1,n,d['chi2'],d['xh_cap'],d['w_cap'],d['stem_cap']))
    else: print('  %-32s NOT INSTALLED / unmeasurable'%n)
json.dump(rows,open('/home/user/new-skinny-bob/analysis/cyrillic/fp.json','w'),indent=1,ensure_ascii=False)
