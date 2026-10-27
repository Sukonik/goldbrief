# GoldBrief identity

## Logo

The primary mark is a spare circuit brain: a brain outline, central seam, and six short signal traces. It suggests understanding and connected reporting without imitating the dense circuitry of the reference image. The dark field and restrained outline match the site palette. It is drawn as vector paths and remains legible at favicon size.

- `assets/goldbrief-mark.svg`: primary icon for the header, sharing, and artwork.
- `assets/favicon.svg`: compact browser icon using the same geometry.
- `assets/goldbrief-mark.png`: 512 px export for places that do not support SVG.
- `assets/goldbrief-briefcase-concept.svg`: alternate literal briefcase concept, retained for comparison.
- Header lockup: icon followed by the live text **GoldBrief**, with “Brief” in the site accent. Keep this as HTML text so it remains sharp and accessible at any viewport width.

Keep clear space around the mark equal to at least one eighth of its width. Do not add a glow inside the icon, bevel the letters, or use the icon as a source of article imagery. The small mark uses flat color; the site can reserve luminous effects for selected calls to action. Avoid adding more circuit branches, which would blur at favicon scale.

## Two font system

| Role | Family | Use |
| --- | --- | --- |
| Display | Space Grotesk, weights 500–700 | Wordmark, headlines, page and section titles |
| Reading | Inter, weights 400–700 | Story summaries, navigation, tables, forms, dates, labels |

Space Grotesk gives the masthead and headlines a recognizable technical character. Inter keeps dense news and directory text clear. Labels and dates use Inter with spacing or tabular numerals where useful; avoid introducing a third monospace family. Both families are served with `font-display: swap` through Google Fonts and have Helvetica/Arial fallbacks if the request fails. The underlying fonts are available under the SIL Open Font License.

The source of truth for families is `css/tokens.css`. Keep the logo readable at 30 px in the mobile header, and do not turn the wordmark into an image.
