# qa-selftest.py -- regression test for qa-scan.py.
# Builds a blog that FOLLOWS the rules and asserts the scanner clears it on every check.
# Run this after every edit to qa-scan.py. A gate that fails everything is as useless as one
# that passes everything.
#   python3 qa-selftest.py && python3 qa-scan.py /tmp/selftest.docx \
#      --keyphrase "Auburn dog bite lawyer" --domain kreegerlaw.com --city Auburn --state CA
# Expected: 47/47 on the good blog (2026-09-22). 31/31 before the metadata and claims checks.
#
# 2026-09-22: --teeth builds one broken copy per new check and confirms the scanner FAILS it.
# A passing selftest proves nothing about a new check. Only a failing mutant does.
#   python3 qa-selftest.py --teeth
import sys, importlib.util
spec = importlib.util.spec_from_file_location("minidocx", "minidocx.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

KP   = "Auburn dog bite lawyer"
SITE = "https://kreegerlaw.com"

def para(sents):
    return "<p>" + " ".join(sents) + "</p>"

# short declarative sentences, all well under 25 words
S = {
 'a':["Placer County handles these claims through its own filing rules.","The Auburn Police Department writes the initial report.","Animal Services logs the quarantine order separately.","Both records matter to the claim.","A parent should request each one in writing."],
 'b':["Sutter Auburn Faith Hospital treats most of these injuries.","The emergency record sets the starting medical number.","Follow up care is billed separately.","Keep every statement you receive.","Those bills anchor the damages figure."],
 'c':["The Placer County Superior Court sits on Historic Courthouse Drive.","A minor's case follows a different track there.","The judge reviews the settlement before anyone is paid.","That hearing is scheduled, not automatic.","Ask about it early."],
 'd':["Highway 49 and Auburn Ravine Road see frequent loose dog calls.","Location changes who is responsible.","A public sidewalk is not a private yard.","The distinction decides the claim.","Document where the bite happened."],
 'e':["Homeowner coverage usually responds first.","Renter policies apply when the owner rents.","Some policies exclude certain breeds.","Read the declarations page.","An exclusion changes the whole strategy."],
}
KEYS=list(S)
def P(k, n=2):
    out=[]
    for i in range(n):
        kk=KEYS[(KEYS.index(k)+i)%len(KEYS)]
        out.append(para(S[kk]))
    return "".join(out)

H = []
H.append(f"<h1>When Should You Call an {KP} After a Child Is Bitten?</h1>")
H.append(f"<p><strong>Call an {KP} before the ten day quarantine ends. "
         "California makes the owner liable without any prior bite. "
         "A child's deadline runs differently than an adult's. "
         "Evidence in Placer County disappears fast.</strong></p>")
H.append("<p>An insurer may call the same week. Kreeger Law has handled Placer County "
         "bite claims for years. The firm represents injured people only. "
         "A parent does not have to sort the policies out alone.</p>")
H.append("<p>Call our office at <a href=\"tel:5305551212\">530-555-1212</a> for a free review.</p>")

# H2 #1 -- first paragraph MUST carry the internal link
H.append("<h2>Who Pays for a Child's Dog Bite Injuries in Auburn</h2>")
H.append(f"<p>The dog's owner pays first. <a href=\"{SITE}/auburn-dog-bite-lawyer/\">Kreeger Law</a> "
         "reviews the policy before any adjuster calls. "
         "Placer County claims often involve two carriers. "
         "Sorting that out early protects the child's recovery. "
         "The owner's identity is only the starting point. "
         "A landlord may carry separate coverage. "
         "A dog walker may not be covered at all. "
         "Each possibility changes who you notify first. "
         "Notice deadlines are shorter than most parents expect.</p>")
H.append(P('a'))
H.append("<h3>Medical Costs Drive the Starting Number</h3>"); H.append(P('b'))
H.append("<h4>Emergency Treatment at Sutter Auburn Faith Hospital</h4>"); H.append(P('b'))
H.append("<h5>Why Rabies Prophylaxis Changes the Bill</h5>"); H.append(P('e'))
H.append("<h5>What the Trauma Record Should Show</h5>"); H.append(P('a'))
H.append("<h4>Plastic Surgery Deferred Until a Child Stops Growing</h4>"); H.append(P('c'))
H.append("<h3>Scarring Is Valued Separately From Bills</h3>"); H.append(P('d'))

H.append("<h2>Where the Auburn Strict Liability Rule Stops</h2>")
H.append(f"<p>The statute reaches bites. It does not reach every injury a dog causes. "
         f"Read <a href=\"{SITE}/practice-areas/personal-injury/\">our personal injury page</a> for the wider rule. "
         "A knockdown is a negligence claim instead. "
         "The difference decides what you must prove.</p>")
H.append(P('e'))
H.append("<h3>It Reaches Bites, Not Every Dog Injury</h3>"); H.append(P('d'))
H.append("<h4>How Placer County Adjusters Treat Knockdowns</h4>"); H.append(P('a'))
H.append("<h4>Why the Animal Services Report Still Helps</h4>"); H.append(P('c'))
H.append("<h3>A Trespassing Child Falls Outside the Statute</h3>"); H.append(P('b'))

H.append("<h2>What Happens During the Auburn Ten Day Quarantine</h2>")
H.append(f"<p>Placer County Animal Services orders the hold. See "
         f"<a href=\"{SITE}/auburn/\">our Auburn office page</a> for local contacts. "
         "The order is written the same day. "
         "It creates a record you will want.</p>")
H.append(P('a'))
H.append("<h3>Who Files the Report and When</h3>"); H.append(P('c'))
H.append("<h3>What the Quarantine Order Does Not Decide</h3>"); H.append(P('e'))

H.append(f"<h2>How an {KP} Proves the Owner Is Liable</h2>")
H.append(f"<p>Liability rests on <a href=\"https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&amp;sectionNum=3342.\">California Civil Code section 3342</a>. "
         "The owner is liable without any prior bite. "
         "You do not have to prove the owner knew.</p>")
H.append(P('e'))
H.append("<h3>The Four Elements You Must Show</h3>"); H.append(P('d'))
H.append("<h3>Where the Owner Definition Runs Out</h3>"); H.append(P('b'))

H.append("<h2>How a Child's Deadline Differs in Placer County</h2>")
H.append("<p>A minor's clock is tolled. The deadline runs from the eighteenth birthday. "
         "Evidence does not wait that long. "
         "Move early anyway.</p>")
H.append(P('c'))
H.append("<h3>Why Waiting Costs the Claim</h3>"); H.append(P('a'))
H.append("<h3>How the Court Approval Hearing Fits the Timeline</h3>"); H.append(P('c'))

H.append("<h2>Answers for a Parent Whose Child Was Just Bitten</h2>")
H.append("<p>These are the questions parents ask most often after a bite in Auburn. "
         "Each answer reflects how Placer County actually handles these claims. "
         "Local practice differs from the general rule in several places. "
         "Call us if your situation does not match any of them. A short conversation usually tells you whether the claim is worth pursuing.</p>")
H.append("<h3>Does Homeowner's Insurance Cover a Dog Bite in California?</h3>")
H.append("<p>Usually yes. Most homeowner policies include liability coverage for dog bites. Some carriers exclude specific breeds or cap the payout. Read the declarations page before you accept anything.</p>")
H.append("<h3>Do We Have to Sue a Neighbor Personally?</h3>")
H.append("<p>No. The claim goes to the insurer, not to your neighbor personally. The neighbor is named on paper but the carrier pays the settlement. Most neighbors never write a check.</p>")
H.append("<h3>How Long Will a Child's Case Take?</h3>")
H.append("<p>Most resolve in nine to eighteen months. The Placer County court approval hearing adds several weeks. Cases involving scarring often wait for a surgeon to confirm the final result.</p>")
H.append("<h3>Can the Dog Be Declared Dangerous?</h3>")
H.append("<p>Yes. Placer County Animal Services can hold a dangerous dog hearing. That finding supports the civil claim and creates a record the insurer cannot ignore.</p>")

H.append(f"<h2>Talk to an {KP} Before Anyone Settles Your Child's Claim</h2>")
H.append(f"<p>Kreeger Law handles dog bite claims across Placer County. "
         f"Call <a href=\"tel:5305551212\">530-555-1212</a> for a free consultation. "
         "We review the policy and the quarantine record at no cost. You will know within a day whether the claim holds up.</p>")
H.append("<p>An adjuster may call within days. You do not have to answer alone. "
         "A first offer rarely reflects future surgery. Children heal, but scars change as they grow. Settling early can close the door on that cost.</p>")
H.append(f"<p>Reach us through our <a href=\"{SITE}/contact/\">contact page</a> or by phone. "
         "We will tell you where your child's claim stands. There is no fee unless we recover, and you owe no case costs without a recovery.</p>")

TITLES = [
 "Auburn Dog Bite Lawyer Help for Parents. Call Today",
 "Ask an Auburn Dog Bite Lawyer Who Pays a Child's Bills",
 "Talk to an Auburn Dog Bite Lawyer Before Quarantine Ends",
 "Bitten in Placer County? Call an Auburn Dog Bite Lawyer",
 "Get an Auburn Dog Bite Lawyer on the Insurance Claim Early",
 "Auburn Dog Bite Lawyer for Scar Claims. Free Case Review",
 "Start With an Auburn Dog Bite Lawyer After an Attack",
 "Book an Auburn Dog Bite Lawyer Review of the Owner's Policy",
 "Why Call an Auburn Dog Bite Lawyer Within Ten Days",
 "Does a Child Need an Auburn Dog Bite Lawyer? Find Out",
]
DESCS = [
 "A child bitten in Auburn needs fast answers. An Auburn dog bite lawyer explains who pays under California law. Call Kreeger Law for a free consultation.",
 "The owner's homeowner policy usually pays first. Ask an Auburn dog bite lawyer how Placer County claims work and call Kreeger Law for a free review today.",
 "Placer County Animal Services orders a ten day hold after a bite. Talk to an Auburn dog bite lawyer about that record. Your first consultation is free.",
 "Scars change as children grow, so an early offer rarely fits. An Auburn dog bite lawyer can value future surgery. Call today to start your free case review.",
 "Civil Code section 3342 makes the owner liable without a prior bite. See how an Auburn dog bite lawyer proves the claim, then call for a free consultation.",
 "Treated at Sutter Auburn Faith Hospital? An Auburn dog bite lawyer can use that record to set the claim value. Call Kreeger Law for a free review today.",
 "A minor's deadline runs from the eighteenth birthday, but evidence fades. Get an Auburn dog bite lawyer on the claim early and book a free review today.",
 "Most neighbors never pay out of pocket because the insurer does. Learn how an Auburn dog bite lawyer handles the claim, then contact Kreeger Law today.",
 "A Placer County judge must approve a child's settlement. An Auburn dog bite lawyer prepares that hearing. Call Kreeger Law and start a free case review.",
 "Most child bite cases resolve in nine to eighteen months. Ask an Auburn dog bite lawyer what your timeline looks like and request a free consultation today.",
]

def meta_html(titles, descs):
    out = ["<h2>Metadata Options Not Page Copy</h2>", "<p>SEO titles</p>"]
    out += [f"<p>{i}. {t}</p>" for i, t in enumerate(titles, 1)]
    out.append("<p>Meta descriptions</p>")
    out += [f"<p>{i}. {d}</p>" for i, d in enumerate(descs, 1)]
    return "".join(out)

GOOD = "".join(H)

# One mutant per 2026-09-22 check: (label the scanner must FAIL, page html, titles, descs)
def mutants():
    T, D = list(TITLES), list(DESCS)
    def t(i, v): x = list(T); x[i] = v; return x
    def d(i, v): x = list(D); x[i] = v; return x
    yield ("Metadata block has 10 SEO titles", GOOD, T[:9], D)
    yield ("SEO titles 60 chars max, option 1 at 55", GOOD, t(0, "Auburn Dog Bite Lawyer Help for Worried Parents. Call Today"), D)
    yield ("Meta descriptions 150 to 156 chars", GOOD, T, d(2, "A short description with an Auburn dog bite lawyer. Call today."))
    yield ("Exact keyphrase in every title and description", GOOD, t(4, "Get a Placer County Bite Attorney on the Claim Early"), D)
    yield ("A CTA in every title and description", GOOD, t(5, "Auburn Dog Bite Lawyer for Children With Facial Scars"), D)
    yield ("No word repeated inside a title", GOOD, t(6, "Auburn Dog Bite Lawyer for an Auburn Family. Call Today"), D)
    yield ("No AI-styled or over-punctuated title wording", GOOD, t(7, "The Ultimate Auburn Dog Bite Lawyer Guide. Call Today"), D)
    yield ("No colons, dashes, or phone numbers in titles and descriptions", GOOD, T,
           d(0, "Dog bite help: an Auburn dog bite lawyer explains who pays under California law. Call Kreeger Law for a free consultation about your child's claim."))
    yield ("Title options vary in shape and option 1 is a statement", GOOD,
           t(0, "Who Pays When You Call an Auburn Dog Bite Lawyer?"), D)
    yield ("Metadata promises only what the page delivers", GOOD, t(8, "Call an Auburn Dog Bite Lawyer Within 72 Hours"), D)
    yield ("Exact keyphrase in 3 headings or fewer", GOOD.replace(
           "<h3>The Four Elements You Must Show</h3>", "<h3>The Four Elements an Auburn Dog Bite Lawyer Must Show</h3>"), T, D)
    yield ("No generic or vague headings", GOOD.replace(
           "<h3>Who Files the Report and When</h3>", "<h3>Overview</h3>"), T, D)
    yield ("Descriptive anchor text", GOOD.replace(">our Auburn office page</a>", ">click here</a>"), T, D)
    yield ("No guarantee or predicted outcome", GOOD.replace(
           "The owner's identity is only the starting point.", "We guarantee a settlement for your child."), T, D)
    yield ("Money and percentages as $ and %", GOOD.replace(
           "Some policies exclude certain breeds.", "Some policies cut payouts by 20 percent."), T, D)
    yield ("No-fee statement also says whether the client owes costs", GOOD.replace(
           ", and you owe no case costs without a recovery.", "."), T, D)
    # the loophole the 2026-09-22 review found: the word "costs" with no cost disclosure
    yield ("No-fee statement also says whether the client owes costs", GOOD.replace(
           ", and you owe no case costs without a recovery.", ". The call costs nothing."), T, D)
    yield ("No-fee statement also says whether the client owes costs", GOOD, T,
           d(9, "No fee unless we win for an Auburn dog bite lawyer claim. Most child bite cases resolve in nine to eighteen months. Call today to request a free review."))

if __name__ == "__main__":
    m.build(GOOD + meta_html(TITLES, DESCS), "/tmp/selftest.docx")
    print("built /tmp/selftest.docx")
    if "--teeth" in sys.argv:
        import subprocess, os
        here = os.path.dirname(os.path.abspath(__file__))
        args = ["--keyphrase", KP, "--domain", "kreegerlaw.com", "--city", "Auburn", "--state", "CA"]
        good = subprocess.run([sys.executable, os.path.join(here, "qa-scan.py"), "/tmp/selftest.docx"] + args,
                              capture_output=True, text=True)
        print("good blog:", good.stdout.strip().splitlines()[-1])
        ok_all = good.returncode == 0
        for label, page, titles, descs in mutants():
            m.build(page + meta_html(titles, descs), "/tmp/selftest-mutant.docx")
            r = subprocess.run([sys.executable, os.path.join(here, "qa-scan.py"), "/tmp/selftest-mutant.docx"] + args,
                               capture_output=True, text=True)
            fails = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("FAIL")]
            hit = any(label in f for f in fails)
            other = [f.split("   [")[0][6:] for f in fails if label not in f]
            ok_all &= hit
            print(f"  {'TEETH' if hit else 'MISSED'}  {label}" + (f"   (also failed: {other})" if other else ""))
        print("All new checks have teeth." if ok_all else "A check MISSED its mutant or the good blog failed. Fix before trusting the gate.")
        sys.exit(0 if ok_all else 1)
