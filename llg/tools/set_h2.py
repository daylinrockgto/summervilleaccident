#!/usr/bin/env python3
"""Rename one H2 in the plan for a page, safely under parallel use.
Usage: python3 set_h2.py <page id> "<old H2 exactly>" "<new H2>"
Then change the same H2 in pages/<id>.html yourself."""
import json, subprocess, sys, os
try:
    import fcntl
except ImportError:  # Windows: no file locking, run one set_h2 at a time
    fcntl = None
pid, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
P = os.path.join(os.environ.get("FROST_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plan")
with open(P + "/.lock", "w") as lk:
    if fcntl: fcntl.flock(lk, fcntl.LOCK_EX)
    plan = json.load(open(P + "/plan.json"))
    pg = next(p for p in plan["pages"] if p["id"] == pid)
    if old not in pg["h2"]:
        sys.exit(f"'{old}' is not a current H2 of {pid}. Current: {pg['h2']}")
    # site-wide duplicate guard
    allh = {h.lower() for p in plan["pages"] for h in p["h2"] if not (p["id"] == pid and h == old)}
    if new.lower() in allh: sys.exit("That H2 already exists on another page. Pick a different one.")
    H = json.load(open(P + "/h2_overrides.json"))
    # chain: if old was itself an override value, update that entry
    d = H.setdefault(pid, {})
    src = next((k for k, v in d.items() if v == old), old)
    d[src] = new
    json.dump(H, open(P + "/h2_overrides.json", "w"), indent=1)
    subprocess.run(["python3", P + "/plan.py"], check=True, capture_output=True)
    print(f"{pid}: H2 '{old}' -> '{new}' recorded in plan")
