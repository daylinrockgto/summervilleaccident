"""Hard compliance checks run on every rendered page (South Carolina advertising rules and settled client decisions).

check() returns messages. A message that starts with "!" fails the build. The rest are warnings.
Settled rules behind these checks: Page Manifest v7 and the project instructions (phone format for CallRail DNI,
no CallRail number in content, no retirement year for Jack, no workers' compensation content except the unlinked
legacy page, no Georgia, SC Rule 7.4(b) words, never "Judge Frost").
"""
import html as _html
import re

PHONE_OK = "(843) 419-6653"


def _main(html):
    m = re.search(r"<main[^>]*>(.*)</main>", html, re.S)
    return m.group(1) if m else ""


def _text(fragment):
    fragment = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", fragment, flags=re.S)
    return _html.unescape(re.sub(r"<[^>]+>", " ", fragment))


def check(p, html, pages):
    out = []
    legacy = p.get("_legacy")
    text = _text(html)
    main = _text(_main(html))
    if "983-2304" in html or "9832304" in html:
        out.append("!CallRail tracking number in the page")
    for m in re.finditer(r"href=\"tel:([^\"]+)\"", html):
        if m.group(1) != "+18434196653":
            out.append(f"!tel link {m.group(1)} is not +18434196653")
    for m in re.finditer(r"\(?843\)?[ .-]?\d{3}[ .-]\d{4}", text):
        if m.group(0) != PHONE_OK and "419" in m.group(0):
            out.append(f"!phone shown as {m.group(0)!r}, DNI needs {PHONE_OK}")
    if not legacy:
        if re.search(r"worker'?s'? ?comp", text, re.I) or "workers-compensation" in re.sub(r'<link rel="canonical"[^>]*>', "", html):
            out.append("!workers' compensation named or linked (settled 2026-09-28: no content, no links)")
        if re.search(r"\bgeorgia\b|\bsavannah\b", main, re.I):
            out.append("!Georgia or Savannah named")
    if re.search(r"retire\w*[^.]{0,40}\b(2013|2015)\b|\b(2013|2015)\b[^.]{0,40}retire", text, re.I):
        out.append("!retirement year for Jack Frost")
    if re.search(r"judge frost", text, re.I):
        out.append('!"Judge Frost"')
    if re.search(r"\belli(ana)?\b", text, re.I):
        out.append("!Elli named")
    for m in re.finditer(r"\b(specialist\w*|speciali[sz]\w*|expert\w*|certif\w*)\b", main, re.I):
        if not legacy:
            out.append(f"!SC Rule 7.4(b) word {m.group(0)!r}")
    if p.get("_llg") or not p.get("noindex"):
        if len(p["title"]) > 60 and not legacy:
            out.append(f"title {len(p['title'])} characters")
        if not (150 <= len(p["description"]) <= 160) and not legacy:
            out.append(f"description {len(p['description'])} characters")
    return out
