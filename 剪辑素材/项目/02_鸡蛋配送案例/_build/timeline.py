# -*- coding: utf-8 -*-
"""计算 15 句的精确时间轴（按已知块边界 + 停顿吸附）"""
import json, re, os

WK = "/Users/jiacong/Downloads/剪辑素材/_work"
OUT = "/Users/jiacong/Downloads/剪辑素材/项目/02_鸡蛋配送案例/_build"
os.makedirs(OUT, exist_ok=True)

exec(open(os.path.join(WK, "sync.py")).read().split("base =")[0])

E = frames(os.path.join(WK, "aud/full.wav"))
DUR = len(E) / 100.0

# 停顿区间（>=0.22s）
def gaps(e, thr_ratio=0.06, min_sil=0.22):
    peak = max(e) or 1
    thr = peak * thr_ratio
    ms = int(min_sil * 100)
    out, run, prev_end = [], 0, None
    for i, v in enumerate(e):
        if v < thr:
            if run == 0:
                prev_end = i
            run += 1
        else:
            if run >= ms:
                out.append((prev_end / 100, i / 100))
            run = 0
    return out

GAPS = gaps(E)
print("停顿 %d 处: %s" % (len(GAPS), ", ".join("%.2f-%.2f" % g for g in GAPS)))

SENT = [
    ("在一个城市光靠卖鸡蛋，一年居然能干到 1 个多亿？", 1),
    ("这是我们真实服务的一家同城配送客户。", 1),
    ("很多批发老板问我，他到底是怎么管好几千家门店和车队的？", 1),
    ("其实核心就靠我们帮他定制的这套同城 B2B 配送系统！", 1),
    ("第一，业务员跑市场神器。", 1),
    ("做批发最怕价格乱，系统直接支持阶梯价、新老客户“一客一价”。", 2),
    ("遇到不会用手机的餐饮老板，业务员还能在手机上直接“代客下单”，业绩自动算提成，拓客效率翻倍。", 3),
    ("第二，把配送成本压到极致。", 3),
    ("每天几千单怎么送？系统自动按“配送批次”汇总，给司机做最优的“路径规划”。", 3),
    ("过去人工排线要两小时，现在几秒钟直接发到“配送员系统”里。", 3),
    ("第三，解决批发最头疼的烂账和丢筐。", 3),
    ("餐饮店习惯“记账月结”，而且送鸡蛋每次都要押筐、退筐。", 4),
    ("我们在系统里专门做了“退筐结算”和月结对账，送了多少货、退了几个筐、欠多少款，"
     "手机上一目了然，一年光丢筐和坏账就能省下几十万！", 4),
    ("如果你也是做生鲜、冻品、酒水或者同城批发的老板，想看看这套年销过亿的配送系统后台长什么样？", 4),
    ("评论区留个【配送】，我发你演示号自己体验！", 4),
]

# 已知块：(起, 止, 覆盖句号集合)
BLOCKS = {
    1: (0.00, 18.12, [1, 2, 3, 4, 5]),
    2: (18.20, 25.73, [6]),
    3: (26.00, 53.56, [7, 8, 9, 10, 11]),
    4: (53.80, 80.68, [12, 13, 14, 15]),
}


def n(s):
    return len(re.sub(r"\s", "", s))


def snap(t, lo, hi, tol=0.80):
    """把时间点吸附到最近的停顿中点"""
    best, bd = None, 1e9
    for a, b in GAPS:
        c = (a + b) / 2
        if abs(c - t) < bd:
            bd, best = abs(c - t), c
    if best is not None and bd <= tol and lo < best < hi:
        return round(best, 2), True
    return round(t, 2), False


times = {}
# A 段用人工核定的边界（已知语音单元）
for sid, a, b in [(1,0.00,3.45),(2,3.45,6.99),(3,6.99,12.17),(4,12.17,14.88),(5,14.88,18.12)]:
    times[sid]=[a,b]
for bi, (b0, b1, ids) in BLOCKS.items():
    if bi == 1:
        continue
    total = sum(n(SENT[i - 1][0]) for i in ids)
    span = b1 - b0
    acc = b0
    for k, sid in enumerate(ids):
        d = span * n(SENT[sid - 1][0]) / total
        s = acc
        e = b1 if k == len(ids) - 1 else acc + d
        times[sid] = [s, e]
        acc = e
    # 吸附内部边界
    for k in range(len(ids) - 1):
        sid = ids[k]
        raw = times[sid][1]
        st, ok = snap(raw, times[sid][0] + 0.8, times[ids[k + 1]][0] + 0.8)
        times[sid][1] = st
        times[ids[k + 1]][0] = st
        if ok:
            print(f"  句{sid}/{ids[k+1]} 边界 {raw:.2f} → 吸附 {st:.2f}")

print("\n句子时间轴：")
for i, (txt, _) in enumerate(SENT, 1):
    s, e = times[i]
    print(f"  {i:2d}  {s:6.2f} → {e:6.2f}  ({e-s:5.2f}s)  {txt[:26]}")

json.dump({str(k): v for k, v in times.items()},
          open(os.path.join(OUT, "timeline.json"), "w"), ensure_ascii=False, indent=1)
print("\n总长 %.2f" % DUR)
