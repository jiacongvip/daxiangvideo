#!/usr/bin/env python3
"""大象商城详细功能视频 · 单项目可迁移重渲染入口（非剪映/Premiere工程）。

用法:
  cd 源文件/公共工具
  python render_one.py ../插件/某项目文件夹
  python render_one.py ../核心功能/某项目文件夹 --remake-music

默认复用项目内时间轴、中文旁白与已有混音，只重出画面与成片。
"""
from __future__ import annotations
from pathlib import Path
import sys,json,hashlib,math,wave,subprocess,importlib
from functools import lru_cache
import numpy as np
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import graphics as g

def load_art(batch:str):
  if not batch or batch in {'early','None'}:
    return importlib.import_module('run_series_reference')
  sys.path.insert(0,str(ROOT))
  return importlib.import_module(f'batch_arts_pkg.batch{int(batch):02}.batch_art')

def setup_draw(cfg,tl,artmod,early=False):
  accent=cfg.get('accent','#F0AA79');g.C['orange']=accent
  if early:
    artmod.PHASES[cfg['id']]=cfg['phases'];artmod.PALETTES[cfg['id']]=accent;artmod.C['orange']=accent
    return lambda t,c=cfg,tt=tl: artmod.draw(t,c,tt)
  @lru_cache(maxsize=8)
  def base(i,cap):
    c=tl['chapters'][i];dark=c['visual'] in ['intro','close'];fg=g.C['cream'] if dark else g.C['ink']
    im=Image.new('RGB',(720,1280),g.C['ink'] if dark else g.C['cream']);d=ImageDraw.Draw(im)
    g.tx(d,'大象商城',48,40,29,fg);g.tx(d,cfg['title'],48,92,24,fg,width=470);g.tx(d,'流程示意',570,48,20,g.C['mint'] if dark else g.C['muted'],width=110)
    for k,l in enumerate(cfg['phases']):
      x=104+k*171
      if k<3:g.line(d,[(x+23,217),(x+144,217)],'#9BB8A6',3)
      d.ellipse((x-18,199,x+18,235),fill=g.C['orange'] if k==c.get('phase',0) else g.C['mint']);g.center(d,str(k+1),x,200,20);g.center(d,l,x,252,23,fg,width=160)
    g.tx(d,c['role'],49,321,24,g.C['orange'] if dark else g.C['muted']);g.tx(d,c['heading'],49,375,36,fg,width=621)
    if dark:g.rr(d,(40,465,680,1030),g.C['cream'],34)
    artmod.art(d,cfg,c,0,i);g.labels(d,c['points'],935)
    g.rr(d,(39,1054,681,1187),'#254F46' if dark else g.C['soft'],26);g.center(d,cap,360,1081,33,fg,width=592)
    g.tx(d,'SaaS 产品介绍',49,1215,18,g.C['mint'] if dark else g.C['muted']);g.line(d,[(49,1250),(671,1250)],'#A4B6A6',3);return im
  def draw(t,cfg=cfg,tl=tl):
    i=next((j for j,c in enumerate(tl['chapters']) if c['start']<=t<c['end']+.2),len(tl['chapters'])-1)
    c=tl['chapters'][i];u=t-c['start'];cap=next((v['text'] for v in tl['subtitles'] if v['start']<=t<v['end']),c['points'][0])
    im=base(i,cap).copy();d=ImageDraw.Draw(im)
    if c.get('phase',0)<3:
      x=104+c['phase']*171+26+111*((u*.32)%1);d.ellipse((x-5,212,x+5,222),fill=g.C['orange'])
    if hasattr(artmod,'motion'):artmod.motion(d,cfg,c,u)
    g.line(d,[(49,1250),(49+622*t/tl['duration'],1250)],g.C['orange'],4)
    if 0<=u<.4:
      bg=Image.new('RGB',im.size,g.C['ink'] if c['visual'] in ['intro','close'] else g.C['cream']);im=Image.blend(bg,im,.86+.14*u/.4)
    return im
  return draw

def ensure_mix(p,cfg,tl,remake=False):
  mix=p/'旁白音乐混音.wav';voice=p/'中文旁白.wav'
  if mix.exists() and voice.exists() and not remake:return mix
  with wave.open(str(voice)) as w:sr=w.getframerate();v=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)/32768
  dur=math.ceil(tl['duration']*24)/24;v=np.pad(v,(0,max(0,math.ceil(dur*sr)-len(v))));t=np.arange(len(v))/sr;music=np.zeros(len(v));basef=[130.81,110,87.31,98];shift=(cfg.get('index',0)%3)*2
  for k in range(math.ceil(dur*1.25)):
    start=int(k/1.25*sr);n=min(int(1.7*sr),len(v)-start)
    if n<=0:break
    tt=np.arange(n)/sr;freq=basef[k//8%4]*[1,1.25,1.5][k%3]*2**(shift/12);music[start:start+n]+=(np.sin(2*math.pi*freq*tt)+.1*np.sin(4*math.pi*freq*tt))*np.minimum(tt/.035,1)*np.exp(-2.7*tt)
  music*=np.minimum(t/2,1)*np.minimum((dur-t)/3,1);vrms=np.sqrt(np.mean(v*v));music*=vrms*10**(-22/20)/max(np.sqrt(np.mean(music*music)),1e-9);mixed=v+music;assert np.max(np.abs(mixed))<1
  for name,a in [('原创低音量音乐.wav',music),('旁白音乐混音.wav',mixed)]:
    with wave.open(str(p/name),'w') as w:w.setparams((1,2,sr,0,'NONE','not compressed'));w.writeframes((a*32767).astype('<i2').tobytes())
  return p/'旁白音乐混音.wav'

def render(project:str, remake_music=False):
  p=Path(project).resolve()
  cfg=json.loads((p/'script.json').read_text());tl=json.loads((p/'时间轴.json').read_text())
  meta=json.loads((p/'项目说明.json').read_text()) if (p/'项目说明.json').exists() else {}
  batch=str(meta.get('batch') or meta.get('制作批次') or '')
  early=batch in ('','early','None')
  artmod=load_art(batch);draw=setup_draw(cfg,tl,artmod,early=early)
  mix=ensure_mix(p,cfg,tl,remake=remake_music)
  fps=24;dur=math.ceil(tl['duration']*fps)/fps;frames=round(dur*fps);out=p/cfg['output_filename'];qa=p/'qa_rebuild';qa.mkdir(exist_ok=True)
  draw(3).save(p/'封面.jpg',quality=95)
  with (qa/'encode.log').open('w') as err:
    proc=subprocess.Popen(['ffmpeg','-v','warning','-y','-f','rawvideo','-pix_fmt','rgb24','-s','720x1280','-r','24','-i','-','-i',str(mix),'-c:v','libx264','-threads','2','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-t',str(dur),str(out)],stdin=subprocess.PIPE,stderr=err)
    try:
      for k in range(frames):proc.stdin.write(draw(k/fps).tobytes())
    finally:proc.stdin.close()
    rc=proc.wait()
  if rc!=0:raise SystemExit((qa/'encode.log').read_text()[-3000:])
  print(json.dumps(dict(rebuilt=str(out),bytes=out.stat().st_size,sha256=hashlib.sha256(out.read_bytes()).hexdigest(),duration=dur,batch=batch or 'early'),ensure_ascii=False))

if __name__=='__main__':
  if len(sys.argv)<2:raise SystemExit('用法: python render_one.py <项目文件夹> [--remake-music]')
  render(sys.argv[1], remake_music='--remake-music' in sys.argv)
