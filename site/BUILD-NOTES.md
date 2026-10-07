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

## Launch checklist

1. **Vercel.** Done. Production deploys from `main`, confirmed September 29, and PR 5 merged the Manifest v7 build into `main` that day. The project serves `website/` from this repository with no build step.
2. **Domains.** Add `www.summervilleaccidentattorney.com` as the primary domain and the bare domain as a redirect. The `vercel.json` host rule also sends the bare domain to www. The launch runbook, kept with the kit outside git, has the steps.
3. **DNS.** The domain still points at the Coderrick site on SiteGround. SiteGround's nameservers (`ns1.siteground.net` and `ns2.siteground.net`) hold the zone, so the change is made in SiteGround's DNS Zone Editor. Change only the two web records, the bare domain and www. Leave MX, `mail`, SPF, DKIM, DMARC and the `google-site-verification` TXT record exactly as they are. Move DNS only after Daylin signs off on the Vercel preview.
4. **CallRail.** Done September 30. `CALLRAIL_SCRIPT` in `firm.py` puts CallRail's swap.js tag in the head of every page, and an empty value removes it. The pages carry `(843) 419-6653` in the format the swap matches. After DNS moves, confirm the number swaps on a page and a test call rings the office.
5. **Live check.** `python3 site/verify_live.py <base URL>` checks that every sitemap URL returns 200, every redirect in `redirects.json` lands with a 200, robots.txt and sitemap.xml load, an unknown URL returns 404, and every canonical sits on www with the right path. It passed against the Vercel preview on September 30. After DNS moves, run it against `https://www.summervilleaccidentattorney.com`. On the real domain it also checks that the bare domain and http end at https://www, including `http://summervilleaccidentattorney.com/practice-areas/car-accidents`, which should land on `/car-accident-attorneys-in-summerville/`.
6. **Search Console.** Submit `/sitemap.xml` and request indexing for the home page, the car accident parent, the Dorchester County page, the dog bite parent and the Spanish page.

## Open items for Daylin

- **Rule 7.2 and the fee line.** Resolved October 7, apart from one question. The footer and terms page now carry the client's approved fee wording. South Carolina Rule 7.2(f) says an ad with fee information must disclose whether the client owes any expenses in addition to the fee. The client's wording settles the case with no recovery, since the client never pays out of pocket. It does not say whether case costs come out of a recovery. One more sentence from the client, matching the fee agreement, would close that gap. This reading of 7.2(f) comes from a secondary copy of the rule, so check it against the official Rule 407 text.
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

## Blog cover images

The four September blog covers (`site/assets/img/cover-*.jpg`) are generated illustrations with no text, logos, plates or people, and the captions say so. Replace the files and rebuild to swap in real photos.

The four October 2026 posts use licensed Canva stock photos, placed in copies of Canva template DAHS3fxddsA and exported as 1920x1080 JPGs with no text, logos, plates or AI provenance data. Each file is named for the post's final CTA heading, and the caption, which is also the alt text, describes what the photo shows. A post's hero image is also its social card and BlogPosting image. Do not reuse these stock photos on another post.

| Post | File | Canva stock ID | Canva design |
| --- | --- | --- | --- |
| Summerville car accident medical bills | `talk-with-a-summerville-car-accident-lawyer-at-frost-law-group-today.jpg` | MAEWePdFnOY | DAHXR5r9A4c |
| Goose Creek motorcycle shared fault | `call-a-goose-creek-motorcycle-accident-lawyer-before-you-accept-a-reduced-offer.jpg` | MADAaSpIXVg | DAHXR69-77Q |
| Moncks Corner slip and fall liability | `talk-to-a-moncks-corner-slip-and-fall-lawyer-before-the-video-is-gone.jpg` | MAED4fviN6M | DAHXR_yiA7g |
| North Charleston truck claim value | `talk-to-a-north-charleston-truck-accident-lawyer-about-your-claims-value.jpg` | MAEEgDcNdaY | DAHXRzie3Po |
