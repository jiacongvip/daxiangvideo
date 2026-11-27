import sys,math,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from graphics import *
spec=importlib.util.spec_from_file_location('b07_shapes',str(Path(__file__).resolve().parents[1]/'batch07/batch_art.py'));old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
doc=old.doc;tags=old.tags;trio=old.trio;seal=old.seal;parcel=old.parcel

def hospital(d,x,y,t='医院与服务'):
 rr(d,(x,y,x+218,y+250),C['white'],16,C['ink']);rr(d,(x+75,y-40,x+145,y+30),C['mint'],12,C['ink']);line(d,[(x+110,y-25),(x+110,y+15)],C['ink'],7);line(d,[(x+90,y-5),(x+130,y-5)],C['ink'],7);center(d,t,x+109,y+53,25,width=200)
 for j in range(2):
  for k in range(3):rr(d,(x+24+k*61,y+120+j*54,x+64+k*61,y+154+j*54),C['mint'],6)
def calendar(d,x,y,t='周期工单'):
 rr(d,(x,y,x+208,y+260),C['white'],19,C['ink']);rr(d,(x,y,x+208,y+57),C['orange'],15);center(d,t,x+104,y+13,23,width=192)
 for j in range(3):
  for k in range(4):d.ellipse((x+26+k*44,y+90+j*48,x+40+k*44,y+104+j*48),fill=C['mint'])
def ticket(d,x,y,w=216,h=170,t='独立预售券'):
 rr(d,(x,y,x+w,y+h),C['white'],17,C['ink']);rr(d,(x,y,x+w,y+40),C['orange'],13);center(d,t,x+w/2,y+62,25,width=w-22)
 for xx in [x,x+w]:d.ellipse((xx-9,y+h/2-9,xx+9,y+h/2+9),fill=C['cream'])
def poster(d,x,y,w=206,h=287,t='平台海报版本'):
 rr(d,(x,y,x+w,y+h),C['white'],12,C['ink']);rr(d,(x+13,y+13,x+w-13,y+61),C['orange'],9);center(d,t,x+w/2,y+25,22,width=w-25);rr(d,(x+24,y+83,x+w-24,y+178),C['mint'],9);d.ellipse((x+40,y+98,x+76,y+134),fill=C['cream']);line(d,[(x+30,y+164),(x+w*.48,y+118),(x+w-32,y+164)],C['ink'],4);line(d,[(x+27,y+208),(x+w-27,y+208)],C['ink'],3)
 for xx,yy in [(x+w-59,y+h-55),(x+w-39,y+h-55),(x+w-59,y+h-35)]:d.rectangle((xx,yy,xx+12,yy+12),fill=C['ink'])
def building(d,x,y,t='楼栋房屋'):
 rr(d,(x,y,x+218,y+270),C['white'],12,C['ink']);rr(d,(x+10,y+12,x+208,y+60),C['orange'],8);center(d,t,x+109,y+22,25,width=192)
 for j in range(3):
  for k in range(3):rr(d,(x+28+k*60,y+92+j*51,x+66+k*60,y+124+j*51),C['mint'],5,C['ink'])
def chain(d,left,right,a):doc(d,106,525,222,288,left);arrow(d,(353,667),(413,667));doc(d,449,544,174,255,right)
def art(d,cfg,c,u,index):
 i=cfg['id'];m=c['visual'];a=cfg['accent']
 if m=='close':return old.art(d,cfg,c,u,index)
 if i=='peisong':
  if m in ['intro','staff']:
   avatar(d,149,650,.82,'merchant');arrow(d,(247,666),(325,666));doc(d,361,525,257,288,'配送员资料');badge(d,'状态 / 排序 / 业务统计',146,851,428)
  elif m in ['orders','assign']:doc(d,106,523,223,290,'配送订单');arrow(d,(353,667),(414,667));old.van(d,421,614);badge(d,'按人员 / 单号 / 状态查单',133,851,455)
  elif m=='crates':
   for k in range(3):parcel(d,113+k*17,546+k*39,174,117,'退框记录' if k==2 else '')
   arrow(d,(352,669),(413,669));doc(d,449,537,174,270,'数量与时间');badge(d,'配送员与订单对应',163,851,395)
  elif m=='reviews':old.bubble(d,110,530,250,200,'评分与反馈',C['mint']);arrow(d,(384,667),(427,667));doc(d,457,544,167,258,'对应订单')
  elif m=='finance':trio(d,['提成明细','提现申请','审核状态'],a);badge(d,'查询统计与审核分别处理',135,851,451)
  else:
   old.hub(d,['自营配送','码科跑腿','微信配送','方式及设置'],a);seal(d,360,662,'渠道',a)
 elif i=='peizhen':
  if m in ['intro','choose']:avatar(d,149,653,.82,'user');arrow(d,(246,666),(325,666));hospital(d,382,550);badge(d,'医院 / 服务 / 就诊人',151,851,419)
  elif m=='payment':chain(d,'预约订单','统一支付',a);badge(d,'订单列表与详情继续回查',140,851,440)
  elif m=='dispatch':trio(d,['后台指派','我的工单','抢单大厅'],a);badge(d,'指派模式不进入抢单大厅',132,851,457)
  elif m=='service':trio(d,['接到工单','开始服务','完成服务'],a)
  elif m=='refund':chain(d,'当前服务阶段','对应处理入口',a);badge(d,'待接单申请 / 开始后后台处理',111,851,497)
  elif m=='autoclose':doc(d,109,526,218,286,'待付款订单');arrow(d,(351,666),(414,666));seal(d,537,665,'关单任务',a);badge(d,'按时间参数处理待付订单',133,851,455)
  else:trio(d,['收款资料','资金流水','提现入口'],a)
 elif i=='periodicservice':
  if m in ['intro','project']:doc(d,106,524,222,288,'周期服务项目');arrow(d,(352,666),(413,666));calendar(d,424,545,'关联预约商品');badge(d,'内容价格与频率分别维护',139,851,443)
  elif m=='cycles':trio(d,['按天间隔','指定星期','每月日期'],a)
  elif m=='stages':
   calendar(d,111,527,'激活周期订单');arrow(d,(346,665),(407,665))
   for k in range(3):doc(d,430+k*13,548+k*35,153,183,'各期工单' if k==2 else '')
   badge(d,'激活后生成全部期次',151,851,419)
  elif m=='control':trio(d,['暂停','恢复','取消'],a);badge(d,'整笔订单与单期工单分开',135,851,451)
  else:chain(d,'本期服务工单','关联预约订单',a);badge(d,'待服务 / 服务中 / 完成或跳过',109,851,501)
 elif i=='presalevoucher':
  if m in ['intro','tickets']:
   for k in range(3):ticket(d,110+k*22,531+k*64,218,141,'独立券记录' if k==2 else '')
   arrow(d,(388,670),(431,670));calendar(d,447,555,'单张选择日期');badge(d,'先购买 · 后预约',166,851,389)
  elif m=='product':doc(d,105,522,223,292,'商城预售券商品');arrow(d,(353,666),(414,666));tags2=['有效期','取消与超时','购买说明']
  elif m=='calendar':calendar(d,112,528,'门店预约日期');arrow(d,(347,666),(411,666));doc(d,447,543,175,258,'每日预约库存');badge(d,'商品 / 规格 / 门店 / 日期',131,851,459)
  elif m=='difference':ticket(d,108,549,219,207,'已购买预售券');arrow(d,(353,667),(413,667));doc(d,448,530,176,285,'独立差价单');badge(d,'差价支付成功后预约生效',133,851,455)
  elif m=='timeout':trio(d,['差价待付','超时处理','释放锁定'],a)
  elif m=='cancel':doc(d,106,524,222,290,'取消及审核');arrow(d,(352,666),(414,666));badge(d,'已付差价退款',428,548,200,a);badge(d,'失败不释放库存',418,718,220)
  elif m=='verify':ticket(d,109,551,219,203,'已预约券');arrow(d,(352,667),(414,667));seal(d,538,667,'核销权限',a);badge(d,'对应商户门店 · 保留核销记录',113,851,495)
  elif m=='notify':chain(d,'会员通知','后台通知记录',a);badge(d,'业务状态与通知送达分别核对',119,851,483)
  if m=='product':
   for k,t in enumerate(tags2):badge(d,t,441,530+k*113,183,a if k==1 else C['mint'])
 elif i=='productshareposter':
  if m in ['intro','scheme']:
   doc(d,106,523,222,289,'海报方案');arrow(d,(352,667),(411,667))
   for k,t in enumerate(['公众号版本','小程序版本','其他平台版本']):badge(d,t,435,527+k*118,186,a if k==1 else C['mint'])
  elif m=='design':poster(d,111,514,218,308,'所选平台版本');arrow(d,(352,666),(411,666));badge(d,'背景与文字',436,528,186,a);badge(d,'商品及会员元素',420,662,219);badge(d,'二维码等元素',431,790,197)
  elif m=='apply':poster(d,110,522,217,294,'已设计方案');arrow(d,(353,667),(413,667));parcel(d,447,575,176,193,'选中的商品');badge(d,'搜索 · 勾选 · 应用',151,851,419)
  elif m=='manage':trio(d,['查看与应用','清除绑定','清理缓存'],a)
  elif m=='platform':poster(d,110,523,216,293,'当前平台版本');arrow(d,(352,666),(413,666));doc(d,448,544,174,256,'商品分享图');badge(d,'无独立绑定时走默认回退',132,851,457)
  else:chain(d,'历史海报绑定','历史海报方案',a)
 elif i=='property':
  if m in ['intro','community']:building(d,108,532,'小区及计费');arrow(d,(353,666),(415,666));doc(d,449,544,174,258,'周期与单价')
  elif m=='buildings':building(d,109,529,'楼栋结构');arrow(d,(353,665),(412,665));building(d,443,566,'房屋记录')
  elif m=='rooms':building(d,108,533,'房号与面积');arrow(d,(353,668),(416,668));avatar(d,551,651,.82,'user');badge(d,'业主与会员对应',166,851,389)
  elif m=='settings':tags(d,['在线缴费与周期','账单生成与积分','到期提醒参数'],a)
  elif m=='payment':avatar(d,149,653,.82,'user');arrow(d,(247,666),(324,666));doc(d,360,522,258,293,'待缴物业费账单');badge(d,'选账单 → 创建缴费订单',139,851,443)
  else:trio(d,['已缴记录','待缴账单','逾期统计'],a);badge(d,'应收与实收分开核对',155,851,411)
 elif i=='qywx':
  if m in ['intro','connect']:chain(d,'已保存基础配置','连接测试结果',a);badge(d,'先保存 · 再测试',166,851,389)
  elif m=='apps':
   for k,t in enumerate(['应用甲','应用乙','应用丙']):seal(d,157+k*203,649,t,a if k==1 else C['mint'])
   badge(d,'各自配置 · 各自测试',155,851,411)
  elif m=='contacts':
   badge(d,'部门结构',260,510,200,a);line(d,[(360,567),(360,622),(159,622)],C['ink'],4);line(d,[(360,622),(558,622)],C['ink'],4)
   for x in [159,360,558]:avatar(d,x,718,.57,'user');arrow(d,(x,624),(x,658))
   badge(d,'同步成员 · 绑定后台或会员',127,851,466)
  elif m=='rules':
   old.hub(d,['发送应用','接收成员','接收部门','模板变量'],a);seal(d,360,662,'规则',a)
  elif m=='test':doc(d,105,523,224,291,'手动测试发送');arrow(d,(353,667),(414,667));avatar(d,549,653,.82,'user');badge(d,'对应企业应用核对接收',143,851,435)
  else:doc(d,105,524,223,289,'消息日志');arrow(d,(353,666),(414,666));badge(d,'按成败筛选',440,543,180,a);badge(d,'错误码回查',440,717,180)
 elif i=='scorehuang':
  if m in ['intro','settings']:tags(d,['积分与提现开关','最低额与手续费','处理时间与提现方式'],a)
  elif m=='adjust':avatar(d,147,651,.82,'merchant');arrow(d,(245,665),(321,665));doc(d,357,522,262,292,'会员调整范围');badge(d,'正数增加 / 负数减少 / 写原因',110,851,500)
  elif m=='ledger':chain(d,'积分变化明细','原因与会员',a);badge(d,'按昵称 / 编号 / 状态回查',134,851,453)
  elif m=='review':trio(d,['会员等级','最低金额','手续费'],a)
  else:doc(d,105,523,223,291,'提现申请');arrow(d,(353,666),(414,666));badge(d,'审核及原因',440,544,180,a);badge(d,'打款时间记录',426,717,208);badge(d,'审核状态与到账结果分开核对',118,851,485)
 else:raise ValueError(i)

def motion(d,cfg,c,u):
 m=c['visual'];i=cfg['id'];a=cfg['accent']
 if m=='close':return
 if i=='periodicservice' and m=='cycles':
  x=157+(int(u/2)%3)*203;d.ellipse((x-8,821,x+8,837),fill=a)
 elif i=='productshareposter' and m=='design':
  y=607+88*((u*.18)%1);line(d,[(140,y),(298,y)],a,3)
 elif i=='presalevoucher' and m in ['calendar','difference']:
  x=354+58*((u*.3)%1);d.ellipse((x-5,662,x+5,672),fill=a)
 elif i=='qywx' and m=='contacts':
  x=[159,360,558][int(u/2)%3];d.ellipse((x-8,826,x+8,842),fill=a)
 else:
  d.ellipse((88,866,98,876),fill=a if math.sin(u*1.7)>0 else C['mint'])
