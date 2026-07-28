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

After pushing the branch, confirm the mirror through the API — it is definitive and takes a second:

```bash
curl -s -H "Authorization: Bearer $README_API_KEY" \
  "https://api.readme.com/v2/branches?prefix=v4.0.0" | jq '.data[].name'
```

The `prefix` parameter is required. **A plain `GET /v2/branches` lists only the handful of ReadMe
*versions* (`1.1.0`, `2.0.0`, `2.1.0`, `4.0.0`) and never lists mirrored branches** — checking
without `prefix` shows nothing and looks exactly like a broken sync.

ReadMe drops the leading `v`, so git `v4.0.0_my-slug` appears as `4.0.0_my-slug`. Either spelling
works when addressing the branch in a later API call.

Then:

1. Confirm the changed page is on the branch and not yet on the default branch:
   `GET /v2/branches/v4.0.0_<slug>/guides/<page-slug>` returns 200, while
   `GET /v2/branches/4.0.0/guides/<page-slug>` returns 404 for a new page.
2. Open the branch in the ReadMe UI and confirm the pages render (headings/TOC, nav placement from
   `_order.yaml`, images).
3. Merge into `v4.0.0` to publish; delete the branch after merge.

Mirroring takes up to about a minute after the push. If the branch still does not appear **with the
`prefix` query**, the name almost certainly doesn't match `v4.0.0_<slug>`. Rename by pushing the
same commit under a matching name and repointing the PR:

```bash
git push origin <current-head-sha>:refs/heads/v4.0.0_<slug>
gh pr create --base v4.0.0 --head v4.0.0_<slug> ...
```

## Using the branch in the assistants

A mirrored branch can be used before it is merged. `chat.extole.com` takes the docs branch as
`?docsBranch=v4.0.0_<slug>`, alongside `?branch=` for a catalog branch, and both resolve
independently in the same conversation. Give the catalog branch the same name to keep one name in
your head.

One limit to plan for: ReadMe does not full-text index branch content, so a page that exists only on
a branch is found by the words in its **title and slug**, not its body. Title a new page after the
question it answers, or the assistant may not surface it until the branch merges.

## Scope

- Applies to `docs/` and `custom_pages/` (customer-visible prose). `reference/` is generated from `extole/openapi` and has its own separate preview pipeline — don't hand-edit it.
- Applies no matter what opens the branch/PR: a human, Cursor, Codex, Claude Code, or an automated agent such as catalog. Any tool that creates a product-docs branch must use this naming, or its change is invisible in ReadMe until merged.
