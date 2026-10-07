"""Page design for the long-form pages: sections, accordions, a table of contents, images and navigation cards.

The long-form copy in content/pages/*.html is plain h1 to h6, p, a, strong and em. This module turns that copy into the
designed page at build time without changing a word of it:

* the paragraphs before the first H2 become the intro, with the phone paragraph set off as a call box, and the first
  paragraph of an answer page set off as the short answer;
* each H2 and what follows it becomes a <section> with an id, so the table of contents can link to it;
* the page's photo for that H2 (content/images.json) sits directly under the H2;
* each H3 and everything under it (H4s and H5s included) becomes a <details> accordion whose <summary> keeps the real
  H3 element, so the heading outline is unchanged for search engines and screen readers;
* the last H2 is the call to action and renders as a navy panel with buttons.

Images: content/images.json lists each page's featured image and the photo under each H2, by LLG page id. A file that
is not on disk yet is skipped with a warning, so the page still builds.
"""
import html as _html
import json
import os
import re

from content.base import BY_SLUG, PAGES, esc
from content import firm

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = json.load(open(os.path.join(HERE, "content", "images.json"), encoding="utf-8")) if os.path.exists(os.path.join(HERE, "content", "images.json")) else {}

# Set by build_site.init_design(): url(slug), resp_img(name, alt, cls, sizes, lazy), image_exists(name), warn(msg)
url = resp_img = image_exists = warn = None

H2_RE = re.compile(r"(<h2[^>]*>.*?</h2>)", re.S)
H3_RE = re.compile(r"(<h3[^>]*>.*?</h3>)", re.S)
P_RE = re.compile(r"<p[^>]*>.*?</p>", re.S)

PHONE_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>')
CHAT_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H8l-4 4V5a1 1 0 0 1 1-1z"/></svg>')
CHECK_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.2 4.2L19 7"/></svg>'

LABELS = {
    "en": dict(tell="Tell us what happened", toc="On this page", open_all="Open all sections", close_all="Close all sections", short="The short answer", call="Call", review="Get a free case review",
               more="More help from Frost Law Group", questions="Questions people ask", read="Read more"),
    "es": dict(tell="Cuéntenos qué pasó", toc="En esta página", open_all="Abrir todas las secciones", close_all="Cerrar todas las secciones", short="La respuesta corta", call="Llame", review="Consulta gratis",
               more="Más ayuda de Frost Law Group", questions="Preguntas frecuentes", read="Leer más"),
}


def lab(p, key):
    return LABELS.get(p.get("lang") or "en", LABELS["en"])[key]


def text_of(fragment):
    return _html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def slugify(text, used):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:64].strip("-") or "section"
    base, n = s, 2
    while s in used:
        s, n = f"{base}-{n}", n + 1
    used.add(s)
    return s


def page_images(p):
    """The image record for an LLG page: {"featured": {...}, "h2": {"1": {...}, ...}} with only files that exist."""
    rec = IMAGES.get(p.get("_llg") or "", {})
    out = {"featured": None, "h2": {}}
    f = rec.get("featured")
    if f and image_exists(f["file"]):
        out["featured"] = f
    elif f:
        warn(f"{p['slug']}: featured image {f['file']} not on disk yet")
    for k, v in (rec.get("h2") or {}).items():
        if image_exists(v["file"]):
            out["h2"][int(k)] = v
        else:
            warn(f"{p['slug']}: image {v['file']} not on disk yet")
    return out


def featured(p):
    """(file, alt) of a page's featured image, or None."""
    rec = IMAGES.get(p.get("_llg") or "", {}).get("featured")
    if rec and image_exists(rec["file"]):
        return rec["file"], rec["alt"]
    return None


# ---------------------------------------------------------------- the body


def _figure(img, sizes="(max-width: 920px) 100vw, 760px"):
    return f'<figure class="sec-fig">{resp_img(img["file"], img["alt"], sizes=sizes)}</figure>'


def _accordions(chunk, used):
    """chunk starts at the first H3 of a section. Each H3 and the content up to the next H3 becomes one <details>."""
    parts = H3_RE.split(chunk)
    out = []
    lead = parts[0].strip()
    for i in range(1, len(parts), 2):
        h3 = parts[i]
        inner = parts[i + 1] if i + 1 < len(parts) else ""
        title = text_of(h3)
        hid = slugify(title, used)
        h3_tag = re.sub(r"^<h3[^>]*>", f'<h3 id="{hid}">', h3)
        q = " q" if title.endswith("?") else ""
        out.append(f'<details class="acc{q}"><summary>{h3_tag}<span class="chev" aria-hidden="true"></span></summary><div class="acc-body">{inner.strip()}</div></details>')
    return lead + '<div class="acc-group">' + "".join(out) + "</div>"


def _intro(p, intro):
    paras = P_RE.findall(intro)
    if not paras or p["kind"] == "post":
        return f'<div class="intro">{intro}</div>'
    out = []
    is_answer = p.get("_type") == "Answer page"
    for i, para in enumerate(paras):
        inner = re.sub(r"^<p[^>]*>|</p>$", "", para)
        if i == 0 and is_answer:
            out.append(f'<div class="answer"><div class="eyebrow">{lab(p, "short")}</div><p>{inner}</p></div>')
        elif i == 0:
            out.append(f'<p class="lead-p">{inner}</p>')
        elif i == len(paras) - 1 and "tel:" in para:
            out.append(f'<div class="intro-cta"><span class="ic">{PHONE_SVG}</span><p>{inner}</p></div>')
        else:
            out.append(para)
    return '<div class="intro">' + "".join(out) + "</div>"


def toc_items(p, sections):
    return "".join(f'<li><a href="#{sid}">{esc(title)}</a></li>' for sid, title in sections)


def toc_mobile(p, sections, always=False):
    if len(sections) < 3:
        return ""
    cls = "toc-m always" if always else "toc-m"
    return (f'<details class="{cls}"><summary><span>{lab(p, "toc")}</span><span class="chev" aria-hidden="true"></span></summary>'
            f'<ol>{toc_items(p, sections)}</ol></details>')


def cta_actions(p):
    return (f'<div class="actions"><a class="btn light" href="{url("contact")}">{lab(p, "review")}</a>'
            f'<a class="btn ghost on-dark" href="tel:{firm.PHONE_E164}">{PHONE_SVG}{firm.PHONE}</a></div>')


def _shell(cls, sid, inner):
    return f'<section class="{cls}" id="{sid}">{inner}</section>'


def enhance(p, body, inserts=None, shell=_shell, intro_shell=None):
    """Turn plain long-form copy into designed sections. Returns (html, [(section id, H2 text), ...]).

    inserts: {h2 index: html} placed after that section's intro paragraphs (cards, attorney panels),
    {"intro": html} after the intro, and {"after:N": html} after section N closes.
    shell(cls, id, inner) wraps each section; the home page uses it for full-width bands."""
    inserts = inserts or {}
    imgs = page_images(p)
    used = set()
    parts = H2_RE.split(body)
    intro = _intro(p, parts[0]) if parts[0].strip() else ""
    sections, html_secs = [], []
    n_h2 = (len(parts) - 1) // 2
    for k in range(n_h2):
        h2 = parts[1 + 2 * k]
        rest = parts[2 + 2 * k]
        title = text_of(h2)
        sid = slugify(title, used)
        sections.append((sid, title))
        idx = k + 1
        last = idx == n_h2 and p["kind"] != "post"
        fig = _figure(imgs["h2"][idx], sizes="(max-width: 760px) 100vw, 440px" if last else "(max-width: 920px) 100vw, 760px") if idx in imgs["h2"] else ""
        cut = rest.find("<h3")
        head, tail = (rest, "") if cut == -1 else (rest[:cut], rest[cut:])
        extra = inserts.get(idx, "")
        if last:
            inner = (f'<div class="cta-text">{h2}<div class="sec-intro">{head.strip()}</div>{cta_actions(p)}</div>{fig}'
                     + (_accordions(tail, used) if tail else ""))
            html_secs.append(shell(f'sec sec-cta{" has-fig" if fig else ""}', sid, inner))
        elif p["kind"] == "post":  # articles read top to bottom, so their H3s stay open
            html_secs.append(shell("sec", sid, f'{h2}{fig}<div class="sec-intro">{rest.strip()}</div>'))
        else:
            acc = _accordions(tail, used) if tail else ""
            html_secs.append(shell("sec", sid, f'{h2}{fig}<div class="sec-intro">{head.strip()}</div>{extra}{acc}'))
        html_secs.append(inserts.get(f"after:{idx}", ""))
    toc = toc_mobile(p, sections, always=p["layout"] != "two") if p.get("_toc", True) else ""
    head_html = intro + inserts.get("intro", "") + toc
    if intro_shell:
        head_html = intro_shell(head_html)
    return head_html + "".join(html_secs), sections


# ---------------------------------------------------------------- cards and panels


def card_img(slug):
    pg = BY_SLUG.get(slug)
    f = featured(pg) if pg else None
    if not f:
        return '<span class="ph" aria-hidden="true"></span>'
    return resp_img(f[0], "", sizes="(max-width: 600px) 100vw, 300px", cls="thumb")


def photo_cards(slugs, cls="pcards"):
    lis = []
    for s in slugs:
        pg = BY_SLUG.get(s)
        if not pg:
            continue
        lis.append(f'<li><a href="{url(s)}">{card_img(s)}<span class="t">{esc(pg["nav_label"])}</span></a></li>')
    return f'<ul class="{cls}">' + "".join(lis) + "</ul>" if lis else ""


def link_list(slugs):
    lis = "".join(f'<li><a href="{url(s)}">{esc(BY_SLUG[s]["h1"])}</a></li>' for s in slugs if s in BY_SLUG)
    return f'<ul class="qlist">{lis}</ul>' if lis else ""


def attorney_panel(keys=("tara", "jack"), compact=False):
    out = []
    for k in keys:
        a = firm.ATTORNEYS[k]
        out.append(f'<a class="atty" href="{url(a["slug"])}">{resp_img(a["headshot"], a["name"], sizes="96px", cls="hs")}'
                   f'<span><b>{esc(a["name"])}</b><small>{esc(a["byline"])}</small>' + ("" if compact else f'<span class="bio">{a["aside"]}</span>') + "</span></a>")
    return '<div class="attys">' + "".join(out) + "</div>"


def explore(p):
    """Navigation cards after the page copy: a hub's children, or a child's parent and siblings."""
    kind = p["kind"]
    hub = p["slug"] if kind == "hub" else (p.get("hub") if kind in ("spoke", "city") else None)
    if not hub or hub not in BY_SLUG:
        return ""
    kids = [s for s in firm.HUB_SPOKES.get(hub, []) if s in BY_SLUG]
    answers = [s for s in kids if BY_SLUG[s].get("_type") == "Answer page"]
    pages = [s for s in kids if s not in answers]
    hp = BY_SLUG[hub]
    out = []
    if kind == "hub":
        if pages:
            out.append(f'<p class="ex-title">{esc(hp["section_label"] or hp["nav_label"])}</p>{photo_cards(pages)}')
        if answers:
            out.append(f'<p class="ex-title">{lab(p, "questions")}</p>{link_list(answers)}')
    else:
        sib = [s for s in pages if s != p["slug"]][:5]
        out.append(f'<p class="ex-title">{esc(hp["section_label"] or hp["nav_label"])}</p>{photo_cards([hub] + sib)}')
        if p.get("_type") == "Answer page":
            others = [s for s in answers if s != p["slug"]][:8]
            if others:
                out.append(f'<p class="ex-title">{lab(p, "questions")}</p>{link_list(others)}')
    if not out:
        return ""
    return f'<nav class="explore" aria-label="{esc(hp["nav_label"])}">' + "".join(out) + "</nav>"


# ---------------------------------------------------------------- aside


def aside_long(p, sections):
    promises = "" if p.get("lang") == "es" else "".join(f"<li>{CHECK_SVG}{esc(x)}</li>" for x in firm.PROMISES)
    cta = (f'<div class="acard navy cta-card"><p class="k">{lab(p, "review")}</p><a class="big" href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'
           f'<a class="btn light sm" href="{url("contact")}">{CHAT_SVG}{lab(p, "tell")}</a>'
           + (f'<ul class="mini-promises">{promises}</ul>' if promises else "") + '</div>')
    toc = ""
    if len(sections) >= 3:
        toc = (f'<nav class="acard toc" aria-label="{lab(p, "toc")}"><p class="k">{lab(p, "toc")}</p><ol>{toc_items(p, sections)}</ol>'
               + ("" if p["kind"] == "post" else f'<button class="accall" type="button" data-accall data-open="{lab(p, "open_all")}" data-close="{lab(p, "close_all")}">{lab(p, "open_all")}</button>')
               + '</nav>')
    return f'<aside class="aside long"><div class="aside-stick">{cta}{toc}</div></aside>'
