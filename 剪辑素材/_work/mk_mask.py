# -*- coding: utf-8 -*-
import subprocess, os
FF = "/Users/jiacong/.local/bin/ffmpeg"
OUT = "/Users/jiacong/Downloads/剪辑素材/_work"

def rounded_alpha(w, h, r):
    xr = w - 1 - r
    yb = h - 1 - r
    def corner(cx, cy, sx, sy):
        return (f"255*clip({r}-hypot({cx}-X,{cy}-Y)+0.5,0,1)")
    tl = corner(r, r, 1, 1)
    tr = corner(xr, r, -1, 1)
    bl = corner(r, yb, 1, -1)
    br = corner(xr, yb, -1, -1)
    return (f"if(lt(X,{r})*lt(Y,{r}),{tl},"
            f"if(gt(X,{xr})*lt(Y,{r}),{tr},"
            f"if(lt(X,{r})*gt(Y,{yb}),{bl},"
            f"if(gt(X,{xr})*gt(Y,{yb}),{br},255))))")

def make(path, w, h, r, color="white"):
    a = rounded_alpha(w, h, r)
    cmd = [FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
           "-i", f"color=c={color}:s={w}x{h}:d=1",
           "-vf", f"format=rgba,geq=r=255:g=255:b=255:a='{a}'",
           "-frames:v", "1", path]
    subprocess.run(cmd, check=True)

make(os.path.join(OUT, "pip_mask.png"), 336, 428, 26)
make(os.path.join(OUT, "pip_plate.png"), 350, 442, 30)
print("ok")
