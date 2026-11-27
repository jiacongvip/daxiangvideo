# -*- coding: utf-8 -*-
"""Assemble GEO vertical short v3: same as v2 but card segs use 原图 stickers (cover-fit)."""
import os, subprocess

FF = "/Users/jiacong/.local/bin/ffmpeg"
PROJ = "/Users/jiacong/Downloads/剪辑素材/项目/04_GEO大模型收录"
BUILD = os.path.join(PROJ, "_build")
OUT_DIR = os.path.join(PROJ, "04_成片")
AUD = os.path.join(PROJ, "01_脚本", "audio")
DH = os.path.join(PROJ, "03_数字人视频")
ST = os.path.join(PROJ, "02_贴片", "原图")
CHK = os.path.join(BUILD, "_chk_v3")
ASS = os.path.join(BUILD, "sub_geo_v2.ass")

W, H, FPS = 1080, 1920, 25

os.makedirs(BUILD, exist_ok=True)
os.makedirs(CHK, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

P81 = os.path.join(DH, "pl-WanVideo2_1_multitalk_00001_p81-audio_ftrrx_1793511822.mp4")
P84 = os.path.join(DH, "pl-WanVideo2_1_multitalk_00001_p84-audio_jnfpx_1793518989.mp4")

SEGS = [
    ("seg1_face_v3.mp4", "face", P81, os.path.join(AUD, "seg1_钩子.wav"), 10.740),
    ("seg2_face_v3.mp4", "face", P84, os.path.join(AUD, "seg2_铺垫_三个步骤.wav"), 8.910),
    ("seg3_card_v3.mp4", "card", os.path.join(ST, "01_引用来源.png"), os.path.join(AUD, "seg3_第一步_逆向信源.wav"), 17.380),
    ("seg4_card_v3.mp4", "card", os.path.join(ST, "02_对比.png"), os.path.join(AUD, "seg4_第二步_定点投放.wav"), 18.050),
    ("seg5_card_v3.mp4", "card", os.path.join(ST, "03_低成本路径.png"), os.path.join(AUD, "seg5_第三步_低成本放大.wav"), 12.410),
]

def run(cmd):
    print("+", " ".join(str(c) for c in cmd[:12]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        err = r.stderr[-3000:] if r.stderr else "no stderr"
        print(err)
        raise SystemExit(f"ffmpeg failed rc={r.returncode}")
    return r

def make_face(out, src, audio, dur):
    # delogo BEFORE scale (native 768x1024), then cover crop
    vf = "delogo=x=8:y=2:w=250:h=55,scale=-2:1920,crop=1080:1920,fps=25,format=yuv420p"
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
    """Landscape sticker → cover 1080x1920, then Ken Burns 1.0→1.06."""
    n = int(round(dur * FPS))
    inc = 0.06 / max(n - 1, 1)
    zexpr = f"min(zoom+{inc:.10f},1.06)"
    # Cover-fit first (no letterbox), then zoompan on the 1080x1920 frame
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=increase,"
        f"crop={W}:{H},"
        f"zoompan=z='{zexpr}':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={n}:s={W}x{H}:fps={FPS},"
        f"format=yuv420p"
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
    if not os.path.isfile(ASS):
        raise SystemExit(f"missing ASS: {ASS}")
    for name, kind, src, audio, dur in SEGS:
        if not os.path.isfile(src):
            raise SystemExit(f"missing src: {src}")
        if not os.path.isfile(audio):
            raise SystemExit(f"missing audio: {audio}")

    paths = []
    for name, kind, src, audio, dur in SEGS:
        out = os.path.join(BUILD, name)
        print(f"== {name} ({kind}) {dur}s ==")
        print(f"   src: {src}")
        if kind == "face":
            make_face(out, src, audio, dur)
        else:
            make_card(out, src, audio, dur)
        paths.append(out)
        info = subprocess.run([FF, "-i", out], capture_output=True, text=True).stderr
        for line in info.splitlines():
            if "Duration" in line or "Video:" in line or "Audio:" in line:
                print(" ", line.strip())

    lst = os.path.join(BUILD, "concat_list_v3.txt")
    with open(lst, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")

    raw = os.path.join(BUILD, "成片_v3_nosub.mp4")
    print("== concat →", raw)
    run([
        FF, "-y", "-v", "error",
        "-f", "concat", "-safe", "0", "-i", lst,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-movflags", "+faststart",
        raw,
    ])

    final = os.path.join(OUT_DIR, "成片_v3_字幕.mp4")
    ass_esc = ASS.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    print("== burn ASS →", final)
    run([
        FF, "-y", "-v", "error",
        "-i", raw,
        "-vf", f"ass={ass_esc}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart",
        final,
    ])

    info = subprocess.run([FF, "-i", final], capture_output=True, text=True).stderr
    print("FINAL:")
    for line in info.splitlines():
        if "Duration" in line or "Stream" in line or "Video:" in line or "Audio:" in line:
            print(" ", line.strip())
    print("size", os.path.getsize(final))

    # card-segment check stills (~22 / 45 / 60s) + a couple face frames
    for t in [1.0, 12.0, 22.0, 45.0, 60.0]:
        outp = os.path.join(CHK, f"t{t:.0f}s.png")
        run([FF, "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", final, "-frames:v", "1", outp])
        print("chk", outp, os.path.getsize(outp))

    for t, tag in [(1.0, "face1"), (12.0, "face2")]:
        outp = os.path.join(CHK, f"wm_{tag}_{t:.0f}s.png")
        run([
            FF, "-y", "-v", "error",
            "-ss", f"{t:.3f}", "-i", final,
            "-frames:v", "1",
            "-vf", "crop=360:120:0:0",
            outp,
        ])
        print("wm", outp, os.path.getsize(outp))

    # update cut table (keep v1/v2 notes, mark v3 current)
    md = os.path.join(BUILD, "切点表.md")
    labels = [
        ("seg1_face_v3", "钩子 · 数字人 p81 + delogo", "seg1_钩子.wav"),
        ("seg2_face_v3", "铺垫 · 数字人 p84 + delogo", "seg2_铺垫_三个步骤.wav"),
        ("seg3_card_v3", "第一步 · 原图/01_引用来源.png cover+Ken Burns", "seg3_第一步_逆向信源.wav"),
        ("seg4_card_v3", "第二步 · 原图/02_对比.png cover+Ken Burns", "seg4_第二步_定点投放.wav"),
        ("seg5_card_v3", "第三步 · 原图/03_低成本路径.png cover+Ken Burns", "seg5_第三步_低成本放大.wav"),
    ]
    total = sum(s[4] for s in SEGS)
    lines = [
        "# GEO 大模型收录 · 成片切点表",
        "",
        "## v1（保留）",
        "- 成片：`04_成片/成片_v1.mp4` — 裸拼接，无去水印、无字幕",
        "",
        "## v2（保留）",
        "- 成片：`04_成片/成片_v2_字幕.mp4` — delogo + ASS；贴片仍用 `02_贴片/预览_c1/c2/c3.png`",
        "",
        "## v3（本版 · 新原图贴片）",
        f"- 成片：`04_成片/成片_v3_字幕.mp4`",
        f"- 规格：1080×1920 / 25fps / yuv420p / AAC stereo 44100 / +faststart",
        f"- 总长：**{total:.3f}s**（五段硬切首尾相接）",
        f"- 数字人：`delogo=x=8:y=2:w=250:h=55`（原生 768×1024 上去掉 RunningHub）→ `scale=-2:1920,crop=1080:1920`",
        f"- 贴片：`02_贴片/原图/01_引用来源.png` / `02_对比.png` / `03_低成本路径.png`",
        f"  （1536×1024 → `scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920` cover，无黑边）→ zoompan 1.0→1.06",
        f"- 字幕：`_build/sub_geo_v2.ass`（Hiragino Sans GB W6 / size80 / outline6 / MarginV462 / fad(70,70) / 金绿红高亮）烧录",
        f"- 口播音频替换数字人内嵌音轨；封面未改动；v1/v2 文件不动",
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
    lines.append(f"合计 {total:.3f}s。v1/v2 保留不动；封面已在 `04_成片/`。")
    with open(md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", md)

if __name__ == "__main__":
    main()
