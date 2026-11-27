# -*- coding: utf-8 -*-
import subprocess, os, shlex

FF = "/Users/jiacong/.local/bin/ffmpeg"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
OUT = "/Users/jiacong/Downloads/剪辑素材/_work"

W, H = 1080, 1300
BG = "0xF4F7FC"
WHITE = "white"
DARK = "0x1B2433"
GRAY = "0x7A8498"
BLUE = "0x2B6BFF"
GREEN = "0x00B36B"
LINE = "0xE6EBF5"

parts = []

# 顶部白色 header
parts.append(f"drawbox=x=0:y=0:w={W}:h=104:color={WHITE}@1:t=fill")
parts.append(f"drawbox=x=0:y=104:w={W}:h=2:color={LINE}@1:t=fill")
parts.append(f"drawtext=fontfile='{FONT}':text='客户行为看板':x=44:y=30:fontsize=42:fontcolor={DARK}")
parts.append(f"drawtext=fontfile='{FONT}':text='近 7 天':x=880:y=40:fontsize=26:fontcolor={GRAY}")

# KPI 卡片
kpis = [("访问客户", "128", "人"), ("浏览次数", "342", "次"), ("活动点击", "96", "次"), ("领券", "41", "张")]
cw, gap, cy, ch = 240, 12, 140, 210
for i, (lab, val, unit) in enumerate(kpis):
    x = 40 + i * (cw + gap)
    parts.append(f"drawbox=x={x}:y={cy}:w={cw}:h={ch}:color={WHITE}@1:t=fill")
    parts.append(f"drawbox=x={x}:y={cy}:w={cw}:h={ch}:color={LINE}@1:t=2")
    parts.append(f"drawtext=fontfile='{FONT}':text='{lab}':x={x+26}:y={cy+30}:fontsize=26:fontcolor={GRAY}")
    parts.append(f"drawtext=fontfile='{FONT}':text='{val}':x={x+26}:y={cy+80}:fontsize=66:fontcolor={DARK}")
    parts.append(f"drawtext=fontfile='{FONT}':text='{unit}':x={x+26+len(val)*40}:y={cy+118}:fontsize=24:fontcolor={GRAY}")

# 表格
ty = 400
parts.append(f"drawbox=x=40:y={ty}:w=1000:h=880:color={WHITE}@1:t=fill")
parts.append(f"drawbox=x=40:y={ty}:w=1000:h=880:color={LINE}@1:t=2")
parts.append(f"drawtext=fontfile='{FONT}':text='客户明细':x=72:y={ty+18}:fontsize=30:fontcolor={DARK}")
parts.append(f"drawbox=x=40:y={ty+72}:w=1000:h=2:color={LINE}@1:t=fill")

cols = [(76, "客户"), (430, "访问次数"), (600, "点击活动"), (760, "领券"), (880, "状态")]
for x, name in cols:
    parts.append(f"drawtext=fontfile='{FONT}':text='{name}':x={x}:y={ty+88}:fontsize=24:fontcolor={GRAY}")

rows = [("王", "王**", "8", "3", "1", "高意向", GREEN),
        ("李", "李**", "5", "2", "0", "待跟进", GRAY),
        ("张", "张**", "4", "1", "1", "已领券", BLUE),
        ("陈", "陈**", "2", "0", "0", "新访客", GRAY),
        ("刘", "刘**", "1", "0", "0", "新访客", GRAY),
        ("赵", "赵**", "3", "2", "1", "已领券", BLUE)]
rh = 120
for i, (ini, name, v1, v2, v3, st, stc) in enumerate(rows):
    ry = ty + 132 + i * rh
    parts.append(f"drawbox=x=56:y={ry+22}:w=76:h=76:color=0xDDE7FF@1:t=fill")
    parts.append(f"drawtext=fontfile='{FONT}':text='{ini}':x={56+26}:y={ry+40}:fontsize=34:fontcolor={BLUE}")
    parts.append(f"drawtext=fontfile='{FONT}':text='{name}':x=152:y={ry+38}:fontsize=32:fontcolor={DARK}")
    parts.append(f"drawtext=fontfile='{FONT}':text='{v1} 次':x=430:y={ry+42}:fontsize=30:fontcolor={DARK}")
    parts.append(f"drawtext=fontfile='{FONT}':text='{v2} 次':x=600:y={ry+42}:fontsize=30:fontcolor={DARK}")
    parts.append(f"drawtext=fontfile='{FONT}':text='{v3} 张':x=760:y={ry+42}:fontsize=30:fontcolor={DARK}")
    parts.append(f"drawtext=fontfile='{FONT}':text='{st}':x=880:y={ry+42}:fontsize=28:fontcolor={stc}")
    if i < len(rows) - 1:
        parts.append(f"drawbox=x=40:y={ry+rh}:w=1000:h=1:color={LINE}@1:t=fill")

parts.append(f"drawtext=fontfile='{FONT}':text='数据示意 · 仅用于演示':x=40:y=1255:fontsize=22:fontcolor=0xAEB8C8")

vf = ",".join(parts)
cmd = [FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"color=c={BG}:s={W}x{H}:d=1",
       "-vf", vf, "-frames:v", "1", os.path.join(OUT, "dashboard.png")]
print(shlex.join(cmd)[:300])
subprocess.run(cmd, check=True)
print("ok")
