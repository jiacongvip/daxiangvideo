# -*- coding: utf-8 -*-
"""生成「鸡蛋配送系统」三张知识贴片图 1080x1080"""
import subprocess, os

FF = "/Users/jiacong/.local/bin/ffmpeg"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
OUT = "/Users/jiacong/Downloads/剪辑素材/素材/贴片"
os.makedirs(OUT, exist_ok=True)

W = H = 1080
BG = "0xF5F7FB"
CARD = "0xFFFFFF"
BORDER = "0xE2E8F3"
DARK = "0x16202F"
GRAY = "0x76839A"
BLUE = "0x2B6BFF"
GREEN = "0x00A96E"
ORANGE = "0xE8792B"
PURPLE = "0x6C5CE7"
NAVY = "0x111A2B"


def T(text, x, y, size, color=DARK, extra=""):
    return (f"drawtext=fontfile='{FONT}':text='{text}':x={x}:y={y}:"
            f"fontsize={size}:fontcolor={color}{extra}")


def box(x, y, w, h, color, fill=True, t=2):
    return (f"drawbox=x={x}:y={y}:w={w}:h={h}:color={color}:t="
            f"{'fill' if fill else t}")


def card(x, y, w, h, fill=CARD, border=BORDER):
    return box(x, y, w, h, fill) + "," + box(x, y, w, h, border, False)


def header(tag_no, tag_txt, title, sub):
    p = []
    p.append(box(44, 54, 6, 34, BLUE))
    p.append(T(tag_no, 64, 52, 30, BLUE))
    p.append(T(tag_txt, 118, 56, 26, GRAY))
    p.append(T(title, 44, 118, 58))
    p.append(T(sub, 44, 196, 27, GRAY))
    return p


def render(path, parts):
    cmd = [FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
           "-i", f"color=c={BG}:s={W}x{H}:d=1",
           "-vf", ",".join(parts), "-frames:v", "1", path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-1500:])
        raise SystemExit(1)
    print("ok", os.path.basename(path))


# ============ 图1 拓客与定价 ============
p = header("01", "拓客与定价", "同一批蛋，能有三种价", "批发最怕价格乱，一乱就漏钱")

rows = [
    ("01", "一客一价", "新客、老客、大批量", "各是各的价，不串", "防串价", BLUE),
    ("02", "阶梯价", "拿得越多，单价越低", "系统自动跳档", "自动算", GREEN),
    ("03", "业务员系统", "帮客户手机上直接下单", "业绩自动归集", "防飞单", PURPLE),
]
y0 = 264
for i, (no, title, d1, d2, chip, col) in enumerate(rows):
    y = y0 + i * 232
    p.append(card(44, y, 992, 200))
    p.append(box(44, y, 8, 200, col))
    p.append(T(no, 82, y + 34, 34, col))
    p.append(T(title, 82, y + 88, 44))
    p.append(T(d1, 372, y + 62, 26, GRAY))
    p.append(T(d2, 372, y + 104, 26, GRAY))
    # 右侧标签
    p.append(box(838, y + 78, 156, 46, col, False, 2))
    p.append(T(chip, 866, y + 86, 26, col))

p.append(box(44, 968, 992, 76, NAVY))
p.append(T("结果：报价口径统一，每一单都查得到是谁开的", 72, 990, 28, "0xFFFFFF"))
render(os.path.join(OUT, "图1_拓客定价.png"), p)

# ============ 图2 调度与配送 ============
p = header("02", "调度与配送", "几百个点，怎么一趟送完", "靠老司机记路，漏一单就少一个客户")

flow = [
    ("订单汇总", "同一条街、同一个片区，归到一起"),
    ("配送批次", "按线路分批，谁送哪一片定死"),
    ("路径规划", "系统排顺序，不走回头路"),
    ("配送员接单", "手机上一条条点，送完即回传"),
]
y0 = 262
for i, (title, desc) in enumerate(flow):
    y = y0 + i * 168
    p.append(card(44, y, 992, 132))
    p.append(box(84, y + 40, 52, 52, BLUE if i < 3 else GREEN))
    p.append(T(str(i + 1), 100, y + 50, 30, "0xFFFFFF"))
    p.append(T(title, 162, y + 34, 38))
    p.append(T(desc, 162, y + 84, 25, GRAY))
    if i < 3:
        p.append(box(537, y + 140, 4, 22, "0xC6D2E6"))

p.append(box(44, 940, 992, 76, NAVY))
p.append(T("每一单送到谁手上、几点送到，后台都留痕", 72, 962, 28, "0xFFFFFF"))
render(os.path.join(OUT, "图2_调度配送.png"), p)

# ============ 图3 结算与风控 ============
p = header("03", "结算与风控", "钱和筐，最容易漏的两样", "这两样管不住，卖得越多亏得越多")

# 左：退筐结算
p.append(card(44, 264, 486, 522))
p.append(box(44, 264, 486, 8, ORANGE))
p.append(T("退筐结算", 84, 306, 44))
p.append(T("押筐 · 出筐 · 回筐 · 赔付", 84, 372, 24, GRAY))
steps = ["押金登记，出几个筐", "带回几个，司机当场点", "少了破了，系统自动赔", "月底一起结，不扯皮"]
for i, s in enumerate(steps):
    yy = 430 + i * 88
    p.append(box(84, yy + 10, 12, 12, ORANGE))
    p.append(T(s, 116, yy, 25))

# 右：记账月结
p.append(card(550, 264, 486, 522))
p.append(box(550, 264, 486, 8, BLUE))
p.append(T("记账月结", 590, 306, 44))
p.append(T("账期 · 对账 · 催收", 590, 372, 24, GRAY))
steps2 = ["按客户设账期，到期提醒", "送货单和欠款自动对上", "对账单直接发客户", "谁欠多少，一眼看完"]
for i, s in enumerate(steps2):
    yy = 430 + i * 88
    p.append(box(590, yy + 10, 12, 12, BLUE))
    p.append(T(s, 622, yy, 25))

p.append(box(44, 852, 992, 116, NAVY))
p.append(T("筐和账绑在一起，才不会变成糊涂账", 72, 872, 32, "0xFFFFFF"))
p.append(T("配送系统 · 真实客户案例", 72, 920, 22, "0x8FA0BC"))
render(os.path.join(OUT, "图3_结算风控.png"), p)
