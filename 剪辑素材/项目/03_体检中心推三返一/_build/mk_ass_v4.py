# -*- coding: utf-8 -*-
"""成片 v4 字幕（ASS）
安全区：字幕底线 1458，字号 72，双行，白字黑描边，数字金色
"""
import os

P = "/Users/jiacong/Downloads/剪辑素材/项目/03_体检中心推三返一"
OUT = os.path.join(P, "_build", "sub_v4.ass")

FONT = "Heiti SC"
SIZE = 72
GOLD = r"{\c&H6ED6FF&}"      # RGB(255,214,110)
WHITE = r"{\c&HFFFFFF&}"

# (start, end, 行1, 行2 或 None)  【】内为高亮
CUES = [
    (0.00, 2.82, "为什么你做小程序分销", "根本没人愿意帮你推"),
    (2.82, 4.62, "因为你不懂人性", None),
    (4.62, 7.94, "看看我们给一家体检中心", "做的推三返一系统"),
    (7.94, 9.78, "是怎么引爆客流的", None),
    (9.78, 13.50, "他的体检套餐", "一单【2000】块，很难卖"),
    (13.50, 16.34, "我们帮他在小程序里", "改了个规则"),
    (16.34, 18.98, "凡是下单【2000】块套餐", "的客户"),
    (18.98, 22.70, "系统直接送他【20 张】", "低成本的基础小体检卡"),
    (22.70, 24.94, "让他扫码送给家人朋友", None),
    (24.94, 26.66, "朋友拿卡来体验完", None),
    (26.66, 28.58, "只要在平台上消费升级", None),
    (28.58, 30.22, "系统立马启动", None),
    (30.22, 31.26, "推三返一算法", None),
    (31.26, 33.06, "第一单奖励【10%】", None),
    (33.06, 34.74, "第二单【20%】", None),
    (34.74, 37.26, "第三单直接给到【70%】", None),
    (37.26, 38.42, "你品品这个逻辑", None),
    (38.42, 40.58, "【20 个】朋友免费领了卡", None),
    (40.58, 42.06, "只要有【3 个人】转化", None),
    (42.06, 44.90, "老客户这【2000】块", "就直接免单回本"),
    (44.90, 46.86, "尤其是卡在第二单的时候", None),
    (46.86, 49.02, "为了拿第三单那【70%】", None),
    (49.02, 51.66, "客户自己都会拼命", "帮你催朋友下单"),
    (51.66, 54.54, "想把这套裂变模型", "装进你的小程序里吗？"),
    (54.54, 56.86, "评论区告诉我你的行业", None),
    (56.86, 59.14, "我发你系统后台自己试", None),
]


def hl(s):
    out, on = [], False
    for ch in s:
        if ch == "【":
            on = True; out.append(GOLD)
        elif ch == "】":
            on = False; out.append(WHITE)
        else:
            out.append(ch)
    return "".join(out)


def ts(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return "%d:%02d:%05.2f" % (h, m, s)


head = [
    "[Script Info]",
    "ScriptType: v4.00+",
    "PlayResX: 1080",
    "PlayResY: 1920",
    "WrapStyle: 2",
    "ScaledBorderAndShadow: yes",
    "YCbCr Matrix: TV.709",
    "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
    "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
    "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: Sub,%s,%d,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,1.2,0,1,5,2,2,70,70,462,1" % (FONT, SIZE),
    "",
    "[Events]",
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]

lines = []
for i, (s, e, l1, l2) in enumerate(CUES):
    e_eff = CUES[i + 1][0] - 0.02 if i + 1 < len(CUES) else e
    e_eff = min(e_eff, e) if i + 1 < len(CUES) else e
    if e_eff <= s:
        e_eff = s + 0.6
    txt = hl(l1) if l2 is None else hl(l1) + r"\N" + hl(l2)
    lines.append("Dialogue: 0,%s,%s,Sub,,0,0,0,,%s{\\fad(60,60)}" % (ts(s), ts(e_eff), txt))
    # 注：fad 需放在文本前，这里重排
    lines[-1] = "Dialogue: 0,%s,%s,Sub,,0,0,0,,{\\fad(60,60)}%s" % (ts(s), ts(e_eff), txt)

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(head + lines) + "\n")
print("写好了", OUT, len(lines), "条")
