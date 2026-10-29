"""Case results for the home page and the PPC landers (settled 2026-10-29).

Source: "Case Settlements.xlsx", sent by Dustin Douglas (LLG Customer Experience) on October 29, 2026 as case wins for
Tara Frost, and supplied by Daylin the same day. Each amount is the sheet's "Net Settlement Proceeds" figure, kept to
the cent so the totals match the sheet. Daylin confirmed on 2026-10-29 that the column is each case's total settlement,
and that all 66 rows here are the firm's own injury cases for this site. The sheet's one workers' compensation row is
left out, because the site carries no workers' compensation content (settled 2026-09-28).

SC Rule 7.1(b) and (d)(4), read with Comment [3], allow results only with a clear and conspicuous statement that a result in one
matter does not necessarily indicate similar results for other clients. Daylin decided on 2026-10-29 that the bands
carry no disclaimer of their own, so the footer's firm.PRIOR_RESULTS ("Prior results do not guarantee a similar outcome.")
is the only one, and checks.py fails the build when the footer of a page with a results block is missing it.

Results appear only in the results bands (results_band() in build_site.py for the home page, the [[LP_RESULTS]] part
for the landers). Long-form copy never repeats them.
"""
import math

CAR, DEATH, PREMISES, MED_MAL, INSURANCE = "car", "death", "premises", "med-mal", "insurance"

# (total settlement, case type), in the spreadsheet's row order
SETTLEMENTS = [
    (23000, CAR), (500000, CAR), (7500, CAR), (7300, CAR), (1120, CAR), (1070, CAR), (20500, CAR), (19500, CAR),
    (100000, CAR), (4500, CAR), (275000, CAR), (14337.42, CAR), (35000, CAR), (28000, CAR), (57500, CAR), (11000, CAR),
    (10400, CAR), (213191, CAR), (24000, CAR), (17682, CAR), (20000, CAR), (18500, CAR), (5000, CAR), (35000, CAR),
    (150000, CAR), (12500, CAR), (14000, CAR), (10000, CAR), (29483.60, CAR), (25000, CAR), (59500, CAR), (29000, CAR),
    (27500, CAR), (25000, CAR), (50000, CAR), (4800, CAR), (4000, CAR), (65000, CAR), (12000, CAR), (110000, CAR),
    (125000, CAR), (28000, CAR), (25000, CAR), (125000, CAR), (8000, CAR), (27994.55, CAR), (325000, CAR),
    (26887.22, CAR), (170000, CAR), (72696.40, CAR), (155000, CAR), (2000, CAR),
    (366408.22, INSURANCE),
    (200000, MED_MAL),
    (10000, PREMISES), (15000, PREMISES), (350000, PREMISES), (11000, PREMISES), (4500, PREMISES), (20000, PREMISES),
    (30000, PREMISES), (5500, PREMISES), (37500, PREMISES),
    (2202000, DEATH), (850000, DEATH), (162075, DEATH),
]

# the label under each figure. The sheet says "Premises liability", a legal term, so a premises card says it in the
# home page's own plain words ("falls on unsafe property") unless the firm has said what kind of case it was.
LABELS = {CAR: "Car accident settlement", DEATH: "Wrongful death settlement", PREMISES: "Unsafe property settlement",
          MED_MAL: "Medical malpractice settlement", INSURANCE: "Insurance claim settlement"}

# a confirmed label for one row beats its case type's label. Daylin confirmed on 2026-10-29 that the $350,000 premises
# case was a slip and fall.
CASE_LABELS = {(350000, PREMISES): "Slip and fall settlement"}

# the landers' heading already names car accidents, so their cards carry the short label
LANDER_LABELS = {CAR: "Settlement"}

# The four figures each band shows, largest first. The home page spans the three practice areas the site markets
# (wrongful death, car accidents, slip and fall). Every lander is a car accident ad, so its band shows car results only.
HOME_PICKS = [(2202000, DEATH), (850000, DEATH), (500000, CAR), (350000, PREMISES)]
LANDER_PICKS = [(500000, CAR), (325000, CAR), (275000, CAR), (213191, CAR)]


def total(kind=None):
    """The sum of the net amounts, for one case type or for every row."""
    return sum(a for a, k in SETTLEMENTS if kind in (None, k))


def money(amount):
    """$2,202,000. Cents drop, rounding down, so a figure never reads higher than the sheet."""
    return f"${math.floor(amount):,}"


def more_than(amount):
    """'$7.4 million' for $7,431,445.41: the largest tenth of a million below the amount, so "More than" stays true
    even for a total that lands exactly on a tenth ($3,100,000 reads $3.0 million)."""
    assert amount > 1000000, "more_than() words totals in millions"
    return f"${(math.ceil(amount / 100000) - 1) / 10:.1f} million"


for _pick in HOME_PICKS + LANDER_PICKS + list(CASE_LABELS):  # a pick must be a real row, so a typo can never put a figure on the site
    assert _pick in SETTLEMENTS, f"results pick {_pick} is not in SETTLEMENTS"
