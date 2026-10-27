# GoldBrief identity

## Logo

The primary mark is the **left-facing briefcase** from the logo handoff: an upright document case seen slightly from above and from the viewer's left, one light seam turning round the left edge, handle integrated. The approved graphite master is preserved untouched in `assets/brand/`; the site uses a vector redrawn from the same geometry by `scripts/build_brand.py`.

| File | Use |
| --- | --- |
| `assets/goldbrief-mark.svg` / `.png` (512) | Header and drawer mark (transparent yellow, detailed) |
| `assets/favicon.svg` | Browser tab icon: black tile, yellow case, bolder seam for small sizes |
| `assets/favicon.ico`, `favicon-16/32/48.png` | Legacy and fixed-size favicons |
| `assets/apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `site.webmanifest` | Home-screen and PWA icons (full-bleed black) |
| `assets/brand/` | Handoff originals: transparent PNGs (master, 1024/512/256/128), white-background preview, gradient schematics |

**Rules.** The mark is **yellow on black**, matching the site: case in the site's gold-yellow gradient `#FFF45C` → `#FFE81A` → `#D4C200`, top-plane highlight `#FFF9B0`, seam cut out in the site black `#050504`. The favicon and touch icons use a black tile `#050504`. This replaces the handoff's graphite-on-light treatment, which does not work on the black site; the original graphite files stay untouched in `assets/brand/` for light-background uses (print, white documents). Do not stretch or rotate the mark; keep clear space of at least one eighth of its width. Keep the wordmark as live HTML text.

**Palette.** Site yellow as above on black. From the handoff's schematics, Obsidian `#30343A` → `#191C20` → `#080A0D` applies only to the graphite version on light backgrounds; Gold signal and Platinum remain unused options.

**Status.** The vector is a hand-built redraw for review, not an auto-trace. Before final launch, check it in the real header and as a favicon at 128, 64 and 32 px and on high-DPI screens. Regenerate every icon with `python3 scripts/build_brand.py`.

## Two font system

| Role | Family | Use |
| --- | --- | --- |
| Display | Outfit, weights 500–800 | Wordmark, headlines, page and section titles |
| Reading | Inter, weights 400–700 | Story summaries, navigation, tables, forms, dates, labels |

Outfit gives the masthead and headlines broad geometric forms similar in spirit to the SAKI reference. Inter keeps dense news and directory text clear. Labels and dates use Inter with spacing or tabular numerals where useful; avoid introducing a third monospace family. Both families are served with `font-display: swap` through Google Fonts and have Helvetica/Arial fallbacks if the request fails. The underlying fonts are available under the SIL Open Font License.

The source of truth for families is `css/tokens.css`. Keep the logo readable at 30 px in the mobile header, and do not turn the wordmark into an image.
