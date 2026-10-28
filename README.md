<img src="assets/favicon.svg" width="72" height="72" alt="GoldBrief briefcase logo">

# ☀️ GoldBrief — AI Explained

Free, open-source AI news, education and company tracking. **Understand AI. Question claims. Discover what works.**

## 🏠 Current homepage — v1.0.0 (Build 1)
☀️ **Live:** [sukonik.github.io/goldbrief](https://sukonik.github.io/goldbrief/) · 🔧 [Pull request #5](https://github.com/Sukonik/goldbrief/pull/5) · 🚀 [Deploy workflow](https://github.com/Sukonik/goldbrief/actions/workflows/pages.yml) · 🧪 [QA workflow](https://github.com/Sukonik/goldbrief/actions/workflows/qa.yml)

News-first front page with a compact headline list, an automated "unreviewed headlines" feed, and a single grouped desktop menus and a hamburger drawer under 1024px. Older homepage versions are logged at the [bottom of this README](#-homepage-version-history).

**Key pages:** [Home](https://sukonik.github.io/goldbrief/) · [News](https://sukonik.github.io/goldbrief/news.html) · [Lake](https://sukonik.github.io/goldbrief/lake.html) · [AI USA](https://sukonik.github.io/goldbrief/usa.html) · [International](https://sukonik.github.io/goldbrief/international.html) · [Apps](https://sukonik.github.io/goldbrief/apps.html) · [Tools](https://sukonik.github.io/goldbrief/resources.html) · [UI/UX](https://sukonik.github.io/goldbrief/ui-ux.html) · [Editorial policy](https://sukonik.github.io/goldbrief/trust.html)

## ☀️ Mission
Make AI easier to understand and more useful to everyday people, reduce fear and misinformation, and avoid becoming promotional material for AI companies. Optimistic about the potential, skeptical of unsupported claims, transparent in reporting.

## 📰 Editorial philosophy
- Every item carries its source, date and a label: **Company announcement**, **Independent reporting**, **Educational resource**, or **Automated / unreviewed**.
- No invented revenue, usage, valuations, funding or growth rankings. Features that need such data are labeled *planned*.
- Automated RSS headlines are never presented as fact-checked.

## 🧭 Website navigation
[Home](https://sukonik.github.io/goldbrief/) (news front page) · [Lake](https://sukonik.github.io/goldbrief/lake.html) · [Leaderboards](https://sukonik.github.io/goldbrief/leaderboards.html) · [AI USA](https://sukonik.github.io/goldbrief/usa.html) · [International](https://sukonik.github.io/goldbrief/international.html) · [Visuals](https://sukonik.github.io/goldbrief/visuals.html) · [Markets](https://sukonik.github.io/goldbrief/markets.html) · [Apps](https://sukonik.github.io/goldbrief/apps.html) · [News](https://sukonik.github.io/goldbrief/news.html) · [Index](https://sukonik.github.io/goldbrief/index-directory.html) · [Glossary](https://sukonik.github.io/goldbrief/glossary.html) · [Encyclopedia](https://sukonik.github.io/goldbrief/encyclopedia.html) · [Tools](https://sukonik.github.io/goldbrief/resources.html) · [UI/UX](https://sukonik.github.io/goldbrief/ui-ux.html) · [Editorial policy](https://sukonik.github.io/goldbrief/trust.html) · [About](https://sukonik.github.io/goldbrief/about.html). One responsive hamburger drawer on screens under 1200px.

## 🇺🇸 U.S. tracker / 🌍 International tracker
`data/companies.json` → [usa.html](https://sukonik.github.io/goldbrief/usa.html), [international.html](https://sukonik.github.io/goldbrief/international.html). Each profile has headquarters, country, focus, products/use, official site, updates link, a dated event where one exists, and the date sources were checked. HQ is the organization's primary base; parent-company relationships (e.g. Google DeepMind within Alphabet) are stated. 20 organizations in Build 1.

## 🧩 Applications directory
`data/apps.json` → [apps.html](https://sukonik.github.io/goldbrief/apps.html). 112 apps in 17 categories; searchable and filterable by category and company location, with six questions to ask before signing up and a caution per category. Regenerate with `python3 scripts/build_apps.py`. A directory, not an endorsement; pricing and privacy details are not asserted without a source.

## 📈 Markets and visualizations
[markets.html](https://sukonik.github.io/goldbrief/markets.html) is a watchlist of public companies and IPO status with links to filings, not live prices. [visuals.html](https://sukonik.github.io/goldbrief/visuals.html) shows only counts derived from our datasets (region, focus, listing status, curated stories by month and label). Usage growth, funding and valuation charts are **planned** until reliable dated data exists.

## 📚 Education & resources
[Glossary](https://sukonik.github.io/goldbrief/glossary.html), [Encyclopedia](https://sukonik.github.io/goldbrief/encyclopedia.html), **[Tools](https://sukonik.github.io/goldbrief/resources.html)** (skills directories such as skills.sh, courses, data and safety sources) and **[UI/UX](https://sukonik.github.io/goldbrief/ui-ux.html)** (the most-starred UI component projects on GitHub's ui-components topic, with a guide to building and improving interfaces with AI; public design-system repositories we learn from; check each license before reusing code).

## 🛡️ Verification and corrections policy
See [trust.html](https://sukonik.github.io/goldbrief/trust.html). Report errors by [opening an issue](https://github.com/Sukonik/goldbrief/issues) with the page, the claim, and a source.

## ⏰ Daily 8:30 AM ET update workflow
`.github/workflows/daily.yml` makes five staggered attempts (12:07, 12:37, 13:07, 13:37, 14:07 UTC) because GitHub's scheduler is best-effort and can skip or delay runs; `scripts/daily_update.py` publishes only inside the 8–10 AM America/New_York window and once per ET day, so it handles daylight saving time and extra attempts exit in seconds. News pages show the edition date, collection time, and a warning if today's edition is late. GitHub scheduled runs can start late, so the actual run time is stored in `data/daily.json` (`actual_run_et`). The script collects US and international RSS headlines, timestamps, de-duplicates and clusters them, validates the result, and keeps the last good edition if feeds fail or validation fails. It then runs QA, writes `reports/daily-site-check.json`, and triggers a Pages deploy. Details: `docs/DAILY_OPERATIONS.md`.

## 🎨 UI/UX architecture
Matte black with gold accents, text-first, no frameworks. An angled, black Piano briefcase serves as the favicon and header mark. Outfit sets the masthead and headlines; Inter carries articles and interface text, with Helvetica fallbacks. See [brand and typography](docs/BRAND.md). CSS layers: `tokens` → `base` → `components` → `responsive` → `goldbrief`. Designed from GoldRang3r. Keyboard-accessible drawer (Escape, focus trap), skip link, reduced-motion support.

## 🧪 Testing
```bash
python3 tests/check_site.py            # structure, links, ids, JSON (no dependencies)
npm i --no-save playwright && npx playwright install chromium
node tests/browser_check.js            # 16 pages x 8 widths: overflow, JS errors, drawer
python3 scripts/build_trackers.py      # regenerate tracker cards + Visuals from data/
python3 scripts/build_resources.py     # regenerate Resources and UI/UX pages
```
The pull-request workflow (`qa.yml`) runs all of this and fails if generated pages are stale. Automated checks do not replace human visual review.

## 🚀 Deployment and publishing
GitHub Pages via `.github/workflows/pages.yml` on pushes to `main`. Preview a branch locally with `python3 -m http.server`. Launch approval: Nathan.

## 🗺️ Roadmap
- **1.0** news-first site, trackers, apps, education, daily headlines, QA.
- **1.1** verified per-company history/diffs, richer encyclopedia, screenshot-based visual review.
- **2.0** usage, funding and valuation charts once reliable datasets and update mechanisms exist.

## 📜 License
[Mozilla Public License 2.0](LICENSE).

## 🕰️ Homepage version history
Newest version is shown at the [top](#-current-homepage--v100-build-1); this log lists earlier versions, newest first. **Maintenance rule:** when the homepage changes in a user-visible way, move the previous "Current" entry here, add the new one at the top, and add a matching [CHANGELOG](CHANGELOG.md) entry.

| Version | Date | Status | Homepage summary |
| --- | --- | --- | --- |
| 1.0.0 | 2026-10-27 | **Current** (see top) | First public release: news-first front page, drawer menu, automated unreviewed-headline feed, 20-organization tracker, Resources and UI/UX pages. |
| pre-1.0 draft 3 | 2026-10-27 | Never public | Stable GoldRang3r-style header, mobile navigation and chart styles ([`bc62fde`](https://github.com/Sukonik/goldbrief/commit/bc62fde)). |
| pre-1.0 draft 2 | 2026-10-27 | Never public | Accessible drawer, source-headline rendering, directory search ([`b692ecb`](https://github.com/Sukonik/goldbrief/commit/b692ecb)). |
| pre-1.0 draft 1 | 2026-10-27 | Never public | First news-first homepage ([`b6f570b`](https://github.com/Sukonik/goldbrief/commit/b6f570b)). |

Drafts are listed from branch history before launch. Exact earlier states can be viewed with `git show <commit>:index.html`.
