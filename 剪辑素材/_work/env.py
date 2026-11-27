import wave, array, math, glob, os, json

HOP = 320  # 20ms @16k

def env(path):
    w = wave.open(path, 'rb')
    assert w.getframerate() == 16000 and w.getnchannels() == 1
    n = w.getnframes()
    raw = w.readframes(n)
    a = array.array('h')
    a.frombytes(raw)
    out = []
    for i in range(0, len(a) - HOP, HOP):
        s = 0
        for j in range(i, i + HOP):
            v = a[j]
            s += v * v
        out.append(math.sqrt(s / HOP))
    w.close()
    return out

def norm(e):
    m = max(e) if e else 0
    if m <= 0:
        return e
    return [x / m for x in e]

def best_offset(long, short):
    """slide short over long, return (score, offset_frames, t)"""
    ns = len(short)
    nl = len(long)
    if ns >= nl:
        return (0, -1, 0)
    # prefix sums for mean/std normalization
    # simple normalized cross-correlation on raw (centered) envelopes
    ms = sum(short) / ns
    ss = math.sqrt(sum((x - ms) ** 2 for x in short)) or 1e-9
    sc_short = [(x - ms) / ss for x in short]
    best = (-2, -1)
    step = 1
    # coarse then fine would be faster; keep simple
    for off in range(0, nl - ns + 1, step):
        seg = long[off:off + ns]
        ml = sum(seg) / ns
        sl = math.sqrt(sum((x - ml) ** 2 for x in seg)) or 1e-9
        c = 0.0
        for k in range(ns):
            c += sc_short[k] * (seg[k] - ml)
        c = c / sl
        if c > best[0]:
            best = (c, off)
    return (best[0], best[1], best[1] * HOP / 16000)

files = sorted(glob.glob('/Users/jiacong/Downloads/剪辑素材/_work/aud/*.wav'))
envs = {}
for f in files:
    e = env(f)
    envs[os.path.basename(f)] = (e, len(e) * HOP / 16000)

for k, (e, d) in envs.items():
    print(f"{k}\tdur={d:.2f}s\tframes={len(e)}\tpeak={max(e):.0f}\tmean={sum(e)/len(e):.0f}")

print("\n=== 对比：每个较短视频 在 较长音频 中的最佳匹配位置 ===")
keys = list(envs.keys())
for a in keys:
    for b in keys:
        if a == b:
            continue
        ea, da = envs[a]
        eb, db = envs[b]
        if db >= da - 1:
            continue
        score, off, t = best_offset(ea, eb)
        if score > 0.55:
            print(f"{b}  ⊆  {a}   score={score:.3f}  start={t:.2f}s  (长={da:.2f}s 短={db:.2f}s)")
