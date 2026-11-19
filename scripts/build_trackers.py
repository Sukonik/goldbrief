#!/usr/bin/env python3
"""Regenerate company cards, counts and Visuals charts in the static pages from data/*.json.

Run after editing data/companies.json, data/news.json or data/markets.json:
    python3 scripts/build_trackers.py
Only counts that can be derived from the datasets are produced; nothing is estimated.
"""
import datetime as dt, html, json, re
from collections import Counter
from pathlib import Path
from zoneinfo import ZoneInfo
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
                f'<p class="last-review">Listing status is from the Markets page watchlist ({len(markets_doc["markets"])} entries), last checked {max(m["checked"] for m in markets_doc["markets"])} (oldest entry {min(m["checked"] for m in markets_doc["markets"])}). Verify against exchanges and SEC filings.</p></div></section>'
                f'<section><div class="container"><p class="eyebrow">News coverage</p><h2 class="section-title">Curated stories by month and label.</h2><div class="surface-panel">{bars(by_month)}</div><div class="surface-panel">{bars(by_type)}</div>'
                f'<p class="last-review">Counts of curated stories only, not of all AI news. Planned: usage, funding and valuation charts once reliable, dated datasets exist.</p></div></section>')
    return re.sub(r'<section><div class="container"><p class="eyebrow">Coverage breakdown</p>.*?(?=</main>)', lambda m: sections, s, count=1, flags=re.S)

REFRESH_ICON = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" focusable="false"><path d="M20 12a8 8 0 1 1-2.34-5.66M20 4v5h-5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def et(iso):
    t = dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(ZoneInfo("America/New_York"))
    return t.strftime("%b %-d, %-I:%M %p") + " ET"

def led(m, quotes):
    t = m.get("quote_ticker")
    if not t:
        return '<p class="led-note">Private company: no public share price.</p>'
    q = quotes.get(t)
    if q:
        val = f'${q["price"]:,.2f}'; ghost = re.sub(r"\d", "8", val)
        attrs = f'data-price="{q["price"]}" data-updated="{e(q["updated"])}" data-source="{e(q["source"])}"'
        asof = f'<span class="led__asof">Updated {et(q["updated"])}</span>'; src = f'{e(q["source"])} via Payout Lab · delayed, not live'
    else:
        val, ghost, attrs = "– – –", "$888.88", 'data-price="" data-updated="" data-source=""'
        asof = '<span class="led__asof">Not in Payout Lab data yet</span>'; src = "No delayed price available"
    return (f'<div class="led" data-ticker="{e(t)}" {attrs}><div class="led__top"><span class="led__sym">{e(t)}</span>'
            f'<button type="button" class="led__refresh" aria-label="Refresh price for {e(t)}" title="Refresh {e(t)}">{REFRESH_ICON}</button></div>'
            f'<div class="led__display"><span class="led__ghost" aria-hidden="true">{ghost}</span><span class="led__value">{val}</span></div>'
            f'<p class="led__meta">{asof} <span class="led__age"></span></p><p class="led__src">{src}</p></div>')

def markets(s):
    ms = markets_doc["markets"]
    qdoc = json.loads((ROOT / "data" / "quotes.json").read_text(encoding="utf-8")) if (ROOT / "data" / "quotes.json").exists() else {"quotes": {}}
    cards = "".join(
        f'<article class="card"><p class="card__meta">{e(m["status"])}' + (f' · {e(m["note"])}' if m.get("note") else "") + f'</p><h3>{e(m["name"])}</h3>'
        f'<p>{e(m["ticker"])} · {e(m["exchange"])}</p><p>{e(m["focus"])}</p>{led(m, qdoc["quotes"])}<p class="last-review">Status checked {e(m["checked"])}</p>'
        f'<p class="card__foot"><a href="{e(m["source"])}" target="_blank" rel="noopener noreferrer" class="text-link">Official source ↗</a></p></article>' for m in ms)
    bar = ('<div class="ticker-bar"><button type="button" class="btn" data-variant="solid" id="fetch-quotes">' + REFRESH_ICON + '<span>Fetch market data</span></button>'
           '<p id="quote-status" class="ticker-bar__status" role="status" aria-live="polite">Prices are delayed snapshots from <a class="text-link" href="https://github.com/Sukonik/payout-lab" target="_blank" rel="noopener noreferrer">Payout Lab</a> '
           '(unofficial Yahoo Finance data), not live quotes. Each price shows when it was last updated; press the button for the newest file.</p></div>')
    ups = ""
    for u in markets_doc.get("updates", []):
        ups += (f'<section><div class="container"><p class="eyebrow">Market update · {e(u["date"])}</p><h2 class="section-title">{e(u["headline"])}.</h2>'
                f'<div class="surface-panel"><dl class="facts">' + "".join(f'<div class="facts__row"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in u["facts"]) + '</dl></div>'
                f'<p class="last-review"><b>Sources:</b> ' + " · ".join(f'<a class="text-link" href="{e(x["url"])}" target="_blank" rel="noopener noreferrer">{e(x["label"])} ↗</a>' for x in u["sources"]) + '</p>'
                f'<p class="last-review">{e(u["verification"])}</p></div></section>')
    tl = markets_doc.get("timeline")
    tls = ""
    if tl:
        tls = (f'<section><div class="container"><p class="eyebrow">Learn / IPOs</p><h2 class="section-title">{e(tl["title"])}.</h2><p class="lede">{e(tl["note"])}</p>'
               '<ol class="steps-list">' + "".join(f'<li><b>{e(d)}.</b> {e(t)}</li>' for d, t in tl["steps"]) + '</ol></div></section>')
    main = ('<main id="main"><section class="hero"><div class="container"><p class="eyebrow">Markets / IPOs</p><h1 class="display">Follow the money.<br><span class=\'neon\'>Check the filings.</span></h1>'
            '<p class="lede">Company status is not a share-price feed. Rumors, filings and actual stock listings must be distinguished.</p></div></section>'
            + f'<section><div class="container"><p class="eyebrow">Reference companies</p><h2 class="section-title">Public, private and IPO-related.</h2>{bar}<div class="grid">{cards}</div>'
            f'<p class="last-review">{e(markets_doc["note"])} Last compiled {e(markets_doc["updated"])}.</p></div></section>' + tls +
            '<section><div class="container"><p class="eyebrow">Learn / IPOs</p><h2 class="section-title">Rumor is not a listing.</h2><p class="lede">A report about a possible IPO, a filed registration statement and an exchange-listed stock are three different stages. Consult <a href="https://www.sec.gov/edgar/search/" target="_blank" rel="noopener noreferrer" class="text-link">SEC EDGAR ↗</a> before acting.</p></div></section>' + ups + '</main>')
    s = re.sub(r'<main id="main">.*?</main>', lambda m: main, s, count=1, flags=re.S)
    return s if 'js/ticker.js' in s else s.replace('<script defer src="js/main.js"></script>', '<script defer src="js/main.js"></script><script defer src="js/ticker.js"></script>')

grid("usa"); grid("international"); patch("visuals.html", visuals); patch("markets.html", markets)
print(f"Rebuilt trackers: {len(companies)} organizations, {len(news_doc['news'])} stories")
