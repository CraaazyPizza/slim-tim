import os, json, subprocess
from PIL import ImageFont
NEED = 'ПредыущсобнимеАРОТХЛДГЕ'
out = subprocess.run(['fc-list',':lang=ru','file','family','style'],capture_output=True,text=True).stdout
cands = {}
for ln in out.strip().split('\n'):
    if ':' not in ln: continue
    fp = ln.split(':')[0].strip()
    rest = ln.split(':',1)[1]
    if not os.path.exists(fp): continue
    try:
        f = ImageFont.truetype(fp, 48)
        ok = all(f.getbbox(c)[2] > f.getbbox(c)[0] for c in NEED)
        # reject fonts that render .notdef boxes: compare 'Ж' bitmap vs a private-use char
        import numpy as np
        from PIL import Image, ImageDraw
        def bm(c):
            im=Image.new('L',(80,80),255); ImageDraw.Draw(im).text((5,60),c,font=f,fill=0,anchor='ls')
            return np.asarray(im)
        if ok and np.abs(bm('Ж').astype(int)-bm('').astype(int)).sum() < 100: ok=False
    except Exception:
        ok = False
    if ok:
        try:
            nm = f.getname(); key = (nm[0]+' '+nm[1]).strip()
        except Exception: key = os.path.basename(fp)
        cands[key] = fp
json.dump(cands, open('fonts.json','w'), indent=1, ensure_ascii=False)
print(len(cands),'Cyrillic-capable faces with full coverage of', NEED)
for k in sorted(cands): print('  %-42s %s'%(k,cands[k]))
