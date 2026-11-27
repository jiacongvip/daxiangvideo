from PIL import Image,ImageDraw,ImageFont
import math
W,H=720,1280
C={'ink':'#173F3B','cream':'#F7F1E5','mint':'#B9D6C1','orange':'#F0AA79','pink':'#EDD0C0','soft':'#E7E8D8','muted':'#6D8174','white':'#FFFDF8'}
fonts={}
def f(n,b=True):
 if (n,b) not in fonts:fonts[n,b]=ImageFont.truetype(str((__import__('pathlib').Path(__file__).resolve().parent/'fonts'/('NotoSansCJK-Bold.ttc' if b else 'NotoSansCJK-Regular.ttc'))),n)
 return fonts[n,b]
def wrap(t,n,w):
 a=[];line=''
 for ch in t:
  if line and f(n).getlength(line+ch)>w:a.append(line);line=ch
  else:line+=ch
 if line:a.append(line)
 if len(a)==2:
  choices=[]
  for k in range(1,len(t)):
   x,y=t[:k],t[k:]
   if y[0] in '，。！？、；：':continue
   wx,wy=f(n).getlength(x),f(n).getlength(y)
   if max(wx,wy)<=w:choices.append((abs(wx-wy),x,y))
  if choices:_,x,y=min(choices);a=[x,y]
 return a
def tx(d,t,x,y,n=30,c=None,width=610,b=True):
 c=c or C['ink'];lines=wrap(t,n,width)
 for l in lines:
  box=d.textbbox((x,y),l,font=f(n,b));assert 36<=box[0] and box[2]<=W-36 and box[3]<H-34,(t,box)
  d.text((x,y),l,font=f(n,b),fill=c);y+=n+13
 return y
def center(d,t,x,y,n=30,c=None,width=610):
 lines=wrap(t,n,width)
 for l in lines:tx(d,l,x-f(n).getlength(l)/2,y,n,c,width);y+=n+13
 return y
def rr(d,box,c,r=20,outline=None):d.rounded_rectangle(box,radius=r,fill=c,outline=outline,width=3)
def ease(x):return 1-(1-min(1,max(0,x)))**3
def line(d,pts,c=None,w=5):d.line(pts,fill=c or C['ink'],width=w,joint='curve')
def arrow(d,a,b,c=None,w=5):
 c=c or C['ink'];line(d,[a,b],c,w);ang=math.atan2(b[1]-a[1],b[0]-a[0]);z=12
 p=[b,(b[0]-z*math.cos(ang-.5),b[1]-z*math.sin(ang-.5)),(b[0]-z*math.cos(ang+.5),b[1]-z*math.sin(ang+.5))];d.polygon(p,fill=c)
def badge(d,t,x,y,w=170,fill=None,ink=None):rr(d,(x,y,x+w,y+49),fill or C['mint'],24);center(d,t,x+w/2,y+5,23,ink,width=w-16)
def avatar(d,x,y,scale=1,kind='merchant',pose=0):
 # Original flat-vector people; not photos or system UI.
 s=scale;skin='#E6B697';clothes=C['orange'] if kind=='merchant' else C['mint'];ink=C['ink']
 d.ellipse((x-29*s,y-80*s,x+29*s,y-22*s),fill=skin)
 d.pieslice((x-32*s,y-87*s,x+32*s,y-24*s),180,355,fill=ink)
 rr(d,(x-48*s,y-18*s,x+48*s,y+106*s),clothes,int(22*s))
 if kind=='merchant':
  d.polygon([(x-29*s,y+6*s),(x+29*s,y+6*s),(x+38*s,y+100*s),(x-38*s,y+100*s)],fill='#466C58')
  line(d,[(x-25*s,y-15*s),(x-20*s,y+15*s),(x+20*s,y+15*s),(x+25*s,y-15*s)],C['cream'],int(4*s))
 line(d,[(x-20*s,y+100*s),(x-22*s,y+153*s)],ink,int(11*s));line(d,[(x+20*s,y+100*s),(x+22*s,y+153*s)],ink,int(11*s))
 line(d,[(x-44*s,y+4*s),(x-65*s,y+48*s)],skin,int(15*s));line(d,[(x+44*s,y+4*s),(x+80*s,y+18*s-pose*15*s)],skin,int(15*s))
def ticket(d,x,y,w=234,h=134,label='活动报名',accent=None,angle=0):
 # Clearly an illustrated ticket, with no fake personal data or app controls.
 rr(d,(x,y,x+w,y+h),C['white'],16,C['ink']);d.rectangle((x+3,y+3,x+w-3,y+34),fill=accent or C['orange'])
 d.ellipse((x-11,y+h/2-11,x+11,y+h/2+11),fill=C['cream']);d.ellipse((x+w-11,y+h/2-11,x+w+11,y+h/2+11),fill=C['cream'])
 center(d,label,x+w/2,y+53,27,width=w-24)
 for yy in range(int(y+38),int(y+h-6),12):line(d,[(x+w-37,yy),(x+w-37,yy+5)],'#B4C5B4',2)

def labels(d,pts,y=897):
 cell=610/len(pts)
 for k,t in enumerate(pts):
  x=55+cell*(k+.5);d.ellipse((x-5,y,x+5,y+10),fill=C['orange']);center(d,t,x,y+25,24,width=cell-12)