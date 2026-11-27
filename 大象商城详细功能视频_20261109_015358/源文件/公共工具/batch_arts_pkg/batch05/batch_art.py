import sys,math,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from graphics import *
spec=importlib.util.spec_from_file_location('b04_shapes',str(Path(__file__).resolve().parents[1]/'batch04'/'batch_art.py'));old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def doc(d,x,y,w=180,h=230,label='资料'):old.clean_doc(d,x,y,w,h,label)
def three(d,pts,accent):
 for k,t in enumerate(pts):
  x=155+k*205;rr(d,(x-85,545,x+85,805),accent if k==1 else C['mint'],22,C['ink']);center(d,str(k+1),x,570,34);center(d,t,x,657,25,width=150)
  if k<2:arrow(d,(x+89,640),(x+111,640))
def rows(d,pts,accent):
 for k,t in enumerate(pts):
  y=520+k*126;badge(d,t,180,y,390,accent if k==1 else C['mint'])
  if k<2:arrow(d,(375,y+62),(375,y+113))
def tree(d,label='接点关系',cross=False):
 center(d,label,360,484,26,width=560)
 edges=[((360,599),(191,695)),((191,761),(191,811))]
 if not cross:edges.append(((360,599),(529,695)))
 for a,b in edges:arrow(d,a,b)
 for x,y,t in [(360,555,'推荐人'),(191,717,'接点目标'),(529,717,'网外目标' if cross else '其他分支'),(191,844,'关系记录')]:
  rr(d,(x-78,y-28,x+78,y+28),C['mint'] if x!=529 else C['pink'],19,C['ink']);center(d,t,x,y-17,21,width=150)
 if cross:line(d,[(489,797),(557,865)],C['orange'],7);line(d,[(557,797),(489,865)],C['orange'],7)
def calendar(d,x=116,y=525):
 rr(d,(x,y,x+220,y+262),C['white'],20,C['ink']);rr(d,(x,y,x+220,y+59),C['orange'],18);center(d,'节日日期',x+110,y+13,26,width=200)
 for j in range(3):
  for k in range(4):d.ellipse((x+26+k*47,y+89+j*51,x+43+k*47,y+106+j*51),fill=C['mint'] if (j,k)!=(1,2) else C['orange'])
def art(d,cfg,c,u,index):
 id=cfg['id'];m=c['visual'];pts=c['points'];accent=cfg['accent']
 if m=='close':return old.art(d,cfg,c,u,index)
 if id=='form':
  if m=='fields':
   names=['单行','多行','单选','多选','普通选择','时间','日期','省市区','图片','开关']
   for k,t in enumerate(names):
    x=116+(k%2)*262;y=493+(k//2)*77;rr(d,(x,y,x+228,y+61),accent if k%3==0 else C['mint'],15);center(d,t,x+114,y+13,24,width=210)
  elif m=='bind':
   doc(d,97,523,205,265,'表单字段');doc(d,413,523,205,265,'会员资料');arrow(d,(326,657),(392,657));badge(d,'只更新已绑定字段',177,846,365)
  elif m in ['audit','query','level','validate','payment']:rows(d,pts,accent)
  else:avatar(d,163,654,.85,'user');arrow(d,(252,664),(335,664));doc(d,370,518,235,288,'演示申请');badge(d,'原版后台配置字段',174,846,377)
 elif id=='fxcoupon':
  if m in ['intro','quota','limits']:
   rr(d,(111,535,291,778),C['mint'],20,C['ink']);center(d,'发券预算',201,570,29,width=163)
   for k in range(4):rr(d,(141,645+k*24,261-k*17,658+k*24),accent,5)
   arrow(d,(315,658),(384,658));ticket(d,416,569,190,143,'优惠券',accent);badge(d,'按券面额扣减预算',171,846,378)
  elif m=='coupons':ticket(d,103,561,223,164,'后台券池',accent);ticket(d,401,561,223,164,'自定义券',C['mint']);badge(d,'面额与门槛分别配置',172,828,375)
  elif m=='recipients':tree(d,'按配置选择接收对象');badge(d,'直接下级 / 全团队',197,490,325)
  else:doc(d,107,520,225,293,'发券记录');arrow(d,(356,667),(404,667));ticket(d,436,584,179,131,'我的优惠券',accent)
 elif id=='goldprice':
  if m in ['diy','slots']:
   for k,t in enumerate(['展示位一','展示位二','展示位三']):
    x=160+k*200;rr(d,(x-75,564,x+75,780),accent if k==1 else C['mint'],20,C['ink']);center(d,t,x,600,24,width=140);center(d,'品种代码',x,695,21,width=140)
   badge(d,'首页组件配置示意',182,846,357)
  elif m=='markets':
   names=['上海金交所','期货','银行','港台金店','伦敦','国际现货'];
   for k,t in enumerate(names):
    ang=-math.pi/2+k*math.tau/6;x=360+208*math.cos(ang);y=685+164*math.sin(ang);line(d,[(360,685),(x,y)],C['mint'],4);rr(d,(x-81,y-30,x+81,y+30),accent if k%2 else C['mint'],22);center(d,t,x,y-17,20,width=155)
   d.ellipse((304,629,416,741),fill=C['ink']);center(d,'行情',360,663,29,C['cream'],width=100)
  elif m=='refresh':
   d.ellipse((112,550,326,764),fill=C['mint'],outline=C['ink'],width=4);line(d,[(219,586),(219,658),(271,695)],C['ink'],7);arrow(d,(350,659),(410,659));doc(d,445,536,168,247,'缓存行情');badge(d,'时长与自动刷新',177,846,365)
  elif m=='status':rows(d,pts,accent)
  else:
   for k in range(3):d.polygon([(121+k*34,760-k*29),(230+k*34,760-k*29),(270+k*34,815-k*29),(94+k*34,815-k*29)],fill=accent,outline=C['ink'],width=3)
   arrow(d,(355,665),(412,665));doc(d,445,519,175,284,'行情服务');badge(d,'先配置并测试连接',175,846,370)
 elif id=='goodsrank':
  if m in ['intro','ranking']:
   for k,(x,h,t) in enumerate([(163,135,'第二位'),(360,230,'第一位'),(557,85,'第三位')]):
    rr(d,(x-77,820-h,x+77,820),accent if k==1 else C['mint'],15,C['ink']);center(d,t,x,841,23,width=155)
   badge(d,'排序方式示意',223,490,274)
  elif m=='source':three(d,pts,accent)
  elif m=='design':
   for k in range(3):
    x=106+k*205;rr(d,(x,536,x+153,796),C['white'],16,C['ink']);rr(d,(x+13,550,x+140,607),accent if k==1 else C['mint'],9)
    for j in range(3):line(d,[(x+18,650+j*41),(x+134,650+j*41)],C['ink'],4)
   badge(d,'三种风格 · 抽象示意',167,846,385)
  elif m=='home':
   rr(d,(127,500,593,862),C['mint'],22);center(d,'榜单首页',360,528,30)
   for k,t in enumerate(['已选榜单','已选榜单','独立首页配置']):badge(d,t,197,605+k*78,325,accent if k==2 else C['cream'])
  else:doc(d,115,523,227,289,'榜单内容');arrow(d,(366,665),(411,665));doc(d,446,547,169,243,'分享资料')
 elif id=='hbtk':
  if m in ['lottery','choose','share']:
   ticket(d,99,544,220,151,'订单资格',accent);ticket(d,409,544,220,151,'分享资格',C['mint']);arrow(d,(211,719),(341,809));arrow(d,(519,719),(379,809));badge(d,'选择本次使用资格',178,829,366)
  elif m=='fulfil':doc(d,106,520,220,288,'活动订单');arrow(d,(351,666),(411,666));old.old.folder(d,447,552,168,199,'核销 / 发货');badge(d,'对应独立订单与核销码',153,847,414)
  elif m=='clerk':avatar(d,167,657,.85,'merchant');arrow(d,(265,665),(343,665));doc(d,381,516,232,297,'本活动核销员');badge(d,'先按活动添加与启停',168,847,385)
  elif m=='ranking':rows(d,pts,accent)
  elif m=='export':doc(d,114,518,226,297,'筛选记录');arrow(d,(365,663),(420,663));doc(d,456,547,159,242,'导出表格')
  elif m=='limits':three(d,pts,accent)
  else:avatar(d,156,653,.82,'user');arrow(d,(254,661),(337,661));ticket(d,368,551,248,175,'演示活动订单',accent);badge(d,'参与 → 支付 → 查看资格',135,846,449)
 elif id=='holiday':
  calendar(d)
  if m=='date':
   arrow(d,(363,662),(422,662));rr(d,(459,570,614,751),C['pink'],18,C['ink']);center(d,'同日唯一',536,630,25,width=146)
  elif m=='reference':
   for k,t in enumerate(['今天','未来','过去']):badge(d,t,405,537+k*112,204,accent if k==0 else C['mint'])
  else:
   for k,t in enumerate(pts):badge(d,t,401,534+k*116,215,accent if k==1 else C['mint'])
 elif id=='jiedianmanage':
  if m=='tree':tree(d,'按会员查看接点关系')
  elif m=='audit':doc(d,109,523,231,291,'修改申请');arrow(d,(364,666),(418,666));badge(d,'通过',449,561,159);badge(d,'拒绝',449,681,159,accent)
  elif m in ['rules','check']:rows(d,pts,accent)
  else:avatar(d,167,656,.83,'merchant');arrow(d,(264,663),(336,663));doc(d,373,519,242,296,'接点记录');badge(d,'后台管理与审核',190,846,340)
 elif id=='jiedianteamratio':
  if m=='difference':
   for k,t in enumerate(['设置比例','比例差额','实际比例']):
    x=160+k*200;y=727-k*70;rr(d,(x-74,y-98,x+74,y+94),accent if k==1 else C['mint'],21,C['ink']);center(d,t,x,y-20,24,width=137)
    if k<2:arrow(d,(x+84,y),(x+115,y-38))
   badge(d,'级差处理示意，无收益数据',131,846,459)
  elif m=='dispatch':doc(d,100,528,205,270,'待处理记录');arrow(d,(329,668),(397,668));badge(d,'自动处理',427,548,189,accent);badge(d,'任务处理',427,693,189)
  elif m=='records':doc(d,102,524,236,291,'订单关联');arrow(d,(361,669),(410,669));
  elif m=='member':avatar(d,166,661,.82,'user');doc(d,369,522,238,291,'会员比例设置');arrow(d,(264,670),(344,670))
  else:three(d,pts,accent)
  if m=='records':
   for k,t in enumerate(['待发放','已发放','失败']):badge(d,t,441,539+k*114,174,accent if k==1 else C['mint'])
 elif id=='jietiquanfan':
  if m in ['intro','pool']:
   doc(d,105,520,211,289,'资格订单');arrow(d,(339,669),(403,669));d.ellipse((431,563,615,747),fill=C['mint'],outline=C['ink'],width=4);center(d,'待解锁池',523,626,28,width=175);badge(d,'先确认活动与商品',177,846,365)
  elif m in ['seats','tiers']:
   center(d,'席位示意 · 数量按配置',360,496,27,width=570)
   for k,t in enumerate(['符合条件','占用席位','解锁记录']):
    x=154+k*207;rr(d,(x-78,585,x+78,798),accent if k==1 else C['mint'],26,C['ink']);center(d,t,x,661,25,width=143)
    if k<2:arrow(d,(x+84,690),(x+119,690))
  elif m=='refund':doc(d,109,526,227,285,'退款订单');arrow(d,(363,666),(416,666));badge(d,'席位调整',444,551,171);badge(d,'记录追回',444,693,171,accent)
  else:three(d,pts,accent)
 elif id=='core_wholesale':
  if m in ['intro','tiers','level']:
   for k,t in enumerate(['数量档位','阶梯单价','等级价格']):
    x=111+k*208;y=751-k*74;rr(d,(x,y-105,x+155,838),accent if k==1 else C['mint'],20,C['ink']);center(d,t,x+77,y-71,25,width=145)
   badge(d,'按配置取价，不展示虚构金额',124,489,472)
  elif m in ['sku','quantity']:
   for k,t in enumerate(['规格甲','规格乙']):rr(d,(108+k*300,525,306+k*300,689),accent if k==0 else C['mint'],20,C['ink']);center(d,t,207+k*300,578,28,width=181)
   arrow(d,(207,714),(333,800));arrow(d,(507,714),(387,800));badge(d,'同一商品数量合计',169,820,382)
  elif m=='purchase':doc(d,109,521,226,292,'选择规格数量');arrow(d,(359,665),(414,665));doc(d,448,550,170,237,'当前阶梯价')
  elif m=='coupon':ticket(d,110,558,220,151,'优惠券',accent);arrow(d,(357,659),(415,659));badge(d,'允许叠加？',445,554,172);badge(d,'独立开关',445,697,172)
  else:doc(d,105,521,231,292,'实际阶梯单价');arrow(d,(361,664),(416,664));doc(d,450,546,170,243,'订单快照')
 elif id=='core_register_jiedian':
  if m=='line':tree(d,'接点关系线下范围检查',True)
  elif m=='intro':
   avatar(d,163,653,.82,'user');arrow(d,(265,658),(343,658));badge(d,'推荐关系：邀请来源',364,551,268,accent);badge(d,'接点关系：安置关联',364,720,268)
  elif m in ['settings','conditions']:three(d,pts,accent)
  elif m in ['fill','resolve']:doc(d,111,525,219,283,'注册填写');arrow(d,(356,666),(413,666));doc(d,447,553,171,241,'目标会员')
  else:doc(d,104,521,231,292,'校验通过');arrow(d,(359,666),(414,666));doc(d,448,548,174,242,'关系记录')
 elif id=='core_userinfo_preview':
  if m in ['intro','styles']:
   for k,t in enumerate(['一','二','三','四']):
    x=124+(k%2)*274;y=507+(k//2)*180;rr(d,(x,y,x+196,y+135),accent if k==1 else C['mint'],18);d.ellipse((x+17,y+20,x+61,y+64),fill=C['cream']);line(d,[(x+79,y+32),(x+173,y+32)],C['ink'],4);line(d,[(x+25,y+95),(x+169,y+95)],C['ink'],4);center(d,'样式'+t,x+108,y+57,22,width=151)
   badge(d,'抽象布局示意',208,862,305)
  elif m in ['profile','details']:
   avatar(d,169,649,.78,'user');arrow(d,(259,658),(336,658))
   for k,t in enumerate(pts):badge(d,t,369,526+k*117,257,accent if k==1 else C['mint'])
  else:doc(d,108,526,224,280,'设计器预览');arrow(d,(357,668),(415,668));doc(d,450,547,168,242,'同配置核对');badge(d,'内容与布局逐项比较',168,846,385)
 else:raise ValueError((id,m))

def motion(d,cfg,c,u):
 # A moving connector packet expresses transfer/checking, never a simulated success notification.
 if c['visual'] in ['intro','close','tree','line','styles','fields','markets','ranking','seats','tiers','quantity','sku','profile','details']:return
 x=340+60*((u*.24)%1);y=668;d.ellipse((x-4,y-4,x+4,y+4),fill=cfg['accent'])
