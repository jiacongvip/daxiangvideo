import wave, array, math, glob, os

HOP = 160  # 10ms

def frames(path):
    w = wave.open(path, 'rb')
    a = array.array('h')
    a.frombytes(w.readframes(w.getnframes()))
    w.close()
    out = []
    for i in range(0, len(a) - HOP, HOP):
        s = 0
        for j in range(i, i + HOP):
            v = a[j]
            s += v * v
        out.append(math.sqrt(s / HOP))
    return out

def silence_report(path):
    e = frames(path)
    peak = max(e) or 1
    thr = peak * 0.045
    gaps = []
    run = 0
    for i, v in enumerate(e):
        if v < thr:
            run += 1
        else:
            if run >= 25:  # >=250ms
                gaps.append((i - run, i, run))
            run = 0
    if run >= 25:
        gaps.append((len(e) - run, len(e), run))
    print(f"\n### {os.path.basename(path)}  时长={len(e)/100:.2f}s  峰值={peak:.0f}  静音阈值={thr:.0f}")
    for s, en, r in gaps:
        print(f"   静音 {s/100:6.2f}s -> {en/100:6.2f}s   ({r/100:.2f}s)")
    # 语音片段
    print("   -- 语音段 --")
    run = 0
    segs = []
    start = None
    for i, v in enumerate(e):
        if v >= thr:
            if start is None:
                start = i
            run = 0
        else:
            run += 1
            if run >= 25 and start is not None:
                segs.append((start, i - run))
                start = None
    if start is not None:
        segs.append((start, len(e)))
    for s, en in segs:
        print(f"   语音 {s/100:6.2f}s -> {en/100:6.2f}s  长{(en-s)/100:.2f}s")

base = '/Users/jiacong/Downloads/剪辑素材/_work/aud/'
for n in ['xiaren_00001_tlgfs_1793278119.wav',
          'xiaren_00001_uladl_1793278431.wav',
          'xiaren_00001_qycia_1793278300.wav',
          'ComfyUI_00001_gbccs_1793278563.wav']:
    silence_report(base + n)
