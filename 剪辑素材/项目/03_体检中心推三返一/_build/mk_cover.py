# -*- coding: utf-8 -*-
"""体检中心案例 · 竖版封面（深色科技风，配色取自老板给的参考图）"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
OUT = "/Users/jiacong/Downloads/剪辑素材/项目/03_体检中心推三返一/04_成片"

_fc = {}
def font(s):
    if s not in _fc: _fc[s] = ImageFont.truetype(FONT, s)
    return _fc[s]

NAVY   = (4, 16, 48)
PURPLE = (30, 6, 72)
GOLD1, GOLD2, GOLD3 = (255, 245, 205), (240, 194, 74), (214, 155, 30)
WHITE  = (246, 248, 255)
SUB    = (168, 182, 214)
BLUE   = (54, 130, 246)
VIOLET = (150, 90, 255)


def grad_bg(size):
    w, h = size
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        for x in range(0, w, 4):
            t = (x / w * 0.45 + y / h * 0.55)
            r = int(NAVY[0] + (PURPLE[0] - NAVY[0]) * t)
            g = int(NAVY[1] + (PURPLE[1] - NAVY[1]) * t)
            b = int(NAVY[2] + (PURPLE[2] - NAVY[2]) * t)
            for k in range(4):
                if x + k < w: px[x + k, y] = (r, g, b)
    return img


def add_glow(img, cx, cy, rad, color, strength=90):
    lay = Image.new("RGB", img.size, (0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=color)
    lay = lay.filter(ImageFilter.GaussianBlur(rad * 0.55))
    return Image.blend(img, Image.blend(img, lay, 0.55), strength / 255.0)


def add_grid(img, step=90, alpha=16):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for x in range(0, W, step): d.line([(x, 0), (x, H)], fill=(120, 160, 255, alpha))
    for y in range(0, H, step): d.line([(0, y), (W, y)], fill=(120, 160, 255, alpha))
    img.paste(Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB"), (0, 0))


def gold_text(img, xy, s, size, anchor="la", glow=True):
    """金色渐变字"""
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).text(xy, s, font=font(size), fill=255, anchor=anchor)
    grad = Image.new("RGBA", img.size, (0, 0, 0, 255))
    gp = grad.load()
    bbox = mask.getbbox()
    y0, y1 = bbox[1], bbox[3]
    for y in range(img.size[1]):
        t = max(0.0, min(1.0, (y - y0) / max(1, (y1 - y0))))
        if t < 0.5:
            k = t / 0.5
            c = tuple(int(GOLD1[i] + (GOLD2[i] - GOLD1[i]) * k) for i in range(3))
        else:
            k = (t - 0.5) / 0.5
            c = tuple(int(GOLD2[i] + (GOLD3[i] - GOLD2[i]) * k) for i in range(3))
        for x in range(0, img.size[0], 2):
            gp[x, y] = c + (255,)
            if x + 1 < img.size[0]: gp[x + 1, y] = c + (255,)
    if glow:
        halo = Image.new("RGBA", img.size, (0, 0, 0, 255))
        halo.paste((255, 190, 60, 255), (0, 0), mask)
        halo = halo.filter(ImageFilter.GaussianBlur(16))
        img.paste(Image.blend(img, Image.blend(img, halo, 0.5), 0.45), (0, 0))
    img.paste(grad, (0, 0), mask)


def card(img, box, accent, title, sub, badge):
    x0, y0, x1, y1 = box
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle(box, radius=18, fill=(12, 22, 54, 240))
    img.alpha_composite(lay)
    gl = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle(box, radius=18, outline=accent + (200,), width=3)
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, radius=18, outline=accent + (240,), width=3)
    # 左侧徽章：深底 + 彩色描边 + 彩色字
    bx0, bx1 = x0 + 24, x0 + 138
    d.rounded_rectangle([bx0, y0 + 28, bx1, y1 - 28], radius=12,
                        fill=tuple(int(c * 0.20) for c in accent) + (255,),
                        outline=accent + (255,), width=2)
    d.text(((bx0 + bx1) / 2, (y0 + y1) / 2), badge, font=font(40), fill=accent + (255,), anchor="mm")
    d.text((x0 + 166, y0 + 34), title, font=font(52), fill=WHITE + (255,))
    d.text((x0 + 166, y0 + 104), sub, font=font(29), fill=SUB + (255,))


def build():
    base = grad_bg((W, H))
    base = add_glow(base, 300, 220, 420, (20, 70, 190), 120)
    base = add_glow(base, 860, 1520, 460, (90, 20, 150), 110)
    add_grid(base)
    img = base.convert("RGBA")
    d = ImageDraw.Draw(img)

    # 顶部标签
    d.rounded_rectangle([84, 250, 92, 288], radius=4, fill=(240, 194, 74, 255))
    d.text((114, 244), "体检中心  ·  真实裂变案例", font=font(33), fill=(196, 208, 235, 255))

    # 主标题
    gold_text(img, (84, 330), "一单 2000", 140)
    d = ImageDraw.Draw(img)
    d.text((84, 492), "送出去 20 张卡", font=font(104), fill=WHITE + (255,))

    # 三张卡
    x0, x1 = 84, 996
    ys = [672, 894, 1116]
    hs = 176
    items = [
        (GOLD1, "¥2000 体检套餐", "单卖很难动，客户嫌贵", "¥"),
        (BLUE, "× 20 张基础体检卡", "专属二维码，一键转赠亲友", "20"),
        (VIOLET, "亲友扫码领取", "后台自动绑定上下级关系", "扫"),
    ]
    for (acc, t, s, b), y in zip(items, ys):
        card(img, [x0, y, x1, y + hs], acc, t, s, b)
        if y != ys[-1]:
            cy = y + hs + 8
            d.polygon([(540 - 15, cy + 2), (540 + 15, cy + 2), (540, cy + 24)], fill=(130, 152, 200, 255))

    # 底部结论
    by = 1382
    gl = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([84, by, 996, by + 132], radius=66, outline=(255, 210, 90, 210), width=5)
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(14)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([84, by, 996, by + 132], radius=66, fill=(10, 14, 44, 235), outline=(255, 210, 90, 255), width=4)
    gold_text(img, (540, by + 66), "3 个人转化  →  2000 全退", 62, anchor="mm", glow=False)

    return img.convert("RGB")


if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    im = build()
    im.save(f"{OUT}/封面_1080x1920.png")
    im.crop((0, 240, 1080, 1680)).save(f"{OUT}/封面_1080x1440_抖音.png")
    print("ok")
