import wave, array, math

HOP = 160

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

def units(e, thr_ratio=0.05, min_sil=0.20):
    peak = max(e) or 1
    thr = peak * thr_ratio
    ms = int(min_sil * 100)
    segs, start, run = [], None, 0
    for i, v in enumerate(e):
        if v >= thr:
            if start is None:
                start = i
            run = 0
        else:
            run += 1
            if run >= ms and start is not None:
                segs.append((start / 100, (i - run) / 100))
                start = None
    if start is not None:
        segs.append((start / 100, len(e) / 100))
    return segs

def corr(a, b):
    n = min(len(a), len(b))
    a = a[:n]; b = b[:n]
    ma = sum(a) / n; mb = sum(b) / n
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    da = math.sqrt(sum((x - ma) ** 2 for x in a)) or 1e-9
    db = math.sqrt(sum((x - mb) ** 2 for x in b)) or 1e-9
    return num / (da * db)

base = '/Users/jiacong/Downloads/剪辑素材/_work/aud/'
pairs = [('pl-WanVideo2_1_multitalk_00001_p85-audio_kcthc_1793287603.wav', 'ComfyUI_00001_gbccs_1793278563.wav'),
         ('pl-WanVideo2_1_multitalk_00001_p80-audio_flmij_1793286741.wav', 'xiaren_00001_uladl_1793278431.wav'),
         ('pl-WanVideo2_1_multitalk_00001_p87-audio_lsoyc_1793279696.wav', 'xiaren_00001_qycia_1793278300.wav')]
for v, s in pairs:
    ev = frames(base + v); es = frames(base + s)
    print(f"\n### {v[:38]}  vs  {s[:30]}")
    print(f"   前1秒相关度={corr(ev[:100], es[:100]):.3f}  整体前段={corr(ev[:len(es)], es):.3f}")
    print("   视频语音段:", [(round(a,2), round(b,2)) for a, b in units(ev)][:12])
    print("   源音语音段:", [(round(a,2), round(b,2)) for a, b in units(es)][:12])
