# Extole product-docs — Agent Guide

This repo holds **Extole's customer-facing documentation**, built on **[Mintlify](https://mintlify.com)**. Read this before authoring or editing any page — it points to the standards every change must follow.

## Read first

**Writing standards:** [`.mintlify/AGENTS.md`](.mintlify/AGENTS.md) — voice, terminology,
structure, formatting, links, images, frontmatter, accuracy. Every standard this repo
enforces is defined there, each stated in full, so writing to it needs no other file. Its
**Provenance** section covers where the standards come from and which copy wins.

**Process:**

- Skill: [`.agents/skills/product-docs-placement/SKILL.md`](.agents/skills/product-docs-placement/SKILL.md) — **load before writing a new page**: which tab and group the page belongs in. Guides is not the default.
- Skill: [`.agents/skills/product-docs-authoring/SKILL.md`](.agents/skills/product-docs-authoring/SKILL.md) — the authoring workflow, PR flow, and pre-PR self-review.
- Skill: [`.agents/skills/mintlify-branch-preview/SKILL.md`](.agents/skills/mintlify-branch-preview/SKILL.md) — **load before creating any branch/PR**: how to get a rendered preview, and the `npx mint@latest validate` gate every change owes.
- Rule (always-on): [`.agents/rules/product-docs-style.mdc`](.agents/rules/product-docs-style.mdc) — a short pointer to the standards file, plus three guardrails.

### Why the standards live in `.mintlify/`

Not every editing surface can follow a link. Mintlify's agent — the one behind the web
editor, the Slack bot, and the dashboard — reads `.mintlify/AGENTS.md` and **nothing else**:
not `CLAUDE.md`, not `.cursorrules`, not a file this one references. Claude Code, Cursor,
and Codex can chase pointers; it cannot.

So the standards are written for the most constrained reader — flat, inlined, no outbound
links — and every other consumer points at that same file. A rule stated anywhere else is a
rule some surface silently ignores. When a standard changes, change it there.

The canonical human-owned sources remain the **Extole Style Guide** and **Content Strategy
Outline** (Google Docs, docs-team owned); `.mintlify/AGENTS.md` is the agent-actionable
distillation and defers to them.

## How agent config is wired (all tools)

- **Codex / Cursor** auto-read this `AGENTS.md`, and both read `.agents/skills/` natively (it is the Agent Skills standard location). Cursor also attaches `.cursor/rules/*`, a symlink to `.agents/rules` — measured on Cursor 3.16.29, whose bundle reads `.agents/skills` but not `.agents/rules`, so the rules symlink is the load-bearing one.
- **Claude Code** reads [`.claude/CLAUDE.md`](.claude/CLAUDE.md), which `@`-imports this file and the always-on rule.
- **Mintlify's agent** reads only `.mintlify/AGENTS.md` — see above.
- Always-on rules live in `.agents/rules/*.mdc` (`alwaysApply: true`); repeatable workflows live in `.agents/skills/<name>/SKILL.md`. Neither restates a writing standard; both point at `.mintlify/AGENTS.md`.
- These standards came over from [`extole/product-docs-readme`](https://github.com/extole/product-docs-readme), the ReadMe-based predecessor that used to publish docs.extole.com. Terminology, voice, and guardrails are unchanged; the platform mechanics (nav, links, callouts, images, frontmatter, branch naming, preview) are Mintlify's, not ReadMe's.

## Repo layout

| Path | Purpose |
|------|---------|
| `guides/` | Customer-visible marketer/operator how-tos in My Extole. Not the default for new pages. |
| `product/` | Customer-visible product and program overviews — what a capability is. |
| `technical/` | Customer-visible integration, diagnosis, and implementation pages. |
| `news/` | Announcements. Not evergreen pages. |
| `runbooks/` | Hidden operational checklists for Extole's own review work. |
| `docs.json` | Site config **and** the entire navigation (`navigation.tabs[] → groups[] → pages[]`). A page is unreachable until its path (no `.mdx`) is listed here. |
| `api-reference/*.json` | OpenAPI bundles synced by CI from [`extole/openapi`](https://github.com/extole/openapi) (`sync-to-mintlify.yml`), which extracts them from pluribus. Mintlify **generates** the whole API Reference tab from them — don't hand-edit, and leave the `openapi-preview-*` branches that pipeline owns alone. |
| `images/` | Page assets, referenced root-relative (`/images/…`). `images/extole-manifest.json` inventories the migrated ones. |
| `url-map.json` | Old-URL → new-path redirects; the converter emits them into `docs.json`. Add an entry whenever you rename or move a page. |
| `scripts/convert_from_product_docs.py` | The deterministic generator that produced these pages from the ReadMe corpus. Kept for provenance — never re-run it over pages that have been hand-edited since. |
| `.github/workflows/validate.yml` | CI: runs `npx --yes mint@latest validate` on every PR and on pushes to `main`. The **`validate`** check is required to merge. |
| `.mintlify/AGENTS.md` | The writing standards, including where a page lives. Never served publicly — Mintlify does not expose `.mintlify/`. |
| `AGENTS.md`, `.agents/`, `.claude/`, `.cursor/` | Agent config — not published. `.agents`/`.claude` are Mintlify built-in ignores (Claude Code's `CLAUDE.md` lives in `.claude/`); `.cursor/` and `AGENTS.md` are in `.mintignore`. The built-ins do **not** cover repo-root Markdown, so an un-ignored root `AGENTS.md` is served at `/agents.md`. |

## Tooling

- `npx mint@latest dev` — local preview at http://localhost:3000.
- `npx mint@latest validate` — strict build check; must be **0 errors, 0 warnings** before a PR.
- Mintlify MCP servers: `https://mcp.mintlify.com` to edit content and settings, `https://www.mintlify.com/docs/mcp` to query how to use Mintlify.

## Merging

`main` is protected. A change lands only through a pull request that has:

1. a green **`validate`** check (CI runs `npx --yes mint@latest validate`; it fails on warnings as well as errors), and
2. **one approving review**, and
3. the branch up to date with `main`.

`validate` catches broken MDX and a `docs.json` entry pointing at a missing file. It does **not** catch the reverse — a valid page absent from `docs.json` passes CI and ships unreachable — so nav placement stays a reviewer responsibility.

## Critical rules

1. **Write to [`.mintlify/AGENTS.md`](.mintlify/AGENTS.md) for every doc change.** Apply the unambiguous terminology/style fixes automatically; don't leave them for the reviewer. When a standard changes, change it there and nowhere else.
2. **Never invent product behavior, event names, or metrics.** Match the actual system; verify or flag when unsure.
3. **Keep literals verbatim** — event names (`promotion clicked`, `converted`), schema fields (`step_name`), and API identifiers are not style targets.
4. **This repo is docs.extole.com.** Merging to `main` publishes to the live customer site, so treat a merge as a publish. The converter under `scripts/` is provenance for the original migration, not a pipeline — never re-run it over hand-edited pages.
5. **Default branch is `main`, with no branch-name requirement.** Do not carry over the `v4.0.0_<slug>` prefix the ReadMe repo needed. A rendered preview comes from the **PR** (and is not always produced — see the [`mintlify-branch-preview`](.agents/skills/mintlify-branch-preview/SKILL.md) skill), while the AI assistants can read any **pushed branch** directly through `docsBranch`.
6. **MDX is JSX-strict.** A broken tag fails the whole build. Run `npx mint@latest validate` before opening the PR.
7. **Scope PRs to docs.** Don't touch `api-reference/` specs, `scripts/`, or `url-map.json` unless that's the task.
8. **Place a new page by who acts**, not by neighbouring titles in Guides. Load [`product-docs-placement`](.agents/skills/product-docs-placement/SKILL.md) before writing; Guides is not the default tab.

## Open decisions

Several house-style choices are still split across the corpus and awaiting docs-team ratification — see **Open decisions** at the end of [`.mintlify/AGENTS.md`](.mintlify/AGENTS.md) (client vs. customer, report-name formatting, "Refer A Friend" casing, "step" scope, callout severity). Until decided, match the surrounding page and flag the inconsistency — don't pick a side.
