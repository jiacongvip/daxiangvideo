import sys,math,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from graphics import *
spec=importlib.util.spec_from_file_location('b9',str(Path(__file__).resolve().parents[1]/'batch09'/'batch_art.py'));o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)
doc=o.doc;trio=o.trio;tags=o.tags;seal=o.seal;parcel=o.parcel;pair=o.pair

def clock(d,x,y,a):
 d.ellipse((x-103,y-103,x+103,y+103),fill=C['white'],outline=C['ink'],width=4)
 for k in range(12):
  an=k*math.pi/6;line(d,[(x+86*math.sin(an),y-86*math.cos(an)),(x+94*math.sin(an),y-94*math.cos(an))],C['ink'],3)
 line(d,[(x,y-65),(x,y),(x+51,y+23)],C['ink'],6);d.ellipse((x-8,y-8,x+8,y+8),fill=a)
def tickets(d,x,y,a):
 for k in range(3):o.old.ticket(d,x+18*k,y+53*k,208,132,'参与编号' if k==2 else '')
def pool(d,a):
 rr(d,(109,548,335,810),C['mint'],23,C['ink']);center(d,'公海商机',222,575,26,width=200)
 for k in range(3):d.ellipse((138+k*55,677,163+k*55,702),fill=a)
 arrow(d,(359,666),(416,666));avatar(d,548,651,.8,'merchant');badge(d,'认领与负责人对应',165,851,390)
def poster(d,x,y,a):
 rr(d,(x,y,x+224,y+285),C['white'],16,C['ink']);rr(d,(x+15,y+16,x+209,y+60),a,9);rr(d,(x+21,y+83,x+203,y+180),C['mint'],9);line(d,[(x+32,y+206),(x+191,y+206)],C['ink'],4);o.qrmark(d,x+131,y+213)
def elements(d,a):
 labels=['木','火','土','金','水'];colors=[C['mint'],a,C['soft'],C['white'],C['mint']];xy=[]
 for k,t in enumerate(labels):
  an=-math.pi/2+k*2*math.pi/5;x=360+139*math.cos(an);y=675+139*math.sin(an);xy.append((x,y));line(d,[(360,675),(x,y)],C['ink'],3);seal(d,x,y,t,colors[k])
 badge(d,'文化娱乐内容',253,650,215,a)
def art(d,cfg,c,u,index):
 i=cfg['id'];m=c['visual'];a=cfg['accent']
 if m=='close':return o.old.art(d,cfg,c,u,index)
 if i=='timedlottery':
  if m in ['intro','draw']:tickets(d,102,531,a);arrow(d,(354,667),(413,667));clock(d,527,665,a);badge(d,'任务领号 · 到期统一开奖',139,851,442)
  elif m=='tasks':tags(d,['免费 / 支付 / 积分 / 余额','分享 / 邀请 / 餐饮消费','后台发放编号'],a)
  elif m=='entries':tickets(d,107,530,a);arrow(d,(355,667),(414,667));doc(d,449,541,175,266,'我的编号');badge(d,'总次数 / 每日次数 / 编号模式',118,851,484)
  elif m=='dining':trio(d,['结算发码','反结账撤销','再结算恢复'],a)
  elif m=='prizes':tags(d,['多奖项与指定中奖','白名单 / 黑名单','分享邀请及后台补发'],a)
  elif m=='threshold':
   for k in range(3):avatar(d,128+k*86,651,.43,'user')
   arrow(d,(353,666),(414,666));seal(d,535,665,'人数门槛',a);badge(d,'独立用户数 ≠ 编号总数',139,851,441)
  else:trio(d,['中奖公示','虚拟接口','实物手动处理'],a)
 elif i=='tuozhancrm':
  if m in ['intro','pool']:pool(d,a)
  elif m=='categories':tags(d,['商机分类','意向度分类','系统开关'],a)
  elif m=='profile':doc(d,103,527,225,289,'商机资料');arrow(d,(353,667),(415,667));badge(d,'公司与联系人',434,532,195,a);badge(d,'分类和意向度',434,665,195);badge(d,'人员与会员归属',422,797,219)
  elif m=='transfer':avatar(d,150,651,.8,'merchant');arrow(d,(249,666),(326,666));doc(d,363,525,257,288,'所选商机转出');badge(d,'单个或批量 · 核对归属',144,851,433)
  elif m=='follow':pair(d,'同一条商机','跟进记录',a);badge(d,'添加 / 编辑 / 删除',160,851,401)
  else:pair(d,'搜索商机资料','表格导出',a);badge(d,'公司 / 联系人 / 电话',155,851,410)
 elif i=='tuozhanyuan':
  if m in ['intro','apply']:avatar(d,148,652,.82,'user');arrow(d,(246,667),(327,667));doc(d,362,526,258,288,'申请与审核');badge(d,'申请模式 / 材料 / 协议 / 审核',119,851,482)
  elif m=='staff':trio(d,['分类状态','批量添加','移除重申'],a)
  elif m=='bind':o.old.old.shop(d,102,551,'对应商家');arrow(d,(342,666),(414,666));avatar(d,548,650,.81,'merchant');badge(d,'一个商家 · 一位绑定拓展员',127,851,467)
  elif m=='fees':pair(d,'实际支付订单','拓展费明细',a);badge(d,'订单金额 × 配置抽点比例',132,851,457)
  elif m=='quota':trio(d,['额度增减','费用明细','转到余额'],a)
  elif m=='rewards':doc(d,103,525,225,289,'入驻审核记录');arrow(d,(353,668),(414,668));clock(d,531,665,a);badge(d,'按规则时间 · 查奖励记录',140,851,440)
  else:trio(d,['绑定商户','流水时间维度','团队统计'],a)
 elif i=='warehouse':
  if m in ['intro','products']:parcel(d,107,549,219,227,'仓库商品');arrow(d,(352,667),(413,667));doc(d,448,541,176,263,'商城商品关联');badge(d,'商品建档 · 配件或成品',146,851,428)
  elif m=='inbound':doc(d,103,526,226,289,'入库单及模板');arrow(d,(353,667),(414,667));parcel(d,448,559,176,220,'库存增加')
  elif m=='outbound':parcel(d,106,552,221,228,'库存校验');arrow(d,(353,668),(414,668));doc(d,448,540,176,265,'出库及日志')
  elif m=='reversal':trio(d,['确认单据','删除处理','库存回退'],a)
  elif m in ['assemble','split']:
   if m=='assemble':parcel(d,102,537,145,121,'配件甲');parcel(d,151,696,145,121,'配件乙');arrow(d,(328,668),(414,668));parcel(d,450,560,173,219,'成品增加')
   else:parcel(d,103,557,208,226,'成品减少');arrow(d,(338,668),(410,668));parcel(d,449,537,173,121,'配件甲');parcel(d,449,696,173,121,'配件乙')
  elif m=='inventory':trio(d,['系统库存','实际库存','差异调整'],a);badge(d,'草稿填写 · 确认完成',150,851,421)
  else:pair(d,'商城及收银订单','关联出入库单',a);badge(d,'发货出库 / 退货按配置入库',121,851,479)
 elif i=='weishangsucai':
  if m in ['intro','content']:doc(d,103,527,224,289,'分类与素材内容');arrow(d,(353,667),(414,667));poster(d,421,523,a)
  elif m=='download':trio(d,['复制文案','保存图片','保存视频'],a)
  elif m=='switch':tags(d,['系统专属海报总开关','素材内专属海报开关','逐张进入海报设计'],a)
  elif m=='design':poster(d,108,525,a);arrow(d,(355,668),(413,668));badge(d,'码、文字、图片',412,526,232,a);badge(d,'昵称头像及阴影',421,661,214);badge(d,'拖拽缩放及图层',421,793,214)
  elif m=='generate':avatar(d,148,651,.8,'user');arrow(d,(246,667),(327,667));poster(d,373,524,a);badge(d,'生成专属图 · 原图保持不变',131,851,459)
  else:poster(d,106,527,a);arrow(d,(355,666),(414,666));badge(d,'逐图核对',437,546,185,a);badge(d,'未设计用默认码',423,717,213)
 elif i=='wuxing':
  if m in ['intro','rules']:elements(d,a)
  elif m=='config':tags(d,['AI功能与工作流配置','AI状态查询','异步任务状态查询'],a)
  elif m=='task':trio(d,['提交记录','等待异步任务','获取文化内容'],a)
  elif m=='free':pair(d,'会员等级条件','每日免费次数',a)
  elif m=='recommend':doc(d,104,528,224,286,'推荐规则');arrow(d,(354,668),(414,668));badge(d,'商城商品',441,548,182,a);badge(d,'预约服务',441,717,182);badge(d,'切换类型清除此前所选内容',129,851,464)
  elif m=='records':pair(d,'互动记录详情','状态及导出',a)
  else:trio(d,['时间维度','类型分布','使用统计'],a)
 else:raise ValueError(i)
def motion(d,cfg,c,u):
 i=cfg['id'];m=c['visual'];a=cfg['accent']
 if m=='close':return
 if i=='timedlottery' and m in ['intro','draw']:
  x,y=527,665;an=u*.2;line(d,[(x,y),(x+70*math.sin(an),y-70*math.cos(an))],a,4)
 elif i=='warehouse' and m in ['inbound','outbound','assemble','split']:
  x=356+55*((u*.35)%1);d.ellipse((x-5,662,x+5,672),fill=a)
 elif i=='weishangsucai' and m=='design':
  y=608+80*((u*.2)%1);line(d,[(137,y),(306,y)],a,3)
 elif i=='wuxing' and m in ['intro','rules']:
  an=-math.pi/2+(int(u/2)%5)*2*math.pi/5;x=360+201*math.cos(an);y=675+201*math.sin(an);d.ellipse((x-5,y-5,x+5,y+5),fill=a)
 else:d.ellipse((88,866,98,876),fill=a if math.sin(u*1.6)>0 else C['mint'])
