# GoldBrief identity

## Logo

The primary mark is the **left-facing briefcase** from the logo handoff: an upright document case seen slightly from above and from the viewer's left, one light seam turning round the left edge, handle integrated. The approved graphite master is preserved untouched in `assets/brand/`; the site uses a vector redrawn from the same geometry by `scripts/build_brand.py`.

| File | Use |
| --- | --- |
| `assets/goldbrief-mark.svg` / `.png` (512) | Header and drawer mark (transparent, detailed) |
| `assets/favicon.svg` | Browser tab icon: ivory tile, bolder seam for small sizes |
| `assets/favicon.ico`, `favicon-16/32/48.png` | Legacy and fixed-size favicons |
| `assets/apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `site.webmanifest` | Home-screen and PWA icons (full-bleed ivory) |
| `assets/brand/` | Handoff originals: transparent PNGs (master, 1024/512/256/128), white-background preview, gradient schematics |

**Rules.** The mark is dark, so it always sits on the warm ivory field `#F4F1E9`, including in the dark header. Never place the dark master directly on the black header. Do not stretch or rotate it; keep clear space of at least one eighth of its width. Keep the wordmark as live HTML text.

**Palette (from the gradient schematics).** Obsidian `#30343A` → `#191C20` → `#080A0D` for the case body (used in the mark); seam `#F3F4F4`. Optional, not yet used: Gold signal `#FFF2C4` → `#D4A017` → `#8B5C18` for a seam or editorial accent only; Platinum `#F2F4F5` → `#BBC0C5` → `#717981` as an alternate seam. Keep the case body Obsidian in every variant.

**Status.** The vector is a hand-built redraw for review, not an auto-trace. Before final launch, check it in the real header at 128, 64 and 32 px on white and ivory, and on high-DPI screens. Regenerate every icon with `python3 scripts/build_brand.py`.

## Two font system

| Role | Family | Use |
| --- | --- | --- |
| Display | Outfit, weights 500–800 | Wordmark, headlines, page and section titles |
| Reading | Inter, weights 400–700 | Story summaries, navigation, tables, forms, dates, labels |

Outfit gives the masthead and headlines broad geometric forms similar in spirit to the SAKI reference. Inter keeps dense news and directory text clear. Labels and dates use Inter with spacing or tabular numerals where useful; avoid introducing a third monospace family. Both families are served with `font-display: swap` through Google Fonts and have Helvetica/Arial fallbacks if the request fails. The underlying fonts are available under the SIL Open Font License.

The source of truth for families is `css/tokens.css`. Keep the logo readable at 30 px in the mobile header, and do not turn the wordmark into an image.
