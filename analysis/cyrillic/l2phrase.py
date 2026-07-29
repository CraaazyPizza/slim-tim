"""LINE 2 whole-phrase discrimination: candidate readings vs real-Russian and
nonsense nulls of the same length, at the measured anisotropic geometry."""
import numpy as np, sys, json, time
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
ALL=json.load(open('fonts.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
R2=(998,1078); XS=(432,1640)
def field(fs):
    o=(-RESL[[FR.index(f) for f in fs]].mean(0))[(R2[0]-Y0):(R2[1]-Y0),(XS[0]-X0):(XS[1]-X0)]
    return Field(o,*o.shape)
OBS={'f983':field([983]),'best5':field([983,973,974,984,981]),'stack20':field(CAP),
     'NULL20':field(list(range(1010,1030))),'NULL1':field([1020])}
FS=[f for f in ['Arimo Bold','Roboto Medium','Liberation Sans Bold'] if f in ALL]
CAPS=[45,47,49]; KX=[1.32,1.41,1.50]; BL=[2.2,3.2]
CAND=['предупреждало об АА','предупреждало об ААР','предупреждало об ААГ','предупреждало об ААРО',
      'предупреждало об ААРС','предупреждало об этом','предупреждало об утечке','прослушано об АА',
      'прослушано об ААРО','предупреждало о АА','сообщение получено АА']
NULLS=['уведомление доставлено','сообщение переслано вам','документ отправлен вам','запись передана в архив',
       'материал получен нами','подтверждение отправлено','обращение зарегистрировано','сведения переданы далее',
       'отправлено вчера утром','сохранено в общей папке','копия направлена вам','доступ ограничен приказом',
       'напоминание отложено вами','сформировано автоматически','щшгнёъьэюцхкв фыапролдж','абвгдеёжзий клмнопрстуф',
       'котлета борщик пирожок','мылорама укроп грядка','зжщхфыэююяьъе цукенгш','фывапролдж ячсмитьбю',
       'ъыьэюяжшщчц фхкгпрлднс','юяэьыъщшчцхфут срплкйиз']
def best(fl,txt):
    b=None
    for fn in FS:
        fp=ALL[fn]
        for cap in CAPS:
            A=base_render(fp,txt,capsize(fp,cap))
            for kx in KX:
                ink=place(A,kx,fl.H,fl.W)
                for r,bl,dx,dy in fl.match(ink,BL,dxr=45,dyr=16):
                    if b is None or r>b[0]: b=(r,fn,cap,kx,bl,int(dx),int(dy))
    return b
t0=time.time(); out={}
for tag,fl in OBS.items():
    rows=[]
    for txt in CAND+NULLS:
        b=best(fl,txt)
        rows.append(dict(text=txt,r=b[0],font=b[1],cap=b[2],kx=b[3],blur=b[4],dx=b[5],dy=b[6],cand=txt in CAND))
    nl=np.array([d['r'] for d in rows if not d['cand']])
    for d in rows: d['z']=(d['r']-nl.mean())/nl.std()
    rows.sort(key=lambda d:-d['r']); out[tag]=rows
    print('\n===== LINE 2 whole phrase, %s (%.0fs) ==== null mean %.4f sd %.4f'%(tag,time.time()-t0,nl.mean(),nl.std()))
    print('%-28s %7s %7s %5s %5s %6s  %s'%('string','r','z','cap','kx','dx','cand'))
    for d in rows: print('%-28s %7.4f %+7.2f %5.0f %5.2f %6d  %s'%(d['text'],d['r'],d['z'],d['cap'],d['kx'],d['dx'],'*' if d['cand'] else ''))
    sys.stdout.flush()
json.dump(out,open('l2phrase.json','w'),indent=1,ensure_ascii=False)
