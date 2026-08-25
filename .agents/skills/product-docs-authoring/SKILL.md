---
name: product-docs-authoring
description: Author or edit Extole customer-facing documentation in this repo (product-docs on Mintlify). Use when creating a new page, editing an existing one, converting a draft/.docx into a page, or addressing reviewer comments on a PR. Covers the authoring workflow, docs.json nav placement, the pre-PR self-review, and the PR flow. Writing standards themselves live in .mintlify/AGENTS.md.
---

# Product-docs authoring

This repo is Extole's customer-facing documentation, built on **Mintlify**. This skill is
the **process**: how a change gets written, placed in navigation, checked, and merged.

**The writing standards are not in this skill.** Voice, terminology, structure, formatting,
links, images, frontmatter, and accuracy all live in one self-contained file:
[`.mintlify/AGENTS.md`](../../../.mintlify/AGENTS.md). Read it before your first edit. It is
canonical because Mintlify's own agent reads it directly and cannot follow links — so a
standard stated anywhere else is one that some editing surface silently ignores.

Preview and validation mechanics: [`mintlify-branch-preview`](../mintlify-branch-preview/SKILL.md).

## When to use

- Creating a new page, or converting a supplied draft or `.docx` into a page.
- Editing an existing page — wording, restructure, correction.
- Addressing reviewer comments on a PR (see **Reviewer comments** below).

## Read this before your first edit: this repo is docs.extole.com

**This repo is the source of truth for the live customer documentation.** `main` publishes
docs.extole.com through Mintlify, so an edit here reaches customers on merge. Edit pages
directly and normally.

The pages were originally produced by
[`scripts/convert_from_product_docs.py`](../../../scripts/convert_from_product_docs.py)
from the ReadMe corpus that used to publish the site. That converter is history, not a pipeline: it is
kept for provenance and must not be re-run over hand-edited pages, because it would
overwrite them. `extole/product-docs-readme` is the ReadMe-based predecessor; it no longer
publishes docs.extole.com.

## Repo layout and pipeline

- Pages: `<tab>/<group>/…/<slug>.mdx`. Customer-visible content lives in **`guides/`**,
  **`product/`**, **`technical/`**, **`news/`**, and **`runbooks/`**; **`api-reference/`**
  holds the OpenAPI bundles.
- **Navigation** lives in [`docs.json`](../../../docs.json) under
  `navigation.tabs[] → groups[] → pages[]`. A page entry is its path **without** the `.mdx`
  extension (`guides/audiences-and-segmentation/advocate-tiers`). Groups nest, and a group
  whose landing page is a page of its own carries `"root": "<path>/index"`. **A new page is
  invisible until its path is added to `docs.json`** — add it in the right position.
  Nothing enforces this: a page missing from `docs.json` passes `mint validate`, passes CI,
  and ships unreachable. It is a review responsibility.
- **API reference is generated.** Mintlify renders the entire reference from
  `api-reference/*.json`, and `docs.json` lists endpoints as `METHOD /path` strings. Those
  bundles are written by CI from [`extole/openapi`](https://github.com/extole/openapi)
  (`sync-to-mintlify.yml`), which extracts them from pluribus. Leave them and the API
  Reference tab alone unless that is the task.
- **Published vs. not:** the content directories are customer-visible. `.agents/` and
  `.claude/` are excluded by Mintlify's built-in ignores, `.mintlify/` is never served, and
  `.cursor/` plus the repo-root agent files are excluded by
  [`.mintignore`](../../../.mintignore). Note that Mintlify's built-in ignores do **not**
  cover repo-root Markdown: an un-ignored `AGENTS.md` at the root is served publicly at
  `/agents.md`.
- **Deployment:** merging to `main` deploys **docs.extole.com** — the live customer site,
  so treat a merge as a publish. The Mintlify GitHub App also builds a preview deployment
  per PR and comments the link; see `mintlify-branch-preview` for what to do when it
  doesn't.
- **Agent reads:** the AI assistants read this documentation through `extole_docs_search` /
  `extole_docs_get` — the published site for `main`, and for any other branch the branch's
  own `docs.json` navigation and `.mdx` sources read straight from this repository. A
  pushed branch is therefore queryable by an agent immediately, with no preview build; a
  page missing from `docs.json` navigation is fetchable by exact path but never appears in
  search.

## Authoring workflow

1. **Ground first.** Read [`.mintlify/AGENTS.md`](../../../.mintlify/AGENTS.md). If the
   topic is unfamiliar, research prior framing and the correct product terms in parallel
   with reading neighbouring pages in the same group, and match their structure.
2. **Write to the standard as you go.** Everything in `.mintlify/AGENTS.md` applies while
   you write — terminology, imperative how-to, Title Case, de-hedging, navigation bolding,
   number rules, callout components. Do not leave these for the reviewer.
3. **Place in nav.** Add the page path to the right group in `docs.json`.
4. **Validate.** `npx mint@latest validate` must report **0 errors, 0 warnings**. MDX is
   JSX-strict: a broken tag fails the whole build, not just the page, and `validate` treats
   a warning as a failure. `npx mint@latest dev` renders it locally at
   http://localhost:3000. CI runs the same command on every PR as the required
   **`validate`** check, so this is a gate you clear before review, not after.
5. **Self-review** against the checklist below, then open the PR.

## Self-review checklist

Derived from repeated reviewer feedback — clearing these is the point of this skill. Each
item checks conformance to `.mintlify/AGENTS.md` rather than restating it.

- [ ] **Terminology** matches the glossary, and is consistent throughout — the same concept
      is never spelled or cased two ways on one page.
- [ ] **No hedging or filler** — swept against the de-hedge list.
- [ ] **Title and headings** in Title Case; real `##` headings, not bold lines.
- [ ] **Imperative** how-to steps; reader addressed as "you".
- [ ] **Navigation paths and UI elements** bolded, not quoted.
- [ ] **Numbers, units, spelling** follow the standard.
- [ ] **Accuracy** — wording matches actual product behavior and current UI labels and
      status text; no invented values.
- [ ] **Frontmatter** present (`title`, `description`); **page path added to `docs.json`**.
- [ ] **Links and images resolve** — internal links are site paths, images are
      root-relative repo assets, no `doc:slug` and no remote `expires=` URL.
- [ ] **Literals** — event names, schema fields, and API identifiers left verbatim.
- [ ] **Open decisions** matched to the surrounding page, not silently standardized.
- [ ] **`npx mint@latest validate` is clean** (0 errors, 0 warnings).

## Reviewer comments

To read and resolve inline PR comments — the common "apply the reviewer's suggestions" task:

- List them: `gh api repos/extole/product-docs/pulls/<n>/comments --jq '.[] | {path,line:(.line//.original_line),body,id}'`.
- Apply straightforward suggestions directly, correcting obvious typos in the suggestion
  text; **surface genuinely ambiguous ones to the user** instead of guessing.
- Resolve threads with the GraphQL `resolveReviewThread` mutation (REST cannot): fetch
  thread ids via `pullRequest.reviewThreads`, then mutate each.

## PR workflow

- The default branch is **`main`**. Branch from and target it. There is **no branch-name
  constraint** in this repo — the `v4.0.0_<slug>` prefix that `extole/product-docs-readme`
  requires for ReadMe mirroring means nothing here. Use a bare ticket id (`ENG-12345`) or a
  short kebab-case slug, matching the convention the tech repo uses.
- Doc changes end with an **open PR** (`gh pr create`), which is what produces the
  reviewable Mintlify preview. A docs-standards or terminology PR is a good candidate for
  **draft**, so the docs team can ratify wording before merge.
- Keep the PR scoped to docs. Don't touch `api-reference/` specs, `scripts/`, or
  `url-map.json` unless that is the task.

## Changing the standards themselves

Edit [`.mintlify/AGENTS.md`](../../../.mintlify/AGENTS.md). Do not add the rule to this
skill or to `product-docs-style.mdc` as well — a second copy is a copy that drifts, and
every surface except Claude Code and Cursor will only ever see the canonical file.
