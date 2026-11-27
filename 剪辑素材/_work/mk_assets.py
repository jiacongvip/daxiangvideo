# -*- coding: utf-8 -*-
import subprocess, os
FF = "/Users/jiacong/.local/bin/ffmpeg"
WK = "/Users/jiacong/Downloads/剪辑素材/_work"


def rounded_alpha(w, h, r):
    xr, yb = w - 1 - r, h - 1 - r
    def c(cx, cy):
        return f"255*clip({r}-hypot({cx}-X,{cy}-Y)+0.5,0,1)"
    return (f"if(lt(X,{r})*lt(Y,{r}),{c(r,r)},"
            f"if(gt(X,{xr})*lt(Y,{r}),{c(xr,r)},"
            f"if(lt(X,{r})*gt(Y,{yb}),{c(r,yb)},"
            f"if(gt(X,{xr})*gt(Y,{yb}),{c(xr,yb)},255))))")


def make_rounded(path, w, h, r):
    a = rounded_alpha(w, h, r)
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                    "-i", f"color=c=white:s={w}x{h}:d=1",
                    "-vf", f"format=rgba,geq=r=255:g=255:b=255:a='{a}'",
                    "-frames:v", "1", path], check=True)


# 画中画：视频 300x382，底衬 314x396
make_rounded(os.path.join(WK, "pip_mask.png"), 300, 382, 24)
make_rounded(os.path.join(WK, "pip_plate.png"), 314, 396, 27)
make_rounded(os.path.join(WK, "phone_mask.png"), 532, 1002, 30)
make_rounded(os.path.join(WK, "phone_plate.png"), 550, 1020, 34)

# 上下渐变遮罩
expr = "255*clip(max(0.58*clip(1-Y/470,0,1),0.62*clip(1-(H-Y)/800,0,1)),0,1)"
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                "-i", "color=c=black:s=1080x1920:d=1",
                "-vf", f"format=rgba,geq=r=0:g=0:b=0:a='{expr}'",
                "-frames:v", "1", os.path.join(WK, "scrim.png")], check=True)
print("assets ok")
