# -*- coding: utf-8 -*-
"""字幕 / 标题 / 标签 / CTA"""
import json, os

P = "/Users/jiacong/Downloads/剪辑素材/项目/02_鸡蛋配送案例"
WK = os.path.join(P, "_build")
FONT = "Heiti SC"
W, H = 1080, 1920
WHITE = r"{\c&HFFFFFF&}"
YELLOW = r"{\c&H4DD2FF&}"

TL = {int(k): v for k, v in json.load(open(os.path.join(WK, "timeline.json"))).items()}
END = 81.11


def S(i):
    return TL[i][0]


def E(i):
    return TL[i][1]


def ts(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def hl(t):
    out, on = [], False
    for ch in t:
        if ch == "【":
            on = True; out.append(YELLOW)
        elif ch == "】":
            on = False; out.append(WHITE)
        else:
            out.append(ch)
    return "".join(out)


# 字幕：(句号, 文本)  句内用 \N 分行
CAPS = [
    (1, r"在一个城市光靠卖鸡蛋\N一年能干到 1 个多亿？"),
    (2, r"这是我们真实服务的\N一家同城配送客户"),
    (3, r"很多老板问我\N他怎么管好几千家门店和车队"),
    (4, r"核心就靠这套定制的\N同城 B2B 配送系统"),
    (5, r"第一，业务员跑市场神器"),
    (6, r"做批发最怕价格乱\N系统支持【阶梯价】\N新老客户「一客一价」"),
    (7, r"不会用手机的餐饮老板\N业务员手机直接「代客下单」\N业绩自动算提成"),
    (8, r"第二，把配送成本压到极致"),
    (9, r"每天几千单怎么送\N系统按【配送批次】汇总\N给司机做最优【路径规划】"),
    (10, r"过去人工排线要两小时\N现在几秒发到【配送员系统】"),
    (11, r"第三，最头疼的烂账和丢筐"),
    (12, r"餐饮店习惯「记账月结」\N送鸡蛋每次都要押筐退筐"),
    (13, r"系统里有【退筐结算】\N和月结对账\N送货、退筐、欠款一目了然"),
    (14, r"做生鲜、冻品、酒水\N或同城批发的老板\N想看后台长什么样？"),
    (15, r"评论区留个「配送」\N我发你演示号自己试"),
]

TAGS = [
    (1, "真实客户案例 · 已脱敏", E(5)),
    (6, "01 价格与拓客", E(7)),
    (14, "04 怎么看后台", END),
]

# 全屏段的大字（句, 主行, 副行, 起, 止）
BIG = [
    (4, "一套系统", "管完整个生意", S(4), E(5)),
    (8, "02 配送", "批次 · 路线 · 司机", S(8), E(8)),
    (11, "03 结算", "筐和账，最容易漏", S(11), E(11)),
    (14, "你的行业", "能做成什么样？", S(14), 73.10),
]

CTA = (S(15) + 0.2, END - 0.1, "留个「配送」，我发你体验号")


def char_w(ch, size):
    if "\u4e00" <= ch <= "\u9fff" or ch in "，。！？、：；“”（）「」":
        return size * 1.0
    if ch in "·—/":
        return size * 0.5
    if ch.isdigit() or ch.isalpha():
        return size * 0.56
    return size * 0.42


def fit(lines, size, limit=980):
    mx = max(sum(char_w(c, size) for c in ln) for ln in lines)
    while mx > limit and size > 40:
        size -= 2
    # 重新计算
        mx = max(sum(char_w(c, size) for c in ln) for ln in lines)
    return size


def pill(w, h, r):
    k = r * 0.4477
    return " ".join([f"m {r} 0", f"l {w-r} 0",
                     f"b {w-r+k} 0 {w} {r-k} {w} {r}", f"l {w} {h-r}",
                     f"b {w} {h-r+k} {w-r+k} {h} {w-r} {h}", f"l {r} {h}",
                     f"b {r-k} {h} 0 {h-r+k} 0 {h-r}", f"l 0 {r}",
                     f"b 0 {r-k} {r-k} 0 {r} 0"])


L = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
     "WrapStyle: 2", "ScaledBorderAndShadow: yes", "YCbCr Matrix: TV.709", "",
     "[V4+ Styles]",
     "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
     "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
     "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
     f"Style: Cap,{FONT},80,&H00FFFFFF,&H000000FF,&H00101010,&H00000000,-1,0,0,0,100,100,0.8,0,1,6,2,2,40,40,0,1",
     f"Style: Tag,{FONT},32,&H00FFFFFF,&H000000FF,&H00101010,&H00000000,-1,0,0,0,100,100,0.6,0,1,3,0,7,0,0,0,1",
     f"Style: Big,{FONT},64,&H00FFFFFF,&H000000FF,&H00101010,&H00000000,-1,0,0,0,100,100,1.5,0,1,6,3,8,0,0,0,1",
     f"Style: CTA,{FONT},50,&H00000000,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0.8,0,1,0,0,5,0,0,0,1",
     f"Style: Shape,{FONT},40,&H00000000,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
     "", "[Events]",
     "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]

# 顶部标签（全屏段带底板，截图段直接文字）
for sid, txt, end in TAGS:
    st = S(sid) + 0.05
    if sid in (1,):
        w = 40 + sum(char_w(c, 32) for c in txt) + 8
        L.append(f"Dialogue: 0,{ts(st)},{ts(end)},Shape,,0,0,0,,"
                 f"{{\\an7\\pos(44,150)\\p1\\1c&H2C1A0C&\\1a&H2C&\\bord0\\shad0\\fad(200,150)}}"
                 f"{pill(w, 56, 18)}{{\\p0}}")
        L.append(f"Dialogue: 1,{ts(st)},{ts(end)},Tag,,0,0,0,,"
                 f"{{\\an7\\pos(64,162)\\fad(200,150)}}{txt}")
    else:
        L.append(f"Dialogue: 0,{ts(st)},{ts(end)},Shape,,0,0,0,,"
                 f"{{\\an7\\pos(60,158)\\p1\\1c&H4DD2FF&\\bord0\\shad0\\fad(220,160)}}"
                 f"{pill(10, 40, 4)}{{\\p0}}")
        L.append(f"Dialogue: 1,{ts(st)},{ts(end)},Tag,,0,0,0,,"
                 f"{{\\an7\\pos(86,158)\\fs34\\c&HFFFFFF&\\fad(220,160)}}{txt}")

# 大字
for sid, l1, l2, st, en in BIG:
    L.append(f"Dialogue: 2,{ts(st)},{ts(en)},Big,,0,0,0,,"
             f"{{\\an7\\pos(62,252)\\fad(240,180)\\fscx108\\fscy108"
             f"\\t(0,200,\\fscx100\\fscy100)}}{l1}\\N{YELLOW}{l2}{WHITE}")

# CTA
st, en, txt = CTA
tw = sum(char_w(c, 50) for c in txt)
pw = int(tw + 90)
L.append(f"Dialogue: 2,{ts(st)},{ts(en)},Shape,,0,0,0,,"
         f"{{\\an7\\pos({(W-pw)//2},900)\\p1\\1c&H4DD2FF&\\1a&H00&\\bord0\\shad0"
         f"\\fad(260,120)\\fscx80\\fscy80\\t(0,220,\\fscx100\\fscy100)}}"
         f"{pill(pw, 108, 54)}{{\\p0}}")
L.append(f"Dialogue: 3,{ts(st)},{ts(en)},CTA,,0,0,0,,"
         f"{{\\an5\\pos({W//2},954)\\fad(260,120)\\fscx80\\fscy80"
         f"\\t(0,220,\\fscx100\\fscy100)}}{txt}")

# 字幕
for sid, txt in CAPS:
    size = fit(txt.split("\\N"), 70, 900)
    L.append(f"Dialogue: 4,{ts(S(sid))},{ts(E(sid))},Cap,,0,0,0,,"
             f"{{\\an2\\pos(540,1450)\\fs{size}\\fad(90,0)"
             f"\\fscx104\\fscy104\\t(0,150,\\fscx100\\fscy100)}}{hl(txt)}")

p = os.path.join(WK, "subs.ass")
open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("wrote", p, len(L))
