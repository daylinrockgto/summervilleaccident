"""Core pages: home, practice-area index, areas index, team, attorney bios, contact, reviews, blog index, legal pages, thank-you."""
from .base import page, A, ext, img, p, ul, checks, steps, callout, section, band, esc, twocol, answer
from . import firm
from . import local
from .local import cite, link

PH = firm.PHONE
TEL = f'<a href="tel:{firm.PHONE_E164}">{PH}</a>'
CAR = firm.CAR


def practice_cards():
    icons = {
        "practice-areas/car-accidents": '<path d="M3 13l2-5h14l2 5v6H3z"/><circle cx="7.5" cy="16.5" r="1.5"/><circle cx="16.5" cy="16.5" r="1.5"/>',
        "practice-areas/truck-accidents": '<path d="M2 7h11v10H2zM13 10h5l3 3v4h-8z"/><circle cx="6" cy="18" r="1.6"/><circle cx="17" cy="18" r="1.6"/>',
        "practice-areas/motorcycle-accidents": '<circle cx="5.5" cy="16.5" r="3"/><circle cx="18.5" cy="16.5" r="3"/><path d="M5.5 16.5 9 9h4l3 5h2.5M9 9l-2-3h3"/>',
        "practice-areas/pedestrian-accidents": '<circle cx="12" cy="4.5" r="1.8"/><path d="M12 7v5l-3 7M12 12l3 3v5M9 10l3-3 3 2 2 3"/>',
        "practice-areas/dog-bites": '<path d="M4 10c0-3 2-5 5-5h6c3 0 5 2 5 5v3c0 3-2 5-5 5H9c-3 0-5-2-5-5z"/><path d="M8 5 6 2M16 5l2-3M9 12h.01M15 12h.01M10 15h4"/>',
        "practice-areas/slip-and-fall": '<path d="M3 20h18M6 20l4-9 4 3 3-6"/><circle cx="17.5" cy="5.5" r="1.8"/>',
        "practice-areas/workers-compensation": '<path d="M4 8h16v12H4zM9 8V5h6v3"/><path d="M12 11v5M9.5 13.5h5"/>',
        "practice-areas/catastrophic-injuries": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="M12 8v5M12 16h.01"/>',
        "practice-areas/wrongful-death": '<path d="M12 3v18M6 9h12"/><path d="M4 21h16"/>',
        "practice-areas/rideshare-accidents": '<path d="M3 13l2-5h14l2 5v6H3z"/><path d="M8 5h8M12 3v2"/><circle cx="7.5" cy="16.5" r="1.5"/><circle cx="16.5" cy="16.5" r="1.5"/>',
        "practice-areas/drunk-driving-accidents": '<path d="M7 3h10l-1 7c-.4 2-2 3-4 3s-3.6-1-4-3zM12 13v6M8 21h8"/>',
    }
    from .base import BY_SLUG
    out = ['<ul class="cards">']
    for s in firm.HUBS + ["practice-areas/rideshare-accidents", "practice-areas/drunk-driving-accidents"]:
        pg = BY_SLUG.get(s)
        if not pg:
            continue
        out.append(f'<li class="card"><div class="icon"><svg viewBox="0 0 24 24">{icons.get(s, "")}</svg></div><h3><a href="[[{s}]]">{esc(pg["nav_label"])}</a></h3><p>{pg["summary"]}</p><a class="more" href="[[{s}]]">{esc(pg["nav_label"])}</a></li>')
    out.append("</ul>")
    return "".join(out)


# Home, /practice-areas/ and /locations/ are LLG pages in content/pages (Manifest v7).

# ----------------------------------------------------------------------------- ABOUT / TEAM
about_body = (
    '<h2>A husband-and-wife law firm in Summerville</h2>'
    '<p>Frost Law Group is built on a simple idea: people in a crisis should be able to talk to the lawyer, not a call center. Jack and Tara Frost are married, were Summerville High School sweethearts, and share an office on Linwood Lane with their paralegal, Cassie, and two Golden Retrievers who greet clients at the door.</p>'
    '<p>This site is the firm\'s personal injury practice. Tara L. Frost focuses on personal injury, car accident and truck accident claims, and she is a former Dorchester County Magistrate Judge and Associate Probate Judge. Jack C. Frost spent fourteen years with the Summerville Police Department and the Charleston County Sheriff\'s Office before he practiced law, so he knows how a collision report is put together.</p>'
    '[[team]]'
    '<h2>How we work</h2>'
    + checks([
        "Your consultation is free, and injury cases are handled on a contingency fee: no fee unless we win.",
        "You meet with an attorney, not an intake service.",
                "We say when you do not need a lawyer. A minor property-damage claim with no injury is usually something you can handle yourself, and we will tell you how.",
        "If you cannot travel after an injury, call and tell us. We will talk through how to meet.",
            ]) +
    '<h2>One firm, two websites</h2>'
    f'<p>Frost Law Group, LLC is one South Carolina firm at 128 Linwood Lane in Summerville. This site covers personal injury. {firm.CROSS_LINK_TEXT}, {ext(firm.MAIN_SITE + "/", firm.MAIN_SITE_LABEL)}. Same office, same attorneys, same phone number. We are not affiliated with other firms that use the Frost name in other states.</p>'
    f'<p>{img("office-exterior.jpg", "Frost Law Group’s office on Linwood Lane in Summerville")}</p>'
    '<h2>Our comfort dogs</h2>'
    '<p>Mistoc and Palmer are Golden Retrievers with a talent for finding the most nervous person in the room. Tell us when you book if you would rather they stay in the back.</p>'
    + band("Ready to talk to an attorney?", "Your consultation is free, confidential, and carries no obligation.")
)
page("about", kind="page", hub=None,
     title="Our Attorneys | Jack & Tara Frost | Summerville Accident Attorneys",
     description="Meet Tara Frost, a former Dorchester County magistrate judge who leads Frost Law Group's injury practice, and Jack Frost, a former detective who runs the investigation. Summerville, SC.",
     h1="Our Team", eyebrow="Get to know Frost Law Group", nav_label="Our team", hero_image="client-meeting.jpg", hero_caption="Tara and Jack with a client at the office",
     lead="A former judge, a former detective, a paralegal who keeps every file moving, and two Golden Retrievers. This is who answers when you call.",
     body=about_body, priority=0.8)

# ----------------------------------------------------------------------------- ATTORNEYS
tara_body = (
    '<h2>From the bench to your side of the table</h2>'
    '<p>Tara L. Frost is a Summerville personal injury attorney who represents injured clients and families across Summerville and the surrounding counties. She focuses on personal injury, car accident and truck accident claims, and she handles motorcycle, rideshare and pedestrian crashes, dog bites, falls and wrongful death cases.</p>'
    '<p>Tara believes that effective representation starts with listening. Her personal motto, “Don\'t mistake my kindness for weakness,” describes how she approaches every case. She treats clients with compassion, respect and honesty, and she stands firm when an insurance company or opposing party refuses to do what is right. After a serious accident, clients are often overwhelmed, in pain and unsure what to do next; her job is to make the process clear and manageable and to pursue a fair result on the evidence.</p>'
    '<h2>Judicial service</h2>'
    '<p>Tara served as a Dorchester County Magistrate Judge from July 2022 through August 2025, and then as a Dorchester County Associate Probate Judge from August 2025 through June 2026. Magistrate court is where South Carolina\'s smaller civil claims are tried, and where evidence, credibility and preparation decide cases every week. That service gave her a courtroom perspective on how evidence, preparation and credibility are weighed, and on why the details in a medical record or a collision report matter.</p>'
    '<p>Tara no longer serves on the bench and does not appear in matters she handled as a judge.</p>'
    '<h2>Before the law</h2>'
    '<p>Before becoming an attorney, Tara spent roughly sixteen years in the hospitality industry and later owned a window-covering company with her father. Those years taught her customer service, communication, and how to understand what people need during difficult and stressful times. She brings that same client-centered mindset to every injury claim.</p>'
    '<h2>Education and credentials</h2>'
    + ul([
        "Juris Doctor, Charleston School of Law; Vice President of the Student Trial Lawyers Association; helped institute the Trial Advocacy Board",
        "Dorchester County Associate Probate Judge, August 2025 – June 2026",
        "Dorchester County Magistrate Judge, July 2022 – August 2025",
    ]) +
    '<h2>Rooted here</h2>'
    '<p>A lifelong resident of the tri-county area, Tara is married to her Summerville High School sweetheart, Jack, and the two practice together in Summerville.</p>'
    '<h2>Articles</h2><p>The firm\'s articles on <a href="[[blog]]">the blog</a> cover what to do in the first days after a crash, what South Carolina\'s dog bite and helmet laws mean for a claim, and what to know before you talk to an insurance adjuster.</p>'
    '<h2>Reach Tara</h2>'
    f'<p>Email <a href="mailto:{firm.ATTORNEYS["tara"]["email"]}">{firm.ATTORNEYS["tara"]["email"]}</a>, call {TEL}, or connect on {ext(firm.ATTORNEYS["tara"]["linkedin"], "LinkedIn")}. Tara\'s work on the firm\'s other matters is described on {ext(firm.ATTORNEYS["tara"]["main_site_bio"], "her profile on the main firm site")}.</p>'
    + band("Injured? Talk to Tara first.", "A free, honest conversation about whether you have a claim and what it may be worth.")
)
page("attorneys/tara-frost", kind="attorney", author="tara", hub="about",
     title="Tara L. Frost | Summerville Personal Injury Attorney | Former Magistrate Judge",
     description="Tara L. Frost leads Frost Law Group's personal injury practice in Summerville, SC. She served as a Dorchester County Magistrate Judge (2022–2025) and Associate Probate Judge (2025–2026).",
     h1="Tara L. Frost", eyebrow="Attorney at Law · Personal injury", nav_label="Tara L. Frost",
     lead="A former Dorchester County Magistrate Judge and Associate Probate Judge who focuses on personal injury, car accident and truck accident claims at Frost Law Group.",
     hero_image="tara-bio.jpg", hero_caption="Tara L. Frost, Attorney at Law", body=tara_body, priority=0.8)

jack_body = (
    '<h2>Fourteen years in Lowcountry law enforcement</h2>'
    '<p>Jack Frost was born in Virginia and moved to Summerville with his family at the age of eight. He graduated from Summerville High School and studied political science at the College of Charleston. Following in his grandfather\'s footsteps, he began a career in law enforcement with the Summerville Police Department and went on to serve as a deputy, master deputy and detective with the Charleston County Sheriff\'s Office, retiring after fourteen years.</p>'
    '<p>He served as a police officer and corporal with the Summerville Police Department and as a deputy, master deputy and detective with the Charleston County Sheriff\'s Office, where he also served on the SWAT team.</p>'
    '<h2>What that means for your injury case</h2>'
    + checks([
        "He knows how a collision report is put together, so he can read one for what it leaves out: a witness who was not interviewed, a camera that was not checked, a measurement that was not taken.",
        "He knows that some evidence does not last. Store cameras can record over old footage, and a damaged car can leave the lot before anyone downloads its data.",
    ]) +
    '<h2>Education and credentials</h2>'
    + ul([
        "Juris Doctor, Charleston School of Law",
        "Bachelor of Science in Criminal Justice and Police Administration, Strayer University",
        "Associate of Science in Criminal Justice, Trident Technical College",
        "Political science studies, College of Charleston",
        "Type 1 SWAT Operator designation, U.S. Department of Homeland Security",
    ]) +
    '<h2>Role at the firm</h2>'
    f'<p>On injury cases, Jack works alongside Tara, and his years writing and reviewing reports give the firm a practical read of the facts. The rest of Jack\'s practice is described on {ext(firm.ATTORNEYS["jack"]["main_site_bio"], "his profile on the main firm site")}.</p>'
    '<h2>Off the clock</h2>'
    '<p>Jack once caddied at the Ocean Course on Kiawah Island. He and Tara, his Summerville High School sweetheart, practice together in Summerville.</p>'
    '<h2>Reach Jack</h2>'
    f'<p>Email <a href="mailto:{firm.ATTORNEYS["jack"]["email"]}">{firm.ATTORNEYS["jack"]["email"]}</a>, call {TEL}, or connect on {ext(firm.ATTORNEYS["jack"]["linkedin"], "LinkedIn")}.</p>'
    + band("Questions about a crash report?", "If the report blames you, or leaves out what you saw, call and talk it through with an attorney.")
)
page("attorneys/jack-frost", kind="attorney", author="jack", hub="about",
     title="Jack C. Frost | Former Detective | Summerville Accident Attorneys",
     description="Jack C. Frost spent 14 years as a Summerville police officer and Charleston County Sheriff's Office detective. He now investigates crash and injury cases for Frost Law Group.",
     h1="Jack C. Frost", eyebrow="Attorney at Law", nav_label="Jack C. Frost",
     lead="A former Summerville police officer and Charleston County Sheriff's Office detective, now an attorney at Frost Law Group.",
     hero_image="jack-bio.jpg", hero_caption="Jack C. Frost, Attorney at Law", body=jack_body, priority=0.7)

# ----------------------------------------------------------------------------- CONTACT
contact_body = (
    section(
        twocol(
            '<h3 style="margin-top:0">Tell us about your case</h3><p class="small" style="margin:0 0 .8rem">Free, confidential, no obligation. An attorney will get back to you.</p>[[form]]',
            '<h3 style="margin-top:0">What to expect</h3>' + checks([
                "You talk to Tara or Jack, not an intake service.",
                "We tell you honestly whether you have a claim, what it may be worth, and what to do next, whether or not you hire us.",
                "If you hire us, you pay nothing up front and no fee unless we win.",
                "Bring or send what you have: the collision report or FR-10, photos, the other driver's insurance card, your own policy, medical paperwork and any letters from an insurer. Photos on your phone are fine.",
                "If you cannot travel after an injury, tell us, and we will talk through how to meet.",
            ]) + '<div class="alert"><p><b>Before you talk to the insurance company:</b> you are not required to give the other driver\'s insurer a recorded statement. Talk with a lawyer before you sign a medical release or accept a check.</p></div>'),
        label="Free consultation", title="Get your free case review"),
    section('[[nap]]' + f'<div class="nap"><div><h3>Email</h3><p><a href="mailto:{firm.EMAIL}">{firm.EMAIL}</a></p><p class="small">For a new matter, a call gets a faster answer.</p></div><div><h3>Mail</h3><p>{firm.NAME}<br>{firm.PO_BOX}</p><p class="small">Please send documents to the P.O. Box, and come to Linwood Lane in person.</p></div><div><h3>Attorneys</h3><p><a href="[[attorneys/tara-frost]]">Tara L. Frost</a><br><a href="[[attorneys/jack-frost]]">Jack C. Frost</a></p></div></div>' + '[[map]]', cls="tint", label="Our office", title="128 Linwood Lane, Summerville, SC 29483"),
    section(
        f'<p class="lead">{local.office_roads_sentence() or "Linwood Lane is a short residential street in Summerville; the office is the house with our sign out front."}</p>'
        + local.directions_cards(["i26-199", "goose-creek", "ladson", "north-charleston", "charleston", "mount-pleasant", "moncks-corner", "walterboro", "west-ashley", "nexton", "cane-bay", "knightsville"])
        + f'<p><a class="btn ghost sm" href="{esc(firm.DIRECTIONS_URL)}" rel="noopener" target="_blank">Open turn-by-turn directions in Google Maps</a></p>',
        label="Directions", title="Getting here on local roads", lead="Written for people who know the area by road names, not GPS pins."),
    section('[[findus]]' + f'<p>{firm.CROSS_LINK_TEXT}, {ext(firm.MAIN_SITE + "/", firm.MAIN_SITE_LABEL)}.</p>', cls="tint", label="Online", title="Find and follow Frost Law Group"),
)
page("contact", kind="page", layout="raw", cta=[("tel:" + firm.PHONE_E164, firm.PHONE, "btn"), (firm.DIRECTIONS_URL, "Get directions", "btn ghost")],
     title="Free Consultation | Summerville Accident Attorneys | (843) 419-6653",
     description="Call (843) 419-6653 for a free personal injury consultation with Frost Law Group at 128 Linwood Lane, Summerville, SC. No fee unless we win. Directions from every community we serve.",
     h1="Get Your Free Consultation", eyebrow="No fee unless we win", nav_label="Contact",
     lead="Talk to a Summerville accident attorney today. Your consultation is free, confidential and comes with no obligation. If we take your case, you pay nothing unless we win.",
     body="".join(contact_body), priority=0.9, changefreq="monthly")

# ----------------------------------------------------------------------------- REVIEWS
reviews_body = (
    f'<p class="lead">Frost Law Group is rated {firm.RATING} stars on Google. We are a two-attorney firm, so every review below is about work Tara or Jack did personally.</p>'
    '[[reviews:8]]'
    f'<div class="links"><a href="{esc(firm.GBP_URL)}" rel="noopener" target="_blank">Read every Google review</a><a href="{esc(firm.YELP_URL)}" rel="noopener" target="_blank">Reviews on Yelp</a></div>'
    '<p class="small">Testimonials reflect individual experiences. Prior results do not guarantee a similar outcome.</p>'
    '<h2>Leave a review</h2>'
    '<p>If we helped you or your family after an injury, two minutes on Google helps the next family find us. Reviews are also how Google decides which firms appear on the map when someone in Summerville searches for an accident lawyer.</p>'
    + steps([
        ("Open our Google listing.", f' Use this link: {ext(firm.REVIEW_URL, "leave a Google review")}. Sign in to your Google account if asked.'),
        ("Choose a star rating and write a sentence or two.", " What happened, how it went, and whether you would recommend us. Please leave out medical details and settlement amounts."),
        ("Post it.", " Reviews appear within a few days. We read every one."),
    ]) +
    '<h2>A note on what reviews can and cannot say</h2>'
    '<p>South Carolina attorney advertising rules and client confidentiality mean we never ask anyone to describe the details of a claim or a settlement, and we do not offer anything in exchange for a review. Honest words about your experience are all we ask.</p>'
    + band("Ready to talk?", "Call Tara or Jack, or send us a message. The consultation is free.")
)
page("reviews", kind="page", hub="about", layout="one",
     title="Client Reviews | Summerville Accident Attorneys | Frost Law Group",
     description="What injured clients and their families say about working with Tara and Jack Frost in Summerville, SC, and how to leave a review on Google or Yelp.",
     h1="Client Reviews", eyebrow="Client voices", nav_label="Client reviews", lead="What clients say about working with Frost Law Group after an injury.",
     body=reviews_body, priority=0.5)

# ----------------------------------------------------------------------------- BLOG INDEX
blog_body = (
    '<p class="lead">Local news and neighborhood questions about crashes, injuries and insurance, answered by the attorney who handles those cases. Every article links to the original reporting or the official source, and to the statute where one applies.</p>'
    '[[latestposts:20]]'
    '<h2>Ask the question that is not answered here</h2>'
    f'<p>Most of these articles started as a question a client, a neighbor or a Nextdoor thread asked. If yours is not here, call {TEL} or use the {A("contact", "contact form")}, and it may become the next one.</p>'
)
page("blog", kind="page", layout="one",
     title="Blog | Accident & Injury Questions Answered by Summerville Attorneys",
     description="What Lowcountry news means for a crash claim, a dog-bite case or an insurance dispute, written by Summerville injury attorney Tara Frost with links to the original reporting.",
     h1="The Blog", eyebrow="Local news, explained by your lawyer", nav_label="Blog",
     lead="What happens on I-26, at the dog park and in the General Assembly, and what it means for your claim.", body=blog_body, priority=0.6, changefreq="weekly")

# ----------------------------------------------------------------------------- PRIVACY
privacy_body = (
    '<p>This policy explains what information this website collects, what we do with it, and what we do not do. It applies to summervilleaccidentattorney.com. Our main firm site has its own policy.</p>'
    '<h2>What we collect</h2>'
    + checks([
        "<b>The contact form.</b> Your name, phone number, email address, the kind of case you chose and the message you wrote. The form is processed by Formspree, Inc., which delivers it to the firm by email and stores a copy according to its own privacy policy. We use it to respond to you and, if you become a client, as part of your file.",
        "<b>Calls and emails.</b> If you call or email us, we keep what you send so we can respond.",
        "<b>Server logs.</b> Our hosting provider records the pages requested, the time, your browser type and your IP address, as every web server does, for security and troubleshooting.",
        "<b>The map.</b> The map on the contact page and home page loads from Google only when you click to load it. Google's privacy policy applies once it loads.",
    ]) +
    '<h2>What we do not do</h2>'
    + checks([
        "We do not set tracking cookies, run advertising pixels or use analytics that follow you across sites. The site sets no cookies.",
        "We do not sell, rent or share your information with anyone outside the firm, other than the service providers named above that make the site work.",
        "We do not send marketing email. If you write to us, we write back about your question.",
    ]) +
    '<h2>Confidentiality</h2>'
    '<p>Information you send through the form is not privileged until we agree in writing to represent you, but we treat it as confidential from the moment it arrives. Please do not send details you would not want in an email: a phone call is more private.</p>'
    '<h2>Your choices</h2>'
    f'<p>You may ask us what information we hold about you, ask us to correct it, or ask us to delete it, subject to our professional obligation to keep client records. Write to {firm.NAME}, {firm.STREET}, {firm.CITY}, {firm.STATE} {firm.ZIP}, email <a href="mailto:{firm.EMAIL}">{firm.EMAIL}</a>, or call {TEL}.</p>'
    '<h2>Children</h2>'
    '<p>This site is not directed to children under 13 and we do not knowingly collect information from them. A parent or guardian should contact us on a child\'s behalf.</p>'
    f'<h2>Changes</h2><p>We will post any change to this policy on this page with a new date. Last updated September {firm.BUILD_DATE[:4]}.</p>'
)
page("privacy-policy", kind="page", layout="one", cta=False, priority=0.1,
     title="Privacy Policy | Summerville Accident Attorneys | Frost Law Group",
     description="How summervilleaccidentattorney.com handles the information you share through its contact form, the click-to-load map and server logs, and what we do not do with it.",
     h1="Privacy Policy", eyebrow="Your information", nav_label="Privacy policy", lead="What this site collects, what we do with it, and what we never do.", body=privacy_body)

# ----------------------------------------------------------------------------- TERMS OF USE
terms_body = (
    '<h2>Attorney advertising</h2>'
    f'<p>This website is a communication of {firm.NAME}, {firm.STREET}, {firm.CITY}, {firm.STATE} {firm.ZIP}, and may be considered attorney advertising under the South Carolina Rules of Professional Conduct. The attorneys responsible for its content are Tara L. Frost and Jack C. Frost, both licensed in South Carolina only.</p>'
    '<h2>Not legal advice</h2>'
    '<p>The information on this site is general information about South Carolina law and about our firm. It is not legal advice, it may not reflect the most recent changes in the law, and it may not apply to your situation. Do not act, or refrain from acting, on anything here without talking to a licensed attorney about your own facts.</p>'
    '<h2>No attorney-client relationship</h2>'
    '<p>Reading this site, calling us, or sending a message through the contact form does not make you a client and does not create an attorney-client relationship. We represent you only after we have agreed to do so in a signed engagement agreement. Until then, please do not send us confidential information you would not want disclosed, and understand that we may already represent someone with interests adverse to yours.</p>'
    '<h2>Results and testimonials</h2>'
    '<p>Any results described on this site depended on the facts of that case. Prior results do not guarantee or predict a similar outcome in your case. Client reviews are quoted as written by the reviewer and reflect that person\'s experience.</p>'
    '<h2>Fees</h2>'
    '<p>“No fee unless we win” refers to attorney\'s fees on personal injury cases handled on a contingency fee. Under South Carolina rules, a client may be responsible for case costs and expenses as set out in the engagement agreement, whether or not there is a recovery. We explain costs in writing before you sign.</p>'
    '<h2>Accuracy and changes</h2>'
    '<p>We work to keep the site accurate, and we cite the statute or official source for the legal statements we make. Laws, court addresses and procedures change, and we may not update every page immediately. We may change or remove any content, and these terms, at any time without notice.</p>'
    '<h2>Links</h2>'
    '<p>Links to court, agency, news and community websites are provided for convenience. We do not control those sites and are not responsible for their content.</p>'
    '<h2>Intellectual property</h2>'
    f'<p>The text, design and images on this site belong to {firm.NAME} or are used with permission. You may print or share pages for personal, non-commercial use with attribution. You may not copy the site\'s content for another website or commercial purpose without written permission.</p>'
    '<h2>Limitation of liability</h2>'
    f'<p>The site is provided “as is.” To the fullest extent the law allows, {firm.NAME} and its attorneys and staff are not liable for any loss arising from your use of, or reliance on, the site or any site linked from it.</p>'
    '<h2>Governing law</h2>'
    '<p>These terms are governed by the laws of the State of South Carolina. Any dispute about the site will be heard in the state courts of Dorchester County, South Carolina.</p>'
    f'<h2>Questions</h2><p>Write to {firm.NAME}, {firm.STREET}, {firm.CITY}, {firm.STATE} {firm.ZIP}, or call {TEL}. Our {A("privacy-policy", "privacy policy")} explains how we handle information you share through the site. Terms last updated September {firm.BUILD_DATE[:4]}.</p>'
)
page("terms-of-use", kind="page", layout="one", cta=False, priority=0.1,
     title="Terms of Use & Legal Disclaimer | Summerville Accident Attorneys",
     description="The rules for using summervilleaccidentattorney.com: attorney advertising notice, no legal advice, no attorney-client relationship until an engagement agreement, results and fee disclaimers.",
     h1="Terms of Use &amp; Legal Disclaimer", eyebrow="Please read", nav_label="Terms of use", lead="What this site is, what it is not, and the rules for using it.", body=terms_body)

# ----------------------------------------------------------------------------- ACCESSIBILITY
access_body = (
    '<p>Frost Law Group wants every visitor, including people who use screen readers, keyboard navigation, magnification or voice control, to be able to read this site and reach us. Many of our clients are reading this while injured, medicated or in pain, so the site is built to be simple and light. We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.1 at level AA.</p>'
    '<h2>What we have done</h2>'
    + checks([
        "Every page is built with semantic HTML: one heading per page, ordered headings, real lists, tables with header cells, and landmarks for the header, navigation, main content and footer.",
        "The whole site works with a keyboard. A “Skip to content” link appears on the first Tab press, focus is always visible, and the menus open on focus as well as hover.",
        "Text and background colors meet WCAG contrast ratios, text resizes with your browser or device settings, and nothing depends on color alone.",
        "Images carry descriptive alternative text; decorative graphics are hidden from assistive technology.",
        "Forms have visible labels tied to their fields, and errors are described in text.",
        "There is no autoplaying media or flashing content, and animations are disabled for visitors who have asked their device to reduce motion.",
        "Pages are light and work on slow connections and small screens; the site does not require JavaScript to read.",
        "A Spanish-language page is available for Spanish-speaking visitors.",
    ]) +
    '<h2>Known limitations</h2>'
    + checks([
        "The interactive map is provided by Google and loads only when you choose it; its accessibility is Google's. The written directions and address on the same page carry the same information as text.",
        "Some links lead to court, agency and news websites and to documents (often PDFs) we do not control.",
    ]) +
    '<h2>Our office</h2>'
    '<p>Our office at 128 Linwood Lane has free parking directly in front and a ground-level entrance. If you have a mobility, hearing, vision or other need, tell us when you book and we will make arrangements, including meeting at your home, hospital or rehabilitation facility, meeting by phone or video, providing documents in large print, or allowing extra time. Our comfort dogs stay in the back on request.</p>'
    '<h2>Tell us if something does not work</h2>'
    f'<p>If any part of this site is hard to use, or you need information in another format, call {TEL} or use the {A("contact", "contact form")}. Tell us the page and what happened; we will fix what we can and send you the information another way in the meantime. This statement was last reviewed in September {firm.BUILD_DATE[:4]}.</p>'
)
page("accessibility", kind="page", layout="one", cta=False, priority=0.1,
     title="Accessibility Statement | Summerville Accident Attorneys",
     description="How summervilleaccidentattorney.com and the Frost Law Group office are built to be usable by everyone, including injured visitors, known limitations, and how to report a problem.",
     h1="Accessibility Statement", eyebrow="For every visitor", nav_label="Accessibility", lead="How this site is built to be usable by everyone, and how to reach us if it is not.", body=access_body)

# ----------------------------------------------------------------------------- THANK YOU
thanks_body = (
    '<p class="lead">Your message is on its way to Tara, Jack and Cassie. We read every one, and an attorney will reply by phone or email.</p>'
    '<h2>If it cannot wait</h2>'
    f'<p>Call {TEL}. An attorney will get back to you.</p>'
    '<h2>While you wait</h2>'
    + checks([
        f'{A(CAR + "/what-to-do-after-a-car-accident-in-south-carolina", "What to do in the first 48 hours after a crash")}.',
        f'{A(CAR + "/should-i-talk-to-the-other-drivers-insurance-company", "What to say, and not say, to the other driver’s insurance company")}.',
        f'{A(CAR + "/auto-injury-assessment-after-a-crash", "Getting your injuries evaluated")}, even if you feel fine.',
        f'{A("contact", "Directions to the office")} on local roads, and what to bring.',
    ])
    + '<p class="small">Sending a message does not create an attorney-client relationship until we agree in writing to represent you. Please do not give a recorded statement to any insurance company before we talk.</p>'
)
page("thank-you", kind="page", layout="one", cta=False, noindex=True, priority=0.1,
     title="Thank You | Summerville Accident Attorneys",
     description="We received your message, and an attorney will get back to you. For anything urgent, call the office in Summerville, South Carolina.",
     h1="Thank you. We have your message.", eyebrow="Message received", nav_label="Thank you", lead="", body=thanks_body)
