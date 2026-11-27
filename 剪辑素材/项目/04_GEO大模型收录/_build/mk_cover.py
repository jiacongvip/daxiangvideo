# -*- coding: utf-8 -*-
"""GEO 选题 · 竖版封面（深灰 + 科技蓝 + 霓虹橙）"""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
OUT = "/Users/jiacong/Downloads/剪辑素材/项目/04_GEO大模型收录/04_成片"

_fc = {}
def font(s, w=6):
    k = (s, w)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONT, s, index=2 if w == 6 else 0)
    return _fc[k]

BG_T, BG_B = (17, 19, 25), (7, 8, 12)
BLUE   = (48, 112, 250)
BLUE_D = (24, 58, 140)
ORANGE = (255, 122, 24)
ORANGE_L = (255, 160, 70)
WHITE  = (246, 248, 253)
GRAY   = (150, 160, 178)
DIM    = (108, 118, 136)


def bg():
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        t = y / H
        c = tuple(int(BG_T[i] + (BG_B[i] - BG_T[i]) * t) for i in range(3))
        for x in range(0, W, 2):
            px[x, y] = c
            if x + 1 < W: px[x + 1, y] = c
    return img


def glow(img, cx, cy, r, color, amt=0.55):
    lay = Image.new("RGB", (W, H), (0, 0, 0))
    ImageDraw.Draw(lay).ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    lay = lay.filter(ImageFilter.GaussianBlur(r * 0.6))
    return Image.blend(img, Image.blend(img, lay, 0.75), amt)


def scanlines(img, step=6, alpha=10):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, alpha))
    return Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")


def rrect(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def ai_card(img, box):
    x0, y0, x1, y1 = box
    # 外发光
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle(box, radius=24, outline=BLUE + (160,), width=4)
    img = Image.alpha_composite(img.convert("RGBA"), gl.filter(ImageFilter.GaussianBlur(16))).convert("RGB")
    d = ImageDraw.Draw(img)
    rrect(d, box, 24, fill=(13, 15, 22), outline=(44, 86, 190), width=2)

    # 搜索框
    sb = [x0 + 26, y0 + 26, x1 - 26, y0 + 100]
    rrect(d, sb, 14, fill=(24, 27, 37), outline=(52, 58, 74), width=2)
    d.text((sb[0] + 24, sb[1] + 24), "本地装修公司哪家好？", font=font(30), fill=(214, 220, 234))
    # 光标
    cx = sb[0] + 24 + font(30).getbbox("本地装修公司哪家好？")[2] + 4
    d.line([cx, sb[1] + 22, cx, sb[1] + 54], fill=BLUE, width=3)
    # 搜索键
    rrect(d, [sb[2] - 76, sb[1] + 12, sb[2] - 12, sb[3] - 12], 10, fill=BLUE)
    d.text((sb[2] - 44, (sb[1] + sb[3]) / 2), "问", font=font(28), fill=(255, 255, 255), anchor="mm")

    # 回答区（灰条模拟）
    ay = y0 + 128
    d.text((x0 + 26, ay), "AI 回答", font=font(24), fill=DIM)
    ay += 42
    for i, wd in enumerate([760, 830, 700, 560]):
        d.rounded_rectangle([x0 + 26, ay, x0 + 26 + wd, ay + 20], radius=10, fill=(38, 42, 54))
        ay += 38

    # 引用来源区（重点）
    cy = ay + 26
    d.line([x0 + 26, cy - 10, x1 - 26, cy - 10], fill=(38, 44, 58), width=2)
    d.text((x0 + 26, cy + 6), "引用来源", font=font(28), fill=ORANGE_L)
    rrect(d, [x0 + 152, cy + 4, x0 + 196, cy + 40], 18, fill=ORANGE)
    d.text((x0 + 174, cy + 22), "3", font=font(24), fill=(20, 14, 8), anchor="mm")

    srcs = [("知乎", "专栏 · 高权重"), ("公众号", "行业号 · 已收录"), ("行业论坛", "垂直站 · 长尾")]
    for i, (n, s) in enumerate(srcs):
        bw = 250 if i == 2 else 286
        bx = x0 + 26 + (i % 3) * 306
        by = cy + 62
        rrect(d, [bx, by, bx + bw, by + 96], 12, fill=(20, 23, 32), outline=(46, 52, 68), width=2)
        d.ellipse([bx + 16, by + 30, bx + 52, by + 66], fill=BLUE_D, outline=BLUE, width=2)
        d.text((bx + 34, by + 48), str(i + 1), font=font(22), fill=BLUE, anchor="mm")
        d.text((bx + 68, by + 22), n, font=font(28), fill=WHITE)
        d.text((bx + 68, by + 58), s, font=font(20), fill=DIM)
    return img


def build():
    img = bg()
    img = glow(img, 180, 240, 480, (26, 70, 190), 0.62)
    img = glow(img, 900, 1500, 520, (150, 60, 20), 0.42)
    img = scanlines(img)
    d = ImageDraw.Draw(img)

    # 顶部标签
    d.rounded_rectangle([84, 250, 92, 288], radius=4, fill=ORANGE)
    d.text((114, 244), "GEO  ·  大模型收录的底层逻辑", font=font(30), fill=(178, 190, 210))

    # 主标题
    d.text((80, 328), "别被 GEO", font=font(122), fill=WHITE)
    d.text((80, 470), "割韭菜了", font=font(146), fill=ORANGE)

    # 副标
    d.text((84, 656), "花几万发水文，AI 根本不读", font=font(42), fill=(198, 208, 226))

    # AI 卡片
    img = ai_card(img, [84, 760, 996, 1390])
    d = ImageDraw.Draw(img)

    # 放大镜（指向"引用来源"）
    mx, my = 896, 1332
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gl).ellipse([mx - 44, my - 44, mx + 44, my + 44], outline=ORANGE + (180,), width=8)
    img = Image.alpha_composite(img.convert("RGBA"), gl.filter(ImageFilter.GaussianBlur(10))).convert("RGB")
    d = ImageDraw.Draw(img)
    d.ellipse([mx - 42, my - 42, mx + 42, my + 42], outline=ORANGE, width=7)
    d.line([mx + 30, my + 30, mx + 66, my + 66], fill=ORANGE, width=11)
    d.line([mx - 17, my, mx + 17, my], fill=(255, 220, 190), width=5)

    # 底部条
    by = 1446
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([84, by, 996, by + 128], radius=64, outline=ORANGE + (200,), width=5)
    img = Image.alpha_composite(img.convert("RGBA"), gl.filter(ImageFilter.GaussianBlur(14))).convert("RGB")
    d = ImageDraw.Draw(img)
    rrect(d, [84, by, 996, by + 128], 64, fill=(14, 10, 8), outline=ORANGE, width=4)
    d.text((540, by + 64), "3 步逆向，查出高权重信源", font=font(52), fill=ORANGE_L, anchor="mm")

    return img


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    im = build()
    im.save(f"{OUT}/封面_1080x1920.png")
    im.crop((0, 240, 1080, 1680)).save(f"{OUT}/封面_1080x1440_抖音.png")
    print("ok")
