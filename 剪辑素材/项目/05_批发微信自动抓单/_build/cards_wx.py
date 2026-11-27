# -*- coding: utf-8 -*-
"""批发微信自动抓单 · 三张知识贴片（竖版 1080x1920）
深色底 + 微信绿，安全区：内容 200-1300，1300-1450 留给字幕
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
OUT = "/Users/jiacong/Downloads/剪辑素材/项目/05_批发微信自动抓单/02_贴片"

_fc = {}
def font(s, w=6):
    k = (s, w)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONT, s, index=2 if w == 6 else 1)
    return _fc[k]

BG_T, BG_B = (16, 18, 23), (8, 9, 12)
WX     = (7, 193, 96)      # 微信绿
WX_D   = (5, 90, 52)
BLUE   = (59, 130, 246)
ORANGE = (255, 138, 0)
WHITE  = (245, 247, 250)
GRAY   = (150, 158, 172)
DIM    = (104, 112, 126)
CARD   = (18, 21, 27)
LINE   = (42, 47, 58)


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
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 7))
    return Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")


def glow(img, cx, cy, r, color, amt=0.45):
    lay = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(lay).ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    lay = lay.filter(ImageFilter.GaussianBlur(r * 0.62))
    return Image.blend(img, Image.blend(img, lay, 0.75), amt)


def rrect(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def header(img, step, title, sub):
    d = ImageDraw.Draw(img)
    rrect(d, [84, 250, 268, 306], 28, fill=WX)
    d.text((176, 278), "第 %s 步" % step, font=font(30), fill=(6, 24, 14), anchor="mm")
    d.text((292, 254), "共 3 步", font=font(28), fill=DIM)
    d.text((84, 330), title, font=font(82), fill=WHITE)
    d.text((84, 442), sub, font=font(34), fill=GRAY)


def footer(img, text, color=WX):
    by = 1168
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([84, by, 996, by + 116], radius=58,
                                         outline=color + (170,), width=5)
    img = Image.alpha_composite(img.convert("RGBA"), gl.filter(ImageFilter.GaussianBlur(13))).convert("RGB")
    d = ImageDraw.Draw(img)
    rrect(d, [84, by, 996, by + 116], 58, fill=(10, 14, 12), outline=color, width=4)
    d.text((540, by + 58), text, font=font(44), fill=color, anchor="mm")
    return img


def wechat_window(img, box, bubble, who="客户", t_hl=None):
    """仿微信聊天窗"""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    rrect(d, box, 18, fill=(20, 23, 29), outline=LINE, width=2)
    # 顶栏
    d.rectangle([x0, y0, x1, y0 + 56], fill=(28, 32, 40))
    d.text((x0 + 22, y0 + 16), "批发订货群", font=font(26), fill=(190, 198, 212))
    for i in range(3):
        d.ellipse([x1 - 36 - i * 22, y0 + 22, x1 - 26 - i * 22, y0 + 32], fill=(80, 88, 102))
    # 对方气泡
    by = y0 + 86
    d.ellipse([x0 + 24, by + 2, x0 + 80, by + 58], fill=WX_D)
    d.text((x0 + 52, by + 30), who[0], font=font(24), fill=WX, anchor="mm")
    bx0 = x0 + 96
    bw = min(len(bubble) * 30 + 44, x1 - bx0 - 24)
    rrect(d, [bx0, by, bx0 + bw, by + 92], 12, fill=(38, 42, 50))
    d.text((bx0 + 22, by + 20), bubble, font=font(30), fill=(226, 232, 240))
    return img


def table(img, box, rows, head=("商品", "数量"), hl_row=None):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    rrect(d, box, 16, fill=CARD, outline=LINE, width=2)
    # 表头
    rrect(d, [x0, y0, x1, y0 + 62], 16, fill=(26, 30, 38))
    d.rectangle([x0, y0 + 40, x1, y0 + 62], fill=(26, 30, 38))
    d.text((x0 + 28, y0 + 30), head[0], font=font(26), fill=DIM, anchor="lm")
    d.text((x1 - 28, y0 + 30), head[1], font=font(26), fill=DIM, anchor="rm")
    ry = y0 + 62
    for i, (n, q) in enumerate(rows):
        if i > 0:
            d.line([x0 + 24, ry, x1 - 24, ry], fill=(32, 36, 46), width=1)
        is_hl = (hl_row == i)
        if is_hl:
            d.rounded_rectangle([x0 + 8, ry + 6, x1 - 8, ry + 78], radius=10,
                                fill=(14, 46, 30), outline=WX, width=2)
        d.text((x0 + 30, ry + 42), n, font=font(32), fill=WX if is_hl else WHITE, anchor="lm")
        d.text((x1 - 30, ry + 42), q, font=font(32), fill=WX if is_hl else (206, 214, 228), anchor="rm")
        ry += 88
    return img


# ============ 贴片1：PC 微信自动抓单 ============
def card1(t=99):
    img = bg()
    img = glow(img, 880, 330, 400, (10, 90, 60), 0.5)
    img = glow(img, 200, 1150, 380, (20, 55, 110), 0.35)
    header(img, "1", "自动抓单", "电脑端挂个助手，24 小时盯着")
    img = wechat_window(img, [84, 505, 996, 730], "鸡蛋20箱 调料10包 蒜米5斤")

    d = ImageDraw.Draw(img)
    # 箭头
    d.line([540, 752, 540, 792], fill=WX, width=5)
    d.polygon([(522, 782), (558, 782), (540, 806)], fill=WX)
    d.text((576, 760), "自动识别商品和数量", font=font(28), fill=(140, 210, 170))

    img = table(img, [84, 828, 996, 1152],
                [("鸡蛋", "20 箱"), ("调料", "10 包"), ("蒜米", "5 斤")])
    return footer(img, "不用再一行行肉眼核对了")


# ============ 贴片2：历史常购匹配 ============
def card2(t=99):
    img = bg()
    img = glow(img, 200, 340, 400, (10, 90, 60), 0.45)
    img = glow(img, 900, 1160, 400, (90, 50, 10), 0.35)
    header(img, "2", "模糊报单", "他说「调料10包」，你怎么知道是哪款？")
    img = wechat_window(img, [84, 500, 996, 720], "调料10包", "王老板")

    d = ImageDraw.Draw(img)
    # 箭头 + 说明
    d.line([540, 742, 540, 780], fill=ORANGE, width=5)
    d.polygon([(522, 770), (558, 770), (540, 794)], fill=ORANGE)
    d.text((576, 750), "翻这个客户的历史常购", font=font(28), fill=(240, 175, 110))

    # 历史记录
    x0, y0, x1 = 84, 818, 996
    rrect(d, [x0, y0, x1, y0 + 292], 16, fill=CARD, outline=LINE, width=2)
    d.text((x0 + 26, y0 + 18), "王老板 · 近 3 次常购调料", font=font(26), fill=DIM)
    rows = [("海天金标生抽 500ml", "¥ 8.5"), ("海天生抽 1.9L", "¥ 22"), ("蒸鱼豉油 500ml", "¥ 9.8")]
    for i, (n, p) in enumerate(rows):
        ry = y0 + 64 + i * 74
        hl = (i == 0)
        if hl:
            d.rounded_rectangle([x0 + 10, ry - 6, x1 - 10, ry + 62], radius=10,
                                fill=(12, 44, 28), outline=WX, width=2)
        d.text((x0 + 32, ry + 26), n, font=font(30), fill=WX if hl else (200, 208, 222), anchor="lm")
        d.text((x1 - 32, ry + 26), p, font=font(28), fill=WX if hl else DIM, anchor="rm")

    return footer(img, "自动带出规格，老板不用记")


# ============ 贴片3：防错核对 + 自动打单 ============
def card3(t=99):
    img = bg()
    img = glow(img, 880, 320, 400, (10, 90, 60), 0.45)
    img = glow(img, 200, 1180, 380, (90, 50, 10), 0.32)
    header(img, "3", "防错闭环", "确认过再出单，不漏不错")

    d = ImageDraw.Draw(img)
    steps = [
        ("单子生成", "系统自动整理成待发清单", WX),
        ("推送客户确认", "小程序点一下，或发你手机核对", BLUE),
        ("热敏打印机出单", "核对没问题，直接自动打", ORANGE),
    ]
    y = 500
    for i, (t1, t2, col) in enumerate(steps):
        rrect(d, [84, y, 996, y + 190], 18, fill=CARD, outline=col + (110,), width=2)
        d.rounded_rectangle([84, y, 96, y + 190], radius=6, fill=col)
        d.ellipse([120, y + 57, 196, y + 133], fill=tuple(int(c * 0.18) for c in col) + (255,),
                  outline=col, width=3)
        d.text((158, y + 95), str(i + 1), font=font(42), fill=col, anchor="mm")
        d.text((222, y + 52), t1, font=font(40), fill=WHITE)
        d.text((222, y + 112), t2, font=font(26), fill=GRAY)
        if i < 2:
            d.polygon([(528, y + 194), (552, y + 194), (540, y + 214)], fill=(90, 98, 112))
        y += 224

    return footer(img, "确认过再出单，漏单错单没了", ORANGE)


CARDS = {"c1": card1, "c2": card2, "c3": card3}
DUR = {"c1": 11.61, "c2": 11.97, "c3": 13.81}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, f in CARDS.items():
        f().save(os.path.join(OUT, "预览_%s.png" % k))
    print("ok")
