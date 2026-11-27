# -*- coding: utf-8 -*-
"""批发自动抓单 · 字幕（基于 jrqkm 73.19s 配音）"""
import os

P = "/Users/jiacong/Downloads/剪辑素材/项目/05_批发微信自动抓单"
OUT = os.path.join(P, "_build", "sub_wx.ass")
FONT = "Hiragino Sans GB W6"
SIZE = 76

GOLD   = r"{\c&H6ED6FF&}"
ORANGE = r"{\c&H187AFF&}"
GREEN  = r"{\c&HA0E23C&}"
RED    = r"{\c&H5A5AFF&}"
BIG    = r"\fscx112\fscy112"
RST    = r"{\c&HFFFFFF&\fscx100\fscy100}"

# 【X】金+放大 【G】金 【O】橙 【E】绿 【R】红 【/】复位
CUES = [
    (0.00, 3.62, "今天看到一个做批发生意的", "朋友在网上求助"),
    (3.62, 5.42, "每天盯着电脑上的微信", None),
    (5.42, 9.02, "客户报来鸡蛋【X】20 箱【/】", "调料【X】10 包【/】、蒜米【X】5 斤【/】"),
    (9.02, 11.24, "他得一行行肉眼看", None),
    (11.24, 14.24, "手敲进软件里打印", "【R】眼睛都快看瞎了【/】"),
    (14.24, 17.82, "【R】更头疼的是【/】", "客户只发一句「调料 10 包」"),
    (17.82, 21.02, "具体是哪款调料", "【R】全靠老板脑子记【/】"),
    (21.02, 23.42, "很多人劝他", "找人写复杂的 AI"),
    (23.42, 26.02, "其实解决这个事", "底层逻辑就【O】三步【/】"),
    (26.02, 28.62, "【O】第一步【/】，电脑端", "挂一个微信助手"),
    (28.82, 31.42, "【G】24 小时【/】自动监控聊天记录", None),
    (31.42, 33.62, "客户不管是发文本", "还是发语音"),
    (33.62, 37.62, "自动把商品和数量抓下来", "【E】生成待发清单【/】"),
    (37.62, 40.02, "【O】第二步【/】，解决模糊报单", None),
    (40.02, 42.02, "客户说「【G】调料 10 包【/】」", None),
    (42.02, 45.02, "程序直接翻", "该客户的【G】历史常购记录【/】"),
    (45.02, 47.62, "【E】自动匹配【/】出", "他平时买的具体规格"),
    (47.62, 49.62, "不用老板每次费脑子回忆", None),
    (49.62, 51.82, "【O】第三步【/】，防错闭环", None),
    (51.82, 56.02, "单子生成后", "自动推一条【G】小程序【/】给客户确认"),
    (56.02, 58.82, "或者直接发到老板手机上", "一秒核对"),
    (58.82, 62.82, "核对没问题", "【E】热敏打印机直接自动出单【/】"),
    (62.82, 66.22, "每天手动搬单不仅累", "还容易【R】漏单错单【/】"),
    (66.22, 69.22, "如果有同行也在", "被微信报单折磨"),
    (69.22, 71.82, "想了解这套", "自动抓单的实现流程"),
    (71.82, 73.19, "可以在【G】评论区【/】交流", None),
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
