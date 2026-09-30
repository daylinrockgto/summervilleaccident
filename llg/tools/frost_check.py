#!/usr/bin/env python3
"""frost_check.py  --  the single gate for a Frost Law Group page.

Usage:  python3 llg/tools/frost_check.py <page_id> [--grammar] [--quiet]

Reads   llg/pages/<id>.html   (clean HTML, the page copy only)
        llg/pages/<id>.json   (sidecar, images and report)
        llg/plan/plan.json
Runs    structure, link, keyphrase, compliance, style, cross-page overlap checks,
        the patched LLG qa-scan.py on a scan .docx, and (with --grammar) grammar-scan.py.
Exit 0 only when there is no FAIL. WARN lines need a human look but do not block.
"""
import sys, os, re, json, html, subprocess, itertools
from collections import Counter

ROOT = os.environ.get("FROST_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = json.load(open(f"{ROOT}/plan/plan.json"))
PAGES = {p["id"]: p for p in PLAN["pages"]}
OUTS = {v[0]: k for k, v in PLAN["outbound"].items() if k != "census_quickfacts_counties"}
DOMAIN = "summervilleaccidentattorney.com"
BASE = "https://www.summervilleaccidentattorney.com"
ALLOWED_INTERNAL = {p["url"] for p in PLAN["pages"]} | {BASE + "/contact", BASE + "/about", BASE + "/practice-areas", BASE + "/"}
TEL = "tel:+18434196653"
PHONE = "(843) 419-6653"

fails, warns, passes = [], [], []
def FAIL(msg): fails.append(msg)
def WARN(msg): warns.append(msg)
def OK(msg): passes.append(msg)

def text_of(inner):
    return html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()

def blocks_of(src):
    out = []
    for m in re.finditer(r"<(h[1-6]|p)>(.*?)</\1>", src, re.S):
        tag, inner = m.group(1), m.group(2)
        links = re.findall(r'<a href="([^"]+)">(.*?)</a>', inner, re.S)
        out.append({"tag": tag, "lvl": int(tag[1]) if tag[0] == "h" else 0, "inner": inner,
                    "text": text_of(inner), "links": [(u, text_of(a)) for u, a in links]})
    return out

def sentences(t):
    t = re.sub(r"\b(S\.C|U\.S|No|St|Mt|Dr|Mr|Mrs|Ms|Jr|Sr|v|Ann|Ct|App|seq|e\.g|i\.e)\.", lambda m: m.group(0).replace(".", "§"), t)
    t = re.sub(r"\b(Tara L|Jack C|Berlin G|Ralph H|Robert L|James E)\.", lambda m: m.group(1) + "§", t)   # known middle initials
    return [s.replace("§", ".") for s in re.split(r"(?<=[.?!])[\"”’)]?\s+(?=[A-Z0-9\"“(])", t) if s.strip()]

def words(t): return re.findall(r"[A-Za-z0-9$%][A-Za-z0-9$%'’.,\-/]*", t)

def main():
    args = sys.argv[1:]
    if not args: print(__doc__); sys.exit(2)
    pid = args[0]; grammar = "--grammar" in args; quiet = "--quiet" in args
    p = PAGES[pid]
    ANS = p.get("type") == "Answer page"
    path = f"{ROOT}/pages/{pid}.html"
    src = open(path, encoding="utf8").read()
    kp = p["kp"]; kpl = kp.lower()

    # ---------------- 0. clean HTML
    tags = set(re.findall(r"</?([a-zA-Z0-9]+)", src))
    badtags = tags - {"h1", "h2", "h3", "h4", "h5", "h6", "p", "a", "strong", "em"}
    if badtags: FAIL(f"Disallowed tags {sorted(badtags)}. Only h1-h6, p, a, strong, em. No lists.")
    attr = re.findall(r"<(h[1-6]|p|strong|em)\s+[^>]*>", src)
    if attr: FAIL(f"Attributes on {attr[:3]}, tags must be bare")
    badattr = [a for a in re.findall(r"<a\s+([^>]*)>", src) if not re.fullmatch(r'href="[^"]+"', a.strip())]
    if badattr: FAIL(f"Anchor tags must carry only href, found {badattr[:2]}")
    B = blocks_of(src)
    if not B or B[0]["tag"] != "h1": FAIL("First block must be the H1")
    heads = [b for b in B if b["lvl"]]
    paras = [b for b in B if not b["lvl"]]
    alltext = " ".join(b["text"] for b in paras)
    wc = len(alltext.split())
    lo, hi = p["words"]
    (OK if lo <= wc <= hi else FAIL)(f"Word count {wc} (band {lo} to {hi}, target {p['target']})")

    # ---------------- 1. headings
    h1s = [b for b in heads if b["lvl"] == 1]
    if len(h1s) != 1: FAIL(f"{len(h1s)} H1s")
    elif h1s[0]["text"] != p["h1"]: FAIL(f"H1 must be exactly '{p['h1']}', found '{h1s[0]['text']}'")
    h2s = [b["text"] for b in heads if b["lvl"] == 2]
    if h2s != p["h2"]:
        missing = [h for h in p["h2"] if h not in h2s]; extra = [h for h in h2s if h not in p["h2"]]
        FAIL(f"H2s must match the plan exactly and in order. Missing {missing[:3]} Extra {extra[:3]}")
    for i in range(1, len(heads)):
        if heads[i]["lvl"] - heads[i-1]["lvl"] > 1: FAIL(f"Skipped level before '{heads[i]['text'][:50]}'")
    for i, b in enumerate(B[:-1]):
        if b["lvl"] and B[i+1]["lvl"] and B[i+1]["lvl"] > b["lvl"]: FAIL(f"Stacked heading after '{b['text'][:50]}'")
    for b in heads:
        t = b["text"]
        if re.search(r"[:;—–|]", t): FAIL(f"Banned punctuation in heading '{t}'")
        if b["lvl"] >= 2:
            # APA title case: minor words of 3 letters or fewer lowercase except first word
            ws = t.split()
            minor = {"a","an","the","and","as","but","for","if","nor","or","so","yet","at","by","in","of","off","on","per","to","up","via"}
            for j, w in enumerate(ws):
                core = re.sub(r"[^A-Za-z'’\-]", "", w)
                if not core: continue
                if j > 0 and core.lower() in minor and core != core.lower() and not ws[j-1].endswith((",", "?")):
                    WARN(f"Title case, minor word '{core}' capitalized in '{t[:60]}'")
                if (core.lower() not in minor or j == 0) and core[0].islower() and core.lower() not in ("v",):
                    FAIL(f"Title case, '{core}' should be capitalized in '{t[:60]}'")
    if pid == "home":
        LOCK = [(3,"Motor Vehicle Accident Injuries"),(4,"Summerville Car Accident Attorneys"),
                (4,"Commercial Truck Accident Lawyers in Summerville, South Carolina"),(4,"Motorcycle Accident Injury Lawyers"),
                (4,"Ride Share Accident Attorneys"),(5,"Summerville Uber Accident Lawyers"),
                (5,"Lyft Accident Injury Attorneys in Summerville, South Carolina"),(3,"Slip and Fall Lawyers"),
                (3,"Dog Bite Attorneys in Summerville, South Carolina"),(3,"Wrongful Death Accident Injury Attorneys in Summerville, South Carolina")]
        have = [(b["lvl"], b["text"]) for b in heads]
        for item in LOCK:
            if item not in have: FAIL(f"Homepage approved heading missing or at the wrong level {item}")
    lv = Counter(b["lvl"] for b in heads)
    need_h5 = pid not in ("pa",) and not ANS
    if ANS:
        if lv[3] < 2: FAIL(f"Answer page needs at least 2 H3s, has {lv[3]}")
    elif lv[4] < 3 and pid != "pa": FAIL(f"Needs at least 3 H4s, has {lv[4]}")
    if pid == "pa" and lv[4] < 2: FAIL("Practice Areas page needs its H4s")
    if need_h5 and lv[5] < 1: FAIL("Needs at least 1 H5")
    # lone children
    for i, b in enumerate(heads):
        kids = []
        for m in heads[i+1:]:
            if m["lvl"] <= b["lvl"]: break
            if m["lvl"] == b["lvl"] + 1: kids.append(m)
        if len(kids) == 1: FAIL(f"Lone child under H{b['lvl']} '{b['text'][:45]}'")
    # H2 attorney term
    for t in (h2s[-1:] if ANS else h2s):
        if pid == "home" and t.startswith("Why Turn to Frost Law"): continue
        if not re.search(r"\b(lawyer|lawyers|attorney|attorneys)\b", t, re.I): FAIL(f"H2 without lawyer or attorney term '{t}'")
    # section floors (qa-scan repeats this with its own sentence splitter)
    for i, b in enumerate(B):
        if not b["lvl"] or b["lvl"] == 1: continue
        after = []
        for m in B[i+1:]:
            if m["lvl"]: break
            after.append(m["text"])
        w = sum(len(x.split()) for x in after); s = sum(len(sentences(x)) for x in after)
        need = {2: (90, 2, 1), 3: (60, 1, 3), 4: (45, 1, 3), 5: (40, 1, 3), 6: (40, 1, 3)}[b["lvl"]]
        if w < need[0] or len(after) < need[1] or s < need[2]:
            FAIL(f"Thin H{b['lvl']} '{b['text'][:45]}' {w}w/{len(after)}p/{s}s needs {need[0]}w/{need[1]}p/{need[2]}s")
    # 300-word runs without a heading
    run = 0
    for b in B:
        if b["lvl"]: run = 0
        else:
            run += len(b["text"].split())
            if run > 330: WARN(f"More than 300 words without a subheading near '{b['text'][:50]}'"); run = -10**6

    # ---------------- 2. H1 section and CTA
    fh2 = next((i for i, b in enumerate(B) if b["lvl"] == 2), None)
    intro = [b for b in B[1:fh2] if not b["lvl"]] if fh2 else []
    if len(intro) != 4: FAIL(f"H1 section must be exactly 4 paragraphs, has {len(intro)}")
    if intro:
        if not any(u == TEL for u, _ in intro[-1]["links"]): FAIL("H1 section last paragraph needs the tel link on (843) 419-6653")
        if len(sentences(intro[-1]["text"])) > 3: WARN("H1 phone CTA paragraph should be two sentences")
        first100 = " ".join(" ".join(b["text"] for b in intro).split()[:100]).lower()
        if ANS:
            n1 = len(intro[0]["text"].split())
            if not 35 <= n1 <= 70: FAIL(f"Answer page first paragraph must answer the question directly in 40 to 60 words, has {n1}")
        (OK if kpl in first100 else FAIL)("Exact keyphrase in the first 100 words")
        for j, b in enumerate(intro):
            for u, a in b["links"]:
                if u == TEL: continue
                if DOMAIN in u: FAIL(f"Internal link in the H1 section ({u}), not allowed")
                elif j > 1: FAIL("An outbound link in the H1 section must sit in paragraph 1 or 2")
                elif kpl in a.lower(): FAIL("H1 section outbound link anchored on the keyphrase")
        outs_intro = [u for b in intro for u, _ in b["links"] if u.startswith("http") and DOMAIN not in u]
        if len(outs_intro) > 1: FAIL("More than one outbound link in the H1 section")
    lastH2 = max((i for i, b in enumerate(B) if b["lvl"] == 2), default=None)
    cta = B[lastH2:] if lastH2 is not None else []
    cta_p = [b for b in cta[1:] if not b["lvl"]]
    if any(b["lvl"] for b in cta[1:]): FAIL("Final CTA section has a subheading")
    if not 3 <= len(cta_p) <= 5: FAIL(f"Final CTA needs 3 to 5 paragraphs, has {len(cta_p)}")
    ctat = " ".join(b["text"] for b in cta_p)
    if "Frost Law Group" not in ctat: FAIL("CTA must name Frost Law Group")
    if not any(u == TEL for b in cta_p for u, _ in b["links"]): FAIL("CTA needs the tel link")
    if not ANS and kpl not in (ctat + " " + (cta[0]["text"] if cta else "")).lower(): FAIL("Exact keyphrase missing from the CTA section")
    offers = len(re.findall(r"free(,)? (and )?(confidential )?(consultation|case review|review)|consultation (is|costs) (free|nothing)|no[- ]cost consultation", ctat, re.I))
    if offers != 1: FAIL(f"The free consultation offer must appear exactly once in the CTA, found {offers}")
    if "128 Linwood Lane" not in ctat: FAIL("CTA must carry the office address 128 Linwood Lane, Summerville, SC 29483 (SC Rule 7.2(d),(h))")
    clinks = [(u, a) for b in cta_p for u, a in b["links"] if u.rstrip("/").endswith("/contact")]
    if not clinks: FAIL("CTA needs the contact link")
    else:
        u, a = clinks[0]
        if re.fullmatch(r"(the )?contact( us)?( page)?|here|click here|this page|learn more|read more", a.strip().lower()): FAIL(f"Weak contact anchor '{a}'")
        if not any(u2.rstrip("/").endswith("/contact") for u2, _ in cta_p[-1]["links"]): WARN("Contact link is not in the last CTA paragraph")

    # ---------------- 3. links
    links = [(u, a, i) for i, b in enumerate(B) for u, a in b["links"]]
    internal = [(u, a) for u, a, _ in links if DOMAIN in u]
    outbound = [(u, a) for u, a, _ in links if u.startswith("http") and DOMAIN not in u]
    tels = [(u, a) for u, a, _ in links if u.startswith("tel:")]
    for u, a in internal:
        if u not in ALLOWED_INTERNAL: FAIL(f"Internal link not in the page register {u}")
        if not u.startswith(BASE): FAIL(f"Internal link must use {BASE} {u}")
        if re.fullmatch(r"(here|click here|this page|read more|learn more|more|link)", a.strip().lower()): FAIL(f"Weak anchor '{a}'")
        if re.search(r"\bpage\b", a, re.I): FAIL(f"Anchor calls a page a page '{a}'")
    cnt = Counter(u for u, _ in internal)
    dup = [u for u, c in cnt.items() if c > 1]
    if dup: FAIL(f"Same internal page linked twice {dup}")
    if p["url"] in cnt: FAIL("Page links to itself")
    req = [u for u in p["links"] if u not in cnt]
    if req: FAIL(f"Required internal links missing {req}")
    if len(internal) < 4: FAIL(f"Only {len(internal)} internal links")
    for u, a in outbound:
        if u not in OUTS: FAIL(f"Outbound link not on the verified list {u}")
    if len(outbound) > 2: FAIL(f"{len(outbound)} outbound links, cap is 2")
    if len(outbound) == 0: WARN("No outbound link, 1 or 2 from the plan is expected")
    if len(internal) <= len(outbound): FAIL("Internal must outnumber outbound")
    ocnt = Counter(u for u, _ in outbound)
    if any(c > 1 for c in ocnt.values()): FAIL("Same outbound link twice")
    for u, a in tels:
        if u != TEL: FAIL(f"tel link must be {TEL}, found {u}")
        if a != PHONE: FAIL(f"tel anchor must read {PHONE}, found '{a}'")
    # every phone mention linked
    raw_phones = re.findall(r"\(843\)\s?419-6653", alltext)
    if len(raw_phones) != len(tels): FAIL(f"{len(raw_phones)} phone mentions but {len(tels)} tel links, every mention must be linked")
    if re.search(r"983[-. ]?2304", src): FAIL("CallRail tracking number in content")
    if re.search(r"843[-.]419[-.]6653|\+1 ?843|843 419 6653", alltext): FAIL("Phone in a non-locked format")
    other_ph = [m for m in re.findall(r"\(?\b\d{3}\)?[\s.-]\d{3}[-.]\d{4}\b", alltext) if "419-6653" not in m]
    if other_ph: FAIL(f"Other phone numbers in copy {other_ph[:3]}")
    # first internal link
    if fh2 is not None:
        fp = next((b for b in B[fh2+1:] if not b["lvl"]), None)
        fl = [(u, a) for u, a in (fp["links"] if fp else []) if DOMAIN in u]
        want = p["first_link"][0]
        if not fl: FAIL("First internal link must sit in the first paragraph under the first H2")
        elif fl[0][0] != want: FAIL(f"First internal link should point to {want}, found {fl[0][0]}")
        elif pid != "home" and "Frost Law Group" not in fl[0][1]: FAIL(f"First internal link anchor should be 'Frost Law Group', found '{fl[0][1]}'")
    # links under county H2s etc: at least each required link exists, done

    # ---------------- 4. keyphrase
    kph = [b["text"] for b in heads if kpl in b["text"].lower()]
    if len(kph) > 4: FAIL(f"Exact keyphrase in {len(kph)} headings, max 4 including the H1")
    if pid != "pa" and not ANS and not any(kpl in t.lower() for t in h2s[:-1]): FAIL("Exact keyphrase not in any body H2")
    n = alltext.lower().count(kpl)
    dens = n * len(kp.split()) / max(wc, 1) * 100
    (OK if dens < 2.5 else FAIL)(f"Keyphrase density {dens:.2f}% ({n} uses)")
    if n < max(3, wc // 900): WARN(f"Keyphrase used only {n} times in {wc} words, consider one or two more natural uses")

    # ---------------- 5. firm name per H2 section, attorney name, address
    secs = []
    for i, b in enumerate(B):
        if b["lvl"] == 2:
            j = next((k for k in range(i+1, len(B)) if B[k]["lvl"] == 2), len(B))
            secs.append((b["text"], " ".join(x["text"] for x in B[i+1:j])))
    for t, body in secs:
        if "Frost Law Group" not in body: FAIL(f"H2 section does not name Frost Law Group '{t[:50]}'")
    if not re.search(r"\b(Tara L\. Frost|Jack C\. Frost|Tara Frost|Jack Frost)\b", alltext): FAIL("Name at least one attorney on the page (SC Rule 7.2(d))")

    # ---------------- 6. compliance and banned content
    low = alltext.lower()
    def ban(pattern, why, flags=re.I, where=None, level="FAIL"):
        hits = re.findall(pattern, where if where is not None else alltext + " " + " ".join(b["text"] for b in heads), flags)
        if hits:
            (FAIL if level == "FAIL" else WARN)(f"{why} {sorted(set(h if isinstance(h, str) else h[0] for h in hits))[:5]}")
    ban(r"\b(specialist|specialists|specializ\w*|specialt\w*|expert\w*|certif\w*|authorit\w*)\b", "SC Rule 7.4(b) banned word (includes 'certified mail', name the delivery method another way)")
    ban(r"\b(first|initial)\s+(consultation|meeting|visit|call|conversation)s?\b[^.]{0,40}\b(free|no cost|no charge)|\b(free|no-cost)\s+(first|initial)\s+(consultation|meeting|visit)", "'First' consultation implies later ones cost money (Rule 7.2(f)), say 'the consultation is free'")
    ban(r"only (county|one)[^.]{0,80}losing population|losing population[^.]{0,40}only", "Williamsburg is not the only county losing population, say it had the steepest decline since 2020")
    for b in paras:
        tx = b["text"]
        if re.search(r"summerville high", tx, re.I):
            for s_ in sentences(tx):
                if re.search(r"summerville high", s_, re.I) and re.search(r"\b(both|each|two attorneys|graduates|share a)\b", s_, re.I) and not re.search(r"sweetheart", s_, re.I):
                    FAIL(f"Approved facts do not say Tara graduated from Summerville High School '{s_[:80]}'")
        if re.search(r"probate judge|probate bench", tx, re.I) and re.search(r"\b(petition\w*|filing\w*|files|approv\w*|settlement\w*|appoint\w*|letters of administration|estate)\b", tx, re.I):
            FAIL(f"Tara's probate judgeship sits beside probate filings or approvals, move or cut it '{tx[:80]}'")
        if re.search(r"\bAct (No\. )?42\b", tx) and re.search(r"(under|less than|below) (50%|half)", tx, re.I) and not re.search(r"2005|existed|already|both versions|before the act|long limited|older version|old version|prior version", tx, re.I):
            FAIL(f"Act 42 paragraph states the under-50% rule as new, it dates to 2005 '{tx[:80]}'")
    ban(r"\b(best|top|leading|premier|finest|greatest|foremost)\W+(\w+\W+){0,2}(lawyers?|attorneys?|firms?|legal|injury firm|representation|advocates?|team)\b|\bnumber one\b|#1|most trusted|award[- ]winning|\belite\b|\baggressive\b|\bfierce\b|\brelentless\b|pit bull|heavy hitter|powerhouse|unmatched|unparalleled|second to none", "Superlative or big-firm language")
    ban(r"\b(best|top-rated|top rated|highest rated)\b", "Check 'best' or 'top' is not a claim about the firm", level="WARN")
    ban(r"\bfight(s|ing)? for\b|\bfighters?\b|\bbattle\b", "Fighting language")
    ban(r"\bguarante\w*", "Guarantee language (only 'no lawyer can guarantee' style disclaimers allowed, rewrite)", level="WARN")
    ban(r"no (legal |attorney'?s? )?fees?\b|unless we win|until we win|(you|clients?) (will )?(pay|owe) (us )?nothing|(pay|owe) (us )?nothing (unless|until|if)|only (get )?paid (if|when)|contingen\w*|percentage of (the|your|any) recovery|\bno win\b", "Fee language, on hold under SC Rule 7.2(f)")
    ban(r"judge frost|sitting judge|current judge|serves as a judge|is a (former )?judge who", "Judicial title misuse")
    ban(r"\belli\b|\belliana\b", "Elli has died, never mention")
    ban(r"retire\w*[^.]{0,40}\b(2013|2015)\b|\b(2013|2015)\b[^.]{0,40}retire", "Retirement year for Jack Frost")
    ban(r"\bgeorgia\b|\bsavannah\b", "Georgia or Savannah reference")
    ban(r"workers'? ?comp\w*", "Workers compensation reference")
    ban(r"tiger woods|vijay|caddie|caddied|swat operator|\bdea\b|type 1", "Bio items excluded from injury pages")
    ban(r"scripture|\bprayer\b|\bpray\b|god's|\bblessing|faith[- ]based|faith[- ]grounded|(?<!good )(?<!bad )\bfaith\b", "Faith language not called for in this build")
    ban(r"city of summerville|summerville city\b", "Summerville is a town")
    ban(r"\b134 motorcyclists?\b", "Use 132 motorcyclists killed")
    ban(r"lane splitting is (legal|allowed|permitted)", "Lane splitting is illegal in SC")
    ban(r"berlin g\.? myers parkway[^.]{0,30}\b(sc|s\.c\.)[- ]?165|\b(sc|s\.c\.)[- ]?165[^.]{0,30}berlin", "SC 165 is Bacons Bridge Road, the Berlin G. Myers route number is not verified")
    ban(r"kingstree[^.]{0,60}hospital|hospital[^.]{0,60}kingstree", "No hospital in Kingstree (closed January 2023)", level="WARN")
    ban(r"\bmistoc\b|\bpalmer\b|comfort dog|office dog", "Office dogs only on the homepage", where=(alltext if pid != "home" else ""))
    ban(r"\b(\d[\d,.]*)\s+(percent|per cent|dollars)\b", "Spell money and percent with $ and %")
    ban(r"\bpercent\b", "Use the % symbol", level="WARN")
    if "24/7" in alltext and alltext.count("24/7") > 1: FAIL("'24/7' more than once")
    star = len(re.findall(r"4\.8[- ]stars?|rated 4\.8|4\.8 out of", alltext, re.I))
    if star > 1: FAIL("4.8 star rating more than once")
    if star and pid not in ("home", "pa", "loc", "car", "truck", "moto", "ride", "slip", "dog", "wd", "cat", "ped"):
        FAIL("4.8 star rating is reserved for the homepage, menu pages and practice parents")
    if re.search(r"4\.8[^.]{0,40}(reviews?\b[^.]{0,10}\d)|\d+ reviews", alltext, re.I): FAIL("Never pair the rating with a review count")
    JUD = r"magistrate judge|probate judge|magistrate bench|probate bench|judgeship|served as a (judge|magistrate)|former (dorchester county )?(magistrate|judge)"
    tj = len({i for i, b in enumerate(paras) if re.search(JUD, b["text"], re.I)})
    if tj > 2: FAIL(f"Judicial service mentioned in {tj} paragraphs, max 2 per page")
    # punctuation
    for ch, name in (("—", "em dash"), ("–", "en dash"), (";", "semicolon"), (":", "colon")):
        if ch in alltext: FAIL(f"{name} in copy, e.g. '{alltext[max(0, alltext.find(ch)-40):alltext.find(ch)+20]}'")
    # self reference (LLG Part 5)
    ban(r"\b(this|our) (page|site|website|web page|webpage|section|guide|article|post|overview)\b|\bthe (page|website|web page|webpage|guide)\b|\bread on\b|\bkeep reading\b|\bscroll\w*\b|\breaders?\b|\bhere'?s\b|\bhere is\b|\bnext section\b|\bcomes next\b|\bwhat follows\b|\b(see|covered|discussed|explained|listed) (below|above)\b|\bas (noted|mentioned|discussed) (above|earlier|below)\b|\bclick\b|\blearn more\b|\bread more\b|\bin this (section|page)\b", "Self-referential copy")
    ban(r"\bbelow\b|\babove\b", "Check 'above' or 'below' is not about the page", level="WARN")
    # AI patterns
    ban(r"\b(elevate\w*|revolutioniz\w*|foster\w*|showcas\w*|profound|groundbreaking|delv\w*|synerg\w*|leverag\w*|harness\w*|paradigm|ecosystem|landscape|testament|pivotal|crucial|vibrant|renowned|meticulous\w*|tapestry|interplay|intricac\w*|intricate|underscor\w*|boasts?|garner\w*|cultivat\w*|bolster\w*|enhanc\w*|resonat\w*|reimagin\w*|unleash\w*|navigat\w*|seamless\w*|robust|empower\w*|journey|game[- ]changer|deep dive|rest assured|look no further|peace of mind|in today's|it's important to note|it is important to note|when it comes to|whether you're|don't hesitate|we understand that|at the end of the day|moreover|furthermore|additionally|subsequently|meanwhile|vital(?! signs)|significant\w*|comprehensive)\b", "AI-pattern word")
    ban(r"not only [^.]{0,60} but also|serves as a|stands as a|plays a (key|vital|crucial|pivotal|significant) role|is a testament|in the heart of|nestled", "AI-pattern phrase")
    ban(r"\bkey\s+(factor|point|role|piece|step|element|issue|question|evidence|takeaway)s?\b", "'key' as an adjective", level="WARN")
    ban(r"(,\s(highlighting|ensuring|emphasizing|underscoring|reflecting|showcasing|fostering|contributing)\b)", "Shallow -ing ending")
    ban(r"\b(\d+|a few|several|many|a couple of)\s+(weeks|months)\b", "Duration mention, check it is not a promise about how long a matter takes", level="WARN")
    # passive voice heuristic and sentence stats
    ss = sentences(alltext)
    lens = [len(s.split()) for s in ss]
    over25 = sum(l > 25 for l in lens) / max(len(ss), 1) * 100
    over20 = sum(l > 20 for l in lens) / max(len(ss), 1) * 100
    over35 = [s for s in ss if len(s.split()) > 35]
    (OK if over25 <= 10 else FAIL)(f"{over25:.1f}% of sentences over 25 words (max 10%)")
    (OK if over20 <= 25 else FAIL)(f"{over20:.1f}% of sentences over 20 words (max 25%)")
    if over35: FAIL(f"Sentence over 35 words '{over35[0][:90]}...'")
    irregular = "known|made|given|taken|seen|done|shown|written|held|found|paid|sent|told|kept|brought|built|caught|hit|hurt|struck|driven|thrown|left|put|set|read|heard|meant|led|run|bitten|killed|injured"
    ADJ = r"(?!(uninsured|underinsured|insured|married|red|tired|interested|located|licensed|qualified|experienced|concerned|scared|worried|prepared|entitled|allowed|supposed|related|based|limited|required|needed|designed|unmarked|marked|parked|impaired|intoxicated|distracted|exhausted|unmanned|unattended|unidentified|unknown|unsecured|registered|disabled|skilled|detailed|used)\b)"
    passive = [s for s in ss if re.search(r"\b(is|are|was|were|be|been|being|gets|got)\s+(\w+ly\s+)?" + ADJ + r"(\w+ed|" + irregular + r")\b", s, re.I)]
    pp = len(passive) / max(len(ss), 1) * 100
    (OK if pp < 10 else FAIL)(f"Passive voice estimate {pp:.1f}% of sentences (max under 10%)")
    firsts = [re.sub(r"[^a-z]", "", s.split()[0].lower()) if s.split() else "" for s in ss]
    for i in range(len(firsts) - 2):
        if firsts[i] and firsts[i] == firsts[i+1] == firsts[i+2]:
            FAIL(f"Three sentences in a row open with '{firsts[i]}' near '{ss[i][:60]}'"); break
    # repeated phrases within the page (4+ word, 3+ times, not keyphrase)
    toks = re.findall(r"[a-z0-9']+", low)
    grams = Counter(" ".join(toks[i:i+5]) for i in range(len(toks) - 4))
    fixed_bits = [kpl, "frost law group", "843 419 6653", "128 linwood lane", "south carolina", "free consultation"]
    rep = [g for g, c in grams.items() if c >= 3 and g not in kpl and not any(f in g for f in fixed_bits)]
    if rep: WARN(f"5-word phrases used 3+ times {rep[:4]}")

    # ---------------- 7. cross-page overlap (headers and 8-grams)
    others = [f for f in os.listdir(f"{ROOT}/pages") if f.endswith(".html") and f != f"{pid}.html"]
    myh = [b["text"] for b in heads if b["lvl"] >= 2]
    def normh(h):
        h = h.lower()
        h = re.sub(r"\b(summerville|dorchester|charleston|berkeley|colleton|orangeburg|beaufort|georgetown|williamsburg|county|south carolina|car|auto|truck|semi|18 wheeler|tractor trailer|motorcycle|biker|rider|rideshare|uber|lyft|slip and fall|premises|dog bite|dog attack|wrongful death|fatal|lawyers?|attorneys?|accident|crash|wreck|collision|injury|injuries|a|an|the|in|of|for|with|and|to|your|our)\b", " ", h)
        return re.sub(r"\s+", " ", h).strip()
    def shingles(t, n=8):
        w = re.findall(r"[a-z0-9%']+", t.lower().replace("$", ""))
        return {" ".join(w[i:i+n]) for i in range(len(w) - n + 1)}
    FIXED = ["843 419 6653", "128 linwood lane", "summerville sc 29483", "free confidential consultation"]
    fp = f"{ROOT}/tools/fixed_phrases.txt"
    if os.path.exists(fp): FIXED += [l.strip().lower() for l in open(fp) if l.strip() and not l.startswith("#")]
    FIXED = [re.sub(r"[^a-z0-9%' ]", " ", f.replace("$", "")).split() for f in FIXED]
    FIXED = [" ".join(f) for f in FIXED if f]
    mine8 = {g for g in shingles(alltext) if not any(f in g or g in f for f in FIXED)}
    hx, hn, pr = [], [], Counter()
    for f in others:
        osrc = open(f"{ROOT}/pages/{f}", encoding="utf8").read()
        ob = blocks_of(osrc)
        oh = [b["text"] for b in ob if b["lvl"] >= 2]
        for h in myh:
            if h in oh: hx.append((h, f))
            elif normh(h) and len(normh(h).split()) >= 3 and normh(h) in {normh(x) for x in oh}: hn.append((h, f))
        common = mine8 & shingles(" ".join(b["text"] for b in ob if not b["lvl"]))
        if common: pr[f] = len(common)
        if common and len(common) > 0 and not quiet:
            pr[f + "::ex"] = sorted(common)[:3]
    if hx: FAIL(f"Headings already used on other pages {hx[:4]}")
    if hn: WARN(f"Near-duplicate headings (same shape after removing place and case words) {hn[:4]}")
    tot8 = sum(v for k, v in pr.items() if not k.endswith("::ex"))
    if tot8 > 0:
        (FAIL if tot8 > 3 else WARN)(f"Shared 8-word sequences with other pages, {tot8} total " + str({k: v for k, v in pr.items()})[:600])

    # ---------------- 8. sidecar
    sc_path = f"{ROOT}/pages/{pid}.json"
    if not os.path.exists(sc_path): FAIL("Missing sidecar JSON")
    else:
        sc = json.load(open(sc_path))
        imgs = sc.get("images", [])
        if p["images"] == "none (homepage images are owned by the site design, flag for Daylin)" or p["id"] == "home":
            if imgs: WARN("Homepage images not expected")
        else:
            feat = [i for i in imgs if i.get("placement", "").lower().startswith("featured")]
            body = [i for i in imgs if i not in feat]
            if len(feat) != 1: FAIL("Exactly one featured image entry needed")
            if p["images"] == "parent":
                need = set(h2s)
                got = {i.get("placement") for i in body}
                if need - got: FAIL(f"Parent page needs one image under every H2, missing {list(need - got)[:3]}")
                kpc = sum(kpl in i.get("alt", "").lower() for i in body)
                if body and not (0.3 <= kpc / len(body) <= 0.7): FAIL(f"Parent body alts carrying the keyphrase {kpc}/{len(body)}, keep 30% to 70%")
            else:
                if len(body) != 1 or body[0].get("placement") != h2s[-1]: FAIL("Child page needs one image under the final H2 only")
                if not ANS and any(kpl not in i.get("alt", "").lower() for i in imgs): FAIL("Child page alts must all carry the exact keyphrase")
            for i in imgs:
                a = i.get("alt", "")
                if len(a) > 135: FAIL(f"Alt over 135 chars '{a[:50]}'")
                if re.search(r"[:;—–]", a): FAIL(f"Banned punctuation in alt '{a[:50]}'")
                if re.search(r"attorney[s]? (at|of) frost|frost law group (attorney|lawyer|team|staff|client)|our (attorney|lawyer|client|office)", a, re.I): FAIL(f"Alt presents stock people or places as the firm '{a[:60]}'")
                fn = i.get("file", "")
                if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*\.jpg", fn): FAIL(f"Bad image file name '{fn}'")
            if feat and kpl not in feat[0].get("alt", "").lower(): FAIL("Featured image alt must carry the exact keyphrase")
        for k in ("info_gain", "device", "local_hooks"):
            if not sc.get(k): FAIL(f"Sidecar missing '{k}'")

    # ---------------- 9. patched qa-scan on a scan .docx
    sys.path.insert(0, f"{ROOT}/tools")
    from minidocx2 import build
    os.makedirs(f"{ROOT}/scan", exist_ok=True)
    dpath = f"{ROOT}/scan/{pid}.docx"
    build(src, dpath)
    qkp = "personal injury cases" if pid == "pa" else kp
    city = "Summerville" if "County" not in p["h1"] else p["h1"].split(" in ")[-1].replace(" County", "")
    if p.get("type") == "City page (county child)":
        city = re.sub(r" (Car Accident|Personal Injury) Lawyers$", "", p["h1"])
    cmd = ["python3", f"{ROOT}/tools/qa-scan.py", dpath, "--keyphrase", qkp, "--domain", DOMAIN, "--city", city,
           "--min-words", str(lo), "--max-words", str(hi), "--max-kp-headings", "4",
           "--meta-title", p["title"], "--meta-desc", p["desc"]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    INFO_ONLY = ["6 to 14 H2s"]
    ACCEPT = {"loc": ["option 1 at 55 or fewer"], "pa": ["Keyphrase in H1", "Keyphrase in a body H2", "At least 1 H5 heading"],
              "home": ["Exact keyphrase in every title and description"]}
    if ANS:
        ACCEPT[pid] = ["At least 3 H4", "At least 1 H5", "Keyphrase in a body H2", "Keyphrase in the CTA H2 section", "3+ local markers", "option 1 at 55 or fewer"]
    for line in r.stdout.splitlines():
        m = re.match(r"\s+FAIL\s+(.*)", line)
        if m:
            label = m.group(1)
            if any(x in label for x in INFO_ONLY): continue
            if any(x in label for x in ACCEPT.get(pid, [])): WARN("qa-scan (accepted exception) " + label); continue
            FAIL("qa-scan " + label)
    if "passed." not in r.stdout: FAIL("qa-scan did not run " + r.stderr[-300:])

    # ---------------- 10. grammar
    if grammar:
        subprocess.run(["bash", f"{ROOT}/tools/ensure_lt.sh"])  # restart the LanguageTool server if it died
        env = dict(os.environ, LT_SERVER="http://127.0.0.1:8081")
        g = subprocess.run(["python3", f"{ROOT}/tools/grammar-scan.py", dpath, "--profile", f"{ROOT}/tools/frost-grammar-profile.md"],
                           capture_output=True, text=True, env=env)
        if g.returncode != 0:
            FAIL("grammar-scan errors:\n" + "\n".join(l for l in g.stdout.splitlines() if l.strip().startswith(("[", "...", "->")) or "      " in l)[:3000])
        else: OK("grammar-scan clean")

    # ---------------- report
    print("=" * 78); print(f"FROST CHECK  {pid}  {p['h1']}"); print("=" * 78)
    print(f"words {wc}  H2 {lv[2]} H3 {lv[3]} H4 {lv[4]} H5 {lv[5]} H6 {lv[6]}  internal {len(internal)} outbound {len(outbound)} tel {len(tels)}")
    for f in fails: print("  FAIL ", f)
    for w in warns: print("  WARN ", w)
    if not quiet:
        for o in passes: print("  ok   ", o)
    print("-" * 78)
    print("CLEARED" if not fails else f"{len(fails)} FAIL(S). Fix and rerun.")
    sys.exit(0 if not fails else 1)

if __name__ == "__main__":
    main()
