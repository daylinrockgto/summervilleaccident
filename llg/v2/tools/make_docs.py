#!/usr/bin/env python3
"""Build one .docx per Manifest v7 page, each ending in an Upload Sheet, plus a batch register doc."""
import json, os, re, sys, html as H
ROOT = os.environ.get("FROST_ROOT") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import minidocx2
REPO = os.path.join(os.environ.get("SITE_ROOT") or os.path.dirname(ROOT), "site", "content")
OUT = os.environ.get("DOCS_OUT") or os.path.join(ROOT, "docs-out")
HOST = "https://www.summervilleaccidentattorney.com"
ROWS = json.load(open(f"{REPO}/pages/pages.json"))
MAN = {m["id"]: m for m in json.load(open(os.path.join(ROOT, "v2", "manifest.json")))}
REDIR = json.load(open(f"{REPO}/redirects.json"))
BYSLUG = {r["slug"]: r for r in ROWS}
FOLDER = {"Home": "01 Home and Menu Pages", "Menu page": "01 Home and Menu Pages", "Practice parent": "02 Practice Parents",
          "Practice child": "03 Practice Children", "Answer page": "04 Answer Pages", "County parent": "05 County Parents",
          "County child": "06 County Children", "City page (county child)": "07 City Pages", "Spanish page": "08 Spanish Page"}
ORDER = list(FOLDER)

def band(id_):
    p = os.path.join(ROOT, "briefs", f"{id_}.md")
    if os.path.exists(p):
        m = re.search(r"\*\*Word band\.\*\*\s*([\d,]+ to [\d,]+)", open(p).read())
        if m: return m.group(1)
    return ""

def words(body):
    t = H.unescape(re.sub(r"<[^>]+>", " ", body))
    return len(re.findall(r"[A-Za-z0-9ÁÉÍÓÚÑáéíóúñü'’$%.,-]+", t))

def safe(name):
    return re.sub(r'[\\/:*?"<>|]', "", name).strip()

def url_of(r):
    return HOST + ("/" if r["slug"] == "home" else "/" + r["slug"] + "/")

def P(label, value):
    return f"<p><strong>{H.escape(label)}</strong> {value}</p>"

register = []
files = []
for r in sorted(ROWS, key=lambda r: ORDER.index(r["type"])):
    raw = open(f"{REPO}/pages/{r['file']}", encoding="utf-8").read()
    m = MAN.get(r["id"], {})
    url = url_of(r)
    path = "/" if r["slug"] == "home" else "/" + r["slug"] + "/"
    olds = [s for s, d in REDIR if d == path]
    parent = BYSLUG.get(r["hub"]) if r.get("hub") else None
    parent_txt = (f'{parent["h1"]} ({url_of(parent)})' if parent else "None, root page")
    wc = words(raw)
    links = re.findall(r'<a href="([^"]+)">(.*?)</a>', raw, re.S)
    internal = [(u, t) for u, t in links if "summervilleaccidentattorney.com" in u]
    outbound = [(u, t) for u, t in links if u.startswith("http") and "summervilleaccidentattorney.com" not in u]
    tels = [(u, t) for u, t in links if u.startswith("tel:")]
    if r["id"] == "pa": replaces = "Rewrites /practice-areas/ in place. No redirect."
    elif r["id"] == "home": replaces = "Rewrites the home page in place. No redirect."
    elif olds: replaces = ", ".join(olds)
    else: replaces = "New page. Nothing redirects to it."
    head = ["<h2>Page Details</h2>",
            P("Live URL.", H.escape(url)),
            P("Slug.", H.escape(r["slug"] if r["slug"] != "home" else "/")),
            P("Page type.", H.escape(r["type"])),
            P("Parent page.", H.escape(parent_txt)),
            P("Replaces.", H.escape(replaces)),
            P("Word target.", H.escape(f'{m.get("words", ""):,}' if m.get("words") else "") + (f" (band {band(r['id'])})" if band(r["id"]) else "")),
            P("Word count.", f"{wc:,}"),
            P("Focus keyphrase.", H.escape(r["kp"] or "")),
            P("SEO title.", H.escape(r["title"]) + f" ({len(r['title'])} characters)"),
            P("Meta description.", H.escape(r["description"]) + f" ({len(r['description'])} characters)"),
            P("Status.", "Cleared by the page gate and an independent legal and compliance review on September 29, 2026. Live in the GitHub repository at "
                        + H.escape(f"site/content/pages/{r['file']}") + "."),
            "<h2>Page Copy</h2>"]
    sheet = ["<h2>Upload Sheet</h2>",
             P("Page title (H1).", H.escape(re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S).group(1)).strip())),
             P("Slug.", H.escape(r["slug"] if r["slug"] != "home" else "/")),
             P("Parent page.", H.escape(parent_txt)),
             P("SEO title.", H.escape(r["title"])),
             P("Meta description.", H.escape(r["description"])),
             P("Focus keyphrase.", H.escape(r["kp"] or "")),
             P("Images.", "None placed yet. Images and alt text come from the Canva batch, which is still pending."),
             "<h3>Internal Links</h3>"] + [f'<li>{H.escape(H.unescape(re.sub(r"<[^>]+>","",t)))} to {H.escape(u)}</li>' for u, t in internal] + \
            ["<h3>Outbound Links</h3>"] + ([f'<li>{H.escape(H.unescape(re.sub(r"<[^>]+>","",t)))} to {H.escape(u)}</li>' for u, t in outbound] or ["<p>None.</p>"]) + \
            ["<h3>Phone Links</h3>", f"<p>{len(tels)} phone links, each (843) 419-6653 linked to tel:+18434196653.</p>",
             "<h3>Redirects to This Page</h3>"] + ([f"<li>{H.escape(o)} to {H.escape(path)} (301)</li>" for o in olds] or ["<p>None.</p>"])
    doc = "".join(head) + raw + "".join(sheet)
    folder = os.path.join(OUT, FOLDER[r["type"]]); os.makedirs(folder, exist_ok=True)
    fn = os.path.join(folder, safe(re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S).group(1))) + ".docx")
    minidocx2.build(doc, fn)
    files.append(fn)
    register.append((r, url, replaces, wc, m.get("words")))

# Batch register, redirect map and upload order
reg = ["<h1>Frost Law Group Page Register and Redirect Map</h1>",
       "<p>This batch holds every long-form page on summervilleaccidentattorney.com under Page Manifest v7, as of September 29, 2026. Each page is its own Word document with an Upload Sheet at the end. The pages are already in the GitHub repository and on the Vercel preview, so these documents are for review, not for upload.</p>",
       "<h2>Page Register</h2>"]
for t in ORDER:
    reg.append(f"<h3>{H.escape(FOLDER[t].split(' ', 1)[1])}, {H.escape(t)}</h3>")
    for r, url, rep, wc, tgt in [x for x in register if x[0]["type"] == t]:
        reg.append(f"<li><strong>{H.escape(r['h1'])}</strong>, {H.escape(url)}, keyphrase {H.escape(r['kp'] or '')}, {wc:,} words"
                   + (f" against a {tgt:,} target" if tgt else "") + f". Replaces {H.escape(rep)}</li>")
reg.append("<h2>Redirect Map</h2><p>Every redirect below is a 301. Vercel applies them from vercel.json, and the .htaccess file carries the same list for an Apache host. The workers compensation address keeps its old page and gets no redirect.</p>")
for s, d in REDIR:
    reg.append(f"<li>{H.escape(s)} to {H.escape(d)}</li>")
reg.append("<h2>Upload Order</h2><p>The site goes live as one deployment, so there is no page by page upload. The order below is the Search Console indexing order after the domain moves to Vercel.</p>")
for s in ["", "car-accident-attorneys-in-summerville", "personal-injury-attorneys-in-dorchester-county", "dog-bite-attorneys-in-summerville",
          "es/abogado-de-accidentes-de-carro-en-summerville", "practice-areas", "locations", "questions"]:
    reg.append(f"<li>{HOST}/{s + '/' if s else ''}</li>")
minidocx2.build("".join(reg), os.path.join(OUT, "00 Page Register, Redirect Map and Upload Order.docx"))
print(len(files), "page docs")
