# -*- coding: utf-8 -*-
"""GEO 选题 · 三张知识贴片（竖版 1080x1920，深色科技风）
安全区：内容 200-1300，1300-1450 留给字幕
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
OUT = "/Users/jiacong/Downloads/剪辑素材/项目/04_GEO大模型收录/02_贴片"

_fc = {}
def font(s, w=6):
    k = (s, w)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONT, s, index=2 if w == 6 else 0)
    return _fc[k]

BG_T, BG_B = (17, 19, 25), (8, 9, 13)
BLUE   = (48, 112, 250)
BLUE_D = (24, 58, 140)
ORANGE = (255, 122, 24)
ORANGE_L = (255, 160, 70)
GREEN  = (34, 197, 94)
GREEN_L = (74, 222, 128)
RED    = (239, 68, 68)
WHITE  = (246, 248, 253)
GRAY   = (150, 160, 178)
DIM    = (104, 114, 132)
CARD   = (14, 16, 23)


def bg():
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / H
        c = tuple(int(BG_T[i] + (BG_B[i] - BG_T[i]) * t) for i in range(3))
        for x in range(0, W, 2):
            px[x, y] = c
            if x + 1 < W: px[x + 1, y] = c
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for y in range(0, H, 6):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 8))
    return Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")


def glow(img, cx, cy, r, color, amt=0.5):
    lay = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(lay).ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    lay = lay.filter(ImageFilter.GaussianBlur(r * 0.6))
    return Image.blend(img, Image.blend(img, lay, 0.75), amt)


def rrect(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def header(img, step, title, sub):
    d = ImageDraw.Draw(img)
    # 步骤徽章
    rrect(d, [84, 250, 260, 306], 28, fill=(255, 122, 24, 255))
    d.text((172, 278), "第 %s 步" % step, font=font(30), fill=(24, 14, 6), anchor="mm")
    d.text((286, 254), "共 3 步", font=font(28), fill=DIM)
    d.text((84, 330), title, font=font(84), fill=WHITE)
    d.text((84, 440), sub, font=font(36), fill=GRAY)


def footer(img, text, color=ORANGE_L):
    by = 1190
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([84, by, 996, by + 118], radius=59,
                                         outline=color + (190,), width=5)
    img = Image.alpha_composite(img.convert("RGBA"), gl.filter(ImageFilter.GaussianBlur(13))).convert("RGB")
    d = ImageDraw.Draw(img)
    rrect(d, [84, by, 996, by + 118], 59, fill=(12, 10, 9), outline=color, width=4)
    d.text((540, by + 59), text, font=font(46), fill=color, anchor="mm")
    return img


# ---------------- 贴片1：逆向工程 ----------------
def card1(t=99):
    img = bg()
    img = glow(img, 880, 340, 420, (26, 70, 190), 0.55)
    img = glow(img, 200, 1180, 400, (150, 66, 20), 0.35)
    d = ImageDraw.Draw(img)
    header(img, "1", "GEO 逆向工程", "看 AI 到底引用了谁")

    # ① 搜索
    y = 530
    d.text((92, y), "① 搜你行业的关键词", font=font(32), fill=BLUE)
    rrect(d, [84, y + 44, 996, y + 132], 16, fill=(22, 25, 34), outline=(48, 60, 92), width=2)
    d.text((114, y + 66), "本地装修公司哪家好？", font=font(34), fill=(214, 220, 234))
    rrect(d, [882, y + 56, 976, y + 120], 12, fill=BLUE)
    d.text((929, y + 88), "搜索", font=font(26), fill=(255, 255, 255), anchor="mm")

    # 箭头
    for yy in [y + 150, ]:
        d.line([540, yy, 540, yy + 34], fill=(90, 100, 120), width=5)
        d.polygon([(525, yy + 28), (555, yy + 28), (540, yy + 46)], fill=(90, 100, 120))

    # ② 引用来源
    y2 = 740
    d.text((92, y2), "② 点开回答下面的「引用来源」", font=font(32), fill=ORANGE_L)
    rrect(d, [84, y2 + 46, 996, y2 + 300], 18, fill=CARD, outline=(74, 52, 30), width=2)
    d.text((114, y2 + 66), "引用来源", font=font(30), fill=ORANGE_L)
    rrect(d, [252, y2 + 64, 300, y2 + 104], 20, fill=ORANGE)
    d.text((276, y2 + 84), "3", font=font(24), fill=(20, 14, 8), anchor="mm")
    srcs = [("知乎", "专栏 · 高权重"), ("公众号", "行业号 · 已收录"), ("行业论坛", "垂直站 · 长尾")]
    for i, (n, s) in enumerate(srcs):
        bx = 108 + i * 296
        rrect(d, [bx, y2 + 126, bx + 276, y2 + 262], 14, fill=(20, 23, 32), outline=(48, 56, 76), width=2)
        d.ellipse([bx + 18, y2 + 176, bx + 58, y2 + 216], fill=BLUE_D, outline=BLUE, width=2)
        d.text((bx + 38, y2 + 196), str(i + 1), font=font(24), fill=BLUE, anchor="mm")
        d.text((bx + 76, y2 + 148), n, font=font(32), fill=WHITE)
        d.text((bx + 76, y2 + 196), s, font=font(21), fill=DIM)

    # ③ 结论
    y3 = 1078
    rrect(d, [84, y3, 996, y3 + 84], 12, fill=(20, 32, 26), outline=GREEN + (150,), width=2)
    d.text((116, y3 + 42), "③ 这三个就是 AI 认可的", font=font(32), fill=GREEN_L, anchor="lm")
    rrect(d, [700, y3 + 20, 950, y3 + 64], 22, fill=GREEN)
    d.text((825, y3 + 42), "高权重信源", font=font(30), fill=(10, 26, 16), anchor="mm")

    return footer(img, "AI 引用谁，你就发到谁那儿", ORANGE_L)


# ---------------- 贴片2：抓取喜好 ----------------
def card2(t=99):
    img = bg()
    img = glow(img, 200, 400, 420, (120, 24, 24), 0.40)
    img = glow(img, 880, 980, 440, (20, 110, 70), 0.42)
    d = ImageDraw.Draw(img)
    header(img, "2", "AI 只抓这两种", "内容质量的判定标准")

    # 错误示范
    y = 520
    rrect(d, [84, y, 996, y + 270], 18, fill=(20, 16, 17), outline=(90, 40, 40), width=2)
    d.ellipse([116, y + 30, 186, y + 100], fill=(58, 22, 22), outline=RED, width=3)
    d.line([136, y + 50, 166, y + 80], fill=RED, width=7)
    d.line([166, y + 50, 136, y + 80], fill=RED, width=7)
    d.text((210, y + 34), "批量 AI 泛文", font=font(46), fill=(240, 200, 200))
    d.text((210, y + 100), "几千篇水文群发，话术雷同", font=font(27), fill=(160, 130, 130))
    rrect(d, [116, y + 156, 964, y + 232], 12, fill=(34, 20, 20))
    d.text((140, y + 194), "AI 判定：噪音 · 不收录 · 拉低权重", font=font(30), fill=(255, 120, 120), anchor="lm")

    # 正确示范
    y2 = 830
    rrect(d, [84, y2, 996, y2 + 270], 18, fill=(14, 22, 18), outline=(34, 110, 70), width=2)
    d.ellipse([116, y2 + 30, 186, y2 + 100], fill=(18, 52, 34), outline=GREEN, width=3)
    d.line([132, y2 + 66, 148, y2 + 84], fill=GREEN, width=7)
    d.line([148, y2 + 84, 172, y2 + 50], fill=GREEN, width=7)
    d.text((210, y2 + 34), "真实优势 + 核心观点", font=font(46), fill=(200, 245, 220))
    d.text((210, y2 + 100), "写你自己的差异化，AI 辅助也要改", font=font(27), fill=(130, 170, 148))
    rrect(d, [116, y2 + 156, 964, y2 + 232], 12, fill=(16, 38, 26))
    d.text((140, y2 + 194), "AI 判定：高权重 · 精准推荐", font=font(30), fill=GREEN_L, anchor="lm")

    return footer(img, "水文越多，AI 越不信你", GREEN_L)


# ---------------- 贴片3：投放矩阵 ----------------
def card3(t=99):
    img = bg()
    img = glow(img, 880, 360, 420, (26, 70, 190), 0.5)
    img = glow(img, 220, 1120, 400, (150, 66, 20), 0.34)
    d = ImageDraw.Draw(img)
    header(img, "3", "投放矩阵", "按体量选路，别乱花钱")

    rows = [
        ("本地中小店", "垂直问答 / 论坛", "自己写，成本 0", "半小时出一篇", BLUE, "1"),
        ("规模化企业", "主流新闻源通发", "几十到百来块一篇", "快速提权", ORANGE, "2"),
    ]
    y = 520
    for name, ch, cost, note, col, idx in rows:
        rrect(d, [84, y, 996, y + 290], 20, fill=CARD, outline=col + (110,), width=2)
        rrect(d, [84, y, 96, y + 290], 6, fill=col)
        d.text((128, y + 34), name, font=font(48), fill=WHITE)
        d.text((128, y + 104), ch, font=font(34), fill=col)
        d.line([128, y + 164, 950, y + 164], fill=(40, 44, 56), width=2)
        d.text((128, y + 190), "成本", font=font(26), fill=DIM)
        d.text((128, y + 226), cost, font=font(38), fill=(214, 222, 236))
        d.text((700, y + 226), note, font=font(28), fill=col)
        y += 330

    return footer(img, "花小钱，占住 AI 推荐位", ORANGE_L)


CARDS = {"c1": card1, "c2": card2, "c3": card3}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, f in CARDS.items():
        f().save(os.path.join(OUT, "预览_%s.png" % k))
    print("ok")
