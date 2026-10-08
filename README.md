# summervilleaccidentattorney.com, Frost Law Group's personal injury site

A static build of [summervilleaccidentattorney.com](https://www.summervilleaccidentattorney.com/), the personal injury practice of Frost Law Group, LLC in Summerville, South Carolina. The firm's estate planning, probate and criminal defense work lives on [frostlawgroupsc.com](https://frostlawgroupsc.com/).

The page structure follows Legal Leads Group's **Page Manifest v7** (September 28, 2026), which is Nick Ryan's approved September 15 manifest plus the extra pages the search audit called for. `CLAUDE.md` holds the hard rules, naming rules and settled decisions for anyone working in this repository.

## What is here

| Path | What it is |
|---|---|
| `website/` | The built site. 94 pages, plus `sitemap.xml` (93 URLs, everything except the thank-you page), `robots.txt`, `llms.txt`, `404.html` and an `.htaccess` for Apache hosts |
| `vercel.json` | Serves `website/`, keeps trailing slashes, sends the bare domain to www, applies the redirect map and sets asset caching. The build writes it |
| `site/build_site.py` | The generator. It writes `website/` and `vercel.json`, makes the 800px image copies and runs every check |
| `site/design.py` | Turns the long-form copy into a designed page at build time, with sections, H3 accordions, an "On this page" sidebar, photos and navigation cards. It never changes a word of copy |
| `site/checks.py` | Hard compliance checks. The build fails if any page breaks one |
| `site/verify_live.py` | Checks a deployed site. Every sitemap URL, every redirect, robots.txt, the sitemap, a 404 probe and the canonicals |
| `site/content/pages/` | The 74 long-form pages as plain HTML, plus `pages.json` with each page's id, slug, type, parent, keyphrase and H1. Both are written by `llg/v2/tools/sync_pages.py` from `llg/pages/`, so never edit them by hand |
| `site/content/llg.py` | Registers the long-form pages and builds the menus, sidebars and footer from `pages.json` |
| `site/content/images.json` | The photo map. Each long-form page's featured photo and the photo under each H2, with alt text and the Canva stock ID |
| `site/content/core.py` | Team, attorney bios, contact, reviews, blog index and the legal pages |
| `site/content/posts.py` | The eight blog posts |
| `site/content/questions_index.py` | The `/questions/` page, which links every answer page |
| `site/content/legacy.py` | The old workers' compensation page at its old address, linked from nowhere (Settled 2026-09-28). Never edit it |
| `site/content/redirects.json` | 82 old addresses and where each now points. 74 are from the old site, and 8 are the earlier `/blog/` post addresses |
| `site/content/firm.py` | Firm facts, phone, hours, the approved fee wording, each attorney's bar record, the CallRail tag, the form endpoint and the structured data inputs |
| `site/content/meta.py` | Titles and descriptions for the pages that are not long-form pages |
| `site/assets/site.css` | Every style. The page design work starts at the `Page design, October 2026` banner |
| `site/assets/img/` | Every image. The firm's own photos, the blog covers and 270 Canva stock photos for the long-form pages |
| `site/BUILD-NOTES.md` | How the pages are written and checked, the settled decisions, the launch checklist and the open items |
| `site/PHOTOS.md` | Every stock photo by page, with its file name and Canva stock ID |
| `llg/` | The page kit. `llg/pages/*.html` is the source of truth for long-form copy. `llg/README.md` explains the edit, check, sync and build workflow |

## Building

```bash
pip install pillow
python3 site/build_site.py
```

The build exits 1 on a hard compliance failure or a keyphrase cannibalization, and 0 when clean. A hard failure is any of these.

- The CallRail tracking number, or a phone that is not `(843) 419-6653` in a `tel:+18434196653` link
- Workers' compensation content or links outside the legacy page
- Georgia or Savannah places
- A retirement year for Jack Frost, or "Judge Frost"
- Specialist, expert, certified or authority language barred by Rule 7.4
- An estate planning, probate or criminal defense offer outside the one designed cross-link

It also warns on titles over 70 characters (90 on the home page), descriptions outside 60 to 160 characters, a page without exactly one H1, and an unresolved `[[token]]`. The one expected warning is the legacy workers' compensation description at 172 characters, which stays as it is by decision.

## Editing

- **Long-form copy.** Edit `llg/pages/<id>.html`, check it, sync it and build, as `llg/README.md` describes. The checker needs the kit zip, which is not in git.
- **Other pages.** Edit `site/content/core.py`, `posts.py` or `questions_index.py`. Their titles and descriptions are in `meta.py`.
- **Firm facts.** Edit `site/content/firm.py`.
- **Design.** Edit `site/design.py` and `site/assets/site.css`. Never change copy to fix a design problem.
- **Photos.** Add the file to `site/assets/img/`, update the page's entry in `site/content/images.json`, and update its row in `site/PHOTOS.md`.

Commit the source and the built output together, meaning `site/`, `llg/`, `website/` and `vercel.json`.

## Site map

- **Home** at `/`
- **Menu pages** at `/practice-areas/`, `/locations/` and `/questions/`
- **Nine practice parents** at the root, each "... Attorneys in Summerville". Car, truck, motorcycle, rideshare, slip and fall, dog bite, wrongful death, catastrophic injury and pedestrian
- **Twenty practice children** under their parents, each "... Lawyers in Summerville"
- **Nineteen answer pages**, eighteen under the car accident parent and one under the truck accident parent, each with its question as the H1 and a direct answer first
- **Eight county parents** at `/personal-injury-attorneys-in-{county}-county/`. Dorchester, Charleston, Berkeley, Colleton, Orangeburg, Beaufort, Georgetown and Williamsburg
- **Six county children** for car, truck and motorcycle crashes in Charleston and Berkeley counties
- **Eight city pages** under their counties. Charleston, North Charleston, Mount Pleasant and West Ashley under Charleston County. Goose Creek, Moncks Corner and Ladson under Berkeley County. Walterboro under Colleton County
- **Spanish page** at `/es/abogado-de-accidentes-de-carro-en-summerville/`
- **Firm and legal pages.** Our team at `/about/`, the two attorney bios, contact, reviews, the blog index, privacy, terms, accessibility and the thank-you page, which is not indexed
- **Eight blog posts** at the root, each with its title as the slug. `/blog/` is the blog index
- **The legacy workers' compensation page** at `/practice-areas/workers-compensation/`, linked from nowhere

## Deploying

Vercel serves `website/` straight from the repository with no build step. Production deploys from `main` at [summervilleaccident-pi.vercel.app](https://summervilleaccident-pi.vercel.app/) until DNS moves from SiteGround, and every other branch gets a preview. Work on a branch, open a pull request, and merge it once the build exits 0 and every check passes. `site/BUILD-NOTES.md` has the domain and DNS steps.
