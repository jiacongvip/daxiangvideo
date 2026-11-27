# -*- coding: utf-8 -*-
"""GEO 成片字幕 v2 —— 对齐 03 mk_ass_v5 样式
字体：Hiragino Sans GB W6
三色高亮：金=钱/数字，绿=成功/结果，红=痛点/卡点
重点数字放大 116%
贴片为深色底 → 全程用 Sub（白字），不用 SubD
"""
import os

P = "/Users/jiacong/Downloads/剪辑素材/项目/04_GEO大模型收录"
OUT = os.path.join(P, "_build", "sub_geo_v2.ass")

FONT = "Hiragino Sans GB W6"
SIZE = 80
SIZE_D = 72

GOLD  = r"{\c&H6ED6FF&}"
GREEN = r"{\c&HA0E23C&}"
RED   = r"{\c&H5A5AFF&}"
BIG   = r"\fscx116\fscy116"
RST   = r"{\c&HFFFFFF&\fscx100\fscy100}"

# 【X】=金色放大  【G】=金色  【E】=绿色  【R】=红色  【/】=复位
# 绝对时间轴（与成片一致）；两行用 l2
CUES = [
    # Seg1 face 0.00–10.74
    (0.00, 3.12, "千万别再花【X】几万块【/】", "找代运营刷【R】GEO垃圾稿【/】了"),
    (3.12, 4.50, "大模型根本【R】不读【/】", None),
    (4.50, 7.90, "今天花【X】一分钟【/】把", "【G】DeepSeek、豆包、元宝【/】"),
    (7.90, 10.74, "都在用的【G】GEO核心底层逻辑【/】", "给你讲透"),
    # Seg2 face 10.74–19.65
    (10.74, 15.70, "很多人以为做GEO", "就是用AI【R】批量生成几千篇文章【/】去群发"),
    (15.70, 17.60, "这在今天【R】纯属自嗨【/】", None),
    (17.60, 19.65, "真正的核心只有【X】三步【/】", None),
    # Seg3 card 19.65–37.03
    (19.65, 21.90, "【G】第一步【/】 反向逆推信源", None),
    (21.90, 24.80, "去各大AI平台", "搜你行业的关键词"),
    (24.80, 26.30, "如果推荐的【R】不是你【/】", None),
    (26.30, 29.40, "立刻点开大模型回答下面的", "【G】引用来源【/】"),
    (29.40, 32.50, "看他抓取了【G】知乎、公众号【/】", None),
    (32.50, 34.50, "垂直论坛还是行业站", None),
    (34.50, 37.03, "这就是AI认可的【E】高权重信源【/】", None),
    # Seg4 card 37.03–55.08
    (37.03, 39.40, "【G】第二步【/】 精准定点投放", None),
    (39.40, 41.40, "既然知道它引用谁", None),
    (41.40, 45.30, "我们直接去这些", "【E】被收录的平台【/】上投放内容"),
    (45.30, 47.80, "记住，千万别发【R】纯AI废话【/】", None),
    (47.80, 49.30, "哪怕找AI辅助", None),
    (49.30, 52.40, "也必须写进你的", "【G】真实优势和核心观点【/】"),
    (52.40, 55.08, "【E】真实且有价值【/】的内容", "AI才会抓取"),
    # Seg5 card 55.08–67.49
    (55.08, 57.40, "【G】第三步【/】 低成本放大", None),
    (57.40, 61.40, "【G】本地小店【/】在垂直平台", "发几篇高质量内容就能被收录"),
    (61.40, 65.10, "大企业花【X】几十上百块【/】", "走新闻发稿渠道"),
    (65.10, 67.49, "直接【E】打穿主流媒体源【/】", None),
]


def hl(s, dark=False):
    G_ = GOLD
    E_ = GREEN
    R_ = RED
    RS = RST
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
    # GEO stickers are dark → Sub for all
    txt = hl(l1) if l2 is None else hl(l1) + r"\N" + hl(l2)
    lines.append("Dialogue: 0,%s,%s,Sub,,0,0,0,,{\\fad(70,70)}%s" % (ts(s), ts(e_eff), txt))

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(head + lines) + "\n")
print("ok", len(lines), "→", OUT)
