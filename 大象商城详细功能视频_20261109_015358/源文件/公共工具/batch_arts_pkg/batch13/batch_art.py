import sys,importlib.util,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from graphics import *
s=importlib.util.spec_from_file_location('b12',str(Path(__file__).resolve().parents[1]/'batch12'/'batch_art.py'));o=importlib.util.module_from_spec(s);s.loader.exec_module(o)
doc=o.doc;trio=o.trio;pair=o.pair;tags=o.tags;seal=o.seal

def clock(d,x,y,a):
 d.ellipse((x-87,y-87,x+87,y+87),outline=C['ink'],width=4);line(d,[(x,y-55),(x,y),(x+47,y+26)],a,6);center(d,'文章停留时间',x,y+110,25,width=250)
def sheet(d,x,y,title,a):
 doc(d,x,y,227,286,title);line(d,[(x+28,y+99),(x+193,y+99)],a,3)
def art(d,cfg,c,u,index):
 i=cfg['id'];m=c['visual'];a=cfg['accent']
 if m=='close':return o.art(d,cfg,c,u,index)
 if i=='core_product_copy':
  if m in ['intro','draft']:sheet(d,105,524,'原商品',a);arrow(d,(356,666),(419,666));sheet(d,438,524,'复制的新商品',a);badge(d,'新记录初始为下架',151,851,420)
  elif m=='scope':pair(d,'平台商品范围','商户自己的商品',a)
  else:trio(d,['编辑新商品','保存与验证','核对上下架'],a)
 elif i=='core_seckill_detail_designer':
  if m in ['intro','workspace']:trio(d,['组件选择','预览中选中','修改属性'],a)
  elif m=='content':tags(d,['标题 / 多行文本','图片 / 按钮链接','富文本内容'],a)
  elif m=='media':trio(d,['多图轮播','视频与封面','分类分组商品'],a)
  elif m=='arrange':sheet(d,104,524,'当前内容组件',a);arrow(d,(356,666),(419,666));badge(d,'向上 / 向下',437,535,190,a);badge(d,'图库 / 链接',437,665,190);badge(d,'删除组件',437,795,190,a)
  else:trio(d,['保存设计内容','提交商品表单','回看配置'],a)
 elif i=='core_article_trace':
  if m in ['intro','timer']:sheet(d,105,524,'家居选购文章',a);arrow(d,(356,666),(419,666));clock(d,539,659,a);badge(d,'隐藏或关闭保存 · 少于1秒不保存',99,865,522)
  elif m=='records':tags(d,['文章与访问用户','本次停留时长','本次访问时间'],a)
  else:trio(d,['总访问量','访问用户数','平均时长'],a);badge(d,'汇总统计 → 详细访问记录',129,851,461)
 elif i=='core_score_records':
  if m in ['intro','fields']:pair(d,'这次变更积分','记录变更后积分',a);badge(d,'类型 / 渠道 / 时间 / 备注',124,851,472)
  elif m=='filter':trio(d,['会员与昵称','开始结束时间','普通或允提'],a)
  elif m=='export':sheet(d,105,524,'分页记录',a);arrow(d,(356,666),(419,666));sheet(d,438,524,'导出整理',a)
  else:pair(d,'单条二次确认','勾选批量删除',a);badge(d,'明细删除 ≠ 撤销积分变更',130,851,461)
 elif i=='core_consume_project_search':
  if m in ['intro','keyword']:
   sheet(d,105,524,'支付项目名称',a);d.ellipse((456,573,578,695),outline=C['ink'],width=5);line(d,[(560,678),(612,732)],a,10);badge(d,'部分匹配 · 保留查询词',142,851,435)
  else:trio(d,['支付项目标题','会员ID或昵称','支付方式'],a);badge(d,'多条件共同生效 · 保留排序分页',112,851,497)
 elif i=='core_menu_layout':
  if m in ['intro','layout']:
   for y in [554,674]:
    for x in [125,305,485]:rr(d,(x,y,x+108,y+75),a,15,C['ink']);center(d,'入口',x+54,y+17,24,width=100)
   badge(d,'每行数量 / 每页数量 / 横向滚动',108,851,504)
  elif m=='icons':
   for k,rad in enumerate([3,25,50]):rr(d,(115+k*185,580,215+k*185,680),a,rad,C['ink'])
   badge(d,'图标开关、大小与圆角',141,851,438)
  elif m=='text':tags(d,['标题显示、内容、字号颜色','按钮文字字号与行高','组件背景颜色'],a)
  else:
   center(d,'入口甲',177,631,28,width=160);center(d,'入口乙',360,631,28,width=160);center(d,'入口丙',543,631,28,width=160);line(d,[(268,612),(268,694)],a,4);line(d,[(452,612),(452,694)],a,4);badge(d,'无图标时配置分隔竖线',140,851,439)
 elif i=='core_giftcode_freeze':
  if m in ['intro','list']:trio(d,['全部兑换码','正常状态','已冻结状态'],a)
  elif m=='freeze':sheet(d,105,524,'选择目标兑换码',a);arrow(d,(356,666),(419,666));sheet(d,438,524,'填写冻结原因',a)
  elif m=='block':sheet(d,105,524,'已冻结兑换码',a);arrow(d,(356,666),(419,666));seal(d,539,666,'无法兑换',a)
  else:trio(d,['选择已冻结码','确认解冻','已用码不操作'],a)
 elif i=='core_exam_records':
  if m in ['intro','filter']:trio(d,['课程与昵称','答题时间范围','组合查询重置'],a)
  elif m=='status':pair(d,'是否已经答完','是否已经合格',a);badge(d,'完成状态 ≠ 合格结果',145,851,431)
  elif m=='export':sheet(d,105,524,'当前查询结果',a);arrow(d,(356,666),(419,666));sheet(d,438,524,'CSV表格记录',a);badge(d,'默认最多5000条 · 先核对范围',116,851,489)
  else:tags(d,['课程、用户与分数','答题起止时间与状态','所属商户'],a)
 elif i=='core_queue_display':
  if m in ['intro','style']:
   for x,y,t in [(107,535,'助力次数'),(379,535,'总消费'),(107,709,'已补贴'),(379,709,'补贴中')]:rr(d,(x,y,x+234,y+115),a if y<600 else C['mint'],19,C['ink']);center(d,t,x+117,y+36,26,width=220)
  elif m=='link':trio(d,['按钮文字','内部外部链接','平台与显示范围'],a)
  else:pair(d,'登录会员记录','未登录默认零值',a);badge(d,'页面加载或重新进入更新',134,851,452)
 elif i=='core_order_member_list':
  if m in ['intro','states']:trio(d,['待付款与待发货','待收货与已完成','全部订单回看'],a)
  elif m=='search':sheet(d,105,524,'提交查询关键词',a);arrow(d,(356,666),(419,666));sheet(d,438,524,'返回匹配记录',a);badge(d,'加载占位 → 搜索结果',144,851,432)
  else:trio(d,['下拉刷新','加载反馈','列表或暂无订单'],a)
 elif i=='core_contribution_level':
  if m in ['intro','configure']:trio(d,['确认功能开关','选择适用等级','维护参数保存'],a)
  elif m=='selection':tags(d,['全选：全部等级受限','部分选：只限制所选等级','全不选：关闭这项扣减'],a)
  else:trio(d,['配置保存更新','等级范围判断','扣减执行日志'],a)
 else:raise ValueError(i)
def motion(d,cfg,c,u):
 if c['visual']=='close':return
 a=cfg['accent']
 if cfg['id']=='core_article_trace' and c['visual'] in ['intro','timer']:
  x,y=539,659;ang=u*.18;line(d,[(x,y),(x+64*math.cos(ang),y+64*math.sin(ang))],a,3)
 else:d.ellipse((87,866,97,876),fill=a if math.sin(u*1.6)>0 else C['mint'])
