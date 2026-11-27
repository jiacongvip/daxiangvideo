# -*- coding: utf-8 -*-
"""鸡蛋配送案例 · 画面层合成（无字幕，字幕最后统一烧）"""
import subprocess, os, json, re

FF = "/Users/jiacong/.local/bin/ffmpeg"
P = "/Users/jiacong/Downloads/剪辑素材/项目/02_鸡蛋配送案例"
WK = os.path.join(P, "_build")
SHOT = os.path.join(P, "02_贴片图", "真实截图")
PIPM = os.path.join(WK, "pipm.png")
PIPP = os.path.join(WK, "pipp.png")

C1 = os.path.join(P, "03_数字人视频", "01_0到18秒.mp4")
C2 = os.path.join(P, "03_数字人视频", "02_18到26秒.mp4")
C3 = os.path.join(P, "03_数字人视频", "03_26到54秒.mp4")
C4 = os.path.join(P, "03_数字人视频", "04_54到81秒.mp4")

TL = {int(k): v for k, v in json.load(open(os.path.join(WK, "timeline.json"))).items()}
END = 81.11


def T(i, k=0):
    return TL[i][k]


def E(i):
    return TL[i][1]


# 需要打码的区域（源图像素坐标 x,y,w,h）
PRECROP = {
    "06_配送员端_智能排单与专属会员.png": (0, 188, 376, 473),
}

DESENS = {
    "07_配送员端_智能排单_按远近顺路地图.png": [
        (55, 135, 68, 16),     # 国雅大厦（卡1）
        (55, 343, 68, 16),     # 国雅大厦（卡2）
        (52, 482, 165, 80),    # 西城便利店 / 李四 / 两个真实地址
    ],
}

SEGS = [
    ("v01", "full", 0.00, 1.85, None, C1, 0.00),
    ("v01b", "dash", 1.85, T(3, 0), "数据看板_示意.png", C1, 1.85),
    ("v01c", "full", T(3, 0), T(6, 0), None, C1, T(3, 0)),
    ("v02", "shot", T(6, 0), T(7, 0), "图1_拓客定价.png", C2, 0.00),
    ("v03", "phone", T(7, 0), T(8, 0), "02_业务员_帮他下单_红圈标注.png", C3, 0.00),
    ("v04", "full", T(8, 0), T(9, 0), None, C3, T(8, 0) - 26.00),
    ("v05", "shot", T(9, 0), T(10, 0), "03_配送批次列表_含框统计.png", C3, T(9, 0) - 26.00),
    ("v06", "phone", T(10, 0), T(11, 0), "06_配送员端_智能排单与专属会员.png", C3, T(10, 0) - 26.00),
    ("v07", "full", T(11, 0), T(12, 0), None, C3, T(11, 0) - 26.00),
    ("v08", "shot", T(12, 0), T(13, 0), "04_配送设置_批次与退框开关.png", C4, T(12, 0) - 53.80),
    ("v09", "shot", T(13, 0), T(14, 0), "08_退框记录_筐数与退款明细.png", C4, T(13, 0) - 53.80),
    ("v10", "full", T(14, 0), 73.13, None, C4, T(14, 0) - 53.80),
    ("v10b", "dash", 73.13, E(14), "数据看板_示意.png", C4, 73.13 - 53.80),
    ("v11", "full", E(14), END, None, C4, E(14) - 53.80),
]

X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "25", "-g", "50",
        "-profile:v", "high", "-level", "4.2"]

AREA_TOP, AREA_BOT = 380, 1280          # 主视觉可用区
PIP_X, PIP_Y, PIP_W, PIP_H = 700, 165, 220, 281


def run(cmd, tag):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print("FAIL", tag)
        print(" ".join(cmd)[:2200])
        print(r.stderr[-2500:])
        raise SystemExit(1)


def props(path):
    out = subprocess.run([FF, "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"(\d{2,5})x(\d{2,5})", out.split("Stream")[1])
    return int(m.group(1)), int(m.group(2))


def make_pip_assets():
    def rounded_alpha(w, h, r):
        xr, yb = w - 1 - r, h - 1 - r
        def c(cx, cy):
            return f"255*clip({r}-hypot({cx}-X,{cy}-Y)+0.5,0,1)"
        return (f"if(lt(X,{r})*lt(Y,{r}),{c(r,r)},if(gt(X,{xr})*lt(Y,{r}),{c(xr,r)},"
                f"if(lt(X,{r})*gt(Y,{yb}),{c(r,yb)},if(gt(X,{xr})*gt(Y,{yb}),{c(xr,yb)},255))))")
    for path, w, h, r in [(PIPM, PIP_W, PIP_H, 20), (PIPP, PIP_W + 12, PIP_H + 12, 23)]:
        run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
             "-i", f"color=c=white:s={w}x{h}:d=1", "-vf",
             f"format=rgba,geq=r=255:g=255:b=255:a='{rounded_alpha(w,h,r)}'",
             "-frames:v", "1", path], "mask")


def build_seg(name, kind, t0, t1, asset, clip, coff):
    dur = t1 - t0
    ins, fc = ["-ss", f"{coff:.3f}", "-t", f"{dur:.3f}", "-i", clip], []

    if kind == "full":
        fc.append("[0:v]fps=25,setpts=PTS-STARTPTS,crop=552:984:106:40,"
                  "scale=1080:1920:flags=lanczos,setsar=1,"
                  "zoompan=z='min(1+0.00025*on,1.035)':x='iw/2-(iw/zoom/2)':"
                  "y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=25[v]")
    else:
        img = os.path.join(SHOT, asset)
        if not os.path.exists(img):
            img = os.path.join(P, "02_贴片图", asset)
        iw, ih = props(img)
        if asset in PRECROP:
            _, cy, _, chh = PRECROP[asset]
            ih = chh
        ins += ["-loop", "1", "-framerate", "25", "-i", img,
                "-loop", "1", "-i", PIPM, "-loop", "1", "-i", PIPP]
        boxes = DESENS.get(asset, [])
        # 图像预处理：打码 → 缩放
        if boxes:
            n = len(boxes) + 1
            fc.append("[1:v]format=rgb24,split=" + str(n) + "[p0]" +
                      "".join(f"[p{i+1}]" for i in range(len(boxes))))
            cur = "p0"
            for k, (x, y, w, h) in enumerate(boxes):
                fc.append(f"[p{k+1}]crop={w}:{h}:{x}:{y},gblur=sigma=16[b{k}]")
                fc.append(f"[{cur}][b{k}]overlay={x}:{y}[q{k}]")
                cur = f"q{k}"
            fc.append(f"[{cur}]split=2[sbg][scd]")
        else:
            if asset in PRECROP:
                cx0, cyy, cw, chh = PRECROP[asset]
                fc.append(f"[1:v]crop={cw}:{chh}:{cx0}:{cyy},format=rgb24,split=2[sbg][scd]")
            else:
                fc.append("[1:v]format=rgb24,split=2[sbg][scd]")

        fc.append("[sbg]scale=1080:1920:force_original_aspect_ratio=increase,"
                  "crop=1080:1920,gblur=sigma=30,eq=brightness=-0.26:saturation=0.55,"
                  "drawbox=x=0:y=0:w=1080:h=1920:color=0x060A14@0.5:t=fill[bg]")

        if kind in ("dash", "phone"):
            AH = AREA_BOT - AREA_TOP
            if kind == "dash":
                th = AH
                tw = int(round(th * 1080 / 1200))
                tw += tw % 2
            else:
                tw = 660
                th = int(round(ih * tw / iw))
                if th > AH:
                    th = AH
                    tw = int(round(iw * th / ih))
                th += th % 2
                tw += tw % 2
            ty = AREA_TOP + (AREA_BOT - AREA_TOP - th) // 2
            fad = ",format=rgba,fade=t=in:st=0:d=0.35:alpha=1" if kind == "dash" else ""
            fc.append(f"[scd]scale={tw}:{th}:flags=lanczos,"
                      f"pad={tw+14}:{th+14}:7:7:color=0xE7EEFA{fad}[card]")
            fc.append(f"[bg][card]overlay={(1080-tw-14)//2}:{ty-7}[t0]")
        else:
            th = min(AREA_BOT - AREA_TOP, int(round(ih * 1.45)))
            th += th % 2
            tw = int(round(iw * th / ih))
            tw += tw % 2
            ty = AREA_TOP + (AREA_BOT - AREA_TOP - th) // 2
            if tw > 1080:
                fc.append(f"[scd]scale={tw}:{th}:flags=lanczos,"
                          f"crop=1080:{th}:{tw-1080}*t/{dur:.3f}:0[card]")
                fc.append(f"[bg][card]overlay=0:{ty}[t0]")
            else:
                fc.append(f"[scd]scale={tw}:{th}:flags=lanczos,"
                          f"pad={tw+14}:{th+14}:7:7:color=white[card]")
                fc.append(f"[bg][card]overlay={(1080-tw-14)//2}:{ty-7}[t0]")

        fc.append("[0:v]fps=25,setpts=PTS-STARTPTS,crop=768:984:0:40,"
                  f"scale={PIP_W}:{PIP_H}:flags=lanczos,setsar=1[hu]")
        fc.append("[hu][2:v]alphamerge[hm]")
        fc.append(f"[t0][3:v]overlay={PIP_X-6}:{PIP_Y-6}[t1]")
        fc.append(f"[t1][hm]overlay={PIP_X}:{PIP_Y}[v]")

    out = os.path.join(WK, f"{name}.mp4")
    run([FF, "-hide_banner", "-loglevel", "error", "-y"] + ins +
        ["-filter_complex", ";".join(fc), "-map", "[v]", "-t", f"{dur:.3f}"] +
        X264 + [out], name)
    print(f"  {name}  {t0:6.2f}-{t1:6.2f} ({dur:5.2f}s)  {kind:5s} {asset or ''}")


if __name__ == "__main__":
    make_pip_assets()
    outs = []
    for s in SEGS:
        build_seg(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
        outs.append(os.path.join(WK, s[0] + ".mp4"))
    lst = os.path.join(WK, "vlist.txt")
    open(lst, "w").write("".join(f"file '{o}'\n" for o in outs))
    run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", lst, "-c", "copy", os.path.join(WK, "video.mp4")], "concat")
    d = subprocess.run([FF, "-hide_banner", "-i", os.path.join(WK, "video.mp4")],
                       capture_output=True, text=True).stderr
    print("完成:", [l for l in d.split("\n") if "Duration" in l][0].strip())
