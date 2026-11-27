import sys,math,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from graphics import *
spec=importlib.util.spec_from_file_location('b05_shapes',str(Path(__file__).resolve().parents[1]/'batch05/batch_art.py'));old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
doc=old.doc

def steps(d,pts,accent,arrows=True):
 for k,t in enumerate(pts):
  x=155+k*205;rr(d,(x-80,553,x+80,803),accent if k==1 else C['mint'],22,C['ink']);center(d,t,x,621,25,width=145)
  if arrows and k<2:arrow(d,(x+85,681),(x+116,681))
 if not arrows:badge(d,'分别配置 · 按条件选择',159,852,402)
def parcel(d,x,y,w=160,h=150,label='商品资料'):
 rr(d,(x,y,x+w,y+h),C['mint'],14,C['ink']);line(d,[(x,y+43),(x+w,y+43)],C['ink'],3);line(d,[(x+w/2,y),(x+w/2,y+43)],C['ink'],3);center(d,label,x+w/2,y+72,23,width=w-15)
def van(d,x,y,label='配送车次'):
 rr(d,(x,y,x+194,y+116),C['mint'],16,C['ink']);rr(d,(x+137,y+39,x+235,y+116),C['orange'],14,C['ink']);d.ellipse((x+26,y+92,x+74,y+140),fill=C['ink']);d.ellipse((x+168,y+92,x+216,y+140),fill=C['ink']);center(d,label,x+117,y-43,25,width=245)
def calendar(d,x,y,label='计划配送日'):
 rr(d,(x,y,x+202,y+248),C['white'],18,C['ink']);rr(d,(x,y,x+202,y+58),C['orange'],16);center(d,label,x+101,y+14,23,width=188)
 for j in range(3):
  for k in range(4):d.ellipse((x+25+k*43,y+88+j*49,x+39+k*43,y+102+j*49),fill=C['mint'])
def camera(d,x,y):
 rr(d,(x-89,y-67,x+65,y+66),C['mint'],18,C['ink']);d.polygon([(x+65,y-37),(x+111,y-60),(x+111,y+60),(x+65,y+37)],fill=C['orange'],outline=C['ink'],width=3);d.ellipse((x-49,y-31,x+13,y+31),fill=C['cream'],outline=C['ink'],width=3);line(d,[(x-12,y+69),(x-47,y+160)],C['ink'],6);line(d,[(x-12,y+69),(x+30,y+160)],C['ink'],6)
def mapzones(d):
 for x in [125,235,345,455,565]:line(d,[(x,520),(x+35,824)],'#D4DBCE',4)
 for y in [570,665,760]:line(d,[(92,y),(621,y+20)],'#D4DBCE',4)
 d.ellipse((120,565,330,775),outline=C['orange'],width=6);d.polygon([(397,541),(602,588),(568,811),(363,750)],outline=C['ink'],width=5)
 for x,y in [(217,673),(478,668)]:d.ellipse((x-15,y-15,x+15,y+15),fill=C['orange'])
 badge(d,'圆形 / 多边形服务范围',139,853,441)
def art(d,cfg,c,u,index):
 id=cfg['id'];m=c['visual'];p=c['points'];a=cfg['accent']
 if m=='close':return old.old.art(d,cfg,c,u,index)
 if id=='jushuitan':
  if m in ['intro','auth']:
   avatar(d,155,660,.83,'merchant');arrow(d,(249,671),(328,671));rr(d,(371,529,601,806),C['mint'],24,C['ink']);center(d,'ERP授权',486,574,30,width=211);d.arc((449,643,523,720),180,360,fill=C['ink'],width=5);rr(d,(442,678,530,746),a,11);badge(d,'商家在官方页面确认',159,850,402)
  elif m=='stores':parcel(d,105,548,210,219,'本地范围');arrow(d,(341,666),(403,666));parcel(d,438,548,180,219,'ERP店仓')
  elif m=='sku':
   for k,t in enumerate(['普通SKU','组合装SKU']):parcel(d,107,522+k*169,203,132,t)
   arrow(d,(337,671),(403,671));doc(d,440,550,178,252,'本地规格')
  elif m=='orders':doc(d,104,522,219,290,'已支付订单');arrow(d,(345,666),(414,666));doc(d,449,550,171,245,'同步队列');badge(d,'按单号补入 · 回查任务',145,850,431)
  elif m=='refund':doc(d,101,525,225,292,'本站售后');arrow(d,(351,670),(415,670));badge(d,'ERP待退款',443,550,177,a);badge(d,'同意 / 取消单',443,708,177)
  elif m=='shipping':van(d,103,599,'发货物流');arrow(d,(367,667),(422,667));doc(d,454,545,168,259,'原商城订单')
  else:parcel(d,110,561,214,198,'库存消息');arrow(d,(351,666),(414,666));doc(d,449,542,173,269,'业务日志');badge(d,'先匹配规格 · 再回查处理',143,850,435)
 elif id=='kouzidai':
  if m in ['intro','products']:
   for k,t in enumerate(['产品资料','产品分类','申请入口']):
    x=104+k*205;doc(d,x,531,153,254,t)
   badge(d,'产品展示与线索收集',159,850,402)
  elif m in ['apply','records']:avatar(d,155,655,.83,'user');arrow(d,(250,666),(329,666));doc(d,367,522,249,296,'申请资料' if m=='apply' else '我的申请记录')
  elif m=='membership':
   for k,t in enumerate(['对应等级','当前等级','入口状态']):
    x=110+k*206;y=748-k*64;rr(d,(x,y-100,x+157,829),a if k==1 else C['mint'],18,C['ink']);center(d,t,x+78,y-60,24,width=144)
   badge(d,'会员入口 ≠ 贷款获批',166,490,389)
  elif m=='auth':doc(d,108,531,217,280,'申请前检查');arrow(d,(351,667),(413,667));rr(d,(450,552,620,793),C['mint'],22,C['ink']);center(d,'认证场景',535,612,27,width=152);badge(d,'开关与场景分别启用',159,852,402)
  else:
   doc(d,111,529,220,290,'线索记录');arrow(d,(356,669),(417,669));badge(d,'人工处理',446,544,173,a);badge(d,'产品延时策略',432,710,199);badge(d,'状态标签不是放款凭证',145,850,431)
 elif id=='linggong':
  if m in ['intro','publish']:
   avatar(d,155,659,.85,'merchant');arrow(d,(252,669),(330,669));doc(d,369,521,245,296,'演示打包任务');parcel(d,413,696,155,93,'任务资料')
  elif m=='auth':steps(d,p,a,False)
  elif m=='apply':
   avatar(d,147,650,.75,'user');avatar(d,315,694,.64,'user');doc(d,452,528,171,275,'报名记录');arrow(d,(362,670),(426,670));badge(d,'记录申请 · 检查满员',158,851,405)
  elif m=='proof':avatar(d,151,648,.85,'user');arrow(d,(250,665),(330,665));doc(d,367,520,248,300,'完工凭证');old.old.old.check(d,492,742)
  elif m=='verify':doc(d,111,525,223,292,'验收资料');arrow(d,(360,665),(416,665));badge(d,'通过',446,552,170);badge(d,'驳回',446,708,170,a)
  elif m=='settle':doc(d,111,525,220,293,'结算记录');arrow(d,(356,667),(416,667));rr(d,(451,571,620,763),C['mint'],20,C['ink']);center(d,'钱包明细',536,641,26,width=153)
  elif m=='withdraw':doc(d,110,521,221,293,'提现申请');arrow(d,(358,668),(415,668));badge(d,'审核记录',445,551,174);badge(d,'驳回退余额',430,705,204,a)
  else:doc(d,111,525,220,294,'投诉记录');arrow(d,(357,669),(415,669));doc(d,451,547,170,250,'平台处理')
 elif id=='live':
  if m in ['intro','stream','style']:
   camera(d,192,637);arrow(d,(317,660),(375,660));rr(d,(421,530,613,816),C['mint'],26,C['ink']);d.polygon([(483,622),(483,714),(558,668)],fill=C['ink']);badge(d,'直播场次与播放线路',158,851,403)
  elif m in ['list','reserve']:
   for k,t in enumerate(['预告预约','直播中','结束回放']):
    x=157+k*202;rr(d,(x-79,556,x+79,790),a if k==1 else C['mint'],19,C['ink']);center(d,t,x,627,25,width=143)
   badge(d,'按场次状态组织入口',159,851,402)
  elif m=='control':avatar(d,151,655,.83,'merchant');arrow(d,(247,666),(325,666));doc(d,365,518,254,300,'公屏公告');badge(d,'主播发言 / 置顶通知',145,851,431)
  elif m=='moderation':
   for k,t in enumerate(['禁言管理','黑名单','敏感词库']):
    x=157+k*202;rr(d,(x-79,558,x+79,790),a if k==1 else C['mint'],21,C['ink']);center(d,t,x,630,25,width=143)
   badge(d,'场控身份与规则分别维护',135,851,451)
  elif m=='gift':
   rr(d,(126,584,323,765),a,13,C['ink']);line(d,[(225,584),(225,765)],C['ink'],5);line(d,[(126,640),(323,640)],C['ink'],5);d.ellipse((173,525,225,584),outline=C['ink'],width=5);d.ellipse((225,525,277,584),outline=C['ink'],width=5);arrow(d,(349,668),(416,668));doc(d,451,539,174,267,'礼物记录')
  elif m in ['product','price']:
   camera(d,172,629);arrow(d,(299,669),(359,669));parcel(d,405,552,209,225,'讲解商品' if m=='product' else '直播规格价');badge(d,'讲解 / 详情 / 下单各自对应',122,851,477)
  elif m=='coupon':ticket(d,107,555,232,166,'任务条件',a);arrow(d,(365,666),(422,666));ticket(d,450,571,168,136,'优惠券');badge(d,'按任务条件核对一次领取',133,851,454)
  else:doc(d,110,525,221,291,'分享资料');arrow(d,(357,667),(415,667));doc(d,449,548,172,247,'站内直播入口')
 elif id=='core_delivery_assign':
  if m in ['intro','bind','exclusive']:
   avatar(d,155,648,.8,'user');avatar(d,550,648,.8,'merchant');arrow(d,(254,660),(442,660));badge(d,'会员与专属配送员',181,519,361);badge(d,'绑定 / 换绑 / 解绑',172,849,380)
  elif m=='fallback':steps(d,p,a,False)
  elif m=='area':mapzones(d)
  elif m=='schedule':calendar(d,112,526,'待排期订单');arrow(d,(342,668),(408,668));calendar(d,429,526,'计划配送日')
  else:doc(d,113,526,217,291,'已排期订单');arrow(d,(358,668),(417,668));van(d,415,612,'对应批次')
 elif id=='core_delivery_day':
  if m in ['intro','date']:
   calendar(d,112,526);arrow(d,(345,669),(411,669));van(d,412,613,'计划配送')
  elif m=='batch':doc(d,109,524,222,292,'配送人员与日期');arrow(d,(356,667),(416,667));van(d,415,612,'按车次归组')
  elif m=='picking':
   for k,t in enumerate(['商品甲规格','商品乙规格']):parcel(d,106,534+k*160,214,124,t)
   arrow(d,(344,671),(414,671));doc(d,450,548,173,259,'合并件数')
  elif m=='list':doc(d,110,523,223,298,'逐单配送清单');arrow(d,(356,667),(416,667));avatar(d,544,649,.84,'merchant');badge(d,'日期 / 人员 / 订单对应',146,851,429)
  elif m=='proof':parcel(d,107,550,212,219,'配送订单');arrow(d,(345,668),(412,668));doc(d,449,524,174,293,'送达凭证');badge(d,'按开关检查再完成',167,851,387)
  else:steps(d,p,a)
 elif id=='core_delivery_capacity':
  if m=='intro':van(d,113,596,'待配货批次');arrow(d,(377,668),(430,668));doc(d,464,534,159,268,'分车处理')
  elif m=='limits':
   for k,t in enumerate(['最大单数','最大件数']):
    x=118+k*300;rr(d,(x,550,x+187,792),a if k==0 else C['mint'],23,C['ink']);center(d,t,x+93,618,27,width=171)
   badge(d,'任一超出即另开车次',158,851,405)
  elif m=='split':
   doc(d,108,525,213,290,'待配货订单');arrow(d,(345,671),(408,671));badge(d,'车次甲',445,552,177);badge(d,'车次乙',445,708,177,a);badge(d,'车次数量按本次订单与容量',120,851,482)
  elif m=='oversize':parcel(d,128,545,248,248,'单张超大订单');arrow(d,(402,669),(451,669));doc(d,487,570,136,210,'独立车次')
  elif m=='print':van(d,109,607,'当前车次');arrow(d,(371,672),(423,672));doc(d,457,533,165,283,'本车单据')
  else:calendar(d,112,526,'重新排期');arrow(d,(345,669),(411,669));van(d,415,614,'回首车次');badge(d,'需要时再次手动分车',157,851,406)
 else:raise ValueError((id,m))

def motion(d,cfg,c,u):
 m=c['visual'];id=cfg['id']
 if id=='live' and m in ['intro','stream','style']:
  for k in range(3):
   x=351+k*15;y=621+int(12*math.sin(u*2.6+k));d.ellipse((x-3,y-3,x+3,y+3),fill=cfg['accent'])
 elif m not in ['close','area','limits','list','fallback','date','moderation','membership','auth','bind','exclusive']:
  x=345+55*((u*.28)%1);d.ellipse((x-4,664,x+4,672),fill=cfg['accent'])
