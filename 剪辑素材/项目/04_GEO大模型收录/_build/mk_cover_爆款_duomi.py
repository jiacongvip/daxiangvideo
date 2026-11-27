# -*- coding: utf-8 -*-
"""GEO 选题 · 抖音爆款封面（Duomi API，无人脸 / 纯图形字排）

用法:
  python3 mk_cover_爆款_duomi.py

从 Docker MySQL 读 duomi key（aid=62），提交 gpt-image-2.5-sunburst 竖版，
下载后 cover-crop 到 1080x1920 与 1080x1440，覆盖 04_成片/封面_爆款_*.png。
旧信息图封面 封面_1080x*.png 不动。
"""
from __future__ import annotations

import json
import pathlib
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path("/Users/jiacong/Downloads/剪辑素材/项目/04_GEO大模型收录")
OUT = ROOT / "04_成片"
COVER_DIR = ROOT / "_build" / "_cover"
COVER_DIR.mkdir(parents=True, exist_ok=True)

MODEL_TRY = ["gpt-image-2.5-sunburst", "gpt-image-2"]
SIZES_TRY = ["1024x1536", "1024x1792", "1024x1024"]
CTX = ssl.create_default_context()

PROMPT = """Create a high-CTR vertical Douyin / TikTok thumbnail cover (portrait), Chinese short-video style.

STRICT: ZERO humans, ZERO faces, ZERO digital humans, ZERO talking heads, ZERO stock photo people, ZERO hands holding phones with faces. Graphic / typography / UI chrome ONLY. Flat modern tech poster, not photorealistic.

STYLE: Dark tech background (deep navy / charcoal / near-black). High contrast. Bold Chinese text with thick black outline, mobile-first readability. Accent colors: gold/orange + vivid red emphasis. Clean, sharp Chinese glyphs — text must be correct Simplified Chinese, no garbled characters.

BIG HOOK LINES (must appear large and readable, stacked vertically, center/top-heavy):
1) 「千万别再花几万块」 — white/cream; emphasize 「几万」 in gold or red
2) 「刷GEO垃圾稿」 — white; emphasize 「垃圾稿」 in orange/red
3) 「大模型根本不读」 — white; emphasize 「不读」 in vivid red

OPTIONAL MID UI FRAGMENT (abstract, no people):
- Dark generic AI answer card chrome (no real brand logos/trademarks)
- Small red highlight around a button labeled 「引用来源」
- Tiny abstract badges: 「知乎」「公众号」 (text chips only)

BOTTOM TAG (smaller): 「GEO · 3步逆向信源」 in cyan/gold

Composition: vertical 2:3 poster, generous margins, punchy CTR thumbnail. No watermarks. No logos of real AI products. No photographs of people.
"""


def load_creds_from_mysql():
    cmd = [
        "docker", "exec", "tpdaxiangshop_mysql",
        "mysql", "-uroot", "-proot123456", "tpdaxiangshop", "-N", "-e",
        "SELECT api_key, base_url FROM ddwx_digitalavatar_provider_config "
        "WHERE aid=62 AND provider_key='duomiapi' LIMIT 1",
    ]
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
    # strip mysql password warning lines
    lines = [ln for ln in out.splitlines() if ln.strip() and "Warning" not in ln and "insecure" not in ln]
    if not lines:
        raise RuntimeError(f"no duomi creds from mysql: {out!r}")
    parts = lines[0].split("\t")
    if len(parts) < 2:
        raise RuntimeError(f"bad creds line: {lines[0]!r}")
    return parts[0].strip(), parts[1].strip().rstrip("/")


# Same key used for GEO stickers / Unichant kit batch (workspace duomi.json).
# MySQL aid=62 key often returns 余额不足; fall back to this for production gens.
FALLBACK_STICKER_CREDS = (
    "v4rzUOVquJBGvLg89eoLcFu4zd",
    "https://duomiapi.com",
)


def load_creds():
    """Prefer MySQL aid=62; caller may swap to FALLBACK_STICKER_CREDS on balance error."""
    return load_creds_from_mysql()


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
    """Scale+center-crop to exact size, no letterbox."""
    img = src.convert("RGB")
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(round(sw * scale)), int(round(sh * scale))
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def crop_1440_from_1920(img_1920: Image.Image) -> Image.Image:
    """1080x1920 → 1080x1440 by cropping y240–1680 (center band)."""
    return img_1920.crop((0, 240, 1080, 1680))


def maybe_overlay_hooks(base: Image.Image) -> tuple[Image.Image, bool]:
    """If Chinese looks unusable we could overlay — default: skip auto OCR.
    Provide a light optional overlay path controlled by env OVERLAY=1.
    Returns (image, did_overlay).
    """
    import os

    if os.environ.get("OVERLAY", "0") != "1":
        return base, False

    FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"
    W, H = base.size
    img = base.convert("RGBA")
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)

    def fnt(size, idx=2):
        return ImageFont.truetype(FONT, size, index=idx)

    def outlined(xy, text, font, fill, ow=7, anchor="mm"):
        x, y = xy
        for dx in range(-ow, ow + 1):
            for dy in range(-ow, ow + 1):
                if dx * dx + dy * dy > ow * ow or (dx == 0 and dy == 0):
                    continue
                d.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 230), anchor=anchor)
        d.text((x, y), text, font=font, fill=fill, anchor=anchor)

    # Semi-dark band behind hooks for readability
    band = Image.new("RGBA", (W, int(H * 0.42)), (0, 0, 0, 110))
    img.alpha_composite(band, (0, int(H * 0.08)))

    cy = int(H * 0.18)
    outlined((W // 2, cy), "千万别再花几万块", fnt(72), (255, 248, 236, 255), ow=8)
    cy += int(H * 0.10)
    outlined((W // 2, cy), "刷GEO垃圾稿", fnt(78), (255, 214, 90, 255), ow=8)
    cy += int(H * 0.10)
    outlined((W // 2, cy), "大模型根本不读", fnt(78), (255, 70, 60, 255), ow=8)
    outlined((W // 2, int(H * 0.88)), "GEO · 3步逆向信源", fnt(40), (120, 220, 255, 255), ow=5)

    out = Image.alpha_composite(img, lay).convert("RGB")
    return out, True


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
    key, base = load_creds()
    cred_source = 'mysql_aid62'
    print(f"creds ok base={base} key={key[:6]}…", flush=True)

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
                if cred_source == 'mysql_aid62':
                    print("MySQL key balance不足 → fallback to GEO-sticker/Unichant duomi.json key", flush=True)
                    key, base = FALLBACK_STICKER_CREDS
                    cred_source = 'sticker_duomi_json'
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
            # poll
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
                fitted, overlaid = maybe_overlay_hooks(src)
                # Always fit to 1080x1920 first
                img1920 = cover_fit(fitted if overlaid else src.convert("RGB"), 1080, 1920)
                # If overlay requested after fit for better text placement:
                if overlaid:
                    img1920 = cover_fit(fitted, 1080, 1920)
                img1440 = crop_1440_from_1920(img1920)

                p1920 = OUT / "封面_爆款_1080x1920.png"
                p1440 = OUT / "封面_爆款_1080x1440_抖音.png"
                img1920.save(p1920, "PNG", optimize=True)
                img1440.save(p1440, "PNG", optimize=True)

                prev1920 = COVER_DIR / "preview_爆款_duomi_1080x1920.png"
                prev1440 = COVER_DIR / "preview_爆款_duomi_1080x1440.png"
                img1920.save(prev1920, "PNG", optimize=True)
                img1440.save(prev1440, "PNG", optimize=True)

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
                    "pil_overlay": overlaid,
                    "cred_source": cred_source,
                    "cdn_url": img_url,
                    "prompt_head": PROMPT[:180],
                }
                meta_path = COVER_DIR / "duomi_cover.meta.json"
                meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
                print(json.dumps(meta, ensure_ascii=False, indent=2), flush=True)
                print("DONE", flush=True)
                return

            # task failed / no url — try next size/model
            continue

    print("ALL_FAILED", str(last_err)[:500], flush=True)
    sys.exit(1)


if __name__ == "__main__":
    main()
