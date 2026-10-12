# Advertising record, Rule 7.2(b)

South Carolina Rule 7.2(b) says a lawyer keeps a copy of each advertisement for two years after it last ran, with a record of when and where it ran. This website is an advertisement, so every version that has run on www.summervilleaccidentattorney.com is listed below. These notes are not published.

## Where Each Copy Is Kept

- **Exact copy.** Each version's `website/` folder is in git at the commit listed. `git archive <commit> website | tar -x -C <folder>` restores every file byte for byte, and `python3 -m http.server --directory <folder>/website` serves it.
- **Vercel.** Each production deployment stays in the deployment list of the `summervilleaccident` project in `daylinrockgtos-projects`, with its commit.
- **PDF snapshots.** `python3 site/snapshot.py OUT.pdf --commit <commit>` prints every page of a version to one PDF. Each sheet shows the 1280px desktop layout with every accordion open, plus the live URL, the version and the capture time. Photos are scaled to 640px so a full set stays small enough to file. The PDFs are too large for git, so they go to Daylin for the firm's advertising file.

## Versions on www.summervilleaccidentattorney.com

Times are Eastern. Each start time is the moment Vercel built that production deployment from `main`. The domain went onto the Vercel project on October 9, 2026 at 2:49 PM ET. Before that, the domain served the old Coderrick site from SiteGround.

| Version | Commit | Live from | Live until | What changed | PDF snapshot |
| --- | --- | --- | --- | --- | --- |
| Launch | `42ba6a1` (PR 21) | Oct 9, 2026, 2:49 PM | Oct 9, 2026, 7:01 PM | The first version on the real domain | `summervilleaccidentattorney.com launch 2026-10-09 (42ba6a1).pdf` |
| 2 | `cd3912f` (PR 22) and `4f3acfa` (PR 23) | Oct 9, 2026, 7:01 PM | Oct 11, 2026, 3:22 PM | Added `/favicon.ico` and its link in every page head. No visible change, so the launch snapshot covers it. PR 23 changed only the build notes | The launch snapshot |
| 3 | `197a1bf` (PR 24) | Oct 11, 2026, 3:22 PM | Oct 12, 2026, 2:44 PM | The home page rewrite. Only the home page and the 404 page changed | `summervilleaccidentattorney.com home page 2026-10-11 (197a1bf).pdf` |
| 4 | `17421bc` (PR 25) | Oct 12, 2026, 2:44 PM | Still live | The October 12 review fixes. Every footer gained the Rule 7.2(f) costs sentence and the responsible attorney line, and the top bar gained "Se habla español". 52 pages gained the short form, and images gained alt text | `summervilleaccidentattorney.com review fixes 2026-10-12 (17421bc).pdf` |

The same production deployments also answer at summervilleaccident-pi.vercel.app, which has served production since September 29, 2026 (PR 5). Its pages name www.summervilleaccidentattorney.com as their canonical address.

## Snapshot Files

Made on October 12, 2026 with `site/snapshot.py` and sent to Daylin for the firm's advertising file. A file whose SHA-256 matches the one here is unchanged since it was made.

| File | Pages | Sheets | Size | SHA-256 |
| --- | --- | --- | --- | --- |
| `summervilleaccidentattorney.com launch 2026-10-09 (42ba6a1).pdf` | 94 | 792 | 25.5 MB | `75b769c62d66e9b4b7c6c002b99b39fca99beb45b21dc5f0abdfe77beee7fa85` |
| `summervilleaccidentattorney.com home page 2026-10-11 (197a1bf).pdf` | 1 | 12 | 1.3 MB | `ad7e9ce8277386a541d860b58f9b9e66f591fc401120ea03519bfbdd1491659d` |
| `summervilleaccidentattorney.com review fixes 2026-10-12 (17421bc).pdf` | 94 | 802 | 26.5 MB | `c3ee5ff03f05512cbdac220581619284f3fdedabadbd62e13347f4ab636eefa9` |

## Keeping This Record

- With every merge to `main` that changes `website/`, add a row for the new version and fill in the previous row's end time from Vercel's production deployment list.
- Print a snapshot of the new version with `site/snapshot.py`, or of only the pages it changed with `--pages`, and add the PDF to the firm's advertising file.
- Keep every row and snapshot for at least two years after its version stops running.
