# -*- coding: utf-8 -*-
"""用老板给的三张 16:9 原图做竖屏贴片段（模糊背景 + 前景推拉）"""
import subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H, FPS = 1080, 1920, 25
SRC = "/Users/jiacong/Downloads/剪辑素材/项目/03_体检中心推三返一/02_贴片/原图"
OUT = "/Users/jiacong/Downloads/剪辑素材/项目/03_体检中心推三返一/02_贴图版"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"


def prep(path):
    src = Image.open(path).convert("RGB")
    bw = int(H * 16 / 9)
    bg = src.resize((bw, H), Image.LANCZOS).crop(((bw - W) // 2, 0, (bw - W) // 2 + W, H))
    bg = bg.filter(ImageFilter.GaussianBlur(48))
    bg = ImageEnhance.Brightness(bg).enhance(0.32)
    bg = ImageEnhance.Color(bg).enhance(1.3)
    return src, bg


def frame(src, bg, t, dur, fw=1000, zoom=1.05, y=596, fade=0.35, overlay=None):
    """t 段内秒"""
    p = t / max(dur, 0.01)
    s = 1.0 + (zoom - 1.0) * p
    fh = int(fw * 1080 / 1920)
    w, h = int(fw * s), int(fh * s)
    fg = src.resize((w, h), Image.LANCZOS)
    canvas = bg.copy()
    yy = y - (h - fh) // 2
    canvas.paste(fg, ((W - w) // 2, yy))
    # 边缘发光框
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle([(W - w) // 2 - 2, yy - 2, (W - w) // 2 + w + 2, yy + h + 2],
                                           radius=8, outline=(120, 170, 255, 110), width=3)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(8)))
    canvas = canvas.convert("RGB")

    if overlay:
        canvas = overlay(canvas, t, dur, yy + h)

    if fade > 0:
        a = min(1.0, t / fade, (dur - t) / fade)
        a = max(0.0, min(1.0, a))
        if a < 1.0:
            canvas = Image.blend(bg, canvas, a)
    return canvas


def _ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def _seg(t, a, b):
    if b <= a: return 1.0 if t >= b else 0.0
    return max(0.0, min(1.0, (t - a) / (b - a)))


def overlay_round4(img, t, dur, y_bottom):
    """段4 叠加：20 张送出 → 3 人转化 → 2000 全退"""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = lambda s: ImageFont.truetype(FONT, s)
    GOLD = (255, 214, 110)
    GREEN = (60, 226, 160)

    steps = [
        (0.6, 4.6, "20 张卡，已经送出去", (200, 214, 245)),
        (4.6, 8.8, "只要 3 个人转化", GOLD),
        (8.8, 99, "2000 块，直接全退", GREEN),
    ]
    for a0, a1, txt, col in steps:
        a = _ease(_seg(t, a0, a0 + 0.45)) * (1 - _ease(_seg(t, a1 - 0.35, a1)))
        if a <= 0.01: continue
        cy = y_bottom + 96
        tw = f(58).getbbox(txt)[2]
        pad = 54
        d.rounded_rectangle([540 - tw / 2 - pad, cy - 52, 540 + tw / 2 + pad, cy + 52],
                            radius=52, fill=(8, 12, 36, int(235 * a)),
                            outline=col + (int(210 * a),), width=3)
        d.text((540, cy), txt, font=f(58), fill=col + (int(255 * a),), anchor="mm")
    return Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")


def render(name, path, dur, **kw):
    src, bg = prep(path)
    out = os.path.join(OUT, name + ".mp4")
    n = int(round(dur * FPS))
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-g", "50", "-movflags", "+faststart", out]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        pr.stdin.write(frame(src, bg, i / FPS, dur, **kw).tobytes())
    pr.stdin.close()
    pr.wait()
    print("  %s %.2fs" % (name, dur))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    render("图版1_1拖20", f"{SRC}/01_1拖20赠卡裂变.png", 15.17, zoom=1.06)
    render("图版2_私域关系链", f"{SRC}/02_私域关系链.png", 5.85, zoom=1.04)
    render("图版3_推三返一", f"{SRC}/03_推三返一3单回本.png", 6.56, zoom=1.05)
    render("图版4_三单回本", f"{SRC}/03_推三返一3单回本.png", 14.40, zoom=1.09, y=470, overlay=overlay_round4)
