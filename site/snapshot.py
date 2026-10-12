#!/usr/bin/env python3
"""PDF snapshot of one version of the site, for the Rule 7.2(b) advertising record (site/ADVERTISING-RECORD.md).

    python3 site/snapshot.py OUT.pdf                    # the website/ folder as built now
    python3 site/snapshot.py OUT.pdf --commit 42ba6a1   # the website/ folder at a commit, restored from git
    python3 site/snapshot.py OUT.pdf --commit 197a1bf --pages /    # only some pages

Each page prints at the 1280px desktop layout with screen styles, every accordion open and every image loaded. Each
sheet names the live URL, the version and the capture time, and the PDF has one bookmark per page. Photos are scaled to
640px for the archive copy, so a full set stays small enough to file; the full-size files stay in git at the commit.
Needs Node with Playwright (preinstalled in cloud sessions), Pillow and pypdf (pip install pillow pypdf).
"""
import argparse
import datetime
import functools
import hashlib
import http.server
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading

from PIL import Image
from pypdf import PdfReader, PdfWriter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE = "https://www.summervilleaccidentattorney.com"
PHOTO_MAX = 640

PRINT_JS = r"""
const { chromium } = require(process.env.PWMOD);
const fs = require('fs');
const [base, out, label, stamp, ...paths] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch(process.env.PWCHROME ? { executablePath: process.env.PWCHROME } : {});
  const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  await ctx.route(/calltrk\.com|google\.com\/maps|formspree\.io/, r => r.abort());
  const p = await ctx.newPage();
  await p.emulateMedia({ media: 'screen' });
  for (const [i, path] of paths.entries()) {
    await p.goto(base + path, { waitUntil: 'load', timeout: 60000 });
    await p.evaluate(async () => {
      document.querySelectorAll('img[loading=lazy]').forEach(img => img.loading = 'eager');
      document.querySelectorAll('details').forEach(d => d.open = true);
      await Promise.all([...document.images].map(img => img.complete ? 0 : new Promise(r => { img.onload = img.onerror = r; })));
      await document.fonts.ready;
    });
    await p.waitForTimeout(200);
    const head = `<div style="font:7px Arial,sans-serif;color:#555;width:100%;padding:0 .3in;display:flex;justify-content:space-between"><span>${process.env.LIVE}${path}</span><span>${label}</span></div>`;
    const foot = `<div style="font:7px Arial,sans-serif;color:#555;width:100%;padding:0 .3in;display:flex;justify-content:space-between"><span>Captured ${stamp}</span><span>Sheet <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`;
    await p.pdf({ path: `${out}/${String(i).padStart(3, '0')}.pdf`, format: 'Letter', printBackground: true, scale: 0.6, displayHeaderFooter: true,
                  headerTemplate: head, footerTemplate: foot, margin: { top: '0.45in', bottom: '0.45in', left: '0.25in', right: '0.25in' } });
  }
  await b.close();
})();
"""


def restore(commit, dest):
    """Extract website/ at a commit into dest/website."""
    tar = subprocess.run(["git", "archive", commit, "website"], cwd=ROOT, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", dest], input=tar, check=True)
    return os.path.join(dest, "website")


def shrink_photos(site):
    for name in os.listdir(os.path.join(site, "assets", "img")):
        path = os.path.join(site, "assets", "img", name)
        if not name.lower().endswith((".jpg", ".jpeg")):
            continue
        im = Image.open(path)
        if im.width > PHOTO_MAX:
            im = im.resize((PHOTO_MAX, round(im.height * PHOTO_MAX / im.width)), Image.LANCZOS)
        im.convert("RGB").save(path, "JPEG", quality=60, optimize=True, progressive=True)


def pages_of(site):
    """Every URL in the version's sitemap, plus the thank-you page, which the sitemap leaves out."""
    xml = open(os.path.join(site, "sitemap.xml"), encoding="utf-8").read()
    paths = [re.sub(r"^https?://[^/]+", "", u) for u in re.findall(r"<loc>([^<]+)</loc>", xml)]
    if os.path.exists(os.path.join(site, "thank-you", "index.html")):
        paths.append("/thank-you/")
    return paths


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve(site):
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=site))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--commit", help="snapshot website/ at this commit instead of the current build")
    ap.add_argument("--label", help="version label printed on every sheet")
    ap.add_argument("--pages", nargs="*", help="paths to print (default: every page)")
    args = ap.parse_args()
    work = tempfile.mkdtemp(prefix="snapshot-")
    try:
        if args.commit:
            site = restore(args.commit, work)
            sha = subprocess.run(["git", "rev-parse", "--short", args.commit], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        else:
            site = os.path.join(work, "website")
            shutil.copytree(os.path.join(ROOT, "website"), site)
            sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip() + " build"
        label = args.label or f"Version at commit {sha}"
        shrink_photos(site)
        paths = args.pages or pages_of(site)
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        httpd = serve(site)
        sheets = os.path.join(work, "sheets")
        os.makedirs(sheets)
        js = os.path.join(work, "print.js")
        open(js, "w", encoding="utf-8").write(PRINT_JS)
        env = dict(os.environ, LIVE=LIVE)
        env.setdefault("PWMOD", os.path.join(subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip(), "playwright"))
        if os.path.exists("/opt/pw-browsers/chromium"):
            env.setdefault("PWCHROME", "/opt/pw-browsers/chromium")
        subprocess.run(["node", js, f"http://127.0.0.1:{httpd.server_port}", sheets, label, stamp, *paths], env=env, check=True)
        httpd.shutdown()
        w = PdfWriter()
        for i, path in enumerate(paths):
            start = len(w.pages)
            w.append(PdfReader(os.path.join(sheets, f"{i:03d}.pdf")))
            w.add_outline_item(LIVE + path, start)
        w.add_metadata({"/Title": f"summervilleaccidentattorney.com, {label}", "/Subject": f"Rule 7.2(b) advertising record, captured {stamp}"})
        try:  # one copy of each photo and font the pages share
            w.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
        except TypeError:  # pypdf before 6
            w.compress_identical_objects(remove_identicals=True, remove_orphans=True)
        buf = io.BytesIO()
        w.write(buf)
        open(args.out, "wb").write(buf.getvalue())
        print(f"{args.out}: {len(paths)} pages, {len(w.pages)} sheets, {len(buf.getvalue()) / 1e6:.1f} MB, sha256 {hashlib.sha256(buf.getvalue()).hexdigest()}")
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
