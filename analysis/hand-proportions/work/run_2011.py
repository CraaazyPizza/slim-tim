import numpy as np, json, sys, os
os.chdir('/home/user/new-skinny-bob/analysis/hand-proportions'); sys.path.insert(0,'work')
from pipeline import row_track, cleft_level, transverse_width
from PIL import Image, ImageDraw

norm=np.load('work/xju_norm.npy')          # 1.0 = paper, 0.28 = ink   (crop offset X0=492,Y0=8)
tipsets={t:[np.array(z[:2]) for z in json.load(open('work/xju_tips.json'))[t]['tips']]
         for t in ['t55','t64']}

SCALE = 1.0     # 2011 print pixel scale reference (D3 length ~ 830 px)
def run(tipkey, frac, hold=45, sm=15):
    T=tipsets[tipkey]                       # TH,T2,T3,T4
    out={'tips':{n:[float(p[0]),float(p[1])] for n,p in zip(['TH','T2','T3','T4'],T)}}
    for key,(a,b),x0,y0,y1 in [('C23',(1,2),487,300,700),('C34',(2,3),612,300,700)]:
        y,x,vs,vf=row_track(norm,y0,y1,x0,+1,halfwin=55,follow=20)
        yy,idx,g0,V,thr=cleft_level(y,vs,vf,frac,hold,sm)
        out[key]=[float(x[idx]),float(yy)]
        out[key+'_prof']={'y':y.tolist(),'x':x.tolist(),'V':V.tolist(),'thr':thr.tolist()}
    return out

for frac in [0.5,0.7,0.85]:
    for tk in ['t55','t64']:
        r=run(tk,frac)
        print(f'2011 {tk} frac={frac}: C23={np.round(r["C23"],1)} C34={np.round(r["C34"],1)}')
        json.dump({k:v for k,v in r.items() if not k.endswith('_prof')},
                  open(f'work/xju_land_{tk}_f{int(frac*100)}.json','w'),indent=1)
        if frac==0.7 and tk=='t64':
            json.dump(r, open('work/xju_land_full.json','w'))
