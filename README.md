# summervilleaccidentattorney.com, Frost Law Group's personal injury site

A static build of [summervilleaccidentattorney.com](https://www.summervilleaccidentattorney.com/), the personal injury practice of Frost Law Group, LLC in Summerville, South Carolina. The firm's estate planning, probate and criminal defense work lives on [frostlawgroupsc.com](https://frostlawgroupsc.com/).

The page structure follows Legal Leads Group's **Page Manifest v7** (September 28, 2026), which is Nick Ryan's approved September 15 manifest plus the extra pages the search audit called for.

## What is here

| Path | What it is |
|---|---|
| `website/` | The built site, 90 pages plus `sitemap.xml`, `robots.txt`, `llms.txt`, `404.html` and an `.htaccess` for Apache hosts |
| `vercel.json` | Serves `website/`, keeps trailing slashes, sends the bare domain to www, applies the redirect map and sets asset caching |
| `site/build_site.py` | The generator. It writes `website/` and `vercel.json` |
| `site/checks.py` | Hard compliance checks. The build fails if any page breaks one |
| `site/content/pages/` | The 74 long-form pages as plain HTML, plus `pages.json` with each page's slug, type, parent, title, description and keyphrase |
| `site/content/llg.py` | Registers those pages and builds the menus, sidebars and footer from `pages.json` |
| `site/content/core.py` | Team, attorney bios, contact, reviews, blog index and the legal pages |
| `site/content/posts.py` | The four blog articles |
| `site/content/questions_index.py` | The `/questions/` page, which links every answer page |
| `site/content/legacy.py` | The old workers' compensation page at its old address, unlinked (Settled 2026-09-28) |
| `site/content/redirects.json` | Every old address and where it now points |
| `site/content/firm.py` | Firm facts, phone, hours, form endpoint and structured data inputs |
| `site/content/meta.py` | Titles and descriptions for the pages that are not long-form pages |
| `site/BUILD-NOTES.md` | How the pages are written and checked, the launch checklist and the open items |

## Building

```bash
pip install pillow
python3 site/build_site.py
```

The build exits with an error if a page carries the CallRail tracking number, a phone number that is not `(843) 419-6653` in a `tel:+18434196653` link, workers' compensation content outside the legacy page, anything about Georgia, a retirement year for Jack Frost, "Judge Frost", specialist or expert language barred by Rule 7.4, or an estate planning, probate or criminal defense offer outside the one designed cross-link. It warns on titles over 60 characters and descriptions outside 150 to 160.

## Editing a page

Page copy is written and checked outside the repository, then copied in. Edit the HTML in `site/content/pages/<id>.html` only for small corrections, keep every link and heading as it is, and rebuild. Headings must match the manifest, and the H1 and the slug are the same string.

## Site map

- **Home** at `/`
- **Menu pages** at `/practice-areas/`, `/locations/` and `/questions/`
- **Nine practice parents** at the root, each "... Attorneys in Summerville": car, truck, motorcycle, rideshare, slip and fall, dog bite, wrongful death, catastrophic injury and pedestrian
- **Twenty practice children** under their parents, each "... Lawyers in Summerville"
- **Nineteen answer pages**, eighteen under the car accident parent and one under the truck accident parent, each with its question as the H1 and a direct answer first
- **Eight county parents** at `/personal-injury-attorneys-in-{county}-county/`
- **Six county children** for car, truck and motorcycle crashes in Charleston and Berkeley counties
- **Eight city pages** under their counties: Charleston, North Charleston, Mount Pleasant and West Ashley under Charleston County, Goose Creek, Moncks Corner and Ladson under Berkeley County, and Walterboro under Colleton County
- **Spanish page** at `/es/abogado-de-accidentes-de-carro-en-summerville/`
- Team, two attorney bios, contact, reviews, blog with four articles, privacy, terms, accessibility and thank-you (not indexed)

## Deploying

Vercel serves `website/` straight from the repository with no build step. See `site/BUILD-NOTES.md` for the domain and DNS steps.
