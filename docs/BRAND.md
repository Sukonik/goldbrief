# GoldBrief identity

## Logo

The primary mark is a flat line drawing of a briefcase with **GB** formed by simple strokes on the case front. Its uncluttered outline draws from the supplied reference while the initials give GoldBrief its own identity. The transparent mark sits directly on the dark header; the favicon uses the same drawing on a dark square.

- `assets/goldbrief-mark.svg`: primary transparent vector icon for the header and artwork.
- `assets/favicon.svg`: browser icon with a dark backing for contrast.
- `assets/goldbrief-mark.png`: 512 px transparent export for places that do not support SVG.
- Header lockup: icon followed by live text **GoldBrief**, with “Brief” in the site accent. Keep this as HTML text so it remains sharp and accessible at any viewport width.

Keep clear space around the mark equal to at least one eighth of its width. Do not add a glow, bevel, gradients, or extra case details. The mark uses one gold stroke color and a transparent field; the site can reserve luminous effects for selected calls to action.

## Two font system

| Role | Family | Use |
| --- | --- | --- |
| Display | Space Grotesk, weights 500–700 | Wordmark, headlines, page and section titles |
| Reading | Inter, weights 400–700 | Story summaries, navigation, tables, forms, dates, labels |

Space Grotesk gives the masthead and headlines a recognizable technical character. Inter keeps dense news and directory text clear. Labels and dates use Inter with spacing or tabular numerals where useful; avoid introducing a third monospace family. Both families are served with `font-display: swap` through Google Fonts and have Helvetica/Arial fallbacks if the request fails. The underlying fonts are available under the SIL Open Font License.

The source of truth for families is `css/tokens.css`. Keep the logo readable at 30 px in the mobile header, and do not turn the wordmark into an image.
