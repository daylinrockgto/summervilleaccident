"""Blog posts: local news and community questions about crashes, injuries and insurance, answered by the attorney who
handles those cases. Tara writes; Jack reviews (his investigation background is the natural second set of eyes).
Outbound links go to official sources (statutes, SCDMV, SCDPS, DPH, SC Courts) and to the community threads where the
question is asked (Nextdoor, Reddit, nofollow). Community links come from local_data.json via local.link(). The official
URLs below were verified in research R1 to R5 (2026-09-28) and are set here because some local_data.json entries
(scdmv_reports, schp, scdoi) point at stale or generic pages.

Corrected 2026-09-29 against repo reviews RR-2 and RR-4: FR-10 return duty, I-26 county geography, dog bite reporting
to DPH, the 47-3-110 text and exceptions, minors' settlements and deadlines, helmet and eye protection rules, UIM
settlement rules under 38-77-160, stacking, the 2024 rewrite of 38-77-170, and cover captions matched to the images."""
import re

from .base import page, BY_SLUG, A, ext, img, p, ul, checks, steps, callout, answer, band, esc, table
from . import firm
from .local import cite, link, LINKS

TEL = f'<a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'
DATE = "2026-09-16"
MODIFIED = "2026-09-29"

# Live slugs (plan.json). Planned pages that are not built yet resolve to their nearest live parent until they are.
CARP = "car-accident-attorneys-in-summerville"
MOTO = "motorcycle-accident-attorneys-in-summerville"
DOG = "dog-bite-attorneys-in-summerville"
BERK = "personal-injury-attorneys-in-berkeley-county"

# Verified official URLs (R1, R2, R3, R4, R5).
DMV_REPORTS = "https://dmv.sc.gov/vehicle-owners/collision-reports"
SCHP_TROOPS = "https://scdps.sc.gov/schp/contact/troops"
FACTBOOKS = "https://scdps.sc.gov/ohsjp/stat_services/factbooks"
SCDOT_EXIT199 = "https://info2.scdot.org/GISMapping/GISMapdl/I26_TCP_Diagrams_Public/Exit199.pdf"
CODE_15_3 = "https://www.scstatehouse.gov/code/t15c003.php"
CODE_38_77 = "https://www.scstatehouse.gov/code/t38c077.php"
CODE_47_3 = "https://www.scstatehouse.gov/code/t47c003.php"
CODE_47_5 = "https://www.scstatehouse.gov/code/t47c005.php"
CODE_56_5 = "https://www.scstatehouse.gov/code/t56c005.php"
CODE_56_9 = "https://www.scstatehouse.gov/code/t56c009.php"
CODE_62_5 = "https://www.scstatehouse.gov/code/t62c005.php"
DPH_RABIES = "https://dph.sc.gov/diseases-conditions/infectious-diseases/animal-borne-diseases/rabies"
DOI_AUTO = "https://doi.sc.gov/588/Automobile-Insurance"
CLEA = "https://www.sccourts.org/media/opinions/HTMLFiles/SC/27029.htm"
CONCRETE = "https://www.sccourts.org/media/opinions/HTMLFiles/SC/24773.htm"
SCCOURTS_BERKELEY = "https://www.sccourts.org/courts/courthouse-search/berkeley/"
EXIT_DIAGRAMS = ext(SCDOT_EXIT199, "SCDOT's interchange diagrams")


def src(*keys):
    out = []
    for k in keys:
        l = LINKS.get(k)
        if l:
            out.append((l["label"], l["url"], l.get("nofollow", False)))
    return out


def slugify(text):
    """A post's URL slug is its H1, lowercased, apostrophes dropped and every other run of punctuation and spaces made one
    hyphen, with every word kept (Settled 2026-10-08). Posts sit at the root, never under /blog/, which is the blog index."""
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"['’]", "", text.lower())).strip("-")


def post(**kw):
    slug = slugify(kw["h1"])
    if slug in BY_SLUG:
        raise ValueError(f"post slug {slug} is already a page")
    kw.setdefault("kind", "post")
    kw.setdefault("hub", "blog")
    kw.setdefault("date", DATE)
    kw.setdefault("modified", MODIFIED)
    kw.setdefault("cta", False)
    kw.setdefault("changefreq", "yearly")
    kw.setdefault("priority", 0.5)
    kw.setdefault("author", "tara")
    kw.setdefault("reviewer", "jack")
    return page(slug, **kw)


# ----------------------------------------------------------------------------- 1. I-26 crash report
post(hero_image="cover-i26-report.jpg",
     hero_caption="A patrol car with its lights on, stopped on the shoulder behind a car on a highway lined with pines (illustration)",
     category="Car accidents",
     title="Crash on I-26 Near Summerville: Who Writes the Report, and How to Get It",
     description="After a crash on I-26 near Summerville, a Highway Patrol trooper often writes the report. What the FR-10 is, why it goes back to SCDMV within 15 days, and how to get the TR-310.",
     h1="Crash on I-26 near Summerville: who writes the report, and how to get it",
     summary="Who usually works an interstate crash, the form you must send back within 15 days, and how to get the full report from SCDMV.",
     lead="After a crash on I-26 near Summerville, the first question is often where the report is. The answer depends on which agency worked the crash.",
     body=(
         '<h2>Who works a crash on the interstate</h2>'
         f'<p>The Summerville Police Department investigates many crashes in town, and it sends people to CrashDocs for the reports it writes. On I-26 the officer is often a trooper with the {ext(SCHP_TROOPS, "South Carolina Highway Patrol")}. The Highway Patrol investigated 80,380 of South Carolina\'s 143,801 collisions in 2024, and 3,468 of Berkeley County\'s 6,536, according to the {ext(FACTBOOKS, "SCDPS Fact Book")}. If a trooper worked your crash, the Highway Patrol directs you to {ext(DMV_REPORTS, "SCDMV")} for the collision report, not to the town.</p>'
         '<h2>What you are handed at the scene</h2>'
         f'<p>At the scene of an investigated crash, the officer gives each driver or owner an insurance verification form. The Highway Patrol calls it the FR-10, its “mandatory insurance verification form.” It is not the full report. It is a form you have to send back. Under {ext(CODE_56_9, "Section 56-9-350")}, the driver or owner must return the completed and verified form to SCDMV within 15 days of the date the officer delivered it. A form that never comes back is prima facie evidence that the vehicle was uninsured.</p>'
         '<p>Keep a copy, because the SCDMV request form for the full report asks for the FR-10 number. If you lose the form, the Highway Patrol says to contact the troop office where the crash happened.</p>'
         f'<p>If no officer investigated a crash that caused injury, death or property damage of $1,000 or more, {cite("report_dmv", "Section 56-5-1270")} requires the driver or owner to send SCDMV a written report, on Form FR-309, within 15 days of the crash.</p>'
         '<h2>The full report</h2>'
         f'<p>The collision report itself is Form TR-310. SCDMV says it is more detailed than the paperwork you received the day of the collision. When an officer investigates a crash with injury, death or $1,000 or more in apparent damage, Section 56-5-1270 has the officer forward the report to SCDMV within 24 hours after finishing the investigation. SCDMV does not publish a processing time. An official copy is available only after SCDMV has received and processed the report.</p>'
         f'<p>You can request it online, at any SCDMV branch, or by mail with Form FR-50. The fee is $10 per report. {A(CARP + "/how-to-get-a-south-carolina-accident-report", "How to get a South Carolina accident report")} walks through each option. Frost Law Group can also request the 911 audio and any dash-camera or body-camera video, along with the findings of the Highway Patrol\'s Multi-disciplinary Accident Investigation Team (Troop Nine) if that team investigated the crash.</p>'
         '<h2>Which county the crash happened in</h2>'
         f'<p>It is easy to assume a crash near Summerville happened in Dorchester County. On I-26 it usually did not. {EXIT_DIAGRAMS} place Exit 194 (Jedburg Road), Exit 197 (Nexton Parkway), Exit 199 (North Main Street, US 17A) and Exit 203 (College Park Road) in Berkeley County, and Exit 205 (US 78) in Charleston County. SCDOT\'s 2024 Dorchester County traffic counts show I-26 in Dorchester only from I-95 to SC 27.</p>'
         f'<p>The county matters because each one has its own courthouse. The Berkeley County Courthouse is in Moncks Corner and the Charleston County Courthouse is on Broad Street in Charleston, and both counties sit in the Ninth Judicial Circuit. The Dorchester County Courthouse is in St. George, in the First Circuit. Which court hears a lawsuit is a venue question a lawyer checks early. The Berkeley County numbers show why this stretch draws attention. I-26 at College Park Road (113 collisions) and I-26 at Jedburg Road (103) were the county\'s two most crash-prone intersections in 2024, as recorded in the SCDPS Fact Book. {A(CARP + "/where-car-accidents-happen-in-summerville", "Where car accidents happen in Summerville")} covers the other corridors.</p>'
         '<h2>What people ask on Nextdoor and Reddit</h2>'
         f'<p>After a bad wreck, two questions tend to come up on {link("nextdoor_summerville", "Nextdoor for Summerville")} and in {link("reddit_charleston", "r/Charleston")}. “How do I get my accident report?” And “The trooper put me at fault, what now?”</p>'
         '<p>For the first, request the TR-310 from SCDMV, or ask Frost Law Group to request it. For the second, the officer\'s contributing-factor findings are an opinion formed at the roadside, not a verdict. Section 56-5-1290 says the reports required by Sections 56-5-1260 through 56-5-1280 may not be evidence of either party\'s negligence or due care at the trial of a damages case. Fault is decided on all the evidence, and video, vehicle data and witness statements can all bear on it.</p>'
         + callout("<b>Frost first:</b> call us before you talk with the other driver's insurer. No provision in South Carolina's auto insurance or claims-practices statutes requires you to give that company a recorded statement. And the FR-10 still goes back to SCDMV within 15 days.")
     ),
     sources=[("South Carolina Highway Patrol, troop coverage and report questions", SCHP_TROOPS, False),
              ("SCDMV, collision reports", DMV_REPORTS, False),
              ("SCDPS, Traffic Collision Fact Books", FACTBOOKS, False),
              ("SCDOT, I-26 Exit 199 interchange diagram", SCDOT_EXIT199, False),
              ("S.C. Code §§ 56-5-1260, 56-5-1270 and 56-5-1290 (crash reports)", CODE_56_5, False),
              ("S.C. Code § 56-9-350 (insurance verification form)", CODE_56_9, False)]
             + src("nextdoor_summerville", "reddit_charleston"),
     related=[CARP + "/how-to-get-a-south-carolina-accident-report", CARP + "/where-car-accidents-happen-in-summerville",
              BERK + "/car-accident-lawyers-in-berkeley-county"],
     faqs=[("How long does it take to get a Highway Patrol accident report in South Carolina?", "SCDMV does not publish a processing time. For a crash with injury, death or $1,000 or more in apparent damage, the officer must forward the report to SCDMV within 24 hours after finishing the investigation, and an official copy is available once SCDMV has received and processed it. The fee is $10 per report."),
           ("What do I do with the FR-10 the trooper gave me?", "Send it back. Section 56-9-350 requires the driver or owner to return the completed and verified form to SCDMV within 15 days of the date the officer delivered it. Keep a copy for your records."),
           ("What if the report says the crash was my fault?", "The officer's contributing-factor findings are an opinion, not a ruling. Fault in an injury claim is decided on all the evidence, and Section 56-5-1290 bars using the reports required by Sections 56-5-1260 through 56-5-1280 as evidence of negligence at a damages trial.")])

# ----------------------------------------------------------------------------- 2. Dog bites in the neighborhood
post(hero_image="cover-dog-bite-neighborhood.jpg",
     hero_caption="A dog standing outside a fence gate near a child's bicycle on the sidewalk (illustration)", category="Dog bites",
     title="A Dog Bite in a Summerville Neighborhood: What Parents Should Know",
     description="A loose dog, a child, and a neighbor who says the dog never bit before. What South Carolina's dog bite statute says, who must report the bite, who usually pays, and what to do first.",
     h1="A dog bite in a Summerville neighborhood: what parents should know",
     summary="The loose dog, the child on a bike, the neighbor who says it never bit before. What the law says, who reports the bite, and why insurance usually pays.",
     lead="Warm weather in Summerville brings more kids out on bikes and more dogs into yards. When a bite happens, the questions parents post online have answers in South Carolina law.",
     body=(
         '<h2>A familiar post</h2>'
         f'<p>Picture a post that could run on {link("nextdoor_summerville", "Nextdoor for Summerville")} or {link("nextdoor_goose_creek", "Goose Creek")}. A dog slips through a gate in a subdivision and bites a child riding past on a bicycle. The comments split between “the owner should be held responsible” and “it was an accident, the dog has never bitten anyone.” Under South Carolina\'s dog bite statute, whether the dog ever bit before is not the question.</p>'
         '<h2>South Carolina has no “first bite” rule</h2>'
         f'<p>Some people assume a dog gets one free bite. {cite("dog_bite", "Section 47-3-110")} has no such rule. When a person is bitten or attacked while in a public place or lawfully in a private place, the owner or the person keeping the dog “is liable for the damages suffered by the person bitten or otherwise attacked.” The S.C. Supreme Court has described the statute as imposing strict liability on the owner or keeper ({ext(CLEA, "Clea v. Odom")}), and nothing in it requires an earlier bite.</p>'
         f'<p>The statute has limits. It protects people in a public place or lawfully on private property, so it does not cover a trespasser. It does not apply when the person bitten “provoked or harassed the dog and that provocation was the proximate cause of the attack.” It also exempts a qualifying police dog acting on a lawful command under a written agency policy, though that exemption does not cover a bite on a bystander. A child riding a bicycle on a public street is in a public place, and whether anything the child did counts as provocation is a question of fact. {A(DOG + "/dog-bite-strict-liability-lawyers-in-summerville", "How the dog bite statute works")}.</p>'
         '<h2>Why the neighbor\'s insurance usually pays</h2>'
         f'<p>Some parents hesitate to make a claim because they like their neighbors. In the ordinary case, the owner\'s homeowner\'s or renter\'s liability insurance pays the claim, subject to that policy\'s limits and exclusions, and the neighbor usually pays nothing personally. Not making a claim can leave your family paying for your child\'s later treatment, such as scar revision years from now. {A(DOG + "/dog-bite-insurance-claim-lawyers-in-summerville", "How insurance handles a dog bite claim")}.</p>'
         '<h2>The first day</h2>'
         + steps([
             ("Get medical care.", f" For a facial wound, ask whether a plastic surgeon should close it. The treating doctor must report the bite to the county health department, now part of the {ext(DPH_RABIES, 'S.C. Department of Public Health')}, by the end of the next working day ({ext(CODE_47_5, 'Section 47-5-90')})."),
             ("Make sure the bite is reported.", " If no doctor treats the bite, the law puts the report on the parent or guardian, due to the county health department by the end of the next working day. The health department then orders the owner to quarantine the dog for at least ten days under Section 47-5-100, at the owner's home, an animal shelter or another place the notice names."),
             ("Photograph the injury on day one and every few days after.", " Photos taken over time show how the wound heals and scars."),
             ("Get the owner's name and address, and stay civil.", " You do not need to discuss fault, and you should not discuss insurance."),
             ("Do not sign a release for a quick check.", f" For a child's claim of $2,500 or less, South Carolina lets a parent settle without court approval ({ext(CODE_62_5, 'Section 62-5-433')}). A small check and a signature can end the claim before anyone knows what later treatment will cost."),
         ])
         + '<h2>What a child\'s claim can include</h2>'
         + f'<p>A child\'s claim can include emergency care, later treatment such as plastic surgery and scar revision, counseling, and the scarring itself. The statute makes the owner liable for “the damages suffered,” and what those are depends on the child\'s injuries and treatment. {A(DOG + "/child-dog-bite-injury-lawyers-in-summerville", "If your child was bitten by a dog")}.</p>'
         + '<p>The law also protects a child\'s settlement. Under Section 62-5-433, a claim worth more than $25,000 net to the child needs circuit court approval on a verified petition stating that the settlement is in the child\'s best interests. The money is then paid through a conservator or under a probate court protective order. For $25,000 or less, the circuit or probate court may approve the settlement, or a conservator may settle it without court approval. Without a conservator, the guardian or guardian ad litem must petition the court. Only a claim of $2,500 or less may be settled by a parent with no court approval and no conservator.</p>'
         + f'<p>Time limits apply too. Most injury suits must be filed within three years ({cite("sol_injury", "Section 15-3-530")}). For a child, {cite("sol_minor", "Section 15-3-40")} may extend that time, but never past one year after the child turns 18. Whether a child gains any extra time depends on the dates, so the deadline is worth checking early.</p>'
         + f'<p>For prevention, the {link("avma_dogbites", "American Veterinary Medical Association")} publishes guidance for families and dog owners.</p>'
         + callout("<b>Frost first:</b> if the owner's insurer calls and asks whether your child “did anything” to the dog, that question is aimed at the provocation exception. Decline the conversation and call us.")
     ),
     sources=[("S.C. Code § 47-3-110 (liability for dog attacks)", CODE_47_3, False),
              ("Clea v. Odom, S.C. Sup. Ct. Op. No. 27029 (2011)", CLEA, False),
              ("S.C. Code §§ 47-5-90 and 47-5-100 (bite reports and quarantine)", CODE_47_5, False),
              ("S.C. Department of Public Health, rabies and animal bites", DPH_RABIES, False),
              ("S.C. Code § 62-5-433 (settlements for minors)", CODE_62_5, False),
              ("S.C. Code §§ 15-3-40 and 15-3-530 (filing deadlines)", CODE_15_3, False)]
             + src("nextdoor_summerville", "nextdoor_goose_creek", "avma_dogbites", "cdc_dogbites"),
     related=[DOG, DOG + "/child-dog-bite-injury-lawyers-in-summerville", DOG + "/dog-bite-insurance-claim-lawyers-in-summerville"],
     faqs=[("Does the dog have to have bitten someone before for the owner to be liable in South Carolina?", "No. Section 47-3-110 does not require a prior bite. The owner or keeper is liable for the damages suffered when the person bitten was in a public place or lawfully on private property, unless the person provoked or harassed the dog and that provocation was the proximate cause of the attack."),
           ("Who do I report a dog bite to in South Carolina?", "The county health department, which is now part of the S.C. Department of Public Health. A doctor who treats the bite must report it by the end of the next working day. If no doctor treats it, the bitten adult, or the parent or guardian of a bitten child, must report it by the end of the next working day (Section 47-5-90)."),
           ("Will my neighbor have to pay out of pocket?", "Usually not, if the neighbor has homeowner's or renter's liability coverage that applies. That policy responds to the claim, subject to its limits and exclusions.")])

# ----------------------------------------------------------------------------- 3. Motorcycle season and the helmet question
post(hero_image="cover-motorcycle-season.jpg",
     hero_caption="A motorcycle on a back road under moss-draped live oaks (illustration)", category="Motorcycle accidents",
     title="Motorcycle Season in the Lowcountry: The Helmet Question and Your Claim",
     description="After a motorcycle crash, riders ask whether not wearing a helmet hurts the claim. What South Carolina's helmet and eye protection laws say, and what they leave to the facts.",
     h1="Motorcycle season in the Lowcountry: the helmet question and your claim",
     summary="Riders 21 and over may ride without a helmet in South Carolina. What that can mean when a driver turns left in front of you.",
     lead="Motorcycle collisions in South Carolina peaked on Saturdays in 2024, according to the SCDPS Fact Book. After a crash, the helmet question tends to come up early.",
     body=(
         '<h2>The call</h2>'
         '<p>Picture this call. “A car turned left in front of me at a light. I went over the hood. I wasn\'t wearing a helmet. The adjuster says that\'s a problem.” The adjuster may well raise the helmet. South Carolina\'s statutes say less about it than many riders expect, and it helps to know what they do say before that conversation goes further.</p>'
         '<h2>What the law says</h2>'
         f'<p>Under {cite("helmet", "Section 56-5-3660")}, riders under 21, whether operating the motorcycle or riding as passengers, must wear a helmet approved by the Department of Public Safety, with a neck or chin strap and reflective material on both sides. Operators under 21 must also wear goggles or a face shield unless the motorcycle has a windscreen that meets the department\'s specifications (Sections 56-5-3670 and 56-5-3680). The eye protection rule does not apply to passengers. Riders 21 and older are not required by statute to wear a helmet. {A(MOTO + "/motorcycle-helmet-law-injury-lawyers-in-summerville", "The helmet law explained")}.</p>'
         '<h2>What insurers do with it</h2>'
         '<p>Insurers sometimes raise helmet use. They may suggest the rider shares the blame, or argue that a helmet would have made a head injury less severe. South Carolina\'s statutes set the helmet rule for riders under 21 but do not say how helmet use affects an injury claim. Whether it matters in a given case is a question of fact. It can turn on what caused the crash, which injuries the rider has, and what the medical evidence shows.</p>'
         f'<p>Fault is a separate question. South Carolina compares fault, and an injured person can recover if their own negligence is not greater than the other side\'s. A rider found more than 50 percent at fault recovers nothing, and a smaller share reduces the award by that share. {A(CARP + "/how-comparative-negligence-works-in-south-carolina", "How comparative negligence works")}.</p>'
         '<h2>The crash the numbers point to</h2>'
         f'<p>Statewide in 2024, officers recorded the other vehicle\'s driver as contributing in 56.4 percent of multi-vehicle motorcycle collisions, and the motorcycle driver in 40.4 percent, according to the {ext(FACTBOOKS, "SCDPS Fact Book")}. In Dorchester County, failure to yield the right of way was the contributing factor listed most often on crash reports that year (986), and the county counted 66 motorcyclists among its crash victims, 7 of whom died.</p>'
         f'<p>A left turn across a rider\'s path raises the yield rule. Section 56-5-2320 requires a driver turning left to yield to oncoming traffic that is in the intersection or close enough to be an immediate hazard. Section 56-5-3640 entitles a motorcycle to the full use of its lane. A violation does not automatically put all the fault on the turning driver, because South Carolina still compares fault. {A(MOTO + "/left-turn-motorcycle-accident-lawyers-in-summerville", "Left-turn motorcycle crashes")}.</p>'
         '<h2>The safety point, plainly</h2>'
         f'<p>Frost Law Group represents riders, and we still ask every rider to wear a helmet. SCDPS counted 132 motorcyclists killed on South Carolina roads in 2024, about one every 2.8 days. For more on helmets, see {link("nhtsa", "NHTSA")} and the {link("iihs_motorcycle", "Insurance Institute for Highway Safety")}. If you were not wearing one and a careless driver hurt you, talk with a lawyer before you accept an adjuster\'s view of what that means for your claim.</p>'
         + callout("<b>Frost first:</b> if an adjuster says the helmet lowers what your claim is worth, do not argue the point on the phone. Call us, and let a lawyer look at the crash and the medical records first.")
     ),
     sources=[("S.C. Code §§ 56-5-2320, 56-5-3640 and 56-5-3660 to 56-5-3700 (left turns, lane use, helmets and eye protection)", CODE_56_5, False),
              ("SCDPS, Traffic Collision Fact Books", FACTBOOKS, False)]
             + src("nhtsa", "iihs_motorcycle", "reddit_charleston"),
     related=[MOTO, MOTO + "/motorcycle-helmet-law-injury-lawyers-in-summerville", MOTO + "/left-turn-motorcycle-accident-lawyers-in-summerville"],
     faqs=[("Can the insurance company reduce my claim because I was not wearing a helmet?", "South Carolina's statutes do not answer that. They require helmets only for riders under 21 and say nothing about how helmet use affects an injury claim. Whether it matters in a given case is a question of fact, so have a lawyer review the crash and the medical records before you accept an adjuster's position."),
           ("Do motorcycle passengers in South Carolina need eye protection?", "Not under the statute. Riders and passengers under 21 must wear a helmet, but the goggles or face shield rule in Section 56-5-3670 applies only to operators under 21, and not when the motorcycle has a windscreen that meets state specifications."),
           ("Is lane-splitting legal in South Carolina?", "No. Section 56-5-3640 bars riding between lanes of traffic or between rows of vehicles. Motorcycles may ride no more than two abreast in one lane.")])

# ----------------------------------------------------------------------------- 4. Goose Creek UM
post(hero_image="cover-goose-creek-uninsured.jpg",
     hero_caption="A damaged sedan stopped against the side of an SUV near a traffic light (illustration)", category="Car accidents",
     title="Hit by an Uninsured Driver in Goose Creek? Your Own Policy May Be the Answer",
     description="When the driver who hit you in Goose Creek had no insurance or too little, the UM coverage on every South Carolina policy, and any UIM coverage you carry, may pay. How it works and what to avoid.",
     h1="Hit by an uninsured driver in Goose Creek? Your own policy may be the answer",
     summary="How the uninsured motorist coverage on every South Carolina policy, and any underinsured coverage you carry, can pay when the other driver's insurance cannot.",
     lead="The other driver's insurance card was expired, or the policy was cancelled, or the driver drove off. The money for your claim may come from your own policy.",
     body=(
         '<h2>When the other driver has little or no insurance</h2>'
         f'<p>South Carolina requires every auto policy to carry liability coverage of at least $25,000 per person and $50,000 per accident for bodily injury, and $25,000 for property damage ({cite("min_liability", "Section 38-77-140")}). Some drivers carry only that minimum, and some carry nothing. When one of them hits you, the coverage that answers may be on your own policy.</p>'
         f'<p>Goose Creek is Berkeley County\'s largest municipality. SCDOT names US 52 through the city North and South Goose Creek Boulevard and US 176 St. James Avenue, and it counted about 66,900 vehicles a day in 2024 on US 52 between the Charleston County line and St. James Avenue. Across all of Berkeley County, US-52 had 653 collisions in 2024, 10 of them fatal, and US-176 had 569, according to the {ext(FACTBOOKS, "SCDPS Fact Book")}.</p>'
         '<h2>The coverage you already have</h2>'
         + steps([
             ("Uninsured motorist (UM).", f" Required on every South Carolina policy, at limits of at least 25/50/25 ({cite('um', 'Section 38-77-150')}). It pays what you are legally entitled to recover from an uninsured driver, up to your UM limits. It also covers a hit-and-run by an unknown driver when the conditions in Section 38-77-170 are met."),
             ("Underinsured motorist (UIM).", f" Optional. Insurers must offer it up to your liability limits ({cite('uim', 'Section 38-77-160')}), and you are not required to buy it. It pays when your damages exceed the at-fault driver's liability limits. Under Section 38-77-350(E), if you did not return the signed offer form within 30 days, the insurer must add UM and UIM at the same limits as your liability coverage, so the offer form is worth checking."),
             ("Stacking.", f" Stacking means combining UM or UIM coverage from more than one vehicle. Under the S.C. Supreme Court's decision in {ext(CONCRETE, 'Concrete Services v. USF&amp;G')}, only the named insured, a spouse or a relative living in the household may stack. Guests and permissive drivers may not. Section 38-77-160 also limits how much coverage can be combined. Whether stacking applies depends on the policies and the facts, so have a lawyer check before you assume it does or does not."),
         ])
         + f'<p>The full explanation, including the unknown-driver rules and how UIM claims are settled, is on {A(CARP + "/uninsured-motorist-coverage-in-south-carolina", "uninsured motorist coverage in South Carolina")}.</p>'
         '<h2>Mistakes that can hurt a UM or UIM claim</h2>'
         + checks([
             "Settling with the at-fault driver's insurer before talking to a lawyer about your UIM claim. Section 38-77-160 bars any policy clause that requires your UIM carrier's consent to that settlement, but the statute sets its own rules. Your UIM carrier must be served with the suit papers and has 30 days to appear, and when the at-fault driver's insurer pays its liability limits, the UIM carrier may take over the defense. A lawyer can walk you through those rules before you sign anything.",
             "Waiting too long to report a hit-and-run. To use UM coverage against an unknown driver, Section 38-77-170 requires a report to the police within a reasonable time under the circumstances. The claim also needs physical contact with the other vehicle, a witness other than the owner or driver of your vehicle who signs an affidavit, or, since May 2024, a recording that shows the unknown vehicle caused the crash. Save any video of the crash.",
             "Understating the injury to your own insurer. Your policy likely requires you to report the crash and cooperate. Keep in mind that in a UM or UIM suit, your own carrier is served with the papers and may defend the case in the at-fault driver's name.",
         ])
         + '<h2>Goose Creek specifics</h2>'
         + '<p>Inside the city, the Goose Creek Police Department works crashes. It investigated 1,284 collisions in 2024, according to the SCDPS Fact Book. The department keeps reports from the preceding 14 days at its office on North Goose Creek Boulevard. A report is free in person for parties the report lists as not at fault, and $5 for others. Across Berkeley County that year, the Highway Patrol investigated 3,468 of the county\'s 6,536 collisions.</p>'
         + f'<p>The at-fault driver\'s traffic ticket may be heard in Goose Creek Municipal Court, but municipal courts have no civil jurisdiction, so an injury claim is not filed there. Berkeley County\'s Court of Common Pleas sits at the {ext(SCCOURTS_BERKELEY, "Berkeley County Courthouse")}, 300-B California Avenue in Moncks Corner, in the Ninth Judicial Circuit. For more on the city, see {A(BERK + "/goose-creek-car-accident-lawyers", "car accident claims in Goose Creek")}.</p>'
         + callout("<b>Frost first:</b> before you accept a policy-limits offer from the other driver's insurer, call us. If you may have a UIM claim, the statute sets notice rules for your own carrier, and a lawyer should go over them with you first.")
     ),
     sources=[("S.C. Code §§ 38-77-140, 38-77-150, 38-77-160, 38-77-170 and 38-77-350 (minimum, UM and UIM coverage, unknown drivers, offer forms)", CODE_38_77, False),
              ("S.C. Department of Insurance, automobile insurance", DOI_AUTO, False),
              ("Concrete Services, Inc. v. United States Fidelity & Guaranty Co., S.C. Sup. Ct. Op. No. 24773 (1998)", CONCRETE, False),
              ("SCDPS, Traffic Collision Fact Books", FACTBOOKS, False),
              ("S.C. Judicial Branch, Berkeley County courts", SCCOURTS_BERKELEY, False)]
             + src("nextdoor_goose_creek"),
     related=[CARP + "/uninsured-motorist-coverage-in-south-carolina", CARP + "/hit-and-run-accident-lawyers-in-summerville",
              BERK + "/goose-creek-car-accident-lawyers"],
     faqs=[("What if the driver who hit me drove off?", "Your UM coverage can apply to an unknown driver if the crash was reported to the police within a reasonable time, you were not careless in failing to identify the other driver, and there was physical contact, a witness other than the owner or driver of your vehicle who signs an affidavit, or a recording showing the unknown vehicle caused the crash (Section 38-77-170). The recording option was added in 2024."),
           ("Do I have UIM coverage?", "Check the declarations page of your policy for underinsured motorist limits. If none appear, ask whether you returned a signed offer form. Under Section 38-77-350(E), if the signed form was not returned within 30 days, the insurer must add UM and UIM at the same limits as your liability coverage.")])


# ============================================================================= October 2026 posts
# Four posts drafted by Legal Leads Group (Daylin Rockwood) and loaded 2026-10-06. Changes from the drafts: the phone is the
# DNI number, fee lines came out of the copy (the template carries them), internal links point at live slugs, Rule 7.4
# words were reworded, and the Goose Creek post now says the under-50% rule dates to 2005 and minor tolling extends the
# deadline. Each post keeps its FAQ section in the copy, and faq_ld() gives it FAQPage markup. The H1 and the slug are
# the same string. Titles and descriptions are in meta.py. Legal and local facts were checked against the sources
# listed with each post and the page kit research. Featured images are licensed Canva stock photos (see BUILD-NOTES.md),
# each file named for the post's final CTA heading, with a caption that describes what the photo shows.
TRUCKP = "truck-accident-attorneys-in-summerville"
SLIPP = "slip-and-fall-attorneys-in-summerville"
DORCH = "personal-injury-attorneys-in-dorchester-county"
CHS = "personal-injury-attorneys-in-charleston-county"

CODE_15_7 = "https://www.scstatehouse.gov/code/t15c007.php"
CODE_15_32 = "https://www.scstatehouse.gov/code/t15c032.php"
CODE_15_38 = "https://www.scstatehouse.gov/code/t15c038.php"
CODE_15_78 = "https://www.scstatehouse.gov/code/t15c078.php"
CODE_22_3 = "https://www.scstatehouse.gov/code/t22c003.php"
CODE_27_40 = "https://www.scstatehouse.gov/code/t27c040.php"
USC_2401 = "https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title28-section2401&num=0&edition=prelim"
ECFR_387_3 = "https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-387/subpart-A/section-387.3"
ECFR_387_9 = "https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-387/subpart-A/section-387.9"
ECFR_382_303 = "https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-382/subpart-C/section-382.303"
SCDPS_FATAL = "https://scdps.sc.gov/fatalities"
DPH_TRAUMA = "https://dph.sc.gov/professionals/healthcare-quality/ems-and-trauma/sc-trauma-system"
MUSC_TRAUMA = "https://muschealth.org/medical-services/emergency/trauma"
SIMS = "https://www.sccourts.org/media/opinions/HTMLFiles/COA/3291.htm"
WINTERSTEEN = "https://www.sccourts.org/media/opinions/HTMLFiles/SC/25254.htm"
ABC4_MONCKS = "https://abcnews4.com/news/local/moncks-corner-receives-12m-grant-for-new-sidewalks-pedestrian-safety-project-infastructure-south-carolina"
LIVE5_LEATHERMAN = "https://www.live5news.com/2026/06/25/sc-ports-pause-leatherman-terminal-operations-aug-1-consolidate-container-work/"


def faq_ld(p, heading):
    """FAQPage markup from the post's own FAQ section: the H3 questions under ``heading`` and the paragraphs after each."""
    sec = re.search(r"<h2>" + re.escape(heading) + r"</h2>(.*?)(?=<h2>|$)", p["body"], re.S)
    out = []
    for m in re.finditer(r"<h3>(.*?)</h3>(.*?)(?=<h[2-5]>|$)", sec.group(1), re.S):
        a = " ".join(re.findall(r"<p>(.*?)</p>", m.group(2), re.S))
        out.append((m.group(1), re.sub(r"<[^>]+>", "", a)))
    p["_faq_schema"] = out


# ----------------------------------------------------------------------------- 5. Summerville car accident medical bills
p5 = post(hero_image='talk-with-a-summerville-car-accident-lawyer-at-frost-law-group-today.jpg',
     hero_caption="A man wearing a cervical collar holds the back of his neck during a visit to a doctor's office.",
     category='Car accidents', date='2026-09-16', modified='2026-09-16',
     title='Summerville Car Accident Lawyer for Medical Bills | Call Now',
     description='South Carolina has no required PIP. Learn how a Summerville car accident lawyer lines up Med Pay, health insurance, and UM coverage. Get a free review.',
     h1='How Does a Summerville Car Accident Lawyer Get Your Medical Bills Paid?',
     summary="How Med Pay, health insurance, the at-fault driver's policy and your own UM and UIM coverage line up to pay medical bills after a Summerville crash.",
     body=(
         "<p>A Summerville car accident lawyer gets your medical bills paid by lining up every source in the right order. That means your own Med Pay and health insurance now, the at-fault driver's liability coverage at settlement, and your uninsured or underinsured motorist coverage when that driver's policy falls short. South Carolina has no required PIP, so the order matters.</p>"
         "<p>Frost Law Group is a husband-and-wife personal injury firm based on Linwood Lane in Summerville. Tara Frost is a former Dorchester County Magistrate Judge. Jack Frost spent 14 years in law enforcement with the Summerville Police Department and the Charleston County Sheriff's Office. You work directly with an attorney, not a call center.</p>"
         '<p>If the bills from your Summerville crash are already piling up, call Frost Law Group at ' + TEL + ' for a free consultation.</p>'
         '<h2>Who Pays Medical Bills After a Car Accident in Summerville?</h2>'
         '<p>Here is the short version. The driver who caused the crash owes you for your medical care, but their insurer pays nothing until the claim settles. That gap is where people get hurt twice. Frost Law Group\'s <a href="[[car-accident-attorneys-in-summerville]]">car accident representation</a> starts by finding every policy that can cover you while the fault claim moves forward.</p>'
         "<p>So who pays today, and who pays at the end? Your own coverage handles the first wave of bills. The at-fault driver's insurer repays the full loss when the case resolves. Your uninsured or underinsured motorist coverage fills the hole if that driver carried too little. Getting that sequence right keeps your credit intact and your claim at full value.</p>"
         "<h2>Why South Carolina's At-Fault Rules Change Who Pays First</h2>"
         '<p>Many drivers assume their own insurer pays their injury bills no matter who caused the wreck. That is true in no-fault states. It is not true here, and the difference shapes every decision you make in the first weeks after a crash on I-26 or Main Street.</p>'
         "<p>South Carolina puts the cost of a crash on the driver who caused it. Your job is to prove fault and damages. Your insurer's job is limited to the coverages you bought, and some of those are optional. Knowing which ones you carry tells you who pays first.</p>"
         '<h3>What Section 38-77-144 Says About PIP and Med Pay</h3>'
         '<p><a href="https://www.scstatehouse.gov/code/t38c077.php" rel="noopener" target="_blank">South Carolina Code Section 38-77-144</a> states that the state mandates no personal injury protection coverage. That surprises a lot of people who moved to Summerville from Florida or Pennsylvania. The same section also protects you. If you bought medical payments coverage, the insurer cannot take it back through subrogation or subtract it from what you recover later. That makes Med Pay one of the best dollars on your policy.</p>'
         '<h3>The 25/50/25 Liability Minimum Runs Out Fast</h3>'
         "<p>Section 38-77-140 sets the minimum liability limits at $25,000 for one person's injuries and $50,000 for everyone hurt in one crash. Another $25,000 covers property damage. Plenty of drivers on Berlin G. Myers Parkway carry exactly that minimum. A serious injury can use it up before you finish treatment. Once the policy is exhausted, the insurer stops paying and the rest has to come from somewhere else.</p>"
         '<h4>How One Hospital Stay in Summerville Can Reach the $25,000 Limit</h4>'
         '<p>Many Summerville crash victims start at HCA Healthcare Summerville Hospital at 295 Midland Parkway, which runs a 24-hour emergency room. An ambulance ride, imaging, and an admission all land on the same claim. Add surgery and months of therapy, and the minimum policy can be gone. Ask the hospital for an itemized bill early.</p>'
         '<h5>Transfers to the Level I Trauma Center in Charleston</h5>'
         '<p>Severe injuries often mean a transfer to the Medical University of South Carolina in downtown Charleston. Its health system says it runs the only Level I trauma program serving the Lowcountry. A transfer adds a second hospital, a second set of physicians, and a much larger bill. Each provider bills you separately.</p>'
         '<h5>Follow-Up Care After You Leave the ER</h5>'
         '<p>The emergency room is usually the smallest part of the total. Orthopedic visits, physical therapy, and pain management can run for months. Each of those bills belongs in your claim, so keep every statement and receipt. Future care counts too when a doctor documents it.</p>'
         '<h4>When Several People Share One $50,000 Limit</h4>'
         '<p>The $50,000 per-crash limit is a shared pot. If three people are hurt in the same wreck, all three claims draw from it. Your share can end up far below $25,000, even with a perfectly clear fault case. That is exactly when your own coverage has to carry more of the load.</p>'
         '<h2>Which Coverages Pay Your Bills Before the Case Settles?</h2>'
         '<p>You should not have to wait a year to get a doctor paid. Several sources can pay now while the liability claim builds. Some of them want their money back later, and some do not.</p>'
         '<p>These are the sources a Summerville car accident lawyer checks first.</p>'
         "<ul><li>Medical payments coverage on your own auto policy pays regardless of fault.</li><li>Your health insurance pays under its normal terms, subject to any repayment clause.</li><li>Medicare or Medicaid pays if you are enrolled, with federal repayment rights attached.</li><li>A provider may agree to wait for payment under a letter of protection.</li><li>Your uninsured or underinsured motorist coverage pays when the other driver's policy falls short.</li></ul>"
         '<p>Each source comes with its own rules. The order you use them in can change how much of the settlement you keep.</p>'
         '<h3>Med Pay on Your Own Auto Policy</h3>'
         '<p>Med Pay is optional in South Carolina, so check your declarations page. If you have it, use it early. It pays covered medical expenses up to your limit without a fault fight. Under Section 38-77-144, that money is not subject to subrogation or setoff. Common Med Pay limits are small, but even a few thousand dollars can cover an ER copay and the first rounds of therapy. Submit those bills to your own adjuster as soon as they arrive.</p>'
         '<h3>Health Insurance and the Repayment Question</h3>'
         '<p>Your health plan should pay your crash bills under its normal terms. You still owe your copays and deductible. Many plans also expect repayment from your injury settlement. Know which kind of plan you have before you sign anything. Give every provider your health insurance card, even when the office asks for auto insurance first. Billing through your plan usually means lower negotiated rates on the same care.</p>'
         '<h4>Employer Plans and Reimbursement Clauses</h4>'
         '<p>Many employer health plans include a reimbursement clause in the plan documents. The plan may claim part of your settlement to cover what it paid. Some of these claims can be negotiated down. Ask for the plan document in writing, not a phone summary. The exact wording decides what the plan can take.</p>'
         '<h4>Medicare and Medicaid Repayment After a Summerville Crash</h4>'
         '<p>Medicare pays conditionally when a liability insurer has not paid yet. The federal Medicare Secondary Payer Act requires repayment once your case settles. Federal Medicaid law also requires states to pursue liable third parties. Your settlement has to account for both before any money goes out. Skipping that step can create a debt later.</p>'
         '<h2>What If the Other Driver Has Little or No Insurance in South Carolina?</h2>'
         '<p>Here is where many claims stall. The driver who hit you on I-26 has no policy, or has only the state minimum. Does that mean your bills go unpaid? Not if your own policy is set up right.</p>'
         '<p>South Carolina builds two protections into auto policies. One is mandatory and one is optional. Pull your declarations page and look for both. Many Summerville families carry the mandatory piece and never realize the optional piece was offered. If you are not sure what you bought, your agent can send a copy of the page the same day.</p>'
         '<h3>Uninsured Motorist Coverage Is Mandatory</h3>'
         '<p>Section 38-77-150 requires every South Carolina auto policy to include uninsured motorist coverage. It must match the 25/50/25 minimums for injuries. It also includes at least $25,000 for property damage, with up to a $200 exclusion. If an uninsured driver hurts you, your own insurer pays what that driver would have owed. Your insurer can still dispute fault and damages. Treat the UM claim with the same care as any other injury claim.</p>'
         '<h3>Underinsured Motorist Coverage Is Optional but Adds Real Money</h3>'
         "<p>Section 38-77-160 requires carriers to offer underinsured motorist coverage up to your own liability limits. You decide whether to buy it. UIM pays when your damages exceed the at-fault driver's limits. For a serious injury, it is often the largest check in the case. The premium is usually modest compared with the protection. Check whether you signed a form turning it down. That form can affect what you can claim.</p>"
         '<h4>Excess UM or UIM Follows the Car in the Crash</h4>'
         "<p>If you carry more than the basic limits, Section 38-77-160 ties that extra coverage to the vehicle involved in the crash. Were you driving your own car? Then that car's coverage controls. This rule stops you from adding the extra limits from every vehicle in your household. Plan your limits with that in mind.</p>"
         '<h4>When None of Your Cars Was in the Wreck</h4>'
         '<p>Were you a passenger or pedestrian when it happened? The same section says coverage is then available only up to the limit on any one of your vehicles. That still gives you real protection. It also means your highest limit matters more than the number of cars you insure.</p>'
         "<h2>How Fault and Deadlines Affect Your Summerville Car Accident Lawyer's Claim</h2>"
         '<p>Every dollar of medical expense runs through two filters. The first is fault. The second is the calendar. Miss either one and the bills can land back on you.</p>'
         '<p>Keep these South Carolina deadlines in front of you.</p>'
         "<ul><li>You have three years to file most injury lawsuits under Section 15-3-530.</li><li>You have two years under the Tort Claims Act when a government vehicle caused the crash.</li><li>That government deadline extends to three years if you file a verified claim first.</li><li>A minor's deadline is tolled, but Section 15-3-40 limits how long that tolling lasts.</li></ul>"
         '<p>Deadlines are only half the picture. Fault decides how much of your medical expense the other side pays.</p>'
         '<h3>Comparative Fault Under Nelson v. Concrete Supply</h3>'
         "<p>The South Carolina Supreme Court set the rule in Nelson v. Concrete Supply Co. in 1991. You can recover if your fault is not greater than the defendants' fault. Your award drops by your percentage. So a driver found 20% at fault recovers 80% of the medical bills and other damages. Insurers push hard to raise your share. Photos, witness names, and the police report are how you push back.</p>"
         '<h3>Three Years to File Under Section 15-3-530</h3>'
         '<p>Section 15-3-530 gives you three years from the crash to file an injury lawsuit. Three years sounds generous, but treatment often runs a year or more. Insurers know when the clock is close. Waiting weakens your position on every bill. Filing before the deadline keeps the pressure on. It also lets your lawyer use subpoenas to get records the insurer will not share. Start the conversation well before the third anniversary of the crash.</p>'
         '<h4>Filing at the Dorchester County Courthouse in St. George</h4>'
         '<p>Most of Summerville sits in Dorchester County. A lawsuit from a crash there usually goes to the Dorchester County Courthouse at 5200 East Jim Bilton Boulevard in St. George. That court is part of the First Judicial Circuit. A crash on the Berkeley or Charleston County side of town can send the case to a different courthouse.</p>'
         '<h4>Two Years When a Government Vehicle Hit You</h4>'
         '<p>A town truck, a county vehicle, or a school bus changes the rules. The South Carolina Tort Claims Act, Section 15-78-110, sets a two-year filing deadline. Section 15-78-120 caps recovery at $300,000 per person and $600,000 per occurrence. Those caps make your own UIM coverage even more important.</p>'
         '<h2>What Summerville Crash Victims Should Do to Protect Their Medical Claim</h2>'
         '<p>The first two weeks after a wreck decide how clean your medical claim will be. Dorchester County is seeing real losses on its roads. The <a href="https://scdps.sc.gov/fatalities" rel="noopener" target="_blank">South Carolina Department of Public Safety</a> reports 18 traffic deaths in Dorchester County from January 1 through September 13, 2026, compared with 15 in the same stretch of 2025. Those figures are preliminary.</p>'
         '<p>Want your bills paid without a fight over paperwork? Take these steps.</p>'
         "<ul><li>Get medical care right away and follow every treatment plan.</li><li>Request your collision report as soon as it is available.</li><li>Tell your own insurer about the crash and ask whether you have Med Pay.</li><li>Keep every bill, explanation of benefits, and receipt in one folder.</li><li>Do not sign a release or give a recorded statement to the other driver's insurer.</li></ul>"
         '<p>Those records become the backbone of the demand your lawyer sends. Missing pieces cost money.</p>'
         '<h3>Getting Your Report From the Summerville Police Department</h3>'
         "<p>Crashes inside town limits are handled by the Summerville Police Department on North Cedar Street. The department releases collision reports through CrashDocs. That report names the drivers, the insurers, and the officer's notes on fault. Jack Frost began his law enforcement career with that department, and those years shape how the firm reads a collision report. Read yours closely and flag any mistakes quickly. A wrong insurer name can delay every payment.</p>"
         '<h3>Crashes Outside Town Limits on I-26 and Rural Roads</h3>'
         '<p>Section 56-5-1260 tells drivers where to report an injury crash. Inside a town, you notify the local police. Outside town limits, it is the county sheriff or the nearest South Carolina Highway Patrol office. You can request those reports from the SCDMV online or with Form FR-50. Commercial vehicles on I-26 add more parties, so read about <a href="[[truck-accident-attorneys-in-summerville]]">truck accident claims</a> if a semi was involved.</p>'
         '<h2>Frequently Asked Questions About Medical Bills After a Summerville Car Accident</h2>'
         '<p>These are the questions Summerville drivers ask most after the first bills arrive. Each answer reflects South Carolina law as of September 2026. Your policy language and the facts of your crash can change the result, so treat these as a starting point. Life-changing injuries raise different issues, and our <a href="[[catastrophic-injury-attorneys-in-summerville]]">catastrophic injury</a> page covers those.</p>'
         "<p>Don't see your question here? Write it down and bring it to your free consultation. Bring your declarations page and your first few bills too. Those three items answer most coverage questions in a single meeting.</p>"
         '<h3>Does South Carolina Require PIP Coverage?</h3>'
         '<p>No. Section 38-77-144 says South Carolina mandates no personal injury protection coverage. Med Pay is optional and pays regardless of fault if you bought it.</p>'
         '<h3>Should I Use My Health Insurance After a Car Accident in Summerville?</h3>'
         '<p>Yes, in most cases. Your health plan pays at negotiated rates and keeps accounts out of collections. Expect the plan to ask for repayment from your settlement.</p>'
         '<h3>Can a Hospital Bill Me Before My Case Settles?</h3>'
         '<p>Yes. The provider is owed payment whether your claim has resolved. Using Med Pay, health insurance, or a letter of protection can hold off collections.</p>'
         "<h3>What If My Medical Bills Are Higher Than the Other Driver's Policy?</h3>"
         '<p>Look to your underinsured motorist coverage under Section 38-77-160. If you did not buy UIM, the other driver may still be personally responsible for the rest.</p>'
         '<h3>Does Being Partly at Fault Mean I Pay My Own Bills?</h3>'
         "<p>Not entirely. Under Nelson v. Concrete Supply, you recover if your fault is not greater than the defendants' fault. Your award is reduced by your percentage.</p>"
         '<h2>Talk With a Summerville Car Accident Lawyer at Frost Law Group Today</h2>'
         '<p>Medical bills do not wait for an insurance adjuster to finish reviewing your file. The sooner the right coverages are lined up, the less stress lands on you and your family.</p>'
         '<p>A Summerville car accident lawyer at Frost Law Group can review your policy, identify every source of payment, and deal with the insurers so you can focus on getting better. Tara and Jack Frost both grew up in Summerville and practice here today. You can learn more about them on the <a href="[[about]]">about page</a>.</p>'
         '<p>Call Frost Law Group at ' + TEL + ' any time, 24 hours a day. Your consultation is free. Prefer to write? Use the <a href="[[contact]]">contact page</a> and the firm will reach out to you.</p>'
         '<p>Hurt in a crash? Call Frost First. See all the firm\'s <a href="[[practice-areas]]">practice areas</a> to find the help that fits your case.</p>'
     ),
     sources=[("S.C. Code §§ 38-77-140, 38-77-144, 38-77-150 and 38-77-160 (liability minimums, PIP and Med Pay, UM and UIM coverage)", CODE_38_77, False),
              ("S.C. Code §§ 15-3-40 and 15-3-530 (filing deadlines)", CODE_15_3, False),
              ("S.C. Code §§ 15-78-110 and 15-78-120 (Tort Claims Act deadline and caps)", CODE_15_78, False),
              ("S.C. Code § 56-5-1260 (reporting an injury crash)", CODE_56_5, False),
              ("MUSC Health, trauma care", MUSC_TRAUMA, False),
              ("SCDPS, traffic fatalities by county", SCDPS_FATAL, False),
              ("SCDMV, collision reports", DMV_REPORTS, False)],
     related=[CARP, CARP + "/uninsured-motorist-coverage-in-south-carolina", CARP + "/how-much-is-my-car-accident-case-worth", DORCH])
faq_ld(p5, 'Frequently Asked Questions About Medical Bills After a Summerville Car Accident')

# ----------------------------------------------------------------------------- 6. Goose Creek motorcycle shared fault
p6 = post(hero_image='call-a-goose-creek-motorcycle-accident-lawyer-before-you-accept-a-reduced-offer.jpg',
     hero_caption='A crashed motorcycle lies on its side in the grass beside a paved road.',
     category='Motorcycle accidents', date='2026-09-21', modified='2026-09-21',
     title='Goose Creek Motorcycle Accident Lawyer | Call Today',
     description='South Carolina requires a helmet only under 21. A Goose Creek motorcycle accident lawyer answers the helmet argument insurers use. Call for a free review.',
     h1='What Can a Goose Creek Motorcycle Accident Lawyer Do If You Were Partly at Fault?',
     summary='A rider who shares the blame can still recover in South Carolina. How insurers split fault after a Goose Creek crash, what the helmet law says, and what changed in 2026.',
     body=(
         '<p>South Carolina still pays you when you share the blame. A Goose Creek motorcycle accident lawyer can win your claim as long as your fault is not greater than the fault of the driver you sue. At 50 percent you recover half your damages. At 51 percent you recover nothing at all.</p>'
         '<p>Frost Law Group works from one office on Linwood Lane in Summerville and handles injury claims across Berkeley, Dorchester, and Charleston counties. It is a husband-and-wife firm. Tara L. Frost and Jack C. Frost both graduated from the Charleston School of Law. You work directly with an attorney rather than a call center.</p>'
         '<p>If a driver turned across your lane in Goose Creek, call Frost Law Group at ' + TEL + ' for a free case review.</p>'
         '<h2>How Does South Carolina Decide Fault in a Goose Creek Motorcycle Crash?</h2>'
         '<p>Fault is not a yes or no question in this state. It is a percentage, and somebody assigns one to every driver involved. The motorcycle injury team at <a href="[[motorcycle-accident-attorneys-in-summerville]]">Frost Law Group</a> sees the same move in almost every rider file. The adjuster does not deny the claim outright. The adjuster offers a number and quietly shaves a piece off it for something you supposedly did wrong.</p>'
         '<p>That quiet shave is the whole fight. Move your share from 40 percent down to 10 percent and the same crash is worth a different amount on identical medical bills. South Carolina calls the rule modified comparative negligence. The rule has a hard ceiling, and riders run into it more often than drivers do.</p>'
         '<h3>The 51 Percent Bar and Why 50 Percent Still Recovers</h3>'
         '<p>South Carolina adopted modified comparative negligence in Nelson v. Concrete Supply Co., decided in 1991. You recover as long as your negligence is not greater than the negligence of the party you sue. Your award then drops by your own percentage. A rider found half at fault still collects, and a rider found 51 percent at fault collects nothing. Run the arithmetic on a $100,000 claim and the stakes get clear.</p>'
         '<ul><li>A rider found 10 percent at fault collects $90,000 of that figure.</li><li>A rider found 40 percent at fault collects $60,000 of the same figure.</li><li>A rider found 50 percent at fault collects $50,000 and stays inside the bar.</li><li>A rider found 51 percent at fault collects nothing, however severe the injuries were.</li></ul>'
         '<p>Those numbers are arithmetic, not a forecast about any real case. The percentage is the single most valuable number in your file.</p>'
         '<h3>What Changed for Shared Fault Cases on January 1, 2026</h3>'
         '<p>Shared fault law in South Carolina moved this year. Section 15-38-15 was rewritten by <a href="https://www.scstatehouse.gov/code/t15c038.php" rel="noopener" target="_blank">2025 Act No. 42</a>, and the new version applies to claims arising after January 1, 2026. The change lands hardest in crashes with more than one careless driver. That describes a lot of afternoon wrecks on Highway 52. Two changes matter to riders, and both of them move money.</p>'
         '<h4>Fault Now Lands on Drivers Who Never Get Sued</h4>'
         '<p>Under the amended statute, a jury can put a share of fault on someone who is not a defendant. The nonparty has to be disclosed within 180 days, and the defense usually names one. A driver who left the scene, a tortfeasor who already settled, or a trucking company that never got served can each take a slice. Every slice assigned elsewhere is a slice not assigned to you.</p>'
         '<h4>Nonparty Fault Now Counts Toward the 50 Percent Line</h4>'
         '<p>Since 2005, a defendant whose fault falls under 50 percent of the total has owed only its own share of your damages, and the amended statute keeps that rule. What changed is the total. Fault assigned to nonparties now counts, so a defendant can drop under the line more easily and avoid paying the rest. If the driver with the small policy carries most of the blame, and the business with real coverage carries 30 percent, your recovery can stall after a win. Sorting out who can actually pay belongs at the start of a case.</p>'
         '<h2>Which Blame Arguments Insurers Aim at Goose Creek Riders</h2>'
         '<p>Every rider claim in Berkeley County arrives with a script. The adjuster reads the collision report, picks a line, and builds a percentage around it. Berkeley County recorded 26 traffic deaths through September 13, 2026, after 28 through the same date in 2025 and 27 in 2024, according to <a href="https://scdps.sc.gov/fatalities" rel="noopener" target="_blank">South Carolina Department of Public Safety counts</a>. Carriers know those numbers too, and they price rider claims accordingly.</p>'
         '<p>These arguments repeat because they work on people who have never heard them before. Each one has an answer in the South Carolina code. Most fold quickly once a rider pushes back with the statute in hand.</p>'
         "<ul><li>You were speeding, based on nothing but the other driver's estimate.</li><li>You were splitting lanes, which is a real violation and needs a real answer.</li><li>You wore no helmet, even when the law required none at your age.</li><li>You were hard to see, as though visibility were your responsibility alone.</li><li>You waited two days to see a doctor, so the injury must be minor.</li></ul>"
         "<h3>Lane Position and a Motorcycle's Right to the Full Lane</h3>"
         '<p>Section 56-5-3640 gives every motorcycle the full use of a lane. No driver may operate in a way that deprives a rider of that lane. The same section sets limits on how riders use it, and those limits are where the defense goes hunting. Read the subsections in order, because the rule that protects you and the rule used against you sit two lines apart.</p>'
         '<h4>Passing in the Same Lane and Riding Between Traffic</h4>'
         '<p>Subsection (b) bars a rider from overtaking and passing inside the lane the other vehicle occupies. Subsection (c) bars operating between lanes of traffic or between adjacent rows of vehicles. Lane splitting is illegal here, so a rider who split a backed-up stretch of Highway 52 starts with a share of fault. That share is rarely 100 percent, and a driver who changed lanes without signaling still owns part of the crash.</p>'
         '<h4>Riding Two Abreast Is Legal and Not Proof of Recklessness</h4>'
         '<p>Two riders may share a single lane under the same section. More than two abreast is not allowed. Group rides on St. James Avenue can draw this accusation, and the statute answers it in one line. Point at the subsection, and the argument drops out of the file.</p>'
         "<h3>Speed Estimates That Rest on One Driver's Guess</h3>"
         "<p>A driver who never saw the motorcycle until impact makes a poor witness to its speed. Collision reports record the estimate anyway, and adjusters later quote it as fact. Skid measurements, damage patterns, and signal timing on Red Bank Road carry far more weight than a guess. Request the full report and the officer's diagram, not the summary page. A crash reconstructionist can convert that diagram into a speed range grounded in the physical evidence.</p>"
         '<h2>What a Goose Creek Motorcycle Accident Lawyer Does About the Helmet Argument</h2>'
         '<p>Helmet use comes up in nearly every rider file, including files where the rider wore one. Insurers raise it because it sounds like common sense to a jury. The question is not whether a helmet is a good idea. The question is whether your choice can legally cut your recovery.</p>'
         '<p>South Carolina law is narrower than the argument. The statute sets an age line and stops there. What the code leaves out about helmets matters as much as what it puts in, and that gap is where a careful answer lives.</p>'
         '<h3>South Carolina Requires a Helmet Only Under Age 21</h3>'
         '<p>Section 56-5-3660 makes it unlawful for a person under 21 to ride without an approved helmet. Section 56-5-3670 adds goggles or a face shield for operators under that same age. A rider who is 21 or older breaks no law by riding bare-headed through Goose Creek. That ends the negligence per se version of the argument before it starts. Nobody can call a legal choice a traffic violation.</p>'
         '<h3>Why Riders Get Less Protection Than Drivers Wearing Seat Belts</h3>'
         '<p>South Carolina wrote a protection into its seat belt statute. Section 56-5-6540(C) says a seat belt violation is not negligence per se, is not contributory negligence, and is not admissible in a civil action. The helmet sections carry no parallel sentence. So the defense may still argue that a bare head worsened a specific head injury. That argument gets answered with medicine and treating-physician testimony rather than with a statute.</p>'
         '<h2>Who Writes the Goose Creek Crash Report and Where Your Case Gets Filed</h2>'
         "<p>Two local facts shape a rider's claim before any lawyer sees it. One is the agency that writes the collision report. The other is the courthouse that would hear the case if the insurer refuses to pay a fair number.</p>"
         '<p>Goose Creek sits in Berkeley County, beside the Naval Weapons Station at Joint Base Charleston. That geography puts city officers, county deputies, state troopers, and sometimes federal drivers on the same roads. Each one changes the paperwork, and some of them change the deadline. Get both answers in the first week.</p>'
         '<h3>The Agency That Writes the Report Depends on the City Line</h3>'
         "<p>Section 56-5-1260 tells a driver in an injury crash to notify the local police department inside a municipality. Outside city limits, that notice goes to the county sheriff or the nearest Highway Patrol office. A wreck on St. James Avenue inside the city goes to the Goose Creek Police Department. A wreck farther up Highway 52 past the line can land with the Berkeley County Sheriff's Office or a state trooper. Collision reports themselves come from the SCDMV, online or with Form FR-50.</p>"
         '<h3>Berkeley County Courthouse in Moncks Corner and the Ninth Judicial Circuit</h3>'
         '<p>A Goose Creek crash suit is filed at the Berkeley County Courthouse at 300-B California Avenue in Moncks Corner. Berkeley County sits in the Ninth Judicial Circuit alongside Charleston County. Venue shapes scheduling and the jury pool your case would draw. Most claims settle, and the venue still shapes every offer an insurer puts on the table. Berkeley County jurors drive these same roads, which cuts both ways for a rider.</p>'
         '<h4>When a Government Vehicle Is in the Crash</h4>'
         '<p>A school bus, a county truck, or a state vehicle moves the claim into the South Carolina Tort Claims Act. Section 15-78-110 sets a two-year deadline, stretched to three years only when a verified claim goes in first. Section 15-78-120 caps damages at $300,000 per person and $600,000 per occurrence and bars punitive damages. A federal driver out of the Naval Weapons Station moves it again, because 28 U.S.C. Section 2401(b) requires a written claim to the agency within two years.</p>'
         '<h4>When the Other Driver Was Working at the Time</h4>'
         '<p>A delivery van, a contractor\'s pickup, or a tractor-trailer brings an employer into the case. Employer policies usually dwarf a personal auto policy, which is why <a href="[[truck-accident-attorneys-in-summerville]]">commercial vehicle claims</a> follow a different track. Employment status is a fact you prove with the report, the vehicle markings, and the driver\'s own words. Ask early, because companies preserve logs and dashcam video only when somebody demands it.</p>'
         '<h2>How Shared Fault Changes What a Goose Creek Motorcycle Claim Pays</h2>'
         '<p>Riders often assume the fault percentage comes off the settlement at the end, the way a fee does. It does not work that way. The percentage applies to the entire damage figure, and that figure includes items people forget to count.</p>'
         '<p>That is why a fight over 15 percentage points is worth more than a fight over one hospital bill. Build the damages number first, then defend the percentage. Prior results do not guarantee a similar outcome, and no honest answer here arrives with a promised figure. Here is what the percentage touches.</p>'
         '<ul><li>Emergency transport and trauma care are reduced by your percentage.</li><li>Future surgery, therapy, and medication count as damages and take the same cut.</li><li>Lost wages and lost earning capacity drop by the same share, overtime included.</li><li>Pain, suffering, and permanent scarring lose that percentage as well.</li><li>Repair or replacement of the motorcycle is trimmed the same way.</li></ul>'
         '<h3>The Math an Adjuster Runs Before the First Offer</h3>'
         "<p>An adjuster builds a damage number, picks a fault percentage, and multiplies. The first offer usually assumes a percentage nobody has proved yet. You may reject that assumption and ask what it rests on. Most of the time the answer is a single sentence in a collision report. That sentence can be challenged with photographs, witness names, and the officer's diagram.</p>"
         '<h4>Medical Bills and Wage Loss Get Cut by Your Percentage</h4>'
         '<p>Bills are the easiest number to prove and the easiest to undercount. Ambulance charges, imaging, orthopedic follow-up, and hardware for a shattered leg all belong in the file. Gaps in treatment hand the defense a second argument about causation. Keep every receipt and every work restriction note your doctor writes.</p>'
         '<h5>Trauma Care After a Highway 52 Crash</h5>'
         '<p>Riders thrown at highway speed usually leave Goose Creek by ambulance for trauma care in the Charleston area. That transfer produces two sets of bills and two sets of records. Request both, because the emergency record often holds the earliest description of how the crash happened. Severe cases become <a href="[[catastrophic-injury-attorneys-in-summerville]]">catastrophic injury claims</a> with a different damages model.</p>'
         '<h5>Wage Loss for Shift Workers and Contractors</h5>'
         '<p>Many Berkeley County riders work shift schedules with overtime built in. A flat hourly rate undercounts that loss badly. Pull a year of pay records instead of two recent stubs. Self-employed riders prove the loss with invoices, tax returns, and the jobs they had to cancel.</p>'
         '<h4>Pain and Suffering Takes the Same Reduction</h4>'
         '<p>Noneconomic damages get no immunity from the percentage. A jury assigns a figure for pain, scarring, and lost activity, and the court applies the same reduction it applies to bills. Road rash and deep tissue wounds leave permanent marks that photographs document better than words do. Take pictures at each stage of healing.</p>'
         '<h3>Where Uninsured and Underinsured Coverage Fills the Gap</h3>'
         "<p>South Carolina sets minimum liability limits of 25/50/25 under Section 38-77-140 and requires uninsured motorist coverage at those same minimums under Section 38-77-150. Carriers must offer underinsured motorist coverage up to your liability limits, though buying it stays optional. A rider with a broken pelvis can exhaust a minimum policy in one hospital stay. Check your own declarations page before you accept anybody's first number.</p>"
         '<h2>What to Do in the First Week After a Goose Creek Motorcycle Crash</h2>'
         '<p>The first week decides how much of your case still exists in month six. Evidence on a road does not wait. Skid marks fade, vehicles get repaired, and witnesses forget which light was green.</p>'
         '<p>None of this requires a lawyer to begin. It requires somebody to move while the record is still there to collect. Here is where to spend those first few days.</p>'
         '<ul><li>Report the crash to the Goose Creek Police Department or the agency with jurisdiction, as Section 56-5-1260 requires.</li><li>Get treated the same day, even when adrenaline has you feeling fine.</li><li>Photograph the bike, the roadway, the debris field, and your damaged gear before anything moves.</li><li>Ask the responding officer for the report number, then request the report through the SCDMV.</li><li>Notify your own insurer about the crash and say nothing about fault to the other carrier.</li></ul>'
         '<p>Decline the recorded statement until you understand your own percentage. That interview exists to build the number an adjuster plans to subtract.</p>'
         '<h2>How Long Do You Have to File a Goose Creek Motorcycle Claim?</h2>'
         '<p>Three years is the general rule in South Carolina, and it sounds like plenty of time. It disappears fast when a claim involves a government vehicle, an injured minor, or an insurer that negotiates for two years and then stops returning calls. Deadlines in a rider case are not one number. They are a set of numbers, and the shortest one controls.</p>'
         '<p>Missing the shortest deadline ends the claim, whatever its merits. Calendar every date in the first month, then work backward from the earliest one. Evidence goes stale long before any statute expires.</p>'
         '<h3>The Three Year Clock Under Section 15-3-530</h3>'
         '<p>Section 15-3-530(5) gives you three years for an injury to the person. The clock runs from the date of the crash in a typical motorcycle case. A <a href="[[wrongful-death-attorneys-in-summerville]]">wrongful death claim</a> runs three years from the date of death under Section 15-3-530(6). Filing is not the same as settling, and a filed case can still resolve the following month. Waiting until year three narrows what a lawyer can do for you.</p>'
         '<h3>Deadlines That Run Out Sooner Than Three Years</h3>'
         "<p>Claims against a South Carolina government entity run two years under Section 15-78-110 unless a verified claim goes in first. A claim against the United States needs a written administrative claim within two years under 28 U.S.C. Section 2401(b). Neither one extends the three-year rule. Each replaces it with something shorter. A minor's claim works the other way, because Section 15-3-40 pauses the clock until age 18, though the extra time never runs past one year after that birthday.</p>"
         '<h2>Questions Goose Creek Riders Ask About Shared Fault</h2>'
         '<p>These five come up in the first phone call more than any others. The short answers below name the statute so you can check the work yourself. Each one turns on facts a rider can still gather in the weeks after a crash, so none of them are settled the day the wreck happens.</p>'
         '<h3>Can I Still Recover if the Crash Report Blames Me?</h3>'
         "<p>Yes. A collision report records an officer's opinion, and it does not bind a jury or an adjuster. Photographs, witness statements, and vehicle damage regularly move the percentage. Ask for the complete report and the diagram rather than the summary page.</p>"
         '<h3>Does Refusing a Recorded Statement Hurt My Claim?</h3>'
         "<p>You owe cooperation to your own insurer under your policy. You owe nothing to the other driver's carrier. Decline that interview politely and route the questions through your attorney.</p>"
         '<h3>What if the Other Driver Was Uninsured in Berkeley County?</h3>'
         '<p>Section 38-77-150 requires uninsured motorist coverage on every South Carolina policy. Your own coverage steps in at those same minimum limits. Tell your carrier quickly, because those policies carry their own notice requirements.</p>'
         '<h3>Does It Matter That I Was Not Wearing a Helmet?</h3>'
         '<p>Not as a legal violation once you turn 21, because Section 56-5-3660 reaches only riders under that age. The defense may still argue the choice worsened a specific head injury. That is a medical argument, and medical proof answers it.</p>'
         '<h3>How Long Does a Goose Creek Motorcycle Case Take?</h3>'
         '<p>Many claims resolve in months, while cases with disputed fault or surgery take considerably longer. Filing inside the three-year window keeps your bargaining position intact. No lawyer can promise a timeline, because the insurer controls half the calendar.</p>'
         '<h2>Call a Goose Creek Motorcycle Accident Lawyer Before You Accept a Reduced Offer</h2>'
         '<p>The percentage an insurer assigns you is a negotiating position, not a finding of fact. Evidence moves it, and it moves most easily in the first few weeks. A Goose Creek motorcycle accident lawyer at Frost Law Group can read the collision report, secure the physical evidence, and answer the blame argument before it hardens into a written offer.</p>'
         '<p>Frost Law Group is a husband-and-wife firm serving Berkeley, Dorchester, and Charleston counties from Summerville. <a href="[[about]]">Tara L. Frost</a> is a former Dorchester County Magistrate Judge, and Jack C. Frost retired from the Charleston County Sheriff\'s Office after 14 years in law enforcement. That background shapes how this firm reads a crash report.</p>'
         '<p>Call ' + TEL + ' for a free case review. The firm answers 24/7. You can also send your crash details through the <a href="[[contact]]">contact page</a> and ask for a call back.</p>'
         '<p>Bring whatever you have. A report number, scene photographs, and your own declarations page are enough to start the conversation. If the offer on your table already assumes you were half to blame, have somebody look at it before you sign.</p>'
     ),
     sources=[("S.C. Code § 15-38-15, as rewritten by 2025 Act No. 42 (fault shared among several parties)", CODE_15_38, False),
              ("S.C. Code §§ 56-5-1260, 56-5-3640, 56-5-3660, 56-5-3670 and 56-5-6540 (crash reports, lane use, helmets, eye protection, seat belts)", CODE_56_5, False),
              ("S.C. Code §§ 38-77-140, 38-77-150 and 38-77-160 (minimum, UM and UIM coverage)", CODE_38_77, False),
              ("S.C. Code §§ 15-3-40 and 15-3-530 (filing deadlines)", CODE_15_3, False),
              ("S.C. Code §§ 15-78-110 and 15-78-120 (Tort Claims Act deadline and caps)", CODE_15_78, False),
              ("28 U.S.C. § 2401(b) (claims against the United States)", USC_2401, False),
              ("SCDPS, traffic fatalities by county", SCDPS_FATAL, False),
              ("S.C. Judicial Branch, Berkeley County courts", SCCOURTS_BERKELEY, False)],
     related=[MOTO, BERK + "/motorcycle-accident-lawyers-in-berkeley-county", MOTO + "/motorcycle-helmet-law-injury-lawyers-in-summerville", BERK + "/goose-creek-car-accident-lawyers"])
faq_ld(p6, 'Questions Goose Creek Riders Ask About Shared Fault')

# ----------------------------------------------------------------------------- 7. Moncks Corner slip and fall liability
p7 = post(hero_image='talk-to-a-moncks-corner-slip-and-fall-lawyer-before-the-video-is-gone.jpg',
     hero_caption="A shopper's feet rest beside an overturned coffee cup and a puddle of spilled coffee on a store floor.",
     category='Slip and fall', date='2026-09-28', modified='2026-09-28',
     title='Ask a Moncks Corner Slip and Fall Lawyer Who Is Liable',
     description='A Moncks Corner slip and fall lawyer explains who is liable for your fall, whether a store, a landlord, or a town. Call Frost Law Group for a free review.',
     h1='Who Can a Moncks Corner Slip and Fall Lawyer Hold Liable for Your Fall?',
     summary='Stores, landlords, contractors and public owners each answer for a fall under different rules. Who can be held liable for a fall in Moncks Corner, and what proof it takes.',
     body=(
         '<p>A Moncks Corner slip and fall lawyer can hold liable whoever controlled the floor, stairs, or walkway where you fell and knew, or should have known, about the hazard. That is usually a store, a landlord, or a cleaning contractor. When the town, Berkeley County, or the state owns the property, the South Carolina Tort Claims Act changes the rules.</p>'
         '<p>Frost Law Group handles injury claims across Berkeley, Dorchester, and Charleston counties from one office at 128 Linwood Lane in Summerville. The firm is a husband-and-wife team, and both Tara L. Frost and Jack C. Frost graduated from the Charleston School of Law. You work directly with an attorney, not a call center.</p>'
         '<p>If you fell in a store, an apartment complex, or a public building in Moncks Corner, call Frost Law Group at ' + TEL + ' for a free case review. You decide what happens next.</p>'
         '<h2>How Does South Carolina Decide Who Is Liable for a Fall in Moncks Corner?</h2>'
         '<p>Liability in a fall case starts with one question. Who controlled the spot where you went down? The <a href="[[slip-and-fall-attorneys-in-summerville]]">slip and fall and premises liability team at Frost Law Group</a> asks it first. The answer decides which insurer pays and which rules apply. A grocery aisle on Highway 52, an apartment stairwell, and a sidewalk on Main Street can each belong to a different owner.</p>'
         "<p>South Carolina has no single slip and fall statute. Courts decide these cases under common law negligence, and the owner's duty depends on why you were on the property. Control matters just as much. A tenant store, the shopping center that leases to it, and the company hired to mop its floors can each carry part of the blame.</p>"
         '<h3>Your Reason for Being on the Property Sets the Duty</h3>'
         '<p>South Carolina recognizes four classes of people who come onto land. The Court of Appeals listed them in Sims v. Giles as adult trespassers, invitees, licensees, and children. Each class is owed a different level of care. A customer and a dinner guest can fall on the same wet step and end up with very different claims. Your status is the first fact a lawyer pins down.</p>'
         '<h4>Customers and Public Visitors Are Invitees</h4>'
         "<p>An invitee enters at the owner's express or implied invitation. That covers a business visitor shopping in a store and a public invitee visiting a place held open to the public, such as a county office. The owner owes an invitee reasonable care for their safety. That duty reaches hazards the owner knows about and hazards a reasonable inspection would have found.</p>"
         '<h4>Social Guests Are Licensees With Narrower Protection</h4>'
         "<p>The most common licensee is a social guest, according to the same Sims decision. A host owes a licensee no duty to make the property safe. The host must use reasonable care in activities on the land and warn the guest about concealed dangers the host already knows about. A fall at a friend's house near Rembert C. Dennis Boulevard turns on what the homeowner knew before you arrived.</p>"
         '<h3>Open and Obvious Hazards Do Not Always End the Claim</h3>'
         '<p>Insurers reach for the open and obvious defense early. Sims v. Giles quoted Restatement (Second) of Torts section 343A, which says an owner is not liable for a danger that was known or obvious to the visitor. The same rule keeps the owner responsible when it should anticipate the harm anyway. Comment f to that section names distraction as a reason to expect a visitor to miss what is obvious. A shopper looking up at a sale display the store built to draw attention can fit that exception.</p>'
         '<h2>When Is a Moncks Corner Store Liable for a Spill on Its Floor?</h2>'
         "<p>Picture the places people shop, eat, and fill up in Moncks Corner. Grocery aisles, gas station restrooms, and restaurant entryways along Highway 52 and North Live Oak Drive all see spilled drinks and tracked-in rain. South Carolina requires a merchant to keep aisles and passageways in reasonably safe condition, but a merchant is not an insurer of its customers' safety.</p>"
         '<p>The South Carolina Supreme Court confirmed the test in <a href="https://www.sccourts.org/media/opinions/HTMLFiles/SC/25254.htm" rel="noopener" target="_blank">Wintersteen v. Food Lion, Inc.</a>, decided in 2001. A shopper slipped on a puddle of clear liquid near a self-service soda fountain with an ice dispenser. She argued the store should answer for a hazard its own setup made likely. The court declined. It held that a storekeeper is liable only if it put the substance on the floor or had actual or constructive notice of it.</p>'
         '<p>Here is the part most online slip and fall articles skip. Some courts elsewhere let a self-service setup stand in for notice, and Wintersteen acknowledged that approach before rejecting it. Your claim needs proof of one of the two routes below. The records a lawyer pulls decide how strong that proof is, so nobody can grade a store claim from the injury alone.</p>'
         '<h3>Proof the Store Created the Hazard</h3>'
         '<p>The first route skips notice entirely. If an employee created the danger, the store already knew about it. Wintersteen repeats the rule that a plaintiff can win by showing a specific act of the store created the dangerous condition. These situations often fit that route.</p>'
         '<ul><li>An employee mopped an aisle and set out no wet floor sign.</li><li>A stocker left a pallet, a box, or shrink wrap in a walkway.</li><li>A produce case misted water onto the tile below it.</li><li>A crew waxed or buffed a floor and left it slick where customers walk.</li></ul>'
         "<p>Each one points to something the store's own staff did.</p>"
         '<h3>Proof the Store Knew or Should Have Known</h3>'
         "<p>The second route is notice. Actual notice means the store knew about the hazard. Constructive notice means the hazard sat there long enough that a reasonable inspection would have found it. Many store cases turn on this route, since a customer usually spilled the liquid, not an employee. Both kinds of notice are proved with the store's own people and records.</p>"
         '<h4>Actual Notice From Employees and Earlier Complaints</h4>'
         '<p>Actual notice is the cleanest proof. A cashier who saw the spill and kept ringing up groceries gives it to you. So does a customer who told a manager about the puddle ten minutes before you fell. Get the names of witnesses at the scene, because the store controls its own employee list and has no reason to volunteer the helpful ones.</p>'
         '<h4>Constructive Notice and How Long the Hazard Sat There</h4>'
         '<p>Constructive notice is a question of time. The longer a hazard stayed on the floor, the stronger the argument that a reasonable inspection would have caught it. No statute sets a number of minutes. Two kinds of records usually answer the question, and both can disappear fast.</p>'
         '<h5>Surveillance Video Shows the Clock</h5>'
         '<p>Store cameras often record the aisle before, during, and after a fall. That footage can show when the spill happened and how many employees walked past it. Many systems overwrite footage on a rolling schedule, so a written preservation request should go out within days. A lawyer can send that request the same week you call.</p>'
         '<h5>Sweep Logs and Inspection Records Fill the Gaps</h5>'
         '<p>Many grocery and big-box stores keep sweep logs, floor walk sheets, or inspection checklists. Those records show when an employee last checked the aisle where you fell. A long gap in a busy store can support constructive notice. A missing log raises its own question about whether anyone was checking at all.</p>'
         '<h2>Who Is Responsible for a Fall at a Moncks Corner Apartment or Shopping Center?</h2>'
         '<p>Not every fall happens inside a store. Apartment stairs, parking lots, and sidewalks in front of strip centers produce their own claims, and ownership there is often split. The tenant, the landlord, and a management company can each control a different piece of the same walkway.</p>'
         '<p>For rentals, the South Carolina Residential Landlord and Tenant Act answers part of the question. Section 27-40-440(a)(3) requires a landlord to keep all common areas of the premises in reasonably safe condition. A loose stair tread in a shared stairwell at a complex off Highway 52 is the kind of hazard that statute speaks to.</p>'
         '<p>Commercial property works through the lease. A shopping center lease usually says whether the owner or the tenant maintains the parking lot, the sidewalk, and the storefront entry. That document decides who gets named, and sometimes both do.</p>'
         '<h2>What Changes When the Town, Berkeley County, or the State Owns the Property?</h2>'
         '<p>Moncks Corner is the Berkeley County seat, so public buildings, town sidewalks, and county property sit close together. ABC News 4 reported in June 2026 that the town won a $1.2 million grant for new sidewalks on Rembert C. Dennis Boulevard and Stony Landing Road. A fall on any of that public ground follows different rules than a fall in a store.</p>'
         '<p>A fall on government property runs through the <a href="https://www.scstatehouse.gov/code/t15c078.php" rel="noopener" target="_blank">South Carolina Tort Claims Act</a>. Section 15-78-40 makes a public body liable like a private person, subject to the Act\'s limits. Section 15-78-60 then carves out dozens of exceptions, and several of them target the places people fall.</p>'
         '<h3>Exceptions That Can Block a Claim Against a Public Owner</h3>'
         '<p>Section 15-78-60 lists more than 30 situations where a governmental entity is not liable. Three of them come up often in fall claims. Each one sets a different notice rule. The same crack in the concrete can support a strong claim in one place and no claim at all in another. Check which item fits your fall before a claim goes out.</p>'
         '<h4>Rain, Ice, and Weather on Public Walkways</h4>'
         "<p>Item 8 bars claims for snow or ice and for temporary or natural conditions on a public way caused by weather. The exception drops away when an employee's negligent act caused the snow or ice. A rain puddle on a town sidewalk usually falls inside the exception. A walkway that a county crew hosed down on a freezing morning may not.</p>"
         '<h4>Sidewalk and Street Defects Someone Else Caused</h4>'
         "<p>Item 15 covers highways, streets, bridges, and other public ways. The public body that maintains the way is not liable for a defect a third party caused. Liability returns when it failed to fix the defect within a reasonable time after actual or constructive notice. A utility trench left uneven or a contractor's debris on a walkway fits that pattern. Complaints to the town or county before your fall become the evidence of notice.</p>"
         '<h4>Parks and Playgrounds Require Actual Notice</h4>'
         '<p>Item 16 is the strictest of the three. It covers public property used as a park, playground, or open recreation area. The entity is liable there only when it failed to fix a defect within a reasonable time after actual notice. Constructive notice is not enough. A loose boardwalk plank at a county or town park needs proof that someone reported it before you fell.</p>'
         '<h3>Deadlines and Caps on Claims Against Public Owners</h3>'
         '<p>Public property claims run on a shorter, stricter clock than claims against a store. The Tort Claims Act sets its own filing rules and its own limit on recovery. Put these numbers on a calendar right away.</p>'
         '<ul><li>Section 15-78-110 requires suit within two years after the loss was or should have been discovered.</li><li>A verified claim filed first under Section 15-78-80 stretches that deadline to three years, and it must be received within one year.</li><li>The public body then has 180 days to allow or deny the claim, and silence counts as a denial.</li><li>Section 15-78-120 caps recovery at $300,000 per person and $600,000 per occurrence, with no punitive damages.</li></ul>'
         '<p>Sometimes nobody knows whether the town, the county, or the state maintains a stretch of sidewalk. Section 15-78-80 lets a verified claim go to the Attorney General when the proper defendant is in doubt. Whether an exception or the cap applies turns on facts a lawyer has to check, starting with who maintains the exact spot.</p>'
         '<h2>How a Moncks Corner Slip and Fall Lawyer Handles Shared Fault and Outside Contractors</h2>'
         '<p>Almost every fall claim draws a shared fault argument. Were you looking at your phone? Were your shoes wrong for the rain? Did you walk right past the sign? Those arguments go straight to your percentage, and your percentage goes straight to the check.</p>'
         '<p>Two rules decide how much that percentage costs you. One dates to 1991. The other took effect on January 1, 2026, and many summaries still describe the old version. Neither rule tells you what your own case is worth, because that depends on evidence a lawyer has to weigh.</p>'
         '<h3>The 50% Line From Nelson v. Concrete Supply</h3>'
         '<p>South Carolina adopted modified comparative negligence in Nelson v. Concrete Supply Co. in 1991. You recover as long as your negligence is not greater than the combined negligence of the defendants. Your award then drops by your share. At 50%, you still recover half, and at 51% you recover nothing. Some summaries say a plaintiff at exactly 50% is barred, and Nelson says otherwise.</p>'
         '<h3>Cleaning Contractors and the 2026 Empty Chair Rule</h3>'
         "<p>Section 15-38-15, rewritten by 2025 Act No. 42, lets a jury assign fault to a tortfeasor who is not a defendant. That party must be disclosed within 180 days of the lawsuit's start unless a court finds good cause, and you may add it as a defendant. A defendant found less than 50% at fault then pays only its own share, unless its conduct was willful, wanton, reckless, or intentional. In a fall case, the parties who can end up on that verdict form include these.</p>"
         '<ul><li>The store or business that operated the space where you fell.</li><li>The property owner that leased the building or parking lot to that business.</li><li>A management company hired to run an apartment complex or shopping center.</li><li>A cleaning, landscaping, or maintenance contractor that worked the area.</li></ul>'
         '<p>Say a jury finds a store 40% at fault and a cleaning contractor 60% at fault. The store pays 40% of the damages, and the rest depends on whether the contractor has coverage. Finding every company that touched the floor, and its insurer, belongs in the first weeks of a case.</p>'
         '<h2>Where a Moncks Corner Fall Case Is Treated and Filed</h2>'
         '<p>Local geography shapes a fall claim from the first hour. Emergency care, the court that would hear a lawsuit, and the magistrate court for small claims all sit inside Moncks Corner.</p>'
         '<p>HCA Healthcare Moncks Corner ER, a part of Trident Hospital, is at 401 North Live Oak Drive and is open 24 hours. The emergency record written there is often the earliest account of how you fell, so check your copy for mistakes. Hip fractures, head injuries, and spinal injuries can become <a href="[[catastrophic-injury-attorneys-in-summerville]]">catastrophic injury claims</a>, and a fatal fall becomes a <a href="[[wrongful-death-attorneys-in-summerville]]">wrongful death claim</a> for the family.</p>'
         '<h3>Circuit Court at the Berkeley County Courthouse</h3>'
         '<p>A slip and fall lawsuit in Berkeley County is filed in the Court of Common Pleas at the Berkeley County Courthouse, 300-B California Avenue. Berkeley County sits in the Ninth Judicial Circuit with Charleston County. Section 15-3-530(5) gives you three years to sue a private owner for an injury to the person, generally counted from the fall. Filing does not mean trial, and how long a case runs depends on the injuries and the evidence in it.</p>'
         '<h3>Magistrate Court for Claims of $7,500 or Less</h3>'
         "<p>Smaller falls sometimes belong in magistrate court. Section 22-3-10 gives magistrates civil jurisdiction over injury claims when the damages claimed do not exceed $7,500. Berkeley County's Small Claims North magistrate court sits at 223 North Live Oak Drive in Moncks Corner. A larger claim belongs in circuit court, and which court fits yours depends on bills and lost wages a lawyer can total with you.</p>"
         '<h2>What to Do in the First Days After a Moncks Corner Fall</h2>'
         '<p>The evidence in a fall case is fragile. Spills get mopped, video gets overwritten, and a cracked sidewalk slab gets patched. The first few days decide what proof still exists when an adjuster starts asking questions.</p>'
         '<p>Each step below ties to a rule covered above. Do what you can, and never let the list delay medical care.</p>'
         '<ul><li>Get checked the same day at HCA Healthcare Moncks Corner ER or by your own doctor, since a treatment gap invites a causation fight.</li><li>Ask the manager to write an incident report, and photograph it if nobody will hand you a copy.</li><li>Photograph the floor, the lighting, your shoes, and the spot where a wet floor sign should have been.</li><li>Write down the names of employees and customers who saw the hazard, because they can prove actual notice under Wintersteen.</li><li>Send the store a written request to keep its video and sweep logs from the day you fell.</li><li>Note the exact spot of a public sidewalk fall, so a verified claim reaches the right town, county, or state office.</li></ul>'
         "<p>Hold off on a recorded statement to the owner's liability insurer until you know who controlled the floor. That interview tends to focus on your attention and your footwear, which is where a fault percentage comes from.</p>"
         '<h2>Questions Moncks Corner Fall Victims Ask About Liability</h2>'
         '<p>Here are four questions people ask about liability after a fall in Berkeley County. Each short answer names the rule behind it, so you can check the source yourself. The right answer for your own fall still depends on who owned the property and what the records show.</p>'
         '<h3>Can I Sue a Store if There Was No Wet Floor Sign?</h3>'
         "<p>A missing sign helps, but it is not the whole case. Under Wintersteen, you still need proof the store created the hazard or had notice of it. A missing sign next to an employee's mop bucket can prove both at once.</p>"
         '<h3>Is a Parking Lot Fall a Premises Liability Claim in South Carolina?</h3>'
         '<p>Yes. Parking lots, sidewalks, and entryways are part of the premises. The lease usually decides whether the store, the property owner, or a management company answers for them.</p>'
         "<h3>What Is the Deadline if My Child Fell on Someone Else's Property?</h3>"
         '<p>Section 15-3-40 pauses the clock while a child is under 18. The extension never runs past one year after the child turns 18, so acting sooner is safer. Section 15-78-110 applies the same tolling rule to Tort Claims Act cases.</p>'
         '<h3>Does It Matter That I Was Looking at My Phone When I Fell?</h3>'
         "<p>It can. The defense will argue distraction raised your share of the fault under Nelson. You still recover if your share is not greater than the defendants' combined share. Your award then drops by your percentage.</p>"
         '<h2>Talk to a Moncks Corner Slip and Fall Lawyer Before the Video Is Gone</h2>'
         "<p>The proof in a fall case lives in records that do not last. A Moncks Corner slip and fall lawyer at Frost Law Group can identify who controlled the floor and send preservation letters for video and sweep logs. The firm can also check whether a public owner's deadlines apply to you.</p>"
         '<p>Frost Law Group serves Berkeley, Dorchester, and Charleston counties from its office at 128 Linwood Lane in Summerville. Tara L. Frost is a former Dorchester County Magistrate Judge, and Jack C. Frost spent 14 years in law enforcement. Read more about <a href="[[about]]">the attorneys at Frost Law Group</a>.</p>'
         '<p>Call Frost First at ' + TEL + ' for a free case review. The firm answers 24/7. You can also send the details of your fall through the <a href="[[contact]]">contact page</a> and ask for a call back.</p>'
         '<p>Bring what you have. An incident report number, a few photographs, and the names of anyone who saw the hazard are enough to start. No lawyer can promise a result, and prior results do not guarantee a similar outcome.</p>'
     ),
     sources=[("Sims v. Giles, S.C. Ct. App. Op. No. 3291 (2001)", SIMS, False),
              ("Wintersteen v. Food Lion, Inc., S.C. Sup. Ct. Op. No. 25254 (2001)", WINTERSTEEN, False),
              ("S.C. Code § 27-40-440 (landlord duties)", CODE_27_40, False),
              ("S.C. Code §§ 15-78-40 to 15-78-120 (Tort Claims Act)", CODE_15_78, False),
              ("S.C. Code § 15-38-15, as rewritten by 2025 Act No. 42 (fault shared among several parties)", CODE_15_38, False),
              ("S.C. Code §§ 15-3-40 and 15-3-530 (filing deadlines)", CODE_15_3, False),
              ("S.C. Code § 22-3-10 (magistrate civil jurisdiction)", CODE_22_3, False),
              ("S.C. Judicial Branch, Berkeley County courts", SCCOURTS_BERKELEY, False),
              ("ABC News 4, Moncks Corner sidewalk grant (June 2026)", ABC4_MONCKS, False)],
     related=[SLIPP, SLIPP + "/retail-slip-and-fall-lawyers-in-summerville", SLIPP + "/apartment-injury-lawyers-in-summerville", BERK + "/moncks-corner-car-accident-lawyers"])
faq_ld(p7, 'Questions Moncks Corner Fall Victims Ask About Liability')

# ----------------------------------------------------------------------------- 8. North Charleston truck claim value
p8 = post(hero_image='talk-to-a-north-charleston-truck-accident-lawyer-about-your-claims-value.jpg',
     hero_caption='An overturned tractor-trailer lies on its side across a curving highway ramp.',
     category='Truck accidents', date='2026-10-06', modified='2026-10-06',
     title='Hire a North Charleston Truck Accident Lawyer for Your Claim',
     description="A North Charleston truck accident lawyer values your claim by adding up your losses and checking each company's insurance and fault. Get a free review.",
     h1='How Does a North Charleston Truck Accident Lawyer Figure Out What Your Claim Is Worth?',
     summary='Damages, federal insurance minimums, shared fault rules and the punitive damages caps all shape what a North Charleston truck crash claim is worth.',
     body=(
         '<p>A North Charleston truck accident lawyer adds up your medical bills, lost income, and pain and suffering. Then the lawyer checks how much insurance each company carries and how a jury could split the fault. Federal rules set a $750,000 floor for most for-hire interstate freight carriers. South Carolina law decides who pays which share.</p>'
         "<p>Frost Law Group represents people hurt in tractor-trailer, dump truck, and delivery truck crashes across Charleston, Dorchester, and Berkeley counties. You work directly with an attorney, not a call center. Jack C. Frost spent 14 years in law enforcement with the Summerville Police Department and the Charleston County Sheriff's Office before he practiced law.</p>"
         '<p>If a semi, dump truck, or delivery truck hit you in North Charleston, call Frost Law Group at ' + TEL + ' for a free case review. The review costs nothing, and you decide what happens next.</p>'
         '<h2>What Goes Into the Value of a North Charleston Truck Accident Claim?</h2>'
         '<p>Every truck claim answers two questions. What did the crash cost you, and who can be made to pay it? The <a href="[[truck-accident-attorneys-in-summerville]]">truck accident lawyers at Frost Law Group</a> answer the first question from your records. They test the second against insurance policies and the fault rules in South Carolina law. A wreck with a loaded tractor-trailer at the I-26 and I-526 interchange can produce large losses and a short list of payers.</p>'
         '<p>No chart or formula turns an injury into a number. Insurers run software, juries use judgment, and both look at the same evidence. What your own claim is worth depends on your records, your recovery, and facts a lawyer has to review.</p>'
         '<h3>Economic Losses Come From Your Records</h3>'
         '<p>Economic damages are the losses with receipts. They include ambulance and hospital bills, surgery, therapy, prescriptions, and the care you will need later. If EMS takes you to HCA Healthcare Trident Hospital at 9330 Medical Plaza Drive, you arrive at a Level II trauma center. The trauma record written there is often the first account of your injuries, so ask for a copy and check it for mistakes.</p>'
         '<p>Lost wages cover the paychecks you missed while you healed. Lost earning capacity covers the gap between what you could have earned over your working life and what you can earn now. Pay stubs and tax returns prove the first. The second often needs testimony from a vocational rehabilitation counselor or an economist. Brain, spine, and amputation injuries can turn a truck case into one of the <a href="[[catastrophic-injury-attorneys-in-summerville]]">catastrophic injury claims</a> that need a life care plan.</p>'
         '<h3>Pain and Suffering Has No General Cap in a South Carolina Truck Case</h3>'
         '<p>Noneconomic damages cover pain, lost enjoyment of life, scarring, and mental distress. South Carolina does cap noneconomic damages in Section 15-32-220. That section is written for medical malpractice claims against health care providers, not for a crash with a commercial truck. A jury sets the number from the evidence. That evidence is your treatment history, your own testimony, and the people who see you struggle every day.</p>'
         '<h2>How Much Insurance Does a Truck Carry Under Federal Rules?</h2>'
         "<p>Insurance often sets the practical limit on a truck claim. A company can owe more than its policy covers, but collecting the excess from business assets is slow and uncertain. That is why a lawyer asks for the carrier's policy limits early.</p>"
         '<p>Federal law sets minimum liability coverage in <a href="https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-387/subpart-A/section-387.9" rel="noopener" target="_blank">the federal insurance schedule at 49 C.F.R. 387.9</a>. The minimum depends on what the truck hauls and whether it crosses state lines. A minimum is only a floor. Many carriers buy more, and only the policy itself shows the real limit on your claim.</p>'
         '<h3>The Federal Minimums by Cargo</h3>'
         '<p>The tiers below apply to trucks with a gross vehicle weight rating of 10,001 pounds or more. Here is how the minimums break down for the trucks you see on I-26, I-526, and Rivers Avenue.</p>'
         '<ul><li>For-hire carriers hauling nonhazardous property in interstate or foreign commerce must carry at least $750,000.</li><li>Carriers hauling oil, hazardous waste, or other hazardous materials generally must carry at least $1,000,000.</li><li>Certain bulk hazardous loads, such as some explosives, poison gases, and highway route controlled radioactive cargo, require at least $5,000,000.</li></ul>'
         '<p>The tier turns on the cargo, so the bill of lading and the placards on the trailer matter.</p>'
         '<h3>Trucks the $750,000 Floor Does Not Reach</h3>'
         '<p>Section 387.3 limits who has to meet the schedule. The $750,000 rule covers for-hire carriers moving property in interstate or foreign commerce. Two common kinds of trucks on local roads can fall outside it, and so can any vehicle rated under 10,001 pounds. Each gap changes where a lawyer looks for coverage, because the federal floor no longer guarantees any number.</p>'
         '<h4>Private Fleets Hauling Their Own Goods</h4>'
         "<p>A company that hauls its own nonhazardous products is a private carrier, not a for-hire carrier. Section 387.3(a) applies the federal subpart to for-hire property carriers, and subsection (b) adds hazardous materials haulers. A distributor's box truck or a manufacturer's own tractor-trailer is not bound by the $750,000 floor. Its coverage depends on its commercial auto policy and any umbrella policy above it.</p>"
         '<h4>Loads That Stay Inside South Carolina</h4>'
         '<p>A for-hire truck hauling nonhazardous freight only within South Carolina is not moving in interstate commerce. The federal $750,000 schedule does not reach that trip by its own terms. Whether a short local haul counts as interstate can turn on where the freight started. Port containers are the common local example, since a container that arrived by ship may still be moving in foreign commerce on its last short leg. SC Ports paused the Leatherman Terminal on August 1, 2026, and consolidated container work at its other two container terminals, including the North Charleston Terminal.</p>'
         '<h2>Who Pays When More Than One Company Shares the Blame?</h2>'
         '<p>Many truck crashes involve more than one company. The driver may work for a motor carrier, pull a trailer owned by a leasing company, and carry freight loaded by a shipper. A repair shop may have serviced the brakes a week earlier. Each one can carry part of the fault, and each one usually has its own insurer.</p>'
         '<p>South Carolina answers the question of who pays in <a href="https://www.scstatehouse.gov/code/t15c038.php" rel="noopener" target="_blank">Section 15-38-15 of the South Carolina Code</a>. It decides whether one company can be made to pay the whole award or only its own share. How it plays out in your case depends on evidence a lawyer still has to develop.</p>'
         '<h3>The Less Than 50% Rule for Each Defendant</h3>'
         '<p>Under Section 15-38-15(A), a defendant found less than 50% at fault pays only its own percentage of the damages. Joint and several liability does not apply to that defendant. A defendant at 50% or more stays jointly and severally liable, which means it can be made to pay the full award. This rule took effect in 2005, and the 2026 rewrite kept it.</p>'
         '<p>Here is how that can play out. Say a jury finds the motor carrier 40% at fault, the company that loaded the trailer 35%, and a car driver who cut off the truck 25%. Each one pays only its share. If that car driver carries only the state minimum of $25,000 per person under Section 38-77-140, most of that share may go uncollected. Your own underinsured coverage may fill part of the gap.</p>'
         '<h3>What the 2026 Rewrite Changed for Newer Crashes</h3>'
         '<p>The General Assembly rewrote Section 15-38-15 in 2025 Act No. 42, effective January 1, 2026. Section 11 of the act applies it only to causes of action arising or accruing after that date. A crash on Ashley Phosphate Road in December 2025 falls under the old version. A crash on the same road in March 2026 falls under the new one, and two of its changes matter most in truck cases.</p>'
         '<h4>Fault Assigned to Companies Outside the Lawsuit</h4>'
         "<p>The new version lets a jury assign fault to a tortfeasor who is not a defendant, often called the empty chair. A defendant has to disclose that company within 180 days after the suit begins, unless a court finds good cause for a later disclosure. You can then add the company as a defendant, and the amended complaint relates back to the filing date. If you do not add it, the defendant carries the burden of proving that company's fault.</p>"
         '<h5>Who the Trucking Company Cannot Blame</h5>'
         "<p>Section 15-38-15(H) keeps some parties off the verdict form. A carrier whose liability rests on its own driver's conduct cannot put that driver on the form as an empty chair. Parties who are immune from suit stay off the form. So does anyone whose conduct was willful, wanton, reckless, or intentional, and strict liability claims are excluded too.</p>"
         '<h5>Settlements With Other Companies Still Count</h5>'
         "<p>A company that settles with you before trial still goes on the verdict form under Section 15-38-15(G)(4), unless subsection (H) excludes it. The jury then assigns that company a share like any other party. Money from a settling company left off the form is credited in proportion to each defendant's share under subsection (E).</p>"
         '<h4>Alcohol Removed From the Full Liability Exception</h4>'
         '<p>The old subsection (F) made a defendant fully liable, whatever its percentage, when its conduct was grossly negligent or involved alcohol. The 2026 version removed gross negligence and alcohol from that list. It keeps full liability for willful, wanton, reckless, or intentional conduct and for the illegal use, sale, or possession of drugs. Drunk driving can still meet the reckless standard. The jury now has to make that finding, because alcohol alone no longer triggers the exception.</p>'
         '<h2>Can a North Charleston Truck Accident Lawyer Seek Punitive Damages?</h2>'
         '<p>Punitive damages punish conduct instead of paying for losses. Under Section 15-32-520(D), you have to prove by clear and convincing evidence that your harm came from willful, wanton, or reckless conduct. In a truck case, that proof often comes from driver logs, dispatch messages, and maintenance records.</p>'
         '<p>A defendant can ask for a split trial under Section 15-32-520(A). The jury first decides fault and compensatory damages, then hears punitive evidence in a second stage. Whether punitive damages fit your crash depends on what those records show. No lawyer can predict that before the evidence is in.</p>'
         '<h3>The Standard Cap and Its Yearly Adjustment</h3>'
         '<p>Section 15-32-530(A) limits most punitive awards to the greater of three times the compensatory damages or $500,000. Some online summaries leave out the three-times multiplier, which changes the math on a serious injury. Subsection (D) directs the state Revenue and Fiscal Affairs Office to adjust the $500,000 figure each year for inflation. The judge applies the cap after the verdict.</p>'
         '<h3>When the Cap Rises or Disappears</h3>'
         "<p>Section 15-32-530 sets two kinds of exceptions to the standard punitive damages cap. The first raises it, and the second removes it. Both depend on findings the trial judge makes after the verdict, based on evidence your lawyer puts in the record. In truck cases, the evidence for either one usually sits in the carrier's files and the driver's test results.</p>"
         '<h4>Profit-Driven Decisions Approved by Management</h4>'
         '<p>The cap rises to the greater of four times compensatory damages or $2 million in two situations under subsection (B). One is conduct driven mainly by unreasonable financial gain, where a managing agent or officer knew about or approved the danger. The other is conduct that could expose the defendant to a felony conviction. A dispatch policy that pushed drivers past their rest breaks is the kind of evidence the first situation looks for.</p>'
         '<h4>An Impaired Driver or a Felony Conviction Removes the Cap</h4>'
         '<p>Subsection (C) removes the cap entirely when the judge finds any one of these three facts.</p>'
         '<ul><li>The defendant intended to harm you, and the conduct did harm you.</li><li>The defendant pleaded guilty to or was convicted of a felony arising from the same conduct.</li><li>The defendant acted under the influence of alcohol or drugs, other than properly taken prescriptions, to the point that judgment was substantially impaired.</li></ul>'
         "<p>Post-crash testing records help prove the third item. Under 49 C.F.R. 382.303, a carrier must test its driver for alcohol after a fatal crash. Testing also applies after some injury or tow-away crashes where the driver gets a citation. If the alcohol test does not happen within two hours, the carrier has to record why, and it stops trying after eight hours. Drug testing attempts stop after 32 hours. Each finding looks at the defendant's own conduct, so whether a driver's impairment lifts the cap for the company is a question for your lawyer.</p>"
         '<h2>What Changes When a Government Truck Causes the Crash?</h2>'
         '<p>Not every heavy truck belongs to a private company. Garbage trucks, dump trucks, and road maintenance vehicles can belong to a city, a county, or the state. A crash with one of them runs through the South Carolina Tort Claims Act, which sets its own deadline and its own limit.</p>'
         '<p>Section 15-78-110 requires suit within two years after the loss was or should have been discovered. That stretches to three years if you file a verified claim first. The two-year limit is a full year shorter than the three-year rule in Section 15-3-530(5) for private defendants. Which rule applies depends on who owned and operated the truck, a fact a lawyer confirms from the registration and the crash report.</p>'
         '<h3>The $300,000 Tort Claims Act Limit</h3>'
         '<p>Section 15-78-120 caps recovery against a governmental entity at $300,000 per person and $600,000 per occurrence. Those caps apply no matter how many agencies are involved. A crash with a city garbage truck or a county dump truck falls under the same limit. The same section bars punitive damages and interest before judgment. A serious truck injury can exceed those numbers, and the cap does not rise with the size of your losses.</p>'
         '<h3>Your Own Underinsured Coverage Above a Statutory Cap</h3>'
         '<p>Section 38-77-160 says underinsured motorist coverage applies to damages above the at-fault driver\'s limits or above any damages cap imposed by statute. That wording can reach the gap a Tort Claims Act cap leaves behind. Underinsured coverage is optional in South Carolina, so check whether you bought it and in what amount. The same coverage can pay when a private trucking policy runs out, just as it does in <a href="[[car-accident-attorneys-in-summerville]]">car accident claims</a>. Whether it pays depends on the policy terms and your facts.</p>'
         '<h2>How Shared Fault Lowers a Truck Crash Award in South Carolina</h2>'
         "<p>Trucking insurers often argue that the car driver caused or worsened the crash. Did you change lanes into the truck's blind spot? Did you slam on the brakes in front of a loaded trailer? Those questions go straight to your percentage. South Carolina adopted modified comparative negligence in Nelson v. Concrete Supply Co. in 1991. You recover if your negligence is not greater than the combined negligence of the defendants, and your award drops by your share.</p>"
         '<p>At 30% fault, your award drops by 30%. At 50%, you still recover half, and at 51% you recover nothing. Section 56-5-6540(C) adds one protection. A seat belt violation is not admissible as evidence in a civil action, so the insurer cannot use it to raise your share. Your own percentage depends on the scene evidence, and a lawyer has to weigh it before anyone can estimate it.</p>'
         '<h2>Where a North Charleston Truck Case Is Reported and Filed</h2>'
         '<p>North Charleston crosses three county lines. Most of the city sits in Charleston County, with parts in Dorchester and Berkeley counties. That split decides which agency writes the report and which courthouse hears a lawsuit. The exact crash location can matter as much as the injury.</p>'
         '<p>Section 56-5-1260 requires a driver in an injury crash to notify the local police department when the crash happens inside a municipality. Inside city limits, that means the North Charleston Police Department. Outside them, notice goes to the county sheriff or the nearest South Carolina Highway Patrol office. You can request most crash reports from the South Carolina Department of Motor Vehicles online or with Form FR-50.</p>'
         '<p>Under Section 15-7-30, a truck crash suit can be filed in the county where the most substantial part of the conduct happened, among other options. For a North Charleston crash, that usually points to one of three circuit courthouses.</p>'
         '<ul><li>Charleston County cases go to the Charleston County Courthouse at 100 Broad Street in Charleston, in the Ninth Judicial Circuit.</li><li>Dorchester County cases go to the Dorchester County Courthouse at 5200 East Jim Bilton Boulevard in St. George, in the First Judicial Circuit.</li><li>Berkeley County cases go to the Berkeley County Courthouse at 300-B California Avenue in Moncks Corner, also in the Ninth Judicial Circuit.</li></ul>'
         '<p>Venue rules also allow other counties in some cases, such as where a defendant has its principal place of business. The right choice depends on the defendants and the facts.</p>'
         '<h2>Questions About Truck Accident Claim Value in North Charleston</h2>'
         '<p>People ask these questions after a truck crash in North Charleston, often right after the first call from an adjuster. Each answer names the rule behind it, so you can check the source yourself. Your own answer still depends on the policies, the fault evidence, and your injuries.</p>'
         '<h3>Is the $750,000 Federal Minimum the Most I Can Recover?</h3>'
         '<p>No. The $750,000 figure in 49 C.F.R. 387.9 is a minimum the carrier must buy, not a cap on your damages. Carriers can buy more coverage, and other companies can share the fault and the payment.</p>'
         '<h3>Does a Jury Know South Carolina Caps Punitive Damages?</h3>'
         '<p>No. Section 15-32-530(B) bars telling the jury about the cap. The judge reduces an award that goes over it after the verdict.</p>'
         '<h3>Does a Criminal Charge Against the Truck Driver Change My Claim?</h3>'
         '<p>It can. If the driver pleads guilty to or is convicted of a felony from the same conduct, Section 15-32-530(C)(2) removes the punitive damages cap. The criminal case and your civil claim still run separately, with different standards of proof.</p>'
         '<h3>How Long Does a Family Have to File After a Fatal Truck Crash?</h3>'
         '<p>Section 15-3-530(6) gives a family three years from the date of death to bring a <a href="[[wrongful-death-attorneys-in-summerville]]">wrongful death claim</a>. If a government truck caused the crash, the Tort Claims Act deadline in Section 15-78-110 applies instead. Evidence can disappear long before either deadline runs.</p>'
         "<h2>Talk to a North Charleston Truck Accident Lawyer About Your Claim's Value</h2>"
         "<p>The value of a truck claim sits in policies, verdict forms, and records the trucking company controls. A North Charleston truck accident lawyer at Frost Law Group can request the carrier's policy limits and identify every company that shared the fault. The firm can also check whether a public owner's shorter deadline applies to your crash.</p>"
         '<p>Frost Law Group serves Charleston, Dorchester, and Berkeley counties from 128 Linwood Lane in Summerville. Tara L. Frost is a former Dorchester County Magistrate Judge, and both attorneys graduated from the Charleston School of Law. Meet the <a href="[[about]]">attorneys at Frost Law Group</a> before you call.</p>'
         '<p>Call Frost First at ' + TEL + ' for a free case review. The firm answers 24/7. You can also send the details of your crash through the <a href="[[contact]]">contact page</a> and ask for a call back.</p>'
         "<p>Bring the crash report number, a photo of the USDOT number on the truck's cab door, and your own auto policy if you have them. No lawyer can promise a result, and prior results do not guarantee a similar outcome.</p>"
     ),
     sources=[("49 C.F.R. § 387.9 (federal minimum insurance)", ECFR_387_9, False),
              ("49 C.F.R. § 387.3 (which carriers the insurance rules cover)", ECFR_387_3, False),
              ("49 C.F.R. § 382.303 (post-crash alcohol and drug testing)", ECFR_382_303, False),
              ("S.C. Code § 15-38-15, as rewritten by 2025 Act No. 42 (fault shared among several parties)", CODE_15_38, False),
              ("S.C. Code §§ 15-32-220, 15-32-520 and 15-32-530 (damages caps and punitive damages)", CODE_15_32, False),
              ("S.C. Code §§ 15-78-110 and 15-78-120 (Tort Claims Act deadline and caps)", CODE_15_78, False),
              ("S.C. Code §§ 38-77-140 and 38-77-160 (minimum and UIM coverage)", CODE_38_77, False),
              ("S.C. Code § 15-3-530 (filing deadlines)", CODE_15_3, False),
              ("S.C. Code § 15-7-30 (venue)", CODE_15_7, False),
              ("S.C. Code §§ 56-5-1260 and 56-5-6540 (crash reports and seat belts)", CODE_56_5, False),
              ("S.C. Department of Public Health, trauma system", DPH_TRAUMA, False),
              ("Live 5 News, SC Ports pauses Leatherman Terminal (June 2026)", LIVE5_LEATHERMAN, False)],
     related=[TRUCKP, CHS + "/truck-accident-lawyers-in-charleston-county", TRUCKP + "/who-is-liable-in-a-truck-accident", CHS + "/north-charleston-personal-injury-lawyers"])
faq_ld(p8, 'Questions About Truck Accident Claim Value in North Charleston')
