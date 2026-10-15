# Google Ads campaign build sheet: Car Accident · Summerville

Everything needed to enter the first campaign into Google Ads, in the order the interface asks for it. The
reasoning behind each choice is in `PPC-ADS.md`; this file is the checklist. Fill the three blanks marked
`[ ]` before you start: the daily budget, the billing contact and who owns the Google Ads account.

## 0. Before the campaign

| Item | Value | Status |
|---|---|---|
| Google Ads account owner | `[ ]` the firm's Google account, with LLG added as a manager (MCC) | |
| Billing | `[ ]` the firm's card, monthly invoicing later | |
| Google Business Profile | Frost Law Group, 128 Linwood Lane, Summerville, SC 29483, linked to the Ads account | |
| Google Tag Manager | Container `GTM-W8WTJ5RF`, on every page of the site; Google tag `G-CP4MHK61GB` and the Ads conversion `AW-18513854265` are configured inside it | done |
| CallRail | Paid-search account (company 571761726), swap script on every `/lp/` page | done |
| Landing pages live | PR #30 merged and deployed; `/lp/summerville-car-accident/` answers with `X-Robots-Tag: noindex` | |
| Auto-tagging | Account settings → Auto-tagging → on | |
| Conversion actions | See section 6, before the campaign goes live | |

## 1. Campaign settings

| Setting | Value |
|---|---|
| Campaign name | `Search · Car Accident · Summerville` |
| Objective | Leads (or "create a campaign without guidance") |
| Type | Search |
| Networks | Google Search only. Search partners off. Display Network off |
| Locations | Summerville, SC (city) + 15 mi radius around 128 Linwood Lane + Dorchester County, SC + Berkeley County, SC |
| Location option | Presence: people in or regularly in your targeted locations (not "presence or interest") |
| Excluded locations | Savannah, GA; Georgia (state) |
| Languages | English, Spanish |
| Bidding, weeks 1–2 | Maximize clicks, max CPC bid limit $75 |
| Bidding, after 15 conversions | Maximize conversions, no target |
| Bidding, after 30 conversions in 30 days | Maximize conversions with a target CPA at the observed cost per lead |
| Daily budget | `[ ]` see section 7 |
| Ad schedule | All days, all hours. Bid adjustment −30% from 1:00 AM to 5:00 AM after week 2 |
| Devices | No adjustments to start |
| Ad rotation | Optimize |
| Broad match keywords | Off (the campaign-level toggle) |
| Brand restrictions | None |
| Conversion goals | Lead form (PPC lander), Call from ads, Call from website; account default goals off for this campaign |
| Final URL expansion | Off |
| Campaign URL options | Tracking template empty; auto-tagging handles `gclid` |

## 2. Ad groups, keywords and final URLs

Phrase and exact only. One theme per ad group. Default max CPC $60 under Maximize clicks (the bid limit above caps
it anyway).

### Ad group 1: car accident lawyer

Final URL: `https://www.summervilleaccidentattorney.com/lp/summerville-car-accident/?kw=car-accident-lawyer`

```
"summerville car accident lawyer"        [summerville car accident lawyer]
"car accident lawyer summerville sc"     [car accident lawyer summerville sc]
"car accident lawyer near me"            [car accident lawyer near me]
"car accident lawyers"                   [car accident lawyers]
"dorchester county car accident lawyer"
"car accident lawyer"
```

### Ad group 2: car accident attorney

Final URL: `…/lp/summerville-car-accident/?kw=car-accident-attorney`

```
"summerville car accident attorney"      [summerville car accident attorney]
"car accident attorney near me"          [car accident attorney near me]
"car accident attorney summerville"
"accident attorney summerville sc"
"car accident attorney"
```

### Ad group 3: auto accident lawyer

Final URL: `…/lp/summerville-car-accident/?kw=auto-accident-lawyer`

```
"auto accident lawyer"                   [auto accident lawyer]
"auto accident attorney"                 [auto accident attorney]
"auto injury lawyer"
"auto accident lawyer near me"
```

### Ad group 4: car wreck lawyer

Final URL: `…/lp/summerville-car-accident/?kw=car-wreck-lawyer`

```
"car wreck lawyer"                       [car wreck lawyer]
"car wreck attorney"
"wreck lawyer near me"
"car crash lawyer"                       [car crash lawyer]
"car crash attorney"
```

### Ad group 5: accident lawyer near me

Final URL: `…/lp/summerville-car-accident/?kw=accident-lawyer`

```
"accident lawyer near me"                [accident lawyer near me]
"accident attorney near me"              [accident attorney near me]
"accident lawyer summerville"
"accident lawyers"
```

### Ad group 6: injury lawyer

Final URL: `…/lp/summerville-car-accident/?kw=injury-lawyer`

```
"summerville injury lawyer"              [summerville injury lawyer]
"personal injury lawyer summerville"     [personal injury lawyer summerville]
"injury attorney near me"
"personal injury attorney summerville sc"
"injury lawyer near me"
```

## 3. Responsive search ads

One RSA per ad group. Pin Headline 1 to position 1 and Headline 2 to position 2; leave the rest unpinned.
Path 1 `Car-Accident`, Path 2 `Summerville`. Character counts are in brackets and computed; every line fits the limit of 30 for headlines and 90 for
descriptions. "Summerville Car Accident Lawyer" is 31 characters, which is why the pinned headline says "Near You"
and the page's `?kw=` H1 carries the city.

### Ad group 1: car accident lawyer (the master copy)

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

### The other five ad groups

Copy the master, then swap only these lines.

| Ad group | H1 (pin 1) | Other swaps |
|---|---|---|
| car accident attorney | `Car Accident Attorney Near You` [30] | none |
| auto accident lawyer | `Auto Accident Lawyer Near You` [29] | D1 → `Hurt in an auto accident near Summerville? Talk directly with attorney Tara Frost. Free.` [88] |
| car wreck lawyer | `Summerville Car Wreck Lawyer` [28] | H8 → `Hurt In A Car Wreck?` [20]; D1 → `Hurt in a Summerville car wreck? Talk directly with attorney Tara Frost. Free review.` [85] |
| accident lawyer near me | `Accident Lawyer In Summerville` [30] | H8 → `Hurt In An Accident?` [20] |
| injury lawyer | `Summerville Injury Lawyer` [25] | H8 → `Hurt In Summerville?` [20]; D1 → `Injured in Summerville? Talk directly with attorney Tara Frost. Free, confidential review.` [90] |

## 4. Negative keywords (campaign level, day one)

Add as one shared negative list named `PI · not a client` and apply it to every search campaign.

```
job, jobs, salary, hiring, paralegal, internship, law school, how to become, degree, career,
free legal aid, legal aid, pro bono, do it yourself, template, form, forms, pdf, sample letter,
accident report, police report, crash report, how to get, lookup, today, yesterday, news, obituary,
statistics, definition, what is, meaning,
criminal, dui, dwi, divorce, immigration, bankruptcy, workers comp, workers compensation,
insurance quote, insurance company, claims adjuster, adjuster jobs, repair, body shop, towing, rental,
columbia, greenville, myrtle beach, florence, spartanburg, rock hill, georgia, north carolina, savannah,
sued for, being sued, i hit, i rear ended, defense attorney, defend,
reviews of, complaints, cheap, cheapest, cost of a lawyer, how much does a lawyer charge
```

## 5. Assets (campaign level)

| Asset | Entry |
|---|---|
| Call | `(843) 242-0821`, call reporting on, count calls of 60+ seconds as conversions, show all hours |
| Callouts | `No Fee Unless We Win` · `Free Case Review` · `Open 24/7` · `Former Magistrate Judge` · `Se Habla Español` · `Local Summerville Office` |
| Structured snippet | Header **Types**: `Car Accidents`, `Truck Accidents`, `Motorcycle Accidents`, `Rideshare Accidents`, `Pedestrian Accidents`, `Wrongful Death` |
| Location | Link the Google Business Profile |
| Image | `https://www.summervilleaccidentattorney.com/assets/img/frost-team-lp.jpg` (the real team photo) and `office-exterior.jpg`. Never stock or generated people |
| Lead form | Do not add |

### Sitelinks (all six, campaign level)

| Sitelink text | Final URL | Description line 1 | Description line 2 |
|---|---|---|---|
| About Frost Law | `https://www.summervilleaccidentattorney.com/lp/about-frost-law/` | Former judge & former detective | One office in Summerville |
| Car Accident FAQs | `https://www.summervilleaccidentattorney.com/lp/summerville-car-accident-faqs/` | Deadlines, fault, no insurance | Answers from a local attorney |
| Free Case Review | `https://www.summervilleaccidentattorney.com/lp/free-case-review/` | An attorney calls you back | Free, confidential, no obligation |
| Injuries We Handle | `https://www.summervilleaccidentattorney.com/lp/injuries-we-handle/` | Whiplash to serious injuries | Talk with an attorney for free |
| No Fee Unless We Win | `https://www.summervilleaccidentattorney.com/lp/no-fee-unless-we-win/` | You never pay out of pocket | In writing before we start |
| What To Do After A Crash | `https://www.summervilleaccidentattorney.com/lp/what-to-do-after-a-crash/` | 8 steps that protect your claim | Then one call. We handle the rest |

## 6. Conversion tracking (do this before the campaign is enabled)

| Step | Where | What |
|---|---|---|
| 1 | Google Ads → Goals → Conversions → New | **Lead form (PPC lander)**: Website, category Submit lead form, count One, no value, click-through window 30 days, Primary. Choose "Use Google Tag Manager" and note the Conversion ID and Label |
| 2 | Google Ads → Goals → Conversions → New | **Call from ads**: Calls from ads using call assets, 60 seconds, Primary |
| 3 | CallRail → Integrations → Google Ads | Connect the paid-search CallRail account to the Ads account; it creates **Call from website** as a conversion. Mark it Primary, 60 seconds |
| 4 | GTM container `GTM-W8WTJ5RF` | Tag: Google Ads Conversion Tracking with the ID and Label from step 1. Trigger: Custom Event, event name `lead_form_submit`. Add the Conversion Linker tag on All Pages. Publish |
| 5 | GTM, optional | Second Google Ads tag on custom event `call_click`, as a Secondary conversion, so phone taps show in reports without inflating the primary count |
| 6 | Test | Open `/lp/summerville-car-accident/?gclid=test` in GTM Preview, complete the form with a real test name, confirm the tag fires on `lead_form_submit` and Formspree emails the lead. Then delete the test lead |

The `dataLayer` on every lander also carries `page_variant`, `h1_swap`, `lead_form_step` (the step-1 answer) and
`lead_form_error`. Each lead's Formspree email includes `gclid`, `kw`, `variant` and the step-1 answer.

## 7. Budget and the first thirty days

Legal car-accident clicks in South Carolina are expensive, and a budget below about five times the average
click price starves the campaign of data. Pick a tier and hold it for thirty days before judging.

| Tier | Daily budget | Monthly | What to expect |
|---|---|---|---|
| Learn | $75 | ~$2,300 | 1 to 2 clicks a day. Enough to read Quality Score, not enough to judge cost per case |
| Run | $150 | ~$4,600 | 2 to 4 clicks a day. The lowest tier at which cost per lead becomes readable in a month |
| Scale | $250+ | ~$7,600+ | Only after the Run tier shows a cost per signed case the firm is happy with |

Weekly:

1. Search terms report. Add negatives to the shared list. Promote converting terms to exact match in the right ad group.
2. Ad strength. Replace the two weakest unpinned headlines. Never touch the pinned keyword headline.
3. Lead quality. Mark each Formspree lead and CallRail call as case or no case. Move budget toward the ad group that produces signed cases.
4. Quality Score columns. Any keyword below 6 after two weeks moves to its own ad group or gets paused.
5. One landing-page test at a time (hero heading, form heading, button text), each with a new `data-variant` id on the page.

## 8. Launch checklist

- [ ] Conversion actions exist and the GTM tag fired in Preview (section 6)
- [ ] Auto-tagging on
- [ ] Campaign settings match section 1, search partners and Display off
- [ ] Six ad groups, keywords phrase + exact, final URLs with the right `?kw=`
- [ ] Six RSAs, H1 and H2 pinned, ad strength Good or better
- [ ] Shared negative list applied
- [ ] Call, callouts, snippets, location, image and six sitelinks added
- [ ] Every final URL opened on a phone: form above the fold, phone number tappable, no 404
- [ ] Daily budget set to the chosen tier, bid limit $75, Maximize clicks
- [ ] Billing active, campaign enabled, first search terms check scheduled for day 3
