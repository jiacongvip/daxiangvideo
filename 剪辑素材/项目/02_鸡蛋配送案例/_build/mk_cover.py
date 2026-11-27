# -*- coding: utf-8 -*-
"""恢复 v1，并出一个「只加对比、不改版式」的 v3"""
import subprocess, os

FF = "/Users/jiacong/.local/bin/ffmpeg"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
BASE = "/Users/jiacong/Downloads/剪辑素材/项目/02_鸡蛋配送案例"
BG = os.path.join(BASE, "02_贴片图", "真实截图", "03_配送批次列表_含框统计.png")
OUT1 = os.path.join(BASE, "04_成片", "封面_鸡蛋配送案例_1080x1920.png")
OUT3 = os.path.join(BASE, "04_成片", "封面_鸡蛋配送案例_加强对比.png")

Y = "0xFFD24D"
W = "white"


def T(t, x, y, s, c, bd=0):
    extra = f":borderw={bd}:bordercolor=black" if bd else ""
    return (f"drawtext=fontfile='{FONT}':text='{t}':x={x}:y={y}:"
            f"fontsize={s}:fontcolor={c}:expansion=none{extra}")


def build(out, border=0, sub_color="0xD6DEEA"):
    steps = [
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "gblur=sigma=24,eq=brightness=-0.12:saturation=0.72,"
        "drawbox=x=0:y=0:w=1080:h=1920:color=0x05090F@0.70:t=fill,"
        "drawbox=x=0:y=0:w=1080:h=1920:color=0x05090F@0.18:t=fill[a]",
        "[a]" + T("真实客户案例 · 已脱敏", 80, 112, 40, Y, border) + "[b]",
        "[b]drawbox=x=80:y=168:w=430:h=4:color=" + Y + ":t=fill[c]",
        "[c]" + T("卖鸡蛋", 195, 430, 230, W, border) + "[d]",
        "[d]" + T("卖出一个", 105, 738, 165, W, border) + "[e]",
        "[e]" + T("亿", 775, 705, 230, Y, border) + "[f]",
        "[f]" + T("一个城市 · 系统是我们做的", 155, 1015, 62, sub_color, border) + "[g]",
        "[g]drawbox=x=55:y=1535:w=970:h=4:color=0xFF4D4F:t=fill[h]",
        "[h]" + T("谁还说实体生意难做？", 55, 1585, 92, Y, border) + "[out]",
    ]
    cmd = [FF, "-hide_banner", "-loglevel", "error", "-y", "-i", BG,
           "-filter_complex", ";".join(steps), "-map", "[out]",
           "-frames:v", "1", "/tmp/base.png"]
    subprocess.run(cmd, check=True)

    cmd2 = [FF, "-hide_banner", "-loglevel", "error", "-y", "-i", "/tmp/base.png",
            "-i", BG, "-filter_complex",
            "[1:v]scale=980:389:flags=lanczos,pad=996:405:8:8:color=white,"
            "eq=brightness=-0.02[s];"
            "[0:v][s]overlay=42:1080[o];"
            "[o]drawbox=x=598:y=1310:w=106:h=126:color=0xFFD24D:t=4[o2]",
            "-map", "[o2]", "-frames:v", "1", out]
    subprocess.run(cmd2, check=True)
    print("ok", os.path.basename(out))


build(OUT1, border=0)                    # 原版
build(OUT3, border=5, sub_color="white")  # 只加描边、副标提亮
