"""LINE 2 — settle it.
(a) independent geometry fit of the candidate line at free cap/kx/blur
(b) whole-line discrimination against real-Russian and nonsense nulls
(c) the glyph after «АА»: ranked over the whole Cyrillic alphabet, scored on a
    window covering ONLY that glyph cell so the shared prefix cannot carry it."""
import numpy as np, sys, json, time, itertools
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/cyrillic')
from c4 import *
from fast import *
ALL=json.load(open('fonts.json'))
LOC=[f for f in range(950,1010) if not (966<=f<=993)]
_lbg=S[[FR.index(f) for f in LOC]].mean(0); RESL=S-_lbg
def win(fs,ROWS,XS):
    o=(-RESL[[FR.index(f) for f in fs]].mean(0))[(ROWS[0]-Y0):(ROWS[1]-Y0),(XS[0]-X0):(XS[1]-X0)]
    return Field(o,*o.shape), ROWS, XS
R2=(998,1078); X2=(432,1640)
OBS={'f983':win([983],R2,X2),'best5':win([983,973,974,984,981],R2,X2),'stack20':win(CAP,R2,X2),
     'NULL20':win(list(range(1010,1030)),R2,X2),'NULL1':win([1020],R2,X2),
     'NULL20b':win(list(range(915,935)),R2,X2)}
FS=[f for f in ['Lato Bold','Carlito Bold','Nimbus Sans Bold','Open Sans Semibold','Roboto Medium',
                'Liberation Sans Bold','DejaVu Sans Bold','Noto Sans Regular','Cantarell Bold'] if f in ALL]
def fitstr(fl,fp,text,caps,kxs,bls,dxr=45,dyr=16):
    best=None
    for cap in caps:
        s=capsize(fp,cap); A=base_render(fp,text,s)
        for kx in kxs:
            ink=place(A,kx,fl.H,fl.W)
            for r,bl,dx,dy in fl.match(ink,bls,dyr=dyr,dxr=dxr):
                if best is None or r>best[0]: best=(r,cap,s,float(kx),bl,dx,dy)
    return best
CAPS=[40,42,44,46,48,50]; KX=np.round(np.arange(1.20,1.59,0.03),2); BL=[0.5,0.9,1.4,2.1,3.0]
CAND=['предупреждало об АА','предупреждало об ААР','предупреждало об ААРО','предупреждало об ААРС',
      'предупреждало об этом','предупреждало об утечке','прослушано об АА','прослушано об ААРО',
      'предупреждало о АА','предыдущее сообщение']
NULLS=['уведомление доставлено','сообщение переслано вам','документ отправлен вам','запись передана в архив',
       'материал получен нами','подтверждение отправлено','обращение зарегистрировано','сведения переданы далее',
       'отправлено вчера утром','сохранено в общей папке','копия направлена вам','доступ ограничен приказом',
       'щшгнёъьэюцхкв фыапролдж','абвгдеёжзий клмнопрстуф','котлета борщик пирожок','мылорама укроп грядка',
       'зжщхфыэююяьъе цукенгш','фывапролдж ячсмитьбю']
if __name__=='__main__':
    t0=time.time(); out={}
    for tag,(fl,ROWS,XS) in OBS.items():
        rows=[]
        for txt in CAND+NULLS:
            best=None
            for fn in FS:
                b=fitstr(fl,ALL[fn],txt,CAPS,KX,BL)
                if best is None or b[0]>best[0]: best=b+(fn,)
            rows.append(dict(text=txt,r=best[0],cap=best[1],kx=best[3],blur=best[4],
                             dx=best[5],dy=best[6],font=best[7],cand=txt in CAND))
        nl=np.array([d['r'] for d in rows if not d['cand']])
        for d in rows: d['z']=(d['r']-nl.mean())/nl.std()
        rows.sort(key=lambda d:-d['r']); out[tag]=rows
        print('\n===== LINE 2 whole-phrase, %s  (%.0fs)  null mean %.4f sd %.4f ====='%(tag,time.time()-t0,nl.mean(),nl.std()))
        print('%-26s %7s %6s %5s %5s %6s %6s %-18s %s'%('string','r','z','cap','kx','dx','dy','font','')) 
        for d in rows: print('%-26s %7.4f %+6.2f %5.0f %5.2f %6d %6d %-18s %s'%(d['text'],d['r'],d['z'],d['cap'],d['kx'],d['dx'],d['dy'],d['font'],'*' if d['cand'] else ''))
        sys.stdout.flush()
    json.dump(out,open('l2phrase.json','w'),indent=1,ensure_ascii=False)
