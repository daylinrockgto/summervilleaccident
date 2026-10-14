# PPC playbook: Google Ads that convert and keep a high Quality Score

For Frost Law Group's personal injury ads on summervilleaccidentattorney.com. The landing pages live at
`/lp/<name>/` (source in `site/landers/`), are `noindex`, and post leads to the firm's Formspree form; the
thank-you page at `/lp/thank-you/` is the conversion.

Current pages:

| Page | Final URL | Use for |
|---|---|---|
| Summerville car accident | `https://www.summervilleaccidentattorney.com/lp/summerville-car-accident/` | every car/auto accident ad group |
| Thank you | `https://www.summervilleaccidentattorney.com/lp/thank-you/` | conversion page; never a final URL |

Append `?kw=` to the final URL to make the H1 match the ad group (allow-listed values are in the page's
script): `car-accident-lawyer`, `car-accident-attorney`, `auto-accident-lawyer`, `accident-lawyer`,
`injury-lawyer`, `personal-injury-lawyer`, `car-wreck-lawyer`, `truck-accident-lawyer`,
`motorcycle-accident-lawyer`. Anything else leaves the default H1.

## 1. What Quality Score actually measures

Google scores each keyword 1–10 from three things, and the score sets both ad rank and what you pay
(roughly: your CPC = the next advertiser's ad rank ÷ your Quality Score + $0.01).

| Component | What Google looks at | What moves it |
|---|---|---|
| Expected CTR | How often people click your ad for that keyword vs. the position average | The keyword in the headline, a benefit, a number, a local signal, tight ad groups |
| Ad relevance | Does the ad text match the search | One theme per ad group; headlines that reuse the keyword's words |
| Landing page experience | Relevance, originality, transparency, speed, mobile usability, ease of navigation | The keyword in the H1 and title, a fast page, the form above the fold, a visible phone, privacy and contact details, no pop-ups |

Legal is one of the most expensive verticals in Google Ads, so a keyword at QS 7 vs. QS 4 is the
difference between a $60 and a $100+ click for the same position. Everything below is in service of
message match: the search → the headline → the H1 → the form all say the same thing.

## 2. Account structure

One campaign per case type and market so budgets, bids and reporting stay clean.

```
Campaign: Search · Car Accident · Summerville          (Dorchester + Berkeley County radius)
  Ad group: car accident lawyer                        → /lp/summerville-car-accident/?kw=car-accident-lawyer
  Ad group: car accident attorney                      → …?kw=car-accident-attorney
  Ad group: auto accident lawyer                       → …?kw=auto-accident-lawyer
  Ad group: car wreck lawyer                           → …?kw=car-wreck-lawyer
  Ad group: accident lawyer near me                    → …?kw=accident-lawyer
  Ad group: injury lawyer                              → …?kw=injury-lawyer
Campaign: Search · Brand                               (frost law group, tara frost, jack frost)
Campaign: Search · Truck Accident · Summerville        (clone the lander with CT = "truck-accident" first)
```

Rules that keep ad relevance high:

- 3 to 8 keywords per ad group, all sharing the same two or three root words.
- Phrase and exact match only to start. Add broad match later, only with a Max Conversions bid strategy and a
  strong negative list, and watch the search terms report weekly.
- Each ad group gets its own responsive search ad whose pinned Headline 1 contains the ad group's keyword.

### Keyword lists

Car accident lawyer ad group (phrase + exact):

```
"summerville car accident lawyer"        [summerville car accident lawyer]
"car accident lawyer summerville sc"     [car accident lawyer summerville sc]
"car accident lawyer near me"            [car accident lawyer near me]
"car accident lawyers"                   [car accident lawyers]
"dorchester county car accident lawyer"
```

Car accident attorney ad group:

```
"summerville car accident attorney"      [summerville car accident attorney]
"car accident attorney near me"          [car accident attorney near me]
"car accident attorney summerville"
"accident attorney summerville sc"
```

Auto accident lawyer ad group:

```
"auto accident lawyer"  "auto accident attorney"  "auto injury lawyer"  "auto accident lawyer near me"
```

Car wreck lawyer ad group:

```
"car wreck lawyer"  "car wreck attorney"  "wreck lawyer near me"  "car crash lawyer"  "car crash attorney"
```

Injury lawyer ad group:

```
"summerville injury lawyer"  "personal injury lawyer summerville"  "injury attorney near me"  "personal injury attorney summerville sc"
```

### Negative keywords (campaign level, add on day one)

These searches look like clients and are not. Each one you leave in drags expected CTR down and burns budget.

```
Jobs & school:   job, jobs, salary, hiring, paralegal, internship, law school, how to become, degree, career
Free / DIY:      free legal aid, legal aid, pro bono, do it yourself, template, form, forms, pdf, sample letter
Information:     accident report, police report, crash report, how to get, lookup, today, yesterday, news, obituary,
                 statistics, definition, what is, meaning
Wrong service:   criminal, dui, dwi, divorce, immigration, bankruptcy, workers comp (unless you run a WC campaign),
                 insurance quote, insurance company, claims adjuster, adjuster jobs, repair, body shop, towing, rental
Wrong place:     columbia, greenville, myrtle beach, florence, spartanburg, rock hill, georgia, north carolina, savannah
Defendants:      "sued for", "being sued", "i hit", "i rear ended", defense attorney, defend
Reviews/pricing: reviews of, complaints, cheap, cheapest, cost of a lawyer, how much does a lawyer charge
Other firms:     (add competitor names only if you decide not to bid on them)
```

Keep the "report" family negative. Those searches convert on the SEO site's answer pages, not on a paid lander.

## 3. Message match: keyword → headline → H1 → form

Write the ad after you open the landing page, not before. The first headline must be on the page, word for word
or close to it.

| Search | Pinned headline 1 | H1 the page shows (`?kw=`) | Form heading |
|---|---|---|---|
| car accident lawyer summerville | Summerville Car Accident Lawyer | Summerville Car Accident Lawyer | Free Summerville Case Review |
| car accident attorney near me | Summerville Car Accident Attorney | Summerville Car Accident Attorney | Free Summerville Case Review |
| auto accident lawyer | Summerville Auto Accident Lawyer | Summerville Auto Accident Lawyer | Free Summerville Case Review |

Everything else on the page is already aligned with the ad promises below: free case review, no fee unless we
win, 24/7, an attorney answers, former judge, local office, Se habla español.

## 4. Responsive search ad copy (ready to paste)

Google allows 15 headlines (30 characters) and 4 descriptions (90 characters). Pin only Headline 1 (the
keyword) and Headline 2 (the offer); leave the rest unpinned so Google can test combinations, which is what
gets an "Excellent" ad strength without hurting relevance. Character counts are in brackets.

### Ad group: car accident lawyer

Headlines

```
H1 (pin 1)  Summerville Car Accident Lawyer      [30]
H2 (pin 2)  Free Case Review, Open 24/7          [27]
H3          No Fee Unless We Win                 [20]
H4          Talk To Attorney Tara Frost          [27]
H5          Former County Magistrate Judge       [29]
H6          An Attorney Answers Your Call        [29]
H7          Local Family Firm In Summerville     [30]
H8          Hurt In A Car Accident? Call Now     [30]
H9          Never Pay Out Of Pocket              [23]
H10         4.8★ Rated On Google                 [20]
H11         Se Habla Español                     [16]
H12         Don't Talk To Their Insurer First    [30]
H13         Former Police Detective On Staff     [29]
H14         Office On Linwood Lane, Summerville  [30]
H15         Get Your Free Case Review Today      [30]
```

Descriptions

```
D1  Injured in a Summerville car accident? Speak directly with attorney Tara Frost. Free review.  [88]
D2  No fee unless we win. Former magistrate judge and former detective handle your case locally. [89]
D3  Serving Summerville, Ladson, Nexton & all of Dorchester County. Call 24/7 for a free review.  [88]
D4  Don't give the insurance company a recorded statement. Call Frost Law Group first. Free 24/7. [89]
```

### Ad group: car accident attorney

Swap H1 for `Summerville Car Accident Attorney` [33 — too long]. Use `Car Accident Attorney Summerville` [32 — too
long] … the 30-character limit bites, so use one of:

```
H1 (pin 1)  Summerville Accident Attorney        [29]
H1 alt      Car Accident Attorney Near You       [30]
```

and set `?kw=car-accident-attorney` on the final URL so the H1 on the page still reads "Summerville Car
Accident Attorney". Keep the rest of the headlines and all four descriptions.

### Ad group: auto accident lawyer

```
H1 (pin 1)  Summerville Auto Accident Lawyer     [30]
H2 (pin 2)  Free Case Review, Open 24/7          [27]
```

### Ad group: car wreck lawyer

```
H1 (pin 1)  Summerville Car Wreck Lawyer         [28]
H8 swap     Hurt In A Car Wreck? Call Now        [28]
D1 swap     Hurt in a Summerville car wreck? Speak directly with attorney Tara Frost. Free case review.  [89]
```

### Ad group: injury lawyer

```
H1 (pin 1)  Summerville Injury Lawyer            [25]
H1 alt      Personal Injury Lawyer, Summerville  [30]
```

### Display path

`summervilleaccidentattorney.com/Car-Accident/Summerville` — set Path 1 = `Car-Accident`, Path 2 = `Summerville`.
The display path is text only; the real final URL is the `/lp/` page.

### Writing rules the copy above follows

- The keyword is in Headline 1 and in Description 1.
- Every ad names one specific person (Tara Frost) and one specific credential (former judge). Specifics beat
  adjectives; "aggressive" and "experienced" are what every competitor says.
- One proof point per ad: rated 4.8 stars on Google (never with a review count), 24/7, 14 years in law enforcement, no fee unless we win.
- A local signal that proves the firm is really here: Linwood Lane, Dorchester County, Ladson, Nexton.
- A single call to action, "free case review", repeated on the page as the button text.
- Nothing the page can't back up. No settlement amounts, no "best", no "guaranteed", no "we win".

## 5. Ad assets (extensions)

Assets raise CTR without touching relevance. Add all of these at the campaign level.

| Asset | Content |
|---|---|
| Call | (843) 419-6653 with call reporting on; count calls of 60+ seconds as conversions |
| Sitelinks (4+) | What To Do After A Crash → `/car-accident-attorneys-in-summerville/what-to-do-after-a-car-accident-in-south-carolina/` · Meet Tara Frost → `/attorneys/tara-frost/` · Client Reviews → `/reviews/` · Free Case Review → `/lp/summerville-car-accident/#case-form` |
| Callouts | No Fee Unless We Win · Free Case Review · Open 24/7 · Former Magistrate Judge · Se Habla Español · Local Summerville Office |
| Structured snippets | Types: Car Accidents, Truck Accidents, Motorcycle Accidents, Rideshare Accidents, Pedestrian Accidents, Wrongful Death |
| Location | Link the Google Business Profile (128 Linwood Lane) so the address and map pin show |
| Image | The real team photo (`/assets/img/frost-team-lp.jpg`) and the office. Never stock or AI-generated people |
| Lead form | Skip it. Google-hosted forms convert worse for injury intake and bypass the TCPA consent text |

Sitelinks may point at the SEO site's pages; those pages are indexed and that is fine, the lander is the only
page that must stay noindex.

## 6. Landing page checklist (what `/lp/` already does, keep it that way)

- `noindex, nofollow` meta tag plus an `X-Robots-Tag` header on `/lp/*`. Never block `/lp/` in robots.txt: Google
  has to crawl the page to see the noindex, and AdsBot has to crawl it to score landing page experience.
- H1 matches the ad group keyword (`?kw=`), form above the fold on desktop and phone, phone number in the
  header, a tap-to-call band and a sticky call/review bar on phones.
- Real people and real photos (Tara, Jack, the dogs), real reviews quoted as written with first name and last
  initial, a real address and hours, the responsible attorney's name and bar number, privacy policy link.
- A local proof line with a cited statistic (SCDPS 2023 Fact Book) and FAQ answers that cite the statute.
- Self-contained: inline CSS, two font files, three images, no third-party scripts except CallRail. Aim for
  Largest Contentful Paint under 2.5 s on 4G; check in PageSpeed Insights after every change.
- No navigation menu, no links that leave the page except the privacy policy and sitelink targets.
- TCPA consent language under every form; no pre-checked boxes.

Clone it for a new case type or town by copying `site/landers/summerville-car-accident/` to a new folder,
changing `CT`, `GEO`, `VARIANT`, the H1 allow-list, the local line and the FAQ, and rebuilding. The build checks
every lander for noindex, one H1, the firm's phone and the cannibalization words.

## 7. Conversion tracking

The lander redirects to `/lp/thank-you/?geo=…&ct=…&variant=…&form=hero|bottom` after Formspree accepts the
lead, and the thank-you page pushes `lead_form_submit` to `dataLayer`. Calls are tracked by CallRail
(`swap.js` is on both pages). The landers carry the CallRail tag supplied with the PPC brief (company 571761726), which is a different CallRail account from the organic-search tag in `firm.py`; keep it that way so paid calls report separately, and keep the number written as `(843) 419-6653` so the swap matches.

Set up, in order:

1. In Google Ads, create a conversion action "Lead form (PPC lander)": type Website, category Submit lead form,
   count One, value none. Use the Google tag or GTM to fire it on a page view of `/lp/thank-you/` (or on the
   `lead_form_submit` event in GTM). Mark it Primary.
2. Create "Call from ads" (Calls from ads using call assets, 60 seconds) and "Call from website" (CallRail's
   Google Ads integration sends qualified calls back as conversions). Mark both Primary.
3. Put the GTM container id in the `GTM_ID` variable on both lander pages and rebuild; until then the pages push
   to `dataLayer` and nothing reads it.
4. Turn on auto-tagging (`gclid`). The lander stores `gclid`, `utm_*` and `kw` with every lead so the Formspree
   email shows which ad group sent it.
5. Read results by `variant`: every lead carries `variant: summerville-car-ppc-v1`. Change the variant id when you
   change the page so before/after is clean.

## 8. Bidding, budget, targeting

- Location: Summerville, SC plus a 15-mile radius, and the Dorchester and Berkeley County boundaries. Setting:
  "Presence" (people in or regularly in the area), not "Presence or interest".
- Schedule: all day. Bid −30% from 1 am to 5 am; the injury line is answered but conversion rates drop.
- Devices: start even; after 100 clicks, bid up the device with the better cost per lead (usually phone,
  because of calls).
- Bidding: Maximize Clicks with a max CPC cap for the first two weeks so Quality Score data accumulates, then
  Maximize Conversions, then a target CPA once there are 30 conversions in 30 days. Legal CPA in this market
  tends to land between $150 and $400 per lead; judge it against signed cases, not leads.
- Budget: a daily budget below 5× the average CPC starves the campaign. Start at $60 to $100 per day and watch
  "limited by budget" status.
- Search partners: off. Display expansion: off.

## 9. Diagnosing a low Quality Score

Check the three component columns (Google Ads → Keywords → Columns → Quality Score).

| Component below average | Likely cause | Fix |
|---|---|---|
| Expected CTR | Keyword too broad or ad too generic | Split the ad group, put the keyword in H1, add a number or a credential, add negatives |
| Ad relevance | Ad group mixes themes | Move the keyword to its own ad group with its own RSA |
| Landing page | Slow page, keyword not on page, mobile problems | Use the `?kw=` H1 swap, compress images, check PageSpeed, make sure the lander isn't blocked in robots.txt |

A new keyword sits at 6 to 7 with "—" components for a week or two; that is normal. React to data, not to day
three.

## 10. Weekly routine

1. Search terms report: add negatives, promote converting terms to exact match in the right ad group.
2. Ad strength and asset report: replace the two lowest-performing unpinned headlines; never touch the pinned
   keyword headline.
3. Lead quality: tag each Formspree lead as case / no case; move budget toward the ad groups that produce
   signed cases, not just forms.
4. Call recordings: listen to two or three; if callers ask about estate planning or criminal matters, add the
   negatives and check that the Business Profile's categories still lead with personal injury.
5. Landing page: PageSpeed check and one small test at a time (hero photo, form heading, button text) with
   a new `VARIANT` id.

## 11. Compliance (South Carolina attorney advertising)

The repository's `CLAUDE.md` hard rules apply to ad copy as much as to pages. In short:

- Every page carries the site's attorney-advertising disclaimer and the Rule 7.2(d) responsible-attorney line,
  filled in from `site/content/firm.py` at build time (the `[[DISCLAIMER]]` and `[[RESPONSIBLE_ATTORNEY]]` tokens).
- Rule 7.4: never "specialist", "specializes", "expert", "certified" or "authority" about the attorneys. Never
  "best", "top", "leading", "premier", "number one" or "award-winning". The build fails on the Rule 7.4(b) words.
- The only approved proof point is "rated 4.8 stars on Google", with no review count. No case results,
  settlement figures, verdicts or client counts anywhere, including headlines and callouts.
- Fee wording is the client's approved text from `firm.py` (`FEE_HEADLINE`, `FEE_TEXT`, `FEE_COSTS`), used word for
  word in the fee band, the cost FAQ and the footer. Do not paraphrase it in ads beyond "No fee unless we win".
- Never "first consultation", "initial consultation" or "first meeting". The case review is free and confidential.
- Tara Frost is a former Dorchester County Magistrate Judge, written in the past tense, never "Judge Frost", and
  never in a way that implies influence or a better outcome. Jack Frost spent fourteen years with the Summerville
  Police Department and the Charleston County Sheriff's Office; never a retirement year, never inside access.
- Local facts come from a primary source cited on the page (the SCDPS fact book) or the firm's research pack.
  Never invent intersections, statistics, hospitals or courthouses, in ads or on the page.
- Testimonials are real Google reviews quoted as written, with the reviewer's first name and last initial.
- No AI-generated or stock images presented as the attorneys or clients. The uploaded draft used a generated
  "attorney" photo; it was replaced with the firm's real photos for exactly this reason.
- Consent language under each form covers calls and texts (TCPA) and says consent is not a condition of hiring.
- Google Ads legal policy: no claims about guaranteed outcomes, and no targeting by sensitive categories.

## Appendix: heading outline of the lander

Use this as the template when a client asks for an H1/H2/H3 outline for a new page.

```
H1  Summerville Car Accident Lawyer                       (swaps with ?kw=)
    H2  Free Summerville Case Review                      (hero form)
    H2  Do You Have a Car Accident Case?
        H3  You were hurt
        H3  Someone else was at fault
        H3  There is insurance to pay
    H2  What to Do After a Car Accident in Summerville    (6 numbered steps)
    H2  Accidents We Handle                               (chips)
    H2  What You May Recover                              (6 damage types)
    H2  Why Summerville Families Call Frost Law Group
        H3  An attorney answers
        H3  A former judge and a former detective
        H3  A local family firm
    H2  What Clients Say                                  (3 Google reviews)
    H2  It's easy to get started                          (second form, "No fee unless we win" band)
    H2  Summerville Car Accident FAQs                     (6 questions, statutes cited)
```
