# Frost Law Group injury site, summervilleaccidentattorney.com

This repository builds the personal injury website for Frost Law Group, LLC in Summerville, South Carolina. The work is done by Legal Leads Group (LLG), and Daylin Rockwood, Head of SEO, owns it. The client is a law firm, so every page is written for people who need legal help.

The firm's estate planning, probate and criminal defense work lives on a separate site, frostlawgroupsc.com. That site is never offered here except through the one designed cross-link in the header and footer.

## How This Repo Works

- **Generator.** `site/build_site.py` generates the static site into `website/` and writes `vercel.json`. Run `python3 site/build_site.py` after every change. It exits 1 on any hard compliance failure or cannibalization, and 0 when clean. It needs `pip install pillow`.
- **Commits.** Commit the source (`site/`, `llg/`) and the built output (`website/`, `vercel.json`) together. Vercel has no build step and serves `website/` exactly as committed.
- **Deploys.** Production is the `main` branch, served at summervilleaccident-pi.vercel.app, and at the real domain once DNS moves from SiteGround. Vercel also builds a preview for every other branch.
- **Branches.** Work on a branch and open a pull request. Never push to `main` directly. Claude merges its own pull request into `main` once `python3 site/build_site.py` exits 0 and every check passes. Merging publishes to staging, so never merge a failing build.
- **Long-form pages.** The 74 long-form pages come from `llg/pages/*.html`, synced into `site/content/pages/`. See `llg/README.md` for the edit, check, sync and build workflow. Never edit `site/content/pages/*.html` by hand.
- **Other pages.** Team, bios, contact, reviews, the blog index and the legal pages are in `site/content/core.py`. Blog posts are in `site/content/posts.py`. Their titles and descriptions are in `site/content/meta.py`. Firm facts, navigation defaults and the form endpoint are in `site/content/firm.py`. The redirect map is `site/content/redirects.json`.
- **Page design.** `site/design.py` turns the long-form copy into sections, H3 accordions, a table of contents, photos and navigation cards at build time. Page photos and their alt text are listed in `site/content/images.json`. The CSS is in `site/assets/site.css`. Never change copy to change the design.
- **Legacy page.** `site/content/legacy.py` is the old workers' compensation page, kept at its old address with its old copy and linked from nowhere. Never edit it and never link to it.
- **Build notes.** `site/BUILD-NOTES.md` has the launch checklist and the open items.

## Hard Rules

`site/checks.py` and `llg/tools/frost_check.py` enforce most of these. A page that breaks one is not deliverable.

**Phone**

- The phone is always `<a href="tel:+18434196653">(843) 419-6653</a>`. The display format is locked, because CallRail's number swap matches it.
- Never write the CallRail tracking number, (843) 983-2304, anywhere.

**Rule 7.4 and proof**

- Never write specialist, specializes, expert, certified or authority about the attorneys. Write "focuses on", "handles" or "practices in".
- No outcome promises. Never call the firm best, top, leading, premier, number one or award-winning.
- The only approved proof point is "rated 4.8 stars on Google", with no review count. There are no case results, settlements, verdicts or client counts.
- Daylin decided on 2026-09-28 to keep the Google review quotes on the home and reviews pages.

**Fees and the consultation**

- Page copy carries no fee language. The site template carries "No fee unless we win", and the footer carries the cost and expense disclosure.
- Never write "first consultation", "initial consultation" or "first meeting". The consultation is free and confidential, with no obligation.

**Tara Frost**

- Tara L. Frost is a former Dorchester County Magistrate Judge and a former Dorchester County Associate Probate Judge. Write it in the past tense, as courtroom perspective only.
- Never write "Judge Frost". Never imply influence or a better outcome.
- Never put her probate judgeship next to any probate court procedure or settlement approval.

**Jack Frost**

- Jack C. Frost spent fourteen years with the Summerville Police Department and the Charleston County Sheriff's Office.
- Never write a retirement year for him.
- Never claim inside access or police relationships.

**Geography and content**

- South Carolina only. No Georgia or Savannah places, courts or hospitals anywhere. Beaufort County needs extra care.
- No workers' compensation content or links anywhere.
- Do not lead injury pages with the comfort dogs.
- Every local detail must come from `llg/context/county-research-pack.md`, `llg/research/`, or a primary source recorded in the page sidecar. Never invent intersections, statistics, hospitals or courthouses.

## Naming Rules

- The H1 and the slug are the same string, lowercased and hyphenated.
- Parents use Attorneys and sit at the root, for example `/car-accident-attorneys-in-summerville/`.
- Children use Lawyers and nest under their parent.
- City pages are children of their county parent. Ladson sits under Berkeley County.
- Answer pages use the question as the H1 and the slug, and the first paragraph answers it in 40 to 60 words.
- `/practice-areas/`, `/locations/` and `/questions/` are menu pages. Their H1s do not have to match their slugs.
- SEO titles are the exact keyphrase, then `|`, then a call to action of two or more words, 60 characters or fewer.
- Meta descriptions run 150 to 156 characters and end in a call to action, with no phone number.

## Settled Decisions

- **2026-09-15. Slugs.** Nick Ryan approved the slugs, and the manifest is the controlling reference.
- **2026-09-15. Frost First.** "Frost First" is client approved for headings, metadata and CTAs.
- **2026-09-28. Architecture.** The site follows Page Manifest v7: the September 15 manifest plus 8 city pages, the Spanish car accident page, 19 answer pages, and the Pedestrian and Catastrophic Injury parents. Distracted Driving replaced the car catastrophic child. See `llg/v2/`.
- **2026-09-28. Fee line and reviews.** "No fee unless we win" and the Google review quotes stay.
- **2026-09-28. Workers' compensation.** The old page keeps its old copy at its old address, unlinked.
- **2026-09-29. Launch.** PR 5 merged the Manifest v7 build into `main`.

## Voice

Warm, plain-spoken and direct. The firm is two attorneys who grew up in Summerville and practice together, and a client reaches an attorney, not a call center. Write short, active sentences, and explain each legal term the first time it appears. Page copy uses no colons, semicolons, bullets or dashes as punctuation. `llg/context/WRITER-BRIEF.md` is binding for page copy.
