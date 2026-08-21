---
name: mintlify-branch-preview
description: Prove an Extole docs change builds, and see it rendered, before it merges to the live site. Use before opening any branch or PR in extole/product-docs, and whenever someone needs to see how a page will look. Covers the `npx mint@latest validate` gate and what it does and does not catch, the CI check that enforces it on every PR, local `npx mint@latest dev`, why the per-PR Mintlify preview cannot be relied on, branch naming (no prefix requirement here — unlike the ReadMe repo), and the fact that merging publishes docs.extole.com.
---

# Mintlify preview & validation

This repo builds with **Mintlify** and `main` publishes the live customer site, so a change is reviewed before it is published, not after. There are two ways to see it rendered first, and one hard gate that must pass either way — enforced in CI, so it is not optional.

## The gate: the MDX build must be clean

Mintlify pages are **MDX** — JSX-strict. A bare `<`, an unclosed tag, a stray `{`, or a nav entry pointing at a file that doesn't exist is a **build failure**, not a rendering quirk on one page. Run this before you open a PR:

```bash
npx mint@latest validate    # target: 0 errors, 0 warnings
```

The migration landed at 0/0 (see [`MIGRATION.md`](../../../MIGRATION.md)), so treat anything else as something you introduced. `validate` fails on **warnings** as well as errors, so there is no "it's only a warning" tier here.

The nav failure it catches is a `docs.json` entry pointing at a file that does not exist — most often a path with the `.mdx` extension left on:

```
warning - "guides/.../understanding-participation-rate.mdx" is referenced in the
docs.json navigation but the file does not exist.
error Build validation failed with 1 warning(s).
```

**The reverse is not caught.** A page file that is valid MDX but appears in no `docs.json` group passes validation with exit 0 — it simply ships unreachable, with no build signal and no CI failure. Measured 2026-08-21 against `mint@latest`. Adding the page to `docs.json` is on you and on the reviewer; the build will not remind you.

## Local preview

```bash
npx mint@latest dev        # http://localhost:3000
```

Renders the whole site from the working tree — the fastest way to check heading structure, the on-page TOC, callout components, image paths, and where a page landed in the sidebar.

## CI runs the gate on every PR

[`.github/workflows/validate.yml`](../../../.github/workflows/validate.yml) runs `npx --yes mint@latest validate` on every pull request, on pushes to `main`, and on manual dispatch. The **`validate`** check is a required status check on `main`, alongside one approving review, so a PR that breaks the build cannot merge.

The workflow deliberately carries no `paths:` filter. A required check that is skipped never reports a conclusion, so filtering it by path would leave any PR outside those paths pending forever. The run takes about 30 seconds; the cost of running it on every PR is far below the cost of a wedged merge queue.

## Shared preview: open the PR

Mintlify's GitHub App builds a **preview deployment for a pull request** and comments the link on the PR. That is the shareable, rendered preview to send a reviewer — it is the PR, not the branch, that produces it.

**Do not count on it.** Observed 2026-08-21: of four open PRs on this repo, two had a preview comment and two did not, one of them 20 minutes after the PR was opened; a merged branch's preview host also served an empty index. When no preview appears, `npx mint@latest dev` locally is the reliable rendered check, and `validate` is the gate that actually blocks a bad build.

So: push the branch and open the PR; use the preview link if it appears, and fall back to local `dev` when it does not. Either way the `validate` check has to be green.

## Branch naming: no constraint here

Name branches however the tech repo's `tech-worktree-workflow` skill says — a bare ticket id (`ENG-12345`) or a short kebab-case slug. Nothing about the name affects the preview.

> **Do not carry the `v4.0.0_` prefix over from `extole/product-docs-readme`.** That prefix existed solely because ReadMe only mirrored branches named `<version>_<slug>`. This repo's default branch is `main` and has no versioning, so a `v4.0.0_` prefix here buys nothing and misdescribes the repo.

## What merging does and does not publish

- Merging to `main` triggers the Mintlify GitHub App to deploy the default branch.
- **It publishes docs.extole.com.** This repo now serves the live customer site, so a merge to `main` is a publish — review it as one.
- **It does not gate the AI assistants.** They can read an unmerged branch already: `extole_docs_search` / `extole_docs_get` with a `docsBranch` read this repository at that branch directly. Pushing is enough; no PR and no preview build are required.

## Scope

- Applies to the content tabs (`guides/`, `product/`, `technical/`, `news/`) and `docs.json`.
- The **API Reference** tab is generated by Mintlify from the OpenAPI bundles in `api-reference/`, which come from `extole/extole-specification` — it has its own upstream and is not hand-edited here.
- Applies no matter what opens the branch/PR: a human, Cursor, Codex, Claude Code, or an automated agent. Any tool that changes a page here owes a clean `validate`.
