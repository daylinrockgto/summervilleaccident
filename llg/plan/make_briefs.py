import json, os
import os
ROOT = os.environ.get("FROST_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(f"{ROOT}/plan/plan.json"))
pages = {p["id"]: p for p in d["pages"]}
label = {p["url"]: p["h1"] for p in d["pages"]}
B = "https://www.summervilleaccidentattorney.com"
label.update({B + "/contact": "Contact (existing live page)", B + "/about": "About Our Team (existing live page, attorney bios)",
              B + "/practice-areas": "Practice Areas menu page", B + "/": "Homepage, Summerville Personal Injury Attorneys"})
os.makedirs(f"{ROOT}/briefs", exist_ok=True)
STAR_OK = {"home", "pa", "loc", "car", "truck", "moto", "ride", "slip", "dog", "wd", "cat", "ped"}

def sib(p):
    # pages sharing a parent or topic, to differentiate from
    same = [q for q in d["pages"] if q["id"] != p["id"] and (q.get("parent") == p.get("parent") and q["type"] == p["type"])]
    return [f"{q['id']} ({q['h1']})" for q in same]

for p in d["pages"]:
    L = []
    L.append(f"# Page brief, {p['id']}\n")
    L.append(f"**Page type.** {p['type']}")
    L.append(f"**H1 (exact).** {p['h1']}")
    L.append(f"**Focus keyphrase (exact).** {p['kp']}")
    L.append(f"**URL.** {p['url']}")
    L.append(f"**Parent.** {p['parent']}")
    L.append(f"**Replaces.** {p['replaces']}")
    L.append(f"**Word band.** {p['words'][0]:,} to {p['words'][1]:,}. **Target** {p['target']:,} (land within about 150 words).")
    L.append(f"**SEO title (already written).** {p['title']}")
    L.append(f"**Meta description (already written).** {p['desc']}")
    L.append("")
    L.append(f"## Structural device\n\n{p['device']}\n")
    if p.get("locked_tree"):
        L.append("## Approved heading tree, reproduce exactly\n\n```\n" + p["locked_tree"] + "\n```\n")
    L.append("## H2s, exact, in this order\n")
    for i, h in enumerate(p["h2"], 1):
        L.append(f"{i}. {h}" + ("   (final CTA, no subheadings)" if i == len(p["h2"]) else ""))
    L.append("")
    if p.get("h2_notes"): L.append(f"**H2 notes.** {p['h2_notes']}\n")
    L.append("## Internal links, each exactly once, full URL as written\n")
    L.append(f"**First internal link** (first paragraph under the first H2): {p['first_link'][0]}, anchored on {p['first_link'][1]}.\n")
    for u in p["links"]:
        L.append(f"- {u}  ({label.get(u, '?')})")
    L.append("\nNo other internal URLs. Place each on a natural service, case or county noun inside a sentence about what Frost Law Group does. The contact link goes in the final CTA's last paragraph.\n")
    L.append("## Outbound links, one or two, only these, each once\n")
    for k in p["outbound"]:
        u, what = d["outbound"][k]
        L.append(f"- {u}  (supports: {what})")
    L.append("\nThe strongest one may go in the H1 section paragraph 1 or 2. Anchor on words naming the source, never the keyphrase.\n")
    L.append("## Local hooks to draw from (verified)\n")
    for code in p["local"]:
        key = code.split()[0]
        if key in d["local"]:
            L.append(f"- **{key}** {d['local'][key]}" + (f"  ({code[len(key):].strip()})" if code[len(key):].strip() else ""))
        else:
            L.append(f"- {code}")
    L.append("\nUse at least three verifiable local specifics. Everything else local must come from the county pack or R3.\n")
    L.append("## Page notes\n")
    L.append(p.get("notes") or "None.")
    L.append("")
    L.append(f"**4.8 star Google rating.** {'Allowed once on this page, identified as client reviews on Google.' if p['id'] in STAR_OK else 'NOT allowed on this page.'}")
    imgs = {"parent": "Featured image plus one image directly under EVERY H2 including the CTA H2. About half of the body alts carry the exact keyphrase.",
            "child": "Featured image plus one image under the final H2 only. Every alt carries the exact keyphrase."}.get(p["images"], "No images on this page.")
    L.append(f"**Images for the sidecar.** {imgs}")
    s = sib(p)
    if s: L.append(f"\n**Sibling pages you must not echo** (different angles, examples, headings and sentences): {', '.join(s)}. If their HTML already exists in llg/pages/, skim it before writing so you take different routes.")
    L.append("\n**Deliverables.** `llg/pages/" + p["id"] + ".html` and `llg/pages/" + p["id"] + ".json`, then run `python3 llg/tools/frost_check.py " + p["id"] + " --grammar` until CLEARED.")
    open(f"{ROOT}/briefs/{p['id']}.md", "w").write("\n".join(L))
print(len(d["pages"]), "briefs written")
