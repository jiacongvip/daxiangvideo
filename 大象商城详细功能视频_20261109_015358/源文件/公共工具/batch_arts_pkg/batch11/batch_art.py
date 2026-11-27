import sys,math,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from graphics import *
spec=importlib.util.spec_from_file_location('b10',str(Path(__file__).resolve().parents[1]/'batch10'/'batch_art.py'));o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)
doc=o.doc;trio=o.trio;tags=o.tags;seal=o.seal;pair=o.pair

def art(d,cfg,c,u,index):
 i=cfg['id'];m=c['visual'];a=cfg['accent']
 if m=='close':return o.o.old.art(d,cfg,c,u,index)
 if i=='yuejie':
  if m in ['intro','users']:avatar(d,148,652,.81,'user');arrow(d,(246,666),(326,666));doc(d,362,525,258,287,'月结会员资格');badge(d,'用户类型 / 设为或取消月结',125,851,471)
  elif m=='credit':trio(d,['用户类型','信用额度','当前欠费'],a)
  elif m=='adjust':doc(d,105,528,223,287,'欠费调整');arrow(d,(353,666),(414,666));seal(d,535,665,'额度校验',a)
  elif m=='orders':pair(d,'月结消费订单','待发货数量',a)
  else:pair(d,'欠费变化明细','查询与导出',a);badge(d,'账面调整 ≠ 收到真实付款',131,851,458)
 elif i=='yuyue':
  if m in ['intro','product']:o.o.old.old.shop(d,101,550,'清洁服务项目');arrow(d,(342,667),(414,667));o.o.grid(d,421,541,'预约项目',a)
  elif m=='category':trio(d,['二级服务类型','人员类型','具体服务人员'],a)
  elif m=='calendar':o.o.grid(d,107,536,'周期与时间点',a);arrow(d,(365,667),(414,667));avatar(d,548,650,.8,'merchant');badge(d,'人员排班与项目时间对应',139,851,443)
  elif m=='traditional':trio(d,['选择项目','时间和人员','下单付款'],a);badge(d,'传统模式：先安排，再付款',127,851,467)
  elif m=='newmode':trio(d,['项目付款','选择时间','选择或分配人'],a);badge(d,'新模式：先付款，再安排',137,851,447)
  elif m=='dispatch':doc(d,105,525,223,290,'当前服务订单');arrow(d,(353,668),(414,668));avatar(d,549,650,.8,'merchant');badge(d,'分配 / 改派 / 当前模式',143,851,435)
  elif m=='verify':o.o.old.ticket(d,106,549,219,222,'服务核销码');arrow(d,(353,667),(414,667));seal(d,536,665,'核销',a);badge(d,'尾款 / 退款 / 导出分别管理',120,851,481)
  elif m=='package':
   for k in range(3):doc(d,107+k*20,529+k*55,219,176,'组合服务' if k==2 else '')
   arrow(d,(389,666),(426,666));seal(d,545,665,'使用次数',a)
  else:trio(d,['商品及人评价','不同商品提成','发放时机'],a)
 elif i=='zhuibaoagent':
  if m in ['intro','codes']:doc(d,104,527,223,288,'单任务码');arrow(d,(353,666),(414,666));doc(d,449,541,175,264,'任务组码');badge(d,'任务先入组，才能从组拉取',132,851,457)
  elif m=='types':
   rr(d,(104,545,325,788),C['mint'],19,C['ink']);center(d,'图文图片',215,583,26,width=200);d.rectangle((145,650,287,750),outline=C['ink'],width=3);arrow(d,(355,665),(413,665));rr(d,(444,545,628,788),a,19,C['ink']);d.polygon([(506,638),(506,706),(557,672)],fill=C['cream']);center(d,'视频',535,731,25)
  elif m=='status':tags(d,['任务状态与当前步骤','进度和缺项说明','素材就绪标识'],a)
  elif m=='images':
   for k in range(3):o.poster(d,107+k*21,520+k*34,a)
   arrow(d,(395,669),(440,669));badge(d,'按页顺序',441,574,185,a);badge(d,'核对缺页',441,724,185)
  elif m=='platform':pair(d,'平台专属内容','标题正文话题',a);badge(d,'小红书 / 抖音 / 默认内容',133,851,455)
  elif m=='cursor':trio(d,['首次空游标','获取新游标','下次增量拉取'],a)
  else:tags(d,['素材就绪且有图片','标题或正文非空','需要时仅收全部完成'],a)
 elif i=='zichanfenqi':
  if m in ['intro','activity']:pair(d,'活动来源账户','独立分期计划',a);badge(d,'记账与额度规则 · 非投资回报',119,851,483)
  elif m=='convert':trio(d,['来源可用量','单次限制','今日剩余额度'],a);badge(d,'只处理约束内的实际数量',139,851,442)
  elif m=='priority':tags(d,['先看活动排序','同排序再看活动编号','先处理先占用额度'],a)
  elif m=='plan':
   doc(d,104,526,224,287,'分期计划');arrow(d,(353,666),(414,666))
   for k,t in enumerate(['待发期次','到期处理','发放日志']):badge(d,t,443,531+k*130,180,a if k==1 else C['mint'])
  elif m=='groups':tags(d,['中文分组与默认额度','关联活动及历史记录','默认值与当日快照分开'],a)
  elif m=='members':trio(d,['分组默认','个人额度','当日有效值'],a);badge(d,'已使用 / 剩余 / 来源余额',138,851,444)
  elif m=='adjust':pair(d,'长期个人额度','指定日期额度',a);badge(d,'填写备注 · 修改不立即转化',129,851,462)
  else:trio(d,['额度明细','转化及发放','奖励日志'],a)
 elif i=='activity':
  if m in ['intro','publish']:
   avatar(d,148,649,.8,'merchant');arrow(d,(246,666),(327,666));o.o.grid(d,375,533,'手作体验活动',a);badge(d,'演示案例：周末手作体验',145,851,431)
  elif m=='rules':tags(d,['每人限报与活动名额','报名时间范围','单活动位置范围'],a)
  elif m=='form':pair(d,'自定义报名字段','规格价格库存',a);badge(d,'填写信息与选择规格分开',137,851,447)
  elif m=='signup':avatar(d,148,650,.8,'user');arrow(d,(246,666),(327,666));doc(d,362,524,258,291,'手作体验报名单')
  elif m=='payment':trio(d,['积分支付','现金积分混合','优惠及奖励'],a)
  elif m=='orders':pair(d,'报名订单详情','搜索筛选导出',a)
  elif m=='verify':o.o.old.ticket(d,106,550,220,222,'活动核销码');arrow(d,(353,666),(414,666));seal(d,537,666,'现场核销',a)
  elif m=='poster':o.poster(d,107,524,a);arrow(d,(355,666),(414,666));tags2=['活动分类','元素拖拽缩放','图层及预览']
  else:trio(d,['会员发布','审核与待审上限','待付自动关闭'],a)
  if m=='poster':
   for k,t in enumerate(tags2):badge(d,t,426,530+k*132,207,a if k==1 else C['mint'])
 else:raise ValueError(i)
def motion(d,cfg,c,u):
 i=cfg['id'];m=c['visual'];a=cfg['accent']
 if m=='close':return
 if i=='zhuibaoagent' and m=='images':
  y=602+90*((u*.2)%1);line(d,[(170,y),(338,y)],a,3)
 elif i=='zichanfenqi' and m in ['intro','convert','plan']:
  x=356+55*((u*.3)%1);d.ellipse((x-5,662,x+5,672),fill=a)
 elif i in ['activity','yuyue'] and m in ['intro','publish','calendar']:
  x=401+49*(int(u*.7)%4);d.ellipse((x-4,829,x+4,837),fill=a)
 else:d.ellipse((88,866,98,876),fill=a if math.sin(u*1.7)>0 else C['mint'])
