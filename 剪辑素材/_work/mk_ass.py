# -*- coding: utf-8 -*-
"""生成最终字幕 / 图形 ASS"""
import os

WK = "/Users/jiacong/Downloads/剪辑素材/_work"
FONT = "Heiti SC"
W, H = 1080, 1920

WHITE = r"{\c&HFFFFFF&}"
YELLOW = r"{\c&H4DD2FF&}"   # #FFD24D
DARKTXT = r"\c&H2A1C10&"

O_S3 = 19.40   # uladl 源 -> 全局
O_S5 = 48.96   # mp3 源 -> 全局


def ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def hl(text):
    out, on = [], False
    for ch in text:
        if ch == "【":
            on = True
            out.append(YELLOW)
        elif ch == "】":
            on = False
            out.append(WHITE)
        else:
            out.append(ch)
    return "".join(out)


# (全局起点, 全局终点, 文本, 字号)
CAPS = [
    (0.03, 2.05, "现在做个带私域会员的小程序", 80),
    (2.30, 4.78, r"居然还有老板花【三五万】\N苦等【两个月】？", 80),
    (5.00, 6.82, "听句劝，别再当【大冤种】了！", 80),

    (7.02, 8.06, "很多老板不知道", 80),
    (8.20, 11.28, r"【90%】的商业场景\N根本不用从零写代码", 78),
    (11.80, 13.92, "传统外包不仅贵、上线慢", 80),
    (14.04, 16.60, r"最致命的是——\N只给你一个冷冰冰的页面", 76),
    (17.05, 19.32, r"客户来了就走\N根本留不下数据", 80),

    (O_S3 + 0.28, O_S3 + 2.36, r"你看我们这套\N自研的 SaaS 系统", 78),
    (O_S3 + 2.72, O_S3 + 4.50, r"直接把各行业的\N成熟模板做好了", 78),
    (O_S3 + 4.69, O_S3 + 6.53, r"不用你懂技术\N后台直接拖拽组件", 78),
    (O_S3 + 6.87, O_S3 + 11.75, r"把你的产品、优惠券\N还有私域引流入口\N全都挂上去", 74),
    (O_S3 + 12.29, O_S3 + 15.50, r"半小时就能搭好\N一套你自己的品牌小程序", 76),

    (O_S3 + 15.84, O_S3 + 17.17, "而且它不只是个小程序", 80),
    (O_S3 + 17.44, O_S3 + 19.20, "更是一套【私域抓手】", 80),
    (O_S3 + 19.81, O_S3 + 21.24, "哪个客户进来看了几次", 78),
    (O_S3 + 21.52, O_S3 + 23.12, "点没点活动、领没领券", 78),
    (O_S3 + 23.46, O_S3 + 24.52, "有没有产生交互", 80),
    (O_S3 + 24.77, O_S3 + 26.15, "后台数据【一清二楚】", 80),
    (O_S3 + 26.47, O_S3 + 29.40, r"帮你把每一次流量\N都变成【私域资产】", 78),

    (O_S5 + 0.10, O_S5 + 3.10, r"不管你是做门店、零售\N还是企业服务", 78),
    (O_S5 + 3.30, O_S5 + 6.25, r"想看你的行业\N用这套系统做出来长什么样？", 74),
    (O_S5 + 6.40, O_S5 + 7.90, "评论区留个你的行业", 78),
    (O_S5 + 8.14, O_S5 + 10.45, r"我直接发你体验号\N你自己试！", 78),
]

TAGS = [
    (0.15, 6.80, "01 · 别再被外包坑"),
    (6.95, 19.32, "02 · 为什么这么贵"),
    (19.44, 34.94, "03 · 半小时搭好"),
    (35.05, 48.85, "04 · 私域数据"),
    (48.99, 59.45, "05 · 怎么找我要"),
]

# (起, 止, 第一行, 第二行, 字号, x, an)
H1 = [
    (6.98, 19.30, "传统外包的真相", "贵、慢、留不住客户", 56, 62, 7),
    (19.46, 25.86, "后台直接拖拽", "半小时搭好", 62, 540, 8),
    (25.90, 34.93, "你的品牌小程序", "就长这个样", 62, 540, 8),
    (35.05, 39.94, "不只是小程序", "是一套私域抓手", 56, 62, 7),
    (39.95, 48.85, "谁来了、干了啥", "后台全看得见", 56, 62, 7),
    (49.02, 53.15, "你的行业", "能做成什么样？", 62, 540, 8),
]

CHIPS = [
    (21.60, 25.80, 1170, "01", "各行业成熟模板，直接套用"),
    (23.40, 25.80, 1260, "02", "商品 / 优惠券 / 私域入口"),
    (25.40, 25.80, 1350, "03", "拖拽组装，不用懂代码"),
]

LABELS = [
    (25.90, 28.10, "【校园餐饮】 · 会员优惠券"),
    (28.10, 30.30, "【求职招聘】 · 智能匹配"),
    (30.30, 32.50, "【会展活动】 · 展商服务"),
    (32.50, 34.93, "【大健康】 · 产品陈列"),
]

CTA = (53.20, 59.50, "留个行业，我发你体验号")


def char_w(ch, size):
    if "\u4e00" <= ch <= "\u9fff" or ch in "，。！？、：；“”（）":
        return size * 1.0
    if ch in "·—/":
        return size * 0.5
    if ch.isdigit() or ch.isalpha():
        return size * 0.56
    return size * 0.42


def pill(w, h, r):
    k = r * 0.4477
    return " ".join([
        f"m {r} 0", f"l {w-r} 0",
        f"b {w-r+k} 0 {w} {r-k} {w} {r}",
        f"l {w} {h-r}",
        f"b {w} {h-r+k} {w-r+k} {h} {w-r} {h}",
        f"l {r} {h}",
        f"b {r-k} {h} 0 {h-r+k} 0 {h-r}",
        f"l 0 {r}",
        f"b 0 {r-k} {r-k} 0 {r} 0"])


L = []
L.append("[Script Info]")
L.append("ScriptType: v4.00+")
L.append(f"PlayResX: {W}")
L.append(f"PlayResY: {H}")
L.append("WrapStyle: 2")
L.append("ScaledBorderAndShadow: yes")
L.append("YCbCr Matrix: TV.709")
L.append("")
L.append("[V4+ Styles]")
L.append("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
         "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
         "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding")
L.append(f"Style: Cap,{FONT},80,&H00FFFFFF,&H000000FF,&H00101010,&H00000000,"
         f"-1,0,0,0,100,100,0.8,0,1,6,2,2,40,40,0,1")
L.append(f"Style: Tag,{FONT},36,&H00FFFFFF,&H000000FF,&H00101010,&H00000000,"
         f"-1,0,0,0,100,100,0.6,0,1,3,0,7,0,0,0,1")
L.append(f"Style: H1,{FONT},60,&H00FFFFFF,&H000000FF,&H00101010,&H00000000,"
         f"-1,0,0,0,100,100,1.2,0,1,5,3,7,0,0,0,1")
L.append(f"Style: Chip,{FONT},46,&H00FFFFFF,&H000000FF,&H00101010,&H00000000,"
         f"-1,0,0,0,100,100,0.6,0,1,4,0,7,0,0,0,1")
L.append(f"Style: CTA,{FONT},52,&H00000000,&H000000FF,&H00000000,&H00000000,"
         f"-1,0,0,0,100,100,0.8,0,1,0,0,5,0,0,0,1")
L.append(f"Style: Shape,{FONT},40,&H00000000,&H000000FF,&H00000000,&H00000000,"
         f"0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1")
L.append("")
L.append("[Events]")
L.append("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text")

# --- 顶部章节标签 ---
for st, en, txt in TAGS:
    w = 46 + sum(char_w(c, 36) for c in txt) + 10
    L.append(f"Dialogue: 0,{ts(st)},{ts(en)},Shape,,0,0,0,,"
             f"{{\\an7\\pos(44,92)\\p1\\1c&H2C1A0C&\\1a&H2C&\\bord0\\shad0\\fad(220,160)}}"
             f"{pill(w, 62, 20)}{{\\p0}}")
    L.append(f"Dialogue: 1,{ts(st)},{ts(en)},Tag,,0,0,0,,"
             f"{{\\an7\\pos(67,105)\\fad(220,160)}}{txt}")

def fit(lines, size, limit=980):
    mx = max(sum(char_w(c, size) for c in ln) for ln in lines)
    while mx > limit and size > 40:
        size -= 2
        mx = max(sum(char_w(c, size) for c in ln) for ln in lines)
    return size


# --- H1 主标题 ---
for st, en, l1, l2, size, x, an in H1:
    size = fit([l1, l2], size, 620 if an == 7 else 960)
    L.append(f"Dialogue: 2,{ts(st)},{ts(en)},H1,,0,0,0,,"
             f"{{\\an{an}\\pos({x},{190 if an==8 else 210})\\fs{size}\\fad(280,200)"
             f"\\fscx106\\fscy106\\t(0,180,\\fscx100\\fscy100)}}{l1}\\N{YELLOW}{l2}{WHITE}")

# --- 03 卖点 ---
for st, en, y, num, txt in CHIPS:
    L.append(f"Dialogue: 2,{ts(st)},{ts(en)},Chip,,0,0,0,,"
             f"{{\\an7\\pos(96,{y})\\fad(240,0)}}{YELLOW}{num}{WHITE}   {txt}")

# --- 轮播行业标签 ---
for st, en, txt in LABELS:
    L.append(f"Dialogue: 2,{ts(st)},{ts(en)},H1,,0,0,0,,"
             f"{{\\an8\\pos(540,1382)\\fs48\\c&HFFFFFF&\\bord4.5\\fad(160,120)"
             f"\\fscx94\\fscy94\\t(0,140,\\fscx100\\fscy100)}}{hl(txt)}")

# --- 结尾 CTA ---
st, en, txt = CTA
tw = sum(char_w(c, 52) for c in txt)
pw = int(tw + 96)
L.append(f"Dialogue: 2,{ts(st)},{ts(en)},Shape,,0,0,0,,"
         f"{{\\an7\\pos({(W-pw)//2},996)\\p1\\1c&H4DD2FF&\\1a&H00&\\bord0\\shad0"
         f"\\fad(260,120)\\fscx80\\fscy80\\t(0,220,\\fscx100\\fscy100)}}"
         f"{pill(pw, 112, 56)}{{\\p0}}")
L.append(f"Dialogue: 3,{ts(st)},{ts(en)},CTA,,0,0,0,,"
         f"{{\\an5\\pos({W//2},1052)\\fad(260,120)"
         f"\\fscx80\\fscy80\\t(0,220,\\fscx100\\fscy100)}}{txt}")

# --- 字幕 ---
for st, en, txt, size in CAPS:
    size = fit(txt.split("\\N"), size, 960)
    L.append(f"Dialogue: 4,{ts(st)},{ts(en)},Cap,,0,0,0,,"
             f"{{\\an2\\pos(540,1760)\\fs{size}\\fad(90,0)"
             f"\\fscx104\\fscy104\\t(0,150,\\fscx100\\fscy100)}}{hl(txt)}")

out = os.path.join(WK, "subs.ass")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("wrote", out, len(L), "lines")
