#!/usr/bin/env python3
"""Static-site generator for summervilleaccidentattorney.com (Frost Law Group's personal injury site).

    python3 site/build_site.py                 -> website/  (production: one folder per URL, sitemap, .htaccess)
    python3 site/build_site.py --preview OUT   -> single-file preview with a hash router (for the artifact)

Content lives in site/content/*.py; assets in site/assets/.
"""
import argparse
import base64
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
ASSETS = os.path.join(SITE, "assets")
IMG_DIR = os.path.join(ASSETS, "img")
OUT = os.path.join(ROOT, "website")
sys.path.insert(0, SITE)

from content.base import PAGES, BY_SLUG, esc  # noqa: E402
from content import firm  # noqa: E402
import content.llg  # noqa: E402,F401  (registers the LLG long-form pages first: home, menus, parents, children, counties)
import content.core  # noqa: E402,F401  (team, contact, reviews, blog index, legal pages)
import content.posts  # noqa: E402,F401
import content.legacy  # noqa: E402,F401  (old workers' compensation copy at its old address, unlinked)
import content.questions_index  # noqa: E402,F401  (link index of answer pages)
import checks  # noqa: E402  (hard compliance checks; the build fails on any of them)
import design  # noqa: E402  (sections, accordions, table of contents, photos and cards for the long-form pages)

BUILD_DATE = firm.BUILD_DATE
ORIGIN = firm.ORIGIN
MODE = "prod"
WARNINGS = []
CSS_HREF = "/assets/site.css"


def file_hash(path, n=8):
    return hashlib.sha1(open(path, "rb").read()).hexdigest()[:n]


def warn(msg):
    WARNINGS.append(msg)


# ---------------------------------------------------------------- URLs & images

def url(slug):
    if slug == "home":
        return "/" if MODE == "prod" else "#/"
    return f"/{slug}/" if MODE == "prod" else f"#/{slug}/"


def abs_url(slug):
    return ORIGIN + ("/" if slug == "home" else f"/{slug}/")


REMAP = {old.strip("/"): (new.strip("/") or "home") for old, new in firm.REDIRECTS}


def resolve(slug):
    """A live slug, or where an old slug now lives (the redirect map), or its nearest live ancestor. None if nothing fits."""
    seen = set()
    while slug not in BY_SLUG and slug in REMAP and slug not in seen:
        seen.add(slug)
        slug = REMAP[slug]
    if slug in BY_SLUG:
        return slug
    parts = slug.split("/")
    while len(parts) > 1:
        parts = parts[:-1]
        cand = "/".join(parts)
        if cand in BY_SLUG:
            return cand
        if cand in REMAP and resolve(cand):
            return resolve(cand)
    return None


_IMG_CACHE = {}
_PLACEHOLDERS = {}


def image_info(name):
    """Return (src, width, height) for an image name; falls back to a generated SVG placeholder."""
    if name in _IMG_CACHE:
        return _IMG_CACHE[name]
    path = os.path.join(IMG_DIR, name)
    if os.path.exists(path):
        if name.lower().endswith(".svg"):
            w, h = 1200, 800
            m = re.search(r'viewBox="0 0 (\d+) (\d+)"', open(path, encoding="utf-8").read())
            if m:
                w, h = int(m.group(1)), int(m.group(2))
            if MODE == "prod":
                src = f"/assets/img/{name}?v={file_hash(path)}"
            else:
                src = "data:image/svg+xml;base64," + base64.b64encode(open(path, "rb").read()).decode()
        else:
            im = Image.open(path)
            w, h = im.size
            if MODE == "prod":
                src = f"/assets/img/{name}?v={file_hash(path)}"
            else:
                buf = io.BytesIO()
                im2 = im.convert("RGB") if im.mode not in ("RGB", "RGBA") else im
                mx = 900
                if im2.width > mx:
                    im2 = im2.resize((mx, round(im2.height * mx / im2.width)), Image.LANCZOS)
                if name.lower().endswith(".png") and im2.mode == "RGBA":
                    im2.save(buf, "PNG", optimize=True)
                    src = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
                else:
                    im2.convert("RGB").save(buf, "JPEG", quality=78, optimize=True, progressive=True)
                    src = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    else:
        warn(f"missing image {name}; placeholder used")
        w, h = (1200, 900) if not name.startswith("head") else (800, 1000)
        label = os.path.splitext(name)[0].replace("-", " ").title()
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
               f'<stop offset="0" stop-color="#173b66"/><stop offset="1" stop-color="#3f86bd"/></linearGradient></defs>'
               f'<rect width="{w}" height="{h}" fill="url(#g)"/><text x="50%" y="52%" text-anchor="middle" font-family="Georgia,serif" font-size="{int(w/22)}" fill="#ffffff" opacity=".9">{esc(label)}</text>'
               f'<text x="50%" y="60%" text-anchor="middle" font-family="Arial,sans-serif" font-size="{int(w/40)}" fill="#dbe7f3">photo to be supplied</text></svg>')
        _PLACEHOLDERS[name] = svg
        pname = "placeholder-" + os.path.splitext(name)[0] + ".svg"
        src = f"/assets/img/{pname}" if MODE == "prod" else "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    _IMG_CACHE[name] = (src, w, h)
    return _IMG_CACHE[name]


def fix_images(html):
    def rep(m):
        tag = m.group(0)
        name = m.group(1)
        src, w, h = image_info(name)
        tag = tag.replace(f"[[img:{name}]]", src)
        if " width=" not in tag:
            tag = tag[:-1] + f' width="{w}" height="{h}">'
        return tag
    return re.sub(r'<img[^>]*src="\[\[img:([^\]]+)\]\]"[^>]*>', rep, html)


def img_tag(name, alt, extra='loading="lazy" decoding="async"'):
    return fix_images('<img src="[[img:%s]]" alt="%s" %s>' % (name, esc(alt), extra))


VARIANT_W = 800  # every JPG wider than this also ships as a 800px copy for phones (see write_prod)


def image_exists(name):
    return os.path.exists(os.path.join(IMG_DIR, name))


def variant_name(name):
    return os.path.splitext(name)[0] + f"-{VARIANT_W}w.jpg"


def resp_img(name, alt, sizes="100vw", cls="", lazy=True):
    """An <img> with width, height and, in production, a srcset that offers the 800px copy to small screens."""
    src, w, h = image_info(name)
    shown_w = min(w, 1600)
    shown_h = round(h * shown_w / w) if w else h
    srcset = ""
    if MODE == "prod" and name.lower().endswith((".jpg", ".jpeg")) and w > VARIANT_W + 100 and image_exists(name):
        small = src.replace(f"/assets/img/{name}", f"/assets/img/{variant_name(name)}")
        srcset = f' srcset="{small} {VARIANT_W}w, {src} {shown_w}w" sizes="{sizes}"'
    c = f' class="{cls}"' if cls else ""
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    return f'<img src="{src}"{srcset} alt="{esc(alt)}" width="{shown_w}" height="{shown_h}"{c}{load}>'


def init_design():
    design.url, design.resp_img, design.image_exists, design.warn = url, resp_img, image_exists, warn

# ---------------------------------------------------------------- token expansion

def card(pg, new=None):
    isnew = (pg["card_new"] if new is None else new) and MODE == "preview"
    return (f'<li class="card{" new" if isnew else ""}"><h3><a href="{url(pg["slug"])}">{esc(pg["nav_label"])}</a></h3>'
            f'<p>{pg["summary"]}</p><a class="more" href="{url(pg["slug"])}">Learn more</a></li>')


def cards(slugs):
    return '<ul class="cards">' + "".join(card(BY_SLUG[s]) for s in slugs) + "</ul>"


def post_card(pg):
    a = firm.ATTORNEYS[pg["author"]]
    cover = ""
    if pg.get("hero_image") and image_exists(pg["hero_image"]):
        cover = f'<a class="cover" href="{url(pg["slug"])}" tabindex="-1" aria-hidden="true">{resp_img(pg["hero_image"], "", sizes="(max-width: 700px) 100vw, 360px")}</a>'
    return (f'<li class="post-card">{cover}<div class="cat">{esc(pg["category"])}</div><h3><a href="{url(pg["slug"])}">{esc(pg["h1"])}</a></h3>'
            f'<p>{pg["summary"]}</p><div class="meta">{fmt_date(pg["date"])} · {esc(a["short"])}</div></li>')


def posts_sorted():
    return sorted([p for p in PAGES if p["kind"] == "post"], key=lambda p: p["date"], reverse=True)


def fmt_date(d):
    return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")


def reviews_html(n):
    out = []
    for r in firm.REVIEWS[:n]:
        out.append(f'<blockquote class="review"><div class="stars" aria-label="{r["stars"]} out of 5 stars">{"★" * r["stars"]}</div><p>“{esc(r["text"])}”</p><footer><b>{esc(r["name"])}</b> · {esc(r["source"])}</footer></blockquote>')
    return '<div class="cards three" style="list-style:none">' + "".join(out) + "</div>"


def team_html():
    figs = []
    for key in ("jack", "tara", "cassie", "dogs"):
        m = firm.TEAM[key]
        inner = f'{img_tag(m["photo"], m["alt"])}<figcaption><b>{esc(m["name"])}</b><span>{esc(m["role"])}</span></figcaption>'
        if m.get("slug"):
            inner = f'<a href="{url(m["slug"])}" style="text-decoration:none">{inner}</a>'
        figs.append(f"<figure>{inner}</figure>")
    return '<div class="team">' + "".join(figs) + "</div>"


def hours_html():
    return '<ul class="hours">' + "".join(f"<li><span>{d}</span><span>{h}</span></li>" for d, h in firm.HOURS_DISPLAY) + "</ul>"


def nap_html():
    return ('<div class="nap">'
            f'<div><h3>Office</h3><p><b>{esc(firm.NAME)}</b><br>{firm.STREET}<br>{firm.CITY}, {firm.STATE} {firm.ZIP}</p>'
            f'<p><a href="{esc(firm.DIRECTIONS_URL)}" rel="noopener" target="_blank">Get directions</a> · <a href="{esc(firm.GBP_URL)}" rel="noopener" target="_blank">Google Business Profile</a></p></div>'
            f'<div><h3>Call or text</h3><p><a href="tel:{firm.PHONE_E164}" style="font-family:var(--display);font-size:1.4rem;font-weight:600;text-decoration:none">{firm.PHONE}</a></p><p class="small">Friday afternoon appointments available on request.</p></div>'
            f'<div><h3>Hours</h3>{hours_html()}</div></div>')


def map_html():
    q = esc(firm.MAP_QUERY)
    embed = esc(firm.MAP_EMBED_URL)
    return (f'<div class="map" data-embed="{embed}"><div class="inner"><div class="pin"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg></div>'
            f'<p><b>{esc(firm.NAME)}</b><br>{firm.STREET}, {firm.CITY}, {firm.STATE} {firm.ZIP}</p>'
            f'<button class="btn sm" type="button" data-loadmap>Load the interactive map</button>'
            f'<p><a href="{esc(firm.DIRECTIONS_URL)}" rel="noopener" target="_blank">Open turn-by-turn directions in Google Maps</a></p></div></div>')


def findus_html():
    items = [
        (firm.GBP_URL, "Google Business Profile", "g"),
        (firm.REVIEW_URL, "Leave a Google review", "star"),
        (firm.PREFERRED_SOURCE_URL, "Add us as a preferred source on Google", "g"),
        (firm.YELP_URL, "Find us on Yelp", "yelp"),
        (firm.FACEBOOK, "Facebook", "fb"),
        (firm.INSTAGRAM, "Instagram", "ig"),
    ]
    out = []
    for href, label, ic in items:
        if not href:
            continue
        out.append(f'<a href="{esc(href)}" rel="noopener" target="_blank">{ICONS.get(ic, "")}{esc(label)}</a>')
    return '<div class="links">' + "".join(out) + "</div>"


def allfaqs_html():
    """Every question answered on the site, grouped by the page that owns it, each linking to that page. Used by /questions/."""
    groups = []
    order = [p for p in PAGES if p["faqs"] and not p["noindex"] and p["kind"] in ("home", "hub", "spoke", "city", "post", "page") and p["slug"] != "questions" and p.get("lang") != "es"]
    kinds = [("Car accidents", lambda p: p["slug"] == firm.CAR or p.get("hub") == firm.CAR),
             ("Trucks, motorcycles, pedestrians and rideshare", lambda p: any(p["slug"].startswith(h) for h in ("practice-areas/truck", "practice-areas/motorcycle", "practice-areas/pedestrian"))),
             ("Dog bites", lambda p: p["slug"].startswith("practice-areas/dog-bites")),
             ("Falls, work injuries, catastrophic injuries and wrongful death", lambda p: any(p["slug"].startswith(h) for h in ("practice-areas/slip", "practice-areas/workers", "practice-areas/catastrophic", "practice-areas/wrongful"))),
             ("Your town", lambda p: p["kind"] == "city"),
             ("From the blog", lambda p: p["kind"] == "post"),
             ("Working with us", lambda p: True)]
    used = set()
    for label, test in kinds:
        items = []
        for p in order:
            if p["slug"] in used or not test(p):
                continue
            used.add(p["slug"])
            for q, a in p["faqs"]:
                text = re.sub(r"<[^>]+>", "", a)
                items.append(f'<details><summary>{esc(q)}</summary><div class="a"><p>{esc(text)}</p><p class="small"><a href="{url(p["slug"])}">Read the full page: {esc(p["nav_label"] if p["kind"] != "post" else p["h1"])} →</a></p></div></details>')
        if items:
            groups.append(f'<h2>{esc(label)}</h2><div class="faq">{"".join(items)}</div>')
    return "".join(groups)


def form_html():
    """The free-case-review form (Formspree). One per page; the inline script submits it over AJAX and redirects to /thank-you/."""
    topics = ["Car accident", "Truck accident", "Motorcycle accident", "Pedestrian or bicycle accident", "Uber or Lyft accident", "Hit by a drunk driver", "Dog bite",
              "Slip and fall", "Injured at work", "Catastrophic injury", "Wrongful death", "Something else"]
    opts = "".join(f"<option>{esc(t)}</option>" for t in topics)
    return (f'<form class="form" method="POST" action="{esc(firm.FORM_ENDPOINT)}" accept-charset="UTF-8" data-contact data-thanks="{url("thank-you")}">'
            f'<input type="hidden" name="_subject" value="Injury site inquiry">'
            f'<input type="hidden" name="_next" value="{ORIGIN}/thank-you/">'
            f'<input type="hidden" name="site" value="summervilleaccidentattorney.com">'
            '<div class="row"><label>Your name<input type="text" name="name" autocomplete="name" required></label>'
            '<label>Phone<input type="tel" name="phone" autocomplete="tel" required></label></div>'
            '<label>Email<input type="email" name="email" autocomplete="email"></label>'
            f'<label>What happened?<select name="topic">{opts}</select></label>'
            '<label>Tell us briefly what happened, when, and where<textarea name="message" required></textarea></label>'
            '<label class="hp" aria-hidden="true">Leave this field empty<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label>'
            '<p class="fine">Free, confidential and no obligation. Sending a message does not create an attorney-client relationship until we agree in writing to represent you. Please do not give a recorded statement to any insurance company before we talk.</p>'
            f'<p class="fine" data-formmsg hidden style="color:#8a1c1c">We could not send that message. Please call <a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a> or email <a href="mailto:{firm.EMAIL}">{firm.EMAIL}</a>.</p>'
            '<div><button class="btn" type="submit">Request my free case review</button></div></form>')


def citylist_html():
    cities = [p for p in PAGES if p["kind"] == "city"]
    by_county = {}
    for c in cities:
        by_county.setdefault(c["county"], []).append(c)
    out = []
    for county in firm.COUNTY_ORDER:
        if county not in by_county:
            continue
        lis = "".join(f'<li><a href="{url(c["slug"])}">{esc(c["nav_label"])}</a><small>{esc(c["section_label"] or "")}</small></li>' for c in sorted(by_county[county], key=lambda x: x["nav_label"]))
        out.append(f'<h3>{esc(county)}</h3><ul class="areas">{lis}</ul>')
    return "".join(out)


def courts_html(keys):
    out = []
    for k in keys:
        c = firm.COURTS.get(k)
        if not c:
            warn(f"court {k} missing from local_data.json")
            continue
        addr = f'{esc(c["street"])}, {esc(c["city"])}, SC {esc(c["zip"])}'
        extra = f'<p>{esc(c["note"])}</p>' if c.get("note") else ""
        link = f' · <a href="{esc(c["url"])}" rel="noopener" target="_blank">Website</a>' if c.get("url") else ""
        phone = f' · {esc(c["phone"])}' if c.get("phone") else ""
        out.append(f'<div class="court"><h3>{esc(c["name"])}</h3><p>{addr}{phone}{link}</p>{extra}</div>')
    return '<div class="county-grid">' + "".join(out) + "</div>"


def author_box(key, reviewer=None):
    a = firm.ATTORNEYS[key]
    rev = ""
    if reviewer:
        r = firm.ATTORNEYS[reviewer]
        rev = f' Reviewed by <a href="{url(r["slug"])}">{esc(r["name"])}</a>.'
    return (f'<div class="byline">{img_tag(a["headshot"], a["name"])}'
            f'<p><b>Written by <a href="{url(a["slug"])}">{esc(a["name"])}</a></b>, {esc(a["byline"])}.{rev}</p></div>')


ICONS = {
    "g": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.6 12.2c0-.7-.1-1.3-.2-1.9H12v3.7h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.7 3-4.3 3-7.3z"/><path d="M12 22c2.7 0 5-.9 6.6-2.4l-3.2-2.5c-.9.6-2 1-3.4 1a6 6 0 0 1-5.6-4.1H3.1v2.6A10 10 0 0 0 12 22z"/><path d="M6.4 14a6 6 0 0 1 0-3.9V7.5H3.1a10 10 0 0 0 0 9.1L6.4 14z"/><path d="M12 6c1.5 0 2.8.5 3.8 1.5l2.9-2.9A10 10 0 0 0 3.1 7.5L6.4 10A6 6 0 0 1 12 6z"/></svg>',
    "star": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2 3 6.6 7 .8-5.2 4.8 1.4 7L12 17.7 5.8 21.2l1.4-7L2 9.4l7-.8z"/></svg>',
    "yelp": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.6 2.4c.5-.7 1.6-.5 1.8.4l.3 8.6c0 .9-1 1.4-1.7.9L4.6 8.2c-.7-.5-.5-1.6.3-1.8l5.7-4zm2.7 11.2 6.7-2.3c.9-.3 1.7.7 1.2 1.5l-2.4 3.4c-.5.7-1.6.6-1.9-.2l-3.7-1.4c-.4-.3-.3-.9.1-1zm-1 2.5 5 5.1c.6.7 0 1.8-.9 1.6l-4.1-1c-.8-.2-1.1-1.2-.6-1.8l.5-3.7c0-.5.7-.6 1-.2h-.9zm-2.1-1 .9 7c.1.9-1 1.5-1.7 1L6 21.1c-.7-.5-.5-1.6.3-1.9l3.6-3.6c.3-.4.9-.2.9.3l-.6-.8zm-.5-2.2L3.4 14c-.9.3-1.7-.7-1.2-1.5l2.4-3.4c.5-.7 1.6-.6 1.9.2l3.7 1.3c.4.2.3.9-.1 1l-.4 1.3z"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 22v-8.2h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.6-1.6h1.7V4.1c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.4H7.4v3.2h2.8V22h3.3z"/></svg>',
    "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7.2A4.8 4.8 0 1 0 12 16.8 4.8 4.8 0 1 0 12 7.2zm0 7.9a3.1 3.1 0 1 1 0-6.2 3.1 3.1 0 0 1 0 6.2zM17 5.9a1.1 1.1 0 1 0 0 2.2 1.1 1.1 0 0 0 0-2.2zM21.9 8c-.1-1.5-.4-2.9-1.5-4S18 2.4 16.5 2.3C15 2.2 9 2.2 7.5 2.3 6 2.4 4.6 2.7 3.6 3.8S2.2 6.3 2.1 7.8C2 9.3 2 15 2.1 16.5c.1 1.5.4 2.9 1.5 4s2.5 1.4 4 1.5c1.5.1 7.5.1 9 0 1.5-.1 2.9-.4 4-1.5s1.4-2.5 1.5-4c.1-1.5.1-7.5-.2-8.5zm-2.2 10.7c-.3.8-.9 1.4-1.7 1.7-1.2.5-4 .4-5.9.4s-4.8.1-6-.4c-.8-.3-1.4-.9-1.7-1.7-.5-1.2-.4-4-.4-5.9s-.1-4.8.4-6c.3-.8.9-1.4 1.7-1.7C7.3 4.6 10.1 4.7 12 4.7s4.8-.1 6 .4c.8.3 1.4.9 1.7 1.7.5 1.2.4 4 .4 5.9s.1 4.8-.4 6z"/></svg>',
    "in": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.2 8h4.6v14H.2V8zm7.6 0h4.4v1.9h.1c.6-1.1 2.1-2.3 4.3-2.3 4.6 0 5.4 3 5.4 6.9V22h-4.6v-6.6c0-1.6 0-3.6-2.2-3.6s-2.5 1.7-2.5 3.5V22H7.8V8z"/></svg>',
    "x": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.5 3h3.1l-6.8 7.8L21.8 21h-6.3l-4.9-6.4L5 21H1.9l7.3-8.3L1.5 3H8l4.4 5.9L17.5 3zm-1.1 16.2h1.7L7 4.7H5.2l11.2 14.5z"/></svg>',
}


def expand_tokens(html):
    html = re.sub(r"\[\[cards:([a-z0-9,/-]+)\]\]", lambda m: cards(m.group(1).split(",")), html)
    html = re.sub(r"\[\[postcards:([a-z0-9,/-]+)\]\]", lambda m: '<ul class="posts">' + "".join(post_card(BY_SLUG[s]) for s in m.group(1).split(",")) + "</ul>", html)
    html = re.sub(r"\[\[latestposts:(\d+)\]\]", lambda m: '<ul class="posts">' + "".join(post_card(p) for p in posts_sorted()[: int(m.group(1))]) + "</ul>", html)
    html = re.sub(r"\[\[reviews:(\d+)\]\]", lambda m: reviews_html(int(m.group(1))), html)
    html = re.sub(r"\[\[courts:([a-z0-9,_-]+)\]\]", lambda m: courts_html(m.group(1).split(",")), html)
    html = re.sub(r"\[\[author:([a-z]+)(?::([a-z]+))?\]\]", lambda m: author_box(m.group(1), m.group(2)), html)
    html = html.replace("[[team]]", team_html()).replace("[[nap]]", nap_html()).replace("[[map]]", map_html())
    html = html.replace("[[findus]]", findus_html()).replace("[[hours]]", hours_html()).replace("[[citylist]]", citylist_html())
    html = html.replace("[[form]]", form_html())
    if "[[allfaqs]]" in html:
        html = html.replace("[[allfaqs]]", allfaqs_html())
    if "[[practice-cards]]" in html:
        from content.core import practice_cards
        html = html.replace("[[practice-cards]]", practice_cards())
    html = fix_images(html)
    # remaining [[slug]] tokens are internal links
    def link(m):
        slug = resolve(m.group(1))
        if slug is None:
            warn(f"unknown link target [[{m.group(1)}]]")
            return "#"
        return url(slug)
    html = re.sub(r"\[\[([a-z0-9/-]+)\]\]", link, html)
    return html


# ---------------------------------------------------------------- layout pieces

def nav_html():
    def sub(hub_slug, spokes, all_label):
        lis = f'<a class="all" href="{url(hub_slug)}">{all_label}</a>' + "".join(f'<a href="{url(s)}">{esc(BY_SLUG[s]["nav_label"])}</a>' for s in spokes)
        return f'<div class="sub{" wide" if len(spokes) > 5 else ""}">{lis}</div>'
    items = []
    for label, hub_slug, spokes, all_label in firm.NAV:
        if hub_slug not in BY_SLUG:
            continue
        spokes = [s for s in spokes if s in BY_SLUG]
        if spokes:
            items.append(f'<li class="has-sub"><a href="{url(hub_slug)}" aria-haspopup="true">{label}</a>'
                         f'<button class="sub-toggle" type="button" aria-expanded="false" aria-label="Show the {esc(label.lower())} menu" data-subtoggle><span aria-hidden="true"></span></button>'
                         f'{sub(hub_slug, spokes, all_label)}</li>')
        else:
            href = url(hub_slug) if hub_slug in BY_SLUG else hub_slug
            items.append(f'<li><a href="{esc(href)}">{label}</a></li>')
    items.append(f'<li class="cta"><a class="btn sm" href="{url("contact")}">Free case review</a></li>')
    return f'<nav class="nav" id="nav" aria-label="Main"><ul>{"".join(items)}</ul></nav>'


def header_html():
    logo_src, lw, lh = image_info(firm.LOGO)
    promises = " · ".join(firm.PROMISES)
    return (
        f'<a class="skip" href="#main">Skip to content</a>'
        f'<div class="topbar"><div class="wrap"><span class="tag"><span class="line">{esc(promises)} <span style="color:#7f95b0">·</span> </span>'
        f'<a class="xsite" href="{esc(firm.MAIN_SITE)}/" rel="noopener">{firm.CROSS_LINK_SHORT} →</a></span>'
        f'<a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a></div></div>'
        f'<header class="hdr"><div class="wrap">'
        f'<a class="brand" href="{url("home")}" aria-label="{esc(firm.SITE_NAME)} home"><img src="{logo_src}" alt="" width="{lw}" height="{lh}"><span class="word">{esc(firm.SITE_NAME)}<small>{esc(firm.SITE_SUB)}</small></span></a>'
        f'<a class="phone-hdr" href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'
        f'<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" data-navtoggle>Menu</button>'
        f'{nav_html()}</div><div class="progress" aria-hidden="true"><span></span></div></header>')


def footer_html():
    logo_src, lw, lh = image_info(firm.LOGO)
    pa = "".join(f'<li><a href="{url(s)}">{esc(l)}</a></li>' for l, s in firm.FOOTER_PRACTICE if s in BY_SLUG)
    explore = "".join(f'<li><a href="{url(s)}">{esc(l)}</a></li>' for l, s in firm.FOOTER_EXPLORE if s in BY_SLUG)
    areas = "".join(f'<li><a href="{url(s)}">{esc(BY_SLUG[s]["nav_label"])}</a></li>' for s in firm.FOOTER_AREAS if s in BY_SLUG)
    soc = "".join(f'<a href="{esc(h)}" rel="noopener" target="_blank" aria-label="{esc(l)}">{ICONS[i]}</a>' for l, h, i in firm.SOCIAL if h)
    find = (f'<li><a href="{esc(firm.GBP_URL)}" rel="noopener" target="_blank">Google Business Profile</a></li>'
            f'<li><a href="{esc(firm.DIRECTIONS_URL)}" rel="noopener" target="_blank">Directions</a></li>'
            f'<li><a href="{esc(firm.REVIEW_URL)}" rel="noopener" target="_blank">Leave a Google review</a></li>'
            f'<li><a href="{esc(firm.YELP_URL)}" rel="noopener" target="_blank">Find us on Yelp</a></li>')
    return (
        f'<footer class="foot"><div class="wrap"><div class="grid">'
        f'<div><a class="brand" href="{url("home")}"><img src="{logo_src}" alt="" width="{lw}" height="{lh}"><span class="word">{esc(firm.SITE_NAME)}<small>{esc(firm.SITE_SUB)}</small></span></a>'
        f'<p class="tagline">{esc(" · ".join(firm.PROMISES))}</p>'
        f'<address><b>{esc(firm.NAME)}</b><br>{firm.STREET}<br>{firm.CITY}, {firm.STATE} {firm.ZIP}<br><a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a><br><a href="mailto:{firm.EMAIL}">{firm.EMAIL}</a></address>'
        f'<p class="small" style="color:#93a4ba;margin:.6rem 0 0">{firm.HOURS_SHORT}</p><div class="soc">{soc}</div>'
        f'<div class="xsite-box"><b>Our main firm site</b><p>{firm.CROSS_LINK_TEXT}, <a href="{esc(firm.MAIN_SITE)}/" rel="noopener">{esc(firm.MAIN_SITE_LABEL)}</a>. Same office, same attorneys, same phone number.</p></div></div>'
        f'<div><h3>Injury cases we handle</h3><ul>{pa}</ul></div>'
        f'<div><h3>Explore</h3><ul>{explore}</ul><h3 style="margin-top:1.4rem">Find us</h3><ul>{find}</ul></div>'
        f'<div><h3>Locations we serve</h3><ul>{areas}<li><a href="{url("locations")}">All locations →</a></li></ul></div>'
        f'</div><div class="legal"><p>© {BUILD_DATE[:4]} {esc(firm.NAME)}. {firm.DISCLAIMER}</p>'
        f'<p><a href="{url("privacy-policy")}">Privacy policy</a> · <a href="{url("terms-of-use")}">Terms of use &amp; legal disclaimer</a> · <a href="{url("accessibility")}">Accessibility</a> · <a href="{url("locations")}">Locations we serve</a>' + ''.join(f' · <a href="{url(p["slug"])}" lang="es">Español</a>' for p in PAGES if p.get("lang") == "es") + '</p></div></div></footer>'
        + action_bar())


def action_bar(lang="en"):
    """Phone and free review buttons fixed to the bottom of small screens, and a back-to-top button."""
    label = "Consulta gratis" if lang == "es" else "Free case review"
    return (f'<div class="mbar" role="region" aria-label="Contact Frost Law Group"><a class="mbar-call" href="tel:{firm.PHONE_E164}">{design.PHONE_SVG}{firm.PHONE}</a>'
            f'<a class="mbar-cta" href="{url("contact")}">{label}</a></div>'
            '<a class="totop" href="#main" aria-label="Back to top" data-totop><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 14 6-6 6 6"/></svg></a>')


def breadcrumb_trail(p):
    trail = [("home", "Home")]
    top = p["hub"] if p["kind"] == "spoke" and p["hub"] else p["slug"]
    if top in getattr(firm, "COUNTY_HUBS", []) and "locations" in BY_SLUG and p["slug"] != "locations":
        trail.append(("locations", "Locations"))
    elif top in firm.HUBS and "practice-areas" in BY_SLUG and p["slug"] != "practice-areas":
        trail.append(("practice-areas", "Practice areas"))
    if p["kind"] == "spoke" and p["hub"]:
        trail.append((p["hub"], BY_SLUG[p["hub"]]["nav_label"]))
    elif p["kind"] == "post":
        trail.append(("blog", "Blog"))
    elif p["kind"] == "attorney":
        trail.append(("about", "Our team"))
    elif p["hub"]:
        trail.append((p["hub"], BY_SLUG[p["hub"]]["nav_label"]))
    trail.append((p["slug"], p["nav_label"]))
    return trail


def crumbs_html(p):
    if p["kind"] == "home":
        return ""
    trail = breadcrumb_trail(p)
    lis = "".join(f'<li><a href="{url(s)}">{esc(l)}</a></li>' for s, l in trail[:-1]) + f'<li aria-current="page">{esc(trail[-1][1])}</li>'
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'


def hero_html(p):
    cta = p["cta"]
    if cta is None:
        cta = [("contact", "Get a free case review", "btn"), (f"tel:{firm.PHONE_E164}", firm.PHONE, "btn ghost")]
    actions = ""
    if cta:
        btns = []
        for target, label, cls in cta:
            href = target if target.startswith(("tel:", "http", "mailto:")) else url(target)
            btns.append(f'<a class="{cls}" href="{esc(href)}">{esc(label)}</a>')
        actions = f'<div class="actions">{"".join(btns)}</div>'
    kicker = f'<p class="kicker">{p["kicker"]}</p>' if p["kicker"] else ""
    eyebrow = f'<div class="eyebrow">{esc(p["eyebrow"])}</div>' if p["eyebrow"] else ""
    lead = f'<p class="lead">{p["lead"]}</p>' if p["lead"] else ""
    quote = f'<p class="quote">{p["quote"]}</p>' if p["quote"] else ""
    meta = ""
    if p["kind"] == "post":
        a = firm.ATTORNEYS[p["author"]]
        meta = (f'<div class="post-meta"><span class="cat">{esc(p["category"])}</span><span>By <a href="{url(a["slug"])}">{esc(a["name"])}</a></span>'
                f'<span>Published {fmt_date(p["date"])}</span>' + (f'<span>Updated {fmt_date(p["modified"])}</span>' if p["modified"] != p["date"] else "") + "</div>")
    if p.get("hero_style") == "photo" and p["hero_image"]:
        src, w, h = image_info(p["hero_image"])
        if " · " in p["eyebrow"]:  # keep only the first part (the tagline) on small screens
            first, rest = esc(p["eyebrow"]).split(" · ", 1)
            eyebrow = f'<div class="eyebrow">{first}<span class="eb2"> · {rest}</span></div>'
        text = f'<div>{kicker}{eyebrow}<h1>{p["h1"]}</h1>{lead}{actions}</div>'
        band_ = f'<div class="quote-band"><div class="wrap">{p["quote"]}</div></div>' if p["quote"] else ""
        img_html = f'<img class="bg" src="{src}" alt="{esc(p["hero_caption"] or "")}" width="{w}" height="{h}" fetchpriority="high">'
        if p.get("hero_image_wide"):  # wide crop with room for the text beside the subjects on large screens
            wsrc, _, _ = image_info(p["hero_image_wide"])
            img_html = f'<picture><source media="(min-width:1101px)" srcset="{wsrc}">{img_html}</picture>'
        return (f'<section class="hero photo"><div class="media">{img_html}<div class="shade"></div></div>'
                f'<div class="wrap">{text}</div></section>{band_}')
    promises = ""
    if p.get("_llg") and p.get("lang") != "es":
        promises = '<ul class="promises">' + "".join(f"<li>{esc(x)}</li>" for x in firm.PROMISES) + "</ul>"
    text = f'<div class="hero-text">{crumbs_html(p)}{kicker}{eyebrow}<h1>{p["h1"]}</h1>{meta}{lead}{actions}{promises}{quote}</div>'
    feat = design.featured(p) if p.get("_llg") else None
    if feat:
        fig = f'<figure class="hero-fig">{resp_img(feat[0], feat[1], sizes="(max-width: 820px) 100vw, 500px", lazy=False)}</figure>'
        return f'<section class="hero has-photo"><div class="wrap">{text}{fig}</div></section>'
    if p["hero_image"]:
        src, w, h = image_info(p["hero_image"])
        cap = f'<figcaption>{esc(p["hero_caption"])}</figcaption>' if p["hero_caption"] else ""
        fig = f'<figure><img src="{src}" alt="{esc(p["hero_caption"] or p["h1"])}" width="{w}" height="{h}" fetchpriority="high">{cap}</figure>'
        return f'<section class="hero"><div class="wrap">{text}{fig}</div></section>'
    return f'<section class="hero plain"><div class="wrap">{text}</div></section>'


def faq_html(faqs):
    items = "".join(f'<details><summary>{esc(q)}</summary><div class="a"><p>{a}</p></div></details>' for q, a in faqs)
    return f'<h2 id="faq">Questions people ask</h2><div class="faq">{items}</div>'


def related_html(p):
    rel = []
    for s in p["related"]:
        r = resolve(s)
        if r and r != p["slug"] and r not in rel:
            rel.append(r)
    if not rel:
        return ""
    return '<h2>Related pages</h2><ul class="cards">' + "".join(card(BY_SLUG[s], new=False) for s in rel) + "</ul>"


def aside_html(p):
    cards_ = []
    cards_.append(f'<div class="acard navy"><h3>Free case review</h3><a class="big" href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'
                  f'<p style="margin:0 0 .8rem;font-size:.95rem">{firm.ASIDE_BLURB}</p><a class="btn light sm" href="{url("contact")}">Tell us what happened</a>'
                  f'<p class="hours" style="color:#b9c9db">{esc(" · ".join(firm.PROMISES))}</p></div>')
    if p["kind"] in ("hub", "spoke"):
        hub = p["slug"] if p["kind"] == "hub" else p["hub"]
        spokes = [s for s in firm.HUB_SPOKES.get(hub, []) if s in BY_SLUG][:14]
        lis = f'<li class="{"here" if p["slug"] == hub else ""}"><a href="{url(hub)}">{esc(BY_SLUG[hub]["nav_label"])} overview</a></li>'
        lis += "".join(f'<li class="{"here" if s == p["slug"] else ""}"><a href="{url(s)}">{esc(BY_SLUG[s]["nav_label"])}</a></li>' for s in spokes)
        cards_.append(f'<div class="acard"><h3>{esc(BY_SLUG[hub]["section_label"] or BY_SLUG[hub]["nav_label"])}</h3><ul>{lis}</ul></div>')
        key = firm.HUB_ATTORNEY.get(hub)
        if key:
            a = firm.ATTORNEYS[key]
            cards_.append(f'<div class="acard"><div class="person">{img_tag(a["headshot"], a["name"])}<div><b>{esc(a["name"])}</b><small>{esc(a["byline"])}</small></div></div>'
                          f'<p style="font-size:.93rem;margin:.8rem 0 0">{a["aside"]}</p><p style="margin:.6rem 0 0;font-size:.93rem"><a href="{url(a["slug"])}">Read {esc(a["first"])}\'s background →</a></p></div>')
    elif p["kind"] == "city":
        same = [c for c in PAGES if c["kind"] == "city" and c["county"] == p["county"] and c["slug"] != p["slug"]]
        lis = "".join(f'<li><a href="{url(c["slug"])}">{esc(c["nav_label"])}</a></li>' for c in sorted(same, key=lambda x: x["nav_label"])[:9])
        cards_.append(f'<div class="acard"><h3>Also serving {esc(p["county"])}</h3><ul>{lis}<li><a href="{url("areas")}">All service areas →</a></li></ul></div>')
        lis2 = "".join(f'<li><a href="{url(s)}">{esc(BY_SLUG[s]["nav_label"])}</a></li>' for s in firm.HUBS[:6])
        cards_.append(f'<div class="acard"><h3>Injury cases we handle</h3><ul>{lis2}<li><a href="{url("practice-areas")}">All practice areas →</a></li></ul></div>')
    elif p["kind"] == "post":
        a = firm.ATTORNEYS[p["author"]]
        cards_.append(f'<div class="acard"><div class="person">{img_tag(a["headshot"], a["name"])}<div><b>{esc(a["name"])}</b><small>{esc(a["byline"])}</small></div></div><p style="font-size:.93rem;margin:.8rem 0 0">{a["aside"]}</p></div>')
        others = [q for q in posts_sorted() if q["slug"] != p["slug"]][:4]
        lis = "".join(f'<li><a href="{url(q["slug"])}">{esc(q["h1"])}</a></li>' for q in others)
        cards_.append(f'<div class="acard"><h3>More from the blog</h3><ul>{lis}<li><a href="{url("blog")}">All articles →</a></li></ul></div>')
    elif p["kind"] == "attorney":
        other = "tara" if p["author"] == "jack" else "jack"
        o = firm.ATTORNEYS[other]
        cards_.append(f'<div class="acard"><h3>Also on the team</h3><div class="person">{img_tag(o["headshot"], o["name"])}<div><b><a href="{url(o["slug"])}" style="text-decoration:none">{esc(o["name"])}</a></b><small>{esc(o["byline"])}</small></div></div></div>')
    else:
        lis = "".join(f'<li><a href="{url(s)}">{esc(BY_SLUG[s]["nav_label"])}</a></li>' for s in (firm.HUBS[:6] + ["about", "reviews", "locations"]) if s in BY_SLUG)
        cards_.append(f'<div class="acard"><h3>Explore</h3><ul>{lis}</ul></div>')
    return '<aside class="aside">' + "".join(cards_) + "</aside>"


def reviews_band():
    """Three Google review quotes for the home page (settled 2026-09-28: the quotes stay on home and reviews)."""
    picks = [r for r in firm.REVIEWS if r["name"] in ("Shannon D.", "Kevin O.", "Michelle F.")]
    cards = "".join(f'<blockquote class="review"><div class="stars" aria-label="{r["stars"]} out of 5 stars">{"★" * r["stars"]}</div><p>“{esc(r["text"])}”</p><footer><b>{esc(r["name"])}</b> · {esc(r["source"])}</footer></blockquote>' for r in picks)
    return (f'<section class="hsec reviews-band"><div class="wrap"><p class="ex-title center">Frost Law Group is rated {firm.RATING} stars on Google</p>'
            f'<div class="rev-grid">{cards}</div><p class="small center">Testimonials reflect individual experiences. Prior results do not guarantee a similar outcome. '
            f'<a href="{url("reviews")}">Read more client reviews</a></p></div></section>')


def home_body(p):
    """The home page: full-width bands, cards for the practice areas and counties, and the attorneys beside the copy."""
    p["_toc"] = False
    inserts = {
        1: design.photo_cards(firm.HUBS, "pcards three"),
        2: design.attorney_panel(),
        3: design.photo_cards(firm.COUNTY_HUBS, "pcards four"),
        "after:2": reviews_band(),
    }
    n = [0]

    def shell(cls, sid, inner):
        n[0] += 1
        if "sec-cta" in cls:
            return f'<section class="hsec cta-band" id="{sid}"><div class="wrap"><div class="{cls}">{inner}</div></div></section>'
        band = " tint" if n[0] == 2 else ""
        return f'<section class="hsec {cls}{band}" id="{sid}"><div class="wrap">{inner}</div></section>'

    intro_img = design.IMAGES.get("home", {}).get("intro")

    def intro_shell(h):
        fig = f'<figure class="intro-fig">{resp_img(intro_img["file"], intro_img["alt"], sizes="(max-width: 900px) 100vw, 380px")}</figure>' if intro_img and image_exists(intro_img["file"]) else ""
        return f'<section class="hsec intro-band"><div class="wrap{" intro-grid" if fig else ""}"><div>{h}</div>{fig}</div></section>'

    inner, _ = design.enhance(p, p["body"], inserts, shell=shell, intro_shell=intro_shell)
    return f'<main id="main" class="home">{inner}</main>'


def after_content(p):
    if p["kind"] not in ("hub", "spoke", "city"):
        return ""
    return f'<div class="atty-block"><p class="ex-title">The attorneys at Frost Law Group</p>{design.attorney_panel(compact=False)}</div>' + design.explore(p)


def menu_inserts(p):
    if p["slug"] == "practice-areas":
        return {"intro": design.photo_cards(firm.HUBS, "pcards three")}
    if p["slug"] == "locations":
        cities = "".join(f'<a href="{url(s)}">{esc(BY_SLUG[s]["nav_label"])}</a>' for s in getattr(firm, "CITY_PAGES", []) if s in BY_SLUG)
        return {"intro": design.photo_cards(firm.COUNTY_HUBS, "pcards four") + (f'<div class="chips">{cities}</div>' if cities else "")}
    return {}


def body_html(p):
    if p.get("_llg") and p["kind"] == "home":
        return home_body(p)
    if p.get("_llg"):
        inner, secs = design.enhance(p, p["body"], menu_inserts(p))
        inner += after_content(p)
        if p["sources"]:
            from content.base import sources as _sources
            inner += _sources(p["sources"])
        if p["layout"] == "two":
            return f'<main id="main"><div class="wrap layout long"><div class="main prose long">{inner}</div>{design.aside_long(p, secs)}</div></main>'
        return f'<main id="main"><div class="wrap layout single long"><div class="main prose long">{inner}</div></div></main>'
    if p["kind"] == "post":
        inner, secs = design.enhance(p, p["body"])
        inner += f"[[author:{p['author']}{':' + p['reviewer'] if p['reviewer'] else ''}]]"
        if p["faqs"]:
            inner += faq_html(p["faqs"])
        if p["sources"]:
            from content.base import sources as _sources
            inner += _sources(p["sources"])
        others = [q["slug"] for q in posts_sorted() if q["slug"] != p["slug"]][:3]
        inner += '<nav class="explore" aria-label="More from the blog"><p class="ex-title">More from the blog</p><ul class="posts">' + "".join(post_card(BY_SLUG[s]) for s in others) + "</ul></nav>"
        return f'<main id="main"><div class="wrap layout long"><div class="main prose long">{inner}</div>{design.aside_long(p, secs)}</div></main>'
    inner = p["body"]
    if p["faqs"]:
        inner += faq_html(p["faqs"])
    if p["sources"]:
        from content.base import sources as _sources
        inner += _sources(p["sources"])
    inner += related_html(p)
    if p["layout"] == "raw":
        return f'<main id="main">{inner}</main>'
    if p["layout"] == "one":
        return f'<main id="main"><div class="wrap layout single"><div class="main prose" style="max-width:none">{inner}</div></div></main>'
    return f'<main id="main"><div class="wrap layout"><div class="main prose">{inner}</div>{aside_html(p)}</div></main>'


# ---------------------------------------------------------------- structured data

def share_image(p):
    """A post's featured image for its social card and BlogPosting markup. Every other page uses the site card."""
    if p["kind"] == "post" and p.get("hero_image") and os.path.exists(os.path.join(IMG_DIR, p["hero_image"])):
        return f"{ORIGIN}/assets/img/{p['hero_image']}"
    return ORIGIN + "/assets/img/og.jpg"


def firm_ld():
    hours = [{"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c} for d, o, c in firm.HOURS_LD]
    d = {
        "@type": ["LegalService", "Attorney"], "@id": ORIGIN + "/#firm", "name": firm.NAME, "alternateName": "Frost Law Group",
        "slogan": firm.TAGLINE, "url": ORIGIN + "/", "telephone": firm.PHONE_E164, "image": ORIGIN + "/assets/img/og.jpg",
        "logo": ORIGIN + "/assets/img/" + firm.LOGO, "priceRange": "$$",
        "address": {"@type": "PostalAddress", "streetAddress": firm.STREET, "addressLocality": firm.CITY, "addressRegion": firm.STATE, "postalCode": firm.ZIP, "addressCountry": "US"},
        "openingHoursSpecification": hours, "sameAs": [s for s in firm.SAME_AS if s],
        "areaServed": [{"@type": t, "name": n} for t, n in firm.AREA_SERVED],
        "founder": [{"@id": abs_url(firm.ATTORNEYS[k]["slug"]) + "#person"} for k in ("tara", "jack")],
        "knowsAbout": ["Personal injury", "Car accidents", "Truck accidents", "Motorcycle accidents", "Pedestrian accidents", "Rideshare accidents", "Dog bites", "Premises liability", "Catastrophic injuries", "Wrongful death"],
        "hasMap": firm.GBP_URL, "description": firm.LLMS_SUMMARY, "email": firm.EMAIL,
    }
    if firm.GEO:
        d["geo"] = {"@type": "GeoCoordinates", "latitude": firm.GEO[0], "longitude": firm.GEO[1]}
    return d


def person_ld(key):
    a = firm.ATTORNEYS[key]
    return {"@type": "Person", "@id": abs_url(a["slug"]) + "#person", "name": a["name"], "givenName": a["first"], "familyName": "Frost",
            "jobTitle": "Attorney at Law", "url": abs_url(a["slug"]), "image": ORIGIN + "/assets/img/" + a["headshot"],
            "worksFor": {"@id": ORIGIN + "/#firm"}, "alumniOf": [{"@type": "CollegeOrUniversity", "name": s} for s in a["alumni"]],
            "knowsAbout": a["knows"], "sameAs": [s for s in a["same_as"] if s], "description": a["ld_description"],
            "email": a.get("email"), "telephone": firm.PHONE_E164,
            **({"identifier": {"@type": "PropertyValue", "propertyID": "South Carolina Bar Number", "value": a["bar_number"]},
                "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license", "name": "Admitted to the South Carolina Bar",
                                  **({"dateCreated": a["admitted_iso"]} if a.get("admitted_iso") else {}),
                                  "recognizedBy": {"@type": "Organization", "name": "Supreme Court of South Carolina"}}} if a.get("bar_number") else {})}


def page_ld(p):
    graph = []
    trail = breadcrumb_trail(p) if p["kind"] != "home" else [("home", "Home")]
    graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": l, "item": abs_url(s)} for i, (s, l) in enumerate(trail)]})
    wp = {"@type": "WebPage", "@id": abs_url(p["slug"]), "url": abs_url(p["slug"]), "name": p["title"], "description": p["description"],
          "isPartOf": {"@type": "WebSite", "@id": ORIGIN + "/#website", "url": ORIGIN + "/", "name": firm.NAME, "publisher": {"@id": ORIGIN + "/#firm"}},
          "about": {"@id": ORIGIN + "/#firm"}, "inLanguage": "es" if p.get("lang") == "es" else "en-US", "dateModified": p["modified"] or BUILD_DATE}
    graph.append(wp)
    if p["kind"] == "home" or p["slug"] in ("contact", "about"):
        graph.append(firm_ld())
        graph.append(person_ld("tara"))
        graph.append(person_ld("jack"))
    if p["kind"] in ("hub", "spoke"):
        area = ({"@type": "AdministrativeArea", "name": p["county"] + ", South Carolina"} if p.get("county")
                else [{"@type": t, "name": n} for t, n in firm.AREA_SERVED])
        graph.append({"@type": "Service", "name": re.sub(r"<[^>]+>", "", p["h1"]), "serviceType": p["nav_label"], "provider": {"@id": ORIGIN + "/#firm"},
                      "areaServed": area, "url": abs_url(p["slug"]), "description": p["description"]})
    faqs = p["faqs"] or p.get("_faq_schema") or []
    if faqs:
        graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faqs]})
    if p["kind"] == "post":
        a = firm.ATTORNEYS[p["author"]]
        graph.append({"@type": "BlogPosting", "headline": p["h1"], "description": p["description"], "url": abs_url(p["slug"]), "mainEntityOfPage": abs_url(p["slug"]),
                      "datePublished": p["date"], "dateModified": p["modified"], "author": {"@id": abs_url(a["slug"]) + "#person"},
                      "publisher": {"@id": ORIGIN + "/#firm"}, "articleSection": p["category"], "inLanguage": "en-US", "image": share_image(p),
                      **({"reviewedBy": {"@id": abs_url(firm.ATTORNEYS[p["reviewer"]]["slug"]) + "#person"}} if p.get("reviewer") else {})})
    if p["kind"] == "attorney":
        graph.append(person_ld(p["author"]))
    return {"@context": "https://schema.org", "@graph": graph}


# ---------------------------------------------------------------- documents

INLINE_JS = r"""
(function(){
  var t=document.querySelector('[data-navtoggle]'),n=document.getElementById('nav');
  if(t&&n){t.addEventListener('click',function(){var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');t.textContent=o?'Close':'Menu';});}
  document.addEventListener('click',function(e){var b=e.target.closest('[data-loadmap]');if(!b)return;var m=b.closest('.map');
    if(window.__PREVIEW__){b.replaceWith(Object.assign(document.createElement('p'),{textContent:'The interactive Google Map loads here on the live site.'}));return;}
    var f=document.createElement('iframe');f.src=m.getAttribute('data-embed');f.title='Map to Frost Law Group, 128 Linwood Lane, Summerville';f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';f.allowFullscreen=true;m.appendChild(f);});
  var f=document.querySelector('form[data-contact]');
  if(f){f.addEventListener('submit',function(e){var hp=f.querySelector('[name=_gotcha]');if(hp&&hp.value){e.preventDefault();return;}var t=f.querySelector('[name=topic]'),s=f.querySelector('[name=_subject]');if(t&&s){s.value='Injury site inquiry: '+t.value;}
    if(window.__PREVIEW__){e.preventDefault();alert('On the live site this sends your message to the firm and lands on the thank-you page.');return;}
    if(!window.fetch||!window.FormData){return;}
    e.preventDefault();var btn=f.querySelector('button[type=submit]'),msg=f.querySelector('[data-formmsg]');if(btn){btn.disabled=true;btn.textContent='Sending…';}
    fetch(f.action,{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}}).then(function(r){return r.ok?r.json().catch(function(){return {ok:true};}):Promise.reject(r);}).then(function(){window.location.href=f.getAttribute('data-thanks')||'/thank-you/';}).catch(function(){
      if(btn){btn.disabled=false;btn.textContent='Request my free case review';}if(msg){msg.hidden=false;}});});}
  /* submenus open and close on small screens */
  document.querySelectorAll('[data-subtoggle]').forEach(function(b){b.addEventListener('click',function(){var li=b.parentNode,o=li.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});});
  /* open the accordion that holds a linked heading */
  function openTo(id){if(!id)return;var el=document.getElementById(id);if(!el)return;var d=el.closest('details');while(d){d.open=true;d=d.parentElement&&d.parentElement.closest('details');}}
  openTo(decodeURIComponent(location.hash.slice(1)));
  window.addEventListener('hashchange',function(){openTo(decodeURIComponent(location.hash.slice(1)));});
  /* open or close every accordion on the page */
  document.querySelectorAll('[data-accall]').forEach(function(b){b.addEventListener('click',function(){var all=document.querySelectorAll('details.acc'),open=b.getAttribute('aria-pressed')!=='true';
    all.forEach(function(d){d.open=open;});b.setAttribute('aria-pressed',open?'true':'false');b.textContent=open?b.getAttribute('data-close'):b.getAttribute('data-open');});});
  /* the mobile table of contents closes after a pick */
  document.querySelectorAll('.toc-m a').forEach(function(a){a.addEventListener('click',function(){var d=a.closest('details');if(d)d.open=false;});});
  /* highlight the section in view, fill the reading bar, show the back-to-top button */
  var secs=[].slice.call(document.querySelectorAll('main section.sec[id]')),links={},bar=document.querySelector('.progress span'),top=document.querySelector('[data-totop]');
  document.querySelectorAll('.toc a[href^="#"]').forEach(function(a){links[a.getAttribute('href').slice(1)]=a;});
  var ticking=false;function onScroll(){ticking=false;var y=window.scrollY,h=document.documentElement.scrollHeight-window.innerHeight;
    if(bar&&secs.length){bar.style.width=(h>0?Math.min(100,y/h*100):0)+'%';}
    if(top){top.classList.toggle('show',y>900);}
    var cur=null;for(var i=0;i<secs.length;i++){if(secs[i].getBoundingClientRect().top<140)cur=secs[i].id;}
    for(var k in links){links[k].classList.toggle('active',k===cur);}}
  window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScroll);}},{passive:true});onScroll();
})();
"""


def head_html(p):
    og_type = "article" if p["kind"] == "post" else "website"
    robots = '<meta name="robots" content="noindex,follow">' if p["noindex"] else '<meta name="robots" content="index,follow,max-image-preview:large">'
    ld = json.dumps(page_ld(p), ensure_ascii=False, separators=(",", ":"))
    lang = p.get("lang") or "en"
    alt = ""
    if p.get("alternate"):
        alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{abs_url(s)}">' for l, s in p["alternate"].items())
    return (
        f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{esc(p["title"])}</title><meta name="description" content="{esc(p["description"])}">{robots}'
        f'<link rel="canonical" href="{abs_url(p["slug"])}">{alt}'
        f'<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{esc(firm.SITE_NAME)} · {esc(firm.NAME)}"><meta property="og:title" content="{esc(p["title"])}">'
        f'<meta property="og:description" content="{esc(p["description"])}"><meta property="og:url" content="{abs_url(p["slug"])}"><meta property="og:image" content="{share_image(p)}">'
        '<meta name="twitter:card" content="summary_large_image">'
        f'<meta name="geo.region" content="US-SC"><meta name="geo.placename" content="{firm.CITY}">'
        '<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">'
        '<link rel="preload" href="/assets/fonts/fraunces-var.woff2" as="font" type="font/woff2" crossorigin>'
        '<link rel="preload" href="/assets/fonts/public-sans-var.woff2" as="font" type="font/woff2" crossorigin>'
        f'<link rel="stylesheet" href="{CSS_HREF}">'
        f'<script type="application/ld+json">{ld}</script>{firm.CALLRAIL_SCRIPT}'
        '</head><body>')


def render_prod(p):
    foot = footer_html()
    if p.get("lang") == "es":
        foot = foot.replace(f'<a class="mbar-cta" href="{url("contact")}">Free case review</a>', f'<a class="mbar-cta" href="{url("contact")}">Consulta gratis</a>')
    doc = head_html(p) + header_html() + hero_html(p) + body_html(p) + foot + f"<script>{INLINE_JS}</script></body></html>"
    return expand_tokens(doc)


def write_prod():
    global CSS_HREF
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets", "img"))
    css_src = os.path.join(ASSETS, "site.css")
    css_name = f"site.{file_hash(css_src)}.css"
    CSS_HREF = f"/assets/{css_name}"
    shutil.copy(css_src, os.path.join(OUT, "assets", css_name))
    shutil.copytree(os.path.join(ASSETS, "fonts"), os.path.join(OUT, "assets", "fonts"))
    # pages
    for p in PAGES:
        html = render_prod(p)
        check_page(p, html)
        d = OUT if p["slug"] == "home" else os.path.join(OUT, p["slug"])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(html)
    # images (optimized copies) + placeholders
    if os.path.isdir(IMG_DIR):
        for name in os.listdir(IMG_DIR):
            src = os.path.join(IMG_DIR, name)
            dst = os.path.join(OUT, "assets", "img", name)
            if name.lower().endswith((".jpg", ".jpeg", ".png")):
                im = Image.open(src)
                mx = 1600
                if im.width > mx:
                    im = im.resize((mx, round(im.height * mx / im.width)), Image.LANCZOS)
                if name.lower().endswith(".png"):
                    im.save(dst, "PNG", optimize=True)
                else:
                    im.convert("RGB").save(dst, "JPEG", quality=82, optimize=True, progressive=True)
                    if im.width > VARIANT_W + 100:  # the phone-sized copy that resp_img() offers in srcset
                        sm = im.convert("RGB").resize((VARIANT_W, round(im.height * VARIANT_W / im.width)), Image.LANCZOS)
                        sm.save(os.path.join(OUT, "assets", "img", variant_name(name)), "JPEG", quality=78, optimize=True, progressive=True)
            else:
                shutil.copy(src, dst)
    for name, svg in _PLACEHOLDERS.items():
        open(os.path.join(OUT, "assets", "img", "placeholder-" + os.path.splitext(name)[0] + ".svg"), "w", encoding="utf-8").write(svg)
    write_favicons()
    write_og()
    # sitemap, robots, htaccess, llms, 404
    urls = []
    for p in PAGES:
        if p["noindex"]:
            continue
        urls.append(f"<url><loc>{abs_url(p['slug'])}</loc><lastmod>{p['modified'] or BUILD_DATE}</lastmod><changefreq>{p['changefreq']}</changefreq><priority>{p['priority']:.1f}</priority></url>")
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(urls) + "</urlset>")
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nDisallow: /assets/fonts/\n\nSitemap: {ORIGIN}/sitemap.xml\n")
    open(os.path.join(OUT, ".htaccess"), "w", encoding="utf-8").write(htaccess())
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write(llms_txt())
    write_vercel_json()
    p404 = dict(BY_SLUG["home"], slug="404", title="Page not found | Summerville Accident Attorney", description="That page has moved.", h1="We couldn't find that page", kind="page", layout="one", noindex=True,
                eyebrow="Page not found", lead="The address may have changed when we rebuilt the site. The links below will get you where you were headed.", kicker="", quote="", hero_image=None, hero_style=None, hero_image_wide=None, cta=None, faqs=[], related=[], sources=[], lang="en", alternate=None,
                body='<p>Try one of these: <a href="[[car-accident-attorneys-in-summerville]]">Car accidents</a>, <a href="[[practice-areas]]">All practice areas</a>, <a href="[[locations]]">Locations we serve</a>, <a href="[[contact]]">Free case review</a>, or call <a href="tel:' + firm.PHONE_E164 + '">' + firm.PHONE + "</a>.</p>")
    html = expand_tokens(head_html(p404).replace(f'<link rel="canonical" href="{abs_url("404")}">', "") + header_html() + hero_html(p404) + body_html(p404) + footer_html() + f"<script>{INLINE_JS}</script></body></html>")
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(html)


_REDIRECT_CACHE = []


def redirect_pairs():
    """(old path, new path) for every redirect whose target is live. Never redirects a live page."""
    if _REDIRECT_CACHE:
        return _REDIRECT_CACHE
    out = _REDIRECT_CACHE
    for old, new in firm.REDIRECTS:
        src = old.strip("/")
        if src in BY_SLUG:
            warn(f"redirect source {old} is a live page, skipped")
            continue
        dst = resolve(new.strip("/") or "home")
        if dst is None:
            warn(f"redirect {old} -> {new}: target missing, skipped")
            continue
        if dst != (new.strip("/") or "home"):
            warn(f"redirect {old} -> {new}: target not built yet, sent to /{'' if dst == 'home' else dst + '/'} for now")
        out.append(("/" + src, "/" if dst == "home" else f"/{dst}/"))
    return out


def htaccess():
    host = ORIGIN.split("//", 1)[1]
    lines = ["# Summerville Accident Attorney (Frost Law Group) — canonical host, HTTPS, trailing slashes, and the redirect map from the search audit",
             "Options -Indexes", "ErrorDocument 404 /404.html", "", "<IfModule mod_rewrite.c>", "RewriteEngine On",
             "# https + www (one address for every page; Google already chose the www host)",
             "RewriteCond %{HTTPS} off [OR]", "RewriteCond %{HTTP_HOST} !^" + host.replace(".", "\\.") + "$ [NC]",
             "RewriteRule ^ https://" + host + "%{REQUEST_URI} [R=301,L,NE]",
             "# old addresses -> new pages"]
    for old, new in redirect_pairs():
        lines.append(f"RewriteRule ^{re.escape(old.lstrip('/'))}/?$ {new} [R=301,L]")
    lines += ["# add a trailing slash to directory-style URLs", "RewriteCond %{REQUEST_FILENAME} !-f", "RewriteCond %{REQUEST_URI} !/$", "RewriteCond %{REQUEST_URI} !\\.[a-zA-Z0-9]{2,5}$",
              "RewriteRule ^(.*)$ /$1/ [R=301,L]", "</IfModule>", "",
              "<IfModule mod_headers.c>", 'Header set X-Content-Type-Options "nosniff"', 'Header set Referrer-Policy "strict-origin-when-cross-origin"',
              '<FilesMatch "\\.(woff2|css|svg|jpg|png)$">', 'Header set Cache-Control "public, max-age=31536000, immutable"', "</FilesMatch>", "</IfModule>", "",
              "<IfModule mod_deflate.c>", "AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json image/svg+xml", "</IfModule>", ""]
    return "\n".join(lines)


def write_vercel_json():
    """Vercel equivalent of the .htaccess rules: serve website/, keep trailing slashes, redirect old addresses, cache assets."""
    redirects = []
    for old, new in redirect_pairs():
        redirects.append({"source": old, "destination": new, "permanent": True})
        redirects.append({"source": old + "/", "destination": new, "permanent": True})
    host = ORIGIN.split("//", 1)[1]
    redirects.insert(0, {"source": "/:path*", "has": [{"type": "host", "value": host.replace("www.", "")}], "destination": f"{ORIGIN}/:path*", "permanent": True})
    cfg = {
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "framework": None,
        "buildCommand": None,
        "installCommand": None,
        "outputDirectory": "website",
        "trailingSlash": True,
        "redirects": redirects,
        "headers": [
            {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            {"source": "/(.*)", "headers": [{"key": "X-Content-Type-Options", "value": "nosniff"}, {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                                             {"key": "X-Frame-Options", "value": "SAMEORIGIN"}, {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"}]},
        ],
    }
    open(os.path.join(ROOT, "vercel.json"), "w", encoding="utf-8").write(json.dumps(cfg, indent=2) + "\n")


def llms_txt():
    lines = [f"# {firm.SITE_NAME} ({firm.NAME})", "", f"> {firm.LLMS_SUMMARY}", "", f"- Address: {firm.STREET}, {firm.CITY}, {firm.STATE} {firm.ZIP}", f"- Phone: {firm.PHONE}", f"- Hours: {firm.HOURS_SHORT}",
             f"- Attorneys: {firm.ATTORNEYS['tara']['name']} (personal injury; former Dorchester County Magistrate Judge and Associate Probate Judge) and {firm.ATTORNEYS['jack']['name']} (former Summerville Police Department officer and Charleston County Sheriff's Office detective)",
             "- Fees: contingency fee on injury cases; free consultation; no fee unless we win",
             f"- Main firm site (other practice areas): {firm.MAIN_SITE}/", f"- Google Business Profile: {firm.GBP_URL}", f"- Yelp: {firm.YELP_URL}", "", "## Pages", ""]
    for p in PAGES:
        if not p["noindex"] and not p.get("_legacy"):
            lines.append(f"- [{re.sub(r'<[^>]+>', '', p['h1'])}]({abs_url(p['slug'])}): {p['description']}")
    return "\n".join(lines) + "\n"


def write_favicons():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#7a1f1f"/>'
           '<text x="32" y="45" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="40" fill="#fff">F</text></svg>')
    open(os.path.join(OUT, "assets", "img", "favicon.svg"), "w", encoding="utf-8").write(svg)
    im = Image.new("RGB", (180, 180), "#7a1f1f")
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 120)
    except Exception:
        f = ImageFont.load_default()
    d.text((90, 92), "F", fill="#ffffff", font=f, anchor="mm")
    im.save(os.path.join(OUT, "assets", "img", "apple-touch-icon.png"))


def write_og():
    """1200x630 share image: the couple photo if present, otherwise a navy card with the wordmark."""
    path = os.path.join(OUT, "assets", "img", "og.jpg")
    src = os.path.join(IMG_DIR, firm.OG_SOURCE)
    W, H = 1200, 630
    if os.path.exists(src):
        im = Image.open(src).convert("RGB")
        scale = max(W / im.width, H / im.height)
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
        left, top = (im.width - W) // 2, (im.height - H) // 2
        im = im.crop((left, top, left + W, top + H))
    else:
        im = Image.new("RGB", (W, H), "#0f2a4a")
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([0, H - 170, W, H], fill=(15, 42, 74, 235))
    try:
        f1 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 54)
        f2 = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 28)
    except Exception:
        f1 = f2 = ImageFont.load_default()
    d.text((48, H - 140), "Summerville Accident Attorney", fill="#ffffff", font=f1)
    d.text((48, H - 70), f"Frost Law Group · Personal injury · {' · '.join(firm.PROMISES)} · {firm.PHONE}", fill="#cfdcea", font=f2)
    im.save(path, "JPEG", quality=85, optimize=True)


# ---------------------------------------------------------------- preview (single file)

def write_preview(out_path):
    css = open(os.path.join(ASSETS, "site.css"), encoding="utf-8").read()
    css = re.sub(r"@font-face\{[^}]*\}", "", css)
    tpl = []
    for p in PAGES:
        inner = expand_tokens(hero_html(p) + body_html(p))
        tpl.append(f'<template data-slug="{p["slug"]}" data-title="{esc(p["title"])}">{inner}</template>')
    groups = [("Core pages", [p for p in PAGES if p["kind"] in ("home", "page", "attorney")]),
              ("Car accidents", [p for p in PAGES if p["slug"] == firm.CAR or p.get("hub") == firm.CAR]),
              ("Other injury cases", [p for p in PAGES if p["kind"] in ("hub", "spoke") and p["slug"] != firm.CAR and p.get("hub") != firm.CAR]),
              ("Areas we serve", [p for p in PAGES if p["kind"] == "city"]),
              ("Blog", [p for p in PAGES if p["kind"] == "post"])]
    drawer = ""
    for label, items in groups:
        drawer += f"<h3>{label} ({len(items)})</h3><ul>" + "".join(f'<li><a href="{url(p["slug"])}">{esc(p["h1"])}</a></li>' for p in items) + "</ul>"
    header = expand_tokens(header_html())
    footer = expand_tokens(footer_html())
    js = r"""
window.__PREVIEW__=true;
(function(){
  var T={};document.querySelectorAll('template[data-slug]').forEach(function(t){T[t.dataset.slug]=t;});
  var app=document.getElementById('app'),drawer=document.getElementById('pv-drawer');
  function go(){var s=location.hash.replace(/^#\/?/,'').replace(/\/$/,'')||'home';var t=T[s]||T['home'];app.innerHTML='';app.appendChild(t.content.cloneNode(true));
    document.title=t.dataset.title;window.scrollTo(0,0);var n=document.getElementById('nav');if(n){n.classList.remove('open');}var b=document.querySelector('[data-navtoggle]');if(b){b.textContent='Menu';b.setAttribute('aria-expanded','false');}drawer.classList.remove('open');}
  window.addEventListener('hashchange',go);go();
  document.getElementById('pv-open').addEventListener('click',function(){drawer.classList.add('open');});
  document.getElementById('pv-close').addEventListener('click',function(){drawer.classList.remove('open');});
})();
"""
    doc = (f'<title>Summerville Accident Attorney Site Preview</title><style>{css}</style>'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500..700&family=Public+Sans:ital,wght@0,400..700;1,400&display=swap">'
           f'<div class="pv-note">Preview of the rebuilt summervilleaccidentattorney.com — {len(PAGES)} pages. Use the menu, footer links or the “All pages” button to move around. Maps and the contact form activate on the live site.</div>'
           f'{header}<div id="app"></div>{footer}'
           f'<div class="pv-bar"><button type="button" id="pv-open">All {len(PAGES)} pages</button></div>'
           f'<div class="pv-drawer" id="pv-drawer"><button class="close" type="button" id="pv-close">Close</button><h2>Every page in the rebuild</h2><p class="small">Grouped the way the site is wired: hubs and their spokes, one page per service area, and the blog.</p>{drawer}</div>'
           + "".join(tpl) + f"<script>{INLINE_JS}</script><script>{js}</script>")
    open(out_path, "w", encoding="utf-8").write(doc)
    return len(doc)


# ---------------------------------------------------------------- checks

# This site is personal injury only. The main site owns estate planning, probate and criminal defense, so no page here
# may name those services (or offer to defend a drunk driver) except in the one cross-link sentence defined in firm.py.
CANNIBAL_RE = re.compile(r"estate plan|probate (attorney|lawyer|law firm|practice|services)|criminal defen[cs]e|expungement|guardianship attorney|power of attorney|living will|revocable trust|last will|"
                         r"DUI (lawyer|attorney|defense)|defend(ing)? (a |the )?DUI|drug charge (lawyer|attorney|defense)|we (can )?(defend|fight) (your|the) (ticket|charge)", re.I)


def check_page(p, html):
    for msg in checks.check(p, html, PAGES):
        warn(("HARD FAIL " if msg.startswith("!") else "") + f"{p['slug'] or 'home'}: {msg.lstrip('!')}")
    if len(p["title"]) > (90 if p["kind"] == "home" else 70):
        warn(f"{p['slug']}: title {len(p['title'])} chars")
    if not (60 <= len(p["description"]) <= 160):
        warn(f"{p['slug']}: description {len(p['description'])} chars")
    if html.count("<h1") != 1:
        warn(f"{p['slug']}: {html.count('<h1')} h1 tags")
    if "[[" in html:
        warn(f"{p['slug']}: unresolved token near {html[html.find('[['):html.find('[[') + 40]!r}")
    body = html
    for ph in firm.CROSS_LINK_PHRASES:
        body = body.replace(ph, "")
    m = CANNIBAL_RE.search(body)
    if m:
        warn(f"CANNIBALIZATION on {p['slug']}: ...{body[max(0, m.start() - 60):m.end() + 60]!r}")
    words = len(re.sub(r"<[^>]+>", " ", html.split('<main', 1)[1].split("</main>", 1)[0]).split()) if "<main" in html else 0
    p["_words"] = words


def check_global():
    titles, descs = {}, {}
    for p in PAGES:
        titles.setdefault(p["title"], []).append(p["slug"])
        descs.setdefault(p["description"], []).append(p["slug"])
    for t, s in titles.items():
        if len(s) > 1:
            warn(f"duplicate title {t!r}: {s}")
    for t, s in descs.items():
        if len(s) > 1:
            warn(f"duplicate description: {s}")
    for p in PAGES:
        for s in p["related"]:
            if resolve(s) is None:
                warn(f"{p['slug']}: related target {s} missing")
        if p["hub"] and p["hub"] not in BY_SLUG:
            warn(f"{p['slug']}: hub {p['hub']} missing")


def main():
    global MODE
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", help="write a single-file preview to this path instead of website/")
    args = ap.parse_args()
    init_design()
    check_global()
    if args.preview:
        MODE = "preview"
        for p in PAGES:  # run per-page checks against a rendered document too
            check_page(p, hero_html(p) + expand_tokens(body_html(p)))
        n = write_preview(args.preview)
        print(f"preview: {args.preview} ({n/1e6:.2f} MB, {len(PAGES)} pages)")
    else:
        MODE = "prod"
        write_prod()
        total = sum(len(open(os.path.join(dp, f), encoding="utf-8").read()) for dp, _, fs in os.walk(OUT) for f in fs if f.endswith(".html"))
        print(f"website/: {len(PAGES)} pages, {total/1e6:.2f} MB of HTML")
    kinds = {}
    for p in PAGES:
        kinds[p["kind"]] = kinds.get(p["kind"], 0) + 1
    print("pages by kind:", kinds)
    short = sorted(((p.get("_words", 0), p["slug"]) for p in PAGES))[:6]
    print("shortest pages (words in main):", short)
    for w in WARNINGS:
        print("WARN:", w)
    if any("CANNIBALIZATION" in w or "HARD FAIL" in w for w in WARNINGS):
        sys.exit(1)


if __name__ == "__main__":
    main()
