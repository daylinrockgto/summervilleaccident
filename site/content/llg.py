"""Long-form pages written to Legal Leads Group's standard for Frost Law Group (Page Manifest v7, 2026-09-28).

Each page is plain HTML in content/pages/<id>.html (h1 to h6, p, a, strong, em) plus one row in content/pages/pages.json.
This module registers them with the page registry:

* the H1 moves into the hero, and the rest of the file becomes the body;
* links to https://www.summervilleaccidentattorney.com/... become [[slug]] tokens, so the builder resolves them and
  warns on any target that does not exist;
* outbound links get rel="noopener" and open in a new tab;
* headings that ask a question, with the paragraphs under them, feed FAQPage structured data.

Copy is edited in the HTML files, never here. The build fails if a page breaks a hard rule (see checks.py).
"""
import html as _html
import json
import os
import re

from .base import page, BY_SLUG
from . import firm

DIR = os.path.join(os.path.dirname(__file__), "pages")
ROWS = json.load(open(os.path.join(DIR, "pages.json"), encoding="utf-8"))
HOST_RE = re.compile(r'href="https?://(?:www\.)?summervilleaccidentattorney\.com(/[^"#?]*)?([#?][^"]*)?"')
EXT_RE = re.compile(r'<a href="(https?://[^"]+)">')
H1_RE = re.compile(r"<h1[^>]*>.*?</h1>\s*", re.S)
HEAD_RE = re.compile(r"<(h[2-6])[^>]*>(.*?)</\1>", re.S)

# Short labels for menus, sidebars and breadcrumbs, by page id.
LABELS = {
    "home": "Home", "pa": "Practice areas", "loc": "Locations",
    "car": "Car accidents", "truck": "Truck accidents", "moto": "Motorcycle accidents", "ride": "Uber and Lyft accidents",
    "slip": "Slip and fall", "dog": "Dog bites", "wd": "Wrongful death", "cat": "Catastrophic injuries", "ped": "Pedestrian accidents",
    "car-dui": "Drunk driving crashes", "car-hr": "Hit and run crashes", "car-distracted": "Distracted driving crashes",
    "truck-tt": "Tractor trailer crashes", "truck-deliv": "Delivery truck crashes", "truck-fatigue": "Truck driver fatigue",
    "moto-left": "Left turn crashes", "moto-helmet": "Helmet law and your claim", "moto-um": "Uninsured motorist claims for riders",
    "ride-uber": "Uber accidents", "ride-lyft": "Lyft accidents",
    "slip-retail": "Store falls", "slip-apt": "Apartment injuries", "slip-prem": "Premises liability",
    "dog-strict": "Strict liability law", "dog-child": "Children bitten by dogs", "dog-ins": "Dog bite insurance claims",
    "wd-car": "Fatal car crashes", "wd-survival": "Survival actions", "wd-truck": "Fatal truck crashes",
    "chs-car": "Car accidents in Charleston County", "chs-truck": "Truck accidents in Charleston County", "chs-moto": "Motorcycle accidents in Charleston County",
    "brk-car": "Car accidents in Berkeley County", "brk-truck": "Truck accidents in Berkeley County", "brk-moto": "Motorcycle accidents in Berkeley County",
    "city-charleston": "Charleston", "city-north-charleston": "North Charleston", "city-mount-pleasant": "Mount Pleasant", "city-west-ashley": "West Ashley",
    "city-goose-creek": "Goose Creek", "city-moncks-corner": "Moncks Corner", "city-ladson": "Ladson", "city-walterboro": "Walterboro",
    "es": "Español", "questions": "Questions",
}
SECTION = {"car": "Car accident help", "truck": "Truck accident help", "moto": "Motorcycle accident help", "ride": "Rideshare accident help",
           "slip": "Slip and fall help", "dog": "Dog bite help", "wd": "Wrongful death help", "cat": "Catastrophic injury help", "ped": "Pedestrian accident help"}
EYEBROW = {"home": "Frost Law Group · Summerville, South Carolina", "hub": "Frost Law Group · Summerville, SC", "spoke": "Frost Law Group · Summerville, SC",
           "page": "Frost Law Group · Summerville, SC"}


def _slug_of(path):
    p = (path or "/").strip("/")
    return "home" if not p else p


def _links(body):
    body = HOST_RE.sub(lambda m: f'href="[[{_slug_of(m.group(1))}]]{m.group(2) or ""}"', body)
    return EXT_RE.sub(lambda m: f'<a href="{m.group(1)}" rel="noopener" target="_blank">', body)


def _faqs(body):
    """Question headings and the paragraphs that follow them, up to the next heading."""
    out = []
    parts = re.split(r"(<h[2-6][^>]*>.*?</h[2-6]>)", body, flags=re.S)
    for i, part in enumerate(parts):
        m = HEAD_RE.fullmatch(part.strip()) if part.strip().startswith("<h") else None
        if not m:
            continue
        q = _html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        if not q.endswith("?") or i + 1 >= len(parts):
            continue
        a = " ".join(re.findall(r"<p>(.*?)</p>", parts[i + 1], re.S))
        a = _html.unescape(re.sub(r"<[^>]+>", "", a)).strip()
        if a:
            out.append((q, a))
    return out


def _hero_lead(row):
    return ""


for row in ROWS:
    raw = open(os.path.join(DIR, row["file"]), encoding="utf-8").read()
    h1m = re.search(r"<h1[^>]*>(.*?)</h1>", raw, re.S)
    h1 = h1m.group(1).strip() if h1m else row["h1"]
    body = _links(H1_RE.sub("", raw, count=1))
    kind = row["kind"]
    kw = dict(title=row["title"], description=row["description"], h1=h1, body=body, kind=kind,
              eyebrow=EYEBROW.get(kind, ""), nav_label=LABELS.get(row["id"], row["h1"]), hub=row.get("hub"),
              county=row.get("county"), section_label=SECTION.get(row["id"]), lang=row.get("lang", "en"),
              priority={"home": 1.0, "hub": 0.9, "spoke": 0.7}.get(kind, 0.6))
    if kind == "home":
        kw.update(layout="one", hero_style="photo", hero_image="couple.jpg", hero_image_wide="couple-wide.jpg",
                  hero_caption="Tara and Jack Frost, Frost Law Group", changefreq="weekly",
                  cta=[("contact", "Get a free case review", "btn light"), ("tel:" + firm.PHONE_E164, firm.PHONE, "btn ghost")])
    elif row["id"] in ("pa", "loc", "questions", "es"):
        kw.update(layout="two", kind="page")
    slug = row["slug"]
    p = page(slug, **kw)
    p["_faq_schema"] = _faqs(body)
    p["_llg"] = row["id"]
    p["_kp"] = row.get("kp")


# Menus and sidebars follow the manifest: each hub lists its children first, then its answer pages.
def _ids(prefix_types):
    return [r for r in ROWS if r["type"] in prefix_types]


PRACTICE_HUBS = [r["slug"] for r in ROWS if r["type"] == "Practice parent"]
COUNTY_HUBS = [r["slug"] for r in ROWS if r["type"] == "County parent"]
HUB_SPOKES = {}
for h in PRACTICE_HUBS + COUNTY_HUBS:
    kids = [r for r in ROWS if r.get("hub") == h]
    kids.sort(key=lambda r: {"Practice child": 0, "County child": 0, "City page (county child)": 1, "Answer page": 2}.get(r["type"], 3))
    HUB_SPOKES[h] = [r["slug"] for r in kids]
CITY_PAGES = [r["slug"] for r in ROWS if r["type"] == "City page (county child)"]
ANSWER_PAGES = [r for r in ROWS if r["type"] == "Answer page"]

firm.HUBS = PRACTICE_HUBS
firm.COUNTY_HUBS = COUNTY_HUBS
firm.HUB_SPOKES = HUB_SPOKES
firm.HUB_ATTORNEY = {h: "tara" for h in PRACTICE_HUBS + COUNTY_HUBS}
firm.CAR = "car-accident-attorneys-in-summerville"
firm.FOOTER_PRACTICE = [(LABELS[r["id"]], r["slug"]) for r in ROWS if r["type"] == "Practice parent"]
firm.FOOTER_AREAS = COUNTY_HUBS + CITY_PAGES
firm.NAV = [
    ("Practice areas", "practice-areas", PRACTICE_HUBS, "All practice areas"),
    ("Locations", "locations", COUNTY_HUBS, "All locations"),
    ("About", "about", ["attorneys/tara-frost", "attorneys/jack-frost", "reviews"], "Our team"),
    ("Questions", "questions", [], ""),
    ("Blog", "blog", [], ""),
]
es = next((r for r in ROWS if r["id"] == "es"), None)
if es:
    firm.NAV.append(("Español", es["slug"], [], ""))
