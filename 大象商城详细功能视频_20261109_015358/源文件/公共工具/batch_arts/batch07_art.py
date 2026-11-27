import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from graphics import *

def doc(d,x,y,w=203,h=244,label='业务记录'):
 rr(d,(x,y,x+w,y+h),C['white'],18,C['ink']);d.polygon([(x+w-40,y),(x+w,y+40),(x+w-40,y+40)],fill=C['mint']);center(d,label,x+w/2,y+37,25,width=w-20)
 for yy in range(int(y+118),int(y+h-18),36):line(d,[(x+24,yy),(x+w-24,yy)],'#B6C8BA',4)
def tags(d,arr,accent):
 for k,t in enumerate(arr):
  y=529+k*105;rr(d,(146,y,576,y+76),accent if k==1 else C['mint'],22,C['ink']);center(d,t,361,y+18,26,width=408)
def trio(d,arr,accent):
 for k,t in enumerate(arr):
  x=157+k*203;rr(d,(x-79,564,x+79,790),accent if k==1 else C['mint'],21,C['ink']);center(d,t,x,625,25,width=142)
  if k<2:arrow(d,(x+83,675),(x+117,675))
def bubble(d,x,y,w,h,t,accent):
 rr(d,(x,y,x+w,y+h),accent,21,C['ink']);d.polygon([(x+31,y+h-2),(x+27,y+h+24),(x+58,y+h-2)],fill=accent,outline=C['ink'],width=2);center(d,t,x+w/2,y+25,25,width=w-30)
def parcel(d,x,y,w=173,h=154,label='门店商品'):
 rr(d,(x,y,x+w,y+h),C['mint'],14,C['ink']);line(d,[(x,y+43),(x+w,y+43)],C['ink'],3);line(d,[(x+w/2,y),(x+w/2,y+43)],C['ink'],3);center(d,label,x+w/2,y+66,23,width=w-15)
def shop(d,x,y,label='本地门店'):
 rr(d,(x,y+53,x+210,y+228),C['white'],15,C['ink']);rr(d,(x-7,y,x+217,y+68),C['orange'],15,C['ink']);center(d,label,x+105,y+98,26,width=190)
 for xx in [x+27,x+83,x+139]:line(d,[(xx,y+7),(xx-13,y+58)],C['cream'],12)
def van(d,x,y):
 rr(d,(x,y,x+172,y+100),C['mint'],16,C['ink']);rr(d,(x+130,y+29,x+213,y+100),C['orange'],13,C['ink']);d.ellipse((x+24,y+80,x+66,y+122),fill=C['ink']);d.ellipse((x+156,y+80,x+198,y+122),fill=C['ink'])
def seal(d,x,y,t,accent):
 d.ellipse((x-58,y-58,x+58,y+58),fill=accent,outline=C['ink'],width=4);center(d,t,x,y-19,24,width=107)
def hub(d,items,accent):
 positions=[(185,557),(535,557),(185,768),(535,768)]
 for (x,y),t in zip(positions,items):line(d,[(360,662),(x,y)],C['ink'],4);rr(d,(x-106,y-47,x+106,y+47),C['mint'],20,C['ink']);center(d,t,x,y-19,23,width=196)
 seal(d,360,662,'授权',accent)
def check(d,x,y):line(d,[(x-15,y),(x-3,y+13),(x+23,y-18)],C['ink'],7)
def art(d,cfg,c,u,index):
 ident=cfg['id'];m=c['visual'];a=cfg['accent'];pts=c['points']
 if m=='close':
  for k,(x,y) in enumerate([(163,547),(553,547),(553,765),(163,765)]):seal(d,x,y,str(k+1),a if k%2==0 else C['mint']);center(d,cfg['phases'][k],x,y+74,26,width=220)
  for st,en in [((235,547),(480,547)),((553,615),(553,696)),((480,765),(235,765))]:arrow(d,st,en,C['mint'])
  return
 if ident=='luntan':
  if m in ['intro','publish']:
   avatar(d,146,654,.83,'user');arrow(d,(244,665),(317,665));bubble(d,352,523,263,268,'图文 / 视频帖子',C['mint']);d.rectangle((405,638,563,739),fill=C['cream'],outline=C['ink'],width=3);d.polygon([(425,719),(464,665),(502,707),(535,673),(549,719)],fill=a)
  elif m=='categories':
   badge(d,'论坛分类',262,511,196,a);arrow(d,(360,566),(360,623));line(d,[(191,626),(530,626)],C['ink'],4)
   for x,t in [(191,'一级栏目'),(530,'一级栏目')]:arrow(d,(x,627),(x,683));badge(d,t,x-92,697,184);center(d,'二级分类 · 图片 · 排序',x,788,22,width=280)
  elif m=='review':doc(d,105,525,224,287,'待审核帖子');arrow(d,(355,665),(412,665));badge(d,'查看与审核',440,550,180,a);badge(d,'置顶 / 删除',440,717,180)
  elif m in ['comments','replies']:
   bubble(d,104,522,303,126,'主评论' if m=='replies' else '帖子内容',C['mint']);arrow(d,(282,685),(383,721));bubble(d,338,722,275,128,'回复审核' if m=='replies' else '评论与点赞',a)
  else:trio(d,['查看量','点赞量','评论量'],a);badge(d,'三种口径分别核对',158,851,404)
 elif ident=='maiyatian':
  if m in ['intro','stores']:shop(d,101,549,'本地门店');arrow(d,(340,673),(409,673));shop(d,429,549,'配送门店');badge(d,'同步并建立对应关系',158,851,405)
  elif m=='settings':tags(d,['环境与回调','发单策略','余额与扣费开关'],a)
  elif m=='modes':
   for (x,y),t in zip([(205,577),(516,577),(205,755),(516,755)],['价格优先','速度优先','指定运力','顺序呼叫']):rr(d,(x-112,y-61,x+112,y+61),a if y<600 else C['mint'],22,C['ink']);center(d,t,x,y-18,26,width=200)
  elif m=='dispatch':doc(d,107,527,219,285,'原订单资料');arrow(d,(353,666),(410,666));doc(d,445,543,179,258,'配送接口');badge(d,'选门店 · 组商品 · 发请求',140,851,441)
  elif m=='tracking':
   for k,t in enumerate(['待接单','到店取货','完成取消']):
    x=157+k*203;seal(d,x,566,t,a if k==1 else C['mint'])
   line(d,[(114,799),(603,799)],C['ink'],4);van(d,237,672);badge(d,'骑手与节点按回传核对',145,851,430)
  else:doc(d,107,525,221,287,'配送回调');arrow(d,(353,666),(412,666));badge(d,'接单配送费',437,544,183,a);badge(d,'取消违约金',437,716,183);badge(d,'扣费开关与资金流水对应',134,851,453)
 elif ident=='matrixreward':
  if m in ['intro','structure','placement']:
   positions=[(360,530),(160,661),(360,661),(560,661),(160,803),(360,803),(560,803)]
   for x,y in positions[1:4]:line(d,[(360,550),(x,y-24)],C['ink'],3)
   for (x,y),(xx,yy) in zip(positions[1:4],positions[4:]):line(d,[(x,y+25),(xx,yy-25)],C['ink'],3)
   for k,(x,y) in enumerate(positions):d.ellipse((x-27,y-27,x+27,y+27),fill=a if k==2 else C['mint'],outline=C['ink'],width=3)
   badge(d,'独立点位关系示意',151,856,419)
  elif m=='unlocks':doc(d,105,522,224,293,'层级规则');arrow(d,(354,668),(413,668));rr(d,(448,545,618,799),C['mint'],24,C['ink']);d.arc((485,589,583,689),180,360,fill=C['ink'],width=6);rr(d,(485,640,584,731),a,14,C['ink']);badge(d,'规则条件 → 解锁日志',151,851,419)
  elif m=='orders':doc(d,105,525,223,288,'商城订单');arrow(d,(353,666),(413,666));doc(d,448,543,174,256,'对应层记录');badge(d,'订单 / 点位 / 解锁分别核对',116,851,489)
  else:trio(d,['矩阵点位','解锁日志','奖励日志'],a)
 elif ident=='mendiangroupbuy':
  if m in ['intro','bind']:avatar(d,149,655,.82,'merchant');arrow(d,(247,666),(324,666));shop(d,382,548,'绑定门店');badge(d,'只维护本店货盘',163,851,395)
  elif m in ['warehouse','status']:
   for k,t in enumerate(['现有商品','上下架','推荐状态']):parcel(d,93+k*202,574,133,186,t)
   badge(d,'搜索与状态分别维护',149,851,423)
  elif m=='add':
   for k in range(3):parcel(d,103+k*21,536+k*27,172,146,'可选商品库' if k==2 else '')
   arrow(d,(353,667),(411,667));parcel(d,443,585,179,170,'本店货盘');badge(d,'多选加入 · 排除已有商品',140,851,442)
  elif m=='remove':parcel(d,110,572,208,198,'本店货盘');arrow(d,(348,668),(414,668));doc(d,449,538,174,272,'货盘关联移出');badge(d,'货盘关系与商品资料分开',134,851,453)
  else:shop(d,102,548,'本店货盘');arrow(d,(343,669),(412,669));avatar(d,549,651,.83,'user');badge(d,'对应门店的商品展示',154,851,413)
 elif ident=='mpcenter':
  if m in ['intro','account']:hub(d,['授权绑定','账号资料','服务类目','权限范围'],a)
  elif m=='qualification':doc(d,104,523,224,291,'材料与草稿');arrow(d,(351,668),(412,668));doc(d,447,543,175,256,'提交和查询');badge(d,'微信授权付费由管理员确认',122,851,477)
  elif m=='privacy':tags(d,['隐私指引','用途和联系方式','位置接口开通状态'],a)
  elif m=='location':
   for k in range(3):doc(d,107+k*23,530+k*30,178,214,'证明材料' if k==2 else '')
   arrow(d,(351,668),(412,668));seal(d,535,667,'完整性',a);badge(d,'图片 / 视频 / 说明页',148,851,425)
  elif m=='shipping':doc(d,105,526,222,288,'发货与履约');arrow(d,(352,666),(412,666));doc(d,448,543,174,257,'订单详情路径')
  elif m=='links':trio(d,['跳转链接','短链接','小程序码'],a);badge(d,'不同渠道 · 对应不同入口',134,851,453)
  elif m=='services':hub(d,['客服消息','交易投诉','交易保障','物流基础'],a)
  elif m=='ecosystem':hub(d,['好物圈','交易组件','联盟推客','微信AI申诉'],a)
  elif m=='official':trio(d,['带参二维码','订阅通知','图文发布'],a);badge(d,'公众号补充能力',163,851,395)
  else:avatar(d,146,651,.82,'merchant');arrow(d,(244,666),(321,666));doc(d,359,523,260,291,'令牌动作范围');badge(d,'按账号 / 类目 / 认证授权',124,851,473)
 elif ident=='ordercvt':
  if m in ['intro','submit']:avatar(d,146,653,.82,'user');arrow(d,(244,666),(320,666));doc(d,357,522,260,291,'外部订单号');badge(d,'金额 / 凭证 / 备注',163,851,395)
  elif m=='settings':tags(d,['奖励类型与比例','金额及凭证要求','页面展示开关'],a)
  elif m=='review':doc(d,105,523,223,292,'人工核对资料');arrow(d,(352,666),(413,666));badge(d,'改审核金额',440,544,180,a);badge(d,'通过 / 拒绝',440,716,180)
  elif m=='records':doc(d,106,525,222,290,'转换审核记录');arrow(d,(353,666),(413,666));doc(d,448,543,174,256,'对应账户');badge(d,'不抓取外部真实订单',147,851,426)
  else:hub(d,['企业头图','金额设置','客服中心','会员中心'],a)
 elif ident=='core_balance_receipt':
  if m in ['intro','states']:trio(d,['处理中','用户确认','查询成功'],a);badge(d,'发起处理 ≠ 已收款',157,851,407)
  elif m=='confirm':avatar(d,149,653,.82,'user');arrow(d,(247,666),(323,666));doc(d,360,521,257,294,'对应提现记录');seal(d,489,730,'确认',a)
  elif m=='query':doc(d,106,523,222,293,'查询转账状态');arrow(d,(351,666),(412,666));badge(d,'仍在处理中',438,543,184,a);badge(d,'成功 / 失败',438,716,184)
  else:avatar(d,150,650,.81,'merchant');avatar(d,565,650,.81,'user');doc(d,260,559,201,232,'同笔提现状态');arrow(d,(212,675),(244,675));arrow(d,(474,675),(506,675))
 elif ident=='core_maidan_reward_paytype':
  if m in ['intro','settings','choices']:
   doc(d,105,531,220,277,'实际付款类型');arrow(d,(353,666),(414,590));arrow(d,(353,666),(414,760));badge(d,'余额支付',442,558,177,a);badge(d,'微信支付',442,731,177);badge(d,'分别勾选 · 可同时选择',140,851,440)
  elif m=='empty':
   seal(d,200,643,'余额',C['mint']);seal(d,520,643,'微信',C['mint']);line(d,[(249,705),(309,775)],C['ink'],4);line(d,[(471,705),(411,775)],C['ink'],4);badge(d,'两项不选 → 不赠送',151,795,419,a)
  else:doc(d,105,523,223,291,'支付方式匹配');arrow(d,(353,666),(413,666));badge(d,'用户奖励',440,545,180,a);badge(d,'管理员奖励',440,716,180);badge(d,'贡献值和黄积分的适用范围',126,851,469)
 else:raise ValueError(ident)

def motion(d,cfg,c,u):
 ident=cfg['id'];a=cfg['accent'];m=c['visual']
 if m=='close':return
 if ident=='maiyatian' and m=='tracking':
  x=119+481*((u*.1)%1);d.ellipse((x-5,793,x+5,803),fill=a)
 elif ident=='matrixreward' and m in ['intro','structure','placement']:
  x,y=[(360,530),(160,661),(360,661),(560,661),(160,803),(360,803),(560,803)][int(u/2)%7];d.ellipse((x-36,y-36,x+36,y+36),outline=a,width=4)
 elif ident=='mpcenter' and m in ['intro','account','services','ecosystem']:
  ang=u*.6;x=360+74*math.cos(ang);y=662+74*math.sin(ang);d.ellipse((x-5,y-5,x+5,y+5),fill=a)
 elif ident=='luntan' and m in ['comments','replies']:
  for k in range(3):d.ellipse((353+k*20,690,362+k*20,699),fill=a if int(u*2)%3==k else C['mint'])
 elif ident=='mendiangroupbuy' and m=='add':
  x=353+57*((u*.35)%1);d.ellipse((x-5,661,x+5,671),fill=a)
 elif ident in ['core_balance_receipt','core_maidan_reward_paytype']:
  d.ellipse((657,501,665,509),fill=a if math.sin(u*2)>0 else C['mint'])
 else:
  d.ellipse((89,864,97,872),fill=a if math.sin(u*1.7)>0 else C['mint'])
