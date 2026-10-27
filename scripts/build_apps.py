#!/usr/bin/env python3
"""Regenerate the apps.html directory from data/apps.json. Run: python3 scripts/build_apps.py"""
import html, json, re
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
e = html.escape
d = json.loads((ROOT / "data/apps.json").read_text(encoding="utf-8"))
apps = d["apps"]
WATCH = {  # general cautions per category, not claims about any one product
 "Assistant": "Can state wrong things confidently. Check important facts; avoid pasting private or confidential data.",
 "Research": "Citations can be wrong or irrelevant. Open the source before relying on a claim.",
 "Coding": "Generated code can contain bugs and security holes. Review and test it; mind what code you upload.",
 "Images": "Check usage rights and each service's content rules. Generated images can show people or styles you should not publish.",
 "Video": "Realistic video can mislead. Do not generate real people without permission, and label synthetic media.",
 "Music": "Rights to commercial use differ by service and plan. Read the terms before publishing.",
 "Audio": "Voice cloning needs the speaker's consent. Be careful with recordings of other people.",
 "Meetings": "Recording and transcribing people often requires their consent. Know your local rules.",
 "Writing": "Do not submit AI-assisted text where it is prohibited, such as some schools and journals. You remain responsible for accuracy.",
 "Productivity": "These tools may access your files, email or calendar. Review permissions before connecting accounts.",
 "Design": "Check licensing for generated assets used in client or commercial work.",
 "Learning": "A tutor that sounds sure can still be wrong. Cross-check with course material.",
 "Characters": "Emotional attachment is real. Be cautious with personal information and with children's use.",
 "Developer": "Tools for building. Check licenses of models and data, and where your data is processed.",
 "Data": "Verify calculations and charts independently; spreadsheets uploaded may contain sensitive data.",
 "Accessibility": "Useful, but errors in descriptions can matter. Do not rely on one tool for safety-critical decisions.",
 "Creative": "Check usage rights and content rules for generated media.",
}
CHECK = [("What does it do?", "Read the product page, not just the name. Many apps do one thing well."),
         ("Who benefits?", "Look at the 'Best for' line, then try it on a real but low-stakes task."),
         ("Is there a free tier?", "Often, but limits change. Check the pricing page today."),
         ("What are the limits?", "Expect usage caps, errors and out-of-date knowledge. See the category caution on each section."),
         ("Do I need an account?", "Most do. Look for what personal data the sign-up asks for."),
         ("What about privacy?", "Check whether your inputs are stored or used for training, and whether you can opt out. We do not state privacy terms as fact.")]
cats = sorted({a["category"] for a in apps})
def card(a):
    us = a["country"] == "United States"
    search = e(f'{a["name"]} {a["company"]} {a["country"]} {a["category"]} {a["description"]} {a["best_for"]}'.lower())
    return (f'<article class="card company-card" data-search="{search}" data-category="{e(a["category"])}" data-region="{"us" if us else "intl"}">'
            f'<p class="card__meta">{e(a["category"])} · {e(a["company"])} · {e(a["country"])}</p><h3>{e(a["name"])}</h3>'
            f'<p>{e(a["description"])}</p><p><b>Best for:</b> {e(a["best_for"])}</p>'
            f'<p class="card__foot"><a href="{e(a["url"])}" target="_blank" rel="noopener noreferrer" class="text-link">Visit tool ↗</a></p></article>')
opts = "".join(f'<option value="{e(c)}">{e(c)} ({n})</option>' for c, n in sorted(Counter(a["category"] for a in apps).items()))
main = (f'<main id="main"><section class="hero"><div class="container"><p class="eyebrow">Apps / Everyday AI</p><h1 class="display">AI you can<br><span class=\'neon\'>actually use.</span></h1>'
        f'<p class="lede">{len(apps)} apps across {len(cats)} categories, from big firms and smaller developers, with plain-English notes on who each is for.</p></div></section>'
        f'<section><div class="container"><p class="eyebrow">Before you sign up</p><h2 class="section-title">Six questions for any AI app.</h2><div class="grid">'
        + "".join(f'<article class="card"><h3>{e(q)}</h3><p>{e(a)}</p></article>' for q, a in CHECK) +
        f'</div><p class="last-review">{e(d["note"])}</p></div></section>'
        f'<section><div class="container"><p class="eyebrow">Explore tools</p><h2 class="section-title">The applications directory.</h2>'
        f'<div class="toolbar"><input type="search" class="field" id="app-search" placeholder="Search apps, companies, uses..." aria-label="Search AI apps">'
        f'<select class="field" id="app-category" aria-label="Filter by category"><option value="all">All categories</option>{opts}</select>'
        f'<select class="field" id="app-region" aria-label="Filter by company location"><option value="all">All locations</option><option value="us">United States</option><option value="intl">Other countries</option></select></div>'
        f'<p id="result-count" class="result-count" aria-live="polite"></p><div id="app-grid" class="tracker-grid">' + "".join(card(a) for a in apps) + '</div></div></section>'
        f'<section><div class="container"><p class="eyebrow">Know the risks</p><h2 class="section-title">What to watch for, by category.</h2><div class="surface-panel"><ul>'
        + "".join(f'<li><b>{e(c)}:</b> {e(WATCH[c])}</li>' for c in cats if c in WATCH) +
        f'</ul></div><p class="last-review">Last compiled {d["updated"]}. A listing is not an endorsement. Suggest an app or report an error via <a class="text-link" href="https://github.com/Sukonik/goldbrief/issues" target="_blank" rel="noopener noreferrer">GitHub issues ↗</a>.</p></div></section></main>')
p = ROOT / "apps.html"; s = p.read_text(encoding="utf-8")
p.write_text(re.sub(r"<main id=\"main\">.*?</main>", lambda m: main, s, count=1, flags=re.S), encoding="utf-8")
missing = [c for c in cats if c not in WATCH]
print(f"Rebuilt apps.html: {len(apps)} apps, {len(cats)} categories", "missing cautions: " + ", ".join(missing) if missing else "")
