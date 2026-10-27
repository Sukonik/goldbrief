# GoldBrief identity

## Logo

The primary mark is a dimensional briefcase built from five horizontal planes. Lit faces and receding edges give the restrained Piano rhythm depth without a GB monogram. The transparent vector sits on the dark header; the favicon includes a dark backing.

- `assets/goldbrief-mark.svg`: primary transparent vector icon for the header and artwork.
- `assets/favicon.svg`: browser icon with dark backing.
- `assets/goldbrief-mark.png`: 512 px transparent export.
- Header lockup: icon followed by live text **GoldBrief**. Keep the wordmark as HTML text for sharpness and accessibility.

Keep clear space around the mark equal to at least one eighth of its width. Keep the five-bar rhythm, warm gold face, and dark recessed sides. Avoid adding lettering inside the case or thin details that disappear at small sizes.

## Two font system

| Role | Family | Use |
| --- | --- | --- |
| Display | Outfit, weights 500–800 | Wordmark, headlines, page and section titles |
| Reading | Inter, weights 400–700 | Story summaries, navigation, tables, forms, dates, labels |

Outfit gives the masthead and headlines broad geometric forms similar in spirit to the SAKI reference. Inter keeps dense news and directory text clear. Labels and dates use Inter with spacing or tabular numerals where useful; avoid introducing a third monospace family. Both families are served with `font-display: swap` through Google Fonts and have Helvetica/Arial fallbacks if the request fails. The underlying fonts are available under the SIL Open Font License.

The source of truth for families is `css/tokens.css`. Keep the logo readable at 30 px in the mobile header, and do not turn the wordmark into an image.
