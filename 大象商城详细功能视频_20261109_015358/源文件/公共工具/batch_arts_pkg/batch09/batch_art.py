import sys,math,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from graphics import *
spec=importlib.util.spec_from_file_location('old8',str(Path(__file__).resolve().parents[1]/'batch08'/'batch_art.py'));old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
doc=old.doc;trio=old.trio;tags=old.tags;seal=old.seal;parcel=old.parcel

def pair(d,left,right,a):
 doc(d,106,525,222,288,left);arrow(d,(353,667),(413,667));doc(d,449,544,174,255,right)
def flower(d,x,y,a):
 line(d,[(x,y),(x,y+124)],C['ink'],7)
 d.ellipse((x-43,y+52,x+2,y+85),fill=C['mint']);d.ellipse((x-1,y+77,x+44,y+109),fill=C['mint'])
 for k in range(6):
  ang=k*math.pi/3;xx=x+33*math.cos(ang);yy=y+33*math.sin(ang);d.ellipse((xx-25,yy-25,xx+25,yy+25),fill=a,outline=C['ink'],width=2)
 d.ellipse((x-18,y-18,x+18,y+18),fill=C['cream'],outline=C['ink'],width=2)
def grid(d,x,y,title,a):
 rr(d,(x,y,x+234,y+255),C['white'],19,C['ink']);center(d,title,x+117,y+19,24,width=220)
 for j in range(3):
  for k in range(4):
   xx=x+26+k*49;yy=y+89+j*52;rr(d,(xx,yy,xx+28,yy+28),a if k==j else C['mint'],6)
def ticks(d,arr,a):
 for k,t in enumerate(arr):
  y=538+k*107;rr(d,(130,y,590,y+72),C['mint'] if k!=1 else a,19,C['ink']);old.old.check(d,165,y+35);center(d,t,382,y+19,25,width=380)
def qrmark(d,x,y):
 for xx,yy in [(x,y),(x+42,y),(x,y+42)]:d.rectangle((xx,yy,xx+23,yy+23),outline=C['ink'],width=5)
 d.rectangle((x+43,y+43,x+62,y+62),fill=C['ink'])
def factory(d,x,y,a):
 d.polygon([(x,y+80),(x+57,y+48),(x+57,y+80),(x+113,y+48),(x+113,y+80),(x+180,y+80),(x+180,y+218),(x,y+218)],fill=C['mint'],outline=C['ink'],width=3)
 rr(d,(x+140,y,x+165,y+80),a,7,C['ink']);center(d,'出厂工作台',x+90,y+128,24,width=166)
def wheel(d,x,y,a):
 for k in range(8):d.pieslice((x-125,y-125,x+125,y+125),k*45,(k+1)*45,fill=a if k%2 else C['mint'],outline=C['ink'],width=2)
 d.ellipse((x-47,y-47,x+47,y+47),fill=C['cream'],outline=C['ink'],width=3);center(d,'奖项',x,y-17,25)
 d.polygon([(x-12,y-137),(x+12,y-137),(x,y-112)],fill=C['ink'])
def art(d,cfg,c,u,index):
 i=cfg['id'];m=c['visual'];a=cfg['accent']
 if m=='close':return old.art(d,cfg,c,u,index)
 if i=='shangxiang':
  if m=='intro':flower(d,195,617,a);arrow(d,(285,671),(395,671));doc(d,438,532,185,276,'数字体验订单');badge(d,'线上体验 · 不代表线下履行',121,851,479)
  elif m=='settings':
   for (x,y),t in zip([(205,579),(515,579),(205,761),(515,761)],['供花价格','供果价格','上香价格','许愿价格']):rr(d,(x-115,y-53,x+115,y+53),a if y<600 else C['mint'],20,C['ink']);center(d,t,x,y-17,26,width=214)
   badge(d,'背景 / 描述 / 自定义金额开关',119,851,482)
  elif m=='order':trio(d,['选择体验','创建订单','支付更新'],a)
  elif m=='personal':avatar(d,155,649,.78,'user');arrow(d,(248,668),(329,668));doc(d,364,524,257,289,'我的记录与内容')
  elif m=='records':doc(d,104,523,222,291,'许愿记录');arrow(d,(352,666),(412,666));badge(d,'类型与支付状态',421,527,211,a);badge(d,'会员与时间',439,661,179);badge(d,'显示隐藏及删除',421,793,212)
  else:trio(d,['次数与金额','用户与均值','最近记录'],a)
 elif i=='shiftmaster':
  if m in ['intro','campus']:old.building(d,106,531,'独立校区');arrow(d,(352,668),(412,668));avatar(d,550,650,.8,'merchant');badge(d,'校区范围与管理员对应',148,851,424)
  elif m=='assign':trio(d,['班次管理','成员审核','管理员指派'],a)
  elif m=='registration':grid(d,101,536,'本校区班次',a);arrow(d,(356,667),(413,667));doc(d,446,545,178,255,'我的安排');badge(d,'报名 / 取消 / 回查',161,851,398)
  elif m=='availability':grid(d,105,536,'个人空闲申报',a);arrow(d,(363,667),(414,667));badge(d,'查看',456,541,158);badge(d,'保存',456,665,158,a);badge(d,'删除',456,789,158)
  elif m=='leave':pair(d,'个人请假申请','我的请假记录',a)
  else:pair(d,'考勤标记','日报与概览',a);badge(d,'计划安排与实际记录分开',138,851,445)
 elif i=='shuquanbaoclient':
  if m in ['intro','queue']:
   doc(d,99,537,187,255,'商城调用端');doc(d,435,537,187,255,'数权宝本体');arrow(d,(308,619),(412,619));arrow(d,(308,715),(412,715));badge(d,'事件同步',298,516,124,a);badge(d,'分端处理与回查',162,851,396)
  elif m=='config':tags(d,['本体接口地址','企业应用编号','企业接入密钥'],a)
  elif m=='connection':doc(d,106,527,221,285,'已保存配置');arrow(d,(353,668),(414,668));seal(d,535,666,'连接响应',a);badge(d,'地址 / 企业凭据 / 时钟',143,851,434)
  elif m=='switches':
   for (x,y),t in zip([(201,580),(518,580),(201,762),(518,762)],['登录身份','订单支付','积分事件','佣金事件']):rr(d,(x-111,y-52,x+111,y+52),a if x<300 else C['mint'],19,C['ink']);center(d,t,x,y-17,25,width=204)
  else:trio(d,['连接响应','同步记录','本体结果'],a);badge(d,'模拟成功 ≠ 正式链上成功',129,851,462)
 elif i=='sign':
  if m in ['intro','daily']:grid(d,101,537,'每日一次签到',a);arrow(d,(362,666),(413,666));seal(d,536,666,'基础积分',a);badge(d,'签到时间与连续次数',155,851,411)
  elif m=='settings':tags(d,['签到开关','每日基础积分','页面背景'],a)
  elif m in ['streak','gift']:
   grid(d,102,536,'连续签到条件' if m=='streak' else '连续赠送条件',a);arrow(d,(364,667),(413,667));old.ticket(d,441,558,184,200,'积分与优惠券');badge(d,'两组规则分别检查',166,851,389)
  else:trio(d,['累计次数','连续次数','签到积分'],a)
 elif i=='suyuan':
  if m in ['intro','codes']:
   parcel(d,105,525,251,270,'外箱');parcel(d,156,636,187,171,'中包');parcel(d,207,728,125,107,'产品码');arrow(d,(381,665),(420,665));doc(d,451,546,171,256,'关联码记录');badge(d,'包装层级与码关系示意',146,851,428)
  elif m=='export':pair(d,'生码与冻结','导出任务下载',a)
  elif m=='roles':
   for (x,y),t in zip([(196,567),(525,567),(196,773),(525,773)],['出厂操作','代理商','门店操作','门店巡查']):seal(d,x,y,t,a if x<300 else C['mint'])
  elif m=='factory':factory(d,103,538,a);arrow(d,(308,666),(410,666));parcel(d,442,571,179,208,'入库 / 出库')
  elif m=='agent':trio(d,['采购审核','代理库存','转代理'],a)
  elif m=='store':old.old.shop(d,103,550,'门店与门店码');arrow(d,(343,667),(413,667));doc(d,450,542,171,265,'铺货与巡查')
  elif m=='consumer':parcel(d,104,556,222,224,'演示商品编码');qrmark(d,184,678);arrow(d,(352,666),(413,666));avatar(d,550,650,.81,'user');badge(d,'扫码 / 手输 / 时间轴',145,851,431)
  elif m=='states':
   for (x,y),t in zip([(202,580),(520,580),(202,768),(520,768)],['未知码','首次查询','非首次查询','已冻结']):rr(d,(x-112,y-54,x+112,y+54),a if x<300 else C['mint'],20,C['ink']);center(d,t,x,y-18,25,width=204)
  else:trio(d,['流转轨迹','查询日志','汇总面板'],a)
 elif i=='sweepstakes':
  if m in ['intro','styles']:wheel(d,209,660,a);arrow(d,(356,667),(411,667));old.ticket(d,442,549,183,235,'刮卡 / 抽奖机');badge(d,'多种活动样式示意',165,851,391)
  elif m=='stock':wheel(d,206,662,a);arrow(d,(355,666),(411,666));doc(d,445,540,180,268,'剩余库存权重')
  elif m=='empty':doc(d,105,526,222,288,'奖品库存耗尽');arrow(d,(353,667),(413,667));badge(d,'奖品已抽完',434,617,195,a)
  elif m=='times':trio(d,['活动次数','分享次数','任务次数'],a);badge(d,'消耗类型与次数来源分开',140,851,440)
  elif m=='tasks':ticks(d,['本人订单支付','直推用户购买','直推用户升级'],a)
  elif m=='records':pair(d,'业务任务事件','奖励次数流水',a);badge(d,'防重复 / 子订单匹配',148,851,425)
  else:old.ticket(d,106,546,221,251,'我的奖品');arrow(d,(353,667),(413,667));doc(d,449,541,175,265,'兑奖信息物流')
 else:raise ValueError(i)
def motion(d,cfg,c,u):
 i=cfg['id'];m=c['visual'];a=cfg['accent']
 if m=='close':return
 if i=='shangxiang' and m=='intro':
  x=195+math.sin(u*1.2)*8;d.ellipse((x-4,530,x+4,538),fill=a)
 elif i=='shiftmaster' and m in ['registration','availability']:
  k=int(u*1.2)%4;x=126+49*k;d.ellipse((x-4,832,x+4,840),fill=a)
 elif i=='shuquanbaoclient' and m in ['intro','queue']:
  x=309+102*((u*.4)%1);d.ellipse((x-5,613,x+5,625),fill=a)
 elif i=='sign' and m in ['intro','daily','streak','gift']:
  x=127+49*(int(u*.7)%4);d.ellipse((x-4,830,x+4,838),fill=a)
 elif i=='suyuan' and m=='consumer':
  y=678+61*((u*.3)%1);line(d,[(177,y),(254,y)],a,3)
 elif i=='sweepstakes' and m in ['intro','styles','stock']:
  x=209 if m!='stock' else 206;an=u*.9;xx=x+104*math.cos(an);yy=(660 if m!='stock' else 662)+104*math.sin(an);d.ellipse((xx-5,yy-5,xx+5,yy+5),fill=C['cream'])
 else:d.ellipse((88,866,98,876),fill=a if math.sin(u*1.6)>0 else C['mint'])
