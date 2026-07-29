from PIL import Image, ImageDraw
import numpy as np
from scipy.ndimage import gaussian_filter
FD='/home/user/new-skinny-bob/frames/Oqw96jCOP7A/f%05d.png'
def L(f): return np.asarray(Image.open(FD%f).convert('L'),dtype=np.float64)
sh={1416:(-28,-49),1417:(-32,-47),1418:(-37,-47),1419:(-23,-26),1420:(-29,-32),1421:(-36,-37),1422:(-37,-29),1423:(-38,-25),1424:(-37,-25),1425:(-26,2),1426:(-22,-6),1427:(-22,-6),1428:(-15,-16),1429:(-6,-22),1430:(0,0),1431:(4,-7),1432:(5,-12),1433:(1,-12),1434:(-4,-16),1435:(-8,-24),1436:(-18,-35),1437:(-25,-47),1438:(-28,-58),1439:(-28,-58),1440:(-26,-75),1441:(-23,-73),1442:(-23,-72),1443:(-21,-67),1444:(-19,-62)}
x0,x1,y0,y1=1000,1600,45,440
# group-average 5 consecutive aligned frames, sliding
def st(a,lo=1,hi=99):
    p1,p2=np.percentile(a,[lo,hi]);return np.clip((a-p1)/(p2-p1),0,1)
groups=[(1416,1420),(1421,1425),(1426,1430),(1431,1435),(1436,1440),(1440,1444)]
tiles=[]
for g0,g1 in groups:
    acc=np.zeros((y1-y0,x1-x0));n=0
    for f in range(g0,g1+1):
        dy,dx=sh[f]; acc+=L(f)[y0+dy:y1+dy,x0+dx:x1+dx];n+=1
    a=acc/n
    a=a+1.0*(a-gaussian_filter(a,3.0))
    tiles.append((f'{g0}-{g1}',(st(a,1,99)*255).astype(np.uint8)))
W,H=x1-x0,y1-y0
sheet=Image.new('L',(3*W,2*H))
for i,(lab,t) in enumerate(tiles):
    sheet.paste(Image.fromarray(t),((i%3)*W,(i//3)*H))
sheet=sheet.convert('RGB'); d=ImageDraw.Draw(sheet)
for i,(lab,t) in enumerate(tiles): d.text(((i%3)*W+6,(i//3)*H+6),lab,fill=(255,255,0))
sheet=sheet.resize((sheet.width*3//2,sheet.height*3//2),Image.LANCZOS)
sheet.save('c22_head_groups.png'); print(sheet.size)
