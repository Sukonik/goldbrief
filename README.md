# ☀️ GoldBrief — AI Explained

Free, open-source AI news, education and company tracking. **Understand AI. Question claims. Discover what works.**

> 🚧 **Status: Build 1 (v1.0.0) in review.** Not yet published. The target address is `sukonik.github.io/goldbrief`; this README will link it once the GitHub Pages deployment is verified.

## ☀️ Mission
Make AI easier to understand and more useful to everyday people, reduce fear and misinformation, and avoid becoming promotional material for AI companies. Optimistic about the potential, skeptical of unsupported claims, transparent in reporting.

## 📰 Editorial philosophy
- Every item carries its source, date and a label: **Company announcement**, **Independent reporting**, **Educational resource**, or **Automated / unreviewed**.
- No invented revenue, usage, valuations, funding or growth rankings. Features that need such data are labeled *planned*.
- Automated RSS headlines are never presented as fact-checked.

## 🧭 Website navigation
Home (news front page) · Lake · Leaderboards · AI USA · International · Visuals · Markets · Apps · News · Index · Glossary · Encyclopedia · Resources · UI/UX · Trust · About. One responsive hamburger drawer on screens under 1200px.

## 🇺🇸 U.S. tracker / 🌍 International tracker
`data/companies.json` → `usa.html`, `international.html`. Each profile has headquarters, country, focus, products/use, official site, updates link, a dated event where one exists, and the date sources were checked. HQ is the organization's primary base; parent-company relationships (e.g. Google DeepMind within Alphabet) are stated. 20 organizations in Build 1.

## 🧩 Applications directory
`data/apps.json` → `apps.html`. Searchable and filterable by category. A directory, not an endorsement; pricing and privacy details are not asserted without a source.

## 📈 Markets and visualizations
`markets.html` is a watchlist of public companies and IPO status with links to filings, not live prices. `visuals.html` shows only counts derived from our datasets (region, focus, listing status, curated stories by month and label). Usage growth, funding and valuation charts are **planned** until reliable dated data exists.

## 📚 Education & resources
Glossary, Encyclopedia, **Resources** (skills directories such as skills.sh, courses, data and safety sources) and **UI/UX** (public design-system repositories we learn from; check each license before reusing code).

## 🛡️ Verification and corrections policy
See `trust.html`. Report errors by [opening an issue](https://github.com/Sukonik/goldbrief/issues) with the page, the claim, and a source.

## ⏰ Daily 8:30 AM ET update workflow
`.github/workflows/daily.yml` runs at 12:30 and 13:30 UTC; `scripts/daily_update.py` publishes only inside the 8–9 AM America/New_York window and once per ET day, so it handles daylight saving time. GitHub scheduled runs can start late, so the actual run time is stored in `data/daily.json` (`actual_run_et`). The script collects US and international RSS headlines, timestamps, de-duplicates and clusters them, validates the result, and keeps the last good edition if feeds fail or validation fails. It then runs QA, writes `reports/daily-site-check.json`, and triggers a Pages deploy. Details: `docs/DAILY_OPERATIONS.md`.

## 🎨 UI/UX architecture
Matte black with gold accents, Helvetica-first, text-first, no frameworks. CSS layers: `tokens` → `base` → `components` → `responsive` → `goldbrief`. Designed from GoldRang3r. Keyboard-accessible drawer (Escape, focus trap), skip link, reduced-motion support.

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
