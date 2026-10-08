# llg/ — the Frost Law Group page kit

This folder holds everything behind the long-form pages on summervilleaccidentattorney.com. It covers the rules they were written to, the research behind every fact, the plan every heading comes from, the page checker, and the review history. Nothing in `llg/` is published, because Vercel serves only `website/`.

## What Is in Git

The repository is public, so only part of this kit is committed. `README.md`, `pages/*.html`, `plan/`, `v2/` and `tools/` are in git. Those cover the edit, sync and build workflow. The sidecars (`pages/*.json`), `briefs/`, `context/`, `research/`, `review/`, `repo-review/`, the handoffs and the launch runbook are in `.gitignore` and travel in the kit zip.

Without the kit, `sync_pages.py` runs as usual and `frost_check.py` runs every check except the sidecar check, so an edit that adds no fact can go through. To clear the sidecar check, or to add a fact, unzip the kit over the checkout first. After you change a sidecar or any other local-only file, rebuild the kit zip so the change is not lost.

## Folder Map

| Path | What it holds |
| --- | --- |
| `pages/<id>.html` | **The source of truth for page copy.** Plain HTML, h1 to h5, p, a, strong and em. |
| `pages/<id>.json` | The sidecar for each page. Its `new_facts` list gives the source URL for every fact added beyond the research files. |
| `plan/plan.json` | Every page's id, URL, keyphrase, H2s, links and word band. The checker reads it. |
| `plan/h2_overrides.json` | H2 renames made after planning. `set_h2.py` writes it. |
| `briefs/<id>.md` | The brief each page was written to, with word band, required links and sibling pages not to echo. |
| `context/WRITER-BRIEF.md` | Binding writing rules for page copy. |
| `context/approved-client-facts.md` | The only firm facts allowed in copy. |
| `context/county-research-pack.md` | Verified county detail. The CORRECTIONS block at the top overrides the rest. |
| `context/REVIEWER-BRIEF.md`, `context/FIXER-BRIEF.md` | How pages were reviewed and fixed. FIXER-BRIEF lists the cross-page corrections A to H. |
| `research/R1` to `R5` | Verified law and local research. `research/raw/` holds the fetched statute and source text. |
| `review/R-*.md`, `review/F-*.md` | Independent review reports and the fix logs that answered them. |
| `repo-review/RR-*.md` | The September 28 audit of the first repo build. |
| `v2/manifest.json`, `v2/meta_v2.json` | Page Manifest v7 (architecture) and the final titles and descriptions. |
| `v2/Frost Law Group - Page Manifest and Redirect Map v7.md` | The readable manifest and redirect map. |
| `v2/tools/sync_pages.py` | Copies `pages/*.html` into `site/content/pages/` and writes `pages.json`. |
| `v2/tools/make_docs.py` | Builds a review .docx for every page, each ending in an Upload Sheet. |
| `tools/frost_check.py` | The page checker. |
| `tools/set_h2.py` | The only safe way to rename an H2. |
| `HANDOFF-2026-09-29.md` | Where the project stood when this kit was made. |

## Changing Page Copy

1. Edit `llg/pages/<id>.html`. Never edit `site/content/pages/*.html` directly, because the next sync overwrites it.
2. If an H2 changes, run `python3 llg/tools/set_h2.py <id> "<old H2>" "<new H2>"` first, then make the same change in the HTML.
3. Check the page with `python3 llg/tools/frost_check.py <id> --grammar`, and repeat until it prints CLEARED. Every link, the first-link position, the phone format, the CTA rules, banned words and 8-word overlap with every other page are checked. If it flags overlap with another page, reword the page you are editing.
4. Run `python3 llg/v2/tools/sync_pages.py`.
5. Run `python3 site/build_site.py`. It must exit 0.
6. Commit `llg/`, `site/` and `website/` together.

A new fact needs a source from `research/` or the county pack. Otherwise, fetch a primary source and add it to the page's sidecar `new_facts` with the URL. Primary sources are the SC Code, SCDPS, SCDMV, SCDOI, the courts, the Census Bureau, and hospital or city sites.

## Grammar Check Setup

`--grammar` needs Java 17 or later and LanguageTool, run as a local server on port 8081. `tools/ensure_lt.sh` starts it.

```bash
pip install language_tool_python
python3 -c "import language_tool_python as l; l.LanguageTool('en-US').close()"   # downloads LanguageTool once
```

If the environment cannot download LanguageTool, run the checker without `--grammar` and say so in the pull request.

## The Spanish Page

`pages/es.html` is outside the plan, so `frost_check.py` does not run on it. Review Spanish edits by hand against the same compliance rules.
