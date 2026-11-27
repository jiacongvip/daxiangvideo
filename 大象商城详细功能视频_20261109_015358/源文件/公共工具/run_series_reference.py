from pathlib import Path
import sys,json,asyncio,subprocess,wave,math,hashlib,csv,re,os
import numpy as np
from PIL import Image,ImageDraw
from graphics import *
ROOT=Path(__file__).parent
PHASES={'address':['录入','识别','默认','收寄'],'agentrecharge':['申请','签约','充值','升级'],'aiapi':['授权','商品','订单','运营'],'aidatasource':['设置','任务','内容','评论'],'aidrama':['剧本','资产','分镜','运营'],'aiscene':['场景库','绑商品','对话','分享'],'aitouchshare':['到店','素材','发布','回流']}
PALETTES={'address':'#F0AA79','agentrecharge':'#E8B76B','aiapi':'#9CBBD7','aidatasource':'#B1C59A','aidrama':'#DDA7A1','aiscene':'#B6B0D5','aitouchshare':'#E7BC83'}
def mark_status(id,status,**kw):
 p=ROOT/'progress.json';x=json.loads(p.read_text())
 for r in x['plugins']:
  if r['id']==id:
   prior=r.get('delivery_status');old_sha=r.get('sha256');new_sha=kw.get('sha256',old_sha)
   resolved='delivered_sha256_verified' if prior=='delivered_sha256_verified' and status=='rendered_technical_qa_passed' and new_sha==old_sha else status
   if prior=='delivered_sha256_verified' and old_sha and new_sha!=old_sha:r['delivery_status']='superseded_needs_new_filename'
   r.update(status=resolved,**kw)
 tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2));tmp.replace(p)
def run(cmd,**kw):return subprocess.run(cmd,check=True,**kw)
def tc(t):
 n=round(t*1000);h,n=divmod(n,3600000);m,n=divmod(n,60000);s,ms=divmod(n,1000);return f'{h:02}:{m:02}:{s:02},{ms:03}'
def srt(arr,p):p.write_text('\n\n'.join(f"{i}\n{tc(v['start'])} --> {tc(v['end'])}\n{v['text']}" for i,v in enumerate(arr,1))+'\n')
async def speech(p,cfg):
 import edge_tts
 a=p/'audio';a.mkdir(exist_ok=True)
 for i,c in enumerate(cfg['chapters']):
  mp=a/f'{i:02}.mp3';js=a/f'{i:02}.jsonl';sig=a/f'{i:02}.sha256';digest=hashlib.sha256(c['narration'].encode()).hexdigest()
  if not (mp.exists() and js.exists() and sig.exists() and sig.read_text()==digest):
   for attempt in range(3):
    try:
     await edge_tts.Communicate(c['narration'],'zh-CN-XiaoxiaoNeural',rate='+8%').save(str(mp),str(js));sig.write_text(digest);break
    except Exception:
     if attempt==2:raise
     await asyncio.sleep(1+attempt)
   print('TTS',cfg['id'],i+1,flush=True)

def align(p,cfg):
 sr=24000;raws=[];cursor=0;chap=[];subs=[];full=[]
 for i,c in enumerate(cfg['chapters']):
  wav=p/'audio'/f'{i:02}.wav';run(['ffmpeg','-v','error','-y','-i',str(p/'audio'/f'{i:02}.mp3'),'-ar',str(sr),'-ac','1',str(wav)])
  with wave.open(str(wav)) as w:raw=w.readframes(w.getnframes());dur=len(raw)/2/sr
  bd=[json.loads(l) for l in (p/'audio'/f'{i:02}.jsonl').read_text().splitlines() if l.strip()];assert bd
  for k,b in enumerate(bd):
   st=min(dur,b['offset']/1e7);en=min(dur,(b['offset']+b['duration'])/1e7)
   if en<=st:continue
   text=b['text'].strip('。，；')
   clauses=re.split('[，；。]',text);short=next((t for t in clauses if 3<=len(t)<=24),text)
   if len(short)>24:short=c['points'][min(k,len(c['points'])-1)]
   item={'start':round(cursor+st,3),'end':round(cursor+en,3),'text':short,'chapter':i};subs.append(item);full.append({**item,'text':b['text']})
  chap.append({**c,'start':cursor,'end':cursor+dur});raws.append(raw);raws.append(b'\0\0'*int(sr*.2));cursor+=dur+.2
 raws.pop();cursor-=.2
 for arr in [subs,full]:
  for a,b in zip(arr,arr[1:]):a['end']=min(a['end'],b['start'])
 with wave.open(str(p/'中文旁白.wav'),'w') as w:w.setparams((1,2,sr,0,'NONE','not compressed'));w.writeframes(b''.join(raws))
 srt(subs,p/'重点字幕.srt');srt(full,p/'完整旁白字幕.srt');timeline={'duration':cursor,'chapters':chap,'subtitles':subs,'full_subtitles':full,'alignment':'edge TTS SentenceBoundary plus decoded PCM duration; 200ms chapter gap'}
 (p/'时间轴.json').write_text(json.dumps(timeline,ensure_ascii=False,indent=2));return timeline

def box(d,x,y,w=100,h=100):
 d.polygon([(x,y+25),(x+w*.5,y),(x+w,y+25),(x+w,y+h),(x,y+h)],fill=C['mint'],outline=C['ink'],width=3);line(d,[(x+w*.5,y),(x+w*.5,y+h)],C['ink'],3)
def pin(d,x,y):
 d.ellipse((x-24,y-50,x+24,y-2),fill=C['orange']);d.polygon([(x-17,y-12),(x+17,y-12),(x,y+20)],fill=C['orange']);d.ellipse((x-9,y-35,x+9,y-17),fill=C['cream'])
def paper(d,x,y,w=240,h=250,label='记录'):
 rr(d,(x,y,x+w,y+h),C['white'],17,C['ink']);d.polygon([(x+w-50,y),(x+w,y+50),(x+w-50,y+50)],fill=C['mint']);center(d,label,x+w/2,y+60,30,width=w-20)
 for yy in range(int(y+125),int(y+h-20),35):line(d,[(x+28,yy),(x+w-28,yy)],'#B9CABE',4)
def lamp(d,x,y,s=1):
 line(d,[(x,y),(x,y+145*s)],C['ink'],int(7*s));d.ellipse((x-55*s,y+125*s,x+55*s,y+148*s),fill=C['ink']);d.polygon([(x-45*s,y-95*s),(x+45*s,y-95*s),(x+82*s,y+8*s),(x-82*s,y+8*s)],fill=C['orange'],outline=C['ink'],width=3)
def labels(d,pts,y=897):
 cell=610/len(pts)
 for k,t in enumerate(pts):
  x=55+cell*(k+.5);d.ellipse((x-5,y,x+5,y+10),fill=C['orange']);center(d,t,x,y+25,24,width=cell-12)
def art(d,cfg,c,u,index):
 id=cfg['id'];mode=c['visual'];accent=C['orange'];pose=math.sin(u*1.1)*.3
 if mode=='close':
  pts=PHASES[id]
  for k,(x,y) in enumerate([(160,515),(550,515),(550,745),(160,745)]):
   d.ellipse((x-48,y-48,x+48,y+48),fill=accent if k%2==0 else C['mint']);center(d,str(k+1),x,y-25,36);center(d,pts[k],x,y+70,28,width=200)
  for a,b in [((235,515),(475,515)),((550,575),(550,682)),((475,745),(235,745))]:arrow(d,a,b,C['mint'])
  return
 if id=='address':
  if mode=='map':
   for x in [140,255,370,485,600]:line(d,[(x,490),(x-30,830)],'#D2DACE',4)
   for y in [530,630,730,830]:line(d,[(110,y),(620,y-30)],'#D2DACE',4)
   line(d,[(173,777),(260,705),(420,705),(510,572)],accent,8);pin(d,510,572+int(math.sin(u)*7));badge(d,'坐标 → 地区',224,840,278)
  elif mode in ['defaults','shipping']:
   box(d,104,600,160,146);box(d,455,600,160,146);arrow(d,(289,675),(430,675));center(d,'寄件',185,788,30);center(d,'收件',535,788,30);pin(d,185,575);pin(d,535,575);badge(d,'分别设置默认地址',183,475,354)
  else:
   avatar(d,147,664,1,'user',pose);paper(d,300,485,292,330,'会员地址');center(d,'省市区 · 详细地址',446,655,23,width=270);center(d,'姓名 · 联系方式',446,707,23,width=270)
   if mode=='search':d.ellipse((470,765,545,840),outline=accent,width=8);line(d,[(535,830),(568,864)],accent,9)
 elif id=='agentrecharge':
  avatar(d,130,670,.9,'user',pose)
  if mode in ['contract','intro']:
   paper(d,295,485,292,337,'电子签约');line(d,[(345,740),(391,715),(426,744),(483,709),(534,726)],accent,5);badge(d,'按配置判断是否需要',277,845,340)
  elif mode=='levels':
   for k in range(3):
    x=279+k*104;y=755-k*83;d.rectangle((x,y,x+80,842),fill=[C['mint'],accent,C['pink']][k]);center(d,chr(65+k),x+40,y-55,32)
   badge(d,'最低额 ← 区间 → 最高额',250,485,386)
  elif mode=='proof':
   paper(d,275,480,285,306,'充值凭证');arrow(d,(400,808),(400,843));badge(d,'后台财务审核',270,850,280)
  else:
   for k,label in enumerate(['余额','积分']):
    x=342+k*195;d.ellipse((x-72,580,x+72,724),fill=accent if k==0 else C['mint'],outline=C['ink'],width=3);center(d,label,x,628,32)
   arrow(d,(438,755),(438,811));badge(d,'到账 → 等级升级',277,834,340)
 elif id=='aiapi':
  if mode in ['gate','intro','log']:
   avatar(d,124,670,.9,'user',pose);rr(d,(270,500,450,815),C['mint'],25);center(d,'授权',360,618,35);d.arc((321,531,399,605),180,360,fill=C['ink'],width=7);rr(d,(320,567,400,621),accent,8);arrow(d,(203,656),(248,656));arrow(d,(475,656),(530,656));paper(d,548,560,120,203,'操作');
  else:
   modes={'product':['分类','商品','库存'],'order':['查询','备注','发货'],'member':['会员','统计','上传']};ls=modes.get(mode,['授权','调用','日志'])
   for k,l in enumerate(ls):
    x=84+k*210;box(d,x,572,137,160);center(d,l,x+68,772,30,width=180)
    if k<2:arrow(d,(x+145,658),(x+197,658))
   badge(d,'按管理员权限与令牌范围',160,468,400)
 elif id=='aidatasource':
  if mode in ['platforms','intro']:
   for k,l in enumerate(['抖音','小红书','快手','B站','微博','贴吧','知乎']):
    a=k*math.tau/7-1.57;x=360+220*math.cos(a);y=675+175*math.sin(a);line(d,[(360,675),(x,y)],C['mint'],4);d.ellipse((x-45,y-45,x+45,y+45),fill=accent if k%2==0 else C['mint']);center(d,l,x,y-15,20,width=94)
   d.ellipse((300,615,420,735),fill=C['ink']);center(d,'任务',360,651,30,C['cream'])
  elif mode=='tasks':
   for k,l in enumerate(['新建','列表','详情']):
    x=95+k*210;paper(d,x,515+k*50,145,190,l)
    if k<2:arrow(d,(x+153,675),(x+194,675))
   badge(d,'刷新 → 查看结果',182,847,354)
  elif mode in ['results','comments']:
   paper(d,120,490,290,330,'评论' if mode=='comments' else '内容');badge(d,'标题 / 正文',409,536,205);badge(d,'作者 / 时间',409,633,205);badge(d,'平台 / 计数',409,731,205)
  else:
   avatar(d,139,677,.9,'merchant',pose);rr(d,(306,533,592,783),C['mint'],32);center(d,'服务连接',449,615,35);arrow(d,(210,660),(281,660));badge(d,'权限与任务范围',279,837,340)
 elif id=='aidrama':
  if mode in ['intro','script','film']:
   rr(d,(133,506,594,815),C['ink'],18);d.rectangle((157,542,570,770),fill=C['cream'])
   for k in range(8):
    x=158+k*54;d.rectangle((x,518,x+23,533),fill=accent);d.rectangle((x,783,x+23,798),fill=accent)
   if mode=='script':paper(d,260,561,210,165,'剧本')
   else:
    d.polygon([(324,594),(324,718),(429,656)],fill=accent);center(d,'分镜 → 视频任务' if mode=='film' else '创作工作台',360,852,31)
  elif mode=='assets':
   for k,l in enumerate(['角色','道具','场景']):
    x=90+k*213;rr(d,(x,530,x+150,791),[C['mint'],accent,C['pink']][k],20);center(d,l,x+75,720,27,width=148)
   avatar(d,164,624,.5,'user');box(d,328,584,102,105);d.polygon([(536,623),(581,572),(624,623)],fill=C['ink']);badge(d,'声音资产：手动上传',173,850,374)
  elif mode in ['queue','health','providers']:
   ls={'queue':['排队','运行','成功 / 失败'],'health':['额度','并发','队列健康'],'providers':['语言模型','生图','视频']}[mode]
   for k,l in enumerate(ls):
    y=480+k*126;badge(d,l,248,y,363,accent if k%2 else C['mint'])
    if k<2:arrow(d,(430,y+58),(430,y+110))
   avatar(d,129,665,.88,'merchant',pose)
  elif mode=='brand':
   rr(d,(127,510,592,806),C['ink'],25);center(d,'品牌',360,606,48,C['cream']);center(d,'标识 · 标题 · 主题色',360,705,27,C['cream']);badge(d,'站点与门店配置',174,848,372)
  else:
   for k,l in enumerate(['套餐','创作点','任务']):
    x=160+k*200;d.ellipse((x-67,580,x+67,714),fill=accent if k==1 else C['mint']);center(d,l,x,626,27,width=140)
    if k<2:arrow(d,(x+75,647),(x+123,647))
 elif id=='aiscene':
  if mode in ['intro','generate','chat']:
   rr(d,(100,490,615,822),C['soft'],24);d.ellipse((390,520,550,680),fill=C['mint']);d.polygon([(104,819),(104,732),(292,674),(611,766),(611,819)],fill=C['pink']);lamp(d,355,644,.9)
   if mode=='chat':badge(d,'文字指令 → 继续生成',149,851,422)
   else:badge(d,'商品 × 场景',214,851,292)
  elif mode=='library':
   for k,l in enumerate(['场景组','提示词','参考图']):
    x=93+k*210;rr(d,(x,530,x+158,795),[C['mint'],accent,C['pink']][k],20);center(d,l,x+79,708,27,width=154)
    d.ellipse((x+38,577,x+119,658),fill=C['cream'])
  elif mode=='binding':
   lamp(d,205,644,.8);arrow(d,(300,663),(401,663));paper(d,451,520,177,245,'场景组');badge(d,'商品详情入口',187,847,346)
  elif mode=='share':
   rr(d,(150,500,557,792),C['white'],24,C['ink']);lamp(d,353,626,.7);arrow(d,(358,806),(358,847));badge(d,'保存相册 / 小程序分享',132,854,456)
  else:
   d.arc((176,510,548,862),190,530,fill=accent,width=18);center(d,'每日次数',360,619,40);center(d,'全局口径',360,689,29);badge(d,'登录 · 模型 · 尺寸',187,850,346)
 elif id=='aitouchshare':
  if mode in ['intro','nfc']:
   rr(d,(281,485,469,819),C['ink'],32);rr(d,(299,517,451,781),C['cream'],18);center(d,'NFC',375,626,35)
   for k in range(3):d.arc((143-k*20,568-k*25,286+k*20,738+k*25),-65,65,fill=accent,width=5)
   rr(d,(500,605,622,727),C['mint'],15);center(d,'标签',561,643,27,width=120);badge(d,'碰一碰 / 扫码',189,850,340)
  elif mode=='store':
   d.polygon([(106,620),(360,488),(613,620)],fill=accent);rr(d,(143,620,577,815),C['mint'],12);center(d,'门店 · 场景',360,685,39);badge(d,'素材组 / 文案模板',180,849,364)
  elif mode in ['proof','funnel']:
   for k,l in enumerate(['提交','审核','结果'] if mode=='proof' else ['触达','操作','回流']):
    x=154+k*205;y=560+k*70;d.ellipse((x-60,y-60,x+60,y+60),fill=accent if k==1 else C['mint']);center(d,l,x,y-18,29,width=130)
    if k<2:arrow(d,(x+72,y+20),(x+140,y+49))
   badge(d,'操作与结果分开看',173,850,374)
  else:
   paper(d,105,510,210,285,'文案素材');avatar(d,550,647,.88,'user',pose);arrow(d,(344,653),(446,653));badge(d,'用户自主确认发布',166,852,388)

def draw(t,cfg,timeline):
 chapters=timeline['chapters'];i=next((i for i,c in enumerate(chapters) if c['start']<=t<c['end']+.2),len(chapters)-1);c=chapters[i];u=t-c['start'];dark=c['visual'] in ['intro','close'];fg=C['cream'] if dark else C['ink']
 im=Image.new('RGB',(720,1280),C['ink'] if dark else C['cream']);d=ImageDraw.Draw(im)
 tx(d,'大象商城',48,40,29,fg);tx(d,cfg['title'],48,92,24,fg,width=470);tx(d,'流程示意',570,48,20,C['mint'] if dark else C['muted'],width=110)
 names=PHASES[cfg['id']];active=c.get('phase',min(3,int(i/max(1,len(chapters)-1)*4)))
 for k,l in enumerate(names):
  x=104+k*171
  if k<3:line(d,[(x+23,217),(x+144,217)],'#9BB8A6',3)
  d.ellipse((x-18,199,x+18,235),fill=C['orange'] if k==active else C['mint']);center(d,str(k+1),x,200,20);center(d,l,x,252,23,fg,width=160)
 tx(d,c['role'],49,321,24,C['orange'] if dark else C['muted']);tx(d,c['heading'],49,375,36,fg,width=621)
 if dark:rr(d,(40,465,680,1030),C['cream'],34)
 art(d,cfg,c,u,i);labels(d,c['points'],935)
 # Per-sentence time-aligned highlights, never the whole narration wall.
 cap=next((v['text'] for v in timeline['subtitles'] if v['start']<=t<v['end']),c['points'][0])
 rr(d,(39,1054,681,1187),'#254F46' if dark else C['soft'],26);center(d,cap,360,1081,33,fg,width=592)
 tx(d,'SaaS 产品介绍',49,1215,18,C['mint'] if dark else C['muted']);line(d,[(49,1250),(671,1250)],'#A4B6A6',3);line(d,[(49,1250),(49+622*t/timeline['duration'],1250)],C['orange'],4)
 # Subtle whole-scene entrance without fake UI or transitions obscuring speech captions.
 local=min(1,max(0,u/.35))
 if local<1:
  overlay=Image.new('RGB',im.size,C['ink'] if dark else C['cream']);im=Image.blend(overlay,im,.82+.18*local)
 return im

def render(p,cfg,tl):
 C['orange']=PALETTES[cfg['id']];fps=24;dur=math.ceil(tl['duration']*fps)/fps;frames=round(dur*fps);qa=p/'qa';qa.mkdir(exist_ok=True)
 for i,c in enumerate(tl['chapters']):draw((c['start']+c['end'])/2,cfg,tl).save(qa/f'layout_{i:02}.jpg',quality=93)
 draw(3,cfg,tl).save(p/'封面.jpg',quality=95)
 with wave.open(str(p/'中文旁白.wav')) as w:sr=w.getframerate();v=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
 voice_secs=len(v)/sr;v=np.pad(v,(0,math.ceil(dur*sr)-len(v)));t=np.arange(len(v))/sr;music=np.zeros(len(v));base=[130.81,110,87.31,98];shift=(cfg['index']%3)*2
 for k in range(math.ceil(dur*1.25)):
  start=int(k/1.25*sr);n=min(int(1.7*sr),len(v)-start)
  if n<=0:break
  tt=np.arange(n)/sr;freq=base[k//8%4]*[1,1.25,1.5][k%3]*2**(shift/12);music[start:start+n]+=(np.sin(2*math.pi*freq*tt)+.1*np.sin(4*math.pi*freq*tt))*np.minimum(tt/.035,1)*np.exp(-2.7*tt)
 music*=np.minimum(t/2,1)*np.minimum((dur-t)/3,1);vrms=np.sqrt(np.mean(v*v));music*=vrms*10**(-22/20)/max(np.sqrt(np.mean(music*music)),1e-9);mixed=v+music;peak=np.max(np.abs(mixed));assert peak<1
 for name,a in [('原创低音量音乐.wav',music),('旁白音乐混音.wav',mixed)]:
  with wave.open(str(p/name),'w') as w:w.setparams((1,2,sr,0,'NONE','not compressed'));w.writeframes((a*32767).astype('<i2').tobytes())
 dest=p/cfg['output_filename']
 with (qa/'encode.log').open('w') as err:
  proc=subprocess.Popen(['ffmpeg','-v','warning','-y','-f','rawvideo','-pix_fmt','rgb24','-s','720x1280','-r','24','-i','-','-i',str(p/'旁白音乐混音.wav'),'-c:v','libx264','-threads','2','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t',str(dur),str(dest)],stdin=subprocess.PIPE,stderr=err)
  try:
   for k in range(frames):proc.stdin.write(draw(k/fps,cfg,tl).tobytes())
  finally:proc.stdin.close()
  assert proc.wait()==0
 result=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(dest),'-f','null','-'],capture_output=True,text=True);assert result.returncode==0,result.stderr
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(dest)]));vs=next(s for s in probe['streams'] if s['codec_type']=='video');au=next(s for s in probe['streams'] if s['codec_type']=='audio');assert (vs['width'],vs['height'])==(720,1280) and float(au['duration'])>=voice_secs
 for n,c in enumerate(tl['chapters']):run(['ffmpeg','-v','error','-y','-ss',str((c['start']+c['end'])/2),'-i',str(dest),'-frames:v','1','-q:v','2',str(qa/f'encoded_{n:02}.jpg')])
 forbidden=['根据文档','未实机验收','以资料为准','尚未实机','未通过','依据业务文档']
 assert all(not any(f in s['narration'] for f in forbidden) for s in cfg['chapters'])
 assert all(s['end']<=dur and s['start']<s['end'] for s in tl['subtitles'])
 summary={'script_sha256':hashlib.sha256((p/'script.json').read_bytes()).hexdigest(),'voice_sha256':hashlib.sha256((p/'中文旁白.wav').read_bytes()).hexdigest(),'id':cfg['id'],'title':cfg['title'],'duration':dur,'video':str(dest),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'full_decode_ok':True,'audio_duration':float(au['duration']),'voice_duration':voice_secs,'last_speech_boundary':tl['full_subtitles'][-1]['end'],'voice_not_truncated':float(au['duration'])>=voice_secs,'dimensions':[720,1280],'fps':24,'codecs':['h264','aac'],'music_rms_below_voice_db':22,'mixed_peak_dbfs':20*math.log10(peak),'subtitle_count':len(tl['subtitles']),'subtitle_alignment':'TTS SentenceBoundary','all_frame_text_bounds_asserted':True,'customer_internal_disclaimer_check':True,'evidence_gaps':cfg['gaps'],'implementation_verified':False,'human_video_review':'pending parent videoReview'}
 (p/'QA.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));(qa/'ffprobe.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2));mark_status(cfg['id'],'rendered_technical_qa_passed',**{k:summary[k] for k in ['video','duration','sha256','bytes']});print('DONE',json.dumps(summary,ensure_ascii=False),flush=True)

def main():
 import fcntl
 lock=(ROOT/'.render.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 mode=sys.argv[1] if len(sys.argv)>1 else 'all'
 for p in sorted((ROOT/'plugins').iterdir()):
  if not (p/'script.json').exists():continue
  cfg=json.loads((p/'script.json').read_text())
  state=next((x for x in json.loads((ROOT/'progress.json').read_text())['plugins'] if x['id']==cfg['id']),{})
  if state.get('status','').startswith(('hold','needs_evidence')):print('HOLD PRESERVED',cfg['id'],flush=True);continue
  try:
   if mode in ['all','speech']:mark_status(cfg['id'],'generating_voice');asyncio.run(speech(p,cfg));tl=align(p,cfg);mark_status(cfg['id'],'voice_ready',voice_duration=tl['duration'])
   if mode in ['all','render']:
    if (p/'QA.json').exists():
     previous=json.loads((p/'QA.json').read_text())
     same_script=previous.get('script_sha256')==hashlib.sha256((p/'script.json').read_bytes()).hexdigest()
     same_voice=previous.get('voice_sha256')==hashlib.sha256((p/'中文旁白.wav').read_bytes()).hexdigest()
     dest=p/cfg['output_filename']
     intact=dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest()==previous.get('sha256')
     if same_script and same_voice and intact:
      mark_status(cfg['id'],'rendered_technical_qa_passed',**{k:previous[k] for k in ['video','duration','sha256','bytes']});print('RESUME VERIFIED SKIP',cfg['id'],flush=True);continue
    tl=json.loads((p/'时间轴.json').read_text());mark_status(cfg['id'],'rendering');render(p,cfg,tl)
  except Exception as e:mark_status(cfg['id'],'failed',error=str(e));raise
if __name__=='__main__':main()
