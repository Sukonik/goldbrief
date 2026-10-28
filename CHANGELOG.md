# Changelog

## Unreleased
- docs: external cron setup recorded with a stale-news runbook and token rotation checklist.
- Daily workflow: manual/API dispatch is no longer forced by default (new `force` input), so an external cron can ping it safely; added `docs/EXTERNAL_CRON.md` with cron-job.org setup.
- Daily news: five staggered scheduled attempts (the single 8:30 slot was skipped by GitHub on 2026-10-28), fast exit when no edition is due, wider ET window, and a visible edition/status line with a stale-edition notice.
- UI/UX page: the 23 most-starred projects on GitHub's `ui-components` topic (dated snapshot, with stars and platform), a step-by-step guide with a prompt template for building components with AI, and a section on how AI can improve interface design, with limits.
- Desktop header is now six grouped dropdown menus (hover, click, keyboard); Resources page renamed **Tools**, Trust labeled **Editorial policy**; hamburger breakpoint lowered to 1024px.
- Apps directory expanded from 20 to 112 apps in 17 categories with location filter, per-category cautions and a six-question checklist.
- UI/UX page no longer lists the project's own repositories.
- Daily workflow: browser-tooling failures no longer block the headline edition.

## 1.0.0 — 2026-10-27 (Build 1)
Live: https://sukonik.github.io/goldbrief/

- News-first Home plus Lake, Leaderboards, AI USA, International, Visuals, Markets, Apps, News, Index, Glossary, Encyclopedia, Trust, About.
- New **Resources** page (skills.sh and similar directories, courses, data, safety) and **UI/UX** page (public design-system repositories).
- Tracker expanded to 20 organizations (added Google/Alphabet, MiniMax); cards show source-checked date.
- Visuals regenerated from datasets: region, focus, listing status, news by month and label.
- Daily engine: US + international feeds, timestamps, clustering, validation, fallback, explicit Pages deploy after bot commits.
- QA: headless-browser checks at 320–1920px, PR workflow, daily review report with priorities and regression flags.
- README rewritten. Live URL not linked until deployment is verified.
