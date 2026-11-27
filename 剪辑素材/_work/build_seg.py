# -*- coding: utf-8 -*-
"""构建 1080x1920 口播成片 —— 分段合成 + 拼接"""
import subprocess, os

W, H, FPS = 1080, 1920, 25
FF = "/Users/jiacong/.local/bin/ffmpeg"
ROOT = "/Users/jiacong/Downloads/剪辑素材"
WK = os.path.join(ROOT, "_work")
OUT = os.path.join(ROOT, "成片")
os.makedirs(OUT, exist_ok=True)

V80 = os.path.join(ROOT, "pl-WanVideo2_1_multitalk_00001_p80-audio_flmij_1793286741.mp4")
V85 = os.path.join(ROOT, "pl-WanVideo2_1_multitalk_00001_p85-audio_kcthc_1793287603.mp4")
V87 = os.path.join(ROOT, "pl-WanVideo2_1_multitalk_00001_p87-audio_lsoyc_1793279696.mp4")
A1 = os.path.join(WK, "aud", "xiaren_00001_qycia_1793278300.wav")
A2 = os.path.join(WK, "aud", "xiaren_00001_uladl_1793278431.wav")
A3 = os.path.join(WK, "aud", "ComfyUI_00001_gbccs_1793278563.wav")
IMG1 = os.path.join(ROOT, "tmpe0kfyofx.jpeg")
IMG2 = os.path.join(ROOT, "tmp8iipmqo_.png")
SHOT = os.path.join(ROOT, "pasted_image_1793288700529_oa0z0z_0.png")
DASH = os.path.join(WK, "dashboard.png")
MASK = os.path.join(WK, "pip_mask.png")
PLATE = os.path.join(WK, "pip_plate.png")
SCRIM = os.path.join(WK, "scrim.png")
PHMASK = os.path.join(WK, "phone_mask.png")
PHPLATE = os.path.join(WK, "phone_plate.png")
ROLL = os.path.join(WK, "phoneroll.mp4")

SEGS = [
    dict(name="s1", src=V87, a=A1, st=0.00, frames=171, kind="full"),
    dict(name="s2", src=V87, a=A1, st=6.84, frames=314, kind="pip"),
    dict(name="s3", src=V80, a=A2, st=0.00, frames=389, kind="screen"),
    dict(name="s4", src=V80, a=A2, st=15.56, frames=350, kind="pip2"),
    dict(name="s5", src=V85, a=A3, st=0.00, frames=266, kind="full"),
]
t = 0.0
for s in SEGS:
    s["start"] = t
    s["dur"] = s["frames"] / FPS
    t += s["dur"]
TOTAL = t

X264 = ["-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "50",
        "-profile:v", "high", "-level", "4.2"]


def run(cmd, tag=""):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAIL", tag)
        print(" ".join(cmd)[:2500])
        print(r.stderr[-3500:])
        raise SystemExit(1)


class G:
    def __init__(self):
        self.inputs, self.fc, self.n = [], [], 0

    def add(self, pre, path):
        self.inputs.extend(pre + ["-i", path])
        i = self.n
        self.n += 1
        return i

    def f(self, s):
        self.fc.append(s)


def dark_bg(g, idx, src_label, out, blur=30, bright=-0.28, sat=0.55, tint="0x050A14@0.45"):
    g.f(f"[{src_label}]scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,gblur=sigma={blur},"
        f"eq=brightness={bright}:saturation={sat},"
        f"drawbox=x=0:y=0:w=1080:h=1920:color={tint}:t=fill[{out}]")


def seg_command(s, out_path):
    dur = s["dur"]
    kind = s["kind"]
    g = G()
    v0 = g.add(["-ss", f"{s['st']:.3f}", "-t", f"{dur:.3f}"], s["src"])

    if kind == "full":
        si = g.add(["-loop", "1"], SCRIM)
        g.f(f"[{v0}:v]fps={FPS},setpts=PTS-STARTPTS,crop=550:978:153:46,"
            f"scale=1080:1920:flags=lanczos,setsar=1,"
            f"zoompan=z='min(1+0.00035*on,1.040)':x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS}[b]")
        g.f(f"[b][{si}:v]overlay=0:0:shortest=1[v]")

    elif kind in ("pip", "pip2"):
        if kind == "pip":
            shots = [(IMG1, dur, 40, 520, 1000)]
        else:
            shots = [(IMG2, 5.0, 40, 520, 1000), (DASH, dur - 5.0, 90, 500, 900)]
        # 各镜头
        for k, (img, sdur, x, y, size) in enumerate(shots):
            i_img = g.add(["-loop", "1"], img)
            g.f(f"[{i_img}:v]format=rgb24,split=2[b{k}][m{k}]")
            dark_bg(g, i_img, f"b{k}", f"bg{k}")
            g.f(f"[m{k}]scale={size}:-1:flags=lanczos[m{k}s]")
            g.f(f"[bg{k}][m{k}s]overlay={x}:{y}[t{k}]")
            g.f(f"[t{k}]trim=0:{sdur:.3f},setpts=PTS-STARTPTS,"
                f"fps={FPS},format=yuv420p[s{k}]")
        if len(shots) == 1:
            g.f("[s0]null[vshots]")
        else:
            g.f("".join(f"[s{k}]" for k in range(len(shots))) +
                f"concat=n={len(shots)}:v=1:a=0[vshots]")
        # 画中画
        i_pl = g.add(["-loop", "1"], PLATE)
        i_mk = g.add(["-loop", "1"], MASK)
        g.f(f"[{v0}:v]fps={FPS},setpts=PTS-STARTPTS,crop=768:978:0:46,"
            f"scale=300:382:flags=lanczos,setsar=1[hu]")
        g.f(f"[hu][{i_mk}:v]alphamerge[hm]")
        g.f(f"[vshots][{i_pl}:v]overlay=713:83[t1]")
        g.f(f"[t1][hm]overlay=720:90[v]")

    elif kind == "screen":
        i_sh = g.add(["-loop", "1"], SHOT)
        i_pm = g.add(["-loop", "1"], PHMASK)
        i_pp = g.add(["-loop", "1"], PHPLATE)
        g.f(f"[{i_sh}:v]format=rgb24,split=3[i0][i1][i2]")
        # 镜头A：后台全貌
        dark_bg(g, i_sh, "i0", "bga", blur=34, bright=-0.30, sat=0.35, tint="0x060C18@0.62")
        g.f("[i1]crop=1060:745:170:55,scale=1050:738:flags=lanczos,pad=1062:750:6:6:color=white[a0]")
        g.f("[bga][a0]overlay=9:396:shortest=1[sa]")
        g.f("[sa]trim=0:6.5,setpts=PTS-STARTPTS,fps=25,format=yuv420p[va]")
        # 镜头B：多行业小程序轮播（滑动转场，已预渲染）
        dark_bg(g, i_sh, "i2", "bgb", blur=34, bright=-0.30, sat=0.35, tint="0x060C18@0.62")
        i_roll = g.add([], ROLL)
        g.f(f"[{i_roll}:v]setsar=1,fps={FPS},format=yuv420p[rv]")
        g.f(f"[rv][{i_pm}:v]alphamerge[pm]")
        g.f(f"[bgb][{i_pp}:v]overlay=265:351[tb0]")
        g.f(f"[tb0][pm]overlay=274:360[tb1]")
        g.f(f"[tb1]trim=0:{dur-6.5:.3f},setpts=PTS-STARTPTS,fps=25,format=yuv420p[vb]")
        g.f("[va][vb]concat=n=2:v=1:a=0,fps=25,format=yuv420p[v]")

    a_i = g.add(["-ss", f"{s['st']:.3f}", "-t", f"{dur:.3f}"], s["a"])
    g.f(f"[{a_i}:a]aresample=44100,aformat=channel_layouts=stereo,"
        f"atrim=0:{dur:.3f},apad=whole_dur={dur:.3f},asetpts=PTS-STARTPTS[a]")

    cmd = [FF, "-hide_banner", "-loglevel", "error", "-y"] + g.inputs + \
          ["-filter_complex", ";".join(g.fc), "-map", "[v]", "-map", "[a]"] + X264 + \
          ["-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
           "-t", f"{dur:.3f}", "-movflags", "+faststart", out_path]
    run(cmd, s["name"])


if __name__ == "__main__":
    print(f"总时长 {TOTAL:.2f}s / {sum(s['frames'] for s in SEGS)} 帧")
    for s in SEGS:
        print("渲染", s["name"], f"{s['start']:.2f} -> {s['start']+s['dur']:.2f}")
        seg_command(s, os.path.join(WK, f"{s['name']}.mp4"))
    lst = os.path.join(WK, "concat.txt")
    with open(lst, "w") as f:
        for s in SEGS:
            f.write(f"file '{os.path.join(WK, s['name'] + '.mp4')}'\n")
    run([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat",
         "-safe", "0", "-i", lst, "-c", "copy", os.path.join(WK, "base.mp4")], "concat")
    print("拼接完成")
