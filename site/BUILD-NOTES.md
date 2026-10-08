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

## Launch checklist

1. **Vercel.** Done. Production deploys from `main`, confirmed September 29, and PR 5 merged the Manifest v7 build into `main` that day. The project serves `website/` from this repository with no build step.
2. **Domains.** Daylin's co-worker handles the domain and DNS once staging is ready (decided October 8, 2026). Add `www.summervilleaccidentattorney.com` as the primary domain and the bare domain as a redirect. The `vercel.json` host rule also sends the bare domain to www. The launch runbook, kept with the kit outside git, has the steps.
3. **DNS.** The domain still points at the Coderrick site on SiteGround. SiteGround's nameservers (`ns1.siteground.net` and `ns2.siteground.net`) hold the zone, so the change is made in SiteGround's DNS Zone Editor. Change only the two web records, the bare domain and www. Leave MX, `mail`, SPF, DKIM, DMARC and the `google-site-verification` TXT record exactly as they are. Move DNS only after Daylin signs off on the Vercel preview.

   Checked October 8, 2026 over public DNS. The bare domain and www are both A records to `35.212.103.239` (SiteGround). These stay exactly as they are: `mail` A `35.212.103.239`, `ftp` A `35.212.103.239`, the three MX records at `mx10`, `mx20` and `mx30.antispam.mailspamprotection.com`, the SPF TXT (`v=spf1 +a +mx include:summervilleaccidentattorney.com.spf.auto.dnssmarthost.net ~all`), the `default._domainkey` CNAME, the `_dmarc` TXT and the `google-site-verification` TXT. On that date Vercel recommended `A 216.198.79.1` and `A 64.29.17.1` for the bare domain and `CNAME cfafbe9dc4928585.vercel-dns-017.com.` for www. Use whatever values Vercel shows when the domain is added, since they can change. Neither domain is on a project in `daylinrockgtos-projects` yet. The live site's own sitemap lists 12 URLs, and every one either keeps its address or has a one-hop redirect.
4. **CallRail.** Done September 30. `CALLRAIL_SCRIPT` in `firm.py` puts CallRail's swap.js tag on every page, and an empty value removes it. Since October 8 it sits just before `</body>`, as CallRail's install guide says, so it no longer holds up the first paint. On October 8 the tag matched the snippet in CallRail's JavaScript Snippet page exactly (company 897987596), and on the Vercel production URL all nine phone links swapped for a visitor arriving from Google and stayed on the office number for a direct visit, because the tracking number's only source is Organic Search. The pages carry `(843) 419-6653` in the format the swap matches. After DNS moves, confirm the number swaps on a page and a test call rings the office.
5. **Live check.** `python3 site/verify_live.py <base URL>` checks that every sitemap URL returns 200, every redirect in `redirects.json` lands with a 200 in one hop, robots.txt and sitemap.xml load, an unknown URL returns 404, and every canonical sits on www with the right path. It passed against the Vercel preview on September 30. After DNS moves, run it against `https://www.summervilleaccidentattorney.com`. On the real domain it also checks that the bare domain and http end at https://www, including `http://summervilleaccidentattorney.com/practice-areas/car-accidents`, which should land on `/car-accident-attorneys-in-summerville/`.
6. **Search Console.** Submit `/sitemap.xml` and request indexing for the home page, the car accident parent, the Dorchester County page, the dog bite parent and the Spanish page.

## Open items for Daylin

- **Goose Creek motorcycle cover.** Done October 8. Daylin picked Canva stock photo MAHBjhWn0Ug, placed in design DAHXdy7RMrI (a copy of template DAHS3fxddsA) and exported at 1920x1080 with no AI provenance data. Canva's photo search blocks a cloud session's own browser, so from a cloud session the search runs on Daylin's PC through Desktop Commander, with Chrome headless in a separate profile (`chrome.exe --headless=new --user-data-dir=<temp profile> --virtual-time-budget=25000 --dump-dom "https://www.canva.com/photos/search/<query>/"`), and the `MA` stock IDs come from the photo links in the saved page. The Canva connector's `get-assets` previews any stock ID. Never use Canva's design generator, which returns AI images (C2PA "TrainedAlgorithmic"). Five unused generated designs from an earlier attempt sit in the Canva account (`DAHXdoLSeyU`, `DAHXdoyUd_4`, `DAHXdr_JrTQ`, `DAHXdqGaRec`, `DAHXdv5nlFk`) and can be deleted.
- **Spanish interface wording.** Waiting on a Spanish reader, and on the client for the fee wording and disclaimer. `site/SPANISH-CHROME.md` has the draft.
- **Rule 7.2 and the fee line.** Resolved October 7, apart from one question. The footer and terms page now carry the client's approved fee wording. South Carolina Rule 7.2(f) says an ad with fee information must disclose whether the client owes any expenses in addition to the fee. The client's wording settles the case with no recovery, since the client never pays out of pocket. It does not say whether case costs come out of a recovery. One more sentence from the client, matching the fee agreement, would close that gap. Daylin approved asking the client for that sentence on October 8. This reading of 7.2(f) comes from a secondary copy of the rule, so check it against the official Rule 407 text.
- **Review quotes and the rating.** Resolved September 30. The reviews page says "rated 4.8 stars on Google" with no review count, and the structured data carries no `aggregateRating`, because Google treats a business's own rating markup as self-serving. The review quotes stay by decision.
- **Blog bylines.** Resolved October 7. The attorneys approve the bylines on all eight posts.
- **Bar numbers and admission years.** Resolved October 7. Both are in `firm.py`, on the bios and in the attorney markup.
- **Available 24/7.** Resolved October 7. The client confirms it is true.
- **Spanish page.** It tells callers to ask what language help is available. It does not promise an interpreter or a Spanish-speaking staff member.
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

All eight blog covers are licensed Canva stock photos, placed in copies of Canva template DAHS3fxddsA and exported as 1920x1080 JPGs with no text, logos, plates or AI provenance data. The caption, which is also the alt text, describes what the photo shows. A post's hero image is also its social card and BlogPosting image. The post hero crops the cover to 4:3 on desktop and 16:10 on phones, and the cards show it at 16:9, so each subject sits near the center. Do not reuse these stock photos on another post or page.

The four October posts' files are named for each post's final CTA heading. The four September posts have no CTA heading, so their files are named for the post's slug and then the subject. The September covers replaced generated illustrations on October 8, 2026. The Goose Creek motorcycle cover, a wrecked scooter (MADAaSpIXVg), became a parked sport motorcycle on a palm-lined plaza (MAHBjhWn0Ug) the same day, the photo Daylin picked. Its file name stayed the same, so anyone who viewed it on the Vercel production URL may need a hard refresh to see the new one, since `/assets/` files are cached for a year.

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
