# GoldBrief identity

## Logo

The primary mark is a flat black briefcase built from measured, slightly angled horizontal bars. The handle and top bar form one continuous shape, with the opening cut from the same geometry. There is no GB lettering. The vector sits on a warm ivory field in the dark header; the favicon uses the same field.

- `assets/goldbrief-mark.svg`: primary transparent vector icon for the header and artwork.
- `assets/favicon.svg`: browser icon with warm ivory backing.
- `assets/goldbrief-mark.png`: 512 px transparent export.
- Header lockup: icon followed by live text **GoldBrief**. Keep the wordmark as HTML text for sharpness and accessibility.

Keep clear space around the mark equal to at least one eighth of its width. Keep the single black color, angled bar rhythm, joined handle, and warm ivory field on dark surfaces. Avoid extrusion, gradients, outlines, or lettering inside the case.

## Two font system

| Role | Family | Use |
| --- | --- | --- |
| Display | Outfit, weights 500–800 | Wordmark, headlines, page and section titles |
| Reading | Inter, weights 400–700 | Story summaries, navigation, tables, forms, dates, labels |

Outfit gives the masthead and headlines broad geometric forms similar in spirit to the SAKI reference. Inter keeps dense news and directory text clear. Labels and dates use Inter with spacing or tabular numerals where useful; avoid introducing a third monospace family. Both families are served with `font-display: swap` through Google Fonts and have Helvetica/Arial fallbacks if the request fails. The underlying fonts are available under the SIL Open Font License.

The source of truth for families is `css/tokens.css`. Keep the logo readable at 30 px in the mobile header, and do not turn the wordmark into an image.
