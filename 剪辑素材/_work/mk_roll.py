# -*- coding: utf-8 -*-
"""预渲染：4 张小程序首页在手机框内滑动轮播"""
import subprocess, os

FF = "/Users/jiacong/.local/bin/ffmpeg"
ROOT = "/Users/jiacong/Downloads/剪辑素材"
WK = os.path.join(ROOT, "_work")
IMGS = [os.path.join(ROOT, "素材", "小程序案例", n) for n in
        ["01_校园餐饮.png", "02_求职招聘.png", "03_会展活动.png", "04_大健康品牌.png"]]
DUR, XD, FPS = 2.6, 0.4, 25


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2000:])
        raise SystemExit(1)


# 1) 单张 -> 短片
clips = []
for k, p in enumerate(IMGS):
    out = os.path.join(WK, f"cr{k}.mp4")
    run([FF, "-hide_banner", "-loglevel", "error", "-y",
         "-loop", "1", "-framerate", str(FPS), "-i", p, "-t", f"{DUR}",
         "-vf", f"scale=532:1002:force_original_aspect_ratio=increase,crop=532:1002,"
                f"setsar=1,fps={FPS},format=yuv420p",
         "-c:v", "libx264", "-crf", "16", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-r", str(FPS), out])
    clips.append(out)

# 2) 滑动转场串联
ins = []
for c in clips:
    ins += ["-i", c]
fc = []
prev = "[0:v]"
for k in range(1, len(clips)):
    off = DUR - XD + (k - 1) * (DUR - XD)
    lbl = f"[x{k}]"
    fc.append(f"{prev}[{k}:v]xfade=transition=slideleft:duration={XD}:offset={off:.2f}{lbl}")
    prev = lbl
fc.append(f"{prev}trim=0:{(DUR-XD)*len(clips)+XD:.3f},setpts=PTS-STARTPTS,"
          f"fps={FPS},format=yuv420p[v]")
run([FF, "-hide_banner", "-loglevel", "error", "-y"] + ins +
    ["-filter_complex", ";".join(fc), "-map", "[v]",
     "-c:v", "libx264", "-crf", "16", "-preset", "medium",
     "-pix_fmt", "yuv420p", "-r", str(FPS), os.path.join(WK, "phoneroll.mp4")])
print("phoneroll ok")
