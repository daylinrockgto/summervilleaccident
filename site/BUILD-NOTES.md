# summervilleaccidentattorney.com build notes

`website/` is generated from `site/` by `python3 site/build_site.py`. These notes are not published.

## Page Manifest v7, September 28, 2026

The site follows Nick Ryan's approved September 15 manifest plus the audit extras Daylin chose on September 28: the catastrophic injury and pedestrian parents, the distracted driving child, eight city pages, nineteen answer pages and a Spanish page. The full manifest with every slug, keyphrase and redirect is the project doc "Frost Law Group - Page Manifest and Redirect Map v7".

### Naming rules

- The H1 and the slug are the same string, lowercased and hyphenated.
- Parents use Attorneys and sit at the root. Children use Lawyers and nest under their parent.
- `/practice-areas/`, `/locations/` and `/questions/` are menu pages. Their H1s do not have to match their slugs.
- Answer pages use the question as the H1 and the slug, and the first paragraph answers it in 40 to 60 words.
- City pages are children of their county parent. Ladson sits under Berkeley County, because the Ladson census place lies in Berkeley and Charleston counties only.

### How each long-form page was made

1. Research from primary sources, stored with the page's sidecar facts: the South Carolina Code, SCDPS and SCDMV, the Department of Insurance, the courts, the Census Bureau and hospital and city sites.
2. A writer draft to the Legal Leads Group rules: search-style headings, short active sentences, no fee language in the copy, one free consultation offer in the final call to action, and the phone as `<a href="tel:+18434196653">(843) 419-6653</a>`.
3. The page gate, which checks headings against the plan, links, calls to action, banned words, grammar and 8-word overlap with every other page.
4. An independent legal and compliance review, then a fix pass and the gate again.

The fix logs sit outside the repository with the page drafts.

### Compliance rules the build enforces

`site/checks.py` fails the build on:

- the CallRail tracking number,
- any phone number other than `(843) 419-6653` in a `tel:+18434196653` link,
- workers' compensation content or links outside the legacy page,
- Georgia places,
- a retirement year for Jack Frost,
- "Judge Frost",
- specialist, expert, certified or authority language under Rule 7.4.

`build_site.py` also fails if a page offers estate planning, probate or criminal defense outside the one designed cross-link sentence.

## Decisions settled on September 28, 2026

- **Architecture.** Manifest v7, with the Sept 15 manifest plus the audit extras.
- **Fee line and reviews.** "No fee unless we win" stays in the template on every page, and the Google review quotes stay on the home and reviews pages. Page copy carries no fee language.
- **Workers' compensation.** `/practice-areas/workers-compensation/` keeps its old copy, title and description, and nothing links to it.
- **The car catastrophic child** became the root parent Catastrophic Injury Attorneys in Summerville. Its old address redirects there.

## Launch checklist

1. **Vercel.** The project serves `website/` from this repository with no build step. Confirm which branch the production deployment tracks, then merge this work into it.
2. **Domains.** Add `www.summervilleaccidentattorney.com` as the primary domain and the bare domain as a redirect. The `vercel.json` host rule also sends the bare domain to www.
3. **DNS.** The domain still points at the Coderrick site on SiteGround. Move DNS to Vercel only after Daylin signs off on the Vercel preview.
4. **CallRail.** The Dynamic Number Insertion script is not on the site yet. Add CallRail's swap script to the page head once Daylin supplies it. The pages already carry `(843) 419-6653` in the format the swap matches.
5. **Redirect test.** After DNS moves, `http://summervilleaccidentattorney.com/practice-areas/car-accidents` should land on `https://www.summervilleaccidentattorney.com/car-accident-attorneys-in-summerville/`. That one test exercises the host, HTTPS and redirect rules.
6. **Search Console.** Submit `/sitemap.xml` and request indexing for the home page, the car accident parent, the Dorchester County page, the dog bite parent and the Spanish page.

## Open items for Daylin

- **Rule 7.2 and the fee line.** "No fee unless we win" appears site-wide by decision. South Carolina's advertising rule expects a contingent-fee statement to say whether the client owes costs and expenses, on the same page as the statement. The footer on every page now repeats the terms page's cost sentence. The attorneys should confirm it matches their fee agreement.
- **Review quotes and the rating.** The home and reviews pages quote Google reviews. Structured data carries a 4.8 rating with a review count of 30. Confirm the count before launch, or remove it from `RATING` in `firm.py`.
- **Blog bylines.** The four blog posts carry Tara's and Jack's names. The attorneys should read and approve each post.
- **Bar numbers and admission years.** Both are blank, so the attorney markup carries none. Add them to `firm.py` when the client supplies them.
- **Available 24/7.** The top bar and footer repeat this approved live-site claim. Confirm the phone is answered after hours, or edit `PROMISES` in `firm.py`.
- **Spanish page.** It tells callers to ask what language help is available. It does not promise an interpreter or a Spanish-speaking staff member.
- **Capability statements.** Firm routines the client has not approved were rewritten as what a lawyer can do. The fix logs list the ones worth a quick client read.
- **Images.** Long-form pages run without hero photos for now. Canva images and alt text are pending.
- **Cross-site links.** The header and footer link to frostlawgroupsc.com for estate planning, probate and criminal defense, per the audit.

## Blog cover images

The four blog covers (`site/assets/img/cover-*.jpg`) are generated illustrations with no text, logos, plates or people, and the captions say so. Replace the files and rebuild to swap in real photos.
