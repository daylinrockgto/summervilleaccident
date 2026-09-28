"""Firm facts for summervilleaccidentattorney.com: name, address, phone, links, people, navigation, redirects.

Same firm, same office and phone as frostlawgroupsc.com. This site covers personal injury only; the
main site covers everything else and the two are cross-linked (see MAIN_SITE and CROSS_LINK_*).
Items marked TODO need the firm's confirmation.
"""
import json
import os

BUILD_DATE = "2026-09-16"
ORIGIN = "https://www.summervilleaccidentattorney.com"  # www is the canonical host (Google already chose it)
MAIN_SITE = "https://frostlawgroupsc.com"
MAIN_SITE_LABEL = "frostlawgroupsc.com"
SITE_NAME = "Summerville Accident Attorney"
SITE_SUB = "A Frost Law Group practice"

NAME = "Frost Law Group, LLC"
TAGLINE = "Frost First."
PROMISES = ("Free consultation", "No fee unless we win", "Available 24/7")
STREET = "128 Linwood Lane"
CITY = "Summerville"
STATE = "SC"
ZIP = "29483"
PHONE = "(843) 419-6653"
PHONE_E164 = "+18434196653"
EMAIL = "tara@frostlawgroupsc.com"
PO_BOX = "PO Box 1986, Summerville, SC 29484"
BAR_DIRECTORY_URL = "https://www.sccourts.org/attorneys/detail/"
GEO = None

MAP_QUERY = "128 Linwood Lane, Summerville, SC 29483"
MAP_EMBED_URL = "https://www.google.com/maps?q=" + MAP_QUERY.replace(" ", "+") + "&output=embed"
DIRECTIONS_URL = "https://www.google.com/maps/dir/?api=1&destination=" + MAP_QUERY.replace(" ", "+")

# One Business Profile and one Yelp listing for the firm; both point at the main site. This site links to them
# and lists them in sameAs so search engines connect the two sites to the same firm.
GBP_URL = "https://maps.google.com/maps?cid=6320073536186250254"
REVIEW_URL = "https://search.google.com/local/writereview?placeid=ChIJ4Vm83lNj_ogRDnS6XmVptVc"  # the Business Profile "write a review" link, opens the review box directly
YELP_URL = "https://www.yelp.com/biz/frost-law-group-summerville"
PREFERRED_SOURCE_URL = "https://www.google.com/preferences/source?q=https://www.summervilleaccidentattorney.com"
FACEBOOK = "https://www.facebook.com/frostlawgroupsc/"
INSTAGRAM = "https://www.instagram.com/frostlawgroupllc/"
TWITTER = "https://twitter.com/FrostLawGroup"
LINKEDIN = "https://www.linkedin.com/company/frost-law-groupsc"
SOCIAL = [("Facebook", FACEBOOK, "fb"), ("Instagram", INSTAGRAM, "ig"), ("LinkedIn", LINKEDIN, "in"), ("X (Twitter)", TWITTER, "x")]
SAME_AS = [MAIN_SITE + "/", GBP_URL, YELP_URL, FACEBOOK, INSTAGRAM, LINKEDIN, TWITTER]
KGMID = "/g/11b5pl8mj4"
RATING = (4.8, 30)  # Google Business Profile, September 2026

HOURS_DISPLAY = [("Monday – Thursday", "9:00 AM – 5:00 PM"), ("Friday", "9:00 AM – 12:00 PM"), ("Phone", "Answered 24/7 for injury calls")]
HOURS_SHORT = "Office Mon–Thu 9–5 · Fri 9–12 · Injury calls answered 24/7"
HOURS_LD = [("Monday", "09:00", "17:00"), ("Tuesday", "09:00", "17:00"), ("Wednesday", "09:00", "17:00"), ("Thursday", "09:00", "17:00"), ("Friday", "09:00", "12:00")]

DISCLAIMER = ("This website is attorney advertising and is for informational purposes only; it is not legal advice and does not create an attorney-client relationship. "
              "Prior results do not guarantee a similar outcome. Talk to a licensed South Carolina attorney about your own situation.")
ASIDE_BLURB = "Tell us what happened. We will tell you whether you have a claim, what it may be worth, and what to do before you talk to the insurance company."
LLMS_SUMMARY = ("summervilleaccidentattorney.com is the personal injury practice of Frost Law Group, LLC, a husband-and-wife law firm at 128 Linwood Lane in Summerville, South Carolina. "
                "Attorney Tara L. Frost, a former Dorchester County magistrate judge, handles car, truck, motorcycle, rideshare and pedestrian accidents, drunk-driving crash victims, dog bites, "
                "slip and fall, workers' compensation, catastrophic injury and wrongful death claims for Dorchester, Berkeley, Charleston and Colleton County residents on a contingency fee: "
                "free consultation, no fee unless we win. The firm's estate planning, probate and criminal defense practice is at frostlawgroupsc.com.")

LOGO = "logo.png"
OG_SOURCE = "client-meeting.jpg"
FORM_ENDPOINT = "https://formspree.io/f/xdekonez"  # Formspree form shared with the main site; the subject line says which site the message came from

# The one sentence that describes the main site. It is the only place the other practice areas are named on this
# site (build_site.py checks that no page names them anywhere else, so the two sites never compete for a search).
CROSS_LINK_TEXT = "Estate planning, probate and criminal defense: visit our main site"
CROSS_LINK_SHORT = "Estate planning, probate &amp; criminal defense"
# Phrases the cannibalization check ignores: the cross-link sentence, and Tara's judicial title (a credential, not a service).
CROSS_LINK_PHRASES = ["Estate planning, probate and criminal defense", "Estate planning, probate &amp; criminal defense", "estate planning, probate and criminal defense",
                      "Associate Probate Judge", "associate probate judge"]

ATTORNEYS = {
    "tara": dict(
        key="tara", slug="attorneys/tara-frost", name="Tara L. Frost", short="Tara Frost", first="Tara", headshot="headshot-tara.jpg", bio_photo="tara-bio.jpg",
        full_name="Tara Leigh Frost", email="tara@frostlawgroupsc.com", bar_number="100610", admitted="November 13, 2012", admitted_iso="2012-11-27", jd_year="2012",
        linkedin="https://www.linkedin.com/in/tara-frost-7b394551/", main_site_bio=MAIN_SITE + "/attorneys/tara-frost/",
        byline="Personal injury attorney · former Dorchester County Magistrate Judge",
        aside="Tara leads the firm's injury practice. As a Dorchester County Magistrate Judge she heard civil cases and weighed evidence every week; she knows what an adjuster's file looks like and what a jury needs to see.",
        alumni=["Charleston School of Law"],
        knows=["Personal injury", "Car accidents", "Truck accidents", "Motorcycle accidents", "Dog bites", "Wrongful death", "Premises liability", "Workers' compensation"],
        same_as=["https://www.linkedin.com/in/tara-frost-7b394551/", MAIN_SITE + "/attorneys/tara-frost/"],
        ld_description="Summerville, SC personal injury attorney; former Dorchester County Magistrate Judge (2022–2025) and Associate Probate Judge (2025–2026); South Carolina Bar No. 100610.",
    ),
    "jack": dict(
        key="jack", slug="attorneys/jack-frost", name="Jack C. Frost", short="Jack Frost", first="Jack", headshot="headshot-jack.jpg", bio_photo="jack-bio.jpg",
        full_name="Jack Christian Frost", email="jack@frostlawgroupsc.com", bar_number="103633", admitted="November 27, 2018", admitted_iso="2018-11-27", jd_year="2016",
        linkedin="https://www.linkedin.com/in/jack-c-frost-9a951253/", main_site_bio=MAIN_SITE + "/attorneys/jack-frost/",
        byline="Attorney at Law · 14 years in Lowcountry law enforcement",
        aside="Jack spent fourteen years as a Summerville police officer and a Charleston County Sheriff's Office detective. He has worked hundreds of crash scenes and knows how a collision report gets written, and what it leaves out.",
        alumni=["Charleston School of Law", "Strayer University", "Trident Technical College", "College of Charleston"],
        knows=["Accident investigation", "Crash reconstruction evidence", "Personal injury", "Law enforcement procedure"],
        same_as=["https://www.linkedin.com/in/jack-c-frost-9a951253/", MAIN_SITE + "/attorneys/jack-frost/"],
        ld_description="Summerville, SC attorney and former Summerville Police Department officer and Charleston County Sheriff's Office detective; investigates crash cases for the firm's injury practice; South Carolina Bar No. 103633.",
    ),
}
ATTORNEYS["tara"]["admitted_iso"] = "2012-11-13"

TEAM = {
    "tara": dict(name="Tara L. Frost", role="Attorney · leads the injury practice", photo="headshot-tara.jpg", alt="Tara L. Frost, personal injury attorney", slug="attorneys/tara-frost"),
    "jack": dict(name="Jack C. Frost", role="Attorney · investigation", photo="headshot-jack.jpg", alt="Jack C. Frost, attorney and former detective", slug="attorneys/jack-frost"),
    "cassie": dict(name="Cassandra “Cassie” Snyder", role="Paralegal", photo="headshot-cassie.jpg", alt="Cassie Snyder, paralegal", slug=None),
    "dogs": dict(name="The Frost Pups", role="Comfort specialists", photo="dogs.jpg", alt="The firm's Golden Retrievers", slug=None),
}

# Google reviews of the firm (public listing), injury-related first, quoted as written; reviewers shown as first name and last initial.
REVIEWS = [
    dict(name="Shannon D.", stars=5, source="Google review · injury claim", text="The Frost Law Group took on our case when several other firms would not. Upon meeting with Tara and Jack to review our case, we knew we were in good hands. We were impressed with their diligence, professionalism and willingness to go the extra mile. We were impressed with the constant communication and thoroughness that the Frost Law Group provided us throughout the entire process."),
    dict(name="Leonard J.", stars=5, source="Google review · car accident", text="My family settled our claim with this company following a car accident last year. The staff was professional, courteous and polite throughout the entire process. I would highly recommend their services."),
    dict(name="Michelle F.", stars=5, source="Google review", text="Very warm, helpful and willing to explain the process so that we clearly understood when we were devastated by grief. Since our initial meeting Tara, Jack and Lauren have kept in touch and kept us aware of every step. Not what I expected of an attorney. Highly recommend!"),
    dict(name="Kevin O.", stars=5, source="Google review", text="Excellent representation! Very honest and genuinely concerned for the client. They care about you and will keep you in the loop regarding your case every step of the way. They are professionals in every sense of the word."),
    dict(name="Nick P.", stars=5, source="Google review", text="Mr. Frost and his staff were very professional and helpful. They gave me hope where everyone else had given up on me."),
    dict(name="Maya J.", stars=5, source="Google review", text="The Frost Law Group went above and beyond for my family. They are passionate about their clients and their client's families. I will always recommend this group and will use them in the future."),
    dict(name="Tony S.", stars=5, source="Google review", text="Professional, fast, and their two dogs are awesome."),
    dict(name="Stacy R.", stars=5, source="Google review", text="They are an awesome group of people. The energy and vibe when you walk into the building is amazing!"),
]

# Hubs and their spokes (order = order in menus and sidebars).
CAR = "practice-areas/car-accidents"
HUB_SPOKES = {
    CAR: [CAR + "/what-to-do-after-a-car-accident-in-south-carolina", CAR + "/is-south-carolina-an-at-fault-state", CAR + "/south-carolina-comparative-negligence",
          CAR + "/south-carolina-car-accident-statute-of-limitations", CAR + "/south-carolina-car-accident-laws", CAR + "/should-i-talk-to-the-other-drivers-insurance-company",
          CAR + "/uninsured-motorist-accidents", CAR + "/hit-and-run-accidents", CAR + "/distracted-driving-accidents", "practice-areas/drunk-driving-accidents",
          "practice-areas/rideshare-accidents", CAR + "/delivery-driver-accidents", CAR + "/auto-injury-assessment-after-a-crash", CAR + "/where-crashes-happen-in-summerville",
          CAR + "/how-to-get-your-south-carolina-accident-report", CAR + "/car-accident-without-a-police-report", CAR + "/how-long-after-a-car-accident-can-you-claim-injury",
          CAR + "/car-accident-that-was-not-your-fault", CAR + "/minor-car-accident-what-to-do", CAR + "/what-happens-if-the-accident-was-my-fault",
          CAR + "/rear-end-collisions", CAR + "/how-much-is-my-car-accident-case-worth", CAR + "/how-long-does-a-car-accident-case-take"],
    "practice-areas/truck-accidents": ["practice-areas/truck-accidents/who-is-liable-in-a-truck-accident"],
    "practice-areas/motorcycle-accidents": ["practice-areas/motorcycle-accidents/south-carolina-motorcycle-helmet-law"],
    "practice-areas/pedestrian-accidents": [],
    "practice-areas/dog-bites": ["practice-areas/dog-bites/south-carolina-dog-bite-law", "practice-areas/dog-bites/child-bitten-by-a-dog", "practice-areas/dog-bites/does-homeowners-insurance-cover-dog-bites"],
    "practice-areas/slip-and-fall": [],
    "practice-areas/workers-compensation": [],
    "practice-areas/catastrophic-injuries": [],
    "practice-areas/wrongful-death": ["practice-areas/wrongful-death/south-carolina-wrongful-death-statute"],
}
HUBS = ["practice-areas/car-accidents", "practice-areas/truck-accidents", "practice-areas/motorcycle-accidents", "practice-areas/pedestrian-accidents", "practice-areas/dog-bites",
        "practice-areas/slip-and-fall", "practice-areas/workers-compensation", "practice-areas/catastrophic-injuries", "practice-areas/wrongful-death"]
HUB_ATTORNEY = {h: "tara" for h in HUB_SPOKES}

NAV = [
    ("Practice areas", "practice-areas", HUBS + ["practice-areas/rideshare-accidents", "practice-areas/drunk-driving-accidents"], "All practice areas"),
    ("Areas we serve", "areas", ["areas/summerville", "areas/goose-creek", "areas/ladson", "areas/north-charleston", "areas/charleston", "areas/mount-pleasant", "areas/moncks-corner", "areas/walterboro", "areas/west-ashley"], "All communities"),
    ("About", "about", ["attorneys/tara-frost", "attorneys/jack-frost", "reviews"], "Our team"),
    ("Questions", "questions", [], ""),
    ("Blog", "blog", [], ""),
    ("Español", "es/abogado-de-accidentes", [], ""),
]

FOOTER_PRACTICE = [("Car accidents", "practice-areas/car-accidents"), ("Truck accidents", "practice-areas/truck-accidents"), ("Motorcycle accidents", "practice-areas/motorcycle-accidents"),
                   ("Pedestrian accidents", "practice-areas/pedestrian-accidents"), ("Uber & Lyft accidents", "practice-areas/rideshare-accidents"), ("Drunk-driving crash victims", "practice-areas/drunk-driving-accidents"),
                   ("Dog bites", "practice-areas/dog-bites"), ("Slip and fall", "practice-areas/slip-and-fall"), ("Workers' compensation", "practice-areas/workers-compensation"),
                   ("Catastrophic injuries", "practice-areas/catastrophic-injuries"), ("Wrongful death", "practice-areas/wrongful-death")]
FOOTER_EXPLORE = [("Our team", "about"), ("Tara L. Frost", "attorneys/tara-frost"), ("Jack C. Frost", "attorneys/jack-frost"), ("Client reviews", "reviews"),
                  ("Questions people ask", "questions"), ("Blog", "blog"), ("Abogado de accidentes (español)", "es/abogado-de-accidentes"), ("Free consultation & directions", "contact")]
FOOTER_AREAS = ["areas/summerville", "areas/goose-creek", "areas/ladson", "areas/north-charleston", "areas/charleston", "areas/mount-pleasant", "areas/moncks-corner", "areas/walterboro", "areas/west-ashley"]

COUNTY_ORDER = ["Dorchester County", "Berkeley County", "Charleston County", "Colleton County"]
AREA_SERVED = ["Summerville", "Goose Creek", "Ladson", "North Charleston", "Charleston", "Mount Pleasant", "Moncks Corner", "Walterboro", "West Ashley",
               "Hanahan", "Knightsville", "Sangaree", "Nexton", "Cane Bay", "Ridgeville", "St. George", "Harleyville", "Daniel Island", "James Island", "Johns Island"]

# Old address (regex, no leading slash) -> new address. From the search audit's redirect map (Appendix D):
# every removed page that Google is still showing gets a permanent redirect to the closest new page.
REDIRECTS = [
    ("goose-creek/?", "/areas/goose-creek/"),
    ("attorneys/?", "/about/"),
    ("truck-accident-3/?", "/practice-areas/truck-accidents/"),
    ("summerville/?", "/areas/summerville/"),
    ("mt-pleasant/?", "/areas/mount-pleasant/"),
    ("mount-pleasant/?", "/areas/mount-pleasant/"),
    ("motorcycle-accident/?", "/practice-areas/motorcycle-accidents/"),
    ("wrongful-death-2/?", "/practice-areas/wrongful-death/"),
    ("wrongful-death/?", "/practice-areas/wrongful-death/"),
    ("north-charleston/?", "/areas/north-charleston/"),
    ("car-accident/?", "/practice-areas/car-accidents/"),
    ("walterboro/?", "/areas/walterboro/"),
    ("moncks-corner/?", "/areas/moncks-corner/"),
    ("charleston/?", "/areas/charleston/"),
    ("ladson/?", "/areas/ladson/"),
    ("results/?", "/about/"),
    ("serving/?", "/areas/"),
    ("other-areas/?", "/areas/"),
    ("west-ashley/?", "/areas/west-ashley/"),
    ("pedestrian-accident/?", "/practice-areas/pedestrian-accidents/"),
    ("dog-bite/?", "/practice-areas/dog-bites/"),
    ("slip-and-fall/?", "/practice-areas/slip-and-fall/"),
    ("workers-compensation/?", "/practice-areas/workers-compensation/"),
    ("catastrophic-injuries/?", "/practice-areas/catastrophic-injuries/"),
    ("contact-us/?", "/contact/"),
    ("about-us/?", "/about/"),
]

COURTS = {}
_ld = os.path.join(os.path.dirname(__file__), "local_data.json")
if os.path.exists(_ld):
    _d = json.load(open(_ld, encoding="utf-8"))
    COURTS = _d.get("courts", {})
    if _d.get("office_geo"):
        GEO = tuple(_d["office_geo"])
