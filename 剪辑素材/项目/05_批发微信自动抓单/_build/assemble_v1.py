# -*- coding: utf-8 -*-
"""批发微信自动抓单 · 成片 v1：露脸→贴片1→贴片2→贴片3→露脸 + jrqkm 口播 + ASS"""
import os, subprocess

FF = "/Users/jiacong/.local/bin/ffmpeg"
PROJ = "/Users/jiacong/Downloads/剪辑素材/项目/05_批发微信自动抓单"
BUILD = os.path.join(PROJ, "_build")
OUT_DIR = os.path.join(PROJ, "04_成片")
CHK = os.path.join(BUILD, "_chk_v1")
ASS = os.path.join(BUILD, "sub_wx.ass")
AUD = os.path.join(PROJ, "01_脚本", "ComfyUI_00001_jrqkm_1793598746.mp3")

W, H, FPS = 1080, 1920, 25
# Master VO ~73.25s; ASS content cuts (same as mk_ass_wx.py)
# face1 ends at 21.02; card1→37.62; card2→49.62; card3→62.82; face2→AUDIO_END
FACE1_END = 21.02
CARD1_END = 37.62
CARD2_END = 49.62
CARD3_END = 62.82
# probe audio length below; fallback
AUDIO_END = 73.25

HOOK = os.path.join(PROJ, "03_数字人视频", "钩子_竖屏_25.73s.mp4")
ENDV = os.path.join(PROJ, "03_数字人视频", "结尾_竖屏_10.68s.mp4")
# raw fallbacks (delogo path) — used only if 竖屏 missing
HOOK_RAW = os.path.join(PROJ, "03_数字人视频", "原始_钩子_27.4s.mp4")
END_RAW = os.path.join(PROJ, "03_数字人视频", "原始_结尾_10.76s.mp4")

ST1 = os.path.join(PROJ, "02_贴片", "贴片1_自动抓单.mp4")
ST2 = os.path.join(PROJ, "02_贴片", "贴片2_常购匹配.mp4")
ST3 = os.path.join(PROJ, "02_贴片", "贴片3_防错打单.mp4")
ST1_IMG = os.path.join(PROJ, "02_贴片", "预览_c1.png")
ST2_IMG = os.path.join(PROJ, "02_贴片", "预览_c2.png")
ST3_IMG = os.path.join(PROJ, "02_贴片", "预览_c3.png")

os.makedirs(BUILD, exist_ok=True)
os.makedirs(CHK, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)


def run(cmd):
    print("+", " ".join(str(c) for c in cmd[:14]), "...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        err = (r.stderr or "")[-3500:]
        print(err)
        raise SystemExit(f"ffmpeg failed rc={r.returncode}")
    return r


def probe_dur(path):
    r = subprocess.run([FF, "-i", path], capture_output=True, text=True)
    for line in (r.stderr or "").splitlines():
        if "Duration" in line:
            # Duration: HH:MM:SS.xx
            part = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = part.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise SystemExit(f"no duration for {path}")


def make_face_竖屏(out, src, dur):
    """Already 1080x1920 delogo'd; trim/pad to dur. Freeze-last if short."""
    src_dur = probe_dur(src)
    if src_dur + 0.02 >= dur:
        vf = f"fps={FPS},format=yuv420p,trim=duration={dur:.3f},setpts=PTS-STARTPTS"
        cmd = [
            FF, "-y", "-v", "error",
            "-i", src,
            "-vf", vf,
            "-an",
            "-t", f"{dur:.3f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            out,
        ]
    else:
        # slow last 0.5s slightly + freeze pad
        pad = dur - src_dur
        vf = (
            f"fps={FPS},format=yuv420p,"
            f"tpad=stop_mode=clone:stop_duration={pad:.3f},"
            f"trim=duration={dur:.3f},setpts=PTS-STARTPTS"
        )
        cmd = [
            FF, "-y", "-v", "error",
            "-i", src,
            "-vf", vf,
            "-an",
            "-t", f"{dur:.3f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            out,
        ]
    run(cmd)


def make_face_raw_delogo(out, src, dur):
    vf = (
        "delogo=x=8:y=2:w=250:h=55,"
        "scale=-2:1920,crop=1080:1920,"
        f"fps={FPS},format=yuv420p,"
        f"trim=duration={dur:.3f},setpts=PTS-STARTPTS"
    )
    run([
        FF, "-y", "-v", "error",
        "-i", src,
        "-vf", vf,
        "-an",
        "-t", f"{dur:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        out,
    ])


def make_card_vid(out, src, dur, fallback_img=None):
    """Loop/trim sticker mp4 to exact dur; fallback Ken Burns still if missing."""
    if not os.path.isfile(src):
        if not fallback_img or not os.path.isfile(fallback_img):
            raise SystemExit(f"missing sticker {src}")
        n = int(round(dur * FPS))
        inc = 0.06 / max(n - 1, 1)
        zexpr = f"min(zoom+{inc:.10f},1.06)"
        vf = (
            f"scale={W}:{H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},"
            f"zoompan=z='{zexpr}':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={n}:s={W}x{H}:fps={FPS},"
            f"format=yuv420p"
        )
        run([
            FF, "-y", "-v", "error",
            "-loop", "1", "-i", fallback_img,
            "-vf", vf,
            "-t", f"{dur:.3f}",
            "-an",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            out,
        ])
        return

    src_dur = probe_dur(src)
    if src_dur + 0.05 >= dur:
        vf = f"fps={FPS},format=yuv420p,trim=duration={dur:.3f},setpts=PTS-STARTPTS"
        run([
            FF, "-y", "-v", "error",
            "-i", src,
            "-vf", vf,
            "-an",
            "-t", f"{dur:.3f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            out,
        ])
    else:
        # loop then trim
        vf = f"fps={FPS},format=yuv420p,trim=duration={dur:.3f},setpts=PTS-STARTPTS"
        run([
            FF, "-y", "-v", "error",
            "-stream_loop", "-1",
            "-i", src,
            "-vf", vf,
            "-an",
            "-t", f"{dur:.3f}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            out,
        ])


def main():
    global AUDIO_END
    if not os.path.isfile(ASS):
        raise SystemExit(f"missing ASS: {ASS} — run mk_ass_wx.py first")
    if not os.path.isfile(AUD):
        raise SystemExit(f"missing audio: {AUD}")

    AUDIO_END = probe_dur(AUD)
    print(f"master audio duration={AUDIO_END:.3f}s")

    segs = [
        ("seg1_face.mp4", "face", HOOK, HOOK_RAW, FACE1_END - 0.0, None),
        ("seg2_card1.mp4", "card", ST1, None, CARD1_END - FACE1_END, ST1_IMG),
        ("seg3_card2.mp4", "card", ST2, None, CARD2_END - CARD1_END, ST2_IMG),
        ("seg4_card3.mp4", "card", ST3, None, CARD3_END - CARD2_END, ST3_IMG),
        ("seg5_face.mp4", "face", ENDV, END_RAW, AUDIO_END - CARD3_END, None),
    ]

    paths = []
    for name, kind, src, raw, dur, fb in segs:
        out = os.path.join(BUILD, name)
        print(f"== {name} ({kind}) {dur:.3f}s ==")
        if kind == "face":
            if os.path.isfile(src):
                make_face_竖屏(out, src, dur)
            elif raw and os.path.isfile(raw):
                print("  using raw+delogo", raw)
                make_face_raw_delogo(out, raw, dur)
            else:
                raise SystemExit(f"missing face src {src}")
        else:
            make_card_vid(out, src, dur, fb)
        paths.append(out)
        info = subprocess.run([FF, "-i", out], capture_output=True, text=True).stderr
        for line in info.splitlines():
            if "Duration" in line or "Video:" in line:
                print(" ", line.strip())

    lst = os.path.join(BUILD, "concat_list_v1.txt")
    with open(lst, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")

    raw = os.path.join(BUILD, "成片_v1_nosub.mp4")
    print("== concat →", raw)
    run([
        FF, "-y", "-v", "error",
        "-f", "concat", "-safe", "0", "-i", lst,
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-an",
        "-movflags", "+faststart",
        raw,
    ])

    # mux master audio (replace any embedded)
    muxed = os.path.join(BUILD, "成片_v1_nosub_aud.mp4")
    print("== mux jrqkm audio →", muxed)
    run([
        FF, "-y", "-v", "error",
        "-i", raw,
        "-i", AUD,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
        "-shortest",
        "-movflags", "+faststart",
        muxed,
    ])

    final = os.path.join(OUT_DIR, "成片_v1_字幕.mp4")
    ass_esc = ASS.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    print("== burn ASS →", final)
    run([
        FF, "-y", "-v", "error",
        "-i", muxed,
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

    # check frames at section boundaries (+1s into each)
    cuts = [0.5, FACE1_END - 0.3, FACE1_END + 0.5, CARD1_END + 0.5,
            CARD2_END + 0.5, CARD3_END + 0.5, AUDIO_END - 1.0]
    labels = ["face1", "face1_end", "card1", "card2", "card3", "face2", "face2_end"]
    for t, lab in zip(cuts, labels):
        outp = os.path.join(CHK, f"{lab}_{t:.1f}s.png")
        run([FF, "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", final, "-frames:v", "1", outp])
        print("chk", outp, os.path.getsize(outp))

    # wm check on face
    for t, tag in [(1.0, "face1"), (CARD3_END + 1.0, "face2")]:
        outp = os.path.join(CHK, f"wm_{tag}.png")
        run([
            FF, "-y", "-v", "error",
            "-ss", f"{t:.3f}", "-i", final,
            "-frames:v", "1",
            "-vf", "crop=360:120:0:0",
            outp,
        ])
        print("wm", outp)

    # cut table
    md = os.path.join(BUILD, "切点表.md")
    rows = [
        (1, "seg1_face.mp4", 0.0, FACE1_END, "全屏露脸 · 钩子_竖屏（已去 RunningHub）", "jrqkm 0–21.02 到「全靠老板脑子记」"),
        (2, "seg2_card1.mp4", FACE1_END, CARD1_END, "贴片1_自动抓单.mp4（loop→16.60s）", "jrqkm 「很多人劝他…生成待发清单」"),
        (3, "seg3_card2.mp4", CARD1_END, CARD2_END, "贴片2_常购匹配.mp4", "jrqkm 「第二步…费脑子回忆」"),
        (4, "seg4_card3.mp4", CARD2_END, CARD3_END, "贴片3_防错打单.mp4（略延）", "jrqkm 「第三步…自动出单」"),
        (5, "seg5_face.mp4", CARD3_END, AUDIO_END, "全屏露脸 · 结尾_竖屏", "jrqkm 「每天手动搬单…评论区交流」"),
    ]
    lines = [
        "# 批发微信自动抓单 · 成片切点表",
        "",
        "## v1（本版）",
        f"- 成片：`04_成片/成片_v1_字幕.mp4`",
        f"- 规格：1080×1920 / 25fps / yuv420p / AAC stereo 44100 / +faststart",
        f"- 总长：**{AUDIO_END:.3f}s**（五段硬切；口播 `ComfyUI_00001_jrqkm_1793598746.mp3`）",
        f"- 结构：露脸 → 贴片1 → 贴片2 → 贴片3 → 露脸（文案零改动）",
        f"- 数字人：优先 `钩子_竖屏_25.73s.mp4` / `结尾_竖屏_10.68s.mp4`（已去水印竖屏）；缺则 raw+delogo",
        f"- 字幕：`_build/sub_wx.ass`（mk_ass_wx.py / Hiragino Sans GB W6 / 强调色）烧录",
        f"- 封面单独存放，未烧进视频",
        "",
        "| 段 | 文件 | 起止 | 时长 | 画面 | 口播区间 |",
        "|---|---|---|---|---|---|",
    ]
    for i, name, a, b, pic, aud in rows:
        lines.append(f"| {i} | `{name}` | {a:.3f} – {b:.3f} | {b-a:.3f}s | {pic} | {aud} |")
    lines.append("")
    lines.append(f"合计 {AUDIO_END:.3f}s。根目录旧预览/`批发微信自动抓单_成片.mp4` 未覆盖。")
    with open(md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", md)


if __name__ == "__main__":
    main()
