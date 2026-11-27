# -*- coding: utf-8 -*-
"""成片字幕 v2 —— 字体/样式/高亮全面升级
字体：Hiragino Sans GB W6（冬青黑体粗体）
三色高亮：金=钱/数字，绿=成功/结果，红=痛点/卡点
重点数字放大 116%
"""
import os

P = "/Users/jiacong/Downloads/剪辑素材/项目/03_体检中心推三返一"
OUT = os.path.join(P, "_build", "sub_v5.ass")

FONT = "Hiragino Sans GB W6"
SIZE = 80
SIZE_D = 72

GOLD  = r"{\c&H6ED6FF&}"
GREEN = r"{\c&HA0E23C&}"
RED   = r"{\c&H5A5AFF&}"
BIG   = r"\fscx116\fscy116"
RST   = r"{\c&HFFFFFF&\fscx100\fscy100}"

# 浅底专用（贴片3 那 14 秒）
D_GOLD  = r"{\c&H0078C7&}"
D_GREEN = r"{\c&H4F7900&}"
D_RED   = r"{\c&H2828C6&}"
D_RST   = r"{\c&H202020&\fscx100\fscy100}"

# 【X】=金色放大  【G】=金色  【E】=绿色  【R】=红色  【/】=复位
CUES = [
    (0.00, 2.82, "为什么你做小程序分销", "【R】根本没人【/】愿意帮你推"),
    (2.82, 4.62, "因为你不【G】懂人性【/】", None),
    (4.62, 7.94, "看看我们给一家体检中心", "做的【G】推三返一【/】系统"),
    (7.94, 9.78, "是怎么【G】引爆客流【/】的", None),
    (9.78, 13.50, "他的体检套餐", "一单【X】2000【/】块，【R】很难卖【/】"),
    (13.50, 16.34, "我们帮他在小程序里", "【E】改了个规则【/】"),
    (16.34, 18.98, "凡是下单【X】2000【/】块套餐", "的客户"),
    (18.98, 22.70, "系统直接送他【X】20 张【/】", "低成本的基础小体检卡"),
    (22.70, 24.94, "让他扫码【E】送给家人朋友【/】", None),
    (24.94, 26.66, "朋友拿卡【G】来体验完【/】", None),
    (26.66, 28.58, "只要在平台上【G】消费升级【/】", None),
    (28.58, 30.22, "系统【G】立马启动【/】", None),
    (30.22, 31.26, "【G】推三返一【/】算法", None),
    (31.26, 33.06, "第一单奖励【X】10%【/】", None),
    (33.06, 34.74, "第二单【X】20%【/】", None),
    (34.74, 37.26, "第三单直接给到【X】70%【/】", None),
    (37.26, 38.42, "你【G】品品【/】这个逻辑", None),
    (38.42, 40.58, "【X】20 个【/】朋友免费领了卡", None),
    (40.58, 42.06, "只要有【X】3 个人【/】转化", None),
    (42.06, 44.90, "老客户这【X】2000【/】块", "就直接【E】免单回本【/】"),
    (44.90, 46.86, "尤其是卡在【R】第二单【/】的时候", None),
    (46.86, 49.02, "为了拿第三单那【X】70%【/】", None),
    (49.02, 51.66, "客户自己都会【R】拼命【/】", "帮你催朋友下单"),
    (51.66, 54.54, "想把这套【G】裂变模型【/】", "装进你的小程序里吗？"),
    (54.54, 56.86, "【G】评论区【/】告诉我你的行业", None),
    (56.86, 59.14, "我发你系统后台【E】自己试【/】", None),
]


def hl(s, dark=False):
    G_ = D_GOLD if dark else GOLD
    E_ = D_GREEN if dark else GREEN
    R_ = D_RED if dark else RED
    RS = D_RST if dark else RST
    out, on = [], None
    i = 0
    while i < len(s):
        if s[i] == "【":
            j = s.index("】", i)
            tag = s[i + 1:j]
            if tag == "/":
                out.append(RS); on = None
            elif tag == "X":
                out.append(G_); out.append("{" + BIG + "}"); on = tag
            elif tag == "G":
                out.append(G_); on = tag
            elif tag == "E":
                out.append(E_); on = tag
            elif tag == "R":
                out.append(R_); on = tag
            i = j + 1
        else:
            out.append(s[i]); i += 1
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
    "Style: Sub,%s,%d,&H00FFFFFF,&H000000FF,&H00000000,&H78000000,-1,0,0,0,100,100,1.6,0,1,6,3,2,60,60,462,1" % (FONT, SIZE),
    "Style: SubD,%s,%d,&H00202020,&H000000FF,&H00FFFFFF,&H00FFFFFF,-1,0,0,0,100,100,1.6,0,1,5,2,2,60,60,470,1" % (FONT, SIZE_D),
    "",
    "[Events]",
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]

lines = []
for i, (s, e, l1, l2) in enumerate(CUES):
    e_eff = min(CUES[i + 1][0] - 0.02, e) if i + 1 < len(CUES) else e
    if e_eff <= s:
        e_eff = s + 0.6
    dark = (s >= 37.0 and s < 51.6)
    txt = hl(l1, dark) if l2 is None else hl(l1, dark) + r"\N" + hl(l2, dark)
    st = "SubD" if dark else "Sub"
    lines.append("Dialogue: 0,%s,%s,%s,,0,0,0,,{\\fad(70,70)}%s" % (ts(s), ts(e_eff), st, txt))

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(head + lines) + "\n")
print("ok", len(lines))
