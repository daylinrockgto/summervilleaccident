"""/questions/ — a link index of the answer pages, grouped by practice area. It copies no answers (each answer lives
on one page only), so it carries no FAQ markup of its own."""
from .base import page, BY_SLUG, esc
from . import llg

GROUPS = {}
for r in llg.ANSWER_PAGES:
    GROUPS.setdefault(r["hub"], []).append(r)

if GROUPS:
    parts = ['<p>These are the questions people in Summerville and the surrounding counties ask most often after a crash or an injury. '
             'Each one has its own page with a direct answer first, the South Carolina law behind it, and what to do next. '
             'If your question is not here, call Frost Law Group and ask it.</p>']
    for hub, rows in GROUPS.items():
        h = BY_SLUG.get(hub)
        label = h["nav_label"] if h else hub
        parts.append(f'<h2>{esc(label)} questions</h2><ul class="qlist">' + "".join(f'<li><a href="[[{r["slug"]}]]">{esc(r["h1"])}</a></li>' for r in rows) + "</ul>")
    page("questions", kind="page", layout="two",
         title="Questions After an Accident in Summerville | Ask Us",
         description="Questions after an accident in Summerville, answered one page at a time by Frost Law Group, from fault and deadlines to insurance. Find yours or call us.",
         h1="Questions People Ask After an Accident in Summerville", eyebrow="Frost Law Group · Summerville, SC", nav_label="Questions",
         body="".join(parts), priority=0.6)
