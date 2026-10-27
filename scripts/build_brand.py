#!/usr/bin/env python3
"""Generate the GoldBrief mark SVGs and the favicon set (PNG sizes, ICO, manifest).

Geometry is the left-facing briefcase from the logo handoff (source coordinates 1494x1053,
mapped by one transform). Needs node + `playwright` + chromium (scripts/render_svg.js) and Pillow. Run: python3 scripts/build_brand.py
"""
import io, json, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; A = ROOT / "assets"
IVORY = "#F4F1E9"
# map handoff source coords (content bbox ~213..1315 x 130..1000) into a 128 box
XF = "translate(-5.3 14.2) scale(.0907)"
DEFS = ('<defs><linearGradient id="obs" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#30343A"/><stop offset=".48" stop-color="#191C20"/><stop offset="1" stop-color="#080A0D"/></linearGradient></defs>')
BODY = "M240 335 L1200 215 L1295 250 L1310 272 L1310 745 L1285 790 L345 985 L225 870 L215 355 Z"
HANDLE = "M545 305 V192 Q545 152 582 148 L985 108 Q1018 106 1018 140 V272 L905 282 V214 Q905 200 892 201 L668 226 Q652 228 652 244 V312 Z"
def art(detail):
    seam_w = 16 if detail else 30
    s = (f'<g transform="{XF}" stroke-linejoin="round">'
         f'<path d="{BODY}" fill="url(#obs)" stroke="url(#obs)" stroke-width="26"/>'
         f'<path d="{HANDLE}" fill="url(#obs)" stroke="url(#obs)" stroke-width="22"/>')
    if detail:  # lighter top plane, as in the approved master
        s += '<path d="M245 330 L1195 214 L1288 249 L1296 262 L1286 268 L1190 236 L262 346 Z" fill="#3A3F46"/>'
    s += f'<path d="M215 505 Q226 556 310 554 L1312 428" fill="none" stroke="#F3F4F4" stroke-width="{seam_w}" stroke-linecap="round"/></g>'
    return s
def svg(inner, label, tile=False):
    bg = f'<rect width="128" height="128" rx="16" fill="{IVORY}"/>' if tile else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" role="img" aria-labelledby="t"><title id="t">{label}</title>{DEFS}{bg}{inner}</svg>\n')
(A / "goldbrief-mark.svg").write_text(svg(art(True), "GoldBrief briefcase mark"))
(A / "favicon.svg").write_text(svg(art(False), "GoldBrief", tile=True))

def render(svg_text, size):
    with tempfile.TemporaryDirectory() as d:
        src, out = Path(d) / "in.svg", Path(d) / "out.png"; src.write_text(svg_text)
        subprocess.run(["node", str(ROOT / "scripts/render_svg.js"), str(src), str(out), str(size)], check=True, cwd=ROOT)
        return out.read_bytes()
fav = (A / "favicon.svg").read_text(); mark = (A / "goldbrief-mark.svg").read_text()
(A / "goldbrief-mark.png").write_bytes(render(mark, 512))
for n in (16, 32, 48): (A / f"favicon-{n}.png").write_bytes(render(fav, n))
# full-bleed ivory square for touch icons (the OS rounds the corners)
bleed = fav.replace('rx="16"', 'rx="0"')
(A / "apple-touch-icon.png").write_bytes(render(bleed, 180)); (A / "icon-192.png").write_bytes(render(bleed, 192)); (A / "icon-512.png").write_bytes(render(bleed, 512))
from PIL import Image
imgs = [Image.open(io.BytesIO((A / f"favicon-{n}.png").read_bytes())).convert("RGBA") for n in (48, 32, 16)]
imgs[0].save(A / "favicon.ico", sizes=[(48, 48), (32, 32), (16, 16)], append_images=imgs[1:])
(ROOT / "site.webmanifest").write_text(json.dumps({"name": "GoldBrief | AI Explained", "short_name": "GoldBrief", "start_url": "./", "display": "standalone",
    "background_color": IVORY, "theme_color": "#050504",
    "icons": [{"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png"},
              {"src": "assets/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, indent=2) + "\n")
print("Brand assets built")
