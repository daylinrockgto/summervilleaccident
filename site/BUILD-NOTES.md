# summervilleaccidentattorney.com rebuild — build notes

`website/` is a complete, deployable rebuild of summervilleaccidentattorney.com generated from `site/` (`python3 site/build_site.py`). Copy changes go in `site/content/*.py`, not in the output. These notes are not published.

## What the audit asked for, and what the rebuild does

| Audit finding (Section 4 and Appendix C/D) | What the rebuild does |
|---|---|
| 17 removed pages still shown by Google, returning "not found" | Every one is 301-redirected to the closest new page (`REDIRECTS` in `firm.py`; applied in `vercel.json` and `.htaccess`). The city pages that earned most of the old impressions (Goose Creek, Mount Pleasant, North Charleston, Walterboro, Moncks Corner, Charleston, West Ashley) are rebuilt under `/areas/` |
| www and non-www both live; Google chose www | `www.summervilleaccidentattorney.com` is the only host. Every canonical, internal link and sitemap entry uses it; the apex host 301s to www (Vercel `has: host` rule; Apache rewrite) |
| One title tag across the site | Every page has its own title (≤ 70 characters) and description (≤ 160), following Appendix C, in `site/content/meta.py` |
| No city pages, no blog, no Spanish page | Nine community pages, four blog articles, one Spanish page (`/es/abogado-de-accidentes/`) |
| Weak "where are we" signals (13% of impressions from other Summervilles) | Full address, click-to-load map, county names and LegalService structured data on every page; Business Profile and main site linked in `sameAs` |
| Stock hero images hot-linked from Unsplash | The firm's own photos, self-hosted and optimized; no hot-linking |
| Car accidents are the volume; dog bites and motorcycle are closest to page one | Car accident hub with 14 answer pages (the audit's 12-spoke cluster plus the two top question searches); dog-bite hub expanded with the statute, children and homeowner's-insurance pages; motorcycle page retitled with the helmet-law page |
| Rideshare, drunk-driving-victim and delivery-driver searches with no page | `/practice-areas/rideshare-accidents/`, `/practice-areas/drunk-driving-accidents/`, `/practice-areas/car-accidents/delivery-driver-accidents/` |
| Review snippets and breadcrumbs already rich results | Kept, plus LegalService/Attorney, Person, Service, FAQPage, BlogPosting and BreadcrumbList JSON-LD on every page |

## The seven two-site rules, as implemented

1. **One subject per site.** This site has no page about estate planning, probate or criminal defense. `build_site.py` fails the build if any page mentions those services (or offers to defend a drunk driver) outside the one cross-link sentence defined in `firm.py` (`CROSS_LINK_TEXT`). The boundary the audit drew is kept: a crash caused by a drunk driver is an injury matter and lives here; the driver's charge is the main site's subject and is never offered here. On the main site, `/personal-injury/` and the old `/motor-vehicle-personal-injury` redirect here (see the matching change in the `frost-audit` repository).
2. **Say it is one firm.** Identical name, address and phone. The LegalService JSON-LD lists the main site, the Business Profile and Yelp in `sameAs`; each attorney's Person markup lists their main-site bio in `sameAs`; the bios link across.
3. **Cross-link in the header and footer with descriptive words.** Top bar: "Estate planning, probate & criminal defense →" to the main site. Footer: a labelled "Our main firm site" box with the same sentence. The about page and contact page repeat it in prose.
4. **The Business Profile links to the main site.** This site links *to* the profile (home, contact, reviews, footer) and does not claim it. TODO for the firm: list this site on Jack's and Tara's Avvo, Justia, FindLaw and Super Lawyers profiles, the LinkedIn company page and the YouTube channel.
5. **Separate content calendars.** The blog here is injury-only; the four articles are the start of the audit's one-per-week injury cadence.
6. **Route the brand.** The header says "A Frost Law Group practice"; the main site's home page carries an injury panel pointing here.
7. **Measure separately.** Two Search Console properties already exist. The `site` hidden field on the form and the "Injury site inquiry" subject line tag every lead from this site.

## Design

Same system as the main site (Fraunces and Public Sans, the navy palette, one ~26 KB stylesheet, no framework) so the two sites read as one firm, with a warmer rust accent, the three promises ("Free consultation · No fee unless we win · Available 24/7") in the top bar, hero and footer, a stats band, and the free-case-review form on every hub, community page, the Spanish page, the home page and the contact page. Practice pages use plain heroes; the county illustrations from the main site head the community pages.

## Facts to confirm before launch

1. **"Available 24/7."** The live site says it; the rebuild repeats it as "injury calls answered 24/7". Confirm the phone is actually answered after hours, or change `PROMISES` and `HOURS_DISPLAY` in `firm.py`.
2. **"$1M+ recovered" and "20+ years of combined experience"** from the live site are not repeated, because they could not be verified. Add them to the home stats band in `core.py` if the firm confirms them.
3. **Hospitals and police agencies** on the community pages (Summerville Medical Center, Trident Medical Center, Roper St. Francis Berkeley Hospital, MUSC, East Cooper Medical Center, Colleton Medical Center, Bon Secours St. Francis; the town police departments and the Highway Patrol) are named without street addresses. Confirm trauma-center levels and which agency the firm sees on reports from each town.
4. **The 2025 hands-free law.** The car-accident-laws and distracted-driving pages state that South Carolina passed a hands-free law in 2025 in addition to the 2014 texting ban. Confirm the effective date and citation and add it to `statutes` in `local_data.json`.
5. **Spanish-language service.** The Spanish page says the firm meets Spanish-speaking clients with a professional interpreter. Confirm, or edit `spanish.py`.
6. **Contact form.** Wired to the Formspree form `xdekonez` shared with the main site. Submissions carry the subject "Injury site inquiry: <case type>" and a hidden `site` field, so the two sites' leads are distinguishable in the inbox. Successful submissions land on `/thank-you/` (not indexed).
7. **Google review link.** Done: `REVIEW_URL` in `firm.py` is the Business Profile "write a review" link (place ID ChIJ4Vm83lNj_ogRDnS6XmVptVc), so the "Leave a Google review" buttons open the review box directly.
8. **Tara's judicial dates and Jack's retirement year** are as on the live site and the main site; Jack's law-enforcement timeline should be confirmed (the main site's notes flag the same question).
9. **Legal pages.** The privacy policy, terms and accessibility statement were drafted to match what the site does and the South Carolina advertising rules as we understand them; the attorneys should review all three.
10. **Videos.** The audit's page template calls for a short video on each hub and answer page. None exist yet; add a `VideoObject` block and an embed when they do.

## Deploying on Vercel

1. Import the GitHub repository; leave the framework as "Other". `vercel.json` serves the prebuilt `website/` folder with no build step, keeps trailing slashes, redirects the apex host to www and applies the redirect map.
2. Add `www.summervilleaccidentattorney.com` and `summervilleaccidentattorney.com` under Domains and make **www** the primary domain.
3. Point DNS at Vercel when ready. Until then the deployment is reachable at its `*.vercel.app` address.
4. After launch, check that `http://summervilleaccidentattorney.com/goose-creek/` lands on `https://www.summervilleaccidentattorney.com/areas/goose-creek/`. That single test exercises the host, HTTPS and redirect rules.
5. Submit `https://www.summervilleaccidentattorney.com/sitemap.xml` in the injury site's Search Console property and request indexing for the home page, the car-accident hub, the dog-bite hub, the Goose Creek page and the Spanish page (the audit's win-fast order).

## Deploying on SiteGround (or any Apache host)

Upload the contents of `website/` to the document root, including the hidden `.htaccess`, and make sure the previous site is no longer serving the root.

## Round two: answer pages from search and community research (September 17)

What the research showed, and what was built from it:

- **The competing Summerville pages are thin.** Gil Gatch's car-accident and dog-bite pages are about 630 words each; Shelbourne's whole home page is about 1,700; their blog posts are 370 to 920 words. Every hub and answer page here is 900 to 1,800 words with FAQ markup, statutes and local specifics. Depth is not the obstacle; authority and the map pack are (see below).
- **The local pack is the real competition** for "personal injury lawyer summerville sc": The Thumbs Up Guys (Nexton Square), Joye Law Firm (N. Main St) and Crantford Meehan / Steinberg hold the three map spots for every money search. Organic positions 4 to 9 are Shelbourne, Joye, Stanley, Super Lawyers, Gil Gatch and John Price. Getting into the pack means reviews, a complete Business Profile with the injury categories, and photos; the site cannot do that alone.
- **Zero-difficulty questions with real volume** that nobody local answers: "sc highway patrol accident reports" (390/mo), "south carolina accident reports" (260), "can you claim car accident without police report" (390, $42 CPC), "how long after a car accident can i claim injury" (260, $74 CPC), "how long after car accident can you go to hospital" (110), "what to do after a car accident not your fault" (2,400, KD 10), "what to do after a minor car accident" (590), "what happens after a car accident that is your fault" (260). Nine new answer pages target these, under `/practice-areas/car-accidents/`.
- **Reddit could not be reached from the build environment** (direct requests, the archive API and the fetch tool all blocked; agent-reach's own README says Reddit now requires a logged-in session). The new pages therefore link to the subreddit search pages (r/Charleston, r/SummervilleSC, r/southcarolina, r/legaladvice, r/Insurance), Nextdoor, and the Justia and Avvo South Carolina question boards, all `rel="nofollow"`. When a logged-in Reddit route is available, replace the search links with the specific threads.
- **`/questions/`** collects every FAQ on the site, grouped by topic, each linking to its page, with the community links above. It is in the main menu and the footer.

Facts to confirm from this round: the SCDMV collision-report fee (described only as "a small fee"); that the tri-county courts require mediation before trial (stated on the timeline page); the FR-10 layout description (the report number "near the top").

## Blog cover images

The four blog covers (`site/assets/img/cover-*.jpg`) were generated with OpenAI's image model to prompts that exclude text, logos, license plates and people. They are illustrations, not photographs of real places or vehicles, and the captions say so. Swap in real photos at any time by replacing the files and rebuilding. The firm's own photos are used everywhere else.
