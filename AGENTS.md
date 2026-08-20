# Extole product-docs — Agent Guide

This repo holds **Extole's customer-facing documentation**, built on **[Mintlify](https://mintlify.com)**. Read this before authoring or editing any page — it points to the standards every change must follow.

## Read first

Before you write or edit a doc, load the **product-docs-authoring** skill and the **product-docs-style** rule:

- Skill: [`.agents/skills/product-docs-authoring/SKILL.md`](.agents/skills/product-docs-authoring/SKILL.md) — the authoring workflow, page structure, `docs.json` nav, PR flow, and reviewer self-check.
- Skill: [`.agents/skills/mintlify-branch-preview/SKILL.md`](.agents/skills/mintlify-branch-preview/SKILL.md) — **load before creating any branch/PR**: how to get a rendered preview, and the `npx mint@latest validate` gate every change owes.
- Rule (always-on): [`.agents/rules/product-docs-style.mdc`](.agents/rules/product-docs-style.mdc) — the terminology and style fixes to apply automatically, in the same edit, before human review.
- Terms: [`.agents/skills/product-docs-authoring/glossary.md`](.agents/skills/product-docs-authoring/glossary.md) — preferred terms + open decisions.
- Style: [`.agents/skills/product-docs-authoring/style-guide.md`](.agents/skills/product-docs-authoring/style-guide.md) — voice, capitalization, formatting, links.

The canonical human-owned sources are the **Extole Style Guide** and **Content Strategy Outline** (Google Docs, docs-team owned); the files above are the agent-actionable distillation and defer to them.

## How agent config is wired (all tools)

- **Codex / Cursor** auto-read this `AGENTS.md`. Cursor also attaches `.cursor/rules/*` and `.cursor/skills/*`, which are symlinks to `.agents/rules` and `.agents/skills`.
- **Claude Code** reads [`CLAUDE.md`](CLAUDE.md), which `@`-imports this file and the always-on rule.
- Always-on standards live in `.agents/rules/*.mdc` (`alwaysApply: true`); repeatable workflows live in `.agents/skills/<name>/SKILL.md`.
- These standards came over from [`extole/product-docs-readme`](https://github.com/extole/product-docs-readme) — the ReadMe-based repo that still publishes docs.extole.com. Terminology, voice, and guardrails are unchanged; the platform mechanics (nav, links, callouts, images, frontmatter, branch naming, preview) are Mintlify's, not ReadMe's.

## Repo layout

| Path | Purpose |
|------|---------|
| `guides/`, `product/`, `technical/`, `news/` | Customer-visible pages — `.mdx` with YAML frontmatter (`title`, `description`). These are the four content tabs. |
| `docs.json` | Site config **and** the entire navigation (`navigation.tabs[] → groups[] → pages[]`). A page is unreachable until its path (no `.mdx`) is listed here. |
| `api-reference/*.json` | OpenAPI bundles from `extole/extole-specification`. Mintlify **generates** the whole API Reference tab from them — don't hand-edit. |
| `images/` | Page assets, referenced root-relative (`/images/…`). `images/extole-manifest.json` inventories the migrated ones. |
| `url-map.json` | Old-URL → new-path redirects; the converter emits them into `docs.json`. Add an entry whenever you rename or move a page. |
| `scripts/convert_from_product_docs.py` | The deterministic generator that produced these pages. See [`MIGRATION.md`](MIGRATION.md). |
| `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, `.cursor/` | Agent config — **not** published (`.agents`/`.claude` are Mintlify built-in ignores; `.cursor` is in `.mintignore`). |

## Tooling

- `npx mint@latest dev` — local preview at http://localhost:3000.
- `npx mint@latest validate` — strict build check; must be **0 errors, 0 warnings** before a PR.
- Mintlify MCP servers: `https://mcp.mintlify.com` to edit content and settings, `https://www.mintlify.com/docs/mcp` to query how to use Mintlify.

## Critical rules

1. **Follow the standards above for every doc change.** Apply the unambiguous terminology/style fixes automatically; don't leave them for the reviewer.
2. **Never invent product behavior, event names, or metrics.** Match the actual system; verify or flag when unsure.
3. **Keep literals verbatim** — event names (`promotion clicked`, `converted`), schema fields (`step_name`), and API identifiers are not style targets.
4. **The pages are generated, and this repo is the Mintlify canary.** A hand edit can be overwritten by a re-run of the converter, and merging here does **not** change docs.extole.com — ReadMe still serves it from `extole/product-docs-readme`. Decide, and state in the PR, whether you are authoring here or previewing a fix that belongs upstream.
5. **Default branch is `main`, with no branch-name requirement.** Do not carry over the `v4.0.0_<slug>` prefix that the ReadMe repo needs; here the rendered preview comes from the **PR**, not the branch name.
6. **MDX is JSX-strict.** A broken tag fails the whole build. Run `npx mint@latest validate` before opening the PR.
7. **Scope PRs to docs.** Don't touch `api-reference/` specs, `scripts/`, or `url-map.json` unless that's the task.

## Open decisions

Several house-style choices are still split across the corpus and awaiting docs-team ratification — see the end of [`glossary.md`](.agents/skills/product-docs-authoring/glossary.md) (client vs. customer, report-name formatting, "Refer A Friend" casing, "step" scope, Title vs. sentence case). Until decided, match the surrounding page and flag the inconsistency — don't pick a side.
