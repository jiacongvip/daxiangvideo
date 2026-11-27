import sys,importlib.util,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from graphics import *
s=importlib.util.spec_from_file_location('b11',str(Path(__file__).resolve().parents[1]/'batch11'/'batch_art.py'));o=importlib.util.module_from_spec(s);s.loader.exec_module(o)
doc=o.doc;trio=o.trio;pair=o.pair;tags=o.tags;seal=o.seal

def art(d,cfg,c,u,index):
 i=cfg['id'];m=c['visual'];a=cfg['accent']
 if m=='close':return o.art(d,cfg,c,u,index)
 if i=='core_member_level_basics':
  if m in ['intro','identity']:
   avatar(d,150,651,.8,'merchant');arrow(d,(248,667),(324,667));doc(d,358,523,267,294,'会员等级');badge(d,'名称 / 图标 / 排序',130,851,459)
  elif m=='groups':trio(d,['选择分组','维护等级','切换分组'],a)
  elif m=='rights':pair(d,'等级有效期','等级与权益说明',a)
  else:o.o.poster(d,105,520,a);arrow(d,(355,666),(414,666));tags2=['上传背景图','更换展示素材','删除不用图片'];[(badge(d,t,426,531+k*130,201,a if k==1 else C['mint'])) for k,t in enumerate(tags2)]
 elif i=='core_refund_process':
  if m in ['intro','conditions']:trio(d,['订单阶段','进行中申请','可退款金额'],a)
  elif m=='items':
   for k in range(2):rr(d,(108+k*87,549,180+k*87,645),C['mint'],9,C['ink']);center(d,'商品',145+k*87,582,22,width=65)
   badge(d,'选择对应数量',109,730,246);arrow(d,(367,666),(419,666));doc(d,445,524,180,288,'核对退款金额')
  elif m=='paths':pair(d,'后台退款提交','用户退款申请',a);badge(d,'两条入口 · 处理步骤不同',130,851,460)
  elif m=='audit':
   doc(d,105,526,225,288,'退款申请详情');arrow(d,(356,666),(418,666));badge(d,'同意并退款',437,544,192,a);badge(d,'驳回申请',437,745,192)
  else:trio(d,['退款状态','关联退款单','操作记录'],a)
 elif i=='core_seckill_level_price':
  if m in ['intro','levels']:trio(d,['默认分类','会员等级','价格配置'],a)
  elif m=='switch':pair(d,'商品规格项目','开启会员价',a)
  elif m=='matrix':
   center(d,'规格 × 等级',360,525,30,width=500)
   for x,t in [(270,'等级甲'),(420,'等级乙')]:badge(d,t,x,589,135,a)
   for y,t in [(690,'规格甲'),(785,'规格乙')]:
    center(d,t,178,y,24,width=120)
    for x in [281,431]:rr(d,(x,y-5,x+110,y+51),C['mint'],12,C['ink']);center(d,'价格',x+55,y+3,22,width=100)
  else:trio(d,['切换价格开关','保留已填价格','提交并核对'],a)
 elif i=='core_cashier_audit':
  if m in ['intro','config']:tags(d,['作废与修改独立配置','确认码方式','管理员审核方式'],a)
  elif m=='submit':avatar(d,149,651,.8,'merchant');arrow(d,(246,666),(327,666));doc(d,360,524,264,289,'审核申请');badge(d,'收银员提交 · 记录原因与时间',113,851,493)
  elif m=='pending':doc(d,105,524,225,290,'待审核订单');arrow(d,(356,666),(418,666));seal(d,537,665,'等待审核',a);badge(d,'不重复提交 / 不继续修改作废',114,851,491)
  else:avatar(d,149,651,.8,'merchant');arrow(d,(246,666),(327,666));badge(d,'审核通过',388,541,236,a);badge(d,'审核驳回',388,741,236);badge(d,'审核备注与日志',167,851,386)
 elif i=='redpacket':
  if m in ['intro','activity']:pair(d,'会员活动设置','活动参与范围',a)
  elif m=='reward':pair(d,'显示金额','实际奖励数值',a);badge(d,'奖励类型与解锁条件单独配置',121,851,477)
  elif m=='unlock':trio(d,['等待天数','任务目标','解锁进度'],a)
  elif m=='checkin':o.o.o.grid(d,106,536,'会员打卡记录',a);arrow(d,(365,666),(414,666));seal(d,539,666,'任务进度',a)
  elif m=='claim':trio(d,['查看解锁状态','领取红包奖励','我的奖励记录'],a)
  else:trio(d,['活动统计','用户参与记录','领取发放日志'],a)
 elif i=='memberredpacket':
  if m in ['intro','budget']:trio(d,['活动预算数量','平分或拼手气','金额范围'],a)
  elif m=='limits':trio(d,['可参与等级','等级金额上限','等级次数上限'],a)
  elif m=='time':pair(d,'固定日期范围','每日活动时间',a);badge(d,'每日模式刷新领取次数',143,851,434)
  elif m=='source':trio(d,['固定或订单比例','选择计算口径','运行补充任务'],a)
  elif m=='claim':avatar(d,148,649,.8,'user');arrow(d,(245,666),(325,666));doc(d,360,526,263,287,'条件检查与余额记录')
  else:pair(d,'会员领取明细','活动展示开关',a)
 else:raise ValueError(i)
def motion(d,cfg,c,u):
 if c['visual']=='close':return
 a=cfg['accent'];x=352+59*((u*.28)%1)
 if c['visual'] not in ['matrix','groups','conditions','config','intro','records']:d.ellipse((x-4,663,x+4,671),fill=a)
 else:d.ellipse((90,869,98,877),fill=a if math.sin(u*1.6)>0 else C['mint'])
