# -*- coding: utf-8 -*-
"""Assemble GEO vertical short v1: 2 face + 3 Ken Burns stickers."""
import os, subprocess, math

FF = "/Users/jiacong/.local/bin/ffmpeg"
PROJ = "/Users/jiacong/Downloads/剪辑素材/项目/04_GEO大模型收录"
BUILD = os.path.join(PROJ, "_build")
OUT_DIR = os.path.join(PROJ, "04_成片")
AUD = os.path.join(PROJ, "01_脚本", "audio")
DH = os.path.join(PROJ, "03_数字人视频")
ST = os.path.join(PROJ, "02_贴片")
CHK = os.path.join(BUILD, "_chk")

W, H, FPS = 1080, 1920, 25

os.makedirs(BUILD, exist_ok=True)
os.makedirs(CHK, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

P81 = os.path.join(DH, "pl-WanVideo2_1_multitalk_00001_p81-audio_ftrrx_1793511822.mp4")
P84 = os.path.join(DH, "pl-WanVideo2_1_multitalk_00001_p84-audio_jnfpx_1793518989.mp4")

SEGS = [
    # (out_name, kind, src, audio, dur)
    ("seg1_face.mp4", "face", P81, os.path.join(AUD, "seg1_钩子.wav"), 10.740),
    ("seg2_face.mp4", "face", P84, os.path.join(AUD, "seg2_铺垫_三个步骤.wav"), 8.910),
    ("seg3_card.mp4", "card", os.path.join(ST, "预览_c1.png"), os.path.join(AUD, "seg3_第一步_逆向信源.wav"), 17.380),
    ("seg4_card.mp4", "card", os.path.join(ST, "预览_c2.png"), os.path.join(AUD, "seg4_第二步_定点投放.wav"), 18.050),
    ("seg5_card.mp4", "card", os.path.join(ST, "预览_c3.png"), os.path.join(AUD, "seg5_第三步_低成本放大.wav"), 12.410),
]

def run(cmd):
    print("+", " ".join(cmd[:8]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:] if r.stderr else "no stderr")
        raise SystemExit(f"ffmpeg failed: {cmd[:6]}")
    return r

def make_face(out, src, audio, dur):
    # scale height to 1920 → width 1440, crop center 1080x1920; replace audio
    # -t dur on output; -shortest also; aresample to 44100 stereo
    vf = "scale=-2:1920,crop=1080:1920,fps=25,format=yuv420p"
    cmd = [
        FF, "-y", "-v", "error",
        "-i", src,
        "-i", audio,
        "-map", "0:v:0", "-map", "1:a:0",
        "-vf", vf,
        "-t", f"{dur:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart",
        out,
    ]
    run(cmd)

def make_card(out, img, audio, dur):
    # Ken Burns via zoompan: 1.0 → 1.06 over exact frame count
    n = int(round(dur * FPS))
    # zoom starts at 1, increment so last frame ~1.06
    # z = min(zoom+inc, 1.06); with zoompan default zoom=1
    # inc = 0.06 / max(n-1,1)
    inc = 0.06 / max(n - 1, 1)
    # Keep x/y centered while zooming
    zexpr = f"min(zoom+{inc:.10f},1.06)"
    vf = (
        f"zoompan=z='{zexpr}':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={n}:s={W}x{H}:fps={FPS},format=yuv420p"
    )
    cmd = [
        FF, "-y", "-v", "error",
        "-loop", "1", "-i", img,
        "-i", audio,
        "-vf", vf,
        "-map", "0:v:0", "-map", "1:a:0",
        "-t", f"{dur:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart",
        out,
    ]
    run(cmd)

def main():
    paths = []
    for name, kind, src, audio, dur in SEGS:
        out = os.path.join(BUILD, name)
        print(f"== {name} ({kind}) {dur}s ==")
        if kind == "face":
            make_face(out, src, audio, dur)
        else:
            make_card(out, src, audio, dur)
        paths.append(out)
        # verify
        info = subprocess.run([FF, "-i", out], capture_output=True, text=True).stderr
        for line in info.splitlines():
            if "Duration" in line or "Video:" in line or "Audio:" in line:
                print(" ", line.strip())

    # concat demuxer
    lst = os.path.join(BUILD, "concat_list.txt")
    with open(lst, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")

    final = os.path.join(OUT_DIR, "成片_v1.mp4")
    print("== concat →", final)
    run([
        FF, "-y", "-v", "error",
        "-f", "concat", "-safe", "0", "-i", lst,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart",
        final,
    ])

    info = subprocess.run([FF, "-i", final], capture_output=True, text=True).stderr
    print("FINAL:")
    for line in info.splitlines():
        if "Duration" in line or "Stream" in line or "Video:" in line or "Audio:" in line:
            print(" ", line.strip())
    print("size", os.path.getsize(final))

    # check stills at ~2s into each segment
    starts = [0.0]
    for _, _, _, _, d in SEGS[:-1]:
        starts.append(starts[-1] + d)
    for i, (name, _, _, _, dur) in enumerate(SEGS):
        t = starts[i] + min(2.0, dur / 2)
        outp = os.path.join(CHK, f"seg{i+1}_{t:.2f}s.png")
        run([FF, "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", final, "-frames:v", "1", outp])
        print("chk", outp, os.path.getsize(outp))

    # cut table
    md = os.path.join(BUILD, "切点表.md")
    labels = [
        ("seg1_face", "钩子 · 数字人 p81", "seg1_钩子.wav"),
        ("seg2_face", "铺垫 · 数字人 p84", "seg2_铺垫_三个步骤.wav"),
        ("seg3_card", "第一步 · 贴片 c1 Ken Burns", "seg3_第一步_逆向信源.wav"),
        ("seg4_card", "第二步 · 贴片 c2 Ken Burns", "seg4_第二步_定点投放.wav"),
        ("seg5_card", "第三步 · 贴片 c3 Ken Burns", "seg5_第三步_低成本放大.wav"),
    ]
    total = sum(s[4] for s in SEGS)
    lines = [
        "# GEO 大模型收录 · 成片切点表 v1",
        "",
        f"- 成片：`04_成片/成片_v1.mp4`",
        f"- 规格：1080×1920 / 25fps / yuv420p / AAC stereo 44100 / +faststart",
        f"- 总长：**{total:.3f}s**（五段首尾相接）",
        f"- 数字人裁切：`scale=-2:1920,crop=1080:1920`（768×1024 → 1440×1920 → center crop）",
        f"- 贴片：已是 1080×1920，zoompan 1.0→1.06 慢推",
        f"- 口播音频替换数字人内嵌音轨；无额外字幕（贴片自带文案）",
        "",
        "| 段 | 文件 | 起止 | 时长 | 画面 | 音频 |",
        "|---|---|---|---|---|---|",
    ]
    t0 = 0.0
    for i, ((name, kind, src, audio, dur), (lab, desc, aname)) in enumerate(zip(SEGS, labels)):
        t1 = t0 + dur
        lines.append(
            f"| {i+1} | `{name}` | {t0:.3f} – {t1:.3f} | {dur:.3f}s | {desc} | `{aname}` |"
        )
        t0 = t1
    lines.append("")
    lines.append(f"合计 {total:.3f}s。封面已在 `04_成片/`，本脚本不覆盖。")
    with open(md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", md)

if __name__ == "__main__":
    main()
