"""Blog posts: local news and community questions about crashes, injuries and insurance, answered by the attorney who
handles those cases. Tara writes; Jack reviews (his investigation background is the natural second set of eyes).
Outbound links go to official sources (statutes, SCDMV, SCDPS, DPH, SC Courts) and to the community threads where the
question is asked (Nextdoor, Reddit, nofollow). Community links come from local_data.json via local.link(). The official
URLs below were verified in research R1 to R5 (2026-09-28) and are set here because some local_data.json entries
(scdmv_reports, schp, scdoi) point at stale or generic pages.

Corrected 2026-09-29 against repo reviews RR-2 and RR-4: FR-10 return duty, I-26 county geography, dog bite reporting
to DPH, the 47-3-110 text and exceptions, minors' settlements and deadlines, helmet and eye protection rules, UIM
settlement rules under 38-77-160, stacking, the 2024 rewrite of 38-77-170, and cover captions matched to the images."""
from .base import page, A, ext, img, p, ul, checks, steps, callout, answer, band, esc, table
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


def post(slug, **kw):
    kw.setdefault("kind", "post")
    kw.setdefault("hub", "blog")
    kw.setdefault("date", DATE)
    kw.setdefault("modified", MODIFIED)
    kw.setdefault("cta", False)
    kw.setdefault("changefreq", "yearly")
    kw.setdefault("priority", 0.5)
    kw.setdefault("author", "tara")
    kw.setdefault("reviewer", "jack")
    return page("blog/" + slug, **kw)


# ----------------------------------------------------------------------------- 1. I-26 crash report
post("i-26-crash-summerville-who-writes-the-report", hero_image="cover-i26-report.jpg",
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
post("dog-bite-summerville-neighborhood-what-parents-should-know", hero_image="cover-dog-bite-neighborhood.jpg",
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
post("motorcycle-season-lowcountry-helmet-law-your-claim", hero_image="cover-motorcycle-season.jpg",
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
post("hit-by-an-uninsured-driver-goose-creek-your-own-policy", hero_image="cover-goose-creek-uninsured.jpg",
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
