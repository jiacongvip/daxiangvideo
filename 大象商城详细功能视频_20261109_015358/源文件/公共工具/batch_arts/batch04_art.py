import sys,math,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from graphics import *
spec=importlib.util.spec_from_file_location('b03_shapes',str(Path(__file__).resolve().parents[1]/'batch03/batch_art.py'));old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def clean_doc(d,x,y,w=170,h=220,label='资料'):
 rr(d,(x,y,x+w,y+h),C['white'],16,C['ink']);d.polygon([(x+w-30,y),(x+w,y+30),(x+w-30,y+30)],fill=C['mint']);center(d,label,x+w/2,y+38,23,width=w-20)
 for yy in range(int(y+148),int(y+h-16),25):line(d,[(x+21,yy),(x+w-22,yy)],'#B5C9B9',4)
old.doc=clean_doc

def obj(d,id,x,y,s=.9):
 if id=='ezviz':old.camera(d,x,y,'摄像通道')
 elif id=='fangyuan':old.shop(d,x,y,s,'演示房源')
 elif id=='filem':old.folder(d,x-90,y-88,180,165,'资料分类')
 elif id=='express100':
  rr(d,(x-78,y-69,x+78,y+78),C['orange'],12,C['ink']);line(d,[(x-78,y-21),(x+78,y-21)],C['ink'],3);line(d,[(x,y-69),(x,y+79)],C['ink'],3);center(d,'包裹',x,y+100,25,width=170)
 elif id=='equitypool':
  d.ellipse((x-78,y-78,x+78,y+78),fill=C['mint'],outline=C['ink'],width=4);center(d,'池内台账',x,y-17,26,width=145)
 elif id=='fadada':
  old.doc(d,x-80,y-107,160,220,'待签合同');line(d,[(x-45,y+51),(x+15,y+78),(x+62,y+27)],C['orange'],7)
 elif id=='evaluation':
  old.doc(d,x-80,y-107,160,220,'测评项目');old.check(d,x,y+45)
 elif id=='dashiji':old.bubble(d,x-83,y-76,'项目反馈',166)
 else:avatar(d,x-12,y,.82,'user')

def art(d,cfg,c,u,index):
 id=cfg['id'];m=c['visual'];pts=c['points'];accent=cfg['accent']
 if m=='close':
  for k,t in enumerate(cfg['phases']):
   x,y=[(150,550),(570,550),(570,780),(150,780)][k];d.ellipse((x-51,y-51,x+51,y+51),fill=accent if k%2 else C['mint']);center(d,str(k+1),x,y-25,35);center(d,t,x,y+74,27,width=215)
  arrow(d,(224,550),(494,550));arrow(d,(570,612),(570,715));arrow(d,(494,780),(224,780));return
 if m in ['intro','config','account','pool','sync','lookup','order','member']:
  obj(d,id,175,663)
  arrow(d,(274,662),(321,662))
  for k,t in enumerate(pts):badge(d,t,345,526+k*116,269,accent if k==1 else C['mint'])
 elif m in ['folders','groups','tree','template','page','sources']:
  old.folder(d,251,489,218,155,pts[0]);line(d,[(360,655),(360,698),(172,698),(172,732)],C['ink'],4);line(d,[(360,698),(548,698),(548,732)],C['ink'],4)
  old.folder(d,89,730,177,155,pts[1]);old.folder(d,454,730,177,155,pts[2])
 elif m in ['privacy','blacklist','scope','visibility']:
  rr(d,(101,615,272,779),C['mint'],20,C['ink']);d.arc((122,522,251,686),180,360,fill=C['ink'],width=7);d.ellipse((177,668,196,687),fill=C['ink']);line(d,[(187,685),(187,726)],C['ink'],5)
  for k,t in enumerate(pts):badge(d,t,335,524+k*120,283,accent if k==1 else C['mint'])
 elif m in ['states','timeline','status','state','rules','pages','notify']:
  for k,t in enumerate(pts):
   y=510+k*134;badge(d,t,160,y,400,accent if k==1 else C['mint'])
   if k<2:arrow(d,(360,y+84),(360,y+120))
 elif m in ['accounts','balance','commission','score','adjust','stats','batch','choices']:
  for k,t in enumerate(pts):
   x=150+k*210;rr(d,(x-80,561,x+80,790),accent if k==1 else C['mint'],23,C['ink']);center(d,t,x,614,27,width=135)
   if m in ['balance','commission','score','adjust']:center(d,'+' if k==0 else '−' if k==1 else '✓',x,724,37,width=130)
  center(d,'分别核对，不混为同一对象',360,854,25,width=560)
 elif m in ['preview','control','mobile'] and id=='ezviz':
  old.camera(d,174,659,'授权设备');arrow(d,(268,659),(334,659))
  if m=='control':
   d.ellipse((417,547,595,725),fill=C['mint'],outline=C['ink'],width=4)
   for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]:arrow(d,(506+dx*20,636+dy*20),(506+dx*67,636+dy*67))
   badge(d,'启动 / 停止',375,790,242)
  else:old.phone(d,408,510,177,321,'预览' if m=='preview' else '登录播放')
 elif m=='booking':
  old.shop(d,165,641,.95,'演示房源');arrow(d,(266,676),(330,676));old.doc(d,380,516,224,284,'看房预约');badge(d,'后台处理预约状态',175,852,370)
 elif m=='staff':
  avatar(d,143,648,.8,'merchant');arrow(d,(242,659),(294,659));avatar(d,388,612,.65,'user');avatar(d,543,707,.65,'user');badge(d,'先核对席位与绑定',160,855,400)
 elif m=='house':
  old.shop(d,174,651,.9,'房源资料');old.doc(d,364,509,235,305,'公开 / 私密');badge(d,'资料与审核分别处理',163,852,394)
 elif m in ['records','result','logs','export','rows']:
  old.doc(d,105,504,247,318,'记录核对');arrow(d,(377,660),(424,660))
  for k,t in enumerate(pts):badge(d,t,441,533+k*109,182,accent if k==1 else C['mint'])
 elif m in ['submit','sign','identity','roles','edit','search','settings','drawer','links','phone','filters','print','logistics']:
  # Each illustration labels actual operations for this topic, not a fake app screen.
  for k,t in enumerate(pts):
   x=150+k*210;old.doc(d,x-74,536+(k%2)*50,148,207,t)
   if k<2:arrow(d,(x+80,677),(x+130,677))
  center(d,c['role'],360,859,25,width=550)
 else:raise ValueError((id,m))
