---
name: product-docs-authoring
description: Author or edit Extole customer-facing documentation in this repo (product-docs on Mintlify) to house style. Use when creating a new page, editing an existing one, converting a draft/.docx into a page, or addressing reviewer comments on a PR. Applies the terminology glossary and style guide automatically, places the page in docs.json nav, validates the MDX build, and ends with a PR.
---

# Product-docs authoring

This repo is Extole's customer-facing documentation, built on **Mintlify**. This skill is how to write or edit those pages so they land in house style the first time and need only substantive review.

Companion always-on rule: [`product-docs-style.mdc`](../../rules/product-docs-style.mdc) (the fixes to apply automatically). Term map: [`glossary.md`](glossary.md). Style reference: [`style-guide.md`](style-guide.md). Preview and validation mechanics: [`mintlify-branch-preview`](../mintlify-branch-preview/SKILL.md).

## When to use

- Creating a new page, or converting a supplied draft / `.docx` into a page.
- Editing an existing page (wording, restructure, correction).
- Addressing reviewer comments on a PR (see **Reviewer comments** below).

## Canonical sources (human-owned, cite them)

- **Extole Style Guide** and **Extole Content Strategy Outline** — Google Docs owned by the docs team. Source of truth for voice, grammar, capitalization, punctuation, and terminology. [`style-guide.md`](style-guide.md) is the agent-actionable distillation; when it and the Google Doc disagree, the Google Doc wins and the distillation should be updated.
- **Brand voice:** professional and informative, optimistic and encouraging, confident; client-centric, expert, clear and accessible. Educate the reader; don't oversell.

## Read this before your first edit: this repo is docs.extole.com

**This repo is the source of truth for the live customer documentation.** `main` publishes docs.extole.com through Mintlify, so an edit here reaches customers on merge. Edit pages directly and normally.

The pages were originally produced by [`scripts/convert_from_product_docs.py`](../../../scripts/convert_from_product_docs.py) from the ReadMe corpus that used to publish the site — see [`MIGRATION.md`](../../../MIGRATION.md). That converter is history, not a pipeline: it is kept for provenance and must not be re-run over hand-edited pages, because it would overwrite them. `extole/product-docs-readme` is the ReadMe-based predecessor; it no longer publishes docs.extole.com.

## Repo layout & pipeline

- Pages: `<tab>/<group>/…/<slug>.mdx`. The four content tabs are **`guides/`**, **`product/`**, **`technical/`**, **`news/`**; **`api-reference/`** holds the OpenAPI bundles.
- **Frontmatter** (YAML) on every page:
  ```yaml
  ---
  title: "Title Case Title"
  description: "One or two sentences describing the page."
  ---
  ```
  `description` is Mintlify's field (the ReadMe corpus called it `excerpt`); it is what shows in search and social previews.
- **Navigation** lives in [`docs.json`](../../../docs.json) under `navigation.tabs[] → groups[] → pages[]`. A page entry is its path **without** the `.mdx` extension (`guides/audiences-and-segmentation/advocate-tiers`). Groups nest, and a group whose landing page is a page of its own carries `"root": "<path>/index"`. **A new page is invisible until its path is added to `docs.json`** — add it in the right position.
- **API reference is generated.** Mintlify renders the entire reference from `api-reference/*.json`, and `docs.json` lists endpoints as `METHOD /path` strings. Those specs come from `extole/extole-specification`; leave them and the API Reference tab alone unless that is the task.
- **Published vs. not:** the content tabs are customer-visible. `.agents/` and `.claude/` are excluded from the build by Mintlify's built-in ignores, and `.cursor/` is excluded by [`.mintignore`](../../../.mintignore); repo-root files like `AGENTS.md`, `MIGRATION.md`, and `README.md` are not published.
- **Deployment:** merging to `main` deploys **docs.extole.com** — that is the live customer site, so treat a merge as a publish. Mintlify's GitHub App also builds a preview deployment per PR, though previews have been observed missing on some PRs, so do not treat one as guaranteed.
- **Agent reads:** the AI assistants read this documentation through `extole_docs_search` / `extole_docs_get` — the published site for `main`, and for any other branch the branch's own `docs.json` navigation and `.mdx` sources read straight from this repository. A pushed branch is therefore queryable by an agent immediately, with no preview build; a page missing from `docs.json` navigation is fetchable by exact path but never appears in search.

## Authoring workflow

1. **Ground first.** Read [`glossary.md`](glossary.md) and [`style-guide.md`](style-guide.md). If the topic is unfamiliar, research prior framing and the correct product terms in parallel with reading neighboring pages in the same group (match their structure).
2. **Structure.** Typical page: `# Overview` (what it is / why it matters — 262/461 pages open with one) → concept sections (`##`) → a how-to or decision section → an optional quick-reference table. Use real `##` headings, not bold-line pseudo-headings, so Mintlify builds the on-page TOC. Title Case headings. Lead with the reader's goal.
3. **Use the Mintlify components the corpus already uses.** `<Info>` / `<Tip>` / `<Warning>` / `<Danger>` / `<Note>` for callouts (76 pages), `<Frame>` for a captioned or bordered image (17 pages), `<Accordion>` for collapsible detail (3 pages). Internal links are site paths (`/guides/…`); images are root-relative under `/images/`.
4. **Write to style automatically.** Apply everything in `product-docs-style.mdc` as you write — terminology, imperative how-to, cut hedging, Title Case, navigation bolding, number rules. Do not leave these for the reviewer.
5. **Respect literals.** Event names (`promotion clicked`, `signed up`, `converted`), field names, and API identifiers stay verbatim. Use "click" for UI actions (reserve "tap" for in-app placements and mobile SDK).
6. **Never fabricate.** Do not invent event names, product behavior, or metrics to make prose flow. Verify against the platform (Extole MCP, existing docs) or mark it as needing confirmation.
7. **Place in nav.** Add the page path to the right group in `docs.json`.
8. **Validate.** `npx mint@latest validate` must report **0 errors, 0 warnings** — MDX is JSX-strict and a broken tag fails the build, not just the page. `npx mint@latest dev` renders it locally at http://localhost:3000.
9. **Self-review** against the checklist below, then open the PR.

## Self-review checklist (what reviewers consistently catch)

Derived from repeated review feedback — clearing these is the point of this skill:

- [ ] **Terminology** matches the glossary; "event" not "step"; consistent throughout (same concept never spelled/cased two ways).
- [ ] **No hedging or filler** — sweep for `just`, `simply`, `very`, `note that`, `please note`, `in order to`; no "related but different and should not be confused".
- [ ] **Title & headings** in Title Case; title reads as a benefit/goal where natural.
- [ ] **Imperative** how-to steps; reader addressed as "you".
- [ ] **Navigation** paths use bolded elements with `>`; UI elements bolded, not quoted.
- [ ] **Numbers, units, spelling** follow the style guide (American English; spell out ≤10; imperial units).
- [ ] **Accuracy** — wording matches actual product behavior and current UI labels/status text; no invented values.
- [ ] **Frontmatter** present (`title`, `description`); **page path added to `docs.json`**.
- [ ] **Links and images resolve** — internal links are site paths, images are root-relative repo assets, no `doc:slug` and no remote `expires=` URL.
- [ ] **`npx mint@latest validate` is clean** (0 errors, 0 warnings).
- [ ] Literal event/field/API names left verbatim.

## Reviewer comments

To read and resolve inline PR comments (the common "apply the reviewer's suggestions" task):

- List them: `gh api repos/extole/product-docs/pulls/<n>/comments --jq '.[] | {path,line:(.line//.original_line),body,id}'`.
- Apply straightforward suggestions directly (correcting obvious typos in the suggestion text); **surface genuinely ambiguous ones to the user** instead of guessing.
- Resolve threads with the GraphQL `resolveReviewThread` mutation (REST cannot): fetch thread ids via `pullRequest.reviewThreads`, then mutate each.

## PR workflow

- The default branch is **`main`**. Branch from and target it. There is **no branch-name constraint** in this repo — the `v4.0.0_<slug>` prefix that `extole/product-docs-readme` requires for ReadMe mirroring means nothing here, so the tech repo's `tech-worktree-workflow` naming applies normally (a bare ticket id, or a short kebab-case slug). See [`mintlify-branch-preview`](../mintlify-branch-preview/SKILL.md).
- Doc changes end with an **open PR** (`gh pr create`), which is what produces the reviewable Mintlify preview. A docs-standards or terms-glossary PR is a good candidate for **draft** so the docs team can ratify wording before merge.
- Keep the PR scoped to docs; don't touch `api-reference/` specs, `scripts/`, or `url-map.json` unless that is the task.
