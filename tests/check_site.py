#!/usr/bin/env python3
"""GoldBrief deterministic, dependency-free structural QA, suitable for daily Actions."""
import json, re, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
pages=["index","resources","ui-ux","news","lake","leaderboards","usa","international","visuals","markets","apps","index-directory","glossary","encyclopedia","trust","about"]
files=[root/f"{p}.html" for p in pages]
assets=["css/tokens.css","css/base.css","css/components.css","css/responsive.css","css/goldbrief.css","js/main.js","assets/favicon.svg","assets/favicon.ico","assets/apple-touch-icon.png","assets/goldbrief-mark.svg","site.webmanifest"]
errors=[]
for f in files:
    if not f.exists():errors.append(f"Missing page: {f.name}");continue
    s=f.read_text(encoding="utf-8")
    if not all(x in s for x in ("<main", "</main>", "<h1", "</footer>", "viewport", "nav-toggle")):errors.append(f"Markup essentials missing: {f.name}")
    ids=re.findall(r'\bid="([^"]+)"',s)
    if len(ids)!=len(set(ids)):errors.append(f"Duplicate HTML ids: {f.name}")
    for u in re.findall(r'(?:href|src)="([^"]+)"',s):
        if not u or u.startswith(("http:","https:","mailto:","#","data:")):continue
        clean=u.split("?",1)[0].split("#",1)[0]
        if clean and not (root/clean).is_file():errors.append(f"{f.name}: missing link/asset: {clean}")
for p in assets:
    if not (root/p).is_file():errors.append("Missing local asset "+p)
for p in ["companies","news","apps","markets","glossary","encyclopedia","daily","resources","ui"]:
    try:
        x=json.loads((root/"data"/f"{p}.json").read_text())
        if not isinstance(x,dict):errors.append(f"Bad dataset type: {p}")
    except Exception as e:errors.append(f"Cannot load data/{p}.json: {e}")
style=(root/"css/goldbrief.css").read_text()
if "@media(max-width:1023px)" not in style:errors.append("Missing mobile single-nav breakpoint")
if "nav-drawer" not in (root/"js/main.js").read_text():errors.append("No mobile navigation controller")
print(json.dumps({"result":"FAIL" if errors else "PASS","pages":len(pages),"checked_files":len(files)+len(assets)+9,"errors":errors},indent=2))
sys.exit(1 if errors else 0)
