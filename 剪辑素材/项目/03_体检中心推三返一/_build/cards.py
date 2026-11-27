# -*- coding: utf-8 -*-
"""体检中心「推三返一」三张贴片 · 渲染库
1080x1920 / 25fps / 浅色系，延续 02 项目视觉语言
安全区：视觉主体 380-1280；y>1300 留给字幕，贴片不放东西
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"

BG    = (245, 246, 248)
INK   = (15, 23, 42)
GRAY  = (100, 116, 139)
LGRAY = (203, 213, 225)
WHITE = (255, 255, 255)
BLUE  = (37, 99, 235)
GREEN = (16, 185, 129)
RED   = (239, 68, 68)
AMBER = (245, 158, 11)

_fc = {}
def font(size):
    if size not in _fc:
        _fc[size] = ImageFont.truetype(FONT, size)
    return _fc[size]

def text(d, xy, s, size, color, anchor="lt"):
    d.text(xy, s, font=font(size), fill=color, anchor=anchor)

def tw(s, size):
    b = font(size).getbbox(s)
    return b[2] - b[0]

def clamp01(t): return max(0.0, min(1.0, t))
def seg(t, a, b):
    if b <= a: return 1.0 if t >= b else 0.0
    return clamp01((t - a) / (b - a))
def ease_out(t):
    t = clamp01(t); return 1 - (1 - t) ** 3
def ease_io(t):
    t = clamp01(t); return 3 * t * t - 2 * t * t * t
def back_out(t):
    t = clamp01(t) - 1
    return 1 + 2.7 * t ** 3 + 1.7 * t ** 2
def A(color, a):
    return (color[0], color[1], color[2], int(255 * clamp01(a)))

def shadow(img, box, r, blur=16, off=(0, 6), opacity=0.10):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([box[0] + off[0], box[1] + off[1], box[2] + off[0], box[3] + off[1]],
                        radius=r, fill=(15, 23, 42, int(255 * opacity)))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))

def canvas(): return Image.new("RGBA", (W, H), BG + (255,))

def header(img, tag, title_lines, sub=None, t=0, dy=0):
    d = ImageDraw.Draw(img)
    a1 = ease_out(seg(t, 0.00, 0.45))
    a2 = ease_out(seg(t, 0.10, 0.65))
    a3 = ease_out(seg(t, 0.35, 0.95))
    X = 90
    if a1 > 0:
        d.rounded_rectangle([X, 206 + dy, X + 8, 240 + dy], radius=4, fill=A(BLUE, a1))
        text(d, (X + 26, 198 + dy), tag, 32, A(GRAY, a1))
    y = 272 + dy
    for i, ln in enumerate(title_lines):
        if a2 > 0:
            text(d, (X, y + i * 104), ln, 86, A(INK, a2))
    y += len(title_lines) * 104 + 12
    if sub and a3 > 0:
        text(d, (X, y), sub, 34, A(GRAY, a3))
    return y + (52 if sub else 0)


# ============ 贴片 1：1 拖 20（9.48–24.65，15.17s） ============
def card1(t):
    img = canvas(); d = ImageDraw.Draw(img)
    header(img, "CASE 02  ·  体检中心", ["一单 2000", "送出去 20 张卡"], None, t)

    # 大卡：¥2000 套餐（1.4s 起）
    a = ease_out(seg(t, 1.4, 2.2))
    if a > 0:
        sc = 0.94 + 0.06 * a
        w, h = 880 * sc, 156 * sc
        cx, cy = 540, 580
        box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
        shadow(img, box, 18, opacity=0.10 * a)
        d.rounded_rectangle(box, radius=18, fill=A(WHITE, a), outline=A(LGRAY, a), width=2)
        text(d, (box[0] + 44, cy - 60), "体检套餐 · 单次", 32, A(GRAY, a))
        text(d, (box[0] + 42, cy - 14), "¥2000", 66, A(INK, a))
        a_lb = ease_out(seg(t, 3.5, 3.9))
        if a_lb > 0:
            lb = "下单即送"
            lw = tw(lb, 30) + 44
            d.rounded_rectangle([box[2] - lw - 40, cy - 24, box[2] - 40, cy + 24],
                                radius=24, fill=A(RED, a_lb))
            text(d, (box[2] - lw / 2 - 40, cy), lb, 30, A(WHITE, a_lb), anchor="mm")

    # 转折说明：先「很难卖」，再「改个规则」
    a_old = ease_out(seg(t, 1.9, 2.4)) * (1 - ease_out(seg(t, 3.0, 3.35)))
    if a_old > 0:
        txt = "单卖 2000，很难动"
        w0 = tw(txt, 42)
        text(d, (90, 674), txt, 42, A(GRAY, a_old))
        d.line([92, 702, 92 + w0 * a_old, 702], fill=A(RED, a_old * 0.9), width=5)
        # 印章
        sw, sh = 470, 196
        stamp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        sd = ImageDraw.Draw(stamp)
        sd.rounded_rectangle([6, 6, sw - 6, sh - 6], radius=16, outline=A(RED, a_old), width=8)
        sd.rounded_rectangle([22, 22, sw - 22, sh - 22], radius=10, outline=A(RED, a_old * 0.5), width=3)
        sd.text((sw / 2, sh / 2), "卖不动", font=font(98), fill=A(RED, a_old), anchor="mm")
        stamp = stamp.rotate(-8, expand=1, resample=Image.BICUBIC)
        img.alpha_composite(stamp, (int(540 - stamp.width / 2), int(862 - stamp.height / 2)))
    a_new = ease_out(seg(t, 3.3, 3.8))
    if a_new > 0:
        text(d, (90, 674), "改个规则：", 38, A(GRAY, a_new))
        text(d, (90 + tw("改个规则：", 38) + 8, 674), "下单就送 20 张基础体检卡", 38, A(INK, a_new))

    # 20 张小卡：5×4，4.0s 起每 0.22s 一张
    X0, Y0 = 90, 744
    cw, ch, gx, gy = 172, 78, 15, 16
    for i in range(20):
        ti = 3.55 + i * 0.21
        ai = ease_out(seg(t, ti, ti + 0.30))
        if ai <= 0: continue
        r, c = divmod(i, 5)
        cx = X0 + c * (cw + gx) + cw / 2; cy = Y0 + r * (ch + gy) + ch / 2
        s = 0.70 + 0.30 * back_out(seg(t, ti, ti + 0.34))
        w, h = cw * s, ch * s
        box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
        d.rounded_rectangle(box, radius=10, fill=A(WHITE, ai), outline=A(LGRAY, ai), width=2)
        d.ellipse([box[0] + 14, box[1] + h / 2 - 7, box[0] + 28, box[1] + h / 2 + 7], fill=A(GREEN, ai))
        text(d, (box[0] + 37, box[1] + h / 2), "体检卡", 28, A(INK, ai), anchor="lm")

    # 结果行（11.2s 起）：放在视觉区内，不占字幕区
    a3 = ease_out(seg(t, 9.8, 10.5))
    if a3 > 0:
        y0 = 1168
        d.rounded_rectangle([90, y0, 990, y0 + 96], radius=10, fill=A(INK, a3))
        text(d, (128, y0 + 48), "1 个客户", 40, A(WHITE, a3), anchor="lm")
        text(d, (330, y0 + 48), "→", 40, A(GREEN, a3), anchor="lm")
        text(d, (400, y0 + 48), "20 个人走进门店", 40, A(WHITE, a3), anchor="lm")
    return img


# ============ 贴片 2：推三返一阶梯（24.65–37.06，12.41s） ============
def card2(t):
    img = canvas(); d = ImageDraw.Draw(img)

    # ---- 前段 0-4.4s：卡 → 到店体验 → 消费升级 ----
    if t < 4.4:
        a_all = 1 - ease_out(seg(t, 4.0, 4.4))
        header(img, "裂变开始", ["朋友拿卡", "到店来体验"], None, t)
        steps = [("持卡到店", "扫码核销"), ("做基础体检", "零成本体验"), ("消费升级", "系统记录归属")]
        y0 = 560
        for i, (m, s2) in enumerate(steps):
            ti = 0.5 + i * 0.55
            ai = ease_out(seg(t, ti, ti + 0.45)) * a_all
            if ai <= 0: continue
            y = y0 + i * 226
            d.rounded_rectangle([90, y, 990, y + 190], radius=16,
                                fill=A(WHITE, ai), outline=A(LGRAY, ai), width=2)
            d.ellipse([126, y + 65, 186, y + 125], fill=A(BLUE if i < 2 else GREEN, ai))
            text(d, (156, y + 95), str(i + 1), 34, A(WHITE, ai), anchor="mm")
            text(d, (216, y + 50), m, 44, A(INK, ai))
            text(d, (216, y + 116), s2, 30, A(GRAY, ai))
        a_h = ease_out(seg(t, 2.4, 3.0)) * a_all
        if a_h > 0:
            text(d, (90, 1232), "20 张卡 → 20 次到店 → 系统自动记在送礼人名下", 32, A(GRAY, a_h))
        return img

    # ---- 后段 4.4s 起：阶梯 ----
    t2 = t - 4.4
    header(img, "重点机制", ["推三返一"], "老客户下面每一单，都按阶梯返现", t2)

    # 累加公式：跟着语音一级一级加上去
    base_y = 1246
    bars = [(10, "第一单", BLUE, 6.64), (20, "第二单", AMBER, 8.46), (70, "第三单", RED, 9.50)]
    bw, gap, X0 = 280, 20, 90
    FH = lambda p: 120 + p / 70 * 520

    # 占位轮廓（全高，先摆好，避免画面空）
    a_ph = ease_out(seg(t2, 0.5, 1.1))
    for i, (pct, lab, col, t_on) in enumerate(bars):
        if ease_out(seg(t, t_on - 0.06, t_on + 0.40)) > 0:
            continue
        x = X0 + i * (bw + gap)
        y = base_y - FH(pct)
        d.rounded_rectangle([x, y, x + bw, base_y], radius=12,
                            fill=A((240, 241, 244), a_ph), outline=A(LGRAY, a_ph), width=2)
        text(d, (x + bw / 2, y + 22), "%d%%" % pct, 62, A(LGRAY, a_ph), anchor="mt")
        text(d, (x + bw / 2, base_y - 54), lab, 32, A(LGRAY, a_ph), anchor="mb")

    # 实心柱（从底部长出来）
    for i, (pct, lab, col, t_on) in enumerate(bars):
        ai = ease_out(seg(t, t_on - 0.04, t_on + 0.34))
        if ai <= 0:
            continue
        x = X0 + i * (bw + gap)
        hh = FH(pct) * ai
        y = base_y - hh
        shadow(img, [x, y, x + bw, base_y], 12, opacity=0.09 * ai)
        d.rounded_rectangle([x, y, x + bw, base_y], radius=12, fill=A(col, ai))
        ta = min(1.0, ai * 2.4)
        text(d, (x + bw / 2, y + 20), "%d%%" % pct, 68, A(WHITE, ta), anchor="mt")
        text(d, (x + bw / 2, base_y - 54), lab, 32, A(WHITE, ta), anchor="mb")

    # 累加计数行
    ay = 452
    a1 = ease_out(seg(t, 6.64, 7.1))
    a2 = ease_out(seg(t, 8.46, 8.9))
    a3 = ease_out(seg(t, 9.50, 10.0))
    a4 = ease_out(seg(t, 10.5, 11.1))
    if a1 > 0:
        x = 90
        text(d, (x, ay), "10%", 60, A(BLUE, a1)); x += tw("10%", 60)
    if a2 > 0:
        text(d, (x, ay), " + ", 60, A(GRAY, a2)); x += tw(" + ", 60)
        text(d, (x, ay), "20%", 60, A(AMBER, a2)); x += tw("20%", 60)
    if a3 > 0:
        text(d, (x, ay), " + ", 60, A(GRAY, a3)); x += tw(" + ", 60)
        text(d, (x, ay), "70%", 60, A(RED, a3)); x += tw("70%", 60)
    if a4 > 0:
        text(d, (x, ay), " = ", 60, A(GRAY, a4)); x += tw(" = ", 60)
        text(d, (x, ay), "100%", 60, A(GREEN, a4))
        text(d, (90, ay + 82), "三单累计满额 → 2000 块全额返还", 32, A(GRAY, a4))
    return img


# ============ 贴片 3：三单回本（37.06–51.46，14.40s） ============
def card3(t):
    img = canvas(); d = ImageDraw.Draw(img)
    header(img, "算一笔账", ["只要 3 个人转化", "2000 块全退"], "另外 17 个不来，也不亏", t)

    X0, Y0 = 90, 620
    cw, ch, gx, gy = 172, 74, 15, 14
    conv = [0, 7, 13]
    for i in range(20):
        ti = 1.0 + i * 0.135
        ai = ease_out(seg(t, ti, ti + 0.28))
        if ai <= 0: continue
        r, c = divmod(i, 5)
        cx = X0 + c * (cw + gx); cy = Y0 + r * (ch + gy)
        g = 0
        if i in conv:
            k = conv.index(i)
            g = ease_out(seg(t, 4.0 + k * 0.30, 4.3 + k * 0.30))
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10,
                            fill=A(WHITE, ai), outline=A(BLUE if (i in conv and g == 0) else LGRAY, ai), width=2)
        if g > 0:
            d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=10, fill=A(GREEN, g))
            text(d, (cx + cw / 2, cy + ch / 2), "已转化", 28, A(WHITE, g), anchor="mm")
        else:
            text(d, (cx + cw / 2, cy + ch / 2), "体检卡", 27, A(INK, ai), anchor="mm")

    # 结算卡：5.0s 起
    a = ease_out(seg(t, 5.0, 5.7))
    if a > 0:
        y0 = 984
        shadow(img, [90, y0, 990, y0 + 182], 16, opacity=0.09 * a)
        d.rounded_rectangle([90, y0, 990, y0 + 182], radius=16,
                            fill=A(WHITE, a), outline=A(LGRAY, a), width=2)
        text(d, (128, y0 + 26), "老客户实际支出", 30, A(GRAY, a))
        text(d, (126, y0 + 78), "¥2000", 66, A(INK, a))
        ax = ease_out(seg(t, 6.3, 6.9))
        if ax > 0:
            w0 = 0
            bb = font(66).getbbox("¥2000")
            d.line([126 + bb[0] + 4, y0 + 132, 126 + bb[0] + 4 + bb[2] * ax, y0 + 132],
                   fill=A(RED, ax), width=6)
        aa = ease_out(seg(t, 6.5, 7.0))
        if aa > 0:
            text(d, (320, y0 + 96), "→", 56, A(GRAY, aa), anchor="lt")
        az = ease_out(seg(t, 6.9, 7.5))
        if az > 0:
            text(d, (392, y0 + 78), "¥0", 86, A(GREEN, az))
        ab = ease_out(seg(t, 7.4, 8.0))
        if ab > 0:
            lb = "已回本"
            lw = tw(lb, 30) + 40
            d.rounded_rectangle([890 - lw, y0 + 92, 890, y0 + 144], radius=26, fill=A(GREEN, ab))
            text(d, (890 - lw / 2, y0 + 118), lb, 30, A(WHITE, ab), anchor="mm")

    # 第二单卡住 → 催单（9.0s 起）
    a2 = ease_out(seg(t, 9.0, 9.8))
    if a2 > 0:
        y0 = 1186
        d.rounded_rectangle([90, y0, 990, y0 + 92], radius=10, fill=A((254, 242, 242), a2))
        d.rounded_rectangle([90, y0, 96, y0 + 92], radius=3, fill=A(RED, a2))
        text(d, (124, y0 + 46), "卡在第二单？第三单 70% 在等他", 34, A(RED, a2), anchor="lm")
        text(d, (900, y0 + 46), "他自己会去催", 26, A((153, 27, 27), a2), anchor="rm")
    return img


CARDS = {"c1": card1, "c2": card2, "c3": card3}
DUR = {"c1": 15.17, "c2": 12.41, "c3": 14.40}

if __name__ == "__main__":
    out = "/Users/jiacong/Downloads/剪辑素材/项目/03_体检中心推三返一/_build"
    for name, ts in [("c1", [1.0, 6.0, 13.5]), ("c2", [2.5, 7.0, 3.0, 11.9]), ("c3", [3.0, 9.0, 13.9])]:
        for t in ts:
            CARDS[name](t).convert("RGB").save(f"{out}/p_{name}_{t}.png")
    print("ok")
