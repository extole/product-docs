---
name: product-docs-authoring
description: Author or edit Extole customer-facing documentation in this repo (product-docs → ReadMe → docs.extole.com) to house style. Use when creating a new page, editing an existing one, converting a draft/.docx into a page, or addressing reviewer comments on a PR. Applies the terminology glossary and style guide automatically, places the page in nav, and ends with a PR.
---

# Product-docs authoring

This repo is Extole's customer-facing documentation; pages publish to **docs.extole.com** through ReadMe. This skill is how to write or edit those pages so they land in house style the first time and need only substantive review.

Companion always-on rule: [`product-docs-style.mdc`](../../rules/product-docs-style.mdc) (the fixes to apply automatically). Term map: [`glossary.md`](glossary.md). Style reference: [`style-guide.md`](style-guide.md).

## When to use

- Creating a new page, or converting a supplied draft / `.docx` into a page.
- Editing an existing page (wording, restructure, correction).
- Addressing reviewer comments on a PR (see **Reviewer comments** below).

## Canonical sources (human-owned, cite them)

- **Extole Style Guide** and **Extole Content Strategy Outline** — Google Docs owned by the docs team. Source of truth for voice, grammar, capitalization, punctuation, and terminology. [`style-guide.md`](style-guide.md) is the agent-actionable distillation; when it and the Google Doc disagree, the Google Doc wins and the distillation should be updated.
- **Brand voice:** professional and informative, optimistic and encouraging, confident; client-centric, expert, clear and accessible. Educate the reader; don't oversell.

## Repo layout & pipeline

- Pages: `docs/<Category>/<slug>.md`. Top-level categories: **Guides**, **Product Docs**, **Technical Docs**.
- **Frontmatter** (YAML) on every page:
  ```yaml
  ---
  title: "Title Case Title"
  excerpt: "One or two sentences describing the page.\n"
  ---
  ```
- **Navigation** is an ordered `_order.yaml` per category (and at `docs/`): a plain list of page slugs (filename without `.md`) in display order. A new page is invisible in nav until its slug is added — add it in the right position.
- **Pipeline:** this repo → ReadMe.io sync → docs.extole.com. Changes merge via PR. The API reference (`reference/`) is a separate flow (`extole/openapi` → ReadMe), so leave `reference/` and API specs alone unless that's the task.
- **Published vs. not:** `docs/`, `reference/`, and `custom_pages/` are customer-visible. Repo-root files (`AGENTS.md`, this `.agents/` tree) are **not** published.

## Authoring workflow

1. **Ground first.** Read [`glossary.md`](glossary.md) and [`style-guide.md`](style-guide.md). If the topic is unfamiliar, research prior framing and the correct product terms in parallel with reading neighboring pages in the same category (match their structure).
2. **Structure.** Typical page: `# Overview` (what it is / why it matters — 262/461 pages open with one) → concept sections (`##`) → a how-to or decision section → an optional quick-reference table. Use real `##` headings, not bold-line pseudo-headings, so ReadMe builds the TOC. Title Case headings. Lead with the reader's goal. Internal links use `doc:slug`; images use Markdown `![]()`.
3. **Write to style automatically.** Apply everything in `product-docs-style.mdc` as you write — terminology, imperative how-to, cut hedging, Title Case, navigation bolding, number rules. Do not leave these for the reviewer.
4. **Respect literals.** Event names (`promotion clicked`, `signed up`, `converted`), field names, and API identifiers stay verbatim. "Tap not click" is for UI actions only.
5. **Never fabricate.** Do not invent event names, product behavior, or metrics to make prose flow. Verify against the platform (Extole MCP, existing docs) or mark it as needing confirmation.
6. **Place in nav.** Add the slug to the category `_order.yaml`.
7. **Self-review** against the checklist below, then open the PR.

## Self-review checklist (what reviewers consistently catch)

Derived from repeated review feedback — clearing these is the point of this skill:

- [ ] **Terminology** matches the glossary; "event" not "step"; consistent throughout (same concept never spelled/cased two ways).
- [ ] **No hedging or filler** — sweep for `just`, `simply`, `very`, `note that`, `please note`, `in order to`; no "related but different and should not be confused".
- [ ] **Title & headings** in Title Case; title reads as a benefit/goal where natural.
- [ ] **Imperative** how-to steps; reader addressed as "you".
- [ ] **Navigation** paths use bolded elements with `>`; UI elements bolded, not quoted.
- [ ] **Numbers, units, spelling** follow the style guide (American English; spell out ≤10; imperial units).
- [ ] **Accuracy** — wording matches actual product behavior and current UI labels/status text; no invented values.
- [ ] **Frontmatter** present (`title`, `excerpt`); **slug added to `_order.yaml`**.
- [ ] Literal event/field/API names left verbatim.

## Reviewer comments

To read and resolve inline PR comments (the common "apply the reviewer's suggestions" task):

- List them: `gh api repos/extole/product-docs/pulls/<n>/comments --jq '.[] | {path,line:(.line//.original_line),body,id}'`.
- Apply straightforward suggestions directly (correcting obvious typos in the suggestion text); **surface genuinely ambiguous ones to the user** instead of guessing.
- Resolve threads with the GraphQL `resolveReviewThread` mutation (REST cannot): fetch thread ids via `pullRequest.reviewThreads`, then mutate each.

## PR workflow

- The repo's default branch is **`v4.0.0`** (ReadMe versioning), not `master`; branch from and target it. Use the ticket id as the branch name when one is in scope, else `docs/<short-description>`.
- Doc changes end with an **open PR** (`gh pr create`). A docs-standards or terms-glossary PR is a good candidate for **draft** so the docs team can ratify wording before merge.
- Keep the PR scoped to docs; don't touch `reference/` or OpenAPI specs unless that is the task.
