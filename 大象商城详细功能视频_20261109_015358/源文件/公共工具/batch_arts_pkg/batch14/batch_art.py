import sys,importlib.util
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from graphics import *
s=importlib.util.spec_from_file_location('oldart',str(Path(__file__).resolve().parents[1]/'batch13'/'batch_art.py'));o=importlib.util.module_from_spec(s);s.loader.exec_module(o)
trio=o.trio;pair=o.pair;tags=o.tags;sheet=o.sheet

def art(d,cfg,c,u,index):
 i=cfg['id'];m=c['visual'];a=cfg['accent']
 if m=='close':return o.o.art(d,cfg,c,u,index)
 if i=='core_deposit_admin':
  if m in ['intro','record']:sheet(d,105,524,'会员押金记录',a);arrow(d,(356,666),(419,666));sheet(d,438,524,'金额与业务状态',a)
  elif m=='lookup':trio(d,['押金总额','已释放金额','剩余与进度'],a)
  elif m=='logs':pair(d,'管理端释放日志','会员端金额记录',a)
  else:tags(d,['标题、副标题与标签','已释放、剩余显示开关','主题颜色与说明'],a)
 elif i=='core_article_content':
  if m in ['intro','list']:pair(d,'我的团列表','我的文章列表',a);badge(d,'切换内容类型 → 选择目标文章',120,851,480)
  elif m=='edit':sheet(d,105,524,'标题与简介',a);arrow(d,(356,666),(419,666));sheet(d,438,524,'文章正文',a)
  else:
   rr(d,(105,565,335,685),a,18,C['ink']);center(d,'保存草稿',220,604,28,width=220);rr(d,(385,565,615,685),C['mint'],18,C['ink']);center(d,'立即发布',500,604,28,width=220);badge(d,'发布状态二选一',170,744,380);badge(d,'已有文章 → 编辑后再次保存',115,851,490)
 elif i=='core_design_group_preview':
  if m in ['intro','scope']:trio(d,['分组分类来源','选择目标范围','预览对应商品'],a)
  elif m=='limit':pair(d,'显示数量配置','已上架商品来源',a);badge(d,'默认10个 · 最多100个',141,851,438)
  else:sheet(d,105,524,'调整来源和数量',a);arrow(d,(356,666),(419,666));sheet(d,438,524,'商品预览更新',a)
 elif i=='core_learning_navigation':
  if m in ['intro','open']:sheet(d,105,524,'后台使用说明',a);arrow(d,(356,666),(419,666));sheet(d,438,524,'分类项目导航',a)
  elif m=='progress':tags(d,['分类已完成 / 总数','具体项目标题','已完成或未完成'],a)
  else:trio(d,['选择导航项目','关闭抽屉定位','目标短暂高亮'],a)
 elif i=='core_fenhongdian_mode':
  if m in ['intro','setting']:trio(d,['基础设置','达标点参与选项','确认当前模式'],a)
  elif m=='compare':pair(d,'参与：总点数','不参与：未达标点数',a)
  else:sheet(d,105,524,'当前模式预览',a);arrow(d,(356,666),(419,666));sheet(d,438,524,'原有历史记录',a);badge(d,'新口径影响后续 · 历史记录不重写',99,851,522)
 elif i=='core_hualuo_threshold':
  if m in ['intro','setting']:trio(d,['阈值相关模式','填写阈值金额','选择计算类型'],a)
  elif m=='compare':tags(d,['流水：实际成交金额','利润：成交减商品成本','先核对成本价与数量'],a)
  else:pair(d,'旧配置默认流水','日志回看计算模式',a)
 elif i=='core_zhoufenhong_filter':
  if m in ['intro','member']:pair(d,'参与等级','指定会员优先',a);badge(d,'同时设置 → 按指定会员',133,851,454)
  elif m=='product':pair(d,'商品分类','指定商品优先',a);badge(d,'同时设置 → 按指定商品',133,851,454)
  else:sheet(d,105,524,'含匹配商品订单',a);arrow(d,(356,666),(419,666));sheet(d,438,524,'订单数量计入',a);badge(d,'命中商品 → 整单计入统计',128,851,464)
 else:raise AssertionError(i)

motion=o.motion
