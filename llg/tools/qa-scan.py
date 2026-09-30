#!/usr/bin/env python3
"""
qa-scan.py  --  mechanical QA gate for weekly legal blogs.
Added 2026-08-26 after five defects shipped across every client while
the old checklist passed them. Rules that only live in prose get skipped.
These do not.

Usage:
  python3 qa-scan.py BLOG.docx --keyphrase "Auburn dog bite lawyer" --domain kreegerlaw.com [--city Auburn]

Exit code 0 = every check passed. 1 = at least one FAIL. Do not deliver on a FAIL.
2026-08-28: added the H1-section checks. The old 28 skipped level 1 completely.
2026-09-22: added the metadata, heading, anchor and claims checks (section 8 and 9).
  The old scanner never read the metadata block except for pipes, so the 09-21
  Hawkins and RH&A blogs scored 31/31 with SEO titles that carried no CTA, a
  "Guide" title, "51 percent" spelled out, and Gold Law's ten titles were one
  question with ten CTA swaps. Sources: Daylin's 2026-09-21 LLG article on PI SEO
  for 2027, Riemer's SEL title tag guide for 2027, Google's title link docs, and
  California Rule of Professional Conduct 7.1 and its comments.
  Pages: pass --max-kp-headings 4. California clients: pass --state CA.
"""
import zipfile, re, sys, argparse, html
from collections import Counter

BANNED = r"\b(elevate|revolutionize|fostering|showcase|profound|groundbreaking|delve|synergies|leverage|harness|paradigm|ecosystem|landscape|testament|pivotal|crucial|vibrant|renowned|meticulous|deep dive|Additionally|Moreover|Furthermore|Subsequently|Meanwhile)\b"
BANNED_PHRASE = r"(not only .{0,40} but also|plays a crucial role|serves as a reminder|stands as a testament|underscores the importance|in today's fast-paced)"

results = []
def check(ok, label, detail=""):
    results.append((ok, label, detail))

def parse(path):
    z = zipfile.ZipFile(path)
    doc = z.read('word/document.xml').decode('utf8')
    try:
        rels = z.read('word/_rels/document.xml.rels').decode('utf8')
    except KeyError:
        rels = ''
    rmap = dict(re.findall(r'Id="([^"]+)"[^>]*?Target="([^"]+)"', rels))
    seq = []
    for p in re.findall(r'<w:p[ >].*?</w:p>', doc, re.S):
        style = re.search(r'w:val="(Heading[1-9]|Title)"', p)
        text = html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p)))
        links = [html.unescape(rmap.get(i, '')) for i in re.findall(r'r:id="([^"]+)"', p)]
        # anchor text per hyperlink, added 2026-09-22
        anchors = []
        for rid, inner in re.findall(r'<w:hyperlink[^>]*?r:id="([^"]+)"[^>]*>(.*?)</w:hyperlink>', p, re.S):
            url = html.unescape(rmap.get(rid, ''))
            txt = html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', inner))).strip()
            if url: anchors.append((url, txt))
        lvl = 0
        if style:
            lvl = 1 if style.group(1) == 'Title' else int(style.group(1)[-1])
        seq.append({'lvl': lvl, 'text': text, 'links': [l for l in links if l], 'anchors': anchors})
    return seq

# ---- 2026-09-22 metadata and claims vocabulary ----
# A title needs a call to action (Daylin's standing metadata rule). This is a floor, not a style guide.
CTA = (r"\b(call|talk|speak|ask|get|start|book|schedule|request|contact|reach|see|find out|learn|check|hire|"
       r"protect|fight|consult|act (fast|now|quickly|today)|free (case )?(review|consultation|evaluation))\b|^review\b")
# AI-styled title wording named in Riemer's 2027 SEL guide, plus the house superlative ban.
AI_TITLE = (r"\b(ultimate|comprehensive|complete guide|guide|everything you need to know|what you need to know|"
            r"the truth about|secrets?|perfect|best(?! interests?)|top|essential|navigat\w*|unlock\w*|demystif\w*|ins and outs)\b")
# A title whose main clause is a question. "Hurt in an Uber? Call..." is a hook, not a question title.
QFORM = (r"^(how (much|many|long|often|do|does|did|is|are|can|should|will)|"
         r"what (is|are|does|do|did|can|should|will|happens|if)|why (is|are|does|do|did|should|would)|"
         r"when (is|are|does|do|should|can|will)|who (is|are|pays|can|should)|which|"
         r"can|could|does|do|did|is|are|should|will|would|was|were)\b")
STOP = set("a an the and or of in on to for with by at is are your you my our from after before "
           "what how why when who which does do can it its this that as if".split())
VALUE = r"\b(worth|how much|value|payout|average settlement|costs?)\b"
GENERIC_HEAD = (r"^(conclusion|summary|in summary|introduction|overview|our process|the process|final thoughts|"
                r"key takeaways|takeaways|next steps|why it matters|why choose us|about us|faqs?|"
                r"frequently asked questions|get help today|contact us( today)?|learn more|the bottom line)$")
GENERIC_ANCHOR = (r"^(click here|here|this page|this link|read more|learn more|more|link|this article|"
                  r"this post|website|this website|click)$")
# Outcome predictions. ABA Model Rule 7.1 and Cal. RPC 7.1 cmt: a truthful statement still misleads
# when it creates an unjustified expectation, and an express guarantee is misleading per se.
# "signature guarantee" and "medallion guarantee" are real transfer terms, so only outcome guarantees count.
OUTCOME = r"(results?|outcomes?|recover(y|ies)|settlements?|wins?|compensation|money|payouts?|verdicts?)"
PROMISE = (r"\b((we|i|the firm) guarantees?\b|guarantee[sd]? (a |an |the |your |that you )?" + OUTCOME +
           r"|guaranteed " + OUTCOME + r"|(we|you) will win\b|(you will|you'll) (recover|receive|get) "
           r"(compensation|money|a settlement|paid|\$)|compensation you deserve)")
NEGATED = r"(\bno|\bnot|cannot|can't|never|n't|without|promis\w*|offer\w*|claim\w*|wary of|beware of)\s+(a\s+|any\s+|an\s+)?$"
# "No fee unless we win" style statements. Cal. RPC 7.1 comment: misleading unless the same
# communication expressly discloses whether the client is liable for costs.
NOFEE = (r"(no (legal |attorney'?s? )?fees?\b.{0,20}\b(unless|until)|pay (nothing|no (legal |attorney'?s? )?fees?)"
         r".{0,10}\b(unless|until)|don'?t pay .{0,15}\b(unless|until)|only (get )?paid (if|when)|"
         r"owe (us )?nothing)")
# What counts as a cost disclosure. "The call costs nothing" does not, so the plain word "costs" is not enough.
COST_DISCLOSE = (r"\b(fees? (or|and) (case )?costs|costs? (or|and) (fees|expenses)|case costs|costs? of the case|"
                 r"(owe|pay|reimburse|repay|responsible for|liable for)\b.{0,40}\b(costs?|expenses)|"
                 r"(costs?|expenses)\b.{0,60}\b(no recovery|without a recovery|if (we|the firm) (lose|loses|do not win|does not win|don't win|doesn't win))|"
                 r"advances?\b.{0,30}\b(costs?|expenses))")
SMALL = {str(i): w for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve".split())}

def meta_lists(meta):
    """Pull the 10 titles and 10 descriptions out of the metadata block.
    Layouts seen across 23 delivered blogs (checked 2026-09-22): a "SEO titles" label line, a
    "10 SEO Titles, 60 characters or fewer" label, "T1." / "Title 1." / "Meta 1." prefixes, and
    bare numbered lines with a "(54)" count and no label at all. A line prefix decides first, then
    the last label, then length (titles run 60 or fewer, descriptions 150 or more)."""
    T_LABEL = r'^(\d+\s+)?(seo\s+)?(title|titles|title options|title tags?)\b'
    D_LABEL = r'^(\d+\s+)?meta\s+(description|descriptions)\b'
    PREFIX = (r'^\s*(seo title|title|t|meta description|meta|description|desc|d|option)?\s*'
              r'(\d+)\s*[.):]\s+(.+)$')
    titles, descs, mode = [], [], None
    for n in meta[1:]:
        t = n['text'].strip()
        if not t: continue
        m = re.match(PREFIX, t, re.I)
        if not m:
            if len(t) < 120 and re.match(T_LABEL, t, re.I): mode = 't'; continue
            if len(t) < 120 and re.match(D_LABEL, t, re.I): mode = 'd'; continue
            if re.match(r'(focus )?keyphrase\b|slug\b|recommended\b|url\b', t, re.I) or n['lvl']:
                # a bare label such as "Focus keyphrase" carries its value on the next line
                mode = 'skip' if len(t) < 30 and ':' not in t else None; continue
            if mode == 'skip':
                mode = None; continue
            body = t
            kind = mode
        else:
            body = m.group(3)
            pre = (m.group(1) or '').lower()
            kind = 't' if pre in ('seo title', 'title', 't') else 'd' if pre in (
                'meta description', 'meta', 'description', 'desc', 'd') else mode
        body = re.sub(r'\s*\(\d+\s*(chars?|characters)?\)\s*$', '', body).strip()
        if kind is None:
            kind = 't' if len(body) <= 80 else 'd' if len(body) >= 110 else None
        if kind == 't': titles.append(body)
        elif kind == 'd': descs.append(body)
    return titles, descs

def norm(s):
    return re.sub(r'[^a-z0-9 ]', '', s.lower()).strip()

def sentences(t):
    return [s for s in re.split(r'(?<=[.?!])\s+', t) if s.strip()]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('docx')
    ap.add_argument('--keyphrase', required=True)
    ap.add_argument('--domain', required=True, help='client site domain, decides internal vs outbound')
    ap.add_argument('--city', default=None)
    ap.add_argument('--min-words', type=int, default=1200)
    ap.add_argument('--max-words', type=int, default=3000, help='raise only when a client brief sets a longer length (Gold Law briefs)')
    ap.add_argument('--max-kp-headings', type=int, default=3,
                    help='headings allowed to carry the exact keyphrase, H1 included. Blogs 3, pages 4')
    ap.add_argument('--state', default=None, help='client state. CA turns on the no-fee cost disclosure check')
    ap.add_argument('--meta-title', default=None, help='FROST PATCH: the single Yoast title (Upload Sheet delivery, LLG Part 9)')
    ap.add_argument('--meta-desc', default=None, help='FROST PATCH: the single meta description')
    a = ap.parse_args()
    seq = parse(a.docx)
    kp = a.keyphrase.lower()

    # strip the metadata block, it is not page copy
    cut = len(seq)
    for i, n in enumerate(seq):
        if n['lvl'] and ('metadata options' in n['text'].lower() or 'upload sheet' in n['text'].lower()):
            cut = i; break
    page, meta = seq[:cut], seq[cut:]
    heads = [n for n in page if n['lvl']]
    body  = [n for n in page if not n['lvl'] and n['text'].strip()]
    alltext = ' '.join(n['text'] for n in body)
    words = len(alltext.split())

    # ---------- 1. structure ----------
    lv = Counter(n['lvl'] for n in heads)
    check(lv[1] == 1, "Exactly one H1", f"found {lv[1]}")
    check(6 <= lv[2] <= 14, "6 to 14 H2s", f"found {lv[2]}")
    check(lv[4] >= 3, "At least 3 H4 headings", f"found {lv[4]}")
    check(lv[5] >= 1, "At least 1 H5 heading", f"found {lv[5]}")

    skips = [(heads[i-1]['text'][:40], heads[i]['text'][:40])
             for i in range(1, len(heads)) if heads[i]['lvl'] - heads[i-1]['lvl'] > 1]
    check(not skips, "No skipped heading levels", str(skips[:3]))

    # lone children
    lone = []
    for i, n in enumerate(heads):
        kids = []
        for m in heads[i+1:]:
            if m['lvl'] <= n['lvl']: break
            if m['lvl'] == n['lvl'] + 1: kids.append(m['text'])
        if len(kids) == 1:
            lone.append(f"H{n['lvl']} '{n['text'][:38]}' has 1 child")
    check(not lone, "No lone child headings", "; ".join(lone[:3]))

    # ---------- 2. thin PText ----------
    MIN = {2: (90, 2, 1), 3: (60, 1, 3), 4: (45, 1, 3), 5: (40, 1, 3), 6: (40, 1, 3)}   # 6 added 2026-09-22, pages reach H6
    idx = {id(n): i for i, n in enumerate(page)}

    # ---- FAQ zone detection, corrected 2026-08-31 ----
    # The old lexical test r'\b(faq|question|answers?)\b' had two defects.
    #   1. "question" never matched the plural, so "Frequently Asked Questions" and
    #      "Questions Parents Ask About X" were held to the full H2 and H3 minimums.
    #      Three blogs failed on this in the 08-31 batch while being spec-correct.
    #   2. Worse, a substantive body H2 containing the word "Answer" silently
    #      relaxed its own section's minimums. That is a hole in the gate, not a
    #      false alarm, and it is the kind of blind spot the last two defects
    #      shipped through.
    # A FAQ section is now identified structurally AND lexically: the H2 has to read
    # like a FAQ heading and its immediate H3 children have to be mostly questions.
    faq_h2 = set()
    for i, n in enumerate(page):
        if n['lvl'] != 2: continue
        if not re.search(r'\b(faq|frequently asked|questions?|answers?)\b', n['text'], re.I):
            continue
        kids = []
        for m in page[i+1:]:
            if m['lvl'] == 2: break
            if m['lvl'] == 3: kids.append(m['text'].strip())
        if len(kids) >= 3 and sum(k.endswith('?') for k in kids) >= 0.75 * len(kids):
            faq_h2.add(i)

    thin, faq_zone = [], False
    for i, n in enumerate(page):
        if not n['lvl'] or n['lvl'] == 1: continue
        if n['lvl'] == 2:
            faq_zone = i in faq_h2
        after = []
        for m in page[i+1:]:
            if m['lvl']: break
            if m['text'].strip(): after.append(m['text'])
        mw, mp, ms = MIN[n['lvl']]
        if faq_zone and n['lvl'] == 2:
            mw, mp, ms = 45, 1, 2   # FAQ lead-in, one real paragraph, not a one-liner
        if faq_zone and n['lvl'] == 3:
            mw, mp, ms = 20, 1, 2   # FAQ answers run 2 to 4 sentences by design
        w = sum(len(x.split()) for x in after)
        s = sum(len(sentences(x)) for x in after)
        if not after:
            thin.append(f"H{n['lvl']} '{n['text'][:38]}' STACKED, no text")
        elif w < mw or len(after) < mp or s < ms:
            thin.append(f"H{n['lvl']} '{n['text'][:38]}' {w}w/{len(after)}p/{s}s needs {mw}w/{mp}p/{ms}s")
    check(not thin, "Every heading has a full paragraph", "; ".join(thin[:4]))

    # ---------- 2b. the H1 section, added 2026-08-28 ----------
    # The scanner skipped level 1 entirely, so a one-paragraph H1 section with no
    # phone CTA scored 28/28 and shipped. Daylin's standing rule is a short phone
    # CTA inside the H1 section whenever the client has an approved number, and the
    # section carries the published line, the answer block, orientation, and the CTA.
    h1i = next((i for i, n in enumerate(page) if n['lvl'] == 1), None)
    intro = []
    if h1i is not None:
        for n in page[h1i+1:]:
            if n['lvl']: break
            if n['text'].strip(): intro.append(n)
    check(len(intro) >= 3, "H1 section has 3+ paragraphs",
          f"found {len(intro)}, needs answer block, orientation, phone CTA")
    check(any(l.lower().startswith('tel:') for n in intro for l in n['links']),
          "Phone CTA with tel: link in the H1 section")
    # Daylin 2026-09-16: never add a "Published ... Last updated ..." line to a blog.
    check(not any(re.search(r'^\s*published\b|last updated', n['text'], re.I) for n in page),
          "No 'Published / Last updated' line anywhere (banned 2026-09-16)")

    # ---------- 3. links ----------
    dom = a.domain.lower().replace('www.', '')
    internal, outbound, tel = [], [], []
    for n in page:
        for l in n['links']:
            ll = l.lower()
            if ll.startswith('tel:'): tel.append(l)
            elif dom in ll: internal.append(l)
            elif ll.startswith('http'): outbound.append(l)
    check(len(internal) >= 4, "At least 4 internal links", f"found {len(internal)}")
    check(len(outbound) <= 2, "At most 2 outbound links", f"found {len(outbound)}: " + ", ".join(
        sorted({re.sub(r'https?://(www\.)?([^/]+).*', r'\2', u) for u in outbound}))[:160])
    check(len(internal) > len(outbound), "Internal outnumbers outbound", f"{len(internal)} vs {len(outbound)}")
    check(len(tel) >= 1, "tel: link present", f"found {len(tel)}")
    check(any('contact' in l.lower() for l in internal), "Contact page link present")

    # first internal link must be in the FIRST paragraph under the FIRST H2
    fh2 = next((i for i, n in enumerate(page) if n['lvl'] == 2), None)
    if fh2 is None:
        check(False, "First internal link in 1st paragraph under 1st H2", "no H2 found")
    else:
        first_para = next((n for n in page[fh2+1:] if not n['lvl'] and n['text'].strip()), None)
        got = [l for l in (first_para['links'] if first_para else []) if dom in l.lower()]
        where = ""
        if not got:
            for j, n in enumerate(page[fh2+1:], 1):
                if any(dom in l.lower() for l in n['links']):
                    where = f"first internal link appears {j} blocks later instead"; break
            if not where: where = "no internal link in the first H2 section at all"
        check(bool(got), "First internal link in 1st paragraph under 1st H2", where)

    # ---------- 4. keyphrase ----------
    h1 = next((n['text'] for n in page if n['lvl'] == 1), '')
    check(kp in h1.lower(), "Keyphrase in H1", f"H1 is '{h1[:70]}'")
    first100 = ' '.join(alltext.split()[:100]).lower()
    check(kp in first100, "Keyphrase in first 100 words")
    check(any(kp in n['text'].lower() for n in heads if n['lvl'] == 2), "Keyphrase in a body H2")
    lasth2 = max((i for i, n in enumerate(page) if n['lvl'] == 2), default=None)
    cta = ' '.join(n['text'] for n in page[lasth2:]).lower() if lasth2 is not None else ''
    check(kp in cta, "Keyphrase in the CTA H2 section")
    dens = alltext.lower().count(kp) * len(kp.split()) / max(words, 1) * 100
    check(dens < 2.5, "Keyphrase density under 2.5%", f"{dens:.2f}%")

    # ---------- 5. sentences ----------
    ss = sentences(alltext)
    long25 = [s for s in ss if len(s.split()) > 25]
    # a directly quoted statute may run long, per blog-spec. Everything else may not.
    long35 = [s for s in ss if len(s.split()) > 35 and '"' not in s]
    quoted = [s for s in ss if len(s.split()) > 35 and '"' in s]
    pct = len(long25) / max(len(ss), 1) * 100
    check(pct <= 10, "10% or fewer sentences over 25 words", f"{pct:.1f}% ({len(long25)}/{len(ss)})")
    check(not long35, "No sentence over 35 words, quoted statutes exempt",
          (long35[0][:110] + "...") if long35 else "")
    if quoted:
        print(f"  NOTE  {len(quoted)} long sentence(s) exempted as quoted statute. Confirm the quote is needed.")

    # ---------- 6. punctuation and banned ----------
    check('—' not in alltext, "No em dashes")
    check(';' not in alltext, "No semicolons")
    hcolon = [n['text'] for n in heads if ':' in n['text']]
    check(not hcolon, "No colons in headings", str(hcolon[:2]))
    metatext = ' '.join(n['text'] for n in meta)
    if a.meta_title is not None:
        # LLG house rule (Part 4, Part 16): SEO titles carry at most one | between keyphrase and CTA.
        check(a.meta_title.count('|') <= 1 and '|' not in (a.meta_desc or ''),
              "Title has at most one | (house rule), description has none")
    else:
        check('|' not in metatext, "No pipes in metadata")
    b = re.findall(BANNED, alltext, re.I) + re.findall(BANNED_PHRASE, alltext, re.I)
    check(not b, "No banned words or phrases", str(Counter(x if isinstance(x, str) else x[0] for x in b).most_common(4)))
    check('faqpage' not in alltext.lower(), "No FAQPage schema")

    # ---------- 7. length and local hook ----------
    check(a.min_words <= words <= a.max_words, f"Word count {a.min_words:,} to {a.max_words:,}", f"{words} words")
    if a.city:
        stripped = re.sub(re.escape(a.city), '', alltext, flags=re.I)
        markers = len(re.findall(r'\b(County|Courthouse|Superior Court|District Court|Police Department|Sheriff|Highway|Freeway|Interstate|Hospital|Medical Center|Avenue|Boulevard|Precinct|Division|Ordinance)\b', stripped))
        check(markers >= 3, "3+ local markers survive the city-name strip", f"{markers} markers")

    # ---------- 8. metadata, added 2026-09-22 ----------
    # Google rewrites titles that are inaccurate, boilerplate or stuffed, and Riemer's 2027 guide
    # finds shorter, human-worded titles win the click when competitors fill 55 to 60 characters.
    if a.meta_title is not None:
        titles, descs = [a.meta_title], [a.meta_desc or '']
        single = True
    else:
        titles, descs = meta_lists(meta)
        single = False
        check(len(titles) == 10 and len(descs) == 10, "Metadata block has 10 SEO titles and 10 descriptions",
              f"found {len(titles)} titles, {len(descs)} descriptions")
    over = [f"{len(t)}c '{t[:40]}'" for t in titles if len(t) > 60]
    lim1 = 55 if len(kp) <= 40 else 60   # a 41+ character keyphrase leaves no room for a CTA at 55
    first_ok = bool(titles) and len(titles[0]) <= lim1
    check(bool(titles) and not over and first_ok, f"SEO titles 60 chars max, option 1 at {lim1} or fewer",
          "; ".join(over[:2]) or (f"option 1 is {len(titles[0])} chars" if titles else "no titles"))
    offd = [f"{len(d)}c" for d in descs if not 150 <= len(d) <= 156]
    check(bool(descs) and not offd, "Meta descriptions 150 to 156 chars", ", ".join(offd[:6]))
    nokp = [x[:45] for x in titles + descs if kp not in x.lower()]
    check(bool(titles) and not nokp, "Exact keyphrase in every title and description", "; ".join(nokp[:3]))
    nocta = [x[:48] for x in titles + descs if not re.search(CTA, x, re.I)
             and not (single and x in titles and x.strip().lower() == kp and len(kp) > 50)]
    check(bool(titles) and not nocta, "A CTA in every title and description",
          f"{len(nocta)} without: " + "; ".join(nocta[:3]))
    stuffed = []
    for t in titles:
        cw = [w for w in re.findall(r"[a-z0-9$%']+", t.lower()) if w not in STOP]
        dup = [w for w, c in Counter(cw).items() if c > 1]
        if dup: stuffed.append(f"'{t[:40]}' repeats '{dup[0]}'")
    check(not stuffed, "No word repeated inside a title", "; ".join(stuffed[:2]))
    ai = [t[:45] for t in titles if re.search(AI_TITLE, t, re.I) or '!' in t
          or len(re.findall(r'[.?](?=\s)', t.rstrip('.? '))) > 1]
    check(not ai, "No AI-styled or over-punctuated title wording", "; ".join(ai[:3]))
    mt = ' '.join(titles + descs)
    badc = [c for c in (':', '—', '–', ';') if c in mt]
    phone = re.search(r'\(?\b\d{3}\)?[\s.-]\d{3}[-.]\d{4}\b', mt)
    check(not badc and not phone, "No colons, dashes, or phone numbers in titles and descriptions",
          (f"found {badc}" if badc else "") + (f" phone {phone.group(0)}" if phone else ""))
    qs = [t for t in titles if t.rstrip().endswith('?') or re.match(QFORM, t.strip(), re.I)]
    opens = Counter(' '.join(norm(t).split()[:4]) for t in titles)
    top_open, top_n = opens.most_common(1)[0] if opens else ('', 0)
    t1 = titles[0] if titles else ''
    shape = []
    # A brief-set question keyphrase (Gold Law) forces question titles and, at 40+ characters,
    # a shared opening, so only the repeats-the-H1 check applies. Judge the ten angles by eye.
    kp_is_q = bool(re.match(QFORM, kp.strip(), re.I))
    if t1 and t1 in qs and not kp_is_q: shape.append("option 1 is a question, ship a statement")
    if t1 and norm(t1) == norm(h1) and not (single and len(kp) > 50): shape.append("option 1 repeats the H1")
    if not single and len(qs) > 3 and not kp_is_q: shape.append(f"{len(qs)} of {len(titles)} titles are questions, max 3")
    if not single and top_n > 5 and not kp_is_q: shape.append(f"{top_n} titles open with '{top_open}', max 5")
    check(bool(titles) and not shape, "Title options vary in shape and option 1 is a statement", "; ".join(shape))
    missing = []
    for x in titles + descs:
        for tok in re.findall(r'\d[\d,]*(?:\.\d+)?', re.sub(r'\b24/7\b', '', x)):
            tok = tok.rstrip(',.')
            if tok in alltext: continue
            if tok in SMALL and re.search(r'\b' + SMALL[tok] + r'\b', alltext, re.I): continue
            missing.append(tok)
    vt = [t[:40] for t in titles if re.search(VALUE, t, re.I)]
    no_dollar = bool(vt) and not re.search(r'\$\s?\d', alltext)
    check(not missing and not no_dollar, "Metadata promises only what the page delivers",
          (f"numbers not in the page: {sorted(set(missing))[:6]}" if missing else "")
          + (f" value title but no $ figure in the page: '{vt[0]}'" if no_dollar else ""))

    # ---------- 9. headings, anchors and claims, added 2026-09-22 ----------
    kph = [n['text'][:50] for n in heads if kp in n['text'].lower()]
    check(len(kph) <= a.max_kp_headings,
          f"Exact keyphrase in {a.max_kp_headings} headings or fewer, variants in the rest",
          f"{len(kph)}: " + "; ".join(kph[:4]))
    gen = [f"H{n['lvl']} '{n['text']}'" for n in heads
           if re.match(GENERIC_HEAD, n['text'].strip().rstrip('?.'), re.I)
           or (n['lvl'] == 2 and len(n['text'].split()) < 4)]
    check(not gen, "No generic or vague headings, every H2 4+ words", "; ".join(gen[:3]))
    anc = [(u, t) for n in page for (u, t) in n.get('anchors', [])]
    weak = [t for u, t in anc if not t.strip() or re.match(GENERIC_ANCHOR, t.strip().rstrip('.'), re.I)]
    kpout = [t for u, t in anc if u.lower().startswith('http') and dom not in u.lower() and kp in t.lower()]
    check(not weak and not kpout, "Descriptive anchor text, no outbound link on the keyphrase",
          "; ".join([f"weak '{t}'" for t in weak[:2]] + [f"outbound on keyphrase '{t[:40]}'" for t in kpout[:1]]))
    prom = []
    for n in body:
        for mm in re.finditer(PROMISE, n['text'], re.I):
            if re.search(NEGATED, n['text'][max(0, mm.start() - 30):mm.start()], re.I): continue
            prom.append(n['text'][max(0, mm.start() - 30):mm.end() + 20])
    check(not prom, "No guarantee or predicted outcome", "; ".join(prom[:2]))
    spelled = re.findall(r'\b\d[\d,.]*\s+(?:percent|per cent|dollars)\b',
                         ' '.join([alltext] + [n['text'] for n in heads] + titles + descs), re.I)
    check(not spelled, "Money and percentages as $ and %, never spelled out", "; ".join(spelled[:3]))
    nofee = [x for x in [n['text'] for n in body] + titles + descs if re.search(NOFEE, x, re.I)
             and not re.search(COST_DISCLOSE, x, re.I)]
    if a.state and a.state.strip().lower() in ('ca', 'california'):
        check(not nofee, "No-fee statement also says whether the client owes costs (Cal. RPC 7.1)",
              "; ".join(x[:90] for x in nofee[:2]))
    elif nofee:
        print(f"  NOTE  {len(nofee)} no-fee statement(s) with no cost disclosure. "
              "Required for California clients, advisable everywhere.")

    # ---------- report ----------
    fails = [r for r in results if not r[0]]
    print("=" * 74)
    print(a.docx.split('/')[-1])
    print("=" * 74)
    for ok, label, detail in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"   [{detail}]" if detail and not ok else ""))
    print("-" * 74)
    print(f"{len(results)-len(fails)}/{len(results)} passed." + ("  DO NOT DELIVER." if fails else "  Cleared for delivery."))
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main())
