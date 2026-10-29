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
2. A writer draft to the Legal Leads Group rules: search-style headings, short active sentences, no fee language in the copy, one free consultation offer in the final call to action, and the phone as `<a href="tel:+18432420821">(843) 242-0821</a>`.
3. The page gate, which checks headings against the plan, links, calls to action, banned words, grammar and 8-word overlap with every other page.
4. An independent legal and compliance review, then a fix pass and the gate again.

The fix logs sit outside the repository with the page drafts.

### Compliance rules the build enforces

`site/checks.py` fails the build on:

- the CallRail tracking number,
- any phone number other than `(843) 242-0821` in a `tel:+18432420821` link,
- workers' compensation content or links outside the legacy page,
- Georgia places,
- a retirement year for Jack Frost,
- "Judge Frost",
- specialist, expert, certified or authority language under Rule 7.4,
- a page with a case results block (`data-results`) that has lost the footer's "Prior results do not guarantee a similar outcome."

`build_site.py` also fails if a page offers estate planning, probate or criminal defense outside the one designed cross-link sentence.

## Decisions settled on September 28, 2026

- **Architecture.** Manifest v7, with the Sept 15 manifest plus the audit extras.
- **Fee line and reviews.** "No fee unless we win" stays in the template on every page, and the Google review quotes stay on the home and reviews pages. Page copy carries no fee language.
- **Workers' compensation.** `/practice-areas/workers-compensation/` keeps its old copy, title and description, and nothing links to it.
- **The car catastrophic child** became the root parent Catastrophic Injury Attorneys in Summerville. Its old address redirects there.

## Decisions settled on September 30, 2026

- **Review count.** The only proof point is "rated 4.8 stars on Google", with no count, and the site carries no rating markup.
- **Home hero photo.** The home hero keeps the photo of Tara and Jack with the comfort dogs.
- **CallRail.** The swap.js tag Daylin supplied runs in the head of every page.

## Decisions settled on October 7, 2026

Daylin confirmed these with the client on October 7.

- **Home page photos.** The home page keeps the firm's own photos, `couple-formal.jpg` in the intro and `client-meeting.jpg` in the call to action.
- **Closing photos.** Child, city and answer pages may keep closing with a person on the phone, as long as no exact photo repeats. No stock ID or file repeats anywhere on the site, and the near-duplicate scan finds no repeated photo.
- **Unused generated images.** `county-berkeley.jpg`, `county-charleston.jpg`, `county-colleton.jpg`, `county-dorchester.jpg` and `summerville-downtown.jpg` looked AI-generated and were used nowhere. They are deleted.
- **Fee wording.** The client's approved wording is "No Fee Unless We Win. You never pay out of pocket. We only collect a fee if we recover compensation for you, so there's no risk in reaching out." The client wrote it with an em dash, which became a comma under the house punctuation rules. It lives in `FEE_HEADLINE` and `FEE_TEXT` in `firm.py`, and it closes the footer disclaimer on every page and the Fees section of the terms page. It replaced the old cost sentence, which said a client may owe costs whether or not there is a recovery and so contradicted the client's wording. The promises row keeps "No fee unless we win" in sentence case to match "Free consultation" and "Available 24/7".
- **Blog bylines.** The attorneys approve the bylines on all eight posts.
- **Available 24/7.** Confirmed true. It stays in the promises row, the top bar and the footer.
- **Bar numbers and admission dates.** These come from each attorney's South Carolina Judicial Branch attorney directory record. Both attorneys are in Good Standing.
  - Tara Leigh Frost, Bar No. 100610, admitted November 13, 2012.
  - Jack Christian Frost, Bar No. 103633, admitted November 27, 2018.

  Both appear in `firm.py`, in the Education and credentials list on each bio, and in each attorney's Person structured data as the bar number and the admission date.

## Decisions settled on October 8, 2026

- **Blog URLs.** Daylin moved all eight posts out of `/blog/` to the root. A post's slug is its H1, lowercased, with apostrophes dropped, every other run of punctuation and spaces made one hyphen, and every word kept. `post()` in `posts.py` derives the slug from the H1 and stops the build if it matches an existing page, so a future post cannot drift from its title. `/blog/` stays as the blog index, and the Blog menu item, the footer link and the Home › Blog breadcrumb stay. No title, description, date or word of copy changed. The posts' `meta.py` keys moved to the new slugs, because `page()` silently falls back to older strings when a key is missing.
- **Blog redirects.** `redirects.json` gained one row for each old post address, so it holds 82 entries. 74 are from the old site, and 8 are the earlier `/blog/` post addresses. The posts had been live on the Vercel production URL since September, so their old addresses redirect even though they never reached the real domain. Four posts only lost `/blog/`. The four September posts also got new slugs that match their titles.

  | Old address | New address |
  | --- | --- |
  | `/blog/i-26-crash-summerville-who-writes-the-report/` | `/crash-on-i-26-near-summerville-who-writes-the-report-and-how-to-get-it/` |
  | `/blog/dog-bite-summerville-neighborhood-what-parents-should-know/` | `/a-dog-bite-in-a-summerville-neighborhood-what-parents-should-know/` |
  | `/blog/motorcycle-season-lowcountry-helmet-law-your-claim/` | `/motorcycle-season-in-the-lowcountry-the-helmet-question-and-your-claim/` |
  | `/blog/hit-by-an-uninsured-driver-goose-creek-your-own-policy/` | `/hit-by-an-uninsured-driver-in-goose-creek-your-own-policy-may-be-the-answer/` |
  | `/blog/how-does-a-summerville-car-accident-lawyer-get-your-medical-bills-paid/` | `/how-does-a-summerville-car-accident-lawyer-get-your-medical-bills-paid/` |
  | `/blog/what-can-a-goose-creek-motorcycle-accident-lawyer-do-if-you-were-partly-at-fault/` | `/what-can-a-goose-creek-motorcycle-accident-lawyer-do-if-you-were-partly-at-fault/` |
  | `/blog/who-can-a-moncks-corner-slip-and-fall-lawyer-hold-liable-for-your-fall/` | `/who-can-a-moncks-corner-slip-and-fall-lawyer-hold-liable-for-your-fall/` |
  | `/blog/how-does-a-north-charleston-truck-accident-lawyer-figure-out-what-your-claim-is-worth/` | `/how-does-a-north-charleston-truck-accident-lawyer-figure-out-what-your-claim-is-worth/` |

  The Manifest v7 documents in `llg/v2/` were updated the same day. They list all eight posts at their root URLs and the eight `/blog/` redirects, and `manifest_v2.py` regenerates `manifest.json` and `redirects.json` to match `site/content/redirects.json`.
- **Blog covers.** The four September covers were generated illustrations. Daylin had them replaced with licensed Canva stock photos, made the same way as the October covers, so the site carries no generated images. Their captions describe the new photos, and the "Blog cover images" table lists all eight covers.
- **One-hop redirects.** Vercel's `"trailingSlash": true` setting runs before every redirect, so an old address typed without its slash took two hops, first to add the slash and then to the new page. 82 of the 164 redirect checks took two. `vercel.json` now adds trailing slashes with the same two rules that setting generates, placed after the redirect map, so all 164 land in one permanent 308. Pages, files, the 404 page and the bare domain behave as before. The host rule also changed from `/:path*` to `/:path(.*)`, because Vercel compiles `/:path*` into a pattern that skips the bare home page and any path ending in a slash. `site/verify_live.py` now fails any redirect that takes more than one hop. Vercel previews are behind Vercel Authentication and the Vercel connector cannot open them, so the change was proved with Vercel's own route compiler (`@vercel/routing-utils` 6.6.0) against the built site, then on production.
- **Final QA decisions.** Daylin approved these from the final QA report the same evening.
  - **Contact form.** The "What happened?" list no longer offers "Injured at work", since Manifest v7 gives workers' compensation no form option.
  - **Tara's probate judgeship.** On the home page, the wrongful death parent, the fatal car accident page and the survival action page, her probate judgeship sat in the same section as probate court or settlement approval content. Those four passages now name only her Magistrate Judge service. Her bios, About and the other pages keep both judgeships.
  - **"First meeting".** The home H4 now reads "Filing Deadlines We Review in Your Free Consultation", and the rideshare parent tells a parent to "mention the child's age in the free consultation."
  - **Titles and descriptions.** Five titles and seven descriptions in `meta.py` changed (About, the I-26, Goose Creek uninsured, North Charleston truck and Moncks Corner post titles, and the dog bite post, About, Accessibility, I-26, Goose Creek uninsured, motorcycle season and Terms descriptions). Every title is 60 characters or fewer and every description 150 to 156. The seven keyphrase-only titles stay, because no call to action of two or more words fits under 60.
  - **About, Contact and Reviews.** About lost "This site is the firm's personal injury practice." and "This site covers personal injury." Reviews now says "so each client review is about work Tara or Jack did personally." The fee clauses on About and Contact are gone, because the template line and the footer carry the approved fee wording.
  - **hreflang.** The Spanish page and the English car accident parent name each other as `es` and `en`, with the English page as `x-default`. `llg.py` sets the pair.
  - **Share images.** Each long-form page's featured photo is its `og:image`, with its real width and height. The home page and the core pages keep the site card `og.jpg`. `share_photo()` in `build_site.py` picks the photo.
  - **From the blog.** The car accident, motorcycle and dog bite parents end with a "From the blog" card for the four posts that had only the `/blog/` link pointing to them. `FROM_BLOG` in `design.py` maps each parent to its posts, and a slug that stops matching a post fails the build. One post runs as a wide card, and two run side by side.
  - **News sources.** Local TV news (Live 5, ABC News 4) is approved as a source for posts, with followed links.
  - **Spanish interface.** The Spanish page's header, breadcrumb and footer stay in English until a Spanish reader approves the wording in `site/SPANISH-CHROME.md`, which is planned for after launch.
  - **After launch.** WebP copies of the photos with a JPG fallback (about 40% smaller, 48.8 MB down to 29.3 MB) go in their own pull request. CallRail's swap.js moved to just before `</body>` the same day, after Daylin asked for CallRail to be set up before launch and CallRail's own install guide named that spot. The number swap was tested on staging before and after the move. A test call still waits for DNS.
  - **Blogs project.** The post items (self-referential lines, "Here is" openers, "contact page" link text and the headline style) went to the Blogs project as a note.
  - **Launch.** Daylin's co-worker adds the domain and moves DNS once staging is ready. Claude does not add domains or change DNS for this site.
  - **Two small copy fixes.** On the "where car accidents happen" answer page, the H3 now reads "Does the US 17 Crash Figure for Dorchester County Mean Main Street?" instead of "...in the Dorchester Count...". The "what to do after a minor car accident" answer opens with 57 words instead of 61, after "If the crash only dented metal," became "If not,".
- **Long-form edits without the kit zip.** `sync_pages.py` needs only files that are in git, and `frost_check.py` runs every check except the sidecar check without the kit zip. A deletion-only edit adds no fact and needs no sidecar change, so the four Tara passages and the two "first meeting" lines went through the normal check, sync and build. Each page's checker output matched its run before the edit, apart from the word count, which stayed in band. A new fact still needs its sidecar entry, which needs the kit zip.

## Home page rewrite, October 11, 2026

Jon Kennedy replied to the launch email that the home page "went deep and mixed pages". Daylin found the copy awkward to read and asked for a rewrite under the legal SEO writer skill.

The old page ran 9,289 words, longer than every practice parent it links to. It repeated statute-level detail that the parent, child and answer pages already cover, such as Act 42, UIM stacking, Medicaid liens, probate approval, FR-10 forms, damages caps and crash counts by hour.

- **Headings.** Every H2 and Nick's locked tree are unchanged. The four Why Turn H3s and seven of the eight county H3s keep their wording. The Charleston H3 promised a cause the research cannot support, so it now reads "Charleston County Has the Most Serious Injury Collisions in South Carolina".
- **Removed H4s.** Seven deep H4s under Why Turn are gone: conflicting accounts, magistrate court limits, SCDMV report ordering, which police agency, Medicaid and Medicare repayment, damages, and probate court approval.
- **H4 pairs.** Two pairs remain. "Questions the Attorneys Ask When You Call About an Injury" is new, paired with "Work That Starts Once You Hire Frost Law Group". "Documents to Gather Before You Meet the Attorneys" pairs with "Filing Deadlines We Review in Your Free Consultation".
- **Copy.** Every paragraph is rewritten in short, active sentences, two to four to a paragraph. Each case type and county gets a summary at home-page depth and a link to the page that covers it.
- **Facts.** No new facts. Each fact comes from the September 30 page, the approved client facts, the county research pack or the attorney bios. Firm routines the client has not approved are written as what the attorneys "can" do.
- **Word band.** The home band is now 4,000 to 5,000 words, target 4,400, in `llg/plan/plan.json`, `plan.py` and Manifest v7. The parent band is 5,040 to 6,000, so the home page now routes to the parents instead of repeating them.
- **Review.** Five independent review lenses checked the draft: facts, South Carolina law, compliance, readability, and SEO and depth. A skeptic then tried to refute every finding. The confirmed findings were fixed, and a second round checked the revision. Two legal errors from the first draft were caught and fixed:
  - "No statute names a following distance" was too broad, because Section 56-5-1960 sets 500 feet behind fire apparatus. The page now says only Section 56-5-1930 names none.
  - Lyft log-on times do not show that a ride was accepted, and acceptance is what triggers the $1,000,000 tier.
- **Gate.** `frost_check.py home --grammar` prints CLEARED. No 8-word run is shared with another page, and no sentence runs past 25 words.
- **For the Monday structure review.**
  - Confirm the 4,000 to 5,000 band. The skill's home default is 6,000 to 8,000, and the September plan had 8,040 to 10,000.
  - Decide whether the home page should link the Pedestrian and Catastrophic Injury parents, which the home brief's link list predates.
  - Decide whether the locked case-type H4s and H5s should stay, since they share keyphrases with the parent pages.

## Review fixes, October 12, 2026

A co-worker reviewed the live site and sent ten items. Daylin answered the three that needed a decision the same day. Everything below is in the template, design and build layer. No page copy in `llg/pages/` changed, and every page's heading outline above the footer is unchanged.

- **Fee disclosure, Rule 7.2(f).** The footer and the terms page keep the client's wording and add `FEE_COSTS`, "If there is no recovery, you owe no fee and no case costs." It restates "You never pay out of pocket" for a case with no recovery. Rule 7.2(f) also asks whether a percentage fee is figured before or after expenses come out of a recovery. Later the same day the client confirmed the `FEE_COSTS` sentence word for word as verified fee wording. The client gave no before-or-after sentence, so `FEE_BASIS` stays empty. If the client adds one, put it in `FEE_BASIS` in `firm.py`, rebuild and merge.
- **Responsible attorney, Rule 7.2(d).** The footer on every page says "The attorney responsible for this website is Tara L. Frost, 128 Linwood Lane, Summerville, SC 29483." The terms page still names both attorneys as responsible for its content.
- **Retention, Rule 7.2(b).** `site/ADVERTISING-RECORD.md` logs every version that has run on the real domain, with its live window and commit, and how to rebuild an exact copy from git. Dated PDF snapshots went to Daylin for the firm's records.
- **Short inline form.** 52 pages carry a short free-case-review form after the intro, with name, phone, date of injury and what happened. They are the home page, the practice parents and children, and the county parents, county children and city pages. On the home page the form runs in its own band after the intro. Name and phone are required. It posts to the same Formspree form as the contact page, with the subject "Injury site inquiry: [page] page" and a `page` field naming the page it came from. Answer pages, menu pages, the Spanish page, posts and the core pages do not carry it. The inline script now handles every form on a page and restores each button's own label after an error.
- **Mobile call button.** Already in place. The phone and "Free case review" bar stays fixed to the bottom of every page at 760px and narrower.
- **Spanish.** Daylin confirmed that Spanish is spoken at the firm. The top bar says "Se habla español" and links the Spanish page. The firm markup carries `knowsLanguage` `["en", "es"]` and a ContactPoint with `availableLanguage` English and Spanish, because schema.org allows `availableLanguage` on a ContactPoint, not on LegalService itself. Every width still shows only what fits in full. Small laptops and tablets (721 to 1023px) show the cross-link, Se habla español and the phone. Phones show the promises and Se habla español, and the phone stays in the bar fixed to the bottom of the screen. The Spanish page still tells callers to ask what language help is available, and a Spanish reader can now make that direct.
- **Main site link.** frostlawgroupsc.com's home page card and its `/motor-vehicle-personal-injury/` redirect pointed at `/practice-areas/car-accidents/`, an old address this site redirects. Both now go straight to `/car-accident-attorneys-in-summerville/`. That site builds from `daylinrockgto/frost-audit` (PR 4).
- **Alt text.** The logo, the practice and county photo cards and the blog card covers had empty alt text, 507 images in all. The logo reads "Frost Law Group logo", each card photo carries its page's featured alt text from `images.json`, and each cover carries its caption. The logo and the card photos also carry `aria-hidden`, so a screen reader still reads each link as its visible label, as Final QA set it.
- **Footer labels.** The four footer column labels are plain text, not H2s, so the footer adds nothing to any page's heading outline. Each list takes its accessible name from its label. This supersedes the Final QA note that made them H2s.
- **Census figures.** Checked against the Census Bureau's Vintage 2025 subcounty file, `sub-est2025_45.csv`, which QuickFacts V2025 draws on. The Town of Summerville's 53,177, the Dorchester part's 44,724, the Berkeley part's 5,798 and the Charleston part's 2,655 all match. QuickFacts blocks automated requests from the cloud environment.

### Plan for Spanish truck and wrongful death pages

- Two pages beside `/es/abogado-de-accidentes-de-carro-en-summerville/`, each the Spanish version of an English parent. One pairs with `/truck-accident-attorneys-in-summerville/` and one with `/wrongful-death-attorneys-in-summerville/`.
- Proposed H1s and slugs, to confirm with Spanish keyword research, are "Abogado de Accidentes de Camión en Summerville" at `/es/abogado-de-accidentes-de-camion-en-summerville/` and "Abogado de Muerte por Negligencia en Summerville" at `/es/abogado-de-muerte-por-negligencia-en-summerville/`. "Muerte injusta" is the other common term, and the research decides.
- Each page is written in Spanish from the English parent's verified facts, not translated line by line. A Spanish reader reviews it, and it is checked against the compliance rules by hand, because `frost_check.py` does not run on Spanish pages.
- Each needs a `pages.json` row, an `images.json` entry, a title and description, and an hreflang pair with its English parent. `llg.py` pairs only the car pages today.
- They change the architecture, so Manifest v7 needs the two rows and Nick's approval. The Spanish interface wording in `site/SPANISH-CHROME.md` should land first or with them.

## Launch checklist

1. **Vercel.** Done. Production deploys from `main`, confirmed September 29, and PR 5 merged the Manifest v7 build into `main` that day. The project serves `website/` from this repository with no build step.
2. **Domains.** Done by October 9, 2026. `www.summervilleaccidentattorney.com` serves the site, and the bare domain answers with one permanent 308 to www. Daylin's co-worker handles the domain and DNS (decided October 8, 2026). Add `www.summervilleaccidentattorney.com` as the primary domain and the bare domain as a redirect. The `vercel.json` host rule also sends the bare domain to www. The launch runbook, kept with the kit outside git, has the steps.
3. **DNS.** Done by October 9, 2026. Over public DNS that day, the bare domain was `A 216.198.79.1` and www was `CNAME cfafbe9dc4928585.vercel-dns-017.com.`, both Vercel. MX, `mail`, `ftp`, SPF, DKIM, DMARC and the `google-site-verification` TXT matched the October 8 values below exactly. The notes that follow describe the zone before the move. The domain pointed at the Coderrick site on SiteGround. SiteGround's nameservers (`ns1.siteground.net` and `ns2.siteground.net`) hold the zone, so the change is made in SiteGround's DNS Zone Editor. Change only the two web records, the bare domain and www. Leave MX, `mail`, SPF, DKIM, DMARC and the `google-site-verification` TXT record exactly as they are. Move DNS only after Daylin signs off on the Vercel preview.

   Checked October 8, 2026 over public DNS. The bare domain and www are both A records to `35.212.103.239` (SiteGround). These stay exactly as they are: `mail` A `35.212.103.239`, `ftp` A `35.212.103.239`, the three MX records at `mx10`, `mx20` and `mx30.antispam.mailspamprotection.com`, the SPF TXT (`v=spf1 +a +mx include:summervilleaccidentattorney.com.spf.auto.dnssmarthost.net ~all`), the `default._domainkey` CNAME, the `_dmarc` TXT and the `google-site-verification` TXT. On that date Vercel recommended `A 216.198.79.1` and `A 64.29.17.1` for the bare domain and `CNAME cfafbe9dc4928585.vercel-dns-017.com.` for www. Use whatever values Vercel shows when the domain is added, since they can change. Neither domain is on a project in `daylinrockgtos-projects` yet. The live site's own sitemap lists 12 URLs, and every one either keeps its address or has a one-hop redirect.
4. **CallRail.** Done September 30. `CALLRAIL_SCRIPT` in `firm.py` puts CallRail's swap.js tag on every page, and an empty value removes it. Since October 8 it sits just before `</body>`, as CallRail's install guide says, so it no longer holds up the first paint. On October 8 the tag matched the snippet in CallRail's JavaScript Snippet page exactly (company 897987596), and on the Vercel production URL all nine phone links swapped for a visitor arriving from Google and stayed on the office number for a direct visit, because the tracking number's only source is Organic Search. The pages carry `(843) 242-0821` in the format the swap matches. On October 9, on the real domain, all nine phone links on the car accident parent swapped to the tracking number for a visitor arriving from Google and stayed on `(843) 242-0821` for a direct visit. Daylin's test calls the same day passed. A direct visit on a phone showed `(843) 242-0821`, and tapping it rang the Summerville office. From a private tab, a Google search and a tap on the site's organic result showed the tracking number, and tapping it also rang the office, so CallRail's forwarding works. CallRail keeps a visitor's first source, so a browser that first came in directly keeps the office number even after a later Google visit. A swap test needs a private tab. The test call should appear in CallRail's call log with Google Organic as its source.
5. **Live check.** `python3 site/verify_live.py <base URL>` checks that every sitemap URL returns 200, every redirect in `redirects.json` lands with a 200 in one hop, robots.txt and sitemap.xml load, an unknown URL returns 404, and every canonical sits on www with the right path. It passed against the Vercel preview on September 30. After DNS moves, run it against `https://www.summervilleaccidentattorney.com`. On the real domain it also checks that the bare domain and http end at https://www, including `http://summervilleaccidentattorney.com/practice-areas/car-accidents`, which should land on `/car-accident-attorneys-in-summerville/`. It passed against the real domain on October 9, 2026, with 93 of 93 pages and 164 of 164 redirects in one hop. That day every one of the 680 files in `website/` matched the live copy byte for byte. A browser pass at 390 and 1440 found no console errors, broken images or sideways scroll on any page, and Lighthouse scored 96 to 100 for performance and 100 for accessibility, best practices and SEO on the home page, the car accident parent, the Goose Creek page and Contact, phone and desktop. The bare domain and http add one hop each before an old address's own redirect, because Vercel upgrades http first and the host rule runs before the map. The old site's pages lived on www, so its indexed addresses still take one hop.
6. **Search Console.** Submit `/sitemap.xml` and request indexing for the home page, the car accident parent, the Dorchester County page, the dog bite parent and the Spanish page.

## Open items for Daylin

- **favicon.ico.** Added October 9, 2026. `write_favicons()` now also writes `/favicon.ico` (16, 32 and 48 px) in the same maroon "F" design as `favicon.svg`, and every page declares it before the SVG. Browsers that read SVG icons keep the SVG. Older Safari, Bing and crawlers that ask for `/favicon.ico` get the icon instead of a 404.
- **old.summervilleaccidentattorney.com.** On October 9 this name pointed at a WordPress copy of the old site on SiteGround (`35.212.126.2`). It redirected to `old.old.summervilleaccidentattorney.com`, which does not resolve, so it served no pages and could not compete with the new site. If the copy is kept, add a noindex or a password. If it is not needed, delete the copy and its DNS record.
- **Contact form test.** The form posts to Formspree form `xdekonez`, shared with the main site. On October 12, 2026 at 2:47 PM ET, one test went through the new short form on the live home page, named "LLG test, please ignore" with the subject "Injury site inquiry: Home page". Formspree answered 200 and the page landed on `/thank-you/`. Delivery still needs an inbox check at tara@frostlawgroupsc.com and legalleadsgroupformfills@gmail.com. The recipients are set in the form's settings in Formspree, which this repository cannot see.

- **Goose Creek motorcycle cover.** Done October 8. Daylin picked Canva stock photo MAHBjhWn0Ug, placed in design DAHXdy7RMrI (a copy of template DAHS3fxddsA) and exported at 1920x1080 with no AI provenance data. Canva's photo search blocks a cloud session's own browser, so from a cloud session the search runs on Daylin's PC through Desktop Commander, with Chrome headless in a separate profile (`chrome.exe --headless=new --user-data-dir=<temp profile> --virtual-time-budget=25000 --dump-dom "https://www.canva.com/photos/search/<query>/"`), and the `MA` stock IDs come from the photo links in the saved page. On October 12 that search got Cloudflare's "Just a moment" page until Chrome sent a normal user agent (`--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/<installed version> Safari/537.36"`). In PowerShell, run it through `Start-Process -Wait -RedirectStandardOutput <file>`, because `& chrome.exe` returns before the page is written. Each photo link carries a short description after the ID, such as `/photos/MAHKepgl7Xo-close-up-of-wooden-gavel-in-courtroom/`, which narrows the list before any preview. The Canva connector's `get-assets` previews any stock ID. Never use Canva's design generator, which returns AI images (C2PA "TrainedAlgorithmic"). Five unused generated designs from an earlier attempt sit in the Canva account (`DAHXdoLSeyU`, `DAHXdoyUd_4`, `DAHXdr_JrTQ`, `DAHXdqGaRec`, `DAHXdv5nlFk`) and can be deleted.
- **Spanish interface wording.** Waiting on a Spanish reader, and on the client for the fee wording and disclaimer. `site/SPANISH-CHROME.md` has the draft.
- **Rule 7.2 and the fee line.** On October 12 the footer and terms page gained `FEE_COSTS`, and the client confirmed it word for word the same day. That closes the no-recovery half of the question below. The client gave no before-or-after sentence, so `FEE_BASIS` stays empty unless the client adds one. Resolved October 7, apart from one question. The footer and terms page now carry the client's approved fee wording. South Carolina Rule 7.2(f) says an ad with fee information must disclose whether the client owes any expenses in addition to the fee. The client's wording settles the case with no recovery, since the client never pays out of pocket. It does not say whether case costs come out of a recovery. One more sentence from the client, matching the fee agreement, would close that gap. Daylin approved asking the client for that sentence on October 8. This reading of 7.2(f) comes from a secondary copy of the rule, so check it against the official Rule 407 text.
- **Review quotes and the rating.** Resolved September 30. The reviews page says "rated 4.8 stars on Google" with no review count, and the structured data carries no `aggregateRating`, because Google treats a business's own rating markup as self-serving. The review quotes stay by decision.
- **Blog bylines.** Resolved October 7. The attorneys approve the bylines on all eight posts.
- **Bar numbers and admission years.** Resolved October 7. Both are in `firm.py`, on the bios and in the attorney markup.
- **Available 24/7.** Resolved October 7. The client confirms it is true.
- **Spanish page.** It tells callers to ask what language help is available. It does not promise an interpreter or a Spanish-speaking staff member. Since October 12, Daylin has confirmed that Spanish is spoken at the firm, and the top bar says "Se habla español". A Spanish reader can update the page to say so directly.
- **Capability statements.** Firm routines the client has not approved were rewritten as what a lawyer can do. The fix logs list the ones worth a quick client read.
- **Images.** Done October 7, 2026. Every long-form page carries Canva stock photos with alt text, listed in `site/content/images.json`. The home page keeps the firm's own photos, which Daylin confirmed on October 7.
- **Home review quotes.** The home page shows three Google review quotes (Shannon D., Michelle F. and Kevin O.), per the September 28 decision, with the same disclaimer as the reviews page. None names an outcome or a dollar figure.
- **Cross-site links.** The header and footer link to frostlawgroupsc.com for estate planning, probate and criminal defense, per the audit.

## Page design, October 7, 2026

The long-form pages were one long block of text. `site/design.py` now turns their copy into a designed page at build time, without changing a word of `llg/pages/*.html`.

- **Hero.** Each long-form page shows its featured photo beside the H1, with the two buttons and the three template promises under it.
- **Intro.** The first paragraph is set larger. On answer pages it sits in a "The short answer" box, since it answers the H1 in 40 to 60 words. The phone paragraph sits in a call box.
- **Sections.** Each H2 opens a section with an id. The H2's photo sits directly under it.
- **Accordions.** Each H3, with its H4s and H5s, folds into an accordion. The `<summary>` keeps the real H3 element, so the heading outline search engines and screen readers see is unchanged. The Gold Law theme did the same, and Daylin kept it. A link to an H3 opens its accordion, and "Open all sections" opens every one. Printing opens them all. Blog posts read top to bottom, so their H3s stay open.
- **Call to action.** The last H2 renders as a navy panel with its photo and two buttons. Beside the sidebar the panel is narrow, so the photo sits above the text as a wide banner.
- **Sidebar.** The call box and an "On this page" list stay in view while you scroll, and the list marks the section on screen. On phones the list becomes a dropdown at the top of the page.
- **After the copy.** Hubs and children close with cards for both attorneys and photo cards for the parent's other pages, plus a list of the parent's answer pages.
- **Home.** Full-width bands, with each H2 beside its paragraphs, the practice area and county photo cards, both attorneys, three Google review quotes, and the firm's own photos (couple-formal.jpg in the intro, client-meeting.jpg in the call to action). The hero is unchanged.
- **Site-wide.** Two-column dropdowns for Practice areas and Locations, collapsible submenus in the phone menu, a reading bar under the header, a back-to-top button, and a phone and "Free case review" bar fixed to the bottom of phone screens. Blog cards show their cover photos.
- **Images.** `site/content/images.json` lists each long-form page's featured photo and the photo under each H2, by LLG page id, with alt text and the Canva stock ID. A file that is not in `site/assets/img/` yet is skipped with a warning. Every JPG wider than 900px also ships as an 800px copy, which `srcset` offers to phones.

### Page photos

The placement follows the plan in `llg/plan/plan.json` and LLG Part 8. Parent pages, meaning the practice and county parents and the two menu pages, get a featured photo plus one under every H2, the call to action included. About half of their alt texts carry the exact keyphrase. Child, city and answer pages get a featured photo plus one under the final H2, and every alt carries the keyphrase. Answer page keyphrases are full questions, so their alts carry the page's topic phrase instead, such as "statute of limitations".

Every photo is a licensed Canva stock photo, placed in a copy of template DAHS3fxddsA and exported at 1200x675 with no added text or logos, no readable plates and no AI provenance data. A few show ordinary road signs, such as a crosswalk button. No photo repeats anywhere on the site, and none shows a person who could be taken for the attorneys or staff. Each file name starts with the page's keyphrase and then describes the photo. `site/PHOTOS.md` lists every photo by page with its Canva stock ID and export design.

A visual review swapped three photos before launch. A New York taxi on the pedestrian page became a boy at a crosswalk button. A roadside memorial cross on the fatal car accident page became an empty country road at sunset. A scooter crash on a street outside the United States on the uninsured motorist motorcycle page became a wrecked motorcycle in roadside grass.

### Visual polish, October 2026

Daylin asked for a polish pass on October 7. Every change is in the design layer (`site.css`, `design.py` and the rendering functions in `build_site.py`). A text snapshot of all 94 pages shows no copy change beyond the removed hero captions.

- **Hero captions.** Blog posts, Our Team and both bios printed the photo's alt text in a white box over the hero photo. The box is gone. The alt text stays in the alt attribute, and the Our Team name cards keep their captions.
- **Home closing panel.** The firm photo was a small 4:3 picture floating in a tall navy panel. It now runs edge to edge across the top of the panel, anchored high so every face stays in frame, with the paragraphs in two columns under the heading. One column under 900px.
- **Top bar.** It cut off its text with an ellipsis on phones and small tablets. Each width now shows only what fits in full. Phones show the three promises, tablets show the cross-link and the phone number, and desktops show everything.
- **Promises.** Each promise stays whole when a line wraps, in the top bar, the footer and the sidebar. The check marks sit on the text line.
- **Home bands.** Each band heading lines up with the paragraph beside it and carries the gold section rule. The review names line up across the row.
- **Cards.** A card left alone on the last row of a navigation grid runs as a wide banner. The blog index shows the newest post as a wide card when eight posts would leave an empty cell.
- **Smaller fixes.** Breadcrumbs wrap as text. Wordmarks and short titles wrap in balanced lines. Phone buttons fill their row. The phone menu button text is centered. The white strip under the footer on phones is gone. Posts with no intro start level with the sidebar. The office photo on Our Team matches the other photos, and the team portraits sit two across on phones.

### Final QA, October 8, 2026

Daylin asked for a final visual, SEO and launch-readiness pass before launch. Every page was shot at 1280 and 390, one page of every type at 1440, 1024, 768 and 360, plus the menus, accordions, deep links, print, the 404 and the thank-you page. Every change below is in the design and build layer (`site.css`, `design.py` and `build_site.py`) or swaps an outbound link for the address it already redirects to. A text snapshot of all 94 pages shows no word changed, and the metadata snapshot shows no title, description, canonical or robots change. The new CSS sits at the end of `site.css` under the `Final QA, October 2026` banner.

- **Footer and sidebar promises.** The three promises stack one per line in the footer and the sidebar call card, so no line starts or ends on a separator dot. `promise_line()` puts each dot in its own `.dot` span.
- **Phone numbers and statute numbers.** A `tel:` link never breaks at its hyphen. `keep_together()` wraps statute numbers and form names (`38-77-140`, `FR-10`, `I-26`) in `.nw` spans inside `<main>`, plus any hyphenated word or month and day in a heading or contents entry. It leaves phone links alone so CallRail still finds the number as one piece of text.
- **Contents list.** A list too long for the sticky sidebar fades at its bottom edge, and the entry for the section on screen scrolls into view. Each entry's title sits in one span, so it stays one grid cell beside its number.
- **Deep links and print.** A link to an H3 lands with its accordion row clear of the sticky header. Printing opens every accordion (a `beforeprint` handler and `::details-content`), and headings stay with the photo under them.
- **Cards and bands.** The CTA band's two buttons stack at one equal width on wide screens. Under 921px the sidebar call card turns light, so it never sits as a second navy box under the page's own navy band. A wide last card asks for the full-size photo. When a parent has more than six children (Charleston County), each child's sibling cards are the five after it, wrapping round, so West Ashley shows up too.
- **Smaller fixes.** Contact hours line up flush right. Bio portraits keep the whole head. Short headings, question rows and buttons wrap in balanced lines, and breadcrumbs avoid a one-word last line. Related-post cards put the date and author on two lines. The mistakes list on the uninsured driver post and the limitations list on Accessibility use plain bullets instead of check marks.
- **Share card.** `og.jpg` keeps the standing attorney's face in frame, and its subtitle shrinks to fit, so the phone number is no longer cut off at the edge. Every page now sets `og:image:width`, `og:image:height` and `og:locale`.
- **Markup and accessibility.** The hero, with the H1, sits inside `<main>`, so the skip link lands on the page title. Footer headings are H2, and blog index cards are H2, so no outline skips a level. The back-to-top button sits inside the footer landmark. Review stars carry `role="img"`. The header logo link's accessible name is its visible wordmark. The main-site link in the footer box is underlined.
- **Links.** The frostlawgroupsc.com cross-link and the contact page's directions button open in a new tab like every other outbound link. The two LinkedIn profiles, the MUSC trauma page and the IIHS motorcycle page point at the address each one already redirected to.
- **Images.** The home hero and the blog post heroes offer the 800px copy to phones.
- **Structured data.** The firm markup no longer carries `priceRange`, which was never verified (LLG Part 14).
- **Tablet and narrow-phone widths.** A second pass at 1440, 1024, 768 and 360 found layout gaps the 1280 and 390 sweep could not show. On phones narrower than 390px the top bar's promises wrap with check marks instead of a dot ending a line. Review quotes never leave an empty cell: three across on wide screens, two on tablets with an odd last quote running full width, and two across on the reviews page. Photo card labels sit on a deeper shade. Nine practice cards run three across on tablets. A set of four help cards beside the sidebar runs two by two. The legal pages keep text at a readable line length. The bio hero shows the portrait at its own size on tablets and phones. The home intro portrait centers when the band stacks. Accordion titles fill their row before wrapping, and route numbers such as `US 278` stay whole. Contact details put the hours across the full width on tablets. The footer stays in two columns up to 1100px. Author and reviewer names in post bylines stay whole. The 404 page's breadcrumb reads Home, then Page not found, instead of Home twice.

## Blog cover images

All eleven blog covers are licensed Canva stock photos, placed in copies of Canva template DAHS3fxddsA and exported as 1920x1080 JPGs with no text, logos, plates or AI provenance data. The caption, which is also the alt text, describes what the photo shows. A post's hero image is also its social card and BlogPosting image. The post hero crops the cover to 4:3 on desktop and 16:10 on phones, and the cards show it at 16:9, so each subject sits near the center. Do not reuse these stock photos on another post or page.

The October posts' files are named for each post's final CTA heading. The four September posts have no CTA heading, so their files are named for the post's slug and then the subject. The September covers replaced generated illustrations on October 8, 2026. The Goose Creek motorcycle cover, a wrecked scooter (MADAaSpIXVg), became a parked sport motorcycle on a palm-lined plaza (MAHBjhWn0Ug) the same day, the photo Daylin picked. Its file name stayed the same, so anyone who viewed it on the Vercel production URL may need a hard refresh to see the new one, since `/assets/` files are cached for a year.

| Post | File | Canva stock ID | Canva design |
| --- | --- | --- | --- |
| Crash on I-26 near Summerville report | `crash-on-i-26-near-summerville-who-writes-the-report-and-how-to-get-it-wrecked-sedan-on-highway-shoulder.jpg` | MAGZanmWg9M | DAHXceP5LrE |
| Dog bite in a Summerville neighborhood | `a-dog-bite-in-a-summerville-neighborhood-what-parents-should-know-dog-barking-behind-iron-gate.jpg` | MAEEP3Y6VTw | DAHXceP5LrE |
| Motorcycle season and the helmet question | `motorcycle-season-in-the-lowcountry-the-helmet-question-and-your-claim-rider-in-helmet-on-wooded-road.jpg` | MAEEXHNkvqk | DAHXceP5LrE |
| Uninsured driver in Goose Creek | `hit-by-an-uninsured-driver-in-goose-creek-your-own-policy-may-be-the-answer-two-cars-after-collision.jpg` | MADlD2viOGg | DAHXceP5LrE |
| Summerville car accident medical bills | `talk-with-a-summerville-car-accident-lawyer-at-frost-law-group-today.jpg` | MAEWePdFnOY | DAHXR5r9A4c |
| Goose Creek motorcycle shared fault | `call-a-goose-creek-motorcycle-accident-lawyer-before-you-accept-a-reduced-offer.jpg` | MAHBjhWn0Ug | DAHXdy7RMrI |
| Moncks Corner slip and fall liability | `talk-to-a-moncks-corner-slip-and-fall-lawyer-before-the-video-is-gone.jpg` | MAED4fviN6M | DAHXR_yiA7g |
| North Charleston truck claim value | `talk-to-a-north-charleston-truck-accident-lawyer-about-your-claims-value.jpg` | MAEEgDcNdaY | DAHXRzie3Po |
| Charleston catastrophic injury, the insurance company's doctor | `talk-to-a-charleston-catastrophic-injury-lawyer-before-any-insurance-medical-exam.jpg` | MAAOa0EFmZU | DAHX1BoJyO4 |
| Ladson slip and fall, churches and charities | `talk-with-a-ladson-slip-and-fall-lawyer-before-the-charitys-insurer-calls.jpg` | MAHIU4GP-X0 | DAHYkHkKS1Q |
| Charleston dog bites, what happens to the dog | `call-a-charleston-dog-bite-lawyer-about-the-bite-not-the-dog.jpg` | MAHVUPwLXbI | DAHZJBxsDgQ |

### Photos inside a post

A post can carry a photo under any H2. `images.json` lists them under the post's slug, the same way it lists a long-form page's photos under its LLG id, and `page_images()` in `design.py` looks a post up by its slug. The cover stays in `hero_image`. The in-article photos are licensed Canva stock photos made the same way as the long-form page photos, placed in a copy of template DAHS3fxddsA and exported at 1200x675 with no AI provenance data. Each file name starts with the post's keyphrase and then describes the photo, and the alt text describes what the photo shows.

| Post | Place | File | Canva stock ID | Canva design |
| --- | --- | --- | --- | --- |
| Charleston catastrophic injury, the insurance company's doctor | Under H2 2 | `charleston-catastrophic-injury-lawyer-wooden-gavel-on-sound-block.jpg` | MAHKepgl7Xo | DAHX1GxzKWs |
| Charleston catastrophic injury, the insurance company's doctor | Under H2 4 | `charleston-catastrophic-injury-lawyer-doctor-writing-exam-notes.jpg` | MAEKANoVVAc | DAHX1GxzKWs |
| Ladson slip and fall, churches and charities | Under H2 1 | `ladson-slip-and-fall-lawyer-wet-floor-sign-on-wooden-floor.jpg` | MAG-LqQOYmA | DAHYkCgykoc |
| Ladson slip and fall, churches and charities | Under H2 5 | `ladson-slip-and-fall-lawyer-wooden-bleachers-beside-ball-field.jpg` | MAEEumGK6XA | DAHYkPntBn0 |
| Charleston dog bites, what happens to the dog | Under H2 2 | `charleston-dog-bite-lawyer-veterinarian-examining-labrador.jpg` | MAEe_r-RyoQ | DAHZJaL84zc |
| Charleston dog bites, what happens to the dog | Under H2 3 | `charleston-dog-bite-lawyer-dog-in-shelter-kennel-run.jpg` | MAHWfFy73hg | DAHZJaqhGDo |

## PPC landing pages (October 14)

A Google Ads lander, `site/landers/summerville-car-accident/index.html`, was built from an uploaded draft and rebuilt to the pattern used on results.goldbergloren.com. The build copies `site/landers/` to `website/lp/` after the normal pages, so `/lp/` survives the `rmtree` on every rebuild.

How the landers differ from the rest of the site:

- **Never indexed.** `<meta name="robots" content="noindex, nofollow">` on every lander, `X-Robots-Tag: noindex, nofollow` on `/lp/*` from `vercel.json` and from `.htaccess` (`SetEnvIf` + `Header set`), and nothing under `/lp/` in the sitemap or `llms.txt`. `robots.txt` must not block `/lp/`: Google only honours a noindex it can crawl, and AdsBot must reach the page or the ad group's landing-page experience falls to "below average".
- **Shared chrome, separate from the SEO template.** Every lander is assembled from `site/landers/_parts/` (head with the GTM snippet, header, call band, form, trust bar, reviews, fee band with a second form, footer with the sticky phone bar) through `[[LP_*]]` tokens, with one stylesheet and one script (`site/assets/lp.css`, `site/assets/lp.js`, served under a content hash). A change to the SEO site cannot break a running campaign, and a change to a part reaches every lander on the next build. The build checks each lander for the noindex tag, exactly one `<h1>`, the firm phone in both display and `tel:` form, leftover `[[` placeholders, the `CANNIBAL_RE` rule, and that every `/assets/` reference exists.
- **Conversion flow.** Two forms (hero and "No fee unless we win" band), both the two-step form from the Goldberg & Loren landers: step 1 is one tap ("Were you injured?", three answers), step 2 is name and mobile phone with an explicit consent checkbox, and success shows inline with a call button. The form posts JSON to the contact page's Formspree endpoint with `name`, `phone`, `injured`, `case_type`, `geo`, `variant`, `form`, and any `gclid`, `utm_*` and `kw` from the URL, then pushes `lead_form_submit` to `window.dataLayer`. That event is the Google Ads conversion. A filled honeypot shows success and sends nothing. Phone links push `call_click`; CallRail's swap script on both pages replaces the number for call tracking (keep the number written as `(843) 242-0821` so the swap matches).
- **Keyword match.** `?kw=car-accident-attorney` (and the other keys in the `KW` table in the page script) swaps the H1 so each ad group lands on its own headline. `PPC-ADS.md` maps ad groups to these URLs.
- **Approved wording is single-sourced.** The landers carry `[[DISCLAIMER]]`, `[[RESPONSIBLE_ATTORNEY]]`, `[[FEE_TEXT]]`, `[[FEE_COSTS]]` and `[[RATING]]` tokens that `write_landers()` fills from `firm.py`, so the fee band, the cost FAQ, the footer and the proof point stay word for word what the client confirmed. Every lander also runs through `checks.py`, and a hard failure there fails the build. The proof point is "rated 4.8 stars on Google" with no review count.
- **CallRail.** The landers carry the CallRail tag supplied with the PPC brief (company 571761726), not the organic-search tag in `firm.py`, so paid calls report in their own account.
- **Google Tag Manager.** Container `GTM-W8WTJ5RF` (`GTM_ID` in `firm.py`) is on every page of the site since October 14, 2026, in the head and as the noscript iframe. It went on the landers first and on the SEO pages the same evening, after Google's tag check scanned the home page and found no tag. Inside the container, LLG configured the Google tag `G-CP4MHK61GB` on all pages, the Google Ads conversion (`AW-18513854265`) on the landers' `lead_form_submit` event, and GA4 events for phone clicks and the `/thank-you/` page. The Google Ads conversion is configured inside the container on the `lead_form_submit` event.
- **Sitelink pages.** Six pages for the Google Ads sitelinks, each a conversion page in its own right: `/lp/about-frost-law/`, `/lp/summerville-car-accident-faqs/`, `/lp/free-case-review/`, `/lp/injuries-we-handle/`, `/lp/no-fee-unless-we-win/` and `/lp/what-to-do-after-a-crash/`. Each carries its own `data-variant`. Their facts come from the approved bios in `core.py` and the home page copy, the statutes cited on the page, and the client's fee wording; the fee page uses only that wording.
- **Photos.** The uploaded draft used AI-generated images: an invented attorney, a street sign for a Charleston address, a rendered dog. None are used. The hero photo is a crop of the firm's own `couple.jpg` (saved as `frost-team-lp.jpg`), and the office dogs photo is the real one. South Carolina Rule 7.1 treats a fabricated attorney photo as misleading, and Google Ads image assets must be real.

Verified locally with Playwright on desktop and phone: fonts load, no console errors, the `?kw=` swap works, a dry-run submission (Formspree intercepted) walks both steps, rejects a missing name, a bad phone number and an unticked consent box, shows the inline success with the `lead_form_submit` event, and the honeypot path shows success without posting.

## Phone number change (October 14)

The firm's number changed to (843) 242-0821. `PHONE` and `PHONE_E164` in `firm.py` carry it, the 74 long-form pages were changed in `llg/pages/` and synced, the landers and their shared parts, the contact page title and description, `checks.py`, `frost_check.py`, `verify_live.py`, `make_docs.py` and the docs all follow. The build output has no trace of (843) 419-6653. CallRail's number swap matches the displayed number, so the swap target in both CallRail accounts (organic and paid search) and the Google Business Profile must be changed to (843) 242-0821 for call tracking and the NAP match to hold.

## Case results (October 29)

Dustin Douglas (LLG Customer Experience) sent "Case Settlements.xlsx" on October 29, 2026 as case wins for Tara, and Daylin had them added to the home page and the PPC landers the same day. The sheet has 67 rows of "Net Settlement Proceeds" with a case type, and Daylin confirmed that the column is each case's total settlement. `site/content/results.py` holds 66 of them in the sheet's order, to the cent, and asserts that every figure shown is one of those rows.

- **Left out.** The one workers' compensation row ($50,000), because the site carries no workers' compensation content (settled September 28).
- **Counted but not shown.** The medical malpractice row ($200,000) and the insurance claim row ($366,408.22). They are real results, so they count toward the total, but the site markets neither, so they get no card.
- **Home page.** A navy band right under the hero. "More than $7.4 million recovered for our clients" (the 66 rows total $7,431,445.41), then $2,202,000 and $850,000 wrongful death, $500,000 car accident and $350,000 slip and fall settlements. The sheet calls the $350,000 case "Premises liability", and Daylin confirmed it was a slip and fall, so `CASE_LABELS` in `results.py` labels that one row. Any other premises row would read "Unsafe property settlement" until the firm says what kind of case it was. The title is a styled paragraph, not an H2, so the page's heading outline stays as written, and the section is labelled by it for screen readers.
- **Landers.** `[[LP_RESULTS]]` sits under the trust bar on all seven landers. `write_landers()` builds it from `results.py` rather than from `_parts/`, so the figures stay single-sourced. Every lander is a car accident ad, so it shows "More Than $3.1 Million Recovered for Car Accident Clients" (52 car rows, $3,167,462.19) and the $500,000, $325,000, $275,000 and $213,191 car accident settlements.
- **Labels.** Both bands open with the eyebrow "Selected case results", so the four figures read as chosen, not typical. On the landers the heading names car accidents, so each card says only "Settlement". The heading keeps "$3.1 Million" on one line with a non-breaking space.
- **Rounding.** Totals round down to a tenth of a million after "More than", and figures drop cents, so no number reads higher than the sheet.
- **Rule 7.1(b) and (d)(4), with Comment [3].** Rule 7.1(b) bars ads that create unjustified expectations about results, and (d)(4) is the testimonial disclaimer. Comment [3] ties them together for results. South Carolina allows advertised results only with a clear and conspicuous statement that a result for one client does not necessarily mean similar results for others. Checked against the official Rule 407 text on sccourts.org (Rule 7.1, last amended August 10, 2016). The first version put that statement right under the figures in each band, with a note that the amounts are net settlement proceeds (before Daylin confirmed they are total settlements). Daylin had it removed on October 29, after being told the rule calls for it beside the results. The footer's "Prior results do not guarantee a similar outcome." is now the only disclaimer on those pages, and `checks.py` fails any page with a `data-results` block that loses it. If the firm wants the per-band statement back, one short line under the figures meets the rule, for example "Past results do not necessarily indicate similar results for other clients."
- **Pending legislation.** S. 821 and H. 5004 (2026) would make Consumer Affairs enforce extra disclosures beside any advertised settlement figure, including the fees and costs deducted from it. On October 29, S. 821's last action was a favorable committee report on March 3, 2026, H. 5004 was still in House Judiciary, and neither had passed. If either becomes law, each band needs a statement of the fees and costs beside its figures.
- **No structured data.** The results stay out of the JSON-LD.

Questions answered by Daylin on October 29:

- **What "net" means.** The "Net Settlement Proceeds" column is each case's total settlement, so the cards and totals name settlement amounts, not what a client took home.
- **Whose results.** All 66 rows are the firm's own injury cases for this site. The client sent them, through Dustin, for the home page and the landers.
- **The premises case.** The $350,000 case was a slip and fall, and its card says "Slip and fall settlement".

Still open:

- **Lander testimonials (for Daylin, not the client).** Before this change, the lander form and reviews band already quoted "My family settled our claim with this company following a car accident last year." A testimonial about a result falls under Rule 7.1(d)(4), and the lander footer is the only statement on those pages. That is worth raising with Daylin alongside the results decision.
