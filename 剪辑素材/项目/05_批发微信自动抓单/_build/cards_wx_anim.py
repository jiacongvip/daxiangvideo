# -*- coding: utf-8 -*-
"""批发微信自动抓单 · 三张贴片动画版"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 25
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
OUT = "/Users/jiacong/Downloads/剪辑素材/项目/05_批发微信自动抓单/02_贴片"

_fc = {}
def font(s, w=6):
    k = (s, w)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONT, s, index=2 if w == 6 else 1)
    return _fc[k]

def tw(s, size):
    b = font(size).getbbox(s); return b[2] - b[0]

def clamp01(t): return max(0.0, min(1.0, t))
def seg(t, a, b):
    if b <= a: return 1.0 if t >= b else 0.0
    return clamp01((t - a) / (b - a))
def ease_out(t):
    t = clamp01(t); return 1 - (1 - t) ** 3
def back_out(t):
    t = clamp01(t) - 1
    return 1 + 2.7 * t ** 3 + 1.7 * t ** 2
def A(c, a):
    return (c[0], c[1], c[2], int(255 * clamp01(a)))

BG_T, BG_B = (16, 18, 23), (8, 9, 12)
WX     = (7, 193, 96)
WX_D   = (5, 90, 52)
BLUE   = (59, 130, 246)
ORANGE = (255, 138, 0)
WHITE  = (245, 247, 250)
GRAY   = (150, 158, 172)
DIM    = (104, 112, 126)
CARD   = (18, 21, 27)
LINE   = (42, 47, 58)

_cache = {}
def base():
    if "bg" in _cache: return _cache["bg"].copy()
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
    img = Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")
    for cx, cy, r, col, amt in [(880, 330, 400, (10, 90, 60), 0.42),
                                (200, 1150, 380, (20, 55, 110), 0.30)]:
        g = Image.new("RGB", (W, H), (0, 0, 0))
        ImageDraw.Draw(g).ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        g = g.filter(ImageFilter.GaussianBlur(r * 0.62))
        img = Image.blend(img, Image.blend(img, g, 0.75), amt)
    _cache["bg"] = img
    return img.copy()


def rrect(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def header(img, t, step, title, sub):
    d = ImageDraw.Draw(img)
    a1 = ease_out(seg(t, 0.0, 0.42))
    a2 = ease_out(seg(t, 0.12, 0.62))
    if a1 > 0:
        rrect(d, [84, 250, 268, 306], 28, fill=A(WX, a1))
        d.text((176, 278), "第 %s 步" % step, font=font(30), fill=A((6, 24, 14), a1), anchor="mm")
        d.text((292, 254), "共 3 步", font=font(28), fill=A(DIM, a1))
    if a2 > 0:
        dy = int(14 * (1 - a2))
        d.text((84, 330 + dy), title, font=font(82), fill=A(WHITE, a2))
        d.text((84, 442 + dy), sub, font=font(34), fill=A(GRAY, a2))


def footer(img, t, text, color=WX, t_in=9.8):
    a = ease_out(seg(t, t_in, t_in + 0.5))
    if a <= 0: return img
    by = 1168
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([84, by, 996, by + 116], radius=58,
                                         outline=color + (int(170 * a),), width=5)
    img = Image.alpha_composite(img.convert("RGBA"), gl.filter(ImageFilter.GaussianBlur(13))).convert("RGB")
    d = ImageDraw.Draw(img)
    rrect(d, [84, by, 996, by + 116], 58, fill=A((10, 14, 12), a), outline=A(color, a), width=4)
    d.text((540, by + 58), text, font=font(44), fill=A(color, a), anchor="mm")
    return img


def chatwin(img, box, who, bubble, a_win, a_bub):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    if a_win <= 0: return img
    rrect(d, box, 18, fill=A((20, 23, 29), a_win), outline=A(LINE, a_win), width=2)
    d.rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + 52], fill=A((28, 32, 40), a_win))
    d.text((x0 + 22, y0 + 14), "批发订货群", font=font(26), fill=A((190, 198, 212), a_win))
    for i in range(3):
        d.ellipse([x1 - 36 - i * 22, y0 + 20, x1 - 26 - i * 22, y0 + 30], fill=A((80, 88, 102), a_win))
    if a_bub > 0:
        by = y0 + 76
        d.ellipse([x0 + 24, by + 2, x0 + 80, by + 58], fill=A(WX_D, a_bub))
        d.text((x0 + 52, by + 30), who[0], font=font(24), fill=A(WX, a_bub), anchor="mm")
        bx0 = x0 + 96
        bw = min(tw(bubble, 30) + 44, x1 - bx0 - 24)
        rrect(d, [bx0, by, bx0 + bw, by + 84], 12, fill=A((38, 42, 50), a_bub))
        d.text((bx0 + 22, by + 16), bubble, font=font(30), fill=A((226, 232, 240), a_bub))
    return img


# ================= 贴片1 11.61s =================
def card1(t):
    img = base(); d = ImageDraw.Draw(img)
    header(img, t, "1", "自动抓单", "电脑端挂个助手，24 小时盯着")

    a_win = ease_out(seg(t, 0.55, 1.15))
    a_bub = ease_out(seg(t, 1.25, 1.95))
    img = chatwin(img, [84, 505, 996, 730], "客", "鸡蛋20箱 调料10包 蒜米5斤", a_win, a_bub)
    d = ImageDraw.Draw(img)

    # 箭头
    a_ar = ease_out(seg(t, 5.9, 6.4))
    a_ar_ph = ease_out(seg(t, 2.0, 2.5)) * 0.35
    a_ar = max(a_ar, a_ar_ph)
    if a_ar > 0:
        d.line([540, 752, 540, 752 + 40 * a_ar], fill=A(WX, a_ar), width=5)
        if a_ar > 0.85:
            d.polygon([(522, 782), (558, 782), (540, 806)], fill=WX)
        d.text((576, 760), "自动识别商品和数量", font=font(28), fill=A((140, 210, 170), a_ar))

    # 表格（2.2s 起灰态占位，7.7s 点亮）
    a_tb = ease_out(seg(t, 7.7, 8.2))
    a_tb_ph = ease_out(seg(t, 2.2, 2.8)) * 0.32
    aa_tb = max(a_tb, a_tb_ph)
    if aa_tb > 0:
        x0, y0, x1 = 84, 828, 996
        rrect(d, [x0, y0, x1, y0 + 324], 16, fill=A(CARD, aa_tb), outline=A(LINE, aa_tb), width=2)
        rrect(d, [x0, y0, x1, y0 + 62], 16, fill=A((26, 30, 38), aa_tb))
        d.rectangle([x0, y0 + 40, x1, y0 + 62], fill=A((26, 30, 38), aa_tb))
        d.text((x0 + 28, y0 + 30), "商品", font=font(26), fill=A(DIM, aa_tb), anchor="lm")
        d.text((x1 - 28, y0 + 30), "数量", font=font(26), fill=A(DIM, aa_tb), anchor="rm")

        rows = [("鸡蛋", "20 箱"), ("调料", "10 包"), ("蒜米", "5 斤")]
        for i, (n, q) in enumerate(rows):
            ai = ease_out(seg(t, 8.2 + i * 0.55, 8.6 + i * 0.55))
            if ai <= 0: continue
            ry = y0 + 62 + i * 88
            if i > 0:
                d.line([x0 + 24, ry, x1 - 24, ry], fill=A((32, 36, 46), max(aa_tb, ai)), width=1)
            d.text((x0 + 30, ry + 42), n, font=font(32), fill=A(WHITE, ai), anchor="lm")
            d.text((x1 - 30, ry + 42), q, font=font(32), fill=A((206, 214, 228), ai), anchor="rm")

    return footer(img, t, "不用再一行行肉眼核对了", WX, 10.3)


# ================= 贴片2 11.97s =================
def card2(t):
    img = base(); d = ImageDraw.Draw(img)
    header(img, t, "2", "模糊报单", "他说「调料10包」，你怎么知道是哪款？")

    a_win = ease_out(seg(t, 0.4, 1.0))
    a_bub = ease_out(seg(t, 2.55, 3.1))
    img = chatwin(img, [84, 500, 996, 720], "王", "调料10包", a_win, a_bub)
    d = ImageDraw.Draw(img)

    a_ar = ease_out(seg(t, 4.1, 4.6))
    if a_ar > 0:
        d.line([540, 742, 540, 742 + 38 * a_ar], fill=A(ORANGE, a_ar), width=5)
        if a_ar > 0.85:
            d.polygon([(522, 770), (558, 770), (540, 794)], fill=ORANGE)
        d.text((576, 750), "翻这个客户的历史常购", font=font(28), fill=A((240, 175, 110), a_ar))

    # 历史常购（含滚动匹配）
    a_card = ease_out(seg(t, 4.6, 5.2))
    if a_card > 0:
        x0, y0, x1 = 84, 818, 996
        rrect(d, [x0, y0, x1, y0 + 292], 16, fill=A(CARD, a_card), outline=A(LINE, a_card), width=2)

        rows = [("李锦记蚝油 700g", "¥ 16"),
                ("海天生抽 1.9L", "¥ 22"),
                ("蒸鱼豉油 500ml", "¥ 9.8"),
                ("恒顺香醋 500ml", "¥ 6.5"),
                ("老抽王 500ml", "¥ 7.8"),
                ("海天金标生抽 500ml", "¥ 8.5"),
                ("料酒 500ml", "¥ 5.5"),
                ("芝麻香油 250ml", "¥ 12"),
                ("郫县豆瓣酱 500g", "¥ 11"),
                ("鸡精 200g", "¥ 9")]
        TARGET = 5
        ROWH = 74

        # 滚动进度
        p_scroll = clamp01((t - 5.0) / 2.5)
        e_scroll = 1 - (1 - p_scroll) ** 3
        done = (t >= 7.5)
        off = int(e_scroll * TARGET * ROWH) if not done else TARGET * ROWH

        # 顶栏状态
        if t < 5.0:
            st, stc = "王老板 · 历史常购调料", DIM
        elif not done:
            st, stc = "匹配中…", ORANGE
        else:
            st, stc = "已匹配：海天金标生抽 500ml", WX
        d.text((x0 + 26, y0 + 16), st, font=font(26), fill=A(stc, a_card))

        # 滚动区（独立图层，裁到窗口内）
        top, bot = y0 + 58, y0 + 290
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for i, (n, p_) in enumerate(rows):
            ry = top + i * ROWH - off + 6
            if ry > bot or ry + ROWH < top: continue
            is_t = (i == TARGET) and done
            if is_t:
                ld.rounded_rectangle([x0 + 10, ry - 2, x1 - 10, ry + 64], radius=10,
                                     fill=(12, 44, 28, 255), outline=WX + (255,), width=2)
            col = WX if is_t else (200, 208, 222)
            ld.text((x0 + 32, ry + 30), n, font=font(30), fill=col + (255,), anchor="lm")
            ld.text((x1 - 32, ry + 30), p_, font=font(28), fill=(WX if is_t else DIM) + (255,), anchor="rm")

        region = img.crop((0, top, W, bot)).convert("RGBA")
        region = Image.alpha_composite(region, layer.crop((0, top, W, bot)))
        img.paste(region.convert("RGB"), (0, top))
        d = ImageDraw.Draw(img)

    return footer(img, t, "自动带出规格，老板不用记", WX, 9.9)


# ================= 贴片3 13.81s =================
def card3(t):
    img = base(); d = ImageDraw.Draw(img)
    header(img, t, "3", "防错闭环", "确认过再出单，三条路随你选")

    # ① 单子生成
    a1 = ease_out(seg(t, 1.7, 2.2))
    if a1 > 0:
        yy = 492 + int(18 * (1 - a1))
        rrect(d, [84, yy, 996, yy + 132], 18, fill=A(CARD, a1), outline=A(WX, a1 * 0.7), width=2)
        d.rounded_rectangle([84, yy, 96, yy + 132], radius=6, fill=A(WX, a1))
        d.ellipse([116, yy + 34, 180, yy + 98], fill=A((10, 48, 30), a1), outline=A(WX, a1), width=3)
        d.text((148, yy + 66), "1", font=font(38), fill=A(WX, a1), anchor="mm")
        d.text((206, yy + 30), "单子生成", font=font(38), fill=A(WHITE, a1))
        d.text((206, yy + 80), "系统自动整理成待发清单", font=font(25), fill=A(GRAY, a1))

    # 分支线
    a_l = ease_out(seg(t, 2.6, 3.0))
    if a_l > 0:
        d.line([540, 624, 540, 656], fill=A((86, 94, 110), a_l), width=4)
        d.line([230, 656, 850, 656], fill=A((86, 94, 110), a_l), width=4)
        for cx in (230, 540, 850):
            d.line([cx, 656, cx, 688 + 10 * a_l], fill=A((86, 94, 110), a_l), width=4)

    # ② 三条路
    paths = [
        ("客户确认", "小程序点一下", BLUE, 3.6),
        ("老板确认", "手机看一眼", (168, 120, 255), 3.75),
        ("直接打印", "不用等确认", ORANGE, 3.9),
    ]
    for i, (t1, t2, col, t_on) in enumerate(paths):
        a = ease_out(seg(t, t_on, t_on + 0.5))
        if a <= 0: continue
        bx = 85 + i * 310
        yy = 698 + int(18 * (1 - a))
        rrect(d, [bx, yy, bx + 290, yy + 162], 16, fill=A((16, 19, 25), a),
              outline=A(col, a * 0.85), width=2)
        d.rounded_rectangle([bx, yy, bx + 290, yy + 6], radius=3, fill=A(col, a))
        d.text((bx + 24, yy + 34), t1, font=font(34), fill=A(WHITE, a))
        d.text((bx + 24, yy + 88), t2, font=font(23), fill=A(GRAY, a))
        # 右下的序号标
        d.text((bx + 262, yy + 130), "0%d" % (i + 1), font=font(21), fill=A(tuple(int(c * 0.8) for c in col), a), anchor="rm")

    # 汇合线
    a_l2 = ease_out(seg(t, 4.5, 4.9))
    if a_l2 > 0:
        for cx in (230, 540, 850):
            d.line([cx, 860, cx, 892 + 10 * a_l2], fill=A((86, 94, 110), a_l2), width=4)
        d.line([230, 902, 850, 902], fill=A((86, 94, 110), a_l2), width=4)
        d.line([540, 902, 540, 930], fill=A((86, 94, 110), a_l2), width=4)

    # ③ 出单（先灰态占位）
    a3 = ease_out(seg(t, 10.9, 11.5))
    a3_ph = ease_out(seg(t, 5.0, 5.5)) * 0.35
    if a3_ph > 0 and a3 <= 0:
        aa = a3_ph
        rrect(d, [84, 934, 996, 1082], 18, fill=A(CARD, aa), outline=A(ORANGE, aa * 0.45), width=2)
        d.text((206, 960), "打印机直接出单", font=font(38), fill=A(WHITE, aa))
        d.text((206, 1016), "热敏 / 小票 / 普通 A4，接上就能打", font=font(25), fill=A(GRAY, aa))
    if a3 > 0:
        yy = 934 + int(18 * (1 - a3))
        rrect(d, [84, yy, 996, yy + 148], 18, fill=A(CARD, a3), outline=A(ORANGE, a3 * 0.8), width=2)
        d.rounded_rectangle([84, yy, 96, yy + 148], radius=6, fill=A(ORANGE, a3))
        d.ellipse([116, yy + 42, 180, yy + 106], fill=A((52, 30, 8), a3), outline=A(ORANGE, a3), width=3)
        d.text((148, yy + 74), "3", font=font(38), fill=A(ORANGE, a3), anchor="mm")
        d.text((206, yy + 26), "打印机直接出单", font=font(38), fill=A(WHITE, a3))
        d.text((206, yy + 82), "热敏 / 小票 / 普通 A4，接上就能打", font=font(25), fill=A(GRAY, a3))

    return footer(img, t, "三种确认方式，一条都不漏", ORANGE, 12.3)


CARDS = {"c1": (card1, 11.72), "c2": (card2, 12.00), "c3": (card3, 13.06)}
NAMES = {"c1": "贴片1_自动抓单", "c2": "贴片2_常购匹配", "c3": "贴片3_防错打单"}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for k, (fn, dur) in CARDS.items():
        path = os.path.join(OUT, NAMES[k] + ".mp4")
        n = int(round(dur * FPS))
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
               "-c:v", "libx264", "-preset", "medium", "-crf", "18",
               "-pix_fmt", "yuv420p", "-g", "50", "-movflags", "+faststart", path]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(n):
            p.stdin.write(fn(i / FPS).convert("RGB").tobytes())
        p.stdin.close(); p.wait()
        print("  %s %.2fs" % (NAMES[k], dur))
