#!/usr/bin/env python3
"""
grammar-scan.py  --  grammar gate for blogs and pages.
Added 2026-08-26 after Daylin said he spends a long time clearing Grammarly
flags on every page.

What the measurement showed, across six shipped blogs and ~15,000 words:
  101 total LanguageTool flags
   66 were correct proper nouns (client names, cities, courthouses,
      hospitals, legal terms). Zero real spelling mistakes.
   ~20 were genuine, mostly comma and hyphen rules.
   ~15 were false positives on legal phrasing.
So the job is two things: fix the real ones, and stop the noise from
drowning them. dictionary.txt handles the noise.

Usage:
  python3 grammar-scan.py FILE.docx            [--profile clients/kreeger-law.md]
  python3 grammar-scan.py FILE.txt --fix       # print corrected text to stdout
  cat draft.txt | python3 grammar-scan.py -

Exit 0 = no blocking errors. Exit 1 = fix before delivery.
Needs: pip install language_tool_python  (and Java, already present)
"""
import sys, os, re, html, zipfile, argparse
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))

# Rules that block delivery. These were all real in the measured sample.
BLOCKING = {
    'MISSING_COMMA_AFTER_YEAR',              # January 1, 2017 and  ->  2017, and
    'COMMA_COMPOUND_SENTENCE',               # comma before and joining two clauses
    'COMMA_COMPOUND_SENTENCE_2',             # comma before so / but / yet
    'MISSING_COMMA_AFTER_INTRODUCTORY_PHRASE',
    'MISSING_HYPHEN',                        # six month deadline -> six-month
    'ANY_BODY', 'NEITHER_NOR',
    'ENGLISH_WORD_REPEAT_BEGINNING_RULE',    # 3 sentences opening the same way
    'ENGLISH_WORD_REPEAT_RULE',
    'EN_A_VS_AN', 'IT_VBZ', 'HE_VERB_AGR', 'THIS_NNS', 'PLURAL_VERB_AFTER_THIS',
    'AGREEMENT_SENT_START', 'SUBJECT_VERB_AGREEMENT',
    'DOUBLE_PUNCTUATION', 'COMMA_PARENTHESIS_WHITESPACE', 'WHITESPACE_RULE',
    'UPPERCASE_SENTENCE_START', 'SENTENCE_WHITESPACE',
}
BLOCKING_CATEGORIES = {'GRAMMAR', 'CONFUSED_WORDS', 'TYPOGRAPHY'}

# Known false positives in legal writing. Reported for review, never blocking.
REVIEW_ONLY = {
    'SPACE_BEFORE_PARENTHESIS',   # O.C.G.A. 19-5-3(13) is correct citation form
    'A_RB_NN',                    # "an underinsured vehicle" is correct
    'POSSESSIVE_APOSTROPHE',      # "medical payments coverage" is the policy term
    'THE_LATER_LATTER',           # "the later of X or Y" is standard legal phrasing
    'ASK_THE_QUESTION', 'RELATIVE_CLAUSE_AGREEMENT',
    'PCT_SINGULAR_NOUN_PLURAL_VERB_AGREEMENT',
    'WHETHER',                    # fine inside a direct statute quotation
}

# Verified-correct phrasing that specific rules get wrong in legal writing.
# Matched on rule id PLUS the surrounding context, so the rule stays live everywhere
# else. Added 2026-08-31 after measuring the eleven-blog batch. Prefer rewriting the
# sentence over adding a line here. Only add a phrasing that will genuinely recur.
PHRASE_ALLOW = [
    ('MANY_NN', 'several liability'),          # joint and several liability, term of art
    ('IN_WHO', 'About Who'),                   # "about who pays", who is the subject
    ('FEWER_LESS', 'grams or less'),           # tracks 8 C.F.R. 316.10 wording
    ('COMMA_COMPOUND_SENTENCE_2', 'issued or renewed on or after'),  # no second clause
    ('AUXILIARY_DO_WITH_INCORRECT_VERB_FORM', 'Does Skipping a Helmet Hurt'),  # Frost moto approved H2, gerund subject, 2026-09-28
    ('HE_VERB_AGR', "What Are South Carolina's Minimum"),  # Frost a-at-fault approved H2, 'Limits' is the plural subject, 2026-09-28
]

def phrase_allowed(rule_id, context):
    c = context.lower()
    return any(rule_id == r and ph.lower() in c for r, ph in PHRASE_ALLOW)

def load_dictionary(profile=None):
    words = set()
    p = os.path.join(HERE, 'dictionary.txt')
    if os.path.exists(p):
        words = {l.strip() for l in open(p, encoding='utf8')
                 if l.strip() and not l.startswith('#')}
    # auto-allow capitalized names that appear in this client's own profile
    if profile and os.path.exists(profile):
        t = open(profile, encoding='utf8', errors='ignore').read()
        words |= set(re.findall(r"\b[A-Z][A-Za-z'\-]{2,}\b", t))
    return {w.lower() for w in words}

def paragraphs(path):
    if path == '-':
        return [l.strip() for l in sys.stdin.read().split('\n') if l.strip()]
    if path.lower().endswith('.docx'):
        doc = zipfile.ZipFile(path).read('word/document.xml').decode('utf8')
        out = []
        for p in re.findall(r'<w:p[ >].*?</w:p>', doc, re.S):
            t = html.unescape(''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p)))
            if t.strip(): out.append(t.strip())
        for i, l in enumerate(out):                     # drop the metadata block
            if 'metadata options' in l.lower() or 'upload sheet' in l.lower() or 'page details for upload' in l.lower(): return out[:i]
        return out
    return [l.strip() for l in open(path, encoding='utf8') if l.strip()]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--profile', default=None, help="client profile, auto-allows its proper nouns")
    ap.add_argument('--fix', action='store_true', help='print corrected text instead of a report')
    ap.add_argument('--show-review', action='store_true', help='also print the non-blocking review items')
    a = ap.parse_args()

    try:
        import language_tool_python as lt
    except ImportError:
        print("grammar-scan needs: pip install language_tool_python --break-system-packages")
        return 2

    allow = load_dictionary(a.profile)
    tool = lt.LanguageTool('en-US', remote_server=os.environ['LT_SERVER']) if os.environ.get('LT_SERVER') else lt.LanguageTool('en-US')
    paras = paragraphs(a.path)

    blocking, review, dropped = [], [], Counter()
    for para in paras:
        for m in tool.check(para):
            word = m.context[m.offset_in_context:m.offset_in_context + m.error_length]
            if m.rule_id == 'MORFOLOGIK_RULE_EN_US':
                bare = word.strip("'’s").lower()
                if bare in allow or word.lower() in allow:
                    dropped[word] += 1
                    continue
            if phrase_allowed(m.rule_id, m.context):
                dropped[word] += 1
                continue
            item = (m.rule_id, m.message, m.context.strip(), word, m.replacements[:3])
            if m.rule_id in REVIEW_ONLY:                      review.append(item)
            elif m.rule_id in BLOCKING:                       blocking.append(item)
            elif m.category in BLOCKING_CATEGORIES:           blocking.append(item)
            elif m.rule_id == 'MORFOLOGIK_RULE_EN_US':        blocking.append(item)
            else:                                             review.append(item)

    if a.fix:
        print('\n'.join(tool.correct(p) for p in paras)); return 0

    name = os.path.basename(a.path)
    print("=" * 74); print(f"GRAMMAR  {name}"); print("=" * 74)
    if dropped:
        print(f"  {sum(dropped.values())} proper-noun flags suppressed by dictionary.txt "
              f"({len(dropped)} distinct)")
        print(f"     {', '.join(sorted(dropped, key=str.lower)[:14])}")
        print()
    if blocking:
        print(f"  {len(blocking)} ERROR(S), must fix before delivery\n")
        for rid, msg, ctx, word, rep in blocking:
            print(f"   [{rid}] {word!r}")
            print(f"      {msg[:100]}")
            print(f"      ...{ctx[:96]}...")
            if rep: print(f"      -> {rep}")
            print()
    else:
        print("  0 errors.\n")
    if review:
        print(f"  {len(review)} review item(s), non-blocking"
              + ("" if a.show_review else ", pass --show-review to list"))
        if a.show_review:
            print()
            for rid, msg, ctx, word, rep in review:
                print(f"   [{rid}] {word!r}  {msg[:80]}")
                print(f"      ...{ctx[:96]}...")
    print("-" * 74)
    print(("CLEARED." if not blocking else f"{len(blocking)} ERROR(S). DO NOT DELIVER."))
    return 1 if blocking else 0

if __name__ == '__main__':
    sys.exit(main())
