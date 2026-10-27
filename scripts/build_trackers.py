#!/usr/bin/env python3
"""Regenerate company cards, counts and Visuals charts in the static pages from data/*.json.

Run after editing data/companies.json, data/news.json or data/markets.json:
    python3 scripts/build_trackers.py
Only counts that can be derived from the datasets are produced; nothing is estimated.
"""
import html, json, re
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
load = lambda n: json.loads((ROOT / "data" / f"{n}.json").read_text(encoding="utf-8"))
e = html.escape
companies_doc, news_doc, markets_doc = load("companies"), load("news"), load("markets")
companies = companies_doc["companies"]; checked = companies_doc["updated"]

def card(c):
    ev = (f'<p><b>Documented event:</b> {e(c["signal"]["title"])} ({c["signal"]["date"]})</p>' if c.get("signal")
          else "<p>Growth metrics not verified in this edition.</p>")
    search = e(f'{c["name"]} {c["country"]} {c["focus"]} {c["use"]}'.lower())
    return (f'<article class="card company-card" data-search="{search}"><p class="card__meta">{e(c["country"])} · {e(c["focus"])}</p>'
            f'<h3>{e(c["name"])}</h3><p>{e(c["city"])}</p><p>{e(c["use"])}</p>{ev}'
            f'<p class="last-review">Source checked {checked}</p>'
            f'<p class="card__foot"><a href="{e(c["url"])}" target="_blank" rel="noopener noreferrer" class="text-link">Official website ↗</a> · '
            f'<a href="{e(c["source"])}" target="_blank" rel="noopener noreferrer" class="text-link">Company updates ↗</a></p></article>')

def patch(path, fn):
    p = ROOT / path; s = p.read_text(encoding="utf-8"); n = fn(s)
    if n != s: p.write_text(n, encoding="utf-8")

def grid(region):
    group = sorted((c for c in companies if c["region"] == region), key=lambda c: c["name"].lower())
    def fn(s):
        a = s.index('id="company-grid">') + len('id="company-grid">'); b = s.index("</article></div>", a) + len("</article>")
        s = s[:a] + "".join(card(c) for c in group) + s[b:]
        return re.sub(r"\d+ organizations · search and explore", f"{len(group)} organizations · search and explore", s)
    patch(f"{'usa' if region == 'usa' else 'international'}.html", fn)

def bars(counter):
    top = max(counter.values())
    return "".join(f'<div class="bar-row"><div class="bar-label"><span>{e(k)}</span><span>{v}</span></div><div class="bar-track"><div class="bar-fill" style="width:{round(100*v/top)}%"></div></div></div>'
                   for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])))

def visuals(s):
    usa = sum(c["region"] == "usa" for c in companies); intl = len(companies) - usa
    stats = "".join(f'<div class="stat"><p class="n">{n}</p><p class="l">{l}</p></div>' for n, l in
                    [(len(companies), "Organizations"), (usa, "U.S.-based"), (intl, "International"), (len(news_doc["news"]), "Curated stories")])
    s = re.sub(r'<div class="stats">.*?</div></div></div></section>', f'<div class="stats">{stats}</div></div></section>', s, count=1, flags=re.S)
    focus = bars(Counter(c["focus"] for c in companies))
    kinds = Counter("Public company" if m["status"] == "Public" else "Private / filing status to verify" for m in markets_doc["markets"])
    by_month = Counter(n["date"][:7] for n in news_doc["news"]); by_type = Counter({"company": "Company announcement", "report": "Independent reporting"}.get(n["type"], n["type"]) for n in news_doc["news"])
    sections = (f'<section><div class="container"><p class="eyebrow">Coverage breakdown</p><h2 class="section-title">Areas covered.</h2><div class="surface-panel">{focus}</div>'
                f'<p class="last-review">Counts cover included organizations only. Counts of tracked organizations are not a measure of market size.</p></div></section>'
                f'<section><div class="container"><p class="eyebrow">Tracked organizations</p><h2 class="section-title">By region and by listing status.</h2><div class="surface-panel">'
                f'{bars(Counter({"U.S.-based": usa, "International": intl}))}</div><div class="surface-panel">{bars(kinds)}</div>'
                f'<p class="last-review">Listing status is from the Markets page watchlist ({len(markets_doc["markets"])} entries), checked {markets_doc["updated"]}. Verify against exchanges and SEC filings.</p></div></section>'
                f'<section><div class="container"><p class="eyebrow">News coverage</p><h2 class="section-title">Curated stories by month and label.</h2><div class="surface-panel">{bars(by_month)}</div><div class="surface-panel">{bars(by_type)}</div>'
                f'<p class="last-review">Counts of curated stories only, not of all AI news. Planned: usage, funding and valuation charts once reliable, dated datasets exist.</p></div></section>')
    return re.sub(r'<section><div class="container"><p class="eyebrow">Coverage breakdown</p>.*?</section>', lambda m: sections, s, count=1, flags=re.S)

grid("usa"); grid("international"); patch("visuals.html", visuals)
print(f"Rebuilt trackers: {len(companies)} organizations, {len(news_doc['news'])} stories")
