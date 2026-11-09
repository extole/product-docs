---
name: docs-site-design
description: Must be read before changing how docs.extole.com looks -- the theme in docs.json, style.css, public/style.css, the homepage -- and before reviewing how a page looks rather than what it says.
---

# Docs site design

How a page reads is [`.mintlify/AGENTS.md`](../../../.mintlify/AGENTS.md): callouts, `<Frame>`,
images, code and headings are standards there, and this skill does not restate them. This skill
covers the layer under the words, the theme and the two stylesheets, and the test a page has to pass
by eye: [`references/rubric.md`](references/rubric.md).

## Know which file styles what

| Area | Styled by | Its variables |
| --- | --- | --- |
| Mintlify's own chrome: nav, sidebar, links, buttons | `theme` and `colors` in [`docs.json`](../../../docs.json) | `colors.primary` |
| The homepage, the Developer Hub in [`index.mdx`](../../../index.mdx) | [`public/style.css`](../../../public/style.css) | `--extole-*` in `:root`, overridden for dark on `.extole-home` |
| API reference, the sandbox request dialog, the evaluatable widgets | [`style.css`](../../../style.css) | `--api-*` in `:root`, overridden on `html.dark` |

Change the file that owns the area, through its variables. Give every new color a dark-theme value
beside it in the same file. Never put a color, a font or an inline `style` in a page.

## Steps

1. **Read the page's words against `.mintlify/AGENTS.md` first.** Most "it looks wrong" on a content
   page is a callout, frame or heading standard broken there.
2. **Make a style change in the owning file**, from the table above, and nowhere else.
3. **Look at the result on a rendered preview**, light and dark, per
   [`mintlify-branch-preview`](../mintlify-branch-preview/SKILL.md). Read the computed font and
   colors in the browser rather than trusting the stylesheet: the font in the first item below
   proves why.
4. **Score it against [`references/rubric.md`](references/rubric.md).** Say the score and the
   weakest criterion when you hand it over.

## Observed, not yet decided

Open for the owner. Do not spread these into new work, and do not settle them in passing:

- **The homepage's monospace headings are not the font they name.** `--extole-heading-font` asks for
  `"PaperMono"`; Mintlify's `@font-face` registers `Paper Mono`, with a space, so those headings
  render in a fallback monospace. Whether the monospace look is the brand is the owner's call.
- **Two palettes.** The homepage is navy and coral; the API pages are warm stone with `#b3003a`.
- **The brand red `#ee0049` is below 4.5:1 as text**: 4.44:1 on white, 4.22:1 on the page
  background `#faf9f7`. Do not set body-size text in it. `--extole-slate` text is 3.12:1.
- **Poppins and Montserrat are named but never loaded.** The site loads only Inter and Paper Mono,
  so those names fall through to Inter.
