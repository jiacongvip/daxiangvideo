# -*- coding: utf-8 -*-
"""钩子段：讲「客户报来鸡蛋20箱…」时，上半屏展示原视频里的微信报单截图"""
import subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 25
P = "/Users/jiacong/Downloads/剪辑素材/项目/05_批发微信自动抓单"
SRC = f"{P}/03_数字人视频/钩子_竖屏_25.73s.mp4"
SHOT = f"{P}/04_素材/截图_d9f8033cedc88c9a2c96631a91b7db4d.jpg"
SHOT2 = f"{P}/04_素材/截图_5febafa3f33a8842436cd3b68ab1efce.jpg"
OUT = f"{P}/03_数字人视频/钩子_分屏_25.73s.mp4"
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"

T_IN, T_OUT = 5.42, 9.02      # 分屏区间
TRANS = 0.28                   # 过渡时长
TOP_H = 780                    # 上半屏高度
DH_Y0, DH_H = 320, 980         # 数字人取的纵向区间

_f = {}
def font(s, w=6):
    k = (s, w)
    if k not in _f:
        _f[k] = ImageFont.truetype(FONT, s, index=2 if w == 6 else 1)
    return _f[k]


def prep_shot(path, box, masks=()):
    im = Image.open(path).convert("RGB")
    from PIL import ImageDraw as _ID
    dd = _ID.Draw(im)
    for mb in masks:
        dd.rectangle(mb, fill=(182, 182, 182))
    im = im.crop(box)
    return im.resize((W, TOP_H), Image.LANCZOS)


def frame(dh, shots, t, dur):
    if t < T_IN or t > T_OUT:
        return dh
    if t < T_IN + TRANS:
        p = (t - T_IN) / TRANS
    elif t > T_OUT - TRANS:
        p = (T_OUT - t) / TRANS
    else:
        p = 1.0
    p = max(0.0, min(1.0, p))
    e = 1 - (1 - p) ** 3
    hgt = int(TOP_H * e)

    canvas = Image.new("RGB", (W, H), (0, 0, 0))
    if hgt > 0:
        seg_t = t - T_IN
        VN = len(VID) // (W * 780 * 3)
        k = min(1.0, seg_t / max(0.1, (T_OUT - T_IN)))
        z = 1.0 + 0.05 * k
        w2, h2 = int(W * z), int(780 * z)
        top = SHOT1.resize((w2, h2), Image.LANCZOS).crop(
            ((w2 - W) // 2, (h2 - 780) // 2, (w2 - W) // 2 + W, (h2 - 780) // 2 + 780))
        canvas.paste(top.crop((0, 780 - hgt, W, 780)), (0, 0))
    # 数字人下滑
    canvas.paste(dh.crop((0, 0, W, H - hgt)), (0, hgt))
    if hgt > 2:
        dr = ImageDraw.Draw(canvas)
        dr.rectangle([0, hgt - 3, W, hgt], fill=(255, 255, 255))
        if e > 0.55:
            lb = "客户微信报单原文"
            tw = font(26).getbbox(lb)[2]
            ty = hgt - 82
            bx1 = W - 40
            dr.rounded_rectangle([bx1 - tw - 44, ty, bx1, ty + 52], radius=26, fill=(0, 0, 0))
            dr.text((bx1 - tw - 22, ty + 26), lb, font=font(26), fill=(235, 240, 250), anchor="lm")
    return canvas


VID = open(f"{P}/_build/vid_seg.raw", "rb").read()
SHOT1 = prep_shot(SHOT, (0, 132, 1000, 912), masks=[(178, 664, 622, 745)])


def main():
    imgs = None
    dec = subprocess.run(["ffmpeg", "-v", "quiet", "-i", SRC, "-f", "rawvideo",
                          "-pix_fmt", "rgb24", "-"], capture_output=True)
    raw = dec.stdout
    n = len(raw) // (W * H * 3)
    print("源帧数", n)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
           "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", OUT]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        dh = Image.frombytes("RGB", (W, H), raw[i * W * H * 3:(i + 1) * W * H * 3])
        pr.stdin.write(frame(dh, imgs, i / FPS, n / FPS).tobytes())
    pr.stdin.close(); pr.wait()
    print("done", OUT)


if __name__ == "__main__":
    main()
