---
name: readme-branch-preview
description: Name every branch in extole/product-docs so ReadMe mirrors it as a previewable branch at https://docs.extole.com/#/branches before merge. REQUIRED before creating any branch, commit, or PR in this repo — including from external tools or agents (catalog, Cursor, Codex, Claude Code, cloud agents). Branch names MUST be `<version>_<slug>` (currently `v4.0.0_<slug>`); a name that doesn't match (e.g. `cursor/…`, `docs/…`, a bare `ENG-1234`) is silently ignored by ReadMe and never gets a preview. Use whenever the work will produce a branch or PR against product-docs.
---

# ReadMe branch preview

This repo publishes to **docs.extole.com** through **ReadMe's bi-directional Git Sync**. ReadMe mirrors a Git branch into its Branches UI — with a shareable, rendered preview link — **only when the branch name matches `<version>_<branch>`**, where `<version>` is an existing ReadMe version. That lets a reviewer see the rendered pages (style, layout, nav) *before* the change goes live. A branch whose name does not match is not mirrored, produces no preview, and shows up nowhere in ReadMe.

## The rule

Name every branch:

```
v4.0.0_<slug>
```

- `v4.0.0` is the current ReadMe version and default branch of this repo (see `AGENTS.md` critical rule 4). If the default version changes, the prefix tracks it.
- `<slug>` is a short kebab-case description (`v4.0.0_add-gemini-guide`) **or** a Jira ticket id (`v4.0.0_ENG-28706`).

**Branch off and target `v4.0.0`.** Merging the branch into `v4.0.0` is what publishes to docs.extole.com.

### Ticket branches keep the prefix

When a ticket is in scope, keep the ticket key **inside** the prefixed name: `v4.0.0_ENG-12345`. Jira and GitHub still auto-link because the key is present in the branch name, and ReadMe still mirrors it because the `v4.0.0_` prefix is present.

> This deliberately **overrides** the tech repo's `tech-worktree-workflow` skill, which says a ticket branch must be the bare ticket id with no prefix. In `extole/product-docs` the `v4.0.0_` prefix is mandatory — without it there is no docs preview — so the prefix wins here. Everything else in that skill (worktrees, one PR per branch, base off the default branch) still applies; only the bare-ticket-id naming is overridden.

## Why (mechanics)

- ReadMe keys off the **Git branch name**, not the pull request. A PR is a GitHub concept ReadMe never consumes — pushing a correctly-named branch is what generates the preview. (A PR is still required by repo policy; it just isn't what triggers the mirror.)
- Branch names must match a ReadMe **version** exactly as a prefix: `v4.0.0_x` syncs; `v4-x` or `docs/x` or `cursor/x` do not.
- Each mirrored branch gets a shareable preview URL; external (logged-out) reviewers can open it without a key for 7 days.

## Verify

After pushing the branch:

1. Open **https://docs.extole.com/#/branches** — the branch should be listed with a preview link.
2. Open the preview and confirm the changed pages render (headings/TOC, nav placement from `_order.yaml`, images).
3. Merge into `v4.0.0` to publish; delete the branch after merge.

If the branch does **not** appear, the name almost certainly doesn't match `v4.0.0_<slug>` (most common cause). Rename by pushing the same commit under a matching name and repointing the PR:

```bash
git push origin <current-head-sha>:refs/heads/v4.0.0_<slug>
gh pr create --base v4.0.0 --head v4.0.0_<slug> ...
```

## Scope

- Applies to `docs/` and `custom_pages/` (customer-visible prose). `reference/` is generated from `extole/openapi` and has its own separate preview pipeline — don't hand-edit it.
- Applies no matter what opens the branch/PR: a human, Cursor, Codex, Claude Code, or an automated agent such as catalog. Any tool that creates a product-docs branch must use this naming, or its change is invisible in ReadMe until merged.
