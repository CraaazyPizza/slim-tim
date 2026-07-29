"""Line-2 phrase test with the LEFT EDGE PINNED to the measured ink start (+-8 px),
so candidate strings cannot slide sideways to fit noise."""
import numpy as np, sys, json
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
from fast import _font
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter as gf
ALL=json.load(open('fonts.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
OFFC=np.r_[np.arange(300-X0,428-X0), np.arange(1660-X0,1750-X0)]
def clean(fs):
    Y=-RESL[[FR.index(f) for f in fs]].mean(0)
    return Y - Y[:,OFFC].mean(1,keepdims=True)
NUL=clean(list(range(1005,1050)))
def sig(fs): return clean(fs)-NUL
R2=(1000,1076)
def extent(X):
    b=np.clip(X[(R2[0]-Y0):(R2[1]-Y0)],0,None)
    e=gf((b**2).sum(0),3.0)
    pk=np.percentile(e[(440-X0):(1560-X0)],85); t=0.25*pk
    idx=np.where(e>t)[0]+X0; idx=idx[(idx>420)&(idx<1700)]
    return int(idx.min()), int(idx.max())
for tag,fs in [('f983',[983]),('best5',[983,973,974,984,981]),('stack20',list(CAP))]:
    a,b=extent(sig(fs)); print('line-2 ink extent %-8s x %d .. %d  (width %d)'%(tag,a,b,b-a))
L,RR=extent(sig([983,973,974,984,981]))
print('pinned left edge x =',L)
def render_pinned(fp,text,size,kx,H,W,xleft,baseline):
    f=_font(fp,size); bb=f.getbbox(text)
    w=max(2,bb[2]-bb[0]+8); h=max(2,bb[3]-bb[1]+8)
    im=Image.new('L',(w,h),255); ImageDraw.Draw(im).text((4-bb[0],4-bb[1]),text,font=f,fill=0)
    A=np.asarray(im,dtype=np.uint8); nw=max(2,int(round(w*kx)))
    T=1.0-np.asarray(Image.fromarray(A).resize((nw,h),Image.LANCZOS),dtype=np.float64)/255.0
    asc,_=f.getmetrics(); by=4-bb[1]+asc
    out=np.zeros((H,W)); y0=int(round(baseline-by)); x0=int(round(xleft-4*kx))
    a,b2=max(0,y0),min(H,y0+h); c,d=max(0,x0),min(W,x0+nw)
    if b2<=a or d<=c: return out
    out[a:b2,c:d]=T[a-y0:b2-y0,c-x0:d-x0]; return out
XS=(428,1700); H=R2[1]-R2[0]; W=XS[1]-XS[0]
def crop(X): return X[(R2[0]-Y0):(R2[1]-Y0),(XS[0]-X0):(XS[1]-X0)]
OBS={'f983':sig([983]),'best5':sig([983,973,974,984,981]),'stack20':sig(list(CAP)),
     'NULL20':sig(list(range(1010,1030))),'NULL1':sig([1020])}
CAND=['предупреждало об АА','предупреждало об ААГ','предупреждало об ААР','предупреждало об ААЕ',
      'предупреждало об ААБ','предупреждало об ААП','предупреждало об ААРО','предупреждало об ААРС',
      'предупреждало об этом','предупреждало об утечке','прослушано об АА','прослушано об ААРО',
      'предупреждало обо всем']
NULLS=['уведомление доставлено','сообщение переслано вам','документ отправлен вам','запись передана в архив',
       'материал получен нами','подтверждение отправлено','обращение зарегистрировано','сведения переданы далее',
       'отправлено вчера утром','сохранено в общей папке','копия направлена вам','доступ ограничен приказом',
       'напоминание отложено вами','сформировано автоматически','щшгнёъьэюцхкв фыапролдж',
       'абвгдеёжзий клмнопрстуф','котлета борщик пирожок','мылорама укроп грядка','зжщхфыэююяьъе цукенгш',
       'фывапролдж ячсмитьбю','ъыьэюяжшщчц фхкгпрлднс','юяэьыъщшчцхфут срплкйиз']
FS=[f for f in ['Arimo Bold','Roboto Medium','Liberation Sans Bold'] if f in ALL]
CAPS=[46,48]; KX=[1.36,1.41,1.47]; BL=[2.2,3.0,3.8]; BASE=[1058]
out={}
for tag,X in OBS.items():
    fl=Field(crop(X),H,W); rows=[]
    for txt in CAND+NULLS:
        b=None
        for fn in FS:
            fp=ALL[fn]
            for cap in CAPS:
                sz=capsize(fp,cap)
                for kx in KX:
                    for base in BASE:
                        ink=render_pinned(fp,txt,sz,kx,H,W,L-XS[0],base-R2[0])
                        for r,bl,dx,dy in fl.match(ink,BL,dyr=6,dxr=8):
                            if b is None or r>b[0]: b=(r,fn,cap,kx,bl,base,int(dx))
        rows.append(dict(text=txt,r=b[0],font=b[1],cap=b[2],kx=b[3],blur=b[4],base=b[5],dx=b[6],cand=txt in CAND))
    nl=np.array([d['r'] for d in rows if not d['cand']])
    for d in rows: d['z']=(d['r']-nl.mean())/nl.std()
    rows.sort(key=lambda d:-d['r']); out[tag]=rows
    print('\n===== PINNED line-2 phrase test, %s ===== null mean %.4f sd %.4f'%(tag,nl.mean(),nl.std()))
    print('%-28s %7s %7s %5s %5s %5s %4s  %s'%('string','r','z','cap','kx','blur','dx','cand'))
    for d in rows: print('%-28s %7.4f %+7.2f %5.0f %5.2f %5.1f %4d  %s'%(d['text'],d['r'],d['z'],d['cap'],d['kx'],d['blur'],d['dx'],'*' if d['cand'] else ''))
    sys.stdout.flush()
json.dump(out,open('l2pin.json','w'),indent=1,ensure_ascii=False)
