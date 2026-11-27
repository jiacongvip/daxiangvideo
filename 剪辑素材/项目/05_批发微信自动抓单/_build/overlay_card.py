# -*- coding: utf-8 -*-
"""钩子段：把「客户微信报单原文」做成一张浮卡，直接盖在数字人身上（不做上下分屏）"""
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 25
P = "/Users/jiacong/Downloads/剪辑素材/项目/05_批发微信自动抓单"
SRC = f"{P}/03_数字人视频/钩子_竖屏_25.73s.mp4"
SHOT1 = f"{P}/04_素材/截图_d9f8033cedc88c9a2c96631a91b7db4d.jpg"
SHOT2 = f"{P}/04_素材/截图_5febafa3f33a8842436cd3b68ab1efce.jpg"
OUT = f"{P}/03_数字人视频/钩子_浮卡_25.73s.mp4"
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"

T_IN, T_OUT = 5.42, 9.02     # 浮卡出现区间
TRANS = 0.32                  # 进出时长
CARD_W, CARD_H = 700, 1021
CX = (W - CARD_W) // 2
CY = 212
RADIUS = 22
CROP = (0, 110, 960, 1510)    # 去掉抖音界面，只留报单内容

_f = {}
def font(s, w=6):
    k = (s, w)
    if k not in _f:
        _f[k] = ImageFont.truetype(FONT, s, index=2 if w == 6 else 1)
    return _f[k]


def cover(im, box, sample):
    """手机号：用旁边干净的纸面色块抹掉，不留字迹"""
    reg = im.crop(sample)
    px = list(reg.getdata())
    avg = tuple(sum(p[i] for p in px) // len(px) for i in range(3))
    ImageDraw.Draw(im).rounded_rectangle(box, radius=5, fill=avg)


def prep(path, masks):
    im = Image.open(path).convert("RGB")
    for mb, sm in masks:
        cover(im, mb, sm)
    im = im.crop(CROP)
    # 预留 2 倍尺寸，方便内部缓推
    return im.resize((CARD_W * 2, CARD_H * 2), Image.LANCZOS)


S1 = prep(SHOT1, [((236, 652, 636, 748), (650, 665, 880, 720))])
S2 = prep(SHOT2, [((326, 1236, 512, 1296), (530, 1246, 780, 1284))])

MASK = Image.new("L", (CARD_W, CARD_H), 0)
ImageDraw.Draw(MASK).rounded_rectangle([0, 0, CARD_W - 1, CARD_H - 1], radius=RADIUS, fill=255)

# 阴影（固定尺寸，一次做好）
SP = 46
sh = Image.new("L", (CARD_W + SP * 2, CARD_H + SP * 2), 0)
ImageDraw.Draw(sh).rounded_rectangle([SP, SP, SP + CARD_W, SP + CARD_H], radius=RADIUS, fill=255)
sh = sh.filter(ImageFilter.GaussianBlur(22))
SHADOW_MASK = sh.point(lambda v: int(v * 0.55))


def content(t, dur):
    """卡片内部：前 2.1s 第一张，之后第二张，交叉淡入；全程缓推"""
    k = min(1.0, (t - T_IN) / max(0.1, dur))
    z = 1.0 + 0.05 * k
    def take(src):
        w2, h2 = int(CARD_W * 2 / z), int(CARD_H * 2 / z)
        x0 = (CARD_W * 2 - w2) // 2
        y0 = (CARD_H * 2 - h2) // 2
        return src.crop((x0, y0, x0 + w2, y0 + h2)).resize((CARD_W, CARD_H), Image.LANCZOS)
    seg = t - T_IN
    if seg < 2.10:
        return take(S1)
    if seg < 2.34:
        return Image.blend(take(S1), take(S2), (seg - 2.10) / 0.24)
    return take(S2)


def build_card(img):
    card = img.convert("RGBA")
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([1, 1, CARD_W - 2, CARD_H - 2], radius=RADIUS,
                        outline=(255, 255, 255, 235), width=3)
    return card


def frame(dh, t):
    if t < T_IN or t > T_OUT:
        return dh
    if t < T_IN + TRANS:
        p = (t - T_IN) / TRANS
    elif t > T_OUT - TRANS:
        p = (T_OUT - t) / TRANS
    else:
        p = 1.0
    p = max(0.0, min(1.0, p))
    e = 1 - (1 - p) ** 3          # ease-out
    dy = int(56 * (1 - e))        # 从下往上托起来

    canvas = dh.convert("RGB")
    canvas.paste((0, 0, 0), (CX - SP, CY - SP + dy), SHADOW_MASK)
    card = build_card(content(t, T_OUT - T_IN))

    f = e
    if f >= 0.999:
        canvas.paste(card, (CX, CY + dy), MASK)
    else:
        lut = bytes(int(i * f) for i in range(256))
        canvas.paste(card, (CX, CY + dy), MASK.point(lut))

    if e > 0.5:
        d = ImageDraw.Draw(canvas)
        lb = "客户微信报单原文"
        tw = int(font(25).getlength(lb))
        ty = CY + dy - 64
        bx = CX + 6
        d.rounded_rectangle([bx, ty, bx + tw + 58, ty + 48], radius=24, fill=(8, 10, 14))
        d.ellipse([bx + 18, ty + 18, bx + 30, ty + 30], fill=(7, 193, 96))
        d.text((bx + 40, ty + 24), lb, font=font(25), fill=(226, 232, 240), anchor="lm")
    return canvas


def main():
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", SRC, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    n = len(raw) // (W * H * 3)
    print("源帧数", n)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
           "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", OUT]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        dh = Image.frombytes("RGB", (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3])
        pr.stdin.write(frame(dh, i / FPS).tobytes())
    pr.stdin.close(); pr.wait()
    print("done", OUT)


if __name__ == "__main__":
    main()
