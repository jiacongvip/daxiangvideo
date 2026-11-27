# -*- coding: utf-8 -*-
"""GEO 选题 · 抖音爆款封面（人脸 + 大字钩子）"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1920
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
ROOT = "/Users/jiacong/Downloads/剪辑素材/项目/04_GEO大模型收录"
OUT = f"{ROOT}/04_成片"
COVER_DIR = f"{ROOT}/_build/_cover"
FACE = f"{COVER_DIR}/nosub_1.5s.png"

_fc = {}
def font(s, w=6):
    k = (s, w)
    if k not in _fc:
        # index 2 ≈ W6 in Hiragino Sans GB.ttc (same as mk_cover)
        _fc[k] = ImageFont.truetype(FONT, s, index=2 if w == 6 else 0)
    return _fc[k]

WHITE = (255, 255, 255)
GOLD  = (255, 214, 90)
ORANGE = (255, 92, 28)
RED   = (255, 48, 48)
RED_D = (220, 28, 36)
YELLOW = (255, 230, 70)
CREAM = (255, 248, 236)


def outlined_text(draw, xy, text, fnt, fill, outline=(0, 0, 0), ow=8, anchor="mm"):
    """Thick black outline for mobile readability."""
    x, y = xy
    # soft outer ring
    for dx in range(-ow, ow + 1):
        for dy in range(-ow, ow + 1):
            if dx * dx + dy * dy > ow * ow:
                continue
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=fnt, fill=outline, anchor=anchor)
    draw.text((x, y), text, font=fnt, fill=fill, anchor=anchor)


def draw_gradient_text_line(base, y, parts, fnt, ow=9, gap=0, anchor_center=True):
    """
    parts: list of (text, fill_color)
    Draws one horizontal line of mixed-color outlined glyphs, centered.
    """
    # measure
    widths = []
    for t, _ in parts:
        bbox = fnt.getbbox(t)
        widths.append(bbox[2] - bbox[0])
    total = sum(widths) + gap * max(0, len(parts) - 1)
    x = (W - total) // 2 if anchor_center else 60
    # draw onto transparent then composite (outline needs RGBA)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx = x
    for (t, fill), tw in zip(parts, widths):
        mid = cx + tw // 2
        outlined_text(d, (mid, y), t, fnt, fill=fill, outline=(0, 0, 0), ow=ow, anchor="mm")
        cx += tw + gap
    return Image.alpha_composite(base.convert("RGBA"), lay)


def stamp_oval(img, text="别被割韭菜", cx=860, cy=520, rx=168, ry=92, angle=-18):
    """Red oval stamp, rotated."""
    pad = 40
    tw, th = rx * 2 + pad * 2, ry * 2 + pad * 2
    stamp = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    box = [pad, pad, pad + rx * 2, pad + ry * 2]
    # outer ring
    sd.ellipse(box, outline=(220, 36, 40, 230), width=10)
    sd.ellipse([box[0] + 8, box[1] + 8, box[2] - 8, box[3] - 8], outline=(220, 36, 40, 200), width=3)
    f = font(42)
    # text along center
    outlined_text(sd, (tw // 2, th // 2), text, f, fill=(230, 40, 44, 240), outline=(80, 0, 0, 180), ow=3, anchor="mm")
    stamp = stamp.rotate(angle, resample=Image.BICUBIC, expand=True)
    sx = cx - stamp.width // 2
    sy = cy - stamp.height // 2
    img = img.convert("RGBA")
    img.alpha_composite(stamp, (sx, sy))
    return img


def prepare_face(path):
    """Close crop face to fill ~50%+, hide TL delogo, darken for text pop."""
    src = Image.open(path).convert("RGB")
    sw, sh = src.size  # 1080x1920

    # Crop out TL delogo residue (top ~80px) and tighten on face.
    # Face roughly centered; close crop: take mid band, scale up.
    # Source crop box focusing on head+shoulders
    # left, top, right, bottom in source
    crop = src.crop((40, 120, 1040, 1500))  # 1000x1380 — drop TL watermark zone
    # Scale to fill canvas width with some bleed for face size
    scale = W / crop.width * 1.18  # ~18% zoom → face fills more
    nw, nh = int(crop.width * scale), int(crop.height * scale)
    face = crop.resize((nw, nh), Image.LANCZOS)

    # Place face: center-x, slightly upper so chest leaves room for bottom text
    canvas = Image.new("RGB", (W, H), (12, 12, 16))
    ox = (W - nw) // 2
    oy = 80  # push up a bit
    canvas.paste(face, (ox, oy))

    # Soft dark vignette / gradient for text readability
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # top bar dark for tag
    for i in range(280):
        a = int(170 * (1 - i / 280))
        od.line([(0, i), (W, i)], fill=(0, 0, 0, a))
    # bottom heavy dark for big hooks
    for i in range(720):
        y = H - 1 - i
        a = int(210 * (1 - i / 720) ** 0.7)
        od.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    # mid soft band behind main title area (~y 980-1400)
    mid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    md = ImageDraw.Draw(mid)
    md.rectangle([0, 920, W, 1580], fill=(0, 0, 0, 110))
    mid = mid.filter(ImageFilter.GaussianBlur(40))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay)
    canvas = Image.alpha_composite(canvas, mid)

    # slight contrast bump
    rgb = canvas.convert("RGB")
    rgb = ImageEnhance.Contrast(rgb).enhance(1.08)
    rgb = ImageEnhance.Color(rgb).enhance(1.05)
    return rgb


def build():
    img = prepare_face(FACE)

    # --- top tag ---
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    tag = "GEO · 3步逆向信源"
    tf = font(34)
    # pill behind tag
    tb = tf.getbbox(tag)
    tw = tb[2] - tb[0]
    # y>=260 so Douyin crop (240–1680) keeps the tag
    pill = [W // 2 - tw // 2 - 36, 268, W // 2 + tw // 2 + 36, 328]
    d.rounded_rectangle(pill, radius=28, fill=(255, 92, 28, 210))
    d.text((W // 2, 298), tag, font=tf, fill=WHITE, anchor="mm")
    img = Image.alpha_composite(img.convert("RGBA"), lay)

    # --- main punch line 1 ---
    # 「千万别再花几万块」 — 几万 highlighted
    f1 = font(92)
    img = draw_gradient_text_line(
        img, 1020,
        [
            ("千万别再花", WHITE),
            ("几万块", ORANGE),
        ],
        f1, ow=10,
    )

    # --- line 2 ---
    f2 = font(72)
    img = draw_gradient_text_line(
        img, 1150,
        [
            ("找代运营刷", WHITE),
            ("GEO", GOLD),
            ("垃圾稿", RED),
        ],
        f2, ow=9,
    )

    # --- stinger ---
    f3 = font(86)
    img = draw_gradient_text_line(
        img, 1295,
        [
            ("大模型根本", WHITE),
            ("不读", RED),
        ],
        f3, ow=11,
    )

    # --- red stamp ---
    img = stamp_oval(img, text="别被割韭菜", cx=880, cy=620, rx=155, ry=86, angle=-22)

    # --- bottom tip bar ---
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    by = 1520
    d.rounded_rectangle([90, by, 990, by + 100], radius=50, fill=(14, 10, 8, 230), outline=ORANGE + (230,), width=4)
    d.text((540, by + 50), "今天一分钟讲透核心逻辑", font=font(40), fill=GOLD, anchor="mm")
    img = Image.alpha_composite(img.convert("RGBA"), lay)

    return img.convert("RGB")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(COVER_DIR, exist_ok=True)
    im = build()
    p1 = f"{OUT}/封面_爆款_1080x1920.png"
    p2 = f"{OUT}/封面_爆款_1080x1440_抖音.png"
    im.save(p1, optimize=True)
    im.crop((0, 240, 1080, 1680)).save(p2, optimize=True)
    # preview copies
    im.save(f"{COVER_DIR}/preview_爆款_1080x1920.png", optimize=True)
    im.crop((0, 240, 1080, 1680)).save(f"{COVER_DIR}/preview_爆款_1080x1440.png", optimize=True)
    print("ok", p1, os.path.getsize(p1))
    print("ok", p2, os.path.getsize(p2))
