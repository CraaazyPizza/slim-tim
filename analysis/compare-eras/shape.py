import pickle,numpy as np
from PIL import Image
R=pickle.load(open('analysis/compare-eras/runs.pkl','rb'))
# (key, runindex, groupindex, charlabel)
SEL=[('zb',0,3,'0'),('zb',0,10,'1'),('zb',0,5,':'),
     ('rs',0,3,'0'),('rs',0,9,'1'),('rs',0,5,':'),
     ('oq',0,3,'0'),('oq',0,6,'1'),('oq',0,5,':'),
     ('l9',1,3,'0'),('l9',1,6,'1'),('l9',1,5,':')]
NAME={'zb':'ZB788_2011','rs':'RsQCX_2011','oq':'Oqw96_2026','l9':'l9RAh_2026'}
def getglyph(P,groups,gi,pad=6):
    x0,x1=groups[gi]
    sub=P[:,max(0,x0-pad):min(P.shape[1],x1+1+pad)].copy()
    sub=sub/sub.max()
    rows=np.nonzero(sub.max(1)>0.5)[0]; cols=np.nonzero(sub.max(0)>0.5)[0]
    core=sub[rows.min():rows.max()+1, cols.min():cols.max()+1]
    return core,(rows.max()-rows.min()+1),(cols.max()-cols.min()+1)
G={}
print('%-12s %-3s  inkH  inkW  W/H     pitch'%('video','ch'))
for k,ri,gi,ch in SEL:
    P,groups,c5,p,i0,i1,n=R[k][ri]
    core,h,w=getglyph(P,groups,gi)
    G[(k,ch)]=core
    print('%-12s %-3s  %4d  %4d  %.4f  %.3f   (run f%d-%d)'%(NAME[k],ch,h,w,w/h,p,i0,i1))
# normalise each glyph to height 80 preserving aspect, then compare pairs
def norm(a,H=80):
    im=Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8))
    W=max(1,int(round(a.shape[1]*H/a.shape[0])))
    return np.asarray(im.resize((W,H),Image.LANCZOS)).astype(np.float32)/255.
def ncc(a,b):
    W=max(a.shape[1],b.shape[1])
    def pad(x):
        o=np.zeros((x.shape[0],W),np.float32); off=(W-x.shape[1])//2; o[:,off:off+x.shape[1]]=x; return o
    A,Bp=pad(a),pad(b)
    best=-9
    for dx in range(-6,7):
        Bs=np.roll(Bp,dx,axis=1)
        u=A-A.mean(); v=Bs-Bs.mean()
        d=np.sqrt((u*u).sum()*(v*v).sum())
        if d>0: best=max(best,float((u*v).sum()/d))
    return best
print()
print('Normalised-shape NCC (height-matched to 80px, best over +/-6px x-shift):')
for ch in ['0','1',':']:
    keys=[k for k in ['zb','rs','oq','l9'] if (k,ch) in G]
    print('  char %s'%ch)
    for i in range(len(keys)):
        for j in range(i+1,len(keys)):
            a,b=norm(G[(keys[i],ch)]),norm(G[(keys[j],ch)])
            tag='WITHIN-era ' if (keys[i] in ('zb','rs'))==(keys[j] in ('zb','rs')) else 'CROSS-era  '
            print('    %s %-11s vs %-11s NCC=%.4f  (aspect %.3f vs %.3f)'%(tag,NAME[keys[i]],NAME[keys[j]],ncc(a,b),
                  G[(keys[i],ch)].shape[1]/G[(keys[i],ch)].shape[0], G[(keys[j],ch)].shape[1]/G[(keys[j],ch)].shape[0]))
# save montage
for ch in ['0','1',':']:
    ims=[norm(G[(k,ch)]) for k in ['zb','rs','oq','l9'] if (k,ch) in G]
    W=sum(i.shape[1]+8 for i in ims)
    can=np.zeros((80,W)); x=0
    for i in ims: can[:,x:x+i.shape[1]]=i; x+=i.shape[1]+8
    Image.fromarray((np.clip(can,0,1)*255).astype(np.uint8)).resize((W*4,320),Image.LANCZOS).save('analysis/compare-eras/CH_%s.png'%('colon' if ch==':' else ch))
print('\nsaved CH_0.png CH_1.png CH_colon.png  (order: ZB788_2011, RsQCX_2011, Oqw96_2026, l9RAh_2026)')
