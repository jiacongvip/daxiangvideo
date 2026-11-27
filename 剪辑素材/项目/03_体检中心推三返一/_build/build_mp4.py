# -*- coding: utf-8 -*-
"""把三张贴片渲染成 mp4（1080x1920 / 25fps）"""
import subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cards import card1, card2, card3
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 25
OUT = "/Users/jiacong/Downloads/剪辑素材/项目/03_体检中心推三返一/02_贴片"

JOBS = [
    ("贴片1_1拖20裂变流程", card1, 15.17),
    ("贴片2_推三返一阶梯算法", card2, 12.41),
    ("贴片3_三单回本逻辑", card3, 14.40),
]

def render(name, fn, dur):
    path = os.path.join(OUT, name + ".mp4")
    n = int(round(dur * FPS))
    cmd = ["ffmpeg", "-v", "error", "-y",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "slow", "-crf", "17",
           "-pix_fmt", "yuv420p", "-g", "50", "-movflags", "+faststart", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        img = fn(i / FPS).convert("RGB")
        p.stdin.write(img.tobytes())
    p.stdin.close()
    p.wait()
    print("  %s  %d帧  %.2fs" % (name, n, dur))

if __name__ == "__main__":
    for name, fn, dur in JOBS:
        render(name, fn, dur)
