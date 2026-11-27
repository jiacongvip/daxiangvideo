import sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
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
def art(d,cfg,c,u,index):
 ident=cfg['id'];m=c['visual']
 if m=='close':
  for k,t in enumerate(cfg['phases']):
   x,y=[(150,550),(570,550),(570,780),(150,780)][k];d.ellipse((x-51,y-51,x+51,y+51),fill=C['orange'] if k%2 else C['mint']);center(d,str(k+1),x,y-25,35);center(d,t,x,y+74,27,width=215)
  arrow(d,(224,550),(494,550));arrow(d,(570,612),(570,715));arrow(d,(494,780),(224,780));return
 if ident=='aizhenliao':
  if m in ['intro','capture']:
   for k,t in enumerate(['面部','舌部','舌下']):camera(d,150+k*210,626,t)
   arrow(d,(225,628),(277,628));arrow(d,(437,628),(489,628));badge(d,'同一次采集记录',195,832,330)
  elif m=='customer':avatar(d,148,658,.92,'user');doc(d,315,492,286,324,'客户资料');badge(d,'年龄 / 身高 / 体重',334,645,250);badge(d,'手机号',334,717,250)
  elif m=='settings':camera(d,198,603,'默认摄像头');pillstack(d,['前置 / 后置','临时检测入口'],x=348,y=557,w=280);badge(d,'后台配置 → 采集流程',161,836,398)
  elif m=='history':
   avatar(d,132,650,.85,'user');line(d,[(307,527),(307,843)],C['ink'],5)
   for k,t in enumerate(['本次采集','检测历史','记录详情']):
    y=531+k*133;d.ellipse((295,y-9,319,y+15),fill=C['orange']);badge(d,t,360,y-15,240)
  elif m=='records':flow3(d,['舌部','面部','综合'],kind='doc');badge(d,'分类型查看与导出',183,838,354)
  elif m=='reports':doc(d,108,500,230,312,'报告');arrow(d,(364,648),(419,648));pillstack(d,['详情 / 表格','JSON汇总','软删除'],435,518,200)
  elif m=='recommend':folder(d,111,550,202,203,'内容分类');arrow(d,(335,649),(391,649));doc(d,431,510,185,282,'推荐内容');badge(d,'保存 · 排序 · 删除',184,843,352)
  else:
   line(d,[(130,818),(130,511),(601,511)],C['ink'],4)
   for k,h in enumerate([100,175,130,245]):x=184+k*100;rr(d,(x,818-h,x+61,818),C['orange'] if k==3 else C['mint'],10)
   badge(d,'类型 / 趋势 / 明细',173,858,374)
 elif ident=='aliyun-ocr':
  if m in ['intro','upload']:
   doc(d,112,509,215,300,'图片');d.rectangle((145,646,294,730),fill=C['mint']);d.polygon([(148,727),(207,668),(253,727)],fill=C['orange']);arrow(d,(352,659),(407,659));doc(d,443,509,183,300,'文字')
  elif m=='settings':avatar(d,132,650,.88,'merchant');pillstack(d,['服务连接','默认识别类型','每日调用额度'],300,510,318)
  elif m=='types':flow3(d,['文字','证照','表格'],kind='doc');badge(d,'按图片材料选择类型',164,838,392)
  elif m=='invoices':
   for k,t in enumerate(['发票','车票','行程单']):ticket(d,105+k*175,520+k*83,161,150,t)
   badge(d,'票据细分类型',224,854,272)
  elif m=='result':doc(d,100,515,203,290,'原图');arrow(d,(331,655),(391,655));pillstack(d,['结构化字段','识别文本','原始返回'],416,521,210)
  else:doc(d,112,504,287,322,'识别记录');d.ellipse((444,581,553,690),outline=C['orange'],width=10);line(d,[(542,678),(589,727)],C['orange'],10);badge(d,'类型 / 状态 / 时间',171,851,378)
 elif ident=='allianceactivity':
  if m in ['intro','merchants']:
   for k,t in enumerate(['商家','商家','商家']):shop(d,150+k*210,569,.85,t)
   for x in [150,360,570]:arrow(d,(x,690),(360,777))
   badge(d,'联盟活动 / 阶梯拼团',162,807,396)
  elif m=='selection':
   for k,t in enumerate(['机构','课程','校区']):
    x=150+k*210;folder(d,x-74,555+k*42,148,149,t)
    if k<2:arrow(d,(x+84,649+k*42),(x+126,649+(k+1)*42))
   badge(d,'选择内容 → 报名与订单',154,847,412)
  elif m=='group':
   for k,t in enumerate(['开团','参团','单买']):avatar(d,150+k*210,640,.63,'user');center(d,t,150+k*210,786,29,width=160)
   badge(d,'购买入口跟随活动开关',152,487,416)
  elif m=='eligibility':doc(d,103,535,212,263,'老客户');doc(d,410,535,212,263,'团员资格');badge(d,'名单识别 / 开团限制',146,852,428)
  elif m=='rules':clock(d,185,651,1.5);pillstack(d,['购买上限','结束时自动成团'],350,548,270);badge(d,'各自独立配置',212,844,296)
  elif m=='share':doc(d,110,497,252,326,'活动海报');arrow(d,(392,662),(442,662));bubble(d,460,554,'分享',160);bubble(d,460,698,'链接',160,C['orange'])
  elif m=='records':flow3(d,['报名','订单','拼团'],kind='doc');badge(d,'有真实记录，再展示',168,839,384)
  elif m=='attribution':
   for k,t in enumerate(['分享落点','浏览绑定','订单归属','佣金记录']):
    x=115+(k%2)*340;y=530+(k//2)*232;badge(d,t,x,y,182)
   arrow(d,(309,554),(445,554));arrow(d,(546,602),(546,741));arrow(d,(445,787),(309,787))
  else:gift(d,166,636,.85,'抽奖配置');doc(d,317,528,155,235,'排行');doc(d,503,528,138,235,'结算');badge(d,'开关 / 规则 / 管理记录',141,851,438)
 elif ident=='apppush':
  if m in ['intro','offline']:
   bubble(d,93,539,'新消息',174);arrow(d,(289,579),(354,579));rr(d,(374,506,622,660),C['mint'],35);center(d,'推送队列',498,550,30,width=224);arrow(d,(495,685),(495,733));phone(d,421,748,148,147,'通知')
  elif m=='settings':avatar(d,148,650,.9,'merchant');phone(d,411,527,166,288,'打包App');badge(d,'授权 · 接入 · 通知设置',156,853,408)
  elif m=='bind':avatar(d,155,650,.94,'user');phone(d,465,521,154,288,'设备');arrow(d,(248,617),(429,617));arrow(d,(429,714),(248,714));center(d,'登录绑定 / 退出解绑',360,842,28,width=520)
  elif m=='online':avatar(d,143,645,.83,'user');avatar(d,565,645,.83,'user');line(d,[(227,644),(478,644)],C['orange'],8);bubble(d,277,503,'长连接',174);badge(d,'前台提醒 / 本地通知',157,846,406)
  elif m=='dedupe':bubble(d,101,503,'在线消息',211);bubble(d,101,721,'推送消息',211);arrow(d,(330,550),(468,659));arrow(d,(330,760),(468,659));phone(d,495,540,136,244,'一次提醒')
  else:phone(d,106,518,164,296,'通知');arrow(d,(303,659),(364,659));pillstack(d,['私聊','群聊','企聊'],406,516,206)
 elif ident=='birthday':
  if m in ['intro','calendar']:
   rr(d,(107,521,365,814),C['white'],24,C['ink']);rr(d,(107,521,365,587),C['orange'],19);center(d,'生日窗口',237,614,32,width=228)
   for k in range(6):d.ellipse((146+(k%3)*65,695+(k//3)*51,164+(k%3)*65,713+(k//3)*51),fill=C['mint'])
   gift(d,527,675,1.0,'可领礼物')
  elif m=='gifts':
   for k,t in enumerate(['优惠券','余额','储值券']):gift(d,150+k*210,666,.78,t)
   badge(d,'全体会员 / 指定等级',167,489,386)
  elif m=='claim':avatar(d,145,649,.85,'user');arrow(d,(249,666),(315,666));gift(d,449,644,1.25,'全部 / 逐项领取');badge(d,'每种礼物，每年一次',168,851,384)
  elif m=='automation':clock(d,157,656,1.18);arrow(d,(237,656),(293,656));gift(d,363,666,.72,'发放');arrow(d,(429,656),(489,656));bubble(d,507,598,'到账通知',134)
  elif m=='manual':avatar(d,145,652,.84,'merchant');doc(d,304,508,278,300,'未领完会员');badge(d,'先预览，再勾选',302,841,310)
  elif m=='records':doc(d,105,510,242,310,'领取记录');pillstack(d,['会员','礼物类型','年份'],406,531,210)
  else:flow3(d,['链接','页面','会员']);gift(d,359,797,.57,'生日入口')
 elif ident=='brainsleep':
  if m in ['intro','scene']:
   for k,t in enumerate(['睡眠','情绪','自定义']):folder(d,95+k*210,546,160,184,t)
   badge(d,'按场景组织音频内容',167,828,386)
  elif m=='library':folder(d,101,535,221,219,'音频分类');arrow(d,(346,666),(402,666));disc(d,522,661,.83);badge(d,'分类与音频归属场景',165,843,390)
  elif m=='entry':folder(d,101,555,192,186,'场景');arrow(d,(323,661),(388,661));phone(d,431,519,167,292,'独立入口');badge(d,'复制入口 / 链接中心',154,849,412)
  elif m=='play':disc(d,267,649,1.19);d.polygon([(477,574),(477,725),(596,649)],fill=C['orange']);line(d,[(142,828),(580,828)],C['mint'],6)
  elif m=='favorites':disc(d,185,630,.8);d.polygon([(499,519),(522,577),(584,583),(538,625),(551,689),(499,657),(447,689),(460,625),(414,583),(476,577)],fill=C['orange']);clock(d,500,798,.7);center(d,'收藏',185,787,30);center(d,'历史',500,858,27)
  elif m=='logs':doc(d,119,495,293,325,'播放记录');disc(d,542,665,.65);badge(d,'按场景查询',231,846,258)
  else:folder(d,111,562,192,182,'场景');arrow(d,(326,658),(393,658));doc(d,433,516,178,281,'关联内容');badge(d,'有关联内容，不直接删',141,845,438)
 elif ident=='carouselpay':
  if m in ['intro','route']:
   doc(d,101,548,167,227,'订单');arrow(d,(293,659),(344,659))
   for k,t in enumerate(['通道A','通道B','通道C']):
    y=514+k*124;badge(d,t,423,y,195,C['orange'] if k==1 else C['mint']);line(d,[(367,659),(407,y+26)],C['ink'],3)
  elif m=='settings':avatar(d,139,653,.84,'merchant');pillstack(d,['站点授权','易支付通道','接管开关'],302,522,315)
  elif m=='reuse':doc(d,105,529,214,275,'同一订单');arrow(d,(346,651),(404,651));badge(d,'原通道',432,623,188);d.arc((342,521,648,833),45,320,fill=C['orange'],width=8);badge(d,'未支付再发起 → 复用',139,854,442)
  else:doc(d,112,529,210,275,'支付结果');arrow(d,(351,654),(407,654));doc(d,448,529,168,275,'路由记录');check(d,532,727)
 elif ident=='core_relation':
  if m in ['intro','tree','depth']:tree(d,3 if m!='tree' else 2)
  elif m=='entry':avatar(d,141,658,.87,'merchant');doc(d,318,505,274,313,'目标会员');badge(d,'会员列表 → 关系图',171,852,378)
  elif m=='node':avatar(d,163,655,.94,'user');pillstack(d,['昵称 / ID','会员等级','直接下级数量'],317,521,294)
  elif m=='counts':tree(d,2);badge(d,'节点下级数 ≠ 展示层数',139,853,442)
  else:tree(d,2);badge(d,'加载提示 / 空状态',176,851,368)
 elif ident=='core_member_tags':
  if m in ['intro','upgrade']:
   badge(d,'基础标签',101,585,213);arrow(d,(338,609),(391,609));badge(d,'进阶标签',415,585,213,C['orange']);clock(d,360,789,.68)
  elif m=='conditions':avatar(d,138,650,.83,'merchant');pillstack(d,['统计区间','标签条件','适用会员'],310,520,304)
  elif m in ['timing','hold']:
   clock(d,197,648,1.45);pillstack(d,['保持当前标签','升级所需天数'],363,553,261);badge(d,'两种时间，分别配置',148,847,424)
  elif m=='downgrade':badge(d,'当前标签',103,572,215,C['orange']);badge(d,'目标标签',414,728,215);arrow(d,(324,599),(417,745));clock(d,538,564,.72);center(d,'新的保持期',228,831,27,width=290)
  elif m=='cleanup':doc(d,106,522,234,289,'已分配标签');arrow(d,(366,658),(418,658));pillstack(d,['符合：保持','期内：保留','超期：处理'],445,527,190)
  else:doc(d,114,518,255,299,'标签变化记录');pillstack(d,['升级','降级','重新计时'],425,526,194)
 elif ident=='core_member_data':
  if m in ['intro','template','fields']:
   doc(d,109,510,240,306,'CSV模板');arrow(d,(377,665),(431,665));pillstack(d,['身份资料','金额与积分','备注'],453,533,179)
  elif m=='validate':doc(d,107,515,238,294,'待导入资料');check(d,485,579);check(d,485,681);center(d,'必填 / 重复检查',489,791,25,width=248)
  elif m=='import':folder(d,105,548,199,200,'导入文件');arrow(d,(328,661),(393,661));pillstack(d,['成功数量','失败数量','错误原因'],415,535,207)
  elif m=='refresh':avatar(d,139,651,.88,'merchant');doc(d,327,505,259,313,'会员列表');d.arc((266,526,646,854),210,520,fill=C['orange'],width=8)
  else:doc(d,109,515,231,299,'筛选会员');arrow(d,(366,661),(418,661));doc(d,448,515,174,299,'导出资料');badge(d,'单次最多一千条',188,856,344)
