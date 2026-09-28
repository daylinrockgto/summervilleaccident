"""Legacy page kept at its old address, with its old copy, by Daylin's decision of 2026-09-28.

/practice-areas/workers-compensation/ serves the copy the live site showed on 2026-09-28, captured from the rendered
page, with its old title and description. Nothing on this site links to it: no menu, footer, form option, card, FAQ
or cross-link. Do not edit the copy, and do not link to the page. (Settled 2026-09-28.)
"""
from .base import page
from . import firm

TEL = f'<a href="tel:{firm.PHONE_E164}">{firm.PHONE}</a>'

WC_BODY = (
    "<p>Hurt on the job? Get the benefits and care you've earned.</p>"
    f"<p>Free Consultation: {TEL}</p>"
    "<p>A workplace injury shouldn't cost you your income or your health. South Carolina workers' compensation should cover your medical care and lost wages — but employers and insurers often delay, deny, or underpay valid claims.</p>"
    "<p>Workers' compensation is a no-fault system, meaning you don't have to prove your employer did anything wrong. But that doesn't make the process easy: claims get denied, treatment gets delayed, and injured workers get pressured back to work too soon.</p>"
    "<p>We handle denied and disputed claims, fight for the medical treatment you need, and pursue permanent disability benefits. When a third party contributed to your injury, we also pursue a separate personal injury claim for even more recovery.</p>"
    "<p>Workers across Summerville, Ladson, North Charleston, Goose Creek, and Dorchester County are injured in industrial facilities, construction sites, warehouses, and distribution centers every year. Our workers' compensation attorneys fight for full benefits and take on employers and insurers who deny or underpay valid claims throughout the Lowcountry.</p>"
    "<h2>Cases We Handle</h2>"
    "<ul><li>Denied and disputed comp claims</li><li>Construction and warehouse injuries</li><li>Repetitive stress and overuse injuries</li>"
    "<li>Back, neck, and joint injuries</li><li>Permanent disability claims</li><li>Third-party injury claims</li></ul>"
    "<h2>Compensation You May Recover</h2>"
    "<ul><li>Full coverage of medical treatment</li><li>Weekly wage-replacement benefits</li><li>Permanent partial or total disability</li>"
    "<li>Vocational rehabilitation</li><li>Third-party damages when applicable</li></ul>"
)
WC_FAQS = [
    ("My workers' comp claim was denied. What now?",
     "A denial is not the end. We appeal denials before the South Carolina Workers' Compensation Commission and gather the medical evidence needed to prove your claim."),
    ("Can I sue my employer for a work injury?",
     "Usually workers' compensation is your exclusive remedy against your employer, but if a third party (like a contractor or equipment maker) contributed, you may have a separate injury claim worth pursuing."),
    ("Will I get fired for filing a claim?",
     "It is illegal for an employer to retaliate against you for filing a legitimate workers' compensation claim. If that happens, we can help protect your rights."),
    ("Can I choose my own doctor for a workers' compensation injury in South Carolina?",
     "In South Carolina, your employer or their insurer typically has the right to direct your medical care initially. However, if you are unhappy with the authorized physician or they are not providing appropriate treatment, we can help you seek a change of physician or an independent medical evaluation."),
    ("What should I do immediately after being injured at work in Summerville, SC?",
     "Report the injury to your employer in writing as soon as possible — South Carolina requires notice within 90 days, but sooner is better. Seek medical care through the employer's authorized provider, document your injuries and the accident conditions, and contact a workers' compensation attorney before giving any recorded statements."),
]

page("practice-areas/workers-compensation", kind="page", layout="one", cta=False, priority=0.3,
     title="Summerville Workers' Compensation Lawyer | Work Injury Attorney SC",
     description="Injured at work in Summerville, SC? Our workers' compensation attorneys fight denied claims and secure medical care and lost wages. Free consultation. No fee unless we win.",
     h1="Summerville Workers' Compensation Lawyers", nav_label="Workers' Comp", body=WC_BODY, faqs=WC_FAQS)["_legacy"] = True
