"""Title tags and meta descriptions for the site pages that are not LLG long-form pages.

LLG pages carry their own title and description in content/pages/pages.json (Page Manifest v7). This file covers the
team, contact, review, blog and legal pages, and the blog posts. Titles stay at or under 60 characters and
descriptions between 150 and 156, each with a call to action and no phone number (LLG Part 4).
Applied by base.page(), which lets these override the values typed in the content modules.
"""
META = {
    "about": ("Our Team | Meet Tara and Jack Frost in Summerville",
              "Meet Tara L. Frost and Jack C. Frost, the husband and wife attorneys of Frost Law Group in Summerville, South Carolina. Call to set up a free consultation."),
    "attorneys/tara-frost": ("Tara L. Frost | Summerville Personal Injury Attorney",
                             "Tara L. Frost is a former Dorchester County Magistrate Judge who focuses on personal injury claims at Frost Law Group in Summerville. Call to talk with her."),
    "attorneys/jack-frost": ("Jack C. Frost | Attorney at Frost Law Group",
                             "Jack C. Frost spent fourteen years with the Summerville Police Department and Charleston County Sheriff's Office before law. Call Frost Law Group to talk."),
    "contact": ("Contact Frost Law Group | Free Consultation",
                "Contact Frost Law Group at 128 Linwood Lane in Summerville, South Carolina, for a free and confidential injury consultation. Call or send a message today."),
    "reviews": ("Client Reviews | Frost Law Group in Summerville",
                "Read what clients say about working with Tara and Jack Frost at Frost Law Group in Summerville, South Carolina, and learn how to leave a review on Google."),
    "blog": ("Injury Law Blog | Frost Law Group in Summerville",
             "Frost Law Group explains what Lowcountry news means for a crash claim, a dog bite case or an insurance dispute in South Carolina. Read the latest articles."),
    "privacy-policy": ("Privacy Policy | Frost Law Group Injury Practice",
                       "How summervilleaccidentattorney.com handles the information you share through its contact form, the map and server logs. Read the full privacy policy here."),
    "terms-of-use": ("Terms of Use and Legal Disclaimer | Frost Law Group",
                     "The terms for using summervilleaccidentattorney.com, including the attorney advertising notice and the fee disclosure. Read them before you contact us."),
    "accessibility": ("Accessibility Statement | Frost Law Group",
                      "How summervilleaccidentattorney.com and the Frost Law Group office in Summerville work to be usable by everyone, and how to tell the firm about a problem."),
    "thank-you": ("Thank You | Frost Law Group",
                  "We received your message, and an attorney at Frost Law Group will get back to you. For anything urgent, call the office in Summerville, South Carolina."),
    # blog posts (the four articles from the first build, corrected in the Manifest v7 fix pass)
    "crash-on-i-26-near-summerville-who-writes-the-report-and-how-to-get-it": ("Crash on I-26 Near Summerville | How to Get the Report",
        "After a crash on I-26 near Summerville, the Highway Patrol usually writes the report. Learn what the FR-10 is and how to request your crash report today."),
    "a-dog-bite-in-a-summerville-neighborhood-what-parents-should-know": ("Dog Bite in a Summerville Neighborhood | Read First",
        "A neighbor's dog bit your child in Summerville. Learn what South Carolina's dog bite law says, who usually pays and the steps to take first. Read the guide."),
    "motorcycle-season-in-the-lowcountry-the-helmet-question-and-your-claim": ("SC Helmet Law and Your Motorcycle Claim | Read This",
        "Riders 21 and over may ride without a helmet in South Carolina. Learn what that means for an injury claim after a crash near Summerville. Read the article."),
    "hit-by-an-uninsured-driver-in-goose-creek-your-own-policy-may-be-the-answer": ("Hit by an Uninsured Driver in Goose Creek | Get Help Today",
        "Hit by a driver with no insurance in Goose Creek? Learn how the uninsured motorist coverage on your own South Carolina policy can help pay. Call us today."),
    # blog posts, October 2026 batch (metadata from the end of each Legal Leads Group draft; the Moncks Corner draft offered
    # ten options and this uses option 1 of each list)
    "how-does-a-summerville-car-accident-lawyer-get-your-medical-bills-paid": ("Summerville Car Accident Lawyer for Medical Bills | Call Now",
        "South Carolina has no required PIP. Learn how a Summerville car accident lawyer lines up Med Pay, health insurance, and UM coverage. Get a free review."),
    "what-can-a-goose-creek-motorcycle-accident-lawyer-do-if-you-were-partly-at-fault": ("Goose Creek Motorcycle Accident Lawyer | Call Today",
        "South Carolina requires a helmet only under 21. A Goose Creek motorcycle accident lawyer answers the helmet argument insurers use. Call for a free review."),
    "who-can-a-moncks-corner-slip-and-fall-lawyer-hold-liable-for-your-fall": ("Moncks Corner Slip and Fall Lawyer | Find Who Is Liable",
        "A Moncks Corner slip and fall lawyer explains who is liable for your fall, whether a store, a landlord, or a town. Call Frost Law Group for a free review."),
    "how-does-a-north-charleston-truck-accident-lawyer-figure-out-what-your-claim-is-worth": ("North Charleston Truck Accident Lawyer | Value Your Claim",
        "A North Charleston truck accident lawyer values your claim by adding up your losses and checking each company's insurance and fault. Get a free review."),
    # October 12, 2026 post. The description is the draft's own. The draft's title, "IME Order? See a Charleston
    # Catastrophic Injury Lawyer", stays in posts.py; this one follows the keyphrase | CTA rule.
    "can-a-charleston-catastrophic-injury-lawyer-keep-you-away-from-the-insurance-companys-doctor": ("Charleston Catastrophic Injury Lawyer | Call Before an IME",
        "Before a lawsuit, the other driver's insurer cannot order an IME. A Charleston catastrophic injury lawyer explains when a judge can. Call for a free review."),
    # October 20, 2026 post. Daylin asked for the draft's own title and description, so the title is not in the
    # keyphrase | CTA form.
    "can-a-ladson-slip-and-fall-lawyer-bring-a-claim-against-a-church-or-charity": ("Hurt at a Church Event? Call a Ladson Slip and Fall Lawyer",
        "Churches and charities can be sued for a fall in South Carolina, but a cap may apply. A Ladson slip and fall lawyer explains it. Call for a free review."),
}
