# PPC playbook: Google Ads that convert and keep a high Quality Score

For Frost Law Group's personal injury ads on summervilleaccidentattorney.com. `PPC-CAMPAIGN.md` is the
enter-it-in-this-order build sheet and `PPC-ACCOUNT-SETUP-PROMPT.md` is a prompt that walks an assistant through
the account setup; this file is the reasoning. The landing pages live at
`/lp/<name>/` (source in `site/landers/`), are `noindex`, and post leads to the firm's Formspree form; the
`lead_form_submit` event the form pushes to the `dataLayer` on success is the conversion.

Current pages:

| Page | Final URL | Use for |
|---|---|---|
| Summerville car accident | `https://www.summervilleaccidentattorney.com/lp/summerville-car-accident/` | every car/auto accident ad group |

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
| car accident lawyer summerville | Car Accident Lawyer Near You | Summerville Car Accident Lawyer | Do I Have a Case? |
| car accident attorney near me | Car Accident Attorney Near You | Summerville Car Accident Attorney | Do I Have a Case? |
| auto accident lawyer | Auto Accident Lawyer Near You | Summerville Auto Accident Lawyer | Do I Have a Case? |

Everything else on the page is already aligned with the ad promises below: free case review, no fee unless we
win, 24/7, an attorney answers, former judge, local office, Se habla español.

## 4. Responsive search ad copy (ready to paste)

Google allows 15 headlines (30 characters) and 4 descriptions (90 characters). Pin only Headline 1 (the
keyword) and Headline 2 (the offer); leave the rest unpinned so Google can test combinations, which is what
gets an "Excellent" ad strength without hurting relevance. Character counts are in brackets and computed; every line fits the limit of 30 for headlines and 90 for
descriptions. "Summerville Car Accident Lawyer" is 31 characters, which is why the pinned headline says "Near You"
and the page's `?kw=` H1 carries the city.

### Ad group: car accident lawyer (the master copy)

```
H1  (pin 1)  Car Accident Lawyer Near You         [28]
H2  (pin 2)  Free Case Review, Open 24/7          [27]
H3           No Fee Unless We Win                 [20]
H4           Talk To Attorney Tara Frost          [27]
H5           Former Magistrate Judge              [23]
H6           An Attorney Answers Your Call        [29]
H7           Family Firm In Summerville, SC       [30]
H8           Hurt In A Car Accident?              [23]
H9           Never Pay Out Of Pocket              [23]
H10          Rated 4.8 Stars On Google            [25]
H11          Se Habla Español                     [16]
H12          Don't Talk To Their Insurer          [27]
H13          Former Detective On The Team         [28]
H14          Office On Linwood Lane               [22]
H15          Get Your Free Case Review            [25]

D1  Hurt in a Summerville car accident? Talk directly with attorney Tara Frost. Free review.    [88]
D2  No fee unless we win. A former magistrate judge and a former detective handle your case.    [88]
D3  Serving Summerville, Ladson, Nexton and Dorchester County. Call 24/7 for a free review.     [87]
D4  Don't give the insurer a recorded statement. Call Frost Law Group first. Free, 24/7.        [84]
```

### The other ad groups

Copy the master, then swap only these lines.

| Ad group | H1 (pin 1) | Other swaps |
|---|---|---|
| car accident attorney | `Car Accident Attorney Near You` [30] | none |
| auto accident lawyer | `Auto Accident Lawyer Near You` [29] | D1 → `Hurt in an auto accident near Summerville? Talk directly with attorney Tara Frost. Free.` [88] |
| car wreck lawyer | `Summerville Car Wreck Lawyer` [28] | H8 → `Hurt In A Car Wreck?` [20]; D1 → `Hurt in a Summerville car wreck? Talk directly with attorney Tara Frost. Free review.` [85] |
| accident lawyer near me | `Accident Lawyer In Summerville` [30] | H8 → `Hurt In An Accident?` [20] |
| injury lawyer | `Summerville Injury Lawyer` [25] | H8 → `Hurt In Summerville?` [20]; D1 → `Injured in Summerville? Talk directly with attorney Tara Frost. Free, confidential review.` [90] |

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
| Call | (843) 242-0821 with call reporting on; count calls of 60+ seconds as conversions |
| Sitelinks (6) | The six `/lp/` sitelink pages in the table below. Every one leads with a call button and a form |
| Callouts | No Fee Unless We Win · Free Case Review · Open 24/7 · Former Magistrate Judge · Se Habla Español · Local Summerville Office |
| Structured snippets | Types: Car Accidents, Truck Accidents, Motorcycle Accidents, Rideshare Accidents, Pedestrian Accidents, Wrongful Death |
| Location | Link the Google Business Profile (128 Linwood Lane) so the address and map pin show |
| Image | The real team photo (`/assets/img/frost-team-lp.jpg`) and the office. Never stock or AI-generated people |
| Lead form | Skip it. Google-hosted forms convert worse for injury intake and bypass the TCPA consent text |

### Sitelinks

Each sitelink has its own landing page under `/lp/`, built on the same chrome as the main lander (sticky phone, hero form, trust bar, reviews, fee band with a second form, sticky call bar on phones) so a click from any sitelink lands on a page whose only ways out are a call or the form. Sitelink text is 25 characters or fewer; each description line is 35 or fewer.

| Sitelink text | Final URL | Description line 1 | Description line 2 |
|---|---|---|---|
| About Frost Law | `/lp/about-frost-law/` | Former judge & former detective | One office in Summerville |
| Car Accident FAQs | `/lp/summerville-car-accident-faqs/` | Deadlines, fault, no insurance | Answers from a local attorney |
| Free Case Review | `/lp/free-case-review/` | An attorney calls you back | Free, confidential, no obligation |
| Injuries We Handle | `/lp/injuries-we-handle/` | Whiplash to serious injuries | Talk with an attorney for free |
| No Fee Unless We Win | `/lp/no-fee-unless-we-win/` | You never pay out of pocket | In writing before we start |
| What To Do After A Crash | `/lp/what-to-do-after-a-crash/` | 8 steps that protect your claim | Then one call. We handle the rest |

Use the full URL `https://www.summervilleaccidentattorney.com` + path. Add all six at the campaign level and let Google pick which to show; on phones it shows two to four. Leads from a sitelink page carry their own `variant` (`lp-about-v1`, `lp-faqs-v1`, `lp-review-v1`, `lp-injuries-v1`, `lp-nofee-v1`, `lp-steps-v1`) so the Formspree email and the `dataLayer` say which page converted.

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
- Shares nothing with the SEO template: one small stylesheet and one script for all the landers (`site/assets/lp.css`,
  `site/assets/lp.js`), two font files, the firm's photos, and no third-party scripts except Google Tag Manager and
  CallRail. Aim for Largest Contentful Paint under 2.5 s on 4G; check in PageSpeed Insights after every change.
- No navigation menu, no links that leave the page except the privacy policy.
- TCPA consent language under every form; no pre-checked boxes.

Clone it for a new case type or town by copying `site/landers/summerville-car-accident/` to a new folder,
changing `data-ct`, `data-geo` and `data-variant` on `<body>`, the H1, the local line and the FAQ, and rebuilding.
The shared chrome comes from `site/landers/_parts/` through `[[LP_HEAD]]`, `[[LP_BODY_OPEN]]`, `[[LP_CALLBAND]]`,
`[[LP_FORM|id|where|heading|subline|button]]`, `[[LP_TRUST]]`, `[[LP_REVIEWS]]`, `[[LP_FEEBAND]]` and `[[LP_FOOTER]]`,
so a change to the header, a form or the footer reaches every lander on the next build. The build checks every
lander for noindex, one H1, the firm's phone, the GTM snippet, a `#case-form`, the cannibalization words and the
hard compliance rules.

## 7. Conversion tracking

The form is the two-step form from the Goldberg & Loren landers: step 1 is one tap ("Were you injured?"), step 2
is name and mobile phone with an explicit consent box, and success shows inline with a call button. After Formspree
accepts the lead the page pushes `lead_form_submit` to `dataLayer` (with `form: hero|bottom` and the step-1
answer as `injured`); there is no thank-you page. Calls are tracked by CallRail (`swap.js` is on every `/lp/`
page). The landers carry the CallRail tag supplied with the PPC brief (company 571761726), which is a different CallRail account from the organic-search tag in `firm.py`; keep it that way so paid calls report separately, and keep the number written as `(843) 242-0821` so the swap matches.

Set up, in order:

1. In Google Ads, create a conversion action "Lead form (PPC lander)": type Website, category Submit lead form,
   count One, value none. Fire it from GTM on the `lead_form_submit` custom event. Mark it Primary.
2. Create "Call from ads" (Calls from ads using call assets, 60 seconds) and "Call from website" (CallRail's
   Google Ads integration sends qualified calls back as conversions). Mark both Primary.
3. Google Tag Manager container `GTM-W8WTJ5RF` is on every `/lp/` page (the id lives in `GTM_ID` in
   `site/content/firm.py`, and on every SEO page too). Inside the container, add a Google Ads conversion tag
   fired by a custom event trigger on `lead_form_submit`, and a second one on `call_click` as a secondary
   conversion. The `dataLayer` also carries `page_variant`, `h1_swap` and `lead_form_step` (the step-1 answer) for
   reporting, and `lead_form_error` for alerting.
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
- The approved proof points are "rated 4.8 stars on Google", with no review count, and the case results band on
  the landers, built from `site/content/results.py` (settled 2026-10-29). Keep settlement figures, recovery totals,
  verdicts and client counts out of the ads themselves, including headlines, descriptions and callouts.
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
    H2  Do I Have a Case?                                 (hero form, two steps)
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
    H2  Do I Have a Case?                                 (second form, "No fee unless we win" band)
    H2  Summerville Car Accident FAQs                     (6 questions, statutes cited)
```
