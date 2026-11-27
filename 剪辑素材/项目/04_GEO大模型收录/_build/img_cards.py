# -*- coding: utf-8 -*-
"""把老板的 3:2 原图做成竖屏贴片段（模糊背景 + 缓推）"""
import subprocess, os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

W, H, FPS = 1080, 1920, 25
SRC = "/Users/jiacong/Downloads/剪辑素材/项目/04_GEO大模型收录/02_贴片/原图"
OUT = "/Users/jiacong/Downloads/剪辑素材/项目/04_GEO大模型收录/02_贴片"

_cache = {}

def prep(path):
    if path in _cache: return _cache[path]
    src = Image.open(path).convert("RGB")
    bw = int(H * src.size[0] / src.size[1])
    bg = src.resize((bw, H), Image.LANCZOS).crop(((bw - W) // 2, 0, (bw - W) // 2 + W, H))
    bg = bg.filter(ImageFilter.GaussianBlur(50))
    bg = ImageEnhance.Brightness(bg).enhance(0.30)
    bg = ImageEnhance.Color(bg).enhance(1.35)
    _cache[path] = (src, bg)
    return src, bg


def frame(path, t, dur, zoom=1.06, y=556, fw=1080):
    src, bg = prep(path)
    fh = int(fw * 1080 / 1536)
    s = 1.0 + (zoom - 1.0) * (t / max(dur, 0.01))
    w, h = int(fw * s), int(fh * s)
    fg = src.resize((w, h), Image.LANCZOS)
    canvas = bg.copy()
    x0 = (W - w) // 2
    y0 = y - (h - fh) // 2
    canvas.paste(fg, (x0, y0))
    gl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(gl).rounded_rectangle([x0 - 2, y0 - 2, x0 + w + 2, y0 + h + 2],
                                         radius=8, outline=(70, 150, 255, 130), width=3)
    canvas = Image.alpha_composite(canvas.convert("RGBA"),
                                   gl.filter(ImageFilter.GaussianBlur(9))).convert("RGB")
    return canvas


def render(name, path, dur, **kw):
    out = os.path.join(OUT, name + ".mp4")
    n = int(round(dur * FPS))
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", "-g", "50", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(path, i / FPS, dur, **kw).tobytes())
    p.stdin.close(); p.wait()
    print("  %s %.2fs" % (name, dur))


if __name__ == "__main__":
    render("图版1_引用来源", f"{SRC}/01_引用来源.jpg", 17.38, zoom=1.07, y=556)
    render("图版3_低成本路径", f"{SRC}/03_低成本路径.jpg", 12.41, zoom=1.09, y=572)
