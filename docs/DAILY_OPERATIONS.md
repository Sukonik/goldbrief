# 🛠️ GoldBrief daily editorial + UI/UX operating cycle

**Goal:** ~8:30 AM America/New_York every day, with GitHub Actions scheduling subject to GitHub's normal delays.

## 📰 Automated editorial layer
- Trigger at 12:30 and 13:30 UTC; Eastern timezone gate keeps the appropriate one (DST-aware).
- Fetch publicly available RSS headline and source URLs, timestamp each edition and identify every article as **automated / unreviewed**.
- Never invent usage, company growth rates, IPO status, revenue, valuation or facts from press releases.
- Preserve the prior successful edition if feeds are unreachable; never make the newsroom falsely appear freshly verified.
- Companies, original summaries and research links stay manually curated until an evidence-first editorial workflow exists.

## 🎨 Daily UI/UX sweep
Run `python3 tests/check_site.py` for structural integrity, duplicate ids, JSON validity, internal pages/assets, responsive CSS and mobile menu scripting. Save the QA status in `reports/daily-site-check.json`.

**Human design review:** examine screenshots at 320/375/390/430/768/1024/1440px, exercise menu keyboard navigation, scan tap targets and contrast, ensure headings don't wrap awkwardly, review page speed and image/video weight, confirm article citations and content age. The daily structural test **is not** a substitute for screenshot-based visual validation.

## 📊 Growth/visual roadmap
A true adoption dashboard must have transparent source-specific definitions, permission to ingest data, citations and dated snapshots. Visits, token counts, financial figures and model benchmarks must **never** be combined into a single unlabeled growth score.

## 🚨 Corrections
Submit false/expired claims to [GitHub Issues](https://github.com/Sukonik/goldbrief/issues). Include article, issue, supporting source and publication date. Automations cannot validate all claims.
