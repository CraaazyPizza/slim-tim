"""SECOND, INDEPENDENT kx ESTIMATOR from the «о» bowl.
The top/bottom arcs of «о» are horizontal strokes: their thickness is a VERTICAL
measurement, untouched by a horizontal stretch. The left/right sides are vertical
strokes: their thickness is a HORIZONTAL measurement, multiplied by kx.
So  (measured side/arc ratio) / (a face's intrinsic side/arc ratio)  =  kx,
using a quantity that never touches the stem or the cap height."""
import numpy as np, sys, json, os
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
import fastvar
from c4 import *
import pipe
from pipe import sig, BEST5
from fast import _font
from PIL import Image, ImageDraw
SIG_PSF=0.9
def fwhm(p):
    p=np.asarray(p,dtype=float)
    m=int(np.argmax(p)); h=p[m]/2.0
    i=m
    while i>0 and p[i-1]>=h: i-=1
    j=m
    while j<len(p)-1 and p[j+1]>=h: j+=1
    l=i-1+(h-p[i-1])/(p[i]-p[i-1]) if i>0 and p[i]!=p[i-1] else i
    r=j+(p[j]-h)/(p[j]-p[j+1]) if j<len(p)-1 and p[j]!=p[j+1] else j
    return float(r-l)
def deconv(w):  return float(np.sqrt(max(w**2-(2.3548*SIG_PSF)**2,0.04)))
# ---------- real: the «о» at x 1173-1221, x-height band y 937-975
def real_o(X, xr=(1170,1226), yr=(934,978)):
    b=np.clip(X[(yr[0]-Y0):(yr[1]-Y0),(xr[0]-X0):(xr[1]-X0)],0,None)
    # arc thickness: row profile through the middle third of the bowl width
    w=b.shape[1]; mid=b[:, int(w*0.35):int(w*0.65)].mean(1)
    top=fwhm(mid[:len(mid)//2]); bot=fwhm(mid[len(mid)//2:])
    # side thickness: column profile through the middle third of the bowl height
    h=b.shape[0]; midc=b[int(h*0.35):int(h*0.65), :].mean(0)
    left=fwhm(midc[:len(midc)//2]); right=fwhm(midc[len(midc)//2:])
    return np.mean([top,bot]), np.mean([left,right])
print('=== real «о» stroke thicknesses ===')
vals=[]
for tag,fs in [('f983',[983]),('best5',BEST5),('stack20',list(CAP))]:
    arc,side=real_o(sig(fs))
    a,s=deconv(arc),deconv(side)
    vals.append((a,s))
    print('  %-8s arc(vertical) %.2f -> %.2f   side(horizontal) %.2f -> %.2f   side/arc = %.3f'%(tag,arc,a,side,s,s/a))
A=np.mean([v[0] for v in vals[:2]]); Sd=np.mean([v[1] for v in vals[:2]])
RATIO=Sd/A
print('  adopted side/arc = %.3f  (PSF-deconvolved, f983 + 5-frame)'%RATIO)
# ---------- templates
def tmpl_o(spec, SZ=400):
    f=_font(spec,SZ); bb=f.getbbox('о')
    W=bb[2]-bb[0]+40; H=bb[3]-bb[1]+40
    im=Image.new('L',(W,H),255); ImageDraw.Draw(im).text((20-bb[0],20-bb[1]),'о',font=f,fill=0)
    a=(255-np.asarray(im,dtype=np.float64))/255.0
    rows=np.where(a.sum(1)>0.5)[0]; cols=np.where(a.sum(0)>0.5)[0]
    if len(rows)<8 or len(cols)<8: return None
    b=a[rows.min():rows.max()+1, cols.min():cols.max()+1]
    h,w=b.shape
    mid=b[:, int(w*0.35):int(w*0.65)].mean(1)
    top=fwhm(mid[:h//2]); bot=fwhm(mid[h//2:])
    midc=b[int(h*0.35):int(h*0.65), :].mean(0)
    left=fwhm(midc[:w//2]); right=fwhm(midc[w//2:])
    arc=np.mean([top,bot]); side=np.mean([left,right])
    if arc<=0: return None
    return side/arc
R=json.load(open('sweep3.json'))['best5']
print()
print('=== kx from the «о» side/arc ratio, compared with the stem prediction and the image fit ===')
print('%-26s %8s %8s %8s %8s   %s'%('face','o s/a','kx_o','kx_stem','kx_fit','r_con'))
SEL=['Roboto Medium','Inter w600 opsz14','Inter w575 opsz14','Montserrat w600','Golos Text w500',
     'Rubik w450','Open Sans Semibold','Lato Semibold','Arimo Bold','Liberation Sans Bold',
     'Nimbus Sans Bold','Go Bold','Carlito Bold','PT Sans Bold','Fira Sans Bold','DejaVu Sans Bold']
D={d['font']:d for d in R}
out={}
for n in SEL:
    if n not in D: print('  %-26s (absent)'%n); continue
    d=D[n]; sa=tmpl_o(d['spec'])
    if sa is None: continue
    kxo=RATIO/sa
    out[n]=dict(sa=sa,kx_o=kxo,kx_stem=d['kx_pred'],kx_fit=d['kx_free'],r_con=d['r_con'])
    print('%-26s %8.3f %8.2f %8.2f %8.2f   %6.4f'%(n,sa,kxo,d['kx_pred'],d['kx_free'],d['r_con']))
json.dump(dict(real_side_arc=RATIO,rows=out),open('stroke2.json','w'),indent=1,ensure_ascii=False)
