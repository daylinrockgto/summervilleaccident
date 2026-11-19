"""The South Carolina statewide Search campaign landers (Jon's November 19 handoff): 27 noindex PPC pages, one per
single-keyword ad group, rendered by build_site.write_landers() from site/landers/_sc/template.html into
/lp/sc/<geo>/<slug>/. Each page shares the lander chrome, form, tracking and footer with the Summerville landers; only
the H1, title, description, subhead, local block and (for truck pages) the body copy change.

Every local number comes from the SCDPS South Carolina Traffic Collision Fact Book 2024, Part VI (county tables) and
Parts II and V (statewide and commercial motor vehicle tables), read on 2026-11-19 from the PDF at FACT_BOOK_URL.
Roads are named from the same county tables (Top 5 Roadways and Top 5 Intersections). Every page says the firm's one
office is in Summerville (SC Rule 7.2) and never claims a local office or uses "near you" in body copy."""

FACT_BOOK_URL = "https://scdps.sc.gov/sites/scdps/files/Documents/ohsjp/2024%20Fact%20Book.pdf"
FACT_BOOK = "S.C. Department of Public Safety, South Carolina Traffic Collision Fact Book 2024"

CITIES = {"charleston": "Charleston", "columbia": "Columbia", "greenville": "Greenville", "myrtle-beach": "Myrtle Beach"}

# geo -> (data-geo, subhead, local paragraph with the source footnote, fact book citation detail)
GEOS = {
    "statewide": {
        "geo": "sc-statewide",
        "sub": "Frost Law Group represents crash victims across South Carolina from our office in Summerville.",
        "local": "Serving all of South Carolina, including I-26, I-95, I-85, I-77, I-20 and US 17. The state recorded 143,801 traffic collisions in 2024. They killed 1,040 people and seriously injured 2,618 more, 15,994 of them happened on an interstate, and 3,260 involved a commercial motor vehicle.",
        "cite": "Part I (143,801 collisions, 1,040 persons killed, 2,618 seriously injured), Part II, 2024 Collisions by Route Category (15,994 interstate collisions), Part V, Commercial Motor Vehicles (3,260 collisions)",
    },
    "charleston": {
        "geo": "charleston-sc",
        "sub": "Frost Law Group represents Charleston crash victims from our office in Summerville, South Carolina.",
        "local": "Serving Charleston and all of Charleston County, including I-26, I-526 and US 17. Charleston County recorded 15,802 collisions in 2024, second in the state, and its 241 serious injury collisions were the most of any county. US 17 alone had 1,805 collisions, I-26 had 1,213 and I-526 had 585.",
        "cite": "Part VI, Charleston County (15,802 total collisions, ranked 2nd, 241 serious injury collisions, ranked 1st, US-17 1,805, I-26 1,213 and I-526 585 collisions)",
    },
    "columbia": {
        "geo": "columbia-sc",
        "sub": "Frost Law Group represents Columbia crash victims from our office in Summerville, South Carolina.",
        "local": "Serving Columbia and Richland and Lexington Counties, including I-20, I-26, I-77 and I-126. Richland County recorded 12,068 collisions in 2024 and Lexington County 8,269. In Richland County, I-20 had 874 collisions and I-77 had 611. In Lexington County, I-26 had 1,059, the most of any road in the county.",
        "cite": "Part VI, Richland County (12,068 total collisions, I-20 874, I-77 611) and Lexington County (8,269 total collisions, I-26 1,059)",
    },
    "greenville": {
        "geo": "greenville-sc",
        "sub": "Frost Law Group represents Greenville crash victims from our office in Summerville, South Carolina.",
        "local": "Serving Greenville and all of Greenville County, including I-85, I-385, I-185, US 29 and Woodruff Road. Greenville County recorded 16,478 collisions in 2024, the most of any county in South Carolina, and its 82 fatal collisions were also the state's highest. I-85 had 1,143 collisions, US 29 had 827, and the I-385 interchange at Woodruff Road (SC 146) saw 99 on its own.",
        "cite": "Part VI, Greenville County (16,478 total collisions and 82 fatal collisions, both ranked 1st, I-85 1,143, US-29 827, SC-146 at I-385 99 collisions)",
    },
    "myrtle-beach": {
        "geo": "myrtle-beach-sc",
        "sub": "Frost Law Group represents Myrtle Beach crash victims from our office in Summerville, South Carolina.",
        "local": "Serving Myrtle Beach and all of Horry County, including US 17, US 501, SC 31 and SC 22. Horry County recorded 11,103 collisions in 2024, and they killed 59 people. US 17 had 1,821 collisions, the most of any road in the county, and US 501 had 1,462.",
        "cite": "Part VI, Horry County (11,103 total collisions, 59 persons killed, US-17 1,821, US-501 1,462 collisions)",
    },
}

# (slug, geo, H1, type, ad group / primary keyword). Slugs and H1s exactly as the handoff lists them.
PAGES = [
    ("car-accident-lawyer-south-carolina", "statewide", "Car Accident Lawyer in South Carolina", "car", "car accident lawyer south carolina"),
    ("car-accident-attorney-south-carolina", "statewide", "South Carolina Car Accident Attorney", "car", "car accident attorney south carolina"),
    ("auto-accident-lawyer-south-carolina", "statewide", "Auto Accident Lawyer in South Carolina", "car", "auto accident lawyer south carolina"),
    ("car-wreck-lawyer-south-carolina", "statewide", "Car Wreck Lawyer in South Carolina", "car", "car wreck lawyer south carolina"),
    ("car-accident-lawyer-near-me", "statewide", "Car Accident Lawyer Near Me in South Carolina", "car", "car accident lawyer near me, car accident attorney near me"),
    ("car-accident-lawyer", "statewide", "Car Accident Lawyer", "car", "car accident lawyer, accident lawyer, lawyer for car accident"),
    ("truck-accident-lawyer-south-carolina", "statewide", "Truck Accident Lawyer in South Carolina", "truck", "truck accident lawyer, semi truck, 18 wheeler, tractor trailer (SC)"),
]
for _slug, _city in CITIES.items():
    PAGES += [
        (f"car-accident-lawyer-{_slug}", _slug, f"Car Accident Lawyer in {_city}, SC", "car", f"car accident lawyer {_city.lower()}"),
        (f"car-accident-attorney-{_slug}", _slug, f"Car Accident Attorney in {_city}, SC", "car", f"car accident attorney {_city.lower()}"),
        (f"auto-accident-lawyer-{_slug}", _slug, f"Auto Accident Lawyer in {_city}, SC", "car", f"auto accident lawyer {_city.lower()}"),
        (f"car-wreck-lawyer-{_slug}", _slug, f"Car Wreck Lawyer in {_city}, SC", "car", f"car wreck lawyer {_city.lower()}"),
        (f"truck-accident-lawyer-{_slug}", _slug, f"Truck Accident Lawyer in {_city}, SC", "truck", f"truck accident lawyer {_city.lower()}, 18 wheeler, semi truck"),
    ]
assert len(PAGES) == 27


def url(slug, geo):
    return f"/lp/sc/{geo}/{slug}/"


def noun(h1):
    """The crash word the H1 uses, for the subhead question and the description."""
    for n in ("truck accident", "car wreck", "auto accident", "car accident"):
        if n in h1.lower():
            return n
    return "car accident"


def place(geo):
    return "South Carolina" if geo == "statewide" else f"{CITIES[geo]}, South Carolina"


def description(h1, geo, kind):
    what = "a truck or 18-wheeler crash" if kind == "truck" else f"a {noun(h1)}"
    where = "South Carolina" if geo == "statewide" else CITIES[geo]
    return f"Hurt in {what} in {where}? Free case review, no fee unless we win. Handled from our Summerville office. Call 24/7: (843) 242-0821."


FAQ_CAR = '''
 <details><summary>How long do I have to file a car accident claim in South Carolina?</summary><p>Usually three years from the crash to file a lawsuit.<sup><a href="#s2">2</a></sup> Claims against a city, county or state agency must be filed within two years.<sup><a href="#s3">3</a></sup> Evidence disappears much sooner, so call early.</p></details>
 <details><summary>What if I was partly at fault?</summary><p>You can still recover if you were 50% or less at fault. Your amount is reduced by your share of the blame, and once your share passes 50% there is no recovery.<sup><a href="#s4">4</a></sup></p></details>
 <details><summary>What does it cost?</summary><p>The case review is free. [[FEE_TEXT]] [[FEE_COSTS]]</p></details>
 <details><summary>Where is your office, and do I have to come to Summerville?</summary><p>Our one office is at 128 Linwood Lane, Summerville, SC 29483. No. Most clients outside Summerville meet with us by phone or video, and we can come to you if you are hurt.</p></details>
 <details><summary>What if the other driver had no insurance?</summary><p>Every South Carolina auto policy must include uninsured motorist coverage, so your own policy may pay.<sup><a href="#s5">5</a></sup> We review your policy for free and explain the options.</p></details>
 <details><summary>The insurance company already called me. What do I say?</summary><p>Give them your name and your attorney's number. Do not give a recorded statement or accept a quick check before you talk to a lawyer. A release ends your claim for good.</p></details>
'''

FAQ_TRUCK = '''
 <details><summary>How long do I have to file a truck accident claim in South Carolina?</summary><p>Usually three years from the crash to file a lawsuit.<sup><a href="#s2">2</a></sup> Claims against a city, county or state agency must be filed within two years.<sup><a href="#s3">3</a></sup> The carrier may lawfully discard driver logs after six months, so the real deadline for evidence is much sooner.<sup><a href="#s6">6</a></sup></p></details>
 <details><summary>Who is responsible after a truck crash, the driver or the company?</summary><p>Often both. Federal rules define a motor carrier to include a company that employs or assigns drivers, which can reach a company that never titled the truck in its own name.<sup><a href="#s8">8</a></sup> The truck's owner, a leasing company and a shipper can also be involved. We identify every one of them early.</p></details>
 <details><summary>How much insurance does a trucking company have to carry?</summary><p>A for-hire carrier moving general freight between states needs at least $750,000 in public liability coverage when the vehicle is rated at 10,001 pounds or more. Oil and most hazardous materials raise that floor to $1,000,000.<sup><a href="#s7">7</a></sup> Carriers operating only within South Carolina and private carriers hauling their own goods follow different rules.</p></details>
 <details><summary>What if I was partly at fault?</summary><p>You can still recover if you were 50% or less at fault. Your amount is reduced by your share of the blame, and once your share passes 50% there is no recovery.<sup><a href="#s4">4</a></sup></p></details>
 <details><summary>What does it cost?</summary><p>The case review is free. [[FEE_TEXT]] [[FEE_COSTS]]</p></details>
 <details><summary>Where is your office, and do I have to come to Summerville?</summary><p>Our one office is at 128 Linwood Lane, Summerville, SC 29483. No. Most clients outside Summerville meet with us by phone or video, and we can come to you if you are hurt.</p></details>
'''

SOURCES_TRUCK = '''  <li id="s6">49 C.F.R. § 395.8(k) (retention of records of duty status and supporting documents for six months): <a href="https://www.ecfr.gov/current/title-49/section-395.8" rel="nofollow noopener">ecfr.gov</a></li>
  <li id="s7">49 C.F.R. § 387.9 (minimum levels of financial responsibility for for-hire motor carriers): <a href="https://www.ecfr.gov/current/title-49/section-387.9" rel="nofollow noopener">ecfr.gov</a></li>
  <li id="s8">49 C.F.R. § 390.5 (definitions of motor carrier and commercial motor vehicle): <a href="https://www.ecfr.gov/current/title-49/section-390.5" rel="nofollow noopener">ecfr.gov</a></li>'''


def render(page, template, body_car, body_truck):
    """Fill the template for one page. The [[LP_*]] and [[FEE_*]] tokens are left for build_site to resolve."""
    slug, geo, h1, kind, _kw = page
    g = GEOS[geo]
    n = noun(h1)
    noun_title = " ".join(w.capitalize() for w in n.split())
    pl = place(geo)
    pl_short = "South Carolina" if geo == "statewide" else CITIES[geo]
    body = (body_truck if kind == "truck" else body_car)
    body = body.replace("{{NOUN_TITLE}}", noun_title).replace("{{PLACE}}", pl).replace("{{PLACE_SHORT}}", pl_short)
    sub = g["sub"] if kind == "car" else g["sub"].replace("crash victims", "truck crash victims")
    html = template
    for k, v in {
        "{{H1}}": h1, "{{DESC}}": description(h1, geo, kind), "{{URL}}": url(slug, geo), "{{CT}}": "truck-accident" if kind == "truck" else "car-accident",
        "{{GEO}}": g["geo"], "{{SUB}}": sub, "{{LOCAL}}": g["local"], "{{BODY}}": body,
        "{{FAQ_H2}}": f"{pl_short} {'Truck' if kind == 'truck' else noun_title} FAQs", "{{FAQ}}": FAQ_TRUCK if kind == "truck" else FAQ_CAR,
        "{{FACT_BOOK}}": FACT_BOOK, "{{FACT_BOOK_URL}}": FACT_BOOK_URL, "{{CITE}}": g["cite"], "{{EXTRA_SOURCES}}": SOURCES_TRUCK if kind == "truck" else "",
    }.items():
        html = html.replace(k, v)
    assert "{{" not in html, f"unfilled placeholder on {slug}"
    return html
