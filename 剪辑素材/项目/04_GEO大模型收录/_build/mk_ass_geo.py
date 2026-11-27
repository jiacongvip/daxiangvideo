# -*- coding: utf-8 -*-
"""GEO 成片字幕"""
import os

P = "/Users/jiacong/Downloads/剪辑素材/项目/04_GEO大模型收录"
OUT = os.path.join(P, "_build", "sub_geo.ass")
FONT = "Hiragino Sans GB W6"
SIZE = 76

GOLD  = r"{\c&H6ED6FF&}"
ORANGE = r"{\c&H187AFF&}"
GREEN = r"{\c&HA0E23C&}"
RED   = r"{\c&H5A5AFF&}"
BIG   = r"\fscx112\fscy112"
RST   = r"{\c&HFFFFFF&\fscx100\fscy100}"

# 【X】金+放大 【G】金 【O】橙 【E】绿 【R】红 【/】复位
CUES = [
    (0.00, 2.98, "千万别再花几万块", "找【R】代运营【/】刷【G】GEO【/】垃圾稿"),
    (3.26, 4.20, "【R】大模型根本不读【/】", None),
    (4.52, 7.64, "今天花一分钟", "把【G】DeepSeek 豆包元宝【/】"),
    (7.66, 10.46, "都在用的【G】GEO【/】核心逻辑", "给你讲透"),
    (11.00, 15.50, "很多人以为做 GEO", "就是用 AI 批量生成几千篇去群发"),
    (15.90, 17.30, "这在今天【R】纯属自嗨【/】", None),
    (17.90, 19.56, "真正的核心", "只有【O】三步【/】"),
    (19.76, 24.56, "【O】第一步【/】，反向逆推信源", "去各大 AI 平台搜行业关键词"),
    (24.92, 29.30, "如果推荐的不是你", "点开回答下面的【G】引用来源【/】"),
    (29.72, 34.12, "看它抓取了", "【G】知乎 公众号 垂直论坛【/】"),
    (34.40, 36.88, "这就是 AI 认可的", "【E】高权重信源【/】"),
    (37.20, 39.22, "【O】第二步【/】，精准定点投放", None),
    (39.80, 41.00, "既然知道它引用谁", None),
    (41.48, 45.04, "就直接去这些被收录的平台", "投放内容"),
    (45.52, 47.58, "记住，千万别发", "【R】纯 AI 废话【/】"),
    (48.04, 52.10, "哪怕找 AI 辅助", "也要写进你的【E】真实优势【/】"),
    (52.20, 54.88, "和【E】核心观点【/】", "【E】AI 才会抓取【/】"),
    (55.30, 57.22, "【O】第三步【/】，低成本放大", None),
    (57.72, 61.24, "本地小店在垂直平台", "发几篇高质量内容就能收录"),
    (61.42, 64.70, "如果是大企业", "【G】几十上百块【/】走新闻发稿渠道"),
    (65.12, 67.30, "直接打穿【G】主流媒体源【/】", None),
]


def hl(s):
    out, on = [], False
    i = 0
    while i < len(s):
        if s[i] == "【":
            j = s.index("】", i)
            tag = s[i + 1:j]
            if tag == "/":
                out.append(RST)
            elif tag == "X":
                out.append(GOLD); out.append("{" + BIG + "}")
            elif tag == "G":
                out.append(GOLD)
            elif tag == "O":
                out.append(ORANGE)
            elif tag == "E":
                out.append(GREEN)
            elif tag == "R":
                out.append(RED)
            i = j + 1
        else:
            out.append(s[i]); i += 1
    return "".join(out)


def ts(t):
    h = int(t // 3600); m = int((t % 3600) // 60); s = t % 60
    return "%d:%02d:%05.2f" % (h, m, s)


head = [
    "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920",
    "WrapStyle: 2", "ScaledBorderAndShadow: yes", "YCbCr Matrix: TV.709", "",
    "[V4+ Styles]",
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
    "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
    "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
    "Style: Sub,%s,%d,&H00FFFFFF,&H000000FF,&H00000000,&H78000000,-1,0,0,0,100,100,1.6,0,1,6,3,2,60,60,462,1" % (FONT, SIZE),
    "", "[Events]",
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
]

lines = []
for i, (s, e, l1, l2) in enumerate(CUES):
    txt = hl(l1) if l2 is None else hl(l1) + r"\N" + hl(l2)
    lines.append("Dialogue: 0,%s,%s,Sub,,0,0,0,,{\\fad(60,60)}%s" % (ts(s), ts(e), txt))

open(OUT, "w", encoding="utf-8").write("\n".join(head + lines) + "\n")
print("ok", len(lines))
