# Extole product-docs — Agent Guide

This repo holds **Extole's customer-facing documentation**. Pages publish to **docs.extole.com** through ReadMe. Read this before authoring or editing any page — it points to the standards every change must follow.

## Read first

Before you write or edit a doc, load the **product-docs-authoring** skill and the **product-docs-style** rule:

- Skill: [`.agents/skills/product-docs-authoring/SKILL.md`](.agents/skills/product-docs-authoring/SKILL.md) — the authoring workflow, page structure, nav, PR flow, and reviewer self-check.
- Rule (always-on): [`.agents/rules/product-docs-style.mdc`](.agents/rules/product-docs-style.mdc) — the terminology and style fixes to apply automatically, in the same edit, before human review.
- Terms: [`.agents/skills/product-docs-authoring/glossary.md`](.agents/skills/product-docs-authoring/glossary.md) — preferred terms + open decisions.
- Style: [`.agents/skills/product-docs-authoring/style-guide.md`](.agents/skills/product-docs-authoring/style-guide.md) — voice, capitalization, formatting, links.

The canonical human-owned sources are the **Extole Style Guide** and **Content Strategy Outline** (Google Docs, docs-team owned); the files above are the agent-actionable distillation and defer to them.

## How agent config is wired (all tools)

- **Codex / Cursor** auto-read this `AGENTS.md`. Cursor also attaches `.cursor/rules/*` and `.cursor/skills/*`, which are symlinks to `.agents/rules` and `.agents/skills`.
- **Claude Code** reads [`CLAUDE.md`](CLAUDE.md), which `@`-imports this file and the always-on rule.
- Always-on standards live in `.agents/rules/*.mdc` (`alwaysApply: true`); repeatable workflows live in `.agents/skills/<name>/SKILL.md`.

## Repo layout

| Path | Purpose |
|------|---------|
| `docs/` | Customer-visible pages, in categories **Guides**, **Product Docs**, **Technical Docs**. Publishes to docs.extole.com. |
| `reference/` | API reference — **generated** from `extole/openapi`. Don't hand-edit unless that's the task. |
| `custom_pages/` | Custom ReadMe pages. |
| `_order.yaml` (per category) | Ordered list of page slugs — sets sidebar order. A new page is invisible until its slug is added. |
| `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.cursor/` | Agent config — **not** published. |

## Critical rules

1. **Follow the standards above for every doc change.** Apply the unambiguous terminology/style fixes automatically; don't leave them for the reviewer.
2. **Never invent product behavior, event names, or metrics.** Match the actual system; verify or flag when unsure.
3. **Keep literals verbatim** — event names (`promotion clicked`, `converted`), schema fields (`step_name`), and API identifiers are not style targets.
4. **Default branch is `v4.0.0`** (ReadMe versioning), not `master`. Branch from and target it.
5. **Scope PRs to docs.** Don't touch `reference/` / OpenAPI specs unless that's the task.

## Open decisions

Several house-style choices are still split across the corpus and awaiting docs-team ratification — see the end of [`glossary.md`](.agents/skills/product-docs-authoring/glossary.md) (client vs. customer, report-name formatting, "Refer A Friend" casing, "step" scope, callout syntax, Title vs. sentence case). Until decided, match the surrounding page and flag the inconsistency — don't pick a side.
