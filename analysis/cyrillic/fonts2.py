"""Rebuild the font inventory including the newly installed faces and, for the
variable fonts, one entry per named weight instance."""
import os, json, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
NEED='ПАБВГРСЕТХЛДадеипрсуыщюёжбнмок'
out=subprocess.run(['fc-list',':lang=ru','file','family','style'],capture_output=True,text=True).stdout
files=set()
for ln in out.strip().split('\n'):
    if ':' in ln:
        fp=ln.split(':')[0].strip()
        if os.path.exists(fp): files.add(fp)
def ok(f):
    try:
        if not all(f.getbbox(c)[2]>f.getbbox(c)[0] for c in NEED): return False
        def bm(c):
            im=Image.new('L',(90,90),255); ImageDraw.Draw(im).text((5,70),c,font=f,fill=0,anchor='ls')
            return np.asarray(im).astype(int)
        return np.abs(bm('Ж')-bm('')).sum()>=100
    except Exception: return False
cands={}
for fp in sorted(files):
    try: f=ImageFont.truetype(fp,48)
    except Exception: continue
    if not ok(f): continue
    try: nm=(f.getname()[0]+' '+f.getname()[1]).strip()
    except Exception: nm=os.path.basename(fp)
    cands[nm]=fp
json.dump(cands,open('fonts2.json','w'),indent=1,ensure_ascii=False)
print(len(cands),'faces with full coverage of',NEED)
NEWD=os.path.expanduser('~/.local/share/fonts/cyr_test/')
print('\nnewly installed, present in the inventory:')
for k,v in sorted(cands.items()):
    if v.startswith(NEWD): print('   %-30s %s'%(k,os.path.basename(v)))
