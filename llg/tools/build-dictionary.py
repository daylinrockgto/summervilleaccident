#!/usr/bin/env python3
"""
build-dictionary.py -- regenerate dictionary.txt from the live registry.
Added 2026-08-26. Grammarly and LanguageTool flag every client name, city,
courthouse, and legal term as a spelling mistake. Measured on six shipped
blogs: 66 of 101 total flags were correct proper nouns. Filtering them is
what makes the real errors visible.
Run after onboarding a client or adding cities to a matrix.
"""
import re, glob, os
here = os.path.dirname(os.path.abspath(__file__))
words = set()

# firm names out of the client profiles
for f in glob.glob(os.path.join(here, 'clients', '*.md')):
    t = open(f, encoding='utf8', errors='ignore').read()
    for m in re.findall(r'Firm name in copy:\s*\*\*(.+?)\*\*', t):
        words.update(re.findall(r"[A-Z][A-Za-z'\-]{2,}", m))
    for m in re.findall(r'(?:Cities|Counties|Locations)\s*:\s*(.+)', t):
        words.update(re.findall(r"[A-Z][A-Za-z'\-]{2,}", m))

# city axis out of every coverage matrix, column 1 of the table
for f in glob.glob(os.path.join(here, 'matrix', '*.md')):
    for line in open(f, encoding='utf8', errors='ignore'):
        if line.startswith('|') and not re.match(r'\|\s*[-:]+', line):
            cell = line.split('|')[1].strip()
            if cell and cell.lower() not in ('location', 'city'):
                words.update(re.findall(r"[A-Z][A-Za-z'\-]{2,}", cell))

# curated terms, verified correct. Add here when the scanner flags a good word.
CURATED = """
# added 2026-09-16 (RH&A Los Angeles blog)
Wilshire Hinman Moradi
rideshare rideshares ridesharing telematics subrogation tortfeasor
litem materialman materialmen chargeability adjudicated adjudication
uninsured underinsured deductible declarations
eFileGA eFileTexas Odyssey TurboCourt
Martindale Avvo Superlawyers Justia Nolo
INTEGRIS MultiCare Harborview Sutter Deaconess Grady Piedmont Wellstar
Bricktown Colcord Mallon Sepulveda Mosk Shondeana Beason
Encino Tarzana Reseda Northridge Sylmar Pacoima Chatsworth Calabasas
Glendale Burbank Sunland Tujunga Winnetka Panorama Granada
Stonecrest Lithonia Tucker Doraville Chamblee Sandy Duluth Snellville
Bellevue Renton Kirkland Puyallup Lynnwood Everett Kennewick Wenatchee
Norman Edmond Moore Yukon Bethany Midwest
USCIS ICE CBP NVC EOIR
OCGA RCW ORS NRS
Faragalla Reiersen Ritchie Kreeger Lassiter Hawkins Felton Gaslamp
Banks Ware Noreen Enoch Andrews
Hindin Deukmejian Rhapilaw Vuong
Anaheim Bakersfield Chula Vista Fresno Riverside
Memorial MemorialCare Harbor
CAALA LACBA OCBA CACI

# added 2026-08-31 from the eleven-blog batch. Every one was flagged by
# LanguageTool and every one is correct as written.
# case names and parties
McCutchen Adeniji Buenrostro Mendez Bondi Sosnava Talisker Rutherford
Yarbray McNary Nevitt Parnell Pickering Blake Oregel Rodriguez Stiles
Tarron Kassman Busfield Beason Guerra
# added 2026-09-08 from the Ogden wrongful death blog. Utah case names and places.
Carvell Drezga McKay Riverdale
# legal terms of art
respondeat entrustment vacatur vacaturs habeas noncitizen noncitizens
removability subrogate subrogee lienholder unfiled lookback palmprints
adjudicative nonconformity nonconformities arraignment arraignments
predicate Molineux Sandoval Huntley Dunaway Rosario repleader
# agencies, programs, reporters
ERISA OASDI SORA CPW DOCCS DCJS NYSACDL NYSDA SDNY EDNY
AZDPS Fedwire CeBONDS LACIV MRTA CCIA Marihuana
# places and institutions
Karnes Frio Dolorosa Tukwila Schermerhorn Wetmore Snyderville Marsac
Arleta Knollwood Roxford Tani Cantil Sakauye Schaber HonorHealth AirMed
Hochul Carfax Kimball Silver Summit Wagoner Sapulpa Owasso Bixby Jenks
Claremore Muskogee Bartlesville Glenpool Ascension
Cordova Rancho Auburn Folsom Rocklin Woodland Marysville Placerville
Scottsdale Chandler Gilbert Tempe Mesa Surprise Flagstaff
Bronx Brooklyn Queens Manhattan Staten Kings Richmond Rikers LaGuardia
Graybar Petrus Aglaia Midwood NoMad Sheepshead Bayside Flushing
Deer Valley Wasatch Murray Ogden Provo Orem Logan Moab
# added 2026-09-08 from the Tacoma truck accident blog. All verified correct.
Tyrrell WSDOT Tideflats drayage Allenmore Commencement Thurston
# hyphenated tokens must appear verbatim, the matcher does not split on the hyphen
Buenrostro-Mendez Cantil-Sakauye Medi-Cal Peterson-KFF
# reporter abbreviations and unit designations
Wn XE
# spellings that are correct inside a quoted statute
wilfully marihuana
# medical and technical
degloved caretaking mTBI polytrauma physiatrist orthotic prosthetic
# added 2026-09-08 from the North Hollywood transit batch. Every one was
# flagged by LanguageTool and every one is correct as written.
Lankershim Vineland Cahuenga Toluca NoHo
LACMTA LADOT STEMI
busway Busway Antonovich
# added 2026-09-08 from the Mesa motorcycle blog. Both are correct Mesa
# street names, verified against Maricopa County and AZDHS sources.
Javelina Crismon
# added 2026-09-08 from the Katy pedestrian blog. Verified proper nouns and
# correct terms of art, all flagged by LanguageTool.
Cinco Heimann Schwertner Bonnen TxDOT Torry
chargemaster sightline overserved
# added 2026-09-08 from the Folsom brain injury blog. Bidwell and Natoma are
# Folsom street names verified against City of Folsom pages. Jennett is a
# co-author of the Glasgow Coma Scale, verified against NCBI StatPearls.
# Sargon is a California Supreme Court case name, 55 Cal.4th 747.
Bidwell Natoma Jennett Sargon
# added 2026-09-08 from the Chula Vista dog bite blog. Rady is Rady Children's
# Hospital San Diego, the region's Level 1 pediatric trauma center. Beyer Way is
# the address of the Chula Vista Animal Care Facility, verified against the
# City of Chula Vista Animal Care pages.
Rady Beyer
# added 2026-09-08 from the Queens assault blog. Chiddick is a New York Court
# of Appeals case name, People v Chiddick. The rest are Queens place names and
# a Queens Community Justice Center program, all verified.
Chiddick Kew Rosedale Laurelton Conduit Elmhurst Uplift
# added 2026-09-22 from the Westlake Injury Law Chatsworth Metro crash blog. Names of
# the victims, the charged driver, the District Attorney and a California Supreme Court
# case, all verified against the DA release, LAPD, NTSB coverage and SCOCAL.
Weida Rios Hochman Marciniw Edy Mejia DaFonte Ercolani Westlake Telemundo
Nollan Etiwanda Penfield Whiteman NewsChopper4 Nordhoff
"""
# Strip comment lines before splitting, then keep 2-character tokens.
# The old line was `CURATED.split() if len(w) > 2`, which had two defects:
# it silently dropped legitimate two-letter tokens such as the reporter
# abbreviations Wn and XE, and it swept every word of the # comment lines
# into the allow list. Fixed 2026-08-31.
_curated = '\n'.join(l for l in CURATED.splitlines() if not l.strip().startswith('#'))
words.update(w for w in _curated.split() if len(w) >= 2)

out = os.path.join(here, 'dictionary.txt')
old = set()
if os.path.exists(out):
    old = {l.strip() for l in open(out, encoding='utf8') if l.strip() and not l.startswith('#')}
words |= old   # never drop a word someone added by hand

with open(out, 'w', encoding='utf8') as fh:
    fh.write("# Known-good words. Not spelling mistakes.\n")
    fh.write("# Auto-built by build-dictionary.py from clients/ and matrix/, plus a curated list.\n")
    fh.write("# Hand-added words are preserved on rebuild. Add one per line.\n")
    for w in sorted(words, key=str.lower):
        fh.write(w + "\n")
print(f"dictionary.txt: {len(words)} words ({len(words)-len(old)} new)")
