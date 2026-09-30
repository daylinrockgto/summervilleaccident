# -*- coding: utf-8 -*-
"""Manifest v7 (2026-09-28): Sept 15 spine + audit extras, per Daylin's decisions of 2026-09-28.
Emits v2/manifest.json (every URL on the rebuilt site) and v2/redirects.json (every 301)."""
import json, re
P = {"car": "/car-accident-attorneys-in-summerville/", "truck": "/truck-accident-attorneys-in-summerville/",
     "moto": "/motorcycle-accident-attorneys-in-summerville/", "ride": "/rideshare-accident-attorneys-in-summerville/",
     "slip": "/slip-and-fall-attorneys-in-summerville/", "dog": "/dog-bite-attorneys-in-summerville/",
     "wd": "/wrongful-death-attorneys-in-summerville/", "cat": "/catastrophic-injury-attorneys-in-summerville/",
     "ped": "/pedestrian-accident-attorneys-in-summerville/"}
C = {k: f"/personal-injury-attorneys-in-{k}-county/" for k in
     ["dorchester", "charleston", "berkeley", "colleton", "orangeburg", "beaufort", "georgetown", "williamsburg"]}
def slug(h1): return re.sub(r"[^a-z0-9]+", "-", h1.lower().replace("'", "")).strip("-")
M = []
def add(id, kind, h1, url, kp, words, status, parent=None, note=""):
    M.append(dict(id=id, kind=kind, h1=h1, url=url, kp=kp, words=words, status=status, parent=parent, note=note))

# Core
add("home", "Home", "Summerville Personal Injury Attorneys", "/", "Summerville personal injury attorneys", 9200, "Written, fix pass")
add("pa", "Menu page", "Personal Injury Cases Frost Law Group Handles in Summerville, South Carolina", "/practice-areas/", "Summerville personal injury cases", 1700, "Written, fix pass, add the two new parents")
add("loc", "Menu page", "South Carolina Personal Injury Attorneys Serving Summerville and the Surrounding Counties", "/locations/", "South Carolina personal injury attorneys", 5300, "Written, fix pass, add city links")
# Parents
for id, k, h1, st in [("car","car","Car Accident Attorneys in Summerville","Written, fix pass"),("truck","truck","Truck Accident Attorneys in Summerville","Written, fix pass"),
    ("moto","moto","Motorcycle Accident Attorneys in Summerville","Written, fix pass"),("ride","ride","Rideshare Accident Attorneys in Summerville","Written, fix pass"),
    ("slip","slip","Slip and Fall Attorneys in Summerville","Written, fix pass"),("dog","dog","Dog Bite Attorneys in Summerville","Written, fix pass"),
    ("wd","wd","Wrongful Death Attorneys in Summerville","Written, fix pass"),
    ("cat","cat","Catastrophic Injury Attorneys in Summerville","NEW, built from the car catastrophic child plus new research"),
    ("ped","ped","Pedestrian Accident Attorneys in Summerville","NEW")]:
    add(id, "Practice parent", h1, P[k], h1, 5200, st)
# Practice children
CH = [("car-dui","car","Drunk Driving Accident Lawyers in Summerville","Written, fix pass"),
      ("car-hr","car","Hit and Run Accident Lawyers in Summerville","Written, fix pass"),
      ("car-distracted","car","Distracted Driving Accident Lawyers in Summerville","NEW, replaces the catastrophic child"),
      ("truck-tt","truck","Tractor Trailer Accident Lawyers in Summerville","Written, fix pass"),
      ("truck-deliv","truck","Delivery Truck Accident Lawyers in Summerville","Written, fix pass"),
      ("truck-fatigue","truck","Truck Driver Fatigue Accident Lawyers in Summerville","Written, fix pass"),
      ("moto-left","moto","Left Turn Motorcycle Accident Lawyers in Summerville","Written, fix pass"),
      ("moto-helmet","moto","Motorcycle Helmet Law Injury Lawyers in Summerville","Written, fix pass"),
      ("moto-um","moto","Uninsured Motorist Motorcycle Lawyers in Summerville","Written, fix pass"),
      ("ride-uber","ride","Uber Accident Lawyers in Summerville","Written, fix pass"),
      ("ride-lyft","ride","Lyft Accident Lawyers in Summerville","Written, fix pass"),
      ("slip-retail","slip","Retail Slip and Fall Lawyers in Summerville","Written, fix pass"),
      ("slip-apt","slip","Apartment Injury Lawyers in Summerville","Written, fix pass"),
      ("slip-prem","slip","Premises Liability Lawyers in Summerville","Written, fix pass"),
      ("dog-strict","dog","Dog Bite Strict Liability Lawyers in Summerville","Written, fix pass"),
      ("dog-child","dog","Child Dog Bite Injury Lawyers in Summerville","Written, fix pass"),
      ("dog-ins","dog","Dog Bite Insurance Claim Lawyers in Summerville","Written, fix pass"),
      ("wd-car","wd","Fatal Car Accident Lawyers in Summerville","Written, fix pass"),
      ("wd-survival","wd","Survival Action Lawyers in Summerville","Written, fix pass"),
      ("wd-truck","wd","Fatal Truck Accident Lawyers in Summerville","Written, fix pass")]
for id, k, h1, st in CH:
    add(id, "Practice child", h1, P[k] + slug(h1) + "/", h1, 3200, st, parent=k)
# County parents
for k in C:
    add("co-" + k, "County parent", f"Personal Injury Attorneys in {k.capitalize()} County", C[k], f"Personal Injury Attorneys in {k.capitalize()} County", 5200, "Written, fix pass")
# County children (vehicle) + city pages
CC = [("chs-car","charleston","Car Accident Lawyers in Charleston County","Written, fix pass"),
      ("chs-truck","charleston","Truck Accident Lawyers in Charleston County","Written, fix pass"),
      ("chs-moto","charleston","Motorcycle Accident Lawyers in Charleston County","Written, fix pass"),
      ("brk-car","berkeley","Car Accident Lawyers in Berkeley County","Written, fix pass"),
      ("brk-truck","berkeley","Truck Accident Lawyers in Berkeley County","Written, fix pass"),
      ("brk-moto","berkeley","Motorcycle Accident Lawyers in Berkeley County","Written, fix pass"),
      ("city-charleston","charleston","Charleston Personal Injury Lawyers","NEW city page"),
      ("city-north-charleston","charleston","North Charleston Personal Injury Lawyers","NEW city page"),
      ("city-mount-pleasant","charleston","Mount Pleasant Car Accident Lawyers","NEW city page"),
      ("city-west-ashley","charleston","West Ashley Car Accident Lawyers","NEW city page"),
      ("city-goose-creek","berkeley","Goose Creek Car Accident Lawyers","NEW city page, audit priority 1"),
      ("city-moncks-corner","berkeley","Moncks Corner Car Accident Lawyers","NEW city page"),
      ("city-ladson","berkeley","Ladson Car Accident Lawyers","NEW city page"),
      ("city-walterboro","colleton","Walterboro Car Accident Lawyers","NEW city page")]
for id, k, h1, st in CC:
    add(id, "County child" if not id.startswith("city") else "City page (county child)", h1, C[k] + slug(h1) + "/", h1, 3200, st, parent="co-" + k)
# Answer pages
AN = [("a-what-to-do","car","What to Do After a Car Accident in South Carolina"),
      ("a-at-fault","car","Is South Carolina an At-Fault State"),
      ("a-comparative","car","How Comparative Negligence Works in South Carolina"),
      ("a-sol","car","South Carolina Car Accident Statute of Limitations"),
      ("a-laws","car","South Carolina Car Accident Laws"),
      ("a-talk-insurer","car","Should I Talk to the Other Driver's Insurance Company"),
      ("a-um","car","Uninsured Motorist Coverage in South Carolina"),
      ("a-assessment","car","Auto Injury Assessment in Summerville"),
      ("a-where","car","Where Car Accidents Happen in Summerville"),
      ("a-report","car","How to Get a South Carolina Accident Report"),
      ("a-no-report","car","Can You Claim a Car Accident Without a Police Report"),
      ("a-claim-later","car","How Long After a Car Accident Can You Claim Injury"),
      ("a-not-fault","car","What to Do After a Car Accident That Was Not Your Fault"),
      ("a-minor","car","What to Do After a Minor Car Accident"),
      ("a-my-fault","car","What Happens If a Car Accident Was Your Fault"),
      ("a-rear-end","car","Who Is at Fault in a Rear End Collision"),
      ("a-worth","car","How Much Is My Car Accident Case Worth"),
      ("a-how-long","car","How Long Does a Car Accident Case Take"),
      ("a-truck-liable","truck","Who Is Liable in a Truck Accident")]
for id, k, h1 in AN:
    add(id, "Answer page", h1, P[k] + slug(h1) + "/", h1.lower(), 1800, "NEW, rewritten from the repo page with its errors fixed", parent=k)
# Language, index, legacy
add("es", "Spanish page", "Abogado de Accidentes de Carro en Summerville", "/es/" + slug("Abogado de Accidentes de Carro en Summerville") + "/", "abogado de accidentes de carro en Summerville", 2500, "NEW, rewritten from the repo page")
add("questions", "Question index", "Questions People Ask After an Accident in Summerville", "/questions/", "questions after an accident in Summerville", 800, "Rebuilt as a link index, no copied answers")
add("wc-legacy", "Legacy page", "(old live copy)", "/practice-areas/workers-compensation/", "", 0, "Old live copy only, no links in, never edited", note="Settled 2026-09-28")
# Utility (repo pages, fixed)
for id, h1, url in [("about","Our Team","/about/"),("tara","Tara L. Frost","/attorneys/tara-frost/"),("jack","Jack C. Frost","/attorneys/jack-frost/"),
                    ("contact","Get Your Free Consultation","/contact/"),("reviews","Client Reviews","/reviews/"),("blog","The Blog","/blog/"),
                    ("post-i26","Crash on I-26 near Summerville","/blog/i-26-crash-summerville-who-writes-the-report/"),
                    ("post-dog","A dog bite in a Summerville neighborhood","/blog/dog-bite-summerville-neighborhood-what-parents-should-know/"),
                    ("post-moto","Motorcycle season in the Lowcountry","/blog/motorcycle-season-lowcountry-helmet-law-your-claim/"),
                    ("post-um","Hit by an uninsured driver in Goose Creek","/blog/hit-by-an-uninsured-driver-goose-creek-your-own-policy/"),
                    ("privacy","Privacy Policy","/privacy-policy/"),("terms","Terms of Use","/terms-of-use/"),("a11y","Accessibility Statement","/accessibility/"),
                    ("thanks","Thank you","/thank-you/")]:
    add(id, "Site page (repo, compliance fixes)", h1, url, "", 0, "Repo page, fix pass")

U = {m["id"]: m["url"] for m in M}
R = [  # old URL (no host), new URL. Order matters: specific before general.
 # live SPA practice pages
 ("/practice-areas/car-accidents", U["car"]), ("/practice-areas/truck-accidents", U["truck"]), ("/practice-areas/motorcycle-accidents", U["moto"]),
 ("/practice-areas/slip-and-fall", U["slip"]), ("/practice-areas/dog-bites", U["dog"]), ("/practice-areas/wrongful-death", U["wd"]),
 ("/practice-areas/catastrophic-injuries", U["cat"]),
 # repo spokes (Vercel preview only) and repo hubs
 ("/practice-areas/car-accidents/hit-and-run-accidents", U["car-hr"]), ("/practice-areas/car-accidents/distracted-driving-accidents", U["car-distracted"]),
 ("/practice-areas/car-accidents/delivery-driver-accidents", U["truck-deliv"]),
 ("/practice-areas/car-accidents/what-to-do-after-a-car-accident-in-south-carolina", U["a-what-to-do"]),
 ("/practice-areas/car-accidents/is-south-carolina-an-at-fault-state", U["a-at-fault"]),
 ("/practice-areas/car-accidents/south-carolina-comparative-negligence", U["a-comparative"]),
 ("/practice-areas/car-accidents/south-carolina-car-accident-statute-of-limitations", U["a-sol"]),
 ("/practice-areas/car-accidents/south-carolina-car-accident-laws", U["a-laws"]),
 ("/practice-areas/car-accidents/should-i-talk-to-the-other-drivers-insurance-company", U["a-talk-insurer"]),
 ("/practice-areas/car-accidents/uninsured-motorist-accidents", U["a-um"]),
 ("/practice-areas/car-accidents/auto-injury-assessment-after-a-crash", U["a-assessment"]),
 ("/practice-areas/car-accidents/where-crashes-happen-in-summerville", U["a-where"]),
 ("/practice-areas/car-accidents/how-to-get-your-south-carolina-accident-report", U["a-report"]),
 ("/practice-areas/car-accidents/car-accident-without-a-police-report", U["a-no-report"]),
 ("/practice-areas/car-accidents/how-long-after-a-car-accident-can-you-claim-injury", U["a-claim-later"]),
 ("/practice-areas/car-accidents/car-accident-that-was-not-your-fault", U["a-not-fault"]),
 ("/practice-areas/car-accidents/minor-car-accident-what-to-do", U["a-minor"]),
 ("/practice-areas/car-accidents/what-happens-if-the-accident-was-my-fault", U["a-my-fault"]),
 ("/practice-areas/car-accidents/rear-end-collisions", U["a-rear-end"]),
 ("/practice-areas/car-accidents/how-much-is-my-car-accident-case-worth", U["a-worth"]),
 ("/practice-areas/car-accidents/how-long-does-a-car-accident-case-take", U["a-how-long"]),
 ("/practice-areas/truck-accidents/who-is-liable-in-a-truck-accident", U["a-truck-liable"]),
 ("/practice-areas/motorcycle-accidents/south-carolina-motorcycle-helmet-law", U["moto-helmet"]),
 ("/practice-areas/dog-bites/south-carolina-dog-bite-law", U["dog-strict"]),
 ("/practice-areas/dog-bites/child-bitten-by-a-dog", U["dog-child"]),
 ("/practice-areas/dog-bites/does-homeowners-insurance-cover-dog-bites", U["dog-ins"]),
 ("/practice-areas/wrongful-death/south-carolina-wrongful-death-statute", U["wd"]),
 ("/practice-areas/pedestrian-accidents", U["ped"]), ("/practice-areas/rideshare-accidents", U["ride"]),
 ("/practice-areas/drunk-driving-accidents", U["car-dui"]),
 ("/areas", U["loc"]), ("/areas/summerville", "/"), ("/areas/goose-creek", U["city-goose-creek"]), ("/areas/ladson", U["city-ladson"]),
 ("/areas/north-charleston", U["city-north-charleston"]), ("/areas/charleston", U["city-charleston"]), ("/areas/mount-pleasant", U["city-mount-pleasant"]),
 ("/areas/moncks-corner", U["city-moncks-corner"]), ("/areas/walterboro", U["city-walterboro"]), ("/areas/west-ashley", U["city-west-ashley"]),
 ("/es/abogado-de-accidentes", U["es"]),
 # pre-2026 site pages Google still shows (audit Appendix D) and other old slugs
 ("/goose-creek", U["city-goose-creek"]), ("/attorneys", "/about/"), ("/truck-accident-3", U["truck"]), ("/summerville", "/"),
 ("/mt-pleasant", U["city-mount-pleasant"]), ("/mount-pleasant", U["city-mount-pleasant"]), ("/motorcycle-accident", U["moto"]),
 ("/wrongful-death-2", U["wd"]), ("/wrongful-death", U["wd"]), ("/north-charleston", U["city-north-charleston"]), ("/car-accident", U["car"]),
 ("/walterboro", U["city-walterboro"]), ("/moncks-corner", U["city-moncks-corner"]), ("/charleston", U["city-charleston"]), ("/ladson", U["city-ladson"]),
 ("/results", "/about/"), ("/serving", U["loc"]), ("/other-areas", U["loc"]), ("/west-ashley", U["city-west-ashley"]),
 ("/pedestrian-accident", U["ped"]), ("/dog-bite", U["dog"]), ("/slip-and-fall", U["slip"]), ("/catastrophic-injuries", U["cat"]),
 ("/workers-compensation", "/practice-areas/workers-compensation/"), ("/contact-us", "/contact/"), ("/about-us", "/about/"),
]
assert len({a for a, b in R}) == len(R), "duplicate redirect source"
live = {m["url"] for m in M}
for a, b in R: assert b in live or b == "/", (a, b)
if __name__ == "__main__":
    json.dump(M, open("llg/v2/manifest.json", "w"), indent=1)
    json.dump(R, open("llg/v2/redirects.json", "w"), indent=1)
    from collections import Counter
    print(Counter(m["kind"] for m in M)); print(len(M), "URLs,", len(R), "redirects,", sum(m["words"] for m in M), "words")
    for m in M:
        if len(m["url"]) > 115: print("LONG", len(m["url"]), m["url"])
