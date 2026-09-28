"""Title tags and meta descriptions for the site pages that are not LLG long-form pages.

LLG pages carry their own title and description in content/pages/pages.json (Page Manifest v7). This file covers the
team, contact, review, blog and legal pages, and the four blog posts. Titles stay at or under 60 characters and
descriptions between 150 and 156, each with a call to action and no phone number (LLG Part 4).
Applied by base.page(), which lets these override the values typed in the content modules.
"""
META = {
    "about": ("Our Team | Tara and Jack Frost | Frost Law Group",
              "Meet Tara L. Frost and Jack C. Frost, the husband and wife attorneys of Frost Law Group in Summerville, South Carolina. Call to schedule a free consultation."),
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
                     "The terms for using summervilleaccidentattorney.com, including the attorney advertising notice and the fee and cost disclosure. Read them before you contact us."),
    "accessibility": ("Accessibility Statement | Frost Law Group",
                      "How summervilleaccidentattorney.com and the Frost Law Group office in Summerville work to be usable by everyone, and how to report a problem to the firm today."),
    "thank-you": ("Thank You | Frost Law Group",
                  "We received your message, and an attorney at Frost Law Group will get back to you. For anything urgent, call the office in Summerville, South Carolina."),
    # blog posts (the four articles from the first build, corrected in the Manifest v7 fix pass)
    "blog/i-26-crash-summerville-who-writes-the-report": ("Crash on I-26 Near Summerville? Get the Report",
        "After a crash on I-26 near Summerville, the Highway Patrol usually writes the report. Learn what the FR-10 is and how to request your collision report today."),
    "blog/dog-bite-summerville-neighborhood-what-parents-should-know": ("Dog Bite in a Summerville Neighborhood | Read First",
        "A neighbor's dog bit your child in Summerville. Learn what South Carolina's dog bite law says, who usually pays, and the steps to take first. Read the guide."),
    "blog/motorcycle-season-lowcountry-helmet-law-your-claim": ("SC Helmet Law and Your Motorcycle Claim | Read This",
        "Riders 21 and over may ride without a helmet in South Carolina. Learn what that can mean for an injury claim after a crash near Summerville. Read the article."),
    "blog/hit-by-an-uninsured-driver-goose-creek-your-own-policy": ("Hit by an Uninsured Driver in Goose Creek? Read This",
        "Hit by a driver with no insurance in Goose Creek? Learn how South Carolina uninsured motorist coverage on your own policy can pay. Read the article and call us."),
}
