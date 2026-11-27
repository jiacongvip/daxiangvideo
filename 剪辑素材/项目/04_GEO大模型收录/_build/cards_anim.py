# -*- coding: utf-8 -*-
"""GEO 三张贴片 · 动画版（竖版 1080x1920）
时间轴对齐 seg3 / seg4 / seg5 的配音
"""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 25
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
OUT = "/Users/jiacong/Downloads/剪辑素材/项目/04_GEO大模型收录/02_贴片"

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

_fc = {}
def font(s, w=6):
    k = (s, w)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONT, s, index=2 if w == 6 else 1)
    return _fc[k]

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
def A(c, a):
    return (c[0], c[1], c[2], int(255 * clamp01(a)))

def stamp(img, cx, cy, text, color, w=340, h=124, angle=-9, a=1.0, fs=66):
    pad = 30
    lay = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([pad, pad, pad + w, pad + h], radius=16,
                         outline=color + (int(240 * a),), width=9)
    ld.rounded_rectangle([pad + 15, pad + 15, pad + w - 15, pad + h - 15], radius=10,
                         outline=color + (int(110 * a),), width=3)
    ld.text((pad + w / 2, pad + h / 2), text, font=font(fs), fill=color + (int(250 * a),), anchor="mm")
    lay = lay.rotate(angle, expand=True, resample=Image.BICUBIC)
    base_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base_img.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))
    return Image.alpha_composite(img.convert("RGBA"), base_img).convert("RGB")


def rrect(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


# ---------- 背景（缓存） ----------
_cache = {}
def base():
    if "bg" in _cache:
        return _cache["bg"].copy()
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
    img = Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")
    # glow
    for cx, cy, r, col, amt in [(880, 340, 420, (26, 70, 190), 0.5),
                                (200, 1180, 400, (150, 66, 20), 0.3)]:
        g = Image.new("RGB", (W, H), (0, 0, 0))
        ImageDraw.Draw(g).ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
        g = g.filter(ImageFilter.GaussianBlur(r * 0.6))
        img = Image.blend(img, Image.blend(img, g, 0.75), amt)
    _cache["bg"] = img
    return img.copy()


def header(img, t, step, title, sub, t_in=0.0):
    d = ImageDraw.Draw(img)
    a1 = ease_out(seg(t, t_in, t_in + 0.4))
    a2 = ease_out(seg(t, t_in + 0.15, t_in + 0.6))
    if a1 > 0:
        rrect(d, [84, 250, 260, 306], 28, fill=A(ORANGE, a1))
        d.text((172, 278), "第 %s 步" % step, font=font(30), fill=A((24, 14, 6), a1), anchor="mm")
        d.text((286, 254), "共 3 步", font=font(28), fill=A(DIM, a1))
    if a2 > 0:
        dy = int(16 * (1 - a2))
        d.text((84, 330 + dy), title, font=font(84), fill=A(WHITE, a2))
        d.text((84, 440 + dy), sub, font=font(36), fill=A(GRAY, a2))


def footer(img, t, text, color=ORANGE_L, t_in=99.0):
    a = ease_out(seg(t, t_in, t_in + 0.5))
    if a <= 0: return img
    by = 1190
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([84, by, 996, by + 118], radius=59,
                                         outline=color + (int(190 * a),), width=5)
    img = Image.alpha_composite(img.convert("RGBA"), gl.filter(ImageFilter.GaussianBlur(13))).convert("RGB")
    d = ImageDraw.Draw(img)
    rrect(d, [84, by, 996, by + 118], 59, fill=A((12, 10, 9), a), outline=A(color, a), width=4)
    d.text((540, by + 59), text, font=font(46), fill=A(color, a), anchor="mm")
    return img


# ================= 贴片1：逆向工程 17.38s =================
def card1(t):
    img = base()
    d = ImageDraw.Draw(img)
    header(img, t, "1", "GEO 逆向工程", "看 AI 到底引用了谁")

    # ① 搜索
    a1 = ease_out(seg(t, 1.0, 1.5))
    if a1 > 0:
        d.text((92, 530), "① 搜你行业的关键词", font=font(32), fill=A(BLUE, a1))
        rrect(d, [84, 574, 996, 662], 16, fill=A((22, 25, 34), a1),
              outline=A((48, 60, 92), a1), width=2)
        # 逐字显示
        full = "本地装修公司哪家好？"
        n = int(len(full) * ease_io(seg(t, 1.6, 3.6)))
        if n > 0:
            d.text((114, 596), full[:n], font=font(34), fill=A((214, 220, 234), 1))
        if n < len(full) and int(t * 3) % 2 == 0:
            cx = 114 + tw(full[:n], 34) + 3
            d.line([cx, 592, cx, 634], fill=A(BLUE, 1), width=3)
        rrect(d, [882, 586, 976, 650], 12, fill=A(BLUE, a1))
        d.text((929, 618), "搜索", font=font(26), fill=A((255, 255, 255), a1), anchor="mm")

    # 箭头
    a_ar = ease_out(seg(t, 4.6, 5.1))
    if a_ar > 0:
        d.line([540, 680, 540, 680 + 34 * a_ar], fill=A((90, 100, 120), a_ar), width=5)
        if a_ar > 0.8:
            d.polygon([(525, 708), (555, 708), (540, 726)], fill=(90, 100, 120))

    # ② 引用来源（1.9s 灰态占位，5.2s 点亮）
    a2 = ease_out(seg(t, 5.2, 5.8))
    a2_ph = ease_out(seg(t, 1.9, 2.4))
    if a2_ph > 0:
        aa = max(a2_ph * 0.55, a2)
        rrect(d, [84, 786, 996, 1040], 18, fill=A(CARD, aa), outline=A((74, 52, 30), max(a2_ph * 0.5, a2)), width=2)
        d.text((92, 740), "② 点开回答下面的「引用来源」", font=font(32), fill=A(ORANGE_L, max(a2_ph * 0.6, a2)))
        d.text((114, 806), "引用来源", font=font(30), fill=A(ORANGE_L, max(a2_ph * 0.7, a2)))
        rrect(d, [252, 804, 300, 844], 20, fill=A(ORANGE, max(a2_ph * 0.7, a2)))
        d.text((276, 824), "3", font=font(24), fill=A((20, 14, 8), max(a2_ph * 0.7, a2)), anchor="mm")

    # 平台逐个点亮
    srcs = [("知乎", "专栏 · 高权重", 10.0), ("公众号", "行业号 · 已收录", 12.0), ("行业论坛", "垂直站 · 长尾", 14.0)]
    for i, (n, s, t_on) in enumerate(srcs):
        a_ph = ease_out(seg(t, 1.9 + i * 0.13, 2.3 + i * 0.13))
        if a_ph <= 0: continue
        lit = ease_out(seg(t, t_on, t_on + 0.5))
        bx = 108 + i * 296
        sc = 1.0 + 0.06 * (back_out(seg(t, t_on, t_on + 0.45)) if lit > 0 else 0)
        w, h = int(276 * sc), int(136 * sc)
        cx, cy = bx + 138, 866 + 68
        box = [cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2]
        line_c = BLUE if lit > 0 else (56, 62, 78)
        bgc = (20, 23, 32) if lit > 0 else (16, 18, 24)
        rrect(d, box, 14, fill=A(bgc, a_ph), outline=A(line_c, max(a_ph * 0.5, lit)), width=2)
        d.ellipse([box[0] + 18, cy - 20, box[0] + 58, cy + 20],
                  fill=A(BLUE_D if lit > 0 else (30, 34, 44), a_ph),
                  outline=A(BLUE if lit > 0 else (60, 66, 82), a_ph), width=2)
        d.text((box[0] + 38, cy), str(i + 1), font=font(24),
               fill=A(BLUE if lit > 0 else DIM, a_ph), anchor="mm")
        d.text((box[0] + 76, box[1] + 22), n, font=font(32),
               fill=A(WHITE if lit > 0 else (120, 128, 144), a_ph))
        d.text((box[0] + 76, box[1] + 70), s, font=font(21),
               fill=A(DIM if lit > 0 else (80, 88, 102), a_ph))

    # ③ 结论：6.5s 灰态占位，14.7 点亮
    a3 = ease_out(seg(t, 14.7, 15.2))
    a3_ph = ease_out(seg(t, 2.2, 2.7)) * 0.30
    aa = max(a3, a3_ph)
    if aa > 0:
        y3 = 1078
        rrect(d, [84, y3, 996, y3 + 84], 12, fill=A((20, 32, 26), aa),
              outline=A(GREEN, aa * (0.6 + 0.4 * a3)), width=2)
        d.text((116, y3 + 42), "③ 这三个就是 AI 认可的", font=font(32), fill=A(GREEN_L, aa), anchor="lm")
        rrect(d, [700, y3 + 20, 950, y3 + 64], 22, fill=A(GREEN, aa))
        d.text((825, y3 + 42), "高权重信源", font=font(30), fill=A((10, 26, 16), min(1, aa * 1.6)), anchor="mm")

    return footer(img, t, "AI 引用谁，你就发到谁那儿", ORANGE_L, 15.6)


# ================= 贴片2：抓取喜好 18.05s =================
def card2(t):
    img = base()
    d = ImageDraw.Draw(img)
    if t < 5.25:
        header(img, t, "2", "精准定点投放", "它引用谁，就投到谁那儿")
    else:
        header(img, t, "2", "AI 只抓这两种", "内容质量的判定标准")

    # ---------- 0-5.2s：投放段（对应「去这些被收录的平台上投放内容」）----------
    if t < 5.25:
        a0 = 1 - ease_out(seg(t, 4.85, 5.20))
        # 三个平台
        names = [("知乎", "专栏"), ("公众号", "行业号"), ("垂直论坛", "长尾")]
        for i, (n, s2) in enumerate(names):
            ai = ease_out(seg(t, 0.55 + i * 0.35, 0.95 + i * 0.35)) * a0
            if ai <= 0: continue
            bx = 108 + i * 296
            by = 600
            rrect(d, [bx, by, bx + 276, by + 210], 16,
                  fill=A((20, 23, 32), ai), outline=A(BLUE, ai * 0.75), width=2)
            d.ellipse([bx + 104, by + 40, bx + 172, by + 108],
                      fill=A(BLUE_D, ai), outline=A(BLUE, ai), width=2)
            d.text((bx + 138, by + 74), n[0], font=font(34), fill=A(WHITE, ai), anchor="mm")
            d.text((bx + 138, by + 140), n, font=font(30), fill=A(WHITE, ai), anchor="mm")
            d.text((bx + 138, by + 178), s2, font=font(22), fill=A(DIM, ai), anchor="mm")

        a_up = ease_out(seg(t, 2.5, 3.0)) * a0
        if a_up > 0:
            text_y = 850
            d.line([540, text_y + 46, 540, text_y + 6], fill=A(ORANGE, a_up), width=6)
            d.polygon([(519, text_y + 14), (561, text_y + 14), (540, text_y - 12)], fill=A(ORANGE, a_up))
            d.text((540, 916), "把你写的内容，投到这几个平台", font=font(34),
                   fill=A(ORANGE_L, a_up), anchor="mt")

        a_src = ease_out(seg(t, 3.2, 3.7)) * a0
        if a_src > 0:
            rrect(d, [260, 990, 820, 1094], 14, fill=A((22, 26, 36), a_src),
                  outline=A((60, 70, 92), a_src), width=2)
            d.text((540, 1042), "你的真实优势 + 核心观点", font=font(32),
                   fill=A((214, 222, 236), a_src), anchor="mm")

        return footer(img, t, "投对地方，比写多少篇都重要", ORANGE_L, 3.9)

    # ---------- 上：批量 AI 废话 ----------
    a1 = ease_out(seg(t, 5.35, 5.9))
    if a1 > 0:
        y = 510 + int(20 * (1 - a1))
        rrect(d, [84, y, 996, y + 290], 18, fill=A((20, 16, 17), a1),
              outline=A((92, 40, 40), a1), width=2)
        a_x = ease_out(seg(t, 8.6, 9.1))
        if a_x > 0:
            d.ellipse([116, y + 32, 190, y + 106], fill=A((58, 22, 22), a_x), outline=A(RED, a_x), width=3)
            d.line([137, y + 53, 169, y + 85], fill=A(RED, a_x), width=8)
            d.line([169, y + 53, 137, y + 85], fill=A(RED, a_x), width=8)
        d.text((216, y + 40), "批量 AI 废话", font=font(50), fill=A((242, 200, 200), a1))

        # 水文示例条
        bars = [0.92, 0.86, 0.94]
        for i, bwf in enumerate(bars):
            if a1 <= 0: continue
            by = y + 122 + i * 52
            rrect(d, [116, by, 116 + int(540 * bwf), by + 32], 8, fill=A((44, 34, 36), a1))

        # 印章
        a_s = ease_out(seg(t, 8.8, 9.3))
        if a_s > 0:
            img = stamp(img, 780, y + 168, "AI 不读", RED, 320, 118, -9, a_s, 64)
            d = ImageDraw.Draw(img)
        if a_x > 0:
            d.text((116, y + 252), "判定：噪音 · 不收录", font=font(28), fill=A((255, 120, 120), a_x), anchor="lm")

    # ---------- 下：真实优势（先占位） ----------
    a_ph = ease_out(seg(t, 5.5, 6.1)) * 0.20
    if a_ph > 0:
        rrect(d, [84, 840, 996, 1130], 18, fill=A((14, 22, 18), a_ph),
              outline=A((34, 110, 70), a_ph), width=2)
        d.text((540, 985), "?", font=font(88), fill=A((40, 90, 66), min(0.5, a_ph * 2.5)), anchor="mm")

    a2 = ease_out(seg(t, 11.0, 11.6))
    if a2 > 0:
        y = 840 + int(20 * (1 - a2))
        rrect(d, [84, y, 996, y + 290], 18, fill=A((14, 22, 18), a2),
              outline=A((36, 118, 74), a2), width=2)
        a_g = ease_out(seg(t, 15.4, 15.9))
        if a_g > 0:
            d.ellipse([116, y + 32, 190, y + 106], fill=A((18, 52, 34), a_g), outline=A(GREEN, a_g), width=3)
            d.line([133, y + 70, 150, y + 88], fill=A(GREEN, a_g), width=8)
            d.line([150, y + 88, 175, y + 52], fill=A(GREEN, a_g), width=8)
        d.text((216, y + 40), "真实优势 + 核心观点", font=font(50), fill=A((200, 245, 220), a2))

        items = [("真实优势", "经验 / 数据 / 案例", 0),
                 ("核心观点", "结论明确", 1),
                 ("结构清晰", "逻辑分明", 2)]
        for name, desc, i in items:
            ai = ease_out(seg(t, 11.6 + i * 0.45, 12.1 + i * 0.45))
            if ai <= 0: continue
            iy = y + 128 + i * 54
            d.ellipse([122, iy + 10, 138, iy + 26], fill=A(GREEN, ai))
            d.text((156, iy), name, font=font(29), fill=A(GREEN_L, ai))
            d.text((300, iy + 2), desc, font=font(26), fill=A((130, 170, 148), ai))

        a_s2 = ease_out(seg(t, 15.7, 16.2))
        if a_s2 > 0:
            img = stamp(img, 800, y + 178, "高权重收录", GREEN, 300, 104, 8, a_s2, 48)
            d = ImageDraw.Draw(img)

    return footer(img, t, "水文越多，AI 越不信你", GREEN_L, 16.3)


# ================= 贴片3：投放矩阵 12.41s =================
def card3(t):
    img = base()
    d = ImageDraw.Draw(img)
    header(img, t, "3", "投放矩阵", "按体量选路，别乱花钱")

    rows = [
        ("本地中小店", "垂直问答 / 论坛", "自己写，成本 0", "半小时出一篇", BLUE, 2.6),
        ("规模化企业", "主流新闻源通发", "几十到百来块一篇", "快速提权", ORANGE, 6.3),
    ]
    y = 520
    for name, ch, cost, note, col, t_on in rows:
        a = ease_out(seg(t, t_on, t_on + 0.55))
        if a <= 0:
            y += 330; continue
        yy = y + int(24 * (1 - a))
        rrect(d, [84, yy, 996, yy + 290], 20, fill=A(CARD, a), outline=A(col, a * 0.45), width=2)
        rrect(d, [84, yy, 96, yy + 290], 6, fill=A(col, a))
        d.text((128, yy + 34), name, font=font(48), fill=A(WHITE, a))
        d.text((128, yy + 104), ch, font=font(34), fill=A(col, a))
        d.line([128, yy + 164, 950, yy + 164], fill=A((40, 44, 56), a), width=2)
        d.text((128, yy + 190), "成本", font=font(26), fill=A(DIM, a))
        d.text((128, yy + 226), cost, font=font(38), fill=A((214, 222, 236), a))
        d.text((700, yy + 226), note, font=font(28), fill=A(col, a))
        y += 330

    return footer(img, t, "花小钱，占住 AI 推荐位", ORANGE_L, 10.4)


CARDS = {"c1": (card1, 17.38), "c2": (card2, 18.05), "c3": (card3, 12.41)}

if __name__ == "__main__":
    import subprocess
    os.makedirs(OUT, exist_ok=True)
    names = {"c1": "贴片1_逆向工程", "c2": "贴片2_抓取喜好", "c3": "贴片3_投放矩阵"}
    for k, (fn, dur) in CARDS.items():
        path = os.path.join(OUT, names[k] + ".mp4")
        n = int(round(dur * FPS))
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
               "-c:v", "libx264", "-preset", "medium", "-crf", "18",
               "-pix_fmt", "yuv420p", "-g", "50", "-movflags", "+faststart", path]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(n):
            p.stdin.write(fn(i / FPS).convert("RGB").tobytes())
        p.stdin.close(); p.wait()
        print("  %s %.2fs" % (names[k], dur))
