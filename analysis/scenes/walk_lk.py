import cv2, numpy as np, pickle
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
def L(f):
    im=cv2.imread(FD%f, cv2.IMREAD_GRAYSCALE).astype(np.float32)
    im=cv2.GaussianBlur(im,(0,0),1.0)
    # local contrast normalize to help LK on this very flat footage
    m=cv2.GaussianBlur(im,(0,0),31); s=np.sqrt(cv2.GaussianBlur((im-m)**2,(0,0),31))+2.0
    return np.clip((im-m)/s*40+128,0,255).astype(np.uint8)
f0,f1=1621,1835
mask=np.zeros((1080,1920),np.uint8); mask[60:1020,350:1590]=255
I=L(f0)
p=cv2.goodFeaturesToTrack(I,maxCorners=1500,qualityLevel=0.008,minDistance=12,blockSize=9,mask=mask)
print('features',len(p))
lk=dict(winSize=(31,31),maxLevel=4,criteria=(cv2.TERM_CRITERIA_EPS|cv2.TERM_CRITERIA_COUNT,40,0.01))
tracks=[p.reshape(-1,2)]
ids=np.arange(len(p)); alive=np.ones(len(p),bool)
cur=p.copy(); curids=ids.copy()
store={int(i):[tuple(p[k,0])] for k,i in enumerate(ids)}
for f in range(f0+1,f1+1):
    J=L(f)
    q,st,err=cv2.calcOpticalFlowPyrLK(I,J,cur,None,**lk)
    b,stb,_=cv2.calcOpticalFlowPyrLK(J,I,q,None,**lk)
    fb=np.linalg.norm(b.reshape(-1,2)-cur.reshape(-1,2),axis=1)
    ok=(st.ravel()==1)&(stb.ravel()==1)&(fb<1.0)
    cur=q[ok].reshape(-1,1,2); curids=curids[ok]
    for k,i in enumerate(curids): store[int(i)].append(tuple(cur[k,0]))
    I=J
print('survivors to f%d: %d'%(f1,len(curids)))
full={i:np.array(v) for i,v in store.items() if len(v)==f1-f0+1}
print('full-length tracks:',len(full))
pickle.dump({'f0':f0,'f1':f1,'tracks':full},open('walk_lk.pkl','wb'))
