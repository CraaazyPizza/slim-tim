"""Variable-font instancing + stem/cap measurement, measured the SAME way on the
real pixels and on every candidate so the systematics cancel."""
import numpy as np, os, json
from PIL import Image, ImageDraw, ImageFont
VD=os.path.expanduser('~/.local/share/fonts/cyr_test/')
VAR={'Inter':(VD+'Inter.ttf',[(14,32)],(100,900)),
     'Golos Text':(VD+'GolosText.ttf',None,(400,900)),
     'Rubik':(VD+'Rubik.ttf',None,(300,900)),
     'Montserrat':(VD+'Montserrat.ttf',None,(100,900))}
STATIC={'PT Sans Bold':VD+'PT_Sans.ttf','Fira Sans Bold':VD+'FiraSans.ttf'}

_C={}
def inst(fp,size,wght=None,opsz=None):
    """ImageFont instance; for variable fonts set the axes."""
    k=(fp,size,wght,opsz)
    if k in _C: return _C[k]
    f=ImageFont.truetype(fp,size)
    if wght is not None:
        try:
            ax=f.get_variation_axes()
            vals=[]
            for a in ax:
                nm=a['name'].decode() if isinstance(a['name'],bytes) else a['name']
                if 'Weight' in nm: vals.append(float(wght))
                elif 'Optical' in nm: vals.append(float(opsz if opsz is not None else a['default']))
                else: vals.append(float(a['default']))
            f.set_variation_by_axes(vals)
        except Exception: pass
    _C[k]=f
    return f

def stem_cap(f, SZ=None):
    """cap height and left-stem FWHM of «П», measured on a high-res render.
    Stem = FWHM of the left peak of the column profile averaged over the stem band
    (the same construction used on the real pixels)."""
    b=f.getbbox('П')
    W=b[2]-b[0]+40; H=b[3]-b[1]+40
    im=Image.new('L',(W,H),255); ImageDraw.Draw(im).text((20-b[0],20-b[1]),'П',font=f,fill=0)
    a=(255-np.asarray(im,dtype=np.float64))/255.0
    rows=np.where(a.sum(1)>0.5)[0]; cols=np.where(a.sum(0)>0.5)[0]
    if len(rows)<4 or len(cols)<4: return None
    cap=rows.max()-rows.min()+1
    # stem band: from 25% to 95% of cap height (below the top bar, above the baseline)
    y0=int(rows.min()+0.25*cap); y1=int(rows.min()+0.95*cap)
    prof=a[y0:y1].mean(0)
    m=int(np.argmax(prof[:len(prof)//2]))     # left stem peak
    h=prof[m]/2.0
    i=m
    while i>0 and prof[i-1]>=h: i-=1
    j=m
    while j<len(prof)-1 and prof[j+1]>=h: j+=1
    l = i-1+(h-prof[i-1])/(prof[i]-prof[i-1]) if i>0 and prof[i]!=prof[i-1] else i
    r = j+(prof[j]-h)/(prof[j]-prof[j+1]) if j<len(prof)-1 and prof[j]!=prof[j+1] else j
    return float(cap), float(r-l)

def ratio(fp,wght=None,opsz=None,SZ=400):
    f=inst(fp,SZ,wght,opsz)
    sc=stem_cap(f)
    if sc is None: return None
    cap,st=sc
    return st/cap
