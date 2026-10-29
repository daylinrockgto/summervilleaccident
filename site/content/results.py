"""Case results for the home page and the PPC landers (settled 2026-10-29).

Source: "Case Settlements.xlsx", sent by Dustin Douglas (LLG Customer Experience) on October 29, 2026 as case wins for
Tara Frost, and supplied by Daylin the same day. Each amount is the sheet's "Net Settlement Proceeds" figure, kept to
the cent so the totals match the sheet. The sheet's one workers' compensation row is left out, because the site carries
no workers' compensation content (settled 2026-09-28).

SC Rule 7.1(d)(4) and its Comment [3] allow results only with a clear and conspicuous statement that a result in one
matter does not necessarily indicate similar results for other clients. Every block that shows a figure from this file
carries DISCLAIMER right under the figures, and checks.py fails the build when a results block is missing it.

Results appear only in the results bands (results_band() in build_site.py for the home page, the [[LP_RESULTS]] part
for the landers). Long-form copy never repeats them.
"""
import math

CAR, DEATH, PREMISES, MED_MAL, INSURANCE = "car", "death", "premises", "med-mal", "insurance"

# (net settlement proceeds, case type), in the spreadsheet's row order
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

# the label under each figure. "Premises liability" is the sheet's own term: an injury caused by unsafe property.
LABELS = {CAR: "Car accident settlement", DEATH: "Wrongful death settlement", PREMISES: "Premises liability settlement",
          MED_MAL: "Medical malpractice settlement", INSURANCE: "Insurance claim settlement"}

# The four figures each band shows, largest first. The home page spans the three practice areas the site markets
# (wrongful death, car accidents, premises injuries). Every lander is a car accident ad, so its band shows car results only.
HOME_PICKS = [(2202000, DEATH), (850000, DEATH), (500000, CAR), (350000, PREMISES)]
LANDER_PICKS = [(500000, CAR), (325000, CAR), (275000, CAR), (213191, CAR)]

DISCLAIMER = ("Any result Frost Law Group has achieved for a client in one matter does not necessarily indicate that "
              "the firm can obtain a similar result for other clients. Each case turns on its own facts and law. "
              "The amounts shown are net settlement proceeds.")


def total(kind=None):
    """The sum of the net amounts, for one case type or for every row."""
    return sum(a for a, k in SETTLEMENTS if kind in (None, k))


def money(amount):
    """$2,202,000. Cents drop, rounding down, so a figure never reads higher than the sheet."""
    return f"${math.floor(amount):,}"


def more_than(amount):
    """'$7.4 million' for $7,431,445.41. Rounds down to a tenth of a million, so 'more than' stays true."""
    return f"${math.floor(amount / 100000) / 10:.1f} million"


for _pick in HOME_PICKS + LANDER_PICKS:  # a pick must be a real row, so a typo can never put a figure on the site
    assert _pick in SETTLEMENTS, f"results pick {_pick} is not in SETTLEMENTS"
