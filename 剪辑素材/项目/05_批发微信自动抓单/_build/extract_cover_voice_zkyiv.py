# -*- coding: utf-8 -*-
"""Extract zkyiv face-only VO (intro+outro) aligned to same script content as jrqkm ASS cuts."""
import os, subprocess

FF = "/Users/jiacong/.local/bin/ffmpeg"
PROJ = "/Users/jiacong/Downloads/剪辑素材/项目/05_批发微信自动抓单"
BUILD = os.path.join(PROJ, "_build")
ZKYIV = os.path.join(PROJ, "01_脚本", "ComfyUI_00001_zkyiv_1793584195.mp3")
JRQKM = os.path.join(PROJ, "01_脚本", "ComfyUI_00001_jrqkm_1793598746.mp3")
OUT = os.path.join(BUILD, "cover_voice_face_zkyiv.wav")

# jrqkm content cuts from mk_ass_wx
FACE1_END_J = 21.02
FACE2_START_J = 62.82


def dur(path):
    r = subprocess.run([FF, "-i", path], capture_output=True, text=True)
    for line in (r.stderr or "").splitlines():
        if "Duration" in line:
            part = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = part.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise SystemExit("no dur")


def main():
    dj = dur(JRQKM)
    dz = dur(ZKYIV)
    scale = dz / dj
    # proportional map (same script; zkyiv slightly slower)
    f1e = FACE1_END_J * scale
    f2s = FACE2_START_J * scale
    print(f"jrqkm={dj:.3f} zkyiv={dz:.3f} scale={scale:.5f}")
    print(f"face1 0–{f1e:.3f}  face2 {f2s:.3f}–{dz:.3f}")

    a = os.path.join(BUILD, "_zkyiv_face1.wav")
    b = os.path.join(BUILD, "_zkyiv_face2.wav")
    for out, ss, t in [
        (a, 0.0, f1e),
        (b, f2s, dz - f2s),
    ]:
        subprocess.check_call([
            FF, "-y", "-v", "error",
            "-ss", f"{ss:.3f}", "-t", f"{t:.3f}",
            "-i", ZKYIV,
            "-ar", "44100", "-ac", "1",
            out,
        ])
    lst = os.path.join(BUILD, "_zkyiv_concat.txt")
    with open(lst, "w") as f:
        f.write(f"file '{a}'\nfile '{b}'\n")
    subprocess.check_call([
        FF, "-y", "-v", "error",
        "-f", "concat", "-safe", "0", "-i", lst,
        "-c:a", "pcm_s16le",
        OUT,
    ])
    # also mp3 copy
    mp3 = OUT.replace(".wav", ".mp3")
    subprocess.check_call([
        FF, "-y", "-v", "error", "-i", OUT, "-b:a", "192k", mp3,
    ])
    print("wrote", OUT, "dur", dur(OUT))
    print("wrote", mp3)
    # meta
    meta = os.path.join(BUILD, "cover_voice_face_zkyiv.meta.txt")
    with open(meta, "w") as f:
        f.write(f"jrqkm={dj:.3f}\nzkyiv={dz:.3f}\nscale={scale:.6f}\n")
        f.write(f"face1=0.000-{f1e:.3f}\nface2={f2s:.3f}-{dz:.3f}\n")
        f.write(f"out={OUT}\n")
    print("meta", meta)


if __name__ == "__main__":
    main()
