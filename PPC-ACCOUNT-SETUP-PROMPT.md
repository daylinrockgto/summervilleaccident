# Prompt: set up the Google Ads account for Frost Law Group

Paste everything below the line into Claude, ChatGPT, or an agent that can operate Google Ads for you. It carries
every fact the assistant needs, the rules it must not break, and the order to work in. Replace the two
`[ ]` blanks first (daily budget, who owns the account). The two files it refers to, `PPC-CAMPAIGN.md` and
`PPC-ADS.md`, are in this repository; attach them to the conversation.

---

You are setting up a Google Ads search campaign for a small personal injury law firm. Work step by step, show me
each screen's exact values before I enter them, and stop and ask before anything that spends money or changes
billing. Do not invent facts about the firm. Everything you need is below or in the two attached files.

## The firm

- Frost Law Group, LLC, 128 Linwood Lane, Summerville, SC 29483. Phone (843) 419-6653, answered 24/7. Spanish spoken.
- Two attorneys, married. Tara L. Frost, a former Dorchester County Magistrate Judge (write it in the past tense,
  never "Judge Frost", never implying influence). Jack C. Frost, fourteen years with the Summerville Police
  Department and the Charleston County Sheriff's Office, a former detective (never a retirement year, never "inside
  access").
- Rated 4.8 stars on Google. That is the only proof point allowed. No review counts, case results, settlement
  figures, verdicts or client counts anywhere.
- Fee wording, which may be shortened in ads only to "No fee unless we win": "You never pay out of pocket. We only
  collect a fee if we recover compensation for you, so there's no risk in reaching out. If there is no recovery, you
  owe no fee and no case costs."
- Website: summervilleaccidentattorney.com (personal injury only). The firm's estate planning and criminal work is on
  a separate site and must never appear in these ads or keywords.

## The landing pages (already built, noindex, with Google Tag Manager and CallRail installed)

- Main lander: https://www.summervilleaccidentattorney.com/lp/summerville-car-accident/
  Append `?kw=` to swap the H1 per ad group. Allowed values: car-accident-lawyer, car-accident-attorney,
  auto-accident-lawyer, accident-lawyer, injury-lawyer, personal-injury-lawyer, car-wreck-lawyer,
  truck-accident-lawyer, motorcycle-accident-lawyer.
- Six sitelink pages under /lp/: about-frost-law, summerville-car-accident-faqs, free-case-review,
  injuries-we-handle, no-fee-unless-we-win, what-to-do-after-a-crash.
- The form is two steps (one tap, then name and phone). On success the page pushes a `lead_form_submit` event to
  the dataLayer. That event is the conversion. There is no thank-you page.
- Google Tag Manager container GTM-W8WTJ5RF is on every /lp/ page. CallRail's paid-search swap script is on every
  /lp/ page; the number must stay written as (843) 419-6653.

## Rules you must follow in every headline, description, callout and sitelink

- Never: specialist, specializes, expert, certified, authority, best, top, leading, premier, number one,
  award-winning, guaranteed, "we win", "first consultation", "initial consultation", "first meeting".
- Never a dollar figure, a review count, or a claim the landing page cannot back up.
- South Carolina only. Never Georgia or Savannah in targeting or copy.
- Never a workers' compensation keyword or ad.
- Use the ad copy in PPC-CAMPAIGN.md section 3 as written. If you propose a new line, keep it to 30 characters for a
  headline or 90 for a description and run it against the rules above before showing it to me.

## What to build, in this order

1. **Account.** Confirm the account is owned by `[ ]` and that the agency has manager access. Turn on
   auto-tagging. Link the Google Business Profile for 128 Linwood Lane.
2. **Conversions first.** Create "Lead form (PPC lander)" (Website, Submit lead form, count One, Primary, via
   Google Tag Manager) and "Call from ads" (60 seconds, Primary). Give me the Conversion ID and Label so I can add
   the Google Ads tag in GTM on the `lead_form_submit` custom event, plus a Conversion Linker tag. Then walk me
   through CallRail's Google Ads integration so website calls come back as a third Primary conversion.
3. **Campaign.** One Search campaign named "Search · Car Accident · Summerville" with the settings in
   PPC-CAMPAIGN.md section 1: Google Search only, search partners and Display off, Summerville + 15 miles +
   Dorchester and Berkeley counties, Presence only, English and Spanish, Maximize clicks with a $75 bid limit,
   daily budget `[ ]`, no broad match, campaign-level conversion goals set to the three above.
4. **Ad groups.** The six in section 2, with the keywords in phrase and exact match and the exact final URL
   (including `?kw=`) for each.
5. **Ads.** One responsive search ad per ad group from section 3, Headline 1 pinned to position 1 and Headline 2
   to position 2, nothing else pinned, paths `Car-Accident` / `Summerville`. Tell me the ad strength Google
   reports for each.
6. **Negatives.** The shared negative list "PI · not a client" from section 4, applied to the campaign.
7. **Assets.** Call, the six callouts, the structured snippet, location, the two image assets and all six
   sitelinks from section 5, with the exact description lines.
8. **Check before enabling.** Open every final URL and every sitelink URL on a phone and confirm the page loads,
   the form is above the fold and the phone number is tappable. Confirm the GTM tag fires in Preview mode when the
   form is completed. Then show me the launch checklist in section 8 with each item marked, and wait for my go-ahead
   before enabling the campaign.

## After launch

Set a reminder for day 3 and day 7 to review the search terms report and add negatives, and a day-14 review of
Quality Score by keyword. Do not change bidding strategy before 15 conversions, and do not raise the budget
without asking me. Report weekly in this shape: spend, clicks, average CPC, leads by source (form, call from ad,
call from site), cost per lead, and the search terms you added as negatives.
