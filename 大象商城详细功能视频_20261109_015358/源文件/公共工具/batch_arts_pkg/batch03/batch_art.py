import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import run_series as r
from graphics import *
# Original illustrated business objects. None are product screenshots or fake forms.
def clock(d,x,y,s=1):
 d.ellipse((x-51*s,y-51*s,x+51*s,y+51*s),fill=C['mint'],outline=C['ink'],width=4);line(d,[(x,y-32*s),(x,y),(x+27*s,y+17*s)],C['ink'],5)
def check(d,x,y):line(d,[(x-13,y),(x-2,y+12),(x+20,y-16)],C['ink'],5)
def doc(d,x,y,w=170,h=220,label='资料'):
 rr(d,(x,y,x+w,y+h),C['white'],16,C['ink']);d.polygon([(x+w-37,y),(x+w,y+37),(x+w-37,y+37)],fill=C['mint']);center(d,label,x+w/2,y+44,27,width=w-18)
 for yy in range(int(y+112),int(y+h-18),28):line(d,[(x+23,yy),(x+w-24,yy)],'#B5C9B9',4)
def phone(d,x,y,w=154,h=283,label='App'):
 rr(d,(x,y,x+w,y+h),C['ink'],26);rr(d,(x+10,y+15,x+w-10,y+h-15),C['cream'],18);center(d,label,x+w/2,y+h*.4,27,width=w-26);line(d,[(x+w*.37,y+h-30),(x+w*.63,y+h-30)],C['mint'],4)
def bubble(d,x,y,t,w=160,fill=None):
 rr(d,(x,y,x+w,y+80),fill or C['mint'],20);d.polygon([(x+28,y+75),(x+17,y+98),(x+60,y+75)],fill=fill or C['mint']);center(d,t,x+w/2,y+22,27,width=w-18)
def folder(d,x,y,w=170,h=150,label='分类'):
 rr(d,(x,y,x+w*.6,y+45),C['orange'],12);rr(d,(x,y+25,x+w,y+h),C['mint'],15,C['ink']);center(d,label,x+w/2,y+66,27,width=w-18)
def gift(d,x,y,s=1,label='礼物'):
 rr(d,(x-58*s,y-42*s,x+58*s,y+56*s),C['orange'],10,C['ink']);d.rectangle((x-8*s,y-42*s,x+8*s,y+56*s),fill=C['cream']);rr(d,(x-66*s,y-57*s,x+66*s,y-31*s),C['mint'],7,C['ink']);d.arc((x-42*s,y-99*s,x+5*s,y-52*s),20,340,fill=C['ink'],width=4);d.arc((x-4*s,y-99*s,x+43*s,y-52*s),180,520,fill=C['ink'],width=4)
 if label:center(d,label,x,y+79*s,25,width=170)
def disc(d,x,y,s=1):
 d.ellipse((x-95*s,y-95*s,x+95*s,y+95*s),fill=C['ink']);d.ellipse((x-61*s,y-61*s,x+61*s,y+61*s),outline=C['mint'],width=3);d.ellipse((x-29*s,y-29*s,x+29*s,y+29*s),fill=C['orange']);d.ellipse((x-5*s,y-5*s,x+5*s,y+5*s),fill=C['cream'])
def camera(d,x,y,label='影像'):
 rr(d,(x-69,y-43,x+69,y+48),C['mint'],16,C['ink']);rr(d,(x-42,y-59,x+3,y-28),C['ink'],7);d.ellipse((x-31,y-29,x+31,y+33),fill=C['cream'],outline=C['ink'],width=4);d.ellipse((x-16,y-14,x+16,y+18),fill=C['orange']);center(d,label,x,y+75,26,width=190)
def shop(d,x,y,s=1,label='商家'):
 rr(d,(x-66*s,y-12*s,x+66*s,y+112*s),C['mint'],11,C['ink']);d.polygon([(x-79*s,y-15*s),(x-56*s,y-64*s),(x+56*s,y-64*s),(x+79*s,y-15*s)],fill=C['orange'],outline=C['ink'],width=3);line(d,[(x-79*s,y-15*s),(x+79*s,y-15*s)],C['ink'],4);center(d,label,x,y+33*s,25,width=143*s)
def flow3(d,ls,y=636,kind='circle'):
 for k,label in enumerate(ls):
  x=150+k*210
  if kind=='doc':doc(d,x-73,y-100,146,187,label)
  else:d.ellipse((x-62,y-62,x+62,y+62),fill=C['orange'] if k==1 else C['mint'],outline=C['ink'],width=3);center(d,label,x,y-17,27,width=130)
  if k<2:arrow(d,(x+78,y),(x+132,y))
def pillstack(d,ls,x=300,y=504,w=307):
 for k,label in enumerate(ls):badge(d,label,x,y+k*100,w,C['orange'] if k==1 else C['mint'])
def tree(d,depth=2):
 coords=[(360,535),(206,682),(514,682)]
 if depth>2:coords +=[(118,822),(277,822),(445,822),(604,822)]
 for a,b in [(0,1),(0,2)]+([(1,3),(1,4),(2,5),(2,6)] if depth>2 else []):line(d,[coords[a],coords[b]],C['ink'],4)
 for k,(x,y) in enumerate(coords):
  d.ellipse((x-37,y-37,x+37,y+37),fill=C['orange'] if k==0 else C['mint'],outline=C['ink'],width=3);center(d,'主' if k==0 else str(k),x,y-20,25,width=74)
 center(d,'会员推荐关系',360,454,27)
def regions(d,x=360,y=650):
 for k,t in enumerate(['省份','城市','区县','街道']):
  xx=x-247+(k%2)*278;yy=y-158+(k//2)*173;rr(d,(xx,yy,xx+218,yy+121),C['mint'] if k%2 else C['orange'],24,C['ink']);center(d,t,xx+109,yy+40,30,width=200)
def shirt(d,x,y,s=1):
 p=[(x-29*s,y-55*s),(x-73*s,y-27*s),(x-51*s,y+13*s),(x-35*s,y),(x-35*s,y+90*s),(x+35*s,y+90*s),(x+35*s,y),(x+51*s,y+13*s),(x+73*s,y-27*s),(x+29*s,y-55*s)];d.polygon(p,fill=C['orange'],outline=C['ink'],width=3)
def envelope(d,x,y,w=220,h=150,label='通知'):
 rr(d,(x,y,x+w,y+h),C['mint'],16,C['ink']);line(d,[(x+4,y+4),(x+w/2,y+h*.56),(x+w-4,y+4)],C['ink'],4);center(d,label,x+w/2,y+h*.62,25,width=w-18)
def art(d,cfg,c,u,index):
 i=cfg['id'];m=c['visual']
 if m=='close':
  for k,t in enumerate(cfg['phases']):
   x,y=[(150,550),(570,550),(570,780),(150,780)][k];d.ellipse((x-51,y-51,x+51,y+51),fill=C['orange'] if k%2 else C['mint']);center(d,str(k+1),x,y-25,35);center(d,t,x,y+74,27,width=215)
  arrow(d,(224,550),(494,550));arrow(d,(570,612),(570,715));arrow(d,(494,780),(224,780));return
 if i=='cityagent':
  if m in ['intro','regions']:regions(d);badge(d,'级别 → 对应覆盖区域',152,852,416)
  elif m=='member':avatar(d,142,650,.88,'user');arrow(d,(246,652),(301,652));doc(d,341,506,260,310,'代理档案');badge(d,'选择并绑定会员',194,852,332)
  elif m=='identities':
   avatar(d,145,649,.91,'user')
   for k,t in enumerate(['区县身份','街道身份']):badge(d,t,379,550+k*180,237);arrow(d,(248,649),(355,577+k*180))
   badge(d,'同一会员，不同区域身份',140,846,440)
  elif m=='partner':avatar(d,139,560,.67,'user');avatar(d,139,766,.67,'user');arrow(d,(226,577),(341,663));arrow(d,(226,778),(341,663));folder(d,386,558,220,207,'合伙组');badge(d,'级别 / 区域保持对应',155,858,410)
  elif m=='status':doc(d,111,502,242,312,'代理列表');pillstack(d,['待审核','正常','禁用'],419,524,196)
  elif m=='records':doc(d,107,514,215,296,'代理档案');arrow(d,(348,659),(403,659));pillstack(d,['分类与参数','账户与累计','记录明细'],429,528,196)
  elif m=='withdraw':flow3(d,['申请','审核','确认']);badge(d,'拒绝 / 审核中 / 已完成',146,843,428)
  else:doc(d,103,511,250,304,'筛选记录');arrow(d,(377,657),(430,657));doc(d,463,542,157,244,'导出')
 elif i=='citytelbook':
  if m in ['intro','apply']:shop(d,170,604,1.05,'演示商家');arrow(d,(284,662),(344,662));doc(d,390,497,229,325,'入驻资料');badge(d,'录入 / 自助申请',188,855,344)
  elif m=='category':folder(d,111,502,214,168,'城市');arrow(d,(353,592),(408,592));pillstack(d,['一级行业','二级行业','三级行业'],429,502,192)
  elif m=='audit':doc(d,107,529,216,271,'申请');arrow(d,(350,656),(414,559));arrow(d,(350,656),(414,750));badge(d,'通过',444,531,176);badge(d,'驳回',444,722,176,C['orange'])
  elif m=='status':avatar(d,137,650,.86,'merchant');pillstack(d,['条目上下架','推荐设置','入驻与审核开关'],302,511,317)
  elif m=='browse':doc(d,115,499,275,326,'商家详情');pillstack(d,['图片与简介','营业时间','联系信息'],423,534,198)
  elif m=='contact':phone(d,111,513,161,299,'联系');arrow(d,(302,657),(354,657));pillstack(d,['电话拨打','地址导航','收藏回找'],396,525,227)
  else:
   line(d,[(120,817),(120,513)],C['ink'],4)
   for k,t in enumerate(['浏览','拨打','申请']):x=200+k*157;h=[137,220,170][k];rr(d,(x,817-h,x+72,817),C['orange'] if k==1 else C['mint'],11);center(d,t,x+36,843,25,width=130)
 elif i=='coupon_hub':
  if m in ['intro','scope']:folder(d,105,533,207,219,'业务范围');arrow(d,(337,659),(396,659));ticket(d,423,574,204,174,'业务券');badge(d,'与商城营销券分开',179,844,362)
  elif m=='select':
   for k,t in enumerate(['选业务','加券','保存']):folder(d,101+k*209,536+k*32,150,163,t)
  elif m=='issue':avatar(d,137,649,.85,'merchant');ticket(d,293,522,236,151,'业务券');arrow(d,(403,700),(403,758));badge(d,'搜索会员 → 发放',264,813,354)
  elif m=='claim':avatar(d,142,650,.87,'user');arrow(d,(247,659),(314,659));ticket(d,360,547,260,194,'主动领取');badge(d,'可领列表 → 我的券',163,842,394)
  elif m=='entry':folder(d,105,527,198,210,'领券中心');arrow(d,(328,658),(391,658));folder(d,423,527,198,210,'我的业务券');badge(d,'通用入口 / 到家范围入口',136,851,448)
  elif m=='links':flow3(d,['装修','链接','会员']);ticket(d,243,761,235,130,'业务券入口')
  else:doc(d,111,503,254,319,'发券流水');pillstack(d,['目标会员','所属业务','发放场景'],414,529,204)
 elif i=='cpcnpay':
  if m in ['intro','subject']:avatar(d,143,652,.88,'merchant');doc(d,317,494,280,332,'商户资料');badge(d,'主体类型 → 对应资料',158,850,404)
  elif m=='documents':flow3(d,['影印件','采集','注册'],kind='doc');badge(d,'主体资料前后对应',184,844,352)
  elif m=='bank':doc(d,110,516,226,298,'绑定申请');arrow(d,(359,655),(413,655));phone(d,454,525,154,277,'确认');badge(d,'申请 → 验证 → 绑定状态',135,848,450)
  elif m=='contract':doc(d,113,505,255,320,'签约申请');arrow(d,(393,660),(448,660));avatar(d,554,654,.77,'user');badge(d,'签约人类型 / 确认环节',143,856,434)
  elif m=='apply':doc(d,108,507,237,319,'商户申请');pillstack(d,['支付方式','支付类别','提交申请'],412,528,207)
  elif m=='status':pillstack(d,['待审核 / 审核中','通过 / 拒绝','生效 / 失效'],159,511,403)
  else:doc(d,103,516,229,294,'申请记录');d.ellipse((438,589,547,698),outline=C['orange'],width=10);line(d,[(537,688),(586,737)],C['orange'],10);badge(d,'定位具体失败环节',182,852,356)
 elif i=='dailyjinju':
  if m in ['intro','category']:folder(d,105,521,214,220,'学习大类');arrow(d,(345,662),(401,662));doc(d,437,515,176,276,'章节');badge(d,'分类 / 内容 / 顺序',166,844,388)
  elif m=='chapter':
   for k,t in enumerate(['第1章','第2章','第3章']):doc(d,103+k*208,523+k*37,149,197,t)
   badge(d,'章节排序决定解锁顺序',149,852,422)
  elif m=='days':clock(d,183,649,1.32);arrow(d,(276,649),(330,649));pillstack(d,['当天不重复','新一天再增加'],369,552,259);badge(d,'累计，不因间隔清零',156,844,408)
  elif m=='progress':folder(d,109,544,206,211,'主题甲');folder(d,411,544,206,211,'主题乙');badge(d,'每个大类，独立计数',162,839,396)
  elif m=='access':avatar(d,140,655,.87,'user');pillstack(d,['选择等级范围','不符合时跳转','独立访问配置'],310,522,310)
  elif m=='free':doc(d,105,515,217,293,'试读章节');arrow(d,(346,660),(399,660));doc(d,435,515,180,293,'打卡章节');badge(d,'不同配置选项',211,848,298)
  else:doc(d,109,507,239,312,'解锁记录');pillstack(d,['大类 / 会员','日期 / 天数','已解锁数量'],407,531,212)
 elif i=='danshujiang':
  if m in ['intro','objects']:avatar(d,143,652,.88,'user');shirt(d,443,626,1.19);badge(d,'适用等级 × 适用商品',152,847,416)
  elif m=='count':avatar(d,143,656,.88,'user');pillstack(d,['本人订单口径','推荐订单口径'],314,548,302);badge(d,'先选计数口径，再配规则',131,847,458)
  elif m=='modes':
   d.ellipse((102,557,214,669),fill=C['mint']);center(d,'单数',158,590,26,width=118);center(d,'普通',158,765,27,width=160)
   for k in range(3):d.rectangle((294+k*35,684-k*47,323+k*35,732),fill=C['orange'])
   center(d,'阶梯',348,765,27,width=160);d.arc((476,539,624,705),30,340,fill=C['ink'],width=9);center(d,'循环',550,765,27,width=160)
  elif m=='advanced':clock(d,178,650,1.18);pillstack(d,['循环与计算基准','贡献值扣除','生成时 / 领取时'],316,511,310)
  elif m=='manual':flow3(d,['申请','审核','处理']);badge(d,'奖励记录：筛选 / 搜索',149,848,422)
  elif m=='auto':clock(d,164,647,1.23);arrow(d,(250,649),(311,649));doc(d,353,509,254,303,'任务规则');badge(d,'先完成对应接入与任务配置',106,851,508)
  elif m=='settlement':doc(d,110,510,224,305,'订单');pillstack(d,['支付 / 收货','退款调整','后续序号不变'],401,525,218)
  else:doc(d,109,526,226,283,'单数奖励');arrow(d,(359,665),(414,665));doc(d,449,526,170,283,'团队分红');badge(d,'独立极差开关',216,848,288)
 elif i=='daojia':
  if m in ['intro','order']:avatar(d,138,650,.85,'user');doc(d,317,504,279,316,'服务订单');badge(d,'选择服务 → 确认商品价',144,852,432)
  elif m in ['price','levels']:doc(d,106,516,224,299,'服务商品');pillstack(d,['对应会员等级','启用专属价格','未设用销售价'],384,522,240)
  elif m=='basis':badge(d,'实际商品价',103,615,218);arrow(d,(346,641),(409,550));arrow(d,(346,641),(409,743));badge(d,'平台抽佣',436,522,186);badge(d,'技师收入基准',398,716,224);badge(d,'围绕本次订单核对',177,851,366)
  elif m=='switches':pillstack(d,['系统总开关','商品参与开关','商品比例参数'],157,505,406)
  elif m=='timing':clock(d,187,647,1.35);pillstack(d,['服务完成','支付成功'],360,548,256);badge(d,'选择结算时机',204,844,312)
  else:badge(d,'商品实付价',113,563,229);badge(d,'路费',422,563,184,C['orange']);arrow(d,(226,640),(226,738));badge(d,'计算基准',119,759,216);center(d,'分别核对',520,758,28,width=210)
 elif i=='core_notice_push':
  if m in ['intro','list']:envelope(d,107,544,227,164);arrow(d,(356,629),(413,629));doc(d,452,510,165,272,'后台通知');badge(d,'创建通知 ≠ 已经外发',142,838,436)
  elif m=='targets':
   for k,t in enumerate(['单个会员','会员名单','符合条件用户']):avatar(d,149+k*210,630,.58,'user');center(d,t,149+k*210,773,25,width=190)
  elif m in ['channels','dispatch']:flow3(d,['小程序','公众号','短信']);badge(d,'先配置渠道与接收条件',154,845,412)
  elif m=='results':
   for k,t in enumerate(['渠道一','渠道二','渠道三']):
    y=520+k*115;badge(d,t,148,y,233);check(d,481,y+26) if k!=1 else line(d,[(463,y+11),(496,y+44)],C['orange'],6)
   badge(d,'分别看数量与状态',182,863,356)
  else:envelope(d,110,565,223,158);arrow(d,(358,649),(412,649));clock(d,523,650,1.18);badge(d,'重发前先编辑通知状态',152,845,416)
 elif i=='core_commission_order':
  if m in ['intro','entry']:doc(d,105,512,224,303,'佣金明细');arrow(d,(354,660),(410,660));doc(d,449,512,174,303,'业务订单');badge(d,'查看关联订单',225,850,270)
  elif m=='types':
   for k,t in enumerate(['商城 / 拼团','预约 / 课程','买单 / 餐饮']):folder(d,101+k*209,538+k*30,150,168,t)
  elif m=='match':pillstack(d,['佣金记录','分红记录','备注辅助识别'],135,507,445)
  else:doc(d,113,507,261,312,'原始记录');d.ellipse((442,581,551,690),outline=C['orange'],width=10);line(d,[(539,680),(589,730)],C['orange'],10);badge(d,'核对会员与业务来源',167,851,386)
 elif i=='core_product_display':
  if m in ['intro','layout']:
   rr(d,(173,493,547,865),C['white'],27,C['ink']);rr(d,(192,510,528,684),C['mint'],19);shirt(d,361,586,.6);center(d,'商品图片',360,697,26);center(d,'标题 · 标签 · 价格区',360,775,24,width=340)
  elif m in ['data','tags']:shirt(d,173,645,1.22);arrow(d,(285,657),(341,657));pillstack(d,['商品分组','服务标签','显示开关'],373,526,251)
  elif m=='component':folder(d,103,546,213,204,'商品组件');arrow(d,(343,658),(399,658));pillstack(d,['分组标签','服务标签','商品卖点'],426,523,194)
  elif m=='style':
   for k,rad in enumerate([2,23,48]):rr(d,(102+k*208,553,252+k*208,752),C['orange'] if k==1 else C['mint'],rad,C['ink'])
   badge(d,'圆角 / 边距 / 背景',174,843,372)
  else:doc(d,106,510,223,303,'设计器预览');arrow(d,(355,660),(409,660));doc(d,449,510,170,303,'发布页面');badge(d,'先核对内容与开关',186,850,348)
 elif i=='core_business_home':
  if m in ['intro','identity']:shop(d,186,586,1.1,'示例门店');pillstack(d,['店名与信息','营业时间','商家详情'],371,527,249)
  elif m=='template':avatar(d,135,650,.86,'merchant');pillstack(d,['经典模板','图式模板','平台统一选择'],307,523,313)
  elif m=='photos':
   for k in range(2):
    x=103+k*274;rr(d,(x,532,x+238,765),C['mint'],23,C['ink']);d.ellipse((x+133,556,x+188,611),fill=C['orange']);d.polygon([(x+18,730),(x+92,623),(x+203,730)],fill=C['ink'])
   badge(d,'点击 → 预览全部照片',156,843,408)
  elif m=='entry':shop(d,188,604,1.1,'门店');arrow(d,(307,658),(363,658));pillstack(d,['买单开关','门店切换'],405,553,215)
  elif m=='contact':
   for x in [142,269,396,523]:line(d,[(x,519),(x+22,788)],'#CFD9CE',5)
   for y in [560,659,759]:line(d,[(105,y),(608,y+20)],'#CFD9CE',5)
   r.pin(d,355,637);badge(d,'地址 → 导航 / 联系',161,843,398)
  elif m=='products':shop(d,171,617,1.04,'商家');arrow(d,(285,660),(346,660));doc(d,393,505,220,311,'商品详情');badge(d,'列表价格与商品入口',165,848,390)
  else:folder(d,109,544,218,206,'商家DIY');folder(d,416,544,200,206,'默认模板');badge(d,'先看DIY，再看默认模板',139,847,442)
