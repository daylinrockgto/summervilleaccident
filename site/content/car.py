"""Car accident hub and its spokes: the answer pages Search Console and the audit say people are asking for.

Each spoke opens with the direct answer (the sentence an AI answer can quote), then the detail, the statute,
the local specifics, and three to five follow-up questions with FAQ markup."""
from .base import page, A, ext, img, p, ul, checks, steps, callout, answer, band, esc, table
from . import firm
from .local import cite, link

HUB = firm.CAR
TEL = f'<a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'


def sp(slug, **kw):
    kw.setdefault("kind", "spoke")
    kw.setdefault("hub", HUB)
    kw.setdefault("eyebrow", "Car accidents · Summerville, SC")
    kw.setdefault("author", "tara")
    kw.setdefault("priority", 0.7)
    return page(slug, **kw)


# ----------------------------------------------------------------------------- HUB
hub_body = (
    answer("If another driver caused your crash in Summerville, that driver's insurance company owes you for your medical bills, lost income, vehicle damage and pain and suffering. You do not have to give them a recorded statement, and you should not accept a settlement before you know what your treatment will cost. Our consultation is free, and we are paid only if we recover money for you.", "The short version") +
    '<h2>Summerville\'s roads, and who gets hurt on them</h2>'
    '<p>Summerville has grown faster than its roads. I-26 between exits 194 and 205 carries commuters, tourists and the freight traffic from the port; Highway 17-A, Dorchester Road, Bacons Bridge Road, Old Trolley Road, Ladson Road and North Main Street funnel that growth through intersections designed for a much smaller town. The crashes we see most often are rear-end collisions in stop-and-go traffic on Main Street and Dorchester Road, left-turn and failure-to-yield crashes at the big intersections, interstate collisions near the 17-A and College Park interchanges, and distracted or impaired drivers on the two-lane roads out toward Ridgeville and Knightsville.</p>'
    f'<p>Jack Frost worked those roads for years as a Summerville police officer. He knows what a collision report says and what it leaves out. Tara Frost, who leads every injury case, sat as a Dorchester County magistrate judge where civil claims are tried. Our page on {A(HUB + "/where-crashes-happen-in-summerville", "where crashes happen in Summerville")} goes intersection by intersection.</p>'
    '<h2>What we handle</h2>'
    f'[[cards:{HUB}/hit-and-run-accidents,{HUB}/distracted-driving-accidents,practice-areas/drunk-driving-accidents,{HUB}/uninsured-motorist-accidents,practice-areas/rideshare-accidents,{HUB}/delivery-driver-accidents]]'
    '<p>Also rear-end and intersection collisions, multi-vehicle pileups on I-26, crashes with commercial vehicles and government vehicles, and collisions that injure passengers, cyclists and pedestrians.</p>'
    '<h2>What you can recover</h2>'
    + checks([
        "<b>Medical expenses</b>, past and future: the ambulance, the emergency room, imaging, surgery, physical therapy, injections, medication and the care you will need years from now.",
        "<b>Lost income and earning capacity</b>: the paychecks you missed and the work you can no longer do.",
        "<b>Pain, suffering and loss of enjoyment of life</b>: the part of the claim insurers most want to minimize, and the part a jury understands best.",
        "<b>Property damage</b>: repair or the vehicle's value, a rental while it is being fixed, and the diminished value of a repaired car.",
        "<b>Punitive damages</b> when the other driver was drunk, racing, or otherwise reckless.",
    ]) +
    '<h2>How South Carolina car accident law works</h2>'
    + steps([
        ("It is an at-fault state.", f" The driver who caused the crash pays, through their liability insurance. Every South Carolina driver must carry at least $25,000 per person and $50,000 per crash for injuries ({cite('min_liability')}), which is rarely enough for a serious injury. {A(HUB + '/is-south-carolina-an-at-fault-state', 'How at-fault works')}."),
        ("Fault can be shared.", f" You can recover as long as you were not more than 50 percent at fault; your award is reduced by your percentage. Insurers use this rule to shave every claim, which is why the evidence matters. {A(HUB + '/south-carolina-comparative-negligence', 'The comparative negligence rule')}."),
        ("Your own policy may pay too.", f" Uninsured motorist coverage is mandatory in South Carolina and underinsured coverage must be offered to you; both pay when the at-fault driver has no insurance or too little. {A(HUB + '/uninsured-motorist-accidents', 'UM and UIM claims')}."),
        ("There is a deadline.", f" Three years from the crash to file suit, two years if a government vehicle or road defect is involved, and practical deadlines much sooner than that for evidence. {A(HUB + '/south-carolina-car-accident-statute-of-limitations', 'The statute of limitations')}."),
    ]) +
    '<h2>What to do now</h2>'
    f'<p>Get checked by a doctor, keep every piece of paper, photograph everything, and do not talk to the other driver\'s insurer until you have talked to us. The full checklist is on {A(HUB + "/what-to-do-after-a-car-accident-in-south-carolina", "what to do after a car accident in South Carolina")}, and the reasons behind the most important rule are on {A(HUB + "/should-i-talk-to-the-other-drivers-insurance-company", "should I talk to the other driver’s insurance company")}.</p>'
    '<h2>How we build a car accident case</h2>'
    + steps([
        ("Preserve the evidence.", " Within days we request the collision report, the 911 call, body-camera and dash-camera video, and surveillance footage from businesses near the scene, and we send preservation letters so the other vehicle's event-data recorder is not destroyed."),
        ("Document the injury.", " We gather every record and bill, and where the injury is lasting we work with your doctors, and sometimes a life-care planner, to project future care."),
        ("Find all the coverage.", " The at-fault driver's policy, any employer's policy if they were working, your UM/UIM coverage, and medical-payments coverage. Most people are surprised how much insurance actually applies."),
        ("Demand, negotiate, and if necessary file suit.", " We send a demand that documents the full claim. If the insurer will not pay what the case is worth, we file in the Court of Common Pleas of the county where the crash happened and prepare for trial."),
    ]) +
    '<h2>Free case review</h2><p>Tell us what happened. We will tell you whether you have a claim, what it may be worth, and what to do next.</p>[[form]]'
    + band("Hurt in a crash in Summerville?", "Call before you talk to the insurance company. No fee unless we win.")
)
page(HUB, kind="hub", section_label="Car accident guides", hero_image="summerville-downtown.jpg", hero_caption="Downtown Summerville",
     title="Summerville Car Accident Lawyer | Free Consultation | Frost Law Group",
     description="Injured in a car accident in Summerville, SC? Frost Law Group's car accident lawyers, a former judge and a former police officer, handle the insurer so you can heal. Free consultation, no fee unless we win.",
     h1="Summerville Car Accident Lawyer", eyebrow="Car accidents · Summerville, SC", nav_label="Car accidents",
     lead="Injured by a negligent driver on I-26, Highway 17-A, Dorchester Road or anywhere in the Lowcountry? We hold them, and their insurer, accountable. Free consultation; you pay nothing unless we win.",
     summary="Rear-end, intersection, interstate, hit-and-run and drunk-driver collisions. What South Carolina's at-fault rules mean for your claim.",
     body=hub_body, priority=0.9,
     faqs=[
         ("How long do I have to file a car accident claim in South Carolina?", "Three years from the date of the crash for a claim against another driver (S.C. Code § 15-3-530). Two years if the at-fault driver was working for a city, county or state agency. Insurance claims should be opened within days, and the evidence that proves fault can disappear within weeks."),
         ("What if the other driver was uninsured?", "Your own uninsured motorist (UM) coverage pays, at limits at least equal to your liability limits. If the other driver had insurance but not enough, your underinsured motorist (UIM) coverage pays if you bought it. We check every policy in the household."),
         ("How much is my car accident case worth?", "It depends on the medical bills and future care, lost wages, the effect on your daily life, whether fault is disputed and how much insurance is available. We give an honest range once we have the report, the records and the policy limits, not before."),
         ("Should I accept the first settlement offer from the insurance company?", "Almost never. The first offer usually arrives before your treatment is finished and before anyone knows what the injury will cost. Once you sign the release, the claim is over, even if you need surgery next month."),
         ("What if I was partly at fault for the accident?", "You can still recover as long as you were not more than 50 percent at fault. Your recovery is reduced by your share: 20 percent at fault means you recover 80 percent of your damages. Insurers exaggerate your share, which is why the evidence has to be gathered early."),
         ("Do you handle crashes in Goose Creek, Ladson and North Charleston too?", "Yes. We handle crashes throughout Dorchester, Berkeley, Charleston and Colleton counties. Each community page explains which agency writes the report there and which court hears the case."),
     ],
     related=[HUB + "/what-to-do-after-a-car-accident-in-south-carolina", HUB + "/should-i-talk-to-the-other-drivers-insurance-company", "practice-areas/truck-accidents"])

# ----------------------------------------------------------------------------- SPOKES
sp(HUB + "/what-to-do-after-a-car-accident-in-south-carolina",
   title="What to Do After a Car Accident in South Carolina | First 48 Hours",
   description="Step by step: at the scene, at the hospital, and in the first two days after a crash in Summerville or anywhere in South Carolina, including the reports you must file and the calls you should not take.",
   h1="What to do after a car accident in South Carolina: the first 48 hours",
   summary="At the scene, at the hospital, and the calls to make (and not make) in the first two days.",
   lead="What you do in the first two days decides how strong your claim is. Here is the order, with the South Carolina rules behind each step.",
   body=(
       answer("Stay at the scene, call 911, get medical care the same day even if you feel fine, photograph everything, get the officer's name and report number, report the crash to your own insurer, and do not give a recorded statement to the other driver's insurance company until you have talked to a lawyer.")
       + '<h2>At the scene</h2>'
       + steps([
           ("Stop, and stay.", f" South Carolina law requires a driver involved in a crash with injury or death to stop, render reasonable aid and exchange information ({cite('hit_run')}). Leaving is a crime, and it destroys a claim."),
           ("Call 911.", f" A crash with injury, death or significant property damage must be reported to law enforcement immediately ({cite('report_duty')}). Inside the town limits the Summerville Police Department responds; on I-26 and most state highways it is the Highway Patrol; elsewhere the county sheriff. The officer's report is the document every insurer reads first."),
           ("Photograph everything before the cars move.", " All four corners of each vehicle, the damage up close, the whole scene from a distance, skid marks, debris, traffic signals and signs, the other driver's license plate, insurance card and license, and your own injuries."),
           ("Get names.", " The other driver, every passenger, and every witness, with phone numbers. Witnesses leave in minutes and are nearly impossible to find later."),
           ("Say less.", " Exchange information and answer the officer's questions truthfully. Do not apologize, do not say you are fine, and do not discuss fault with the other driver. Adrenaline hides injuries, and “I'm okay” will be quoted back to you."),
           ("Get the report number.", " The officer will give you a Form FR-10 (the insurance verification form) and a report number. The full collision report (Form TR-310) is available from the SCDMV in a week or two; we obtain it for our clients."),
       ])
       + '<h2>At the hospital or the doctor</h2>'
       + steps([
           ("Get examined the same day.", f" Whiplash, concussions, disc injuries and internal bleeding can take hours or days to show symptoms. A same-day visit protects your health and creates the record that ties the injury to the crash. {A(HUB + '/auto-injury-assessment-after-a-crash', 'Getting evaluated after a crash')} explains the options in Summerville."),
           ("Tell the provider it was a car accident.", " And describe every symptom, not just the worst one. The chart from the first visit is the most important medical record in the case."),
           ("Follow the treatment plan.", " Gaps in treatment are the insurer's favorite argument that you were not really hurt."),
       ])
       + '<h2>The first two days</h2>'
       + steps([
           ("Report the crash to your own insurance company.", " Your policy requires prompt notice, and your own coverage (medical payments, collision, uninsured and underinsured motorist) may be the coverage that actually pays. Reporting is not the same as giving a recorded statement about fault."),
           ("File the DMV form if no officer investigated.", f" If law enforcement did not come to the scene, the driver must file Form FR-309 with the SCDMV within 15 days when there is injury, death or property damage over $1,000 ({cite('report_dmv')})."),
           ("Do not talk to the other driver's insurer yet.", f" Their adjuster will call within a day, sound friendly, and ask for a recorded statement. You are not required to give one. {A(HUB + '/should-i-talk-to-the-other-drivers-insurance-company', 'Why, and what to say instead')}."),
           ("Do not sign anything.", " Not a medical authorization, not a property-damage release that quietly covers injuries, not a check. A release ends the claim."),
           ("Start a file.", " Photos, the FR-10, every bill, every receipt, mileage to appointments, and a short daily note about pain and what you could not do. Stay off social media about the crash."),
           ("Call a lawyer.", " The consultation is free. Even if you never hire us, you will know what the claim is worth and what the adjuster is about to do."),
       ])
       + callout("<b>Frost first:</b> the most expensive mistake we see is a recorded statement given on day two, when the victim felt fine and said so. By day ten they had a herniated disc and an adjuster with a recording.")
       + '<h2>Getting the report in Summerville</h2>'
       + f'<p>Reports from the {link("summerville_pd", "Summerville Police Department")} and the {link("dorchester_sheriff", "Dorchester County Sheriff’s Office")} can be requested from the agency; Highway Patrol reports come through the {link("scdmv_reports", "SCDMV")}. We request the report, the 911 audio and any body-camera video for every client at no cost.</p>'
   ),
   faqs=[
       ("Do I have to call the police for a minor accident in South Carolina?", "If anyone is hurt or property damage is significant, yes: the law requires an immediate report. For a true fender-bender with no injuries you may exchange information, but a police report is still the best protection if the other driver later changes their story."),
       ("How do I get a copy of my accident report?", "Ask the agency that responded (Summerville Police, the county sheriff or the Highway Patrol) for the report number, then request the TR-310 from that agency or the SCDMV. We obtain it for clients as part of the free consultation."),
       ("What if I did not feel hurt at the scene but hurt the next day?", "That is common. See a doctor as soon as symptoms appear, tell them about the crash, and call us. A delay of a day or two is explainable; a delay of weeks is what insurers use to deny claims."),
       ("Should I post about the accident on Facebook or Nextdoor?", "No. Insurers search social media, and a photo of you at a cookout becomes “evidence” that you are not injured. Ask friends not to tag you."),
   ],
   sources=[("S.C. Code § 56-5-1210 (duty to stop and render aid)", "https://www.scstatehouse.gov/code/t56c005.php", False), ("S.C. Code § 56-5-1260 and § 56-5-1270 (accident reports)", "https://www.scstatehouse.gov/code/t56c005.php", False)],
   related=[HUB + "/should-i-talk-to-the-other-drivers-insurance-company", HUB + "/auto-injury-assessment-after-a-crash", HUB + "/south-carolina-car-accident-statute-of-limitations"])

sp(HUB + "/is-south-carolina-an-at-fault-state",
   title="Is South Carolina an At-Fault State? | Car Accident Claims Explained",
   description="Yes. South Carolina is an at-fault (tort) state: the driver who caused the crash, and that driver's insurer, pay for your injuries. What that means for your claim, and how shared fault works.",
   h1="Is South Carolina an at-fault state?",
   summary="Yes. What that means for who pays after a crash, and how shared fault changes the number.",
   lead="Yes. South Carolina is an at-fault state, which decides who pays after a crash and how you get paid.",
   body=(
       answer("Yes. South Carolina is an at-fault (tort) state. The driver who caused the crash is legally responsible for the harm, and you claim against that driver's liability insurance. There is no no-fault or personal injury protection (PIP) system here; your own policy comes into play mainly through medical-payments, collision, uninsured and underinsured motorist coverage.")
       + '<h2>What “at fault” means in practice</h2>'
       + '<p>In a no-fault state, your own insurer pays your medical bills regardless of who caused the crash, and lawsuits are limited. South Carolina does the opposite. After a crash you (or your lawyer) make a claim against the at-fault driver\'s liability insurer, that insurer investigates fault, and it pays only if it agrees its driver was responsible. If it does not agree, or does not offer enough, the dispute is resolved by a lawsuit in the county where the crash happened.</p>'
       + f'<p>Every South Carolina driver must carry liability coverage of at least $25,000 per person, $50,000 per crash for bodily injury, and $25,000 for property damage ({cite("min_liability")}). Those are minimums; many drivers carry more, and many carry exactly that.</p>'
       + '<h2>Fault is a percentage, not a switch</h2>'
       + f'<p>South Carolina uses modified comparative negligence: you can recover as long as your share of fault is not greater than 50 percent, and your recovery is reduced by your percentage. If you were 10 percent at fault for a $100,000 injury, you recover $90,000. If you were 51 percent at fault, you recover nothing. {A(HUB + "/south-carolina-comparative-negligence", "How the 51 percent rule works")} and how insurers use it.</p>'
       + '<h2>What your own policy does in an at-fault state</h2>'
       + checks([
           f"<b>Uninsured motorist (UM)</b> coverage is required in South Carolina ({cite('um')}) and pays when the at-fault driver has no insurance, cannot be identified (hit-and-run), or was driving a stolen car.",
           f"<b>Underinsured motorist (UIM)</b> coverage must be offered to you ({cite('uim')}) and pays when the at-fault driver's limits are less than your damages. It is the most important coverage most people never think about.",
           "<b>Medical payments (MedPay)</b> pays your medical bills up to its limit regardless of fault, quickly, and is optional.",
           "<b>Collision</b> repairs your car regardless of fault, subject to your deductible, which your insurer then recovers from the at-fault driver.",
       ])
       + '<h2>Why at-fault favors people who prepare</h2>'
       + '<p>Because fault is decided by evidence, the side that gathers evidence first usually wins the argument. Insurers have adjusters at the scene within a day. Most injured people have a phone with a few photos. The collision report, the 911 audio, the body-camera video, the store camera across the street and the event-data recorder in the other car all exist for a short time. Getting them is the first thing we do.</p>'
       + callout("<b>Frost first:</b> in an at-fault state, the other driver's insurer is your opponent from the first phone call, however pleasant the adjuster sounds. Its job is to find fault in you.")
   ),
   faqs=[
       ("Does South Carolina have no-fault insurance or PIP?", "No. South Carolina is a pure at-fault state. Medical-payments coverage is available but optional, and there is no PIP requirement."),
       ("Who decides who was at fault?", "First the insurance adjusters, based on the collision report, statements and evidence. If the parties disagree, a judge or jury decides. The officer's opinion on the report is influential but not final."),
       ("Can I sue the other driver directly?", "Yes. Suit is filed against the driver (and sometimes the vehicle owner or employer), and that driver's insurer defends and pays up to the policy limits."),
       ("What if the at-fault driver was on the job?", "The employer's commercial policy usually applies, which often means far higher limits. Delivery, rideshare, trucking and company vehicles all have their own rules."),
   ],
   sources=[("S.C. Code § 38-77-140 (minimum liability coverage)", "https://www.scstatehouse.gov/code/t38c077.php", False), ("S.C. Code §§ 38-77-150 and 38-77-160 (UM and UIM coverage)", "https://www.scstatehouse.gov/code/t38c077.php", False)],
   related=[HUB + "/south-carolina-comparative-negligence", HUB + "/uninsured-motorist-accidents", HUB + "/south-carolina-car-accident-laws"])

sp(HUB + "/south-carolina-comparative-negligence",
   title="South Carolina Comparative Negligence | The 51% Rule Explained",
   description="South Carolina's modified comparative negligence rule: you recover if you were 50 percent or less at fault, reduced by your share. How insurers use it after a crash, with examples.",
   h1="How comparative negligence works in South Carolina: the 51 percent rule",
   summary="You recover if you were 50 percent or less at fault, minus your share. How adjusters use the rule against you.",
   lead="Fault is a percentage in South Carolina, and the percentage is where most car accident claims are won or lost.",
   body=(
       answer("South Carolina follows modified comparative negligence with a 51 percent bar. An injured person can recover damages if their share of fault is 50 percent or less, and the award is reduced by that share. At 51 percent or more, they recover nothing. The rule comes from the South Carolina Supreme Court's decision in Nelson v. Concrete Supply Co. (1991) and applies to car, truck, motorcycle, pedestrian and premises cases alike.")
       + '<h2>Three examples</h2>'
       + table(["Your share of fault", "Your damages", "You recover"], [
           ["0%", "$100,000", "$100,000"],
           ["25% (you were speeding slightly when the other driver ran the light)", "$100,000", "$75,000"],
           ["50% (both drivers changed lanes into each other)", "$100,000", "$50,000"],
           ["51% or more", "$100,000", "$0"],
       ])
       + '<h2>How insurers use the rule</h2>'
       + '<p>An adjuster does not need to prove you caused the crash. They need to argue you contributed: you were going 5 over, you did not brake soon enough, you were on the phone, you were not wearing a seat belt, you could have swerved. Every percentage point they assign to you is a discount on what they pay. The first recorded statement is where those points are harvested: “I looked down for a second,” “I might have been going a little fast,” “I didn\'t see him until it was too late.”</p>'
       + f'<p>Some of those arguments fail as a matter of law. Not wearing a seat belt, for example, cannot be used as evidence of negligence in a South Carolina civil case ({cite("seatbelt")}). Others are questions of fact that a jury decides, which is why we gather the evidence that answers them: the video, the data, the physical evidence at the scene.</p>'
       + '<h2>More than one at-fault party</h2>'
       + f'<p>When two or more defendants share fault (two drivers, a driver and a trucking company, a driver and a bar that overserved him), South Carolina generally allows you to collect the whole judgment from any defendant who was 50 percent or more at fault, while a defendant less than 50 percent at fault pays only its share ({cite("joint_liability")}). Identifying every responsible party matters more than most people realize.</p>'
       + '<h2>Comparative negligence in other kinds of cases</h2>'
       + checks([
           f"<b>Motorcycle crashes:</b> insurers lean on rider stereotypes to inflate the rider's share. {A('practice-areas/motorcycle-accidents', 'How we answer that')}.",
           f"<b>Pedestrian crashes:</b> a pedestrian outside a crosswalk shares fault, but the driver's duty of due care never goes away. {A('practice-areas/pedestrian-accidents', 'Pedestrian cases')}.",
           f"<b>Slip and fall:</b> the store argues the hazard was open and obvious and you should have seen it. {A('practice-areas/slip-and-fall', 'Premises claims')}.",
           f"<b>Dog bites:</b> the statute removes the owner's defenses except provocation and trespass. {A('practice-areas/dog-bites/south-carolina-dog-bite-law', 'The dog-bite statute')}.",
       ])
       + callout("<b>Frost first:</b> never estimate your own fault to an adjuster. “I guess I could have stopped sooner” becomes 30 percent on their worksheet. Describe what happened; let the evidence assign the percentages.")
   ),
   faqs=[
       ("Is South Carolina a 50 percent or 51 percent state?", "Both descriptions are used. You can recover if your fault is 50 percent or less; you are barred at 51 percent or more. The bar is sometimes called the 51 percent rule and sometimes the “not greater than” rule."),
       ("Who decides the percentages?", "If the case settles, the adjusters and lawyers negotiate them. If it goes to trial, the jury assigns a percentage to each party on the verdict form and the judge applies the reduction."),
       ("Does comparative negligence apply to property damage too?", "Yes. Your vehicle claim is reduced by your share of fault the same way."),
       ("Can my passenger recover if I was partly at fault?", "Yes. A passenger who did nothing wrong recovers in full, from your policy, the other driver's policy or both, depending on the percentages."),
   ],
   sources=[("S.C. Code § 15-38-15 (apportionment among joint tortfeasors)", "https://www.scstatehouse.gov/code/t15c038.php", False), ("S.C. Code § 56-5-6540 (seat belt evidence)", "https://www.scstatehouse.gov/code/t56c005.php", False)],
   related=[HUB + "/is-south-carolina-an-at-fault-state", HUB + "/should-i-talk-to-the-other-drivers-insurance-company", "practice-areas/motorcycle-accidents"])

sp(HUB + "/south-carolina-car-accident-statute-of-limitations",
   title="South Carolina Car Accident Statute of Limitations | 3 Years, With Exceptions",
   description="You have three years from a South Carolina car accident to file suit, two years if a government vehicle or agency is involved, and different rules for minors and wrongful death. What the deadline means in practice.",
   h1="How long do I have to file a car accident claim in South Carolina?",
   summary="Three years to file suit, two against government entities, and practical deadlines that arrive much sooner.",
   lead="Three years is the number everyone quotes. It is right for most cases and dangerously wrong for some.",
   body=(
       answer(f"Three years from the date of the crash to file a lawsuit for personal injury or property damage in South Carolina ({cite('sol_injury')}). Two years if the claim is against a city, county, state agency or their employee, such as a crash with a government vehicle or caused by a road defect ({cite('tort_claims')}). A wrongful death claim runs three years from the date of death. A minor's own claim is generally paused until age 18. Insurance claims have no statutory deadline but must be reported promptly under your policy, and the evidence disappears long before three years.")
       + '<h2>The deadlines, side by side</h2>'
       + table(["Claim", "Deadline to file suit", "Source"], [
           ["Injury or property damage from another driver", "3 years from the crash", cite("sol_injury")],
           ["Wrongful death", "3 years from the date of death", cite("sol_injury", "S.C. Code § 15-3-530(6)")],
           ["Claim against a government entity or employee (Tort Claims Act)", "2 years, or 3 years if a verified claim is filed with the entity within 1 year", cite("tort_claims")],
           ["Injured person under 18", "Generally paused until age 18, then the ordinary period runs", cite("sol_minor")],
           ["Uninsured / underinsured motorist claim against your own insurer", "Contract deadlines apply; treat it as 3 years and report immediately", "Your policy"],
       ])
       + '<h2>Why three years is not really three years</h2>'
       + checks([
           "<b>Video is overwritten in days.</b> Gas stations, restaurants and traffic cameras keep footage for a week or two. Dash-camera and body-camera video is retained on a schedule.",
           "<b>Vehicles are crushed in weeks.</b> The event-data recorder in the other car, which records speed, braking and throttle in the seconds before impact, goes to the salvage yard with the car.",
           "<b>Witnesses move and forget.</b> A statement taken in week one is worth ten taken in year two.",
           "<b>Insurers set their reserves early.</b> The number an adjuster writes in the file in the first month anchors every offer after it.",
           "<b>Suit takes time to prepare.</b> Filing on the last day with no records, no experts and no witnesses is filing to lose.",
       ])
       + '<h2>Government defendants: the trap</h2>'
       + f'<p>Crashes involving a town or county vehicle, a school bus, a CARTA or Tri-County Link bus, a police cruiser, or a dangerous road condition maintained by SCDOT fall under the South Carolina Tort Claims Act. The deadline is two years, damages are capped at $300,000 per person and $600,000 per occurrence ({cite("tort_claims_cap")}), and punitive damages are not available. If you think a government vehicle or a road defect was involved, call within weeks, not months.</p>'
       + '<h2>What the deadline does not change</h2>'
       + '<p>The statute of limitations is the last day to file a lawsuit. It is not the deadline to hire a lawyer, to report the crash to your insurer, or to see a doctor. Those should all happen in the first week. Most claims settle without a lawsuit, but they settle for full value only when the insurer believes a lawsuit will be filed on time and tried well.</p>'
       + callout("<b>Frost first:</b> if you are reading this more than two years after the crash, call today. If it is more than three years, call anyway; there are exceptions, and we will tell you honestly whether one applies.")
   ),
   faqs=[
       ("Does the three years start from the crash or from when I found out I was hurt?", "From the crash, in nearly every car accident case. The “discovery rule” that delays the start date applies only when a reasonable person could not have known they were injured, which is rare after a collision."),
       ("What if the other driver died or moved out of state?", "The claim survives against the driver's estate, and out-of-state drivers can be served through South Carolina's long-arm rules. The deadline does not change."),
       ("Does filing an insurance claim stop the clock?", "No. Only filing a lawsuit stops the statute of limitations. An insurer will happily negotiate past the deadline and then deny the claim as time-barred."),
       ("My child was hurt. Do we have to wait?", "No. A parent can bring the claim now, and the child's own claim is preserved until adulthood. Settlements for minors are approved by the court to protect the child."),
   ],
   sources=[("S.C. Code § 15-3-530 (three-year limitations period)", "https://www.scstatehouse.gov/code/t15c003.php", False), ("S.C. Code § 15-78-110 (Tort Claims Act limitations)", "https://www.scstatehouse.gov/code/t15c078.php", False)],
   related=[HUB + "/what-to-do-after-a-car-accident-in-south-carolina", "practice-areas/wrongful-death/south-carolina-wrongful-death-statute", HUB + "/uninsured-motorist-accidents"])

sp(HUB + "/south-carolina-car-accident-laws",
   title="South Carolina Car Accident Laws, Explained | Insurance, Reporting, Fault",
   description="The South Carolina laws that decide a car accident claim: minimum insurance, the duty to stop and report, the seat-belt evidence rule, the texting and hands-free laws, and comparative fault, in plain English with citations.",
   h1="South Carolina car accident laws, explained",
   summary="Minimum insurance, reporting duties, the seat-belt rule, the phone laws and comparative fault, with citations.",
   lead="Seven statutes decide most car accident claims in South Carolina. Here they are in plain English, with the citation for each.",
   body=(
       answer("South Carolina is an at-fault state with modified comparative negligence (recover if 50 percent or less at fault). Drivers must carry at least 25/50/25 liability coverage plus uninsured motorist coverage. Drivers must stop after a crash and report it when there is injury or significant damage. Failing to wear a seat belt cannot be used against you in a civil case. Texting while driving is illegal. Suit must be filed within three years.")
       + '<h2>1. Fault and comparative negligence</h2>'
       + f'<p>The driver who causes a crash is responsible for the harm. If the injured person shares fault, the recovery is reduced by their percentage, and barred at 51 percent. {A(HUB + "/is-south-carolina-an-at-fault-state", "At-fault explained")} and {A(HUB + "/south-carolina-comparative-negligence", "the 51 percent rule")}.</p>'
       + '<h2>2. Minimum insurance</h2>'
       + f'<p>Every registered vehicle must carry liability coverage of at least $25,000 per person and $50,000 per accident for bodily injury and $25,000 for property damage ({cite("min_liability")}), plus uninsured motorist coverage at the same minimums ({cite("um")}). Insurers must offer underinsured motorist coverage ({cite("uim")}). Driving without insurance is a crime and leads to license and registration suspension, but plenty of people do it, which is why UM coverage is required.</p>'
       + '<h2>3. Duty to stop, help and exchange information</h2>'
       + f'<p>A driver in a crash involving injury or death must stop at the scene, give their name, address, registration and license, and render reasonable assistance ({cite("hit_run")}). Leaving is a felony when someone is hurt. {A(HUB + "/hit-and-run-accidents", "What to do after a hit-and-run")}.</p>'
       + '<h2>4. Duty to report</h2>'
       + f'<p>A crash with injury, death or property damage of $1,000 or more must be reported immediately to the local police, the sheriff or the Highway Patrol ({cite("report_duty")}). If no officer investigates, the driver must send Form FR-309 to the SCDMV within 15 days ({cite("report_dmv")}). The officer\'s collision report (TR-310) is the foundation of every claim.</p>'
       + '<h2>5. The seat-belt evidence rule</h2>'
       + f'<p>Adults must wear seat belts, but a violation is not negligence and is not admissible as evidence in a civil case ({cite("seatbelt")}). An adjuster who says “you weren\'t wearing your seat belt, so we are reducing the offer” is bluffing.</p>'
       + '<h2>6. Phones and distraction</h2>'
       + f'<p>Texting while driving has been illegal in South Carolina since 2014 ({cite("texting")}). In 2025 the General Assembly went further with a hands-free law that prohibits holding a phone while driving. A violation is evidence of negligence in a civil case, and phone records can be subpoenaed. {A(HUB + "/distracted-driving-accidents", "Distracted-driving crashes")}.</p>'
       + '<h2>7. Deadlines</h2>'
       + f'<p>Three years to file suit for injury or property damage, two years against government entities, three years from death for wrongful death ({cite("sol_injury")}). {A(HUB + "/south-carolina-car-accident-statute-of-limitations", "The statute of limitations")}.</p>'
       + '<h2>Laws that surprise people</h2>'
       + checks([
           f"<b>Punitive damages have no cap when the at-fault driver was drunk.</b> The usual cap on punitive damages does not apply to a defendant whose judgment was impaired by alcohol or drugs ({cite('punitive_exceptions')}). {A('practice-areas/drunk-driving-accidents', 'Drunk-driving crash claims')}.",
           "<b>Diminished value is recoverable.</b> A repaired car is worth less than one that was never wrecked, and South Carolina lets you claim the difference from the at-fault driver's insurer.",
           "<b>Your medical bills are your evidence, even if insurance paid them.</b> South Carolina generally lets you present the amount billed, not just the amount your health insurer paid.",
           f"<b>Rideshare drivers carry special coverage.</b> Uber and Lyft must provide at least $1,000,000 in liability coverage during a ride ({cite('tnc')}). {A('practice-areas/rideshare-accidents', 'Uber and Lyft crashes')}.",
           f"<b>Motorcycle riders over 21 need not wear a helmet.</b> ({cite('helmet')}). {A('practice-areas/motorcycle-accidents/south-carolina-motorcycle-helmet-law', 'What that means for a claim')}.",
       ])
   ),
   faqs=[
       ("Is South Carolina a no-fault state?", "No. It is an at-fault state. The at-fault driver's insurer pays; there is no PIP requirement."),
       ("What is the minimum car insurance in South Carolina?", "$25,000 per person and $50,000 per accident for bodily injury, $25,000 for property damage, plus uninsured motorist coverage at the same limits."),
       ("Do I have to report a minor accident in South Carolina?", "Yes if anyone was hurt or property damage is $1,000 or more, which today is nearly any crash involving body damage. Report it to law enforcement immediately, and to the DMV within 15 days if no officer investigated."),
       ("Is it illegal to use a phone while driving in South Carolina?", "Texting has been banned since 2014, and a 2025 hands-free law prohibits holding a phone while driving. Either violation is powerful evidence in an injury claim."),
   ],
   sources=[("S.C. Code Title 56, Chapter 5 (Uniform Act Regulating Traffic on Highways)", "https://www.scstatehouse.gov/code/t56c005.php", False), ("S.C. Code Title 38, Chapter 77 (automobile insurance)", "https://www.scstatehouse.gov/code/t38c077.php", False), ("S.C. Code Title 15, Chapter 32 (damages)", "https://www.scstatehouse.gov/code/t15c032.php", False)],
   related=[HUB + "/is-south-carolina-an-at-fault-state", HUB + "/south-carolina-car-accident-statute-of-limitations", HUB + "/uninsured-motorist-accidents"])

sp(HUB + "/should-i-talk-to-the-other-drivers-insurance-company",
   title="Should I Talk to the Other Driver's Insurance Company? | South Carolina",
   description="No, not before you talk to a lawyer. Why the other driver's adjuster calls so quickly, what a recorded statement is used for, what you must report to your own insurer, and what to say instead.",
   h1="Should I talk to the other driver's insurance company after a crash?",
   summary="No, not before you talk to a lawyer. What the adjuster's call is really for, and what to say instead.",
   lead="The adjuster will call within a day, sound kind, and ask how you are doing. Here is what that call is for.",
   body=(
       answer("No. You are not required to speak to the other driver's insurance company, give a recorded statement, or sign a medical authorization, and doing any of those before you understand your injuries usually reduces what you recover. Report the crash to your own insurer as your policy requires, give the other driver's adjuster your lawyer's contact information, and say nothing else about how the crash happened or how you feel.")
       + '<h2>Why the adjuster calls so fast</h2>'
       + '<p>The other driver\'s insurer has one goal: close your claim for the smallest number it can justify. The fastest way to do that is to get you on a recording in the first days, while you are shaken, sore, and inclined to be polite. “I\'m doing okay” becomes proof you were not badly hurt. “It happened so fast” becomes proof you were not paying attention. “I think I was going about 40” becomes proof you were speeding. Every answer is compared to the collision report, your medical records and your later testimony, and any difference is called a credibility problem.</p>'
       + '<h2>The three requests, and the answer to each</h2>'
       + steps([
           ("“Can we get a recorded statement?”", " No. You have no legal obligation to give one to the other driver's insurer. If you have a lawyer, the adjuster deals with the lawyer. If you do not yet, say that you will provide a written statement through your attorney."),
           ("“Can you sign this medical authorization so we can pay your bills?”", " No. The blanket authorization lets them pull your entire medical history, looking for a prior back complaint or an old injury to blame. Your lawyer provides the records that relate to the crash."),
           ("“We can offer you $X today to wrap this up.”", " No. A check in the first weeks is a bet that your injuries are worse than they look. Once you sign the release, the claim is closed even if you need surgery next month."),
       ])
       + '<h2>What you do have to do</h2>'
       + checks([
           "<b>Report the crash to your own insurer promptly.</b> Your policy requires it, and your own coverage (MedPay, collision, UM and UIM) may be the coverage that actually pays. Reporting is not the same as giving a recorded statement about fault; you can report the basic facts and decline to go further until you have talked to a lawyer.",
           "<b>Cooperate with your own insurer's reasonable requests</b>, especially for a UM or UIM claim, where your own company steps into the at-fault driver's shoes and becomes, in effect, the opponent. We handle those statements for clients.",
           "<b>Be truthful with everyone.</b> Declining to answer is your right; inaccurate answers are not.",
       ])
       + '<h2>What to say instead</h2>'
       + '<p>“I\'m not able to discuss the accident or my injuries right now. Please send anything in writing to my address, and I\'ll have my attorney contact you.” Then hang up politely. You do not need to explain, and you do not need to be rude. Write down the adjuster\'s name, company, claim number and phone number.</p>'
       + '<h2>The property-damage exception, with a warning</h2>'
       + '<p>You can usually handle the car repair or total-loss claim directly with the at-fault insurer, and it is often faster than going through your own collision coverage. Two cautions: read the release before you sign it, because some property-damage releases quietly include bodily injury; and do not let the property-damage conversation drift into a discussion of how the crash happened or how you feel.</p>'
       + callout("<b>Frost first:</b> the adjuster is trained, is doing this for the fortieth time this month, and is recording. You are doing it for the first time, in pain. That is not a fair conversation, and you do not have to have it.")
   ),
   faqs=[
       ("Do I have to give a recorded statement to the other driver's insurer?", "No. There is no legal duty to speak to the other side's insurer at all. Their adjuster may tell you the claim cannot move without it; it can, through your attorney."),
       ("What if the other driver's insurer offers to pay my medical bills?", "They rarely do before settlement, and “we'll take care of your bills” is not a promise you can enforce. Use your health insurance and MedPay for treatment now; the at-fault insurer reimburses at settlement."),
       ("Can I talk to my own insurance company?", "Yes, and you must report the crash to them. Keep the first report to the basic facts (when, where, who, the report number) and tell them you will provide a full statement once you have spoken with an attorney."),
       ("The adjuster says I was at fault. Is the claim over?", "No. The adjuster's opinion is an opening position, not a verdict. Fault is decided by the evidence, and ultimately by a jury if necessary."),
   ],
   related=[HUB + "/what-to-do-after-a-car-accident-in-south-carolina", HUB + "/south-carolina-comparative-negligence", HUB + "/uninsured-motorist-accidents"])

sp(HUB + "/uninsured-motorist-accidents",
   title="Hit by an Uninsured or Underinsured Driver in SC? | UM & UIM Claims",
   description="What to do when the driver who hit you in Summerville or Goose Creek has no insurance or too little: how South Carolina's uninsured (UM) and underinsured (UIM) motorist coverage pays, stacking, and the mistakes that forfeit it.",
   h1="What if the driver who hit me has no insurance? UM and UIM claims in South Carolina",
   summary="Your own policy's uninsured and underinsured motorist coverage is usually the answer. How it works, and how to stack it.",
   lead="Roughly one in ten South Carolina drivers has no insurance, and many more carry the $25,000 minimum. Your own policy is built for exactly this.",
   body=(
       answer(f"If the at-fault driver has no insurance, your own uninsured motorist (UM) coverage pays your claim, up to your UM limits; every South Carolina policy must include it ({cite('um')}). If the at-fault driver has insurance but not enough, your underinsured motorist (UIM) coverage pays the difference, if you bought it ({cite('uim')}). Both coverages also apply to passengers and, in many cases, to family members in the household, and multiple policies can often be stacked.")
       + '<h2>Uninsured motorist (UM) coverage</h2>'
       + '<p>UM coverage is mandatory in South Carolina at least at the 25/50/25 minimums. It pays when the at-fault driver has no insurance, when the driver cannot be identified (a hit-and-run), or when the vehicle was stolen. A hit-and-run UM claim has a catch: the crash must be reported to law enforcement promptly, and if there was no physical contact with the other vehicle, an independent witness is required. That is one more reason to call 911 and get witness names at the scene.</p>'
       + '<h2>Underinsured motorist (UIM) coverage</h2>'
       + '<p>UIM is the coverage most people do not know they have, or wish they had. It pays when the at-fault driver\'s policy is smaller than your damages. A driver with the state-minimum $25,000 hits you, your surgery costs $90,000: the at-fault insurer pays $25,000 and your UIM pays the rest up to your UIM limits. Insurers must offer UIM in writing; if the offer was not made properly, courts have held that the coverage is read into the policy anyway. We review the offer form in every case.</p>'
       + '<h2>Stacking</h2>'
       + '<p>South Carolina allows stacking of UM and UIM coverage in many situations: if you own more than one insured vehicle, or if you were in someone else\'s car and also have your own policy, the limits of each policy may add together. Whether stacking applies depends on the wording and who was driving what. It is common for a claim that looked like a $25,000 policy-limits case to become a $125,000 case once every applicable policy is found.</p>'
       + '<h2>Your own insurer becomes the opponent</h2>'
       + '<p>On a UM or UIM claim, your own insurance company steps into the shoes of the at-fault driver and defends the claim the same way that driver\'s insurer would: disputing fault, questioning the injury, minimizing the bills. Loyalty to a long-time customer does not enter into it. You must cooperate with your own insurer, but you can, and should, do it through a lawyer.</p>'
       + '<h2>Mistakes that forfeit UM and UIM coverage</h2>'
       + checks([
           "<b>Settling with the at-fault driver without your UIM carrier's consent.</b> Your policy gives your insurer the right to approve any settlement with the at-fault driver so it can preserve its own claim against them. Sign without that consent and the UIM claim can be lost.",
           "<b>Not reporting a hit-and-run to police promptly.</b> The UM statute requires it.",
           "<b>Giving a recorded statement to your own insurer that understates the injury.</b> It is used the same way the other side would use it.",
           "<b>Missing the policy's notice and proof-of-loss requirements.</b> Report every crash to your own company, even when the other driver seems insured.",
       ])
       + '<h2>Goose Creek, Ladson and North Charleston</h2>'
       + f'<p>The searches that bring people to this page most often are for uninsured-motorist accidents in {A("areas/goose-creek", "Goose Creek")} and hit-and-run crashes in {A("areas/north-charleston", "North Charleston")}. The rules are the same everywhere in South Carolina; what changes is which police agency wrote the report and which court hears the case, and the community pages explain both.</p>'
       + callout("<b>Frost first:</b> before you accept a policy-limits offer from the other driver's insurer, call. Accepting it the wrong way can cost you your own UIM coverage.")
   ),
   faqs=[
       ("How do I know if the other driver was uninsured?", "The collision report lists the insurance information the driver gave the officer. We verify it with the insurer; a surprising number of policies listed at the scene were cancelled for non-payment weeks earlier."),
       ("Does UM coverage cost me anything to use? Will my rates go up?", "South Carolina prohibits insurers from raising your rates for a claim on a crash you did not cause. You may have a small deductible on property damage."),
       ("I was a passenger. Whose coverage applies?", "Potentially the at-fault driver's liability policy, the policy on the car you were in, and your own household's UM/UIM coverage. Passengers often have more coverage available than the driver."),
       ("What if I was hit while walking or cycling?", "Your own auto policy's UM and UIM coverage generally follows you as a pedestrian or cyclist. If you have no auto policy, a resident relative's policy may apply."),
   ],
   sources=[("S.C. Code § 38-77-150 (uninsured motorist coverage)", "https://www.scstatehouse.gov/code/t38c077.php", False), ("S.C. Code § 38-77-160 (underinsured motorist coverage)", "https://www.scstatehouse.gov/code/t38c077.php", False)],
   related=[HUB + "/hit-and-run-accidents", HUB + "/is-south-carolina-an-at-fault-state", HUB + "/should-i-talk-to-the-other-drivers-insurance-company"])

sp(HUB + "/hit-and-run-accidents",
   title="Hit-and-Run Accident Lawyer | Summerville & Goose Creek, SC",
   description="Hit by a driver who left the scene in Summerville, Goose Creek or North Charleston? How police find hit-and-run drivers, how your uninsured motorist coverage pays when they don't, and the witness rule that can sink a claim.",
   h1="Hit-and-run accidents in Summerville and Goose Creek",
   summary="How hit-and-run drivers are found, and how your own UM coverage pays when they are not.",
   lead="The driver left. You are still hurt. Here is how these claims actually get paid.",
   body=(
       answer(f"After a hit-and-run in South Carolina, report it to police immediately, get any witness's name, and photograph the damage and debris. If the driver is found, their liability insurance pays; if not, your own uninsured motorist coverage pays, provided the crash was reported promptly and, where there was no physical contact, an independent witness confirms what happened. Leaving the scene of an injury crash is a felony ({cite('hit_run')}), and the criminal case often produces the evidence for the civil claim.")
       + '<h2>The first hour</h2>'
       + steps([
           ("Call 911 from the scene.", " A prompt police report is a legal requirement for a UM hit-and-run claim, not just good practice. Tell the dispatcher the direction the vehicle went and anything you saw: color, type, partial plate, damage."),
           ("Find witnesses now.", " If the other vehicle never touched yours (they ran you off the road), South Carolina requires an independent witness for a UM claim. Ask everyone who stopped for a name and number."),
           ("Photograph everything.", " Paint transfer on your car, broken pieces in the road (they carry part numbers), tire marks, and the surrounding businesses whose cameras may have caught the vehicle."),
           ("Note the cameras.", " Gas stations, dollar stores, traffic signals, doorbell cameras on nearby houses. Footage is overwritten within days; we send preservation requests immediately."),
       ])
       + '<h2>How hit-and-run drivers are found</h2>'
       + '<p>More are found than people expect. Debris left at the scene identifies the make and model. Body shops report suspicious repairs. License-plate readers on major corridors, including I-26 and Rivers Avenue, log plates by time and location. Social media posts, and the driver\'s own guilty conscience, close many cases. Jack Frost spent fourteen years in Lowcountry law enforcement and knows which of these to push and whom to ask.</p>'
       + '<h2>Where the money comes from</h2>'
       + checks([
           "<b>The driver is identified:</b> their liability insurer pays, and the criminal charge for leaving the scene gives you real leverage. Punitive damages are available for the flight itself.",
           f"<b>The driver is never found:</b> your uninsured motorist coverage pays, up to your UM limits, and may stack across household policies. {A(HUB + '/uninsured-motorist-accidents', 'How UM claims work')}.",
           "<b>Your medical-payments coverage</b> pays bills right away regardless of who was at fault.",
           "<b>Health insurance</b> pays treatment now and is reimbursed from the settlement.",
       ])
       + '<h2>Goose Creek and North Charleston</h2>'
       + f'<p>Search data shows Goose Creek residents looking for hit-and-run lawyers more than any other community we serve. Crashes inside the city are investigated by Goose Creek Police; on the Highway 52 and 176 corridors outside the city limits, by the Berkeley County Sheriff\'s Office or the Highway Patrol. In North Charleston the police department\'s traffic unit handles hit-and-runs on Rivers Avenue, Dorchester Road and Ashley Phosphate. The community pages for {A("areas/goose-creek", "Goose Creek")} and {A("areas/north-charleston", "North Charleston")} list the agencies and the courts.</p>'
       + callout("<b>Frost first:</b> a hit-and-run UM claim can be denied for a late police report or a missing witness. Both problems are solved in the first hour and nearly impossible to fix later.")
   ),
   faqs=[
       ("Is a hit-and-run a felony in South Carolina?", "Leaving the scene of a crash involving injury is a felony; involving death, a more serious felony; involving only property damage, a misdemeanor. The driver's conviction is powerful evidence in the civil claim."),
       ("The driver ran me off the road but never hit me. Do I have a claim?", "Yes, but for a UM claim South Carolina requires the crash to be reported promptly and, because there was no contact, an independent witness who saw what happened. Get names at the scene."),
       ("Will my insurance rates go up if I use my UM coverage?", "No. South Carolina law prohibits surcharging you for a claim arising from a crash you did not cause."),
       ("How long does a hit-and-run investigation take?", "Days to months. We pursue the civil claim in parallel: preservation letters go out immediately, and if the driver is not found within a reasonable time, we open the UM claim."),
   ],
   sources=[("S.C. Code § 56-5-1210 (leaving the scene)", "https://www.scstatehouse.gov/code/t56c005.php", False), ("S.C. Code § 38-77-150 (uninsured motorist coverage)", "https://www.scstatehouse.gov/code/t38c077.php", False)],
   related=[HUB + "/uninsured-motorist-accidents", HUB + "/what-to-do-after-a-car-accident-in-south-carolina", "areas/goose-creek"])

sp(HUB + "/distracted-driving-accidents",
   title="Distracted Driving Accident Lawyer | Summerville & Goose Creek, SC",
   description="Hit by a driver who was texting or on the phone? How South Carolina's texting ban and hands-free law affect your claim, how phone records are obtained, and what distraction evidence looks like.",
   h1="Distracted driving accidents: proving the other driver was on the phone",
   summary="How South Carolina's texting and hands-free laws help your claim, and how we get the phone records.",
   lead="Most rear-end crashes on Main Street and Dorchester Road have the same cause. Proving it is the job.",
   body=(
       answer(f"A driver who was texting, scrolling or holding a phone when they hit you was violating South Carolina law ({cite('texting')} and the 2025 hands-free law), and that violation is evidence of negligence in your injury claim. Distraction is proved through the driver's phone records, which can be subpoenaed, plus the collision report, witness statements, the absence of skid marks, and vehicle data. Admit nothing about your own phone, and preserve your own records.")
       + '<h2>What South Carolina law says</h2>'
       + f'<p>South Carolina banned texting while driving in 2014 ({cite("texting")}). In 2025 the General Assembly passed a hands-free law prohibiting drivers from holding a phone at all while driving, bringing the state in line with Georgia and most of the Southeast. In an injury case the statute does two things: it makes the distracted driver\'s conduct negligence per se, and it makes the driver\'s phone records relevant, which means they can be obtained.</p>'
       + '<h2>What distraction looks like in the evidence</h2>'
       + checks([
           "<b>No braking.</b> A rear-end crash with no skid marks and no pre-impact braking in the event-data recorder tells a jury the driver never saw you.",
           "<b>The timing.</b> A text sent at 5:42:10 p.m. and a 911 call at 5:42:40 p.m. is the whole case.",
           "<b>Witnesses.</b> The driver behind them who saw the glow of the screen. We find them.",
           "<b>The driver's own words.</b> “I looked down for a second” on body-camera video.",
           "<b>Delivery and rideshare apps.</b> Drivers for Amazon, DoorDash, Uber and Lyft are required to interact with the app constantly; the app logs every tap.",
       ])
       + '<h2>Getting the phone records</h2>'
       + '<p>Phone carriers do not release records on request; they require a subpoena, which requires a lawsuit. This is one of the reasons a distracted-driving claim that the insurer refuses to value fairly is often worth filing. We send a preservation letter to the driver and the carrier immediately so the records exist when the subpoena arrives, and we request the driver\'s phone itself when the crash was serious enough to justify a forensic download.</p>'
       + '<h2>Your own phone</h2>'
       + '<p>Expect the other side to ask about your phone, too. Do not delete anything; deleting is worse than whatever was there. Do not volunteer your phone use to an adjuster. If you were hands-free, on a mounted phone, or not using it at all, your records will show that, and we will obtain them ourselves.</p>'
       + '<h2>Where it happens here</h2>'
       + f'<p>Stop-and-go traffic on North Main Street, Dorchester Road near the Oakbrook shopping centers, Bacons Bridge Road, and Highway 17-A through the Nexton area produces a steady stream of rear-end collisions, and the Goose Creek searches that bring people to this page cluster on Highway 52 and St. James Avenue. {A(HUB + "/where-crashes-happen-in-summerville", "Where crashes happen in Summerville")}.</p>'
       + callout("<b>Frost first:</b> if you suspect the other driver was on the phone, say so to the officer at the scene and tell us in the first call. A preservation letter sent in week one is worth more than a subpoena sent in year two.")
   ),
   faqs=[
       ("Is texting while driving illegal in South Carolina?", "Yes, since 2014, and a 2025 hands-free law prohibits holding a phone while driving. Violations are evidence of negligence in a civil case."),
       ("Can I get the other driver's phone records?", "Through a subpoena in a lawsuit, yes. Insurers will not hand them over voluntarily. We preserve them early so they exist when the subpoena issues."),
       ("Does distracted driving lead to punitive damages?", "It can. Punitive damages require reckless, willful or wanton conduct. Texting at highway speed, especially with a prior pattern, can meet that standard."),
       ("What if I was using my phone hands-free?", "Hands-free use is legal and is not evidence of fault on its own. Do not delete anything, and let us obtain your records so there is no dispute."),
   ],
   sources=[("S.C. Code § 56-5-3890 (texting while driving)", "https://www.scstatehouse.gov/code/t56c005.php", False), ("NHTSA – distracted driving", "https://www.nhtsa.gov/risky-driving/distracted-driving", False)],
   related=[HUB + "/where-crashes-happen-in-summerville", HUB + "/south-carolina-car-accident-laws", HUB + "/delivery-driver-accidents"])

sp("practice-areas/drunk-driving-accidents",
   title="Hit by a Drunk Driver in Summerville, SC? | Injury Claims & Punitive Damages",
   description="If a drunk driver hit you in Summerville or Goose Creek, South Carolina removes the cap on punitive damages, and the bar that overserved the driver may be liable too. How the criminal case and your civil claim work together.",
   h1="Hit by a drunk driver in Summerville? Your claim is different", nav_label="Drunk-driving crash victims",
   summary="Uncapped punitive damages, the bar's liability, and how the criminal case helps your civil claim.",
   lead="A crash caused by an impaired driver is an injury case with more defendants and more damages than an ordinary collision. Here is what changes.",
   eyebrow="Car accidents · Summerville, SC",
   body=(
       answer(f"If you were injured by a drunk driver in South Carolina, you can recover your full damages from the driver and their insurer, plus punitive damages with no statutory cap, because the cap does not apply to a defendant whose judgment was impaired by alcohol or drugs ({cite('punitive_exceptions')}). The bar or restaurant that served a visibly intoxicated driver may also be liable. The driver's criminal case for DUI or felony DUI runs separately from your civil claim, and its evidence (breath or blood results, video, the plea) becomes evidence in yours.")
       + '<h2>What is different about a drunk-driving injury claim</h2>'
       + steps([
           ("Punitive damages are uncapped.", f" South Carolina normally caps punitive damages at three times compensatory damages or $500,000, whichever is greater ({cite('punitive')}). The cap disappears when the defendant's judgment was impaired by alcohol or drugs ({cite('punitive_exceptions')}). Insurers know this, and it changes how they value the claim."),
           ("There may be a second defendant.", f" South Carolina courts allow claims against a bar, restaurant or store that sold alcohol to a person who was visibly intoxicated, based on the statute that makes such a sale unlawful ({cite('alcohol_sale')}). A commercial establishment carries far more insurance than a minimum-limits driver, and the receipt, the tab and the security video are evidence we move to preserve immediately."),
           ("The criminal case builds your evidence.", f" A driver who injures someone while impaired faces felony DUI ({cite('felony_dui')}). The blood or breath result, the dash-camera and body-camera video, the field sobriety tests and the eventual plea or conviction are all admissible in your civil case. We monitor the criminal docket and, as the victim, you have rights to be heard at sentencing."),
           ("Your own coverage still matters.", f" Many impaired drivers carry minimum limits or none. Your uninsured and underinsured motorist coverage fills the gap. {A(HUB + '/uninsured-motorist-accidents', 'UM and UIM claims')}."),
       ])
       + '<h2>Where these crashes happen</h2>'
       + '<p>Late-night crashes on I-26, on Highway 17-A between Summerville and Moncks Corner, on Dorchester Road, and on the two-lane roads out toward Ridgeville and Ladson. Goose Creek residents search for drunk-driving accident attorneys more than any other community we serve; the Highway 52 and St. James Avenue corridors produce many of them. Wrong-way crashes on I-26 are almost always impaired drivers.</p>'
       + '<h2>What to do</h2>'
       + checks([
           "Tell the officer at the scene if you smelled alcohol or saw impairment. It goes in the report and prompts testing.",
           "Get the incident number and the driver's name. We track the criminal case from the first appearance.",
           "Do not accept an early settlement offer. Insurers make them quickly in drunk-driving cases because they know what a jury will do.",
           "Tell us where the driver had been. The bar's liability depends on evidence that disappears within days: the tab, the video, the bartender's memory.",
       ])
       + '<h2>The boundary with the criminal case</h2>'
       + f'<p>This site and this firm\'s injury practice represent the people the impaired driver hurt. We do not represent the driver. The criminal case is prosecuted by the State; your civil claim is yours, it does not depend on a conviction, and it is decided on the lower civil standard of proof. If the driver is acquitted or pleads to a lesser charge, your claim continues.</p>'
       + callout("<b>Frost first:</b> the bar's surveillance video is usually overwritten within a week or two. If the driver came from a bar or restaurant, call us before that happens.")
   ),
   faqs=[
       ("Can I sue the bar that served the drunk driver in South Carolina?", "Often, yes. South Carolina recognizes claims against establishments that serve a visibly intoxicated person who then injures someone. Proving it requires evidence gathered quickly: receipts, video, witnesses."),
       ("Do I have to wait for the criminal case to finish?", "No. The civil claim proceeds on its own schedule. We often use the criminal case's evidence, and sometimes wait for a plea before mediation, but the deadline to file suit is not extended by the criminal case."),
       ("What if the drunk driver has no insurance?", "Your uninsured motorist coverage pays, and any bar liability adds to it. Punitive damages are generally not paid by UM coverage, but the compensatory claim is."),
       ("Can the family of someone killed by a drunk driver sue?", f"Yes. A wrongful death claim, brought by the estate's personal representative for the family, with punitive damages uncapped. See {A('practice-areas/wrongful-death', 'wrongful death')}."),
   ],
   sources=[("S.C. Code §§ 15-32-520 and 15-32-530 (punitive damages and exceptions to the cap)", "https://www.scstatehouse.gov/code/t15c032.php", False), ("S.C. Code § 61-4-580 (sale to intoxicated persons)", "https://www.scstatehouse.gov/code/t61c004.php", False), ("S.C. Code § 56-5-2945 (felony DUI)", "https://www.scstatehouse.gov/code/t56c005.php", False)],
   related=[HUB + "/uninsured-motorist-accidents", "practice-areas/wrongful-death", "areas/goose-creek"])

sp("practice-areas/rideshare-accidents",
   title="Summerville Uber & Lyft Accident Lawyer | Frost Law Group",
   description="Injured in an Uber or Lyft in Summerville, as a passenger, another driver or a pedestrian? Which of the rideshare company's insurance policies applies depends on what the driver's app showed. How the $1 million coverage works.",
   h1="Summerville Uber and Lyft accident lawyer", nav_label="Uber & Lyft accidents",
   summary="Which of the rideshare company's policies pays depends on what the app showed. How the $1 million coverage works.",
   lead="A rideshare crash is an ordinary crash with an unusual insurance question. The answer depends on the driver's app.",
   eyebrow="Car accidents · Summerville, SC",
   body=(
       answer(f"If you were hurt in a crash involving an Uber or Lyft driver in South Carolina, the coverage depends on the driver's status at the moment of the crash. During a ride or on the way to pick up a passenger, the rideshare company must provide at least $1,000,000 in liability coverage ({cite('tnc')}). When the driver was logged in but waiting for a request, lower company-provided limits apply. When the app was off, only the driver's personal policy applies, and many personal policies exclude rideshare driving. Passengers, other drivers and pedestrians are all covered under these rules.")
       + '<h2>The three periods</h2>'
       + table(["Driver's app status", "Coverage that applies", "Typical limits"], [
           ["App off", "Driver's personal auto policy only (often with a rideshare exclusion)", "Whatever the driver bought; possibly the 25/50/25 minimum, possibly nothing that applies"],
           ["App on, waiting for a request", "Rideshare company's contingent coverage", "$50,000 per person / $100,000 per crash bodily injury, $50,000 property damage"],
           ["En route to a pickup, or passenger in the car", "Rideshare company's primary policy", "At least $1,000,000 combined, plus uninsured/underinsured coverage"],
       ])
       + '<p>These are the minimums South Carolina\'s Transportation Network Company Act requires. Uber and Lyft both carry the $1,000,000 policy through large commercial insurers, and both also provide uninsured/underinsured motorist coverage for passengers during a ride, which matters when the other driver, not the rideshare driver, caused the crash.</p>'
       + '<h2>Who can claim</h2>'
       + checks([
           "<b>Passengers</b> in the Uber or Lyft, regardless of which driver was at fault.",
           "<b>Occupants of the other vehicle</b> when the rideshare driver caused the crash.",
           "<b>Pedestrians and cyclists</b> struck by a rideshare driver.",
           "<b>The rideshare driver</b>, when another driver caused the crash (against that driver, and under the company's UM/UIM coverage during a ride).",
       ])
       + '<h2>Why the app data matters</h2>'
       + '<p>The whole claim turns on a timestamp. Uber and Lyft keep the trip log, the driver\'s status changes, GPS and speed. They do not volunteer it. We send a preservation demand to the company on day one, obtain the trip receipt from the passenger\'s app, and, when necessary, subpoena the records. A driver who says the app was off is usually contradicted by the log.</p>'
       + '<h2>Summerville, Nexton and the airport corridor</h2>'
       + '<p>Rideshare trips here run between Summerville and Nexton, downtown Charleston, Charleston International Airport, and the North Charleston hotels along I-26 and International Boulevard. Late-night trips from downtown up I-26 and the airport corridor along Dorchester Road and I-526 produce the crashes we see most.</p>'
       + callout("<b>Frost first:</b> if you were a passenger, screenshot the trip in your app before it disappears from the recent list, including the driver's name and the route. It is the fastest proof of the coverage period.")
   ),
   faqs=[
       ("Does Uber's or Lyft's insurance cover passengers?", "Yes. During a ride, the company's $1,000,000 liability policy covers passengers, and its uninsured/underinsured coverage protects passengers when another driver was at fault."),
       ("Can I sue Uber or Lyft directly?", "The companies classify drivers as independent contractors and resist direct liability, but the insurance they are required to carry applies regardless. In some cases, such as negligent screening of a driver, a direct claim is possible."),
       ("What if the rideshare driver's app was off?", "Then it is an ordinary crash against the driver's personal policy, and your own UM/UIM coverage may matter. The driver's word about the app is checked against the company's log."),
       ("I drive for Uber and was hit by another driver. What now?", "You claim against the at-fault driver like anyone else, and if you were on a ride, the rideshare company's UM/UIM coverage applies. Injured delivery and gig drivers also have workers' compensation questions we can answer."),
   ],
   sources=[("S.C. Code Title 58, Chapter 23, Article 16 (Transportation Network Company Act)", "https://www.scstatehouse.gov/code/t58c023.php", False)],
   related=[HUB + "/delivery-driver-accidents", HUB + "/uninsured-motorist-accidents", "areas/north-charleston"])

sp(HUB + "/delivery-driver-accidents",
   title="Delivery Driver Accidents in Summerville, SC | Amazon, FedEx, UPS & Gig Drivers",
   description="Hit by an Amazon, FedEx, UPS or food-delivery driver in Summerville? Which company's insurance applies, why the contractor question matters, and what injured delivery drivers themselves can claim.",
   h1="Delivery driver accidents: hit by a delivery van, or hurt while delivering",
   summary="Which company's insurance applies when a delivery driver causes a crash, and what injured delivery drivers can claim.",
   lead="Summerville's subdivisions are full of delivery vans from morning to night. When one causes a crash, the question is whose insurance, and the answer is rarely simple.",
   body=(
       answer("If a delivery driver caused your crash, the responsible insurer depends on who the driver worked for and how. Employees of UPS, FedEx Express and the U.S. Postal Service are covered by their employer's commercial policy. Amazon deliveries are usually made by separate contractor companies (delivery service partners) with their own commercial policies, plus Amazon's coverage in some circumstances. Food and gig delivery drivers (DoorDash, Uber Eats, Instacart) are covered by the platform's policy only while on an active delivery, and otherwise by their own personal policy. Injured delivery drivers themselves may have both a workers' compensation claim and a claim against the at-fault driver.")
       + '<h2>Who was driving, and for whom</h2>'
       + table(["Vehicle", "Who the driver usually works for", "Where the coverage usually is"], [
           ["Brown UPS truck", "UPS employee", "UPS's commercial fleet policy; large limits"],
           ["FedEx Express (white, purple/orange)", "FedEx employee", "FedEx's commercial policy"],
           ["FedEx Ground", "Independent contractor company", "The contractor's commercial policy, with FedEx Ground sometimes reachable"],
           ["Amazon-branded van", "A delivery service partner (a separate company), or an Amazon Flex driver in a personal car", "The partner's commercial policy; Amazon's policy for Flex drivers on a delivery block"],
           ["USPS vehicle", "Federal employee", "Claim against the United States under the Federal Tort Claims Act, with its own two-year administrative claim rule"],
           ["Food delivery in a personal car", "Gig contractor for DoorDash, Uber Eats, Grubhub, Instacart", "Platform policy during an active delivery; personal policy otherwise, often with a delivery exclusion"],
       ])
       + '<h2>Why it matters</h2>'
       + '<p>A minimum-limits personal policy pays $25,000. A commercial fleet policy may pay $1,000,000 or more. The difference between the two is whether the driver was an employee acting within the scope of employment, a contractor, or off the clock, and companies structure their delivery operations specifically to keep liability at arm\'s length. Identifying the right defendant, and the right policy, is most of the work in these cases, and it starts with the collision report, the vehicle\'s registration and the driver\'s statement at the scene.</p>'
       + '<h2>Evidence delivery companies keep</h2>'
       + checks([
           "Route and stop logs with GPS and timestamps.",
           "In-vehicle cameras. Many Amazon delivery vans carry driver-facing and road-facing cameras that record the seconds before a crash.",
           "Delivery-app data showing whether the driver was on an active delivery.",
           "Driver qualification and training files, and prior complaints.",
       ])
       + '<p>All of it is on a retention schedule. Preservation letters go out in the first week.</p>'
       + '<h2>Injured while delivering</h2>'
       + f'<p>Search data shows Summerville delivery drivers looking for help after their own crashes and injuries. If you were hit while working, you may have two claims: workers\' compensation from your employer (if you are an employee), which pays medical care and part of your wages regardless of fault, and a third-party injury claim against the driver who hit you. Gig contractors are generally not covered by workers\' compensation, but platform accident policies and your own UM/UIM coverage may apply. See {A("practice-areas/workers-compensation", "workers’ compensation")}.</p>'
       + callout("<b>Frost first:</b> get a photo of the van's DOT number or company markings and the driver's name before they leave. It is the fastest way to find the right insurer.")
   ),
   faqs=[
       ("Can I sue Amazon if an Amazon van hit me?", "Usually the claim is against the delivery service partner that employed the driver and its commercial insurer. Whether Amazon itself is reachable depends on the facts and how much control it exercised. We evaluate both."),
       ("What if a food delivery driver hit me?", "If they were on an active delivery, the platform's commercial policy applies. If they were between deliveries, their personal policy applies and may exclude delivery driving, which makes your own UM coverage important."),
       ("I am a delivery driver and was hurt on the job. Can I get workers' comp and sue the other driver?", "If you are an employee, yes to both: workers' compensation pays regardless of fault, and you can pursue the at-fault driver for what workers' comp does not cover, with reimbursement rules between the two."),
       ("A postal truck hit me. Is that different?", "Yes. Claims against the U.S. Postal Service go through the Federal Tort Claims Act: an administrative claim must be filed with the agency within two years before any lawsuit."),
   ],
   sources=[("Federal Motor Carrier Safety Administration (commercial vehicle rules)", "https://www.fmcsa.dot.gov/", False)],
   related=["practice-areas/rideshare-accidents", "practice-areas/truck-accidents", "practice-areas/workers-compensation"])

sp(HUB + "/auto-injury-assessment-after-a-crash",
   title="Auto Injury Assessment in Summerville, SC | Getting Evaluated After a Crash",
   description="Where to get evaluated after a car accident in Summerville, what to tell the provider, why same-day care protects your health and your claim, and how the bills get paid while the claim is open.",
   h1="Getting your injuries evaluated after a crash in Summerville",
   summary="Where to get checked, what to tell the provider, and how the bills get paid while the claim is open.",
   lead="The most common search that brings people to this site is “auto injury assessment Summerville.” Here is the practical answer.",
   body=(
       answer("Get evaluated the same day as the crash, even if you feel fine: the emergency department at Summerville Medical Center or Trident Medical Center for anything serious, an urgent care or your own doctor for the rest. Tell the provider it was a car accident and describe every symptom. Follow the treatment plan without gaps. Your health insurance, your auto policy's medical-payments coverage, or a provider who agrees to wait for settlement pays the bills now; the at-fault driver's insurer reimburses when the claim resolves.")
       + '<h2>Why same-day matters</h2>'
       + '<p>Adrenaline masks pain. Concussions, whiplash, disc injuries, internal bleeding and fractures of small bones routinely show up a day or more later. A same-day evaluation protects your health first. It also creates the record that connects the injury to the crash; the longer the gap between the collision and the first medical visit, the more room the insurer has to argue that something else caused the injury.</p>'
       + '<h2>Where to go in and around Summerville</h2>'
       + checks([
           "<b>Emergency:</b> Summerville Medical Center on Midland Parkway, Trident Medical Center in North Charleston (the closest Level II trauma center) and Roper St. Francis Berkeley Hospital off Highway 17-A near Nexton. Serious trauma from I-26 crashes often goes to MUSC in Charleston, the region's Level I trauma center.",
           "<b>Urgent care:</b> for soreness, minor cuts and “I think I'm fine but want to be checked.” Ask for imaging if you have neck or back pain.",
           "<b>Your primary care doctor:</b> for follow-up, referrals to orthopedics, neurology or physical therapy, and documentation of how the injury affects your daily life.",
           "<b>Specialists:</b> orthopedic, spine, neurology, pain management and physical therapy. Chiropractic care is common and covered; keep a medical doctor involved for serious injuries.",
       ])
       + '<h2>What to tell the provider</h2>'
       + steps([
           ("That it was a motor vehicle collision, with the date.", " It changes the questions they ask and the tests they order, and it is how the record ties the injury to the crash."),
           ("Every symptom, not just the worst one.", " Headache, dizziness, ringing in the ears, numbness, sleep problems, anxiety about driving. Symptoms that are not in the first chart are later called “new.”"),
           ("Your honest pain level and what you cannot do.", " Lifting, sitting, sleeping, working. The chart becomes the evidence of how the injury affected your life."),
           ("Prior injuries, honestly.", " An old back problem does not defeat a claim; hiding it does. South Carolina law lets you recover for the aggravation of a pre-existing condition."),
       ])
       + '<h2>How the bills get paid while the claim is open</h2>'
       + checks([
           "<b>Health insurance</b> pays as it normally would. Your insurer has a right to be reimbursed from the settlement, which we negotiate down.",
           "<b>Medical-payments (MedPay) coverage</b> on your own auto policy pays bills quickly regardless of fault, if you bought it. Check your declarations page.",
           "<b>Letters of protection.</b> Some providers treat now and agree to be paid from the settlement. Useful when there is no health insurance; we manage the balances.",
           "<b>The at-fault insurer does not pay as you go.</b> It pays once, at the end. Anyone who tells you otherwise is describing a different state.",
       ])
       + '<h2>Gaps and “independent” exams</h2>'
       + '<p>Two things damage claims more than any others: gaps in treatment (the insurer argues you got better), and skipping the specialist referral (the insurer argues it was not serious). Later, the at-fault insurer may demand a so-called independent medical examination by a doctor it pays. We prepare clients for those and, when necessary, obtain our own expert opinions.</p>'
       + callout("<b>Frost first:</b> go to the doctor before you go to the body shop. The car will wait; the record will not.")
   ),
   faqs=[
       ("Should I go to the ER or urgent care after a car accident?", "The ER for head injury, chest or abdominal pain, numbness, severe pain or any loss of consciousness. Urgent care or your doctor for soreness and minor injuries, with imaging if you have neck or back pain. When in doubt, the ER."),
       ("Who pays my medical bills after a car accident in South Carolina?", "Your health insurance or MedPay coverage pays now; the at-fault driver's insurer reimburses at settlement. If you have neither, some providers will treat under a letter of protection."),
       ("Will the insurance company pay for a chiropractor?", "Chiropractic care is compensable, and common for soft-tissue injuries. For serious injuries, keep a medical doctor involved and follow referrals to specialists."),
       ("What if I have a pre-existing condition?", "You can recover for the extent to which the crash aggravated it. Tell your providers about it; the insurer will find it anyway, and honesty preserves your credibility."),
   ],
   related=[HUB + "/what-to-do-after-a-car-accident-in-south-carolina", "practice-areas/catastrophic-injuries", HUB + "/should-i-talk-to-the-other-drivers-insurance-company"])

sp(HUB + "/where-crashes-happen-in-summerville",
   title="Where Car Accidents Happen in Summerville, SC | I-26, Highway 17-A, Dorchester Road",
   description="The Summerville-area roads and intersections where crashes cluster, who investigates each, and what the location means for your claim: I-26, Highway 17-A, Dorchester Road, Bacons Bridge Road, Ladson Road and more.",
   h1="Where crashes happen in Summerville, and what the location means for your claim",
   summary="I-26, Highway 17-A, Dorchester Road, Bacons Bridge Road and the intersections where crashes cluster, with who investigates each.",
   lead="Every road in this town has a crash pattern, an investigating agency and a set of cameras. Knowing them is part of building the case.",
   body=(
       answer("Summerville's crashes cluster on I-26 between exits 194 and 205, along North Main Street and Highway 17-A through Nexton, on Dorchester Road from the Oakbrook shopping centers to Old Trolley Road, at the Bacons Bridge Road and Berlin G. Myers Parkway intersections, and along Ladson Road and College Park Road toward the interstate. Where the crash happened decides which agency wrote the report (Summerville Police inside town, the Highway Patrol on the interstate, a county sheriff elsewhere), which cameras may have recorded it, and which county's court hears the case.")
       + '<h2>The corridors</h2>'
       + '<h3>I-26 (exits 194 to 205)</h3>'
       + '<p>The interstate through Summerville, Ladson and toward North Charleston is the region\'s worst stretch for serious crashes: high speeds, heavy truck traffic from the port, weaving at the 17-A (exit 199) and College Park Road (exit 203) interchanges, and sudden stops when traffic backs up. Wrong-way crashes late at night are almost always impaired drivers. The Highway Patrol investigates; SCDOT traffic cameras cover much of it. Because I-26 through Summerville runs along the Dorchester and Berkeley County line, the exact location decides which county\'s court hears the case.</p>'
       + '<h3>North Main Street and Highway 17-A</h3>'
       + '<p>From downtown through the Nexton and Cane Bay growth north of the interstate, 17-A carries far more traffic than it was built for. Rear-end collisions in stop-and-go traffic, left turns across traffic at the shopping-center entrances and the Nexton Parkway signals, and speed on the open stretches toward Moncks Corner. Summerville Police inside the town limits; Berkeley County Sheriff\'s Office or Highway Patrol beyond them.</p>'
       + '<h3>Dorchester Road (SC-642)</h3>'
       + '<p>The Oakbrook area, the Dorchester Road and Old Trolley Road intersection, the retail strips toward Ladson Road, and the long stretch to North Charleston. Rear-end crashes, distracted drivers pulling out of parking lots, and pedestrians crossing outside crosswalks at night.</p>'
       + '<h3>Bacons Bridge Road, Berlin G. Myers Parkway and Old Trolley Road</h3>'
       + '<p>The south side of town: the parkway\'s intersections with Bacons Bridge Road and Central Avenue, the Old Trolley Road curve, and the two-lane roads toward Ashley River Road. Speed and failure to yield at the intersections; motorcycle crashes on the curves.</p>'
       + '<h3>Ladson Road, College Park Road and US-78</h3>'
       + '<p>The Ladson corridor where three counties meet: the College Park Road interchange, the US-78 and Ladson Road crossroads near the fairgrounds, and the truck traffic between the Palmetto Commerce Parkway warehouses and the interstate. County sheriffs (Dorchester, Berkeley or Charleston depending on the exact spot) or Highway Patrol investigate.</p>'
       + '<h3>The two-lane roads</h3>'
       + '<p>Highway 78 toward Ridgeville and St. George, Orangeburg Road, Central Avenue past the town limits, and Highway 61. Single-vehicle and head-on crashes at speed, often at night, often with impairment.</p>'
       + '<h2>Is there a crash on I-26 right now?</h2>'
       + f'<p>For live conditions, closures and the reason traffic is stopped on I-26, I-526 or I-95, use {link("sc511", "SCDOT’s 511 map")}. It shows incidents as the Highway Patrol reports them and is the fastest way to know whether to take Highway 78 or 17-A instead. If you were in the crash it is showing, the Highway Patrol has the report; {A(HUB + "/how-to-get-your-south-carolina-accident-report", "here is how to get it")}.</p>'
       + '<h2>Why location matters to the claim</h2>'
       + checks([
           "<b>Who investigated.</b> The Summerville Police Department, the Dorchester or Berkeley County Sheriff's Office, or the Highway Patrol. Each keeps reports, body-camera video and 911 audio differently, and we know whom to ask.",
           "<b>Which cameras.</b> SCDOT cameras on the interstate, town traffic cameras at major signals, and the private cameras at gas stations, restaurants and stores. All are overwritten on short schedules.",
           "<b>Which county, which court.</b> A lawsuit is filed in the Court of Common Pleas of the county where the crash happened: Dorchester County in St. George, Berkeley County in Moncks Corner, Charleston County in downtown Charleston.",
           "<b>Whether a government entity is involved.</b> A road defect, a missing sign, a malfunctioning signal or a town vehicle brings in the Tort Claims Act, with its two-year deadline and damage caps.",
       ])
       + f'<p>The community pages cover the same ground for {A("areas/goose-creek", "Goose Creek")}, {A("areas/ladson", "Ladson")}, {A("areas/north-charleston", "North Charleston")} and the rest of the Lowcountry.</p>'
       + callout("<b>Frost first:</b> if you tell us the intersection, we can usually tell you within a day which cameras may exist and which agency has the report. Call before the footage is gone.")
   ),
   faqs=[
       ("Who investigates a crash on I-26 near Summerville?", "The South Carolina Highway Patrol. Its collision reports are obtained through the SCDMV, and its dash-camera and body-camera video through the Department of Public Safety."),
       ("Which court hears a car accident case from Summerville?", "The Court of Common Pleas of the county where the crash happened: Dorchester County (St. George) for most of Summerville, Berkeley County (Moncks Corner) for Nexton, Cane Bay and the area north of the interstate, Charleston County for the Ladson edge."),
       ("Are there traffic cameras in Summerville that record crashes?", "SCDOT cameras on I-26 stream but generally do not record. Town signal cameras vary. The most useful footage usually comes from businesses near the intersection, which is why we send requests within days."),
   ],
   sources=[("SC Department of Public Safety – traffic collision statistics", "https://scdps.sc.gov/ohsjp/stats", False), ("South Carolina Department of Transportation", "https://www.scdot.org/", False)],
   related=[HUB + "/what-to-do-after-a-car-accident-in-south-carolina", "practice-areas/truck-accidents", "areas/summerville"])
