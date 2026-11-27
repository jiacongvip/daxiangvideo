#!/usr/bin/env python3
import hashlib, json, subprocess
from pathlib import Path
ST = Path(__file__).resolve().parent
PARTS = ST/"parts2m"
DEST = ST.parent/"源文件"
manifest = json.loads((ST/"分包清单.json").read_text())
pm = json.loads((ST/"parts_manifest_2m.json").read_text())

def assemble(name):
    pack = next(p for p in pm["packs"] if p["pack"]==name)
    expect = next(p["sha256"] for p in manifest["packs"] if p["pack"]==name)
    part_paths = [PARTS/p["name"] for p in pack["parts"]]
    if any(not p.exists() for p in part_paths):
        return False
    for p,info in zip(part_paths, pack["parts"]):
        if hashlib.sha256(p.read_bytes()).hexdigest()!=info["sha256"]:
            print("PART_HASH_FAIL", p.name); return False
    out = ST/name
    if not (out.exists() and hashlib.sha256(out.read_bytes()).hexdigest()==expect):
        with open(out,'wb') as w:
            for p in part_paths: w.write(p.read_bytes())
        if hashlib.sha256(out.read_bytes()).hexdigest()!=expect:
            print("ZIP_HASH_FAIL", name); return False
        print("ASSEMBLED", name, out.stat().st_size)
    with open('/dev/null','wb') as null:
        subprocess.run(["unzip","-n",str(out),"-d",str(DEST)], stdout=null, stderr=null)
    return True

done=[p['pack'] for p in pm['packs'] if assemble(p['pack'])]
print("DONE2M", len(done), "script_json", sum(1 for _ in DEST.rglob('script.json')))
