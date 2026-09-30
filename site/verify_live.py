#!/usr/bin/env python3
"""Check a deployed copy of the site before and after the domain switch.

    python3 site/verify_live.py https://summervilleaccident-pi.vercel.app
    python3 site/verify_live.py https://www.summervilleaccidentattorney.com

Checks that
  - robots.txt and sitemap.xml load, and robots.txt points at the www sitemap,
  - every URL in the sitemap returns 200 at the base, with no redirect,
  - every page has exactly one canonical, on https://www.summervilleaccidentattorney.com with its own path,
  - every page carries the tel:+18434196653 link, and the CallRail script when firm.CALLRAIL_SCRIPT is set,
  - every redirect in site/content/redirects.json lands on its destination with a 200, with and without the trailing slash,
  - an unknown URL returns 404.
When the base is the real domain, it also checks that the bare domain and http both end at https://www.

Standard library only. Exits 1 on any failure.
"""
import concurrent.futures
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from content import firm  # noqa: E402

WWW = firm.ORIGIN.rstrip("/")                      # https://www.summervilleaccidentattorney.com
WWW_HOST = urllib.parse.urlsplit(WWW).hostname
BARE_HOST = WWW_HOST.removeprefix("www.")
TEL = f'href="tel:{firm.PHONE_E164}"'
TRACKING_NUMBER = re.compile(r"983[\s.)-]*2304")   # the CallRail number, never in the served HTML
PERMANENT = {301, 308}
UA = "frost-verify-live/1.0"
WORKERS = 8


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def get(url, tries=3):
    """One request, no redirects followed. Returns (status, location, body)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(tries):
        try:
            with OPENER.open(req, timeout=30) as r:
                return r.status, r.headers.get("Location"), r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, e.headers.get("Location"), e.read().decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if attempt == tries - 1:
                return None, None, f"{type(e).__name__}: {e}"
            time.sleep(2 ** attempt)


def follow(url, max_hops=6):
    """Follow redirects by hand. Returns (chain, body), where chain is [(status, url), ...]."""
    chain = []
    for _ in range(max_hops + 1):
        status, loc, body = get(url)
        chain.append((status, url))
        if status in (301, 302, 303, 307, 308) and loc:
            url = urllib.parse.urljoin(url, loc)
            continue
        return chain, body
    return chain, ""


def show(chain):
    return " -> ".join(f"{s} {u}" for s, u in chain)


class Canonicals(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.found.append(a.get("href"))


def callrail_src():
    tag = getattr(firm, "CALLRAIL_SCRIPT", "") or ""
    m = re.search(r'src="([^"]+)"', tag)
    return m.group(1) if m else None


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    base = sys.argv[1].rstrip("/")
    if "://" not in base:
        base = "https://" + base
    host = urllib.parse.urlsplit(base).hostname
    real = host in (WWW_HOST, BARE_HOST)
    if real:
        base = WWW                                   # page checks always run on the canonical host
    fails, notes = [], []

    def fail(msg):
        fails.append(msg)

    print(f"Checking {base}" + ("  (real domain)" if real else ""))

    # robots.txt and sitemap.xml
    status, _, robots = get(base + "/robots.txt")
    if status != 200:
        fail(f"robots.txt returned {status}")
    else:
        if f"Sitemap: {WWW}/sitemap.xml" not in robots:
            fail("robots.txt does not name the www sitemap")
        if re.search(r"(?mi)^Disallow:\s*/\s*$", robots):
            fail("robots.txt blocks the whole site")
    status, _, sitemap = get(base + "/sitemap.xml")
    locs = []
    if status != 200:
        fail(f"sitemap.xml returned {status}")
    else:
        try:
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            locs = [e.text.strip() for e in ET.fromstring(sitemap.encode()).findall("sm:url/sm:loc", ns)]
        except ET.ParseError as e:
            fail(f"sitemap.xml does not parse: {e}")
        if not locs:
            fail("sitemap.xml lists no URLs")
    print(f"  robots.txt and sitemap.xml: {len(locs)} URLs in the sitemap")

    # every sitemap page
    swap = callrail_src()

    def check_page(loc):
        out = []
        parts = urllib.parse.urlsplit(loc)
        if f"{parts.scheme}://{parts.netloc}" != WWW:
            out.append(f"sitemap URL is not on {WWW}: {loc}")
        url = base + parts.path
        status, loc_hdr, body = get(url)
        if status != 200:
            out.append(f"{parts.path} returned {status}" + (f" to {loc_hdr}" if loc_hdr else ""))
            return out
        p = Canonicals()
        p.feed(body)
        if len(p.found) != 1:
            out.append(f"{parts.path} has {len(p.found)} canonical tags")
        elif p.found[0] != WWW + parts.path:
            out.append(f"{parts.path} canonical is {p.found[0]}, expected {WWW + parts.path}")
        if TEL not in body:
            out.append(f"{parts.path} has no tel:{firm.PHONE_E164} link")
        if TRACKING_NUMBER.search(body):
            out.append(f"{parts.path} contains the CallRail tracking number")
        if swap and swap not in body:
            out.append(f"{parts.path} is missing the CallRail script")
        return out

    with concurrent.futures.ThreadPoolExecutor(WORKERS) as ex:
        results = list(ex.map(check_page, locs))
    fails += [m for r in results for m in r]
    extra = " and the CallRail script" if swap else ""
    print(f"  pages: {sum(1 for r in results if not r)} of {len(locs)} return 200 with the right canonical and the phone link{extra}")

    # redirect map
    pairs = json.load(open(os.path.join(HERE, "content", "redirects.json"), encoding="utf-8"))
    tests = []
    for old, new in pairs:
        old = "/" + old.strip("/")
        tests += [(old, new), (old + "/", new)]

    def check_redirect(t):
        old, new = t
        chain, _ = follow(base + old)
        final_status, final_url = chain[-1]
        want = base + new
        if final_url != want or final_status != 200:
            return [f"redirect {old} should land on {new} with 200, got {show(chain)}"]
        if chain[0][0] not in PERMANENT:
            return [f"redirect {old} uses {chain[0][0]}, expected a permanent redirect"]
        if len(chain) > 2:
            multi.append(show(chain))
        return []

    multi = []

    with concurrent.futures.ThreadPoolExecutor(WORKERS) as ex:
        redirect_fails = [m for r in ex.map(check_redirect, tests) for m in r]
    fails += redirect_fails
    print(f"  redirects: {len(tests) - len(redirect_fails)} of {len(tests)} land on their destination with 200 ({len(pairs)} entries, with and without the slash)")
    if multi:
        notes.append(f"{len(multi)} redirects take more than one hop, for example {min(multi, key=len)}")

    # unknown URL
    probe = f"/verify-live-{uuid.uuid4().hex[:12]}/"
    chain, _ = follow(base + probe)
    if chain[-1][0] != 404:
        fail(f"unknown URL {probe} should return 404, got {show(chain)}")
    print(f"  unknown URL: {chain[-1][0]}")

    # host and scheme, real domain only
    if real:
        host_tests = [
            (f"http://{BARE_HOST}/", WWW + "/"),
            (f"https://{BARE_HOST}/", WWW + "/"),
            (f"http://{WWW_HOST}/", WWW + "/"),
        ]
        old, new = pairs[0]
        host_tests.append((f"http://{BARE_HOST}{old}", WWW + new))   # host, HTTPS and the redirect map in one request
        for start, want in host_tests:
            chain, _ = follow(start)
            if chain[-1] != (200, want):
                fail(f"{start} should end at {want} with 200, got {show(chain)}")
            elif any(s not in PERMANENT for s, _ in chain[:-1]):
                fail(f"{start} uses a temporary redirect: {show(chain)}")
            else:
                print(f"  {start} -> {want} in {len(chain) - 1} hop(s)")

    for n in notes:
        print(f"  note: {n}")
    if fails:
        print(f"\nFAILED: {len(fails)} problem(s)")
        for f in fails:
            print(f"  - {f}")
        sys.exit(1)
    print("\nPASSED")


if __name__ == "__main__":
    main()
