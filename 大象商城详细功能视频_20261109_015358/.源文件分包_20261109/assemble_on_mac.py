#!/usr/bin/env python3
"""Assemble completed pack parts (512KiB), verify sha256, unzip -n into 源文件."""
import hashlib, json, subprocess, sys
from pathlib import Path
BASE = Path("/Users/jiacong/Downloads/大象商城详细功能视频_20261109_015358")
STAGING = BASE / ".源文件分包_20261109"
PARTS = STAGING / "parts"
DEST = BASE / "源文件"
manifest = json.loads((STAGING/"分包清单.json").read_text())
pm_path = STAGING/"parts_manifest_512.json"
if not pm_path.exists():
    pm_path = STAGING/"parts_manifest.json"
parts_manifest = json.loads(pm_path.read_text())
DEST.mkdir(parents=True, exist_ok=True)
done = []
for pack in parts_manifest.get("packs", []):
    name = pack["pack"]
    expect = next(p["sha256"] for p in manifest["packs"] if p["pack"]==name)
    out = STAGING/name
    part_paths = [PARTS/p["name"] for p in pack["parts"]]
    if not all(p.exists() and p.stat().st_size==info["bytes"] for p,info in zip(part_paths, pack["parts"])):
        missing = sum(1 for p in part_paths if not p.exists())
        print("INCOMPLETE", name, "missing_parts", missing, "of", len(part_paths))
        continue
    ok=True
    for p,info in zip(part_paths, pack["parts"]):
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        if h!=info["sha256"]:
            print("PART_HASH_FAIL", p.name); ok=False
    if not ok: continue
    if out.exists() and hashlib.sha256(out.read_bytes()).hexdigest()==expect:
        print("ALREADY", name)
    else:
        with open(out,'wb') as w:
            for p in part_paths:
                w.write(p.read_bytes())
        h=hashlib.sha256(out.read_bytes()).hexdigest()
        if h!=expect:
            print("ZIP_HASH_FAIL", name, h); continue
        print("ASSEMBLED", name, out.stat().st_size)
    r=subprocess.run(["unzip","-n",str(out),"-d",str(DEST)], capture_output=True, text=True)
    print("UNZIP", name, "rc", r.returncode)
    done.append(name)
print("DONE_PACKS", len(done), done)
