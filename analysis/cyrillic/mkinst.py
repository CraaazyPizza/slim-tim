import numpy as np, os, glob
from fontTools.varLib import instancer
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
OUT=os.path.expanduser('~/.local/share/fonts/cyr_test'); TARGET=0.223
def stem_cap_var(fp, w=None, opsz=None):
    f=ImageFont.truetype(fp,200)
    if w is not None:
        try:
            axes=[a['name'].decode() if isinstance(a['name'],bytes) else str(a['name']) for a in f.get_variation_axes()]
            vals=[]
            for a in f.get_variation_axes():
                nm=a['name'].decode() if isinstance(a['name'],bytes) else str(a['name'])
                vals.append(w if 'eight' in nm or nm=='wght' else (16 if 'ptical' in nm or nm=='opsz' else a['default']))
            f.set_variation_by_axes(vals)
        except Exception as e:
            return None
    im=Image.new('L',(400,320),255); ImageDraw.Draw(im).text((20,280),'П',font=f,fill=0,anchor='ls')
    a=255-np.asarray(im).astype(float); ys,xs=np.nonzero(a>128)
    if len(ys)==0: return None
    cap=ys.max()-ys.min()+1
    row=int(ys.min()+0.75*cap); on=np.nonzero(a[row]>128)[0]
    if len(on)==0: return None
    runs=np.split(on,np.where(np.diff(on)!=1)[0]+1)
    return float(np.mean([len(r) for r in runs]))/cap
made=[]
for vf in sorted(glob.glob(os.path.join(OUT,'*.ttf'))):
    if '_w' in os.path.basename(vf): continue
    ft=TTFont(vf, lazy=True)
    if 'fvar' not in ft:
        r=stem_cap_var(vf); print(f"  static    {os.path.basename(vf):20s} stem/cap={r:.3f}",flush=True); continue
    axes={a.axisTag:(a.minValue,a.maxValue) for a in ft['fvar'].axes}
    lo,hi=axes['wght']; best=None
    for w in range(int(lo),int(hi)+1,25):
        r=stem_cap_var(vf,w)
        if r and (best is None or abs(r-TARGET)<abs(best[1]-TARGET)): best=(w,r)
    if not best: print(f"  SKIP {os.path.basename(vf)} (no variation support)",flush=True); continue
    w,ratio=best
    nm=os.path.basename(vf).replace('.ttf','')+f"_w{w}.ttf"
    kw={'wght':w}; kw.update({'opsz':16} if 'opsz' in axes else {})
    inst=instancer.instantiateVariableFont(TTFont(vf),kw)
    fam=os.path.basename(vf).replace('.ttf','')+f" w{w}"
    for rec in inst['name'].names:
        if rec.nameID in (1,4,16): rec.string=fam
        elif rec.nameID in (2,17): rec.string="Regular"
    inst.save(os.path.join(OUT,nm)); made.append(nm)
    print(f"  instanced {nm:30s} wght={w} stem/cap={ratio:.3f} (target {TARGET})",flush=True)
print("made:",len(made))
