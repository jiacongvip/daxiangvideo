# -*- coding: utf-8 -*-
"""批发微信自动抓单 · 抖音爆款封面（Duomi，无人脸）"""
from __future__ import annotations

import json
import pathlib
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request

from PIL import Image

ROOT = pathlib.Path("/Users/jiacong/Downloads/剪辑素材/项目/05_批发微信自动抓单")
OUT = ROOT / "04_成片"
COVER_DIR = ROOT / "_build" / "_cover"
COVER_DIR.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

MODEL_TRY = ["gpt-image-2.5-sunburst", "gpt-image-2"]
SIZES_TRY = ["1024x1536", "1024x1792", "1024x1024"]
CTX = ssl.create_default_context()

PROMPT = """Create a high-CTR vertical Douyin / TikTok thumbnail cover (portrait), Chinese short-video style.

STRICT: ZERO humans, ZERO faces, ZERO digital humans, ZERO talking heads, ZERO stock photo people, ZERO hands with faces. Graphic / typography / UI chrome ONLY. Flat modern tech poster, not photorealistic.

STYLE: Dark tech background (deep navy / charcoal / near-black). High contrast. Bold Chinese text with thick black outline, mobile-first readability. Accent colors: gold/orange + vivid red + WeChat green accents. Clean, sharp Simplified Chinese glyphs — text must be correct, no garbled characters.

BIG HOOK LINES (must appear large and readable, stacked vertically, top-heavy):
1) 「微信报单靠肉眼看」 — white/cream; emphasize 「肉眼看」 in red
2) 「手敲进软件眼睛瞎」 — white; emphasize 「手敲」 in orange/gold
3) 「调料10包靠脑子记」 — white; emphasize 「10包」「脑子记」 in gold/red

MID UI FRAGMENT (abstract, no people):
- Dark PC WeChat chat chrome mock (generic bubbles, no real logos/trademarks)
- Order chips like 「鸡蛋20箱」「调料10包」「蒜米5斤」
- Small green badge 「自动抓单」 or cyan tag 「3步搞定」

BOTTOM TAG (smaller): 「批发微信 · 自动抓单」 in cyan/gold

Composition: vertical 2:3 poster, generous margins, punchy CTR thumbnail. No watermarks. No real brand logos. No photographs of people.
"""

FALLBACK_STICKER_CREDS = (
    "v4rzUOVquJBGvLg89eoLcFu4zd",
    "https://duomiapi.com",
)


def load_creds_from_mysql():
    cmd = [
        "docker", "exec", "tpdaxiangshop_mysql",
        "mysql", "-uroot", "-proot123456", "tpdaxiangshop", "-N", "-e",
        "SELECT api_key, base_url FROM ddwx_digitalavatar_provider_config "
        "WHERE aid=62 AND provider_key='duomiapi' LIMIT 1",
    ]
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
    lines = [ln for ln in out.splitlines() if ln.strip() and "Warning" not in ln and "insecure" not in ln]
    if not lines:
        raise RuntimeError(f"no duomi creds from mysql: {out!r}")
    parts = lines[0].split("\t")
    if len(parts) < 2:
        raise RuntimeError(f"bad creds line: {lines[0]!r}")
    return parts[0].strip(), parts[1].strip().rstrip("/")


def load_creds():
    try:
        return load_creds_from_mysql(), "mysql_aid62"
    except Exception as e:
        print(f"mysql creds fail: {e} → sticker fallback", flush=True)
        return FALLBACK_STICKER_CREDS, "sticker_duomi_json"


def req(method, url, key, payload=None, timeout=90):
    data = None if payload is None else json.dumps(payload).encode()
    headers = {"Authorization": "Bearer " + key, "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=timeout, context=CTX) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"raw": body[:800]}


def extract_state(o):
    if not isinstance(o, dict):
        return ""
    return str(
        o.get("state")
        or o.get("status")
        or (o.get("data") or {}).get("state")
        or ""
    )


def extract_url(o, img=""):
    if img:
        return img
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("url", "image_url") and isinstance(v, str) and v.startswith("http"):
                return v
            img = extract_url(v, img)
            if img:
                return img
    elif isinstance(o, list):
        for x in o:
            img = extract_url(x, img)
            if img:
                return img
    return img


def is_balance_error(body):
    s = json.dumps(body, ensure_ascii=False) if not isinstance(body, str) else body
    return ("余额不足" in s) or ("API账户余额不足" in s)


def is_busy(body):
    s = json.dumps(body, ensure_ascii=False) if not isinstance(body, str) else body
    return "系统繁忙" in s


def cover_fit(src: Image.Image, tw: int, th: int) -> Image.Image:
    img = src.convert("RGB")
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(round(sw * scale)), int(round(sh * scale))
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def crop_1440_from_1920(img_1920: Image.Image) -> Image.Image:
    return img_1920.crop((0, 240, 1080, 1680))


def submit_once(key, base, model, size):
    payload = {
        "model": model,
        "prompt": PROMPT,
        "size": size,
        "quality": "high",
    }
    code, body = req("POST", base + "/v1/images/generations?async=true", key, payload)
    tid = str((body or {}).get("id") or "")
    if not tid and isinstance(body, dict):
        data = body.get("data") or {}
        if isinstance(data, dict):
            tid = str(data.get("id") or "")
    return code, body, tid


def main():
    (key, base), cred_source = load_creds()
    if cred_source == "mysql_aid62":
        print(f"creds ok base={base} key={key[:6]}… src={cred_source}", flush=True)
    else:
        key, base = FALLBACK_STICKER_CREDS
        print(f"creds ok base={base} key={key[:6]}… src={cred_source}", flush=True)

    last_err = None
    tid = None
    model_used = None
    size_used = None

    for model in MODEL_TRY:
        for size in SIZES_TRY:
            print(f"try model={model} size={size}", flush=True)
            code, body, tid0 = submit_once(key, base, model, size)
            print(f"submit {code} tid={tid0} body={str(body)[:360]}", flush=True)
            if is_balance_error(body):
                if cred_source == "mysql_aid62":
                    print("MySQL key 余额不足 → sticker duomi.json key", flush=True)
                    key, base = FALLBACK_STICKER_CREDS
                    cred_source = "sticker_duomi_json"
                    code, body, tid0 = submit_once(key, base, model, size)
                    print(f"fallback submit {code} tid={tid0} body={str(body)[:360]}", flush=True)
                    if is_balance_error(body):
                        print("BALANCE_INSUFFICIENT_BOTH_KEYS", json.dumps(body, ensure_ascii=False)[:500], flush=True)
                        sys.exit(2)
                else:
                    print("BALANCE_INSUFFICIENT", json.dumps(body, ensure_ascii=False)[:500], flush=True)
                    sys.exit(2)
            raw = json.dumps(body, ensure_ascii=False)
            if (
                ("size" in raw.lower() and ("invalid" in raw.lower() or "不支持" in raw or "unsupported" in raw.lower()))
                or code in (400, 422)
            ) and not tid0:
                last_err = body
                print("bad size/model, next", flush=True)
                continue
            busy_n = 0
            st = "ok" if tid0 else "notid"
            if is_busy(body):
                st = "busy"
            while st in ("busy", "notid") and busy_n < 8:
                busy_n += 1
                wait = min(25, 3 * busy_n)
                print(f"submit_{st}_retry {busy_n} sleep {wait}s", flush=True)
                time.sleep(wait)
                code, body, tid0 = submit_once(key, base, model, size)
                print(f"resubmit {code} tid={tid0}", flush=True)
                if is_balance_error(body):
                    print("BALANCE_INSUFFICIENT", flush=True)
                    sys.exit(2)
                if tid0:
                    st = "ok"
                    break
                if is_busy(body):
                    st = "busy"
                else:
                    st = "notid"
            if not tid0:
                last_err = body
                continue

            tid = tid0
            model_used = model
            size_used = size
            img_url = None
            for i in range(120):
                time.sleep(5)
                try:
                    code, body = req("GET", base + "/v1/tasks/" + tid, key)
                except Exception as e:
                    print(f"poll_net_err {e}", flush=True)
                    continue
                stt = extract_state(body).lower()
                print(f"poll {i} {stt}", flush=True)
                if is_balance_error(body):
                    print("BALANCE_INSUFFICIENT on poll", flush=True)
                    sys.exit(2)
                if stt in ("failed", "error", "failure"):
                    print(f"task failed: {str(body)[:500]}", flush=True)
                    last_err = body
                    tid = None
                    break
                img_url = extract_url(body)
                if img_url and stt in ("succeeded", "success", "completed", "done"):
                    break
            if img_url:
                raw_path = COVER_DIR / "duomi_raw_cover.png"
                urllib.request.urlretrieve(img_url, raw_path)
                print(f"downloaded {raw_path} from {img_url}", flush=True)

                src = Image.open(raw_path)
                print(f"raw size={src.size}", flush=True)
                img1920 = cover_fit(src.convert("RGB"), 1080, 1920)
                img1440 = crop_1440_from_1920(img1920)

                p1920 = OUT / "封面_爆款_1080x1920.png"
                p1440 = OUT / "封面_爆款_1080x1440_抖音.png"
                img1920.save(p1920, "PNG", optimize=True)
                img1440.save(p1440, "PNG", optimize=True)

                (COVER_DIR / "preview_爆款_duomi_1080x1920.png").write_bytes(p1920.read_bytes())
                (COVER_DIR / "preview_爆款_duomi_1080x1440.png").write_bytes(p1440.read_bytes())

                meta = {
                    "task": tid,
                    "model": model_used,
                    "size_requested": size_used,
                    "raw": str(raw_path),
                    "raw_wh": list(src.size),
                    "out_1920": str(p1920),
                    "out_1440": str(p1440),
                    "bytes_1920": p1920.stat().st_size,
                    "bytes_1440": p1440.stat().st_size,
                    "cred_source": cred_source,
                    "cdn_url": img_url,
                    "prompt_head": PROMPT[:200],
                }
                meta_path = COVER_DIR / "duomi_cover.meta.json"
                meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
                print(json.dumps(meta, ensure_ascii=False, indent=2), flush=True)
                print("DONE", flush=True)
                return

            continue

    print("ALL_FAILED", str(last_err)[:500], flush=True)
    sys.exit(1)


if __name__ == "__main__":
    main()
