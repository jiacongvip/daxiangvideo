# -*- coding: utf-8 -*-
"""生成「经营看板」示意数据面板 1080x1200"""
import subprocess, os

FF = "/Users/jiacong/.local/bin/ffmpeg"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
OUT = "/Users/jiacong/Downloads/剪辑素材/项目/02_鸡蛋配送案例/02_贴片图/数据看板_示意.png"

W, H = 1080, 1200
BG = "0xF4F7FC"
WHITE = "white"
DARK = "0x1B2433"
GRAY = "0x7A8498"
BLUE = "0x2B6BFF"
ORANGE = "0xF07A28"
LINE = "0xE6EBF5"

p = []


def T(t, x, y, s, c=DARK, extra=""):
    return (f"drawtext=fontfile='{FONT}':text='{t}':x={x}:y={y}:"
            f"fontsize={s}:fontcolor={c}:expansion=none{extra}")


def B(x, y, w, h, c, fill=True, t=2):
    return f"drawbox=x={x}:y={y}:w={w}:h={h}:color={c}:t={'fill' if fill else t}"


# 顶部
p.append(B(0, 0, W, 86, WHITE))
p.append(B(0, 86, W, 2, LINE))
p.append(f"drawbox=x=44:y=26:w=6:h=34:color={BLUE}:t=fill")
p.append(T("经营看板", 64, 22, 38))
p.append(T("2026 全年", 880, 30, 24, GRAY))

# KPI
kpis = [("年销售额", "1.02", "亿", BLUE, "0xDDE7FF"),
        ("客户数", "1,286", "家", BLUE, "0xDDE7FF"),
        ("配送单量", "32.8", "万单", BLUE, "0xDDE7FF"),
        ("客户复购率", "78", "%", ORANGE, "0xFFE9D8")]
cw, gap, ky, kh = 240, 12, 108, 196
for i, (lab, val, unit, col, bg) in enumerate(kpis):
    x = 40 + i * (cw + gap)
    p.append(B(x, ky, cw, kh, WHITE))
    p.append(B(x, ky, cw, kh, LINE, False))
    p.append(B(x, ky, cw, 6, col))
    p.append(T(lab, x + 24, ky + 26, 23, GRAY))
    p.append(T(val, x + 24, ky + 68, 58))
    p.append(T(unit, x + 24 + len(val) * 36, ky + 106, 22, GRAY))

# 折线/柱状：月度销售额
p.append(B(40, 324, 1000, 480, WHITE))
p.append(B(40, 324, 1000, 480, LINE, False))
p.append(T("月度销售额（万元）", 72, 340, 26))
p.append(T("全年合计 10,360 万元", 760, 344, 21, GRAY))
vals = [620, 680, 740, 710, 800, 860, 830, 920, 960, 1010, 1080, 1150]
base_y, plot_h, maxv = 748, 330, 1150
bw, step, x0 = 56, 75, 112
for i, v in enumerate(vals):
    h = int(v / maxv * plot_h)
    x = x0 + i * step
    col = ORANGE if i >= 10 else BLUE
    p.append(B(x, base_y - h, bw, h, col))
    p.append(T(str(i + 1), x + 20, base_y + 12, 19, GRAY))
p.append(B(72, base_y + 2, 936, 2, "0xCFD9EA"))

# 品类占比
p.append(B(40, 826, 1000, 268, WHITE))
p.append(B(40, 826, 1000, 268, LINE, False))
p.append(T("品类销售占比", 72, 842, 26))
cats = [("鸡蛋", 82, "0xF07A28"), ("米面粮油", 11, "0x2B6BFF"), ("其他", 7, "0x9AA7BC")]
for i, (name, pct, col) in enumerate(cats):
    y = 888 + i * 62
    p.append(T(name, 72, y - 4, 22, GRAY))
    p.append(B(200, y, 600, 22, "0xEDF1F8"))
    p.append(B(200, y, int(600 * pct / 100), 22, col))
    p.append(T(f"{pct}%", 820, y - 4, 22))

p.append(T("数据示意 · 仅用于演示系统形态", 40, 1122, 20, "0xAEB8C8"))

vf = ",".join(p)
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                "-i", f"color=c={BG}:s={W}x{H}:d=1", "-vf", vf,
                "-frames:v", "1", OUT], check=True)
print("ok", OUT)
