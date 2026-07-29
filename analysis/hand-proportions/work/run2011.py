import numpy as np, json, sys
sys.path.insert(0,'/home/user/new-skinny-bob/analysis/hand-proportions/work')
from common import track_separation, cleft_from_track
from scipy import ndimage as ndi
from PIL import Image, ImageDraw

norm=np.load('work/xju_norm.npy')
names=['TH','T2','T3','T4']

def polar_cleft_seeds(T):
    th,R=np.load(f'work/xju_{T}_polar.npy')
    d=json.load(open('work/xju_tips.json'))[T]
    ctr=np.array(d['ctr']); tips=[np.array(t[:2]) for t in d['tips']]
    tang=[t[3] for t in d['tips']]
    Rs=ndi.uniform_filter1d(R,9,mode='wrap')
    seeds=[]
    for i in range(3):
        m=(th>tang[i])&(th<tang[i+1]); idx=np.nonzero(m)[0]
        j=idx[np.argmin(Rs[idx])]
        seeds.append(np.array([ctr[0]+Rs[j]*np.cos(th[j]), ctr[1]+Rs[j]*np.sin(th[j])]))
    return ctr,tips,seeds

for T in ['t55','t64']:
    ctr,tips,seeds=polar_cleft_seeds(T)
    out={}; tracks={}
    print('===',T)
    for i,(a,b) in enumerate([(0,1),(1,2),(2,3)]):
        mid=(tips[a]+tips[b])/2
        seed=seeds[i]
        start = mid + 0.30*(seed-mid)
        dirn  = seed-mid
        S,P,A,W = track_separation(norm, start, dirn, sign=+1, halfwidth=48, step=1.5, nsteps=int(np.linalg.norm(seed-mid)*1.35/1.5))
        s,idx,Aref = cleft_from_track(S,A)
        key=names[a]+names[b]
        out[key]=dict(pt=[float(x) for x in P[idx]], s=float(s), Aref=float(Aref))
        tracks[key]=(S,P,A,idx)
        print(' ',key,'start',np.round(start,1),'cleft',np.round(P[idx],1),'Aref',round(Aref,3),'ntrack',len(S))
    json.dump(out, open(f'work/xju_{T}_clefts.json','w'), indent=1)
    base=np.clip(norm*230,0,255).astype(np.uint8); im=Image.fromarray(np.stack([base]*3,-1)); dr=ImageDraw.Draw(im)
    for key,(S,P,A,idx) in tracks.items():
        for x,y in P[::2]: dr.point((x,y), fill=(0,190,255))
        x,y=P[idx]; dr.ellipse([x-7,y-7,x+7,y+7], outline=(255,0,0), width=3); dr.text((x+10,y-8),key,fill=(255,0,0))
    for n_,t_ in zip(names,tips):
        dr.ellipse([t_[0]-8,t_[1]-8,t_[0]+8,t_[1]+8], outline=(0,255,0), width=3); dr.text((t_[0]+10,t_[1]-8),n_,fill=(0,255,0))
    im.save(f'out/xju_landmarks_{T}.png')
    np.save(f'work/xju_{T}_trackamp.npy', np.array([np.array(tracks[k][2]) for k in tracks], dtype=object), allow_pickle=True)
