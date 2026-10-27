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
    "resources": ("Resources", "AI resources", "Where to go next.", "Skills directories, free courses, data sources and accountability tools.", "data/resources.json"),
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

# Sync drawer + footer on every page.
names = [f.name for f in ROOT.glob("*.html")]
for name in names:
    p = ROOT / name; s = p.read_text(encoding="utf-8")
    if 'href="resources.html"><span class="mono">' not in s:
        item = lambda href, lab: f'<li><a class="nav-drawer__link" href="{href}"><span class="mono">00</span>{lab}</a></li>'
        s = s.replace('<li><a class="nav-drawer__link" href="trust.html">', item("resources.html", "Resources") + item("ui-ux.html", "UI/UX") + '<li><a class="nav-drawer__link" href="trust.html">', 1)
        n = iter(range(1, 100)); s = re.sub(r'(nav-drawer__link"[^>]*><span class="mono">)\d+', lambda m: f"{m.group(1)}{next(n):02d}", s)
    if 'class="site-footer__links"><a href="resources.html"' not in s and 'class="site-footer__links">' in s:
        s = s.replace('class="site-footer__links">', 'class="site-footer__links"><a href="resources.html">Resources</a><a href="ui-ux.html">UI/UX</a>', 1)
    p.write_text(s, encoding="utf-8")
print("Built resources.html and ui-ux.html; navigation synced on", len(names), "pages")
