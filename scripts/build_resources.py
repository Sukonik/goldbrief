#!/usr/bin/env python3
"""Generate resources.html and ui-ux.html from data/resources.json and data/ui.json.

Also keeps the mobile drawer and footer links on every page in sync (idempotent).
Run: python3 scripts/build_resources.py
"""
import html, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
e = html.escape
SITE = "https://sukonik.github.io/goldbrief/"
PAGES = {
    "resources": ("Tools", "AI tools & resources", "Where to go next.", "Skills directories, free courses, data sources and accountability tools.", "data/resources.json"),
    "ui-ux": ("UI/UX", "UI/UX references", "Interfaces we learn from.", "Public GitHub design systems and component libraries behind our interface decisions.", "data/ui.json"),
}
shell = (ROOT / "visuals.html").read_text(encoding="utf-8")

def body(key):
    label, eyebrow, title, lede, data = PAGES[key]
    d = json.loads((ROOT / data).read_text(encoding="utf-8"))
    out = [f'<main id="main"><section class="hero"><div class="container"><p class="eyebrow">{e(eyebrow)}</p><h1 class="display">{e(title)}</h1><p class="lede">{e(lede)}</p></div></section>']
    out.append(f'<section><div class="container"><p class="result-count">{e(d["note"])}</p>')
    out.append('<div class="toolbar"><input class="field" type="search" id="res-search" placeholder="Search this page..." aria-label="Search this page"></div><p id="result-count" class="result-count" aria-live="polite"></p>')
    for g in d["groups"]:
        out.append(f'<h2 class="section-title">{e(g["name"])}</h2><div class="grid">')
        for i in g["items"]:
            note = f'<p class="last-review">{e(i["note"])}</p>' if i.get("note") else ""
            out.append(f'<article class="card" data-search="{e((i["name"] + " " + i["what"] + " " + g["name"]).lower())}"><h3>{e(i["name"])}</h3><p>{e(i["what"])}</p>{note}'
                       f'<p class="card__foot"><a class="text-link" href="{e(i["url"])}" target="_blank" rel="noopener noreferrer">{e(i["url"].split("//")[1].rstrip("/"))} ↗</a></p></article>')
        out.append("</div>")
    if d.get("principles"):
        out.append('<h2 class="section-title">How we use these</h2><div class="surface-panel"><ul>' + "".join(f"<li>{e(p)}</li>" for p in d["principles"]) + "</ul></div>")
    out.append(f'<p class="last-review">Last compiled {d["updated"]}. Spot an error or dead link? <a class="text-link" href="https://github.com/Sukonik/goldbrief/issues" target="_blank" rel="noopener noreferrer">Open an issue ↗</a></p></div></section></main>')
    return "".join(out)

for key, (label, eyebrow, title, lede, _) in PAGES.items():
    s = shell
    s = re.sub(r"<title>.*?</title>", f"<title>{e(label)} | GoldBrief · AI Explained</title>", s)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + e(lede), s)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + e(lede), s)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + f"{e(label)} | GoldBrief", s)
    s = s.replace("visuals.html", f"{key}.html").replace(' aria-current="page"', "")
    s = re.sub(r"<main id=\"main\">.*?</main>", lambda m: body(key), s, count=1, flags=re.S)
    s = s.replace("</body>", "") .replace("</html>", "")
    s += ('<script>(()=>{const i=document.getElementById("res-search"),n=[...document.querySelectorAll(".card[data-search]")],c=document.getElementById("result-count");'
          'if(!i)return;const r=()=>{const q=i.value.trim().toLowerCase();let v=0;n.forEach(x=>{const m=x.dataset.search.includes(q);x.hidden=!m;if(m)v++});c.textContent=v+" results"};i.addEventListener("input",r);r()})();</script></body></html>')
    (ROOT / f"{key}.html").write_text(s, encoding="utf-8")

# Sync header tabs, mobile drawer and footer on every page.
GROUPS = [  # (menu id, label, [(href, label, one-line description)])
    ("briefing", "Briefing", [("index.html", "Home", "Today's AI headlines"), ("lake.html", "Lake", "Related stories grouped by topic"), ("news.html", "News", "Sourced reporting, labeled by type")]),
    ("companies", "Companies", [("usa.html", "AI USA", "U.S.-based AI organizations"), ("international.html", "International", "AI organizations around the world"), ("leaderboards.html", "Leaderboards", "Activity we can verify")]),
    ("data", "Markets & Data", [("markets.html", "Markets", "Public companies and IPO watchlist"), ("visuals.html", "Visuals", "Charts from our own datasets")]),
    ("tools", "Tools", [("apps.html", "Apps", "Searchable AI apps and who they suit"), ("resources.html", "Tools & resources", "Skills directories, courses, data"), ("ui-ux.html", "UI/UX", "Public design systems we learn from")]),
    ("learn", "Learn", [("glossary.html", "Glossary", "AI terms in plain English"), ("encyclopedia.html", "Encyclopedia", "In-depth explainers"), ("index-directory.html", "Index", "A-Z of companies and topics")]),
    ("trust", "Trust", [("trust.html", "Editorial policy", "Sourcing, methods and corrections"), ("about.html", "About", "What GoldBrief is and why")]),
]
HEADER = [(h, l) for _, _, items in GROUPS for h, l, _ in items]
DRAWER = [("index.html", "Home"), ("lake.html", "Lake"), ("leaderboards.html", "Leaderboards"), ("usa.html", "AI USA"), ("international.html", "International"), ("visuals.html", "Visuals"), ("markets.html", "Markets"), ("apps.html", "Apps"), ("news.html", "News"), ("resources.html", "Tools"), ("ui-ux.html", "UI/UX"), ("index-directory.html", "Index"), ("glossary.html", "Glossary"), ("encyclopedia.html", "Encyclopedia"), ("trust.html", "Editorial policy"), ("about.html", "About")]
FOOTER = [("index-directory.html", "Index"), ("glossary.html", "Glossary"), ("encyclopedia.html", "Encyclopedia"), ("resources.html", "Tools"), ("ui-ux.html", "UI/UX"), ("trust.html", "Editorial policy")]
names = [f.name for f in ROOT.glob("*.html")]
for name in names:
    p = ROOT / name; s = p.read_text(encoding="utf-8")
    cur = lambda h: ' aria-current="page"' if h == name else ""
    def group(gid, label, items):
        here = any(h == name for h, _, _ in items)
        links = "".join(f'<a class="nav-panel__link" href="{h}"{cur(h)}><strong>{l}</strong><span>{d}</span></a>' for h, l, d in items)
        return (f'<li class="nav-group"><button type="button" class="nav__link nav-group__btn"{" data-here=\"true\"" if here else ""} aria-expanded="false" aria-controls="menu-{gid}">{label} <span aria-hidden="true" class="caret">▾</span></button>'
                f'<div class="nav-panel" id="menu-{gid}">{links}</div></li>')
    header = '<ul class="nav__list">' + "".join(group(*g) for g in GROUPS) + "</ul>"
    drawer = '<ul class="nav-drawer__list">' + "".join(f'<li><a class="nav-drawer__link" href="{h}"{cur(h)}><span class="mono">{i:02d}</span>{l}</a></li>' for i, (h, l) in enumerate(DRAWER, 1)) + "</ul>"
    s = re.sub(r'<ul class="nav__list">.*?</ul>', lambda m: header, s, count=1, flags=re.S)
    s = re.sub(r'<ul class="nav-drawer__list">.*?</ul>', lambda m: drawer, s, count=1, flags=re.S)
    foot = "".join(f'<a href="{h}">{l}</a>' for h, l in FOOTER) + '<a href="https://github.com/Sukonik/goldbrief/issues" target="_blank" rel="noopener noreferrer">Corrections ↗</a>'
    s = re.sub(r'(<nav class="site-footer__links">).*?(</nav>)', lambda m: m.group(1) + foot + m.group(2), s, count=1, flags=re.S)
    p.write_text(s, encoding="utf-8")
print("Built resources.html and ui-ux.html; navigation synced on", len(names), "pages")
