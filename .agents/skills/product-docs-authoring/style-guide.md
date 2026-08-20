# Extole product-docs style reference (agent distillation)

The agent-actionable subset of Extole's documentation style, for `extole/product-docs` (Mintlify). Pairs with [`glossary.md`](glossary.md) (terminology) and the [`product-docs-authoring`](SKILL.md) skill.

**Canonical sources (human-owned):** the **Extole Style Guide** and **Extole Content Strategy Outline** (Google Docs, owned by the docs team). This file distills the rules that recur in docs work and adds conventions observed in the live corpus. **Where a rule here conflicts with the Google Docs, the Google Docs win** — and this file should be updated to match. Two rules below were set from *observed corpus + reviewer practice* because they diverge from the 2014 draft guide; they are marked ⚑.

## Brand voice

Professional and informative, optimistic and encouraging, confident. Client-centric, expert, clear and accessible. Educate the reader about getting value from their referral programs; use industry language (event tracking, audience segmentation, real-time event streams) without slipping into internal jargon. Don't oversell; don't hunt for problems the reader didn't ask about.

## Voice & grammar

- **Second person, direct.** Address the reader as "you"; the corpus does this in 391/461 pages.
- **Imperative mood for how-to steps.** "Select **Reports**, then choose a date range." Not "You would then want to consider selecting…".
- **Contractions are fine** — the house register is conversational (you'll, don't, it's are used freely).
- **American English** spelling; **imperial** units (unless the doc is explicitly for an international audience).
- **Gender-neutral** language; a named hypothetical ("Jane referred her friend") is fine.
- **Be concise.** Cut padding, verbosity, and redundancy; replace a prepositional phrase with one word. See the de-hedge list in the glossary.

## Capitalization ⚑

- **Titles and section headings: Title Case.** This is the observed, enforced corpus convention (395/461 titles are Title Case; the reviewer's own title suggestion was Title Case). ⚑ It diverges from the 2014 draft guide's "sentence case / only proper nouns" rule — treat Title Case as the current house rule for headings and titles, pending docs-team confirmation.
- **Body text:** normal sentence capitalization. Capitalize proper nouns, product/report names, and acronyms; don't capitalize for emphasis.

## Structure

- **Overview first.** Open most pages with `# Overview` — what it is and why it matters (262/461 pages do). Often lead with a one-sentence definition that mirrors the frontmatter `description`.
- **Real headings.** Use `##`/`###`, not bold-line pseudo-headings, so Mintlify generates the on-page table of contents. ⚑ Some pages use bold lines — don't copy that.
- **Typical shape:** Overview → concept sections → how-to / decision section → optional quick-reference table.

## Formatting

- **Navigation paths:** bold each element, separated by `>`: `Navigate to **Reports** > **Metrics**`. Bold UI elements the reader acts on rather than quoting them (`Click **Logout**`, not `Click "LOGOUT"`).
- **Lists:** bullets for unordered items; numbered lists only when order matters. For item-plus-description, use a colon: `**Events**: a list of people who did an action.` Avoid nesting past two levels.
- **Numbers:** spell out ten and under; numerals for 11 and up. Exceptions kept as numerals: ranges, dates, times, measurements, percentages, currencies. Fractions spelled out and hyphenated.
- **Punctuation:** one space after a period. Em-dashes for sentence breaks; en-dashes for ranges/dichotomies; hyphens for compound modifiers. No trailing period when a sentence ends in a URL.
- **Tables:** standard GitHub pipe tables for reference material (journey types, quality states, field lists).
- **Emphasis / asides:** inline bold (`**Note**:`) for a short aside; for a real callout use a Mintlify component — `<Info>` (context), `<Tip>` (advice), `<Warning>` (caution), `<Danger>` (destructive/irreversible), `<Note>`. 76 pages already use them. Don't use an emoji-prefixed blockquote (`> 📘`) — that was ReadMe's syntax and renders as a plain quote here.

## Links & images

- **Internal links:** the page's site path, rooted at its tab — `[Advocate Tiers](/guides/audiences-and-segmentation/advocate-tiers)`. Not a relative `.mdx` path, and **not** ReadMe's `doc:slug` form: this repo is not on ReadMe, so a `doc:` link renders as literal text. The migration resolved 286 `doc:` links to real paths; keep it that way. If you rename or move a page, add an old-URL → new-path entry to `url-map.json` — the converter emits it as a `docs.json` redirect, so a regeneration cannot drop it.
- **External links:** plain Markdown — `[OpenCart Events](https://docs.opencart.com/developer-guide/events)`. ReadMe's `<Anchor label=… target="_blank">` widget does not exist in Mintlify; the migration converted the 7 files that used it to Markdown links, so don't reintroduce it. A host or endpoint shown as a value in backticks (`https://events.extole.io`) is not a link.
- **Images:** repo assets under `images/`, referenced root-relative — Markdown `![alt](/images/extole/….png)` or `<img src="/images/…" />`, wrapped in `<Frame>` when it wants a border or caption (17 pages do). Migrated images are content-addressed under `images/extole/` and inventoried in `images/extole-manifest.json`; add new ones to `images/` rather than hotlinking. ⚑ Never add a remote image URL with an `expires=` parameter — ~102 pages inherited rotting `intercom-attachments` links from the ReadMe corpus, which is the problem the local `images/` tree exists to end.

## Frontmatter

```yaml
---
title: "Title Case Title"
description: "One or two sentences describing the page."
---
```

`title` (required, quoted) and `description` (strongly recommended — Mintlify's field, and what the ReadMe corpus called `excerpt`) are the fields every page carries. Optional Mintlify fields include `sidebarTitle`, `icon`, `noindex`, and `mode`. Nav placement is **not** frontmatter here: add the page's path (no `.mdx`) to the right group in `docs.json`, or the page ships unreachable.

## Accuracy (non-negotiable)

Wording must match actual product behavior and current UI labels/status text — the reviewer repeatedly catches copy that drifts from what the system does (e.g. status strings, endpoint responses). Never invent event names, behavior, or metrics to make prose flow. When unsure, verify (Extole MCP, existing docs) or mark it for confirmation. Companion rules: `data-analysis-rules`, `never-fabricate-work`.
