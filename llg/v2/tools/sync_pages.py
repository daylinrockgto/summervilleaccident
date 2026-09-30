#!/usr/bin/env python3
"""Sync LLG pages into the repo: copies HTML from llg/pages into site/content/pages,
writes site/content/pages/pages.json from plan.json (metadata) + v2/manifest.json (architecture)."""
import json, os, shutil, sys
ROOT = os.environ.get("FROST_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO = os.path.join(os.environ.get("SITE_ROOT") or os.path.dirname(ROOT), "site", "content", "pages")
PLAN = json.load(open(os.path.join(ROOT, "plan", "plan.json")))
MAN = json.load(open(os.path.join(ROOT, "v2", "manifest.json")))
META2 = json.load(open(os.path.join(ROOT, "v2", "meta_v2.json")))
SRC = [os.path.join(ROOT, "pages")]
plan = {p["id"]: p for p in PLAN["pages"]}
KIND = {"Home": "home", "Menu page": "page", "Practice parent": "hub", "County parent": "hub",
        "Practice child": "spoke", "County child": "spoke", "City page (county child)": "spoke", "Answer page": "spoke",
        "Spanish page": "page", "Question index": "page"}
out = []
os.makedirs(REPO, exist_ok=True)
for m in MAN:
    if m["kind"] not in KIND: continue
    src = next((os.path.join(d, m["id"] + ".html") for d in SRC if os.path.exists(os.path.join(d, m["id"] + ".html"))), None)
    if not src:
        continue
    shutil.copy(src, os.path.join(REPO, m["id"] + ".html"))
    p = plan.get(m["id"], {})
    meta = META2.get(m["id"], {})
    slug = m["url"].strip("/") or "home"
    parent = next((x for x in MAN if x["id"] == m["parent"]), None) if m["parent"] else None
    if m["parent"] and not parent:
        parent = next((x for x in MAN if x["id"] == m["parent"]), None)
    hub = None
    if m["kind"] in ("Practice child", "Answer page"):
        hub = next(x for x in MAN if x["id"] == m["parent"])["url"].strip("/")
    elif m["kind"] in ("County child", "City page (county child)"):
        hub = next(x for x in MAN if x["id"] == m["parent"])["url"].strip("/")
    county = None
    if m["id"].startswith("co-"): county = m["h1"].replace("Personal Injury Attorneys in ", "")
    if m["parent"] and str(m["parent"]).startswith("co-"): county = next(x for x in MAN if x["id"] == m["parent"])["h1"].replace("Personal Injury Attorneys in ", "")
    out.append(dict(id=m["id"], slug=slug, kind=KIND[m["kind"]], type=m["kind"], hub=hub, county=county,
                    h1=meta.get("h1") or p.get("h1") or m["h1"], title=meta.get("title") or p.get("title"), description=meta.get("desc") or p.get("desc"),
                    kp=meta.get("kp") or p.get("kp") or m["kp"], nav_label=meta.get("nav") or None, file=m["id"] + ".html", lang="es" if m["id"] == "es" else "en"))
missing = [o["id"] for o in out if not o["title"] or not o["description"]]
if missing: sys.exit(f"missing title/description: {missing}")
json.dump(out, open(os.path.join(REPO, "pages.json"), "w"), indent=1, ensure_ascii=False)
# remove stale html not in manifest output
keep = {o["file"] for o in out} | {"pages.json"}
for f in os.listdir(REPO):
    if f not in keep: os.remove(os.path.join(REPO, f))
print(len(out), "pages synced")
