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

## Shared preview: open the PR, or ask the API

Mintlify serves any branch of this repo at
`https://extole-<branch>.mintlify.site`, and that is the shareable rendered
preview to send a reviewer.

**Normal path: open the PR.** The Mintlify GitHub App deploys each branch it
sees and posts a `Preview deployment for your docs` comment with a **View
Preview** link on the pull request. Push, open the PR, use that link.

**When there is no PR, ask for the preview directly.** The bot comments on pull
requests, so a branch pushed without one gets a deployment but no link handed to
you anywhere. That is exactly the OpenAPI preview pipeline's situation — it
pushes `openapi-preview-*` branches here and needs the URL back in order to
comment it on a *pluribus* PR — so it calls the API instead:

```bash
curl -X POST \
  -H "Authorization: Bearer $MINTLIFY_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"branch":"YOUR_BRANCH"}' \
  "https://api.mintlify.com/v1/project/preview/$MINTLIFY_PROJECT_ID"
```

It returns `{"statusId":"…","previewUrl":"https://extole-YOUR_BRANCH.mintlify.site"}`.
Poll `GET https://api.mintlify.com/v1/project/update-status/{statusId}` until
`status` is `success` — measured build time for this site is about 90 seconds —
and only then share the link. `POST /v1/project/update/{projectId}` does the
same for `main`, forcing a publish of docs.extole.com.

The branch name becomes a DNS label in that host, so it must be lowercase
`[a-z0-9-]` and the whole `extole-<branch>` subdomain must stay under 63
characters.

`MINTLIFY_API_KEY` and `MINTLIFY_PROJECT_ID` come from the Mintlify dashboard's
API keys page; `extole/openapi` holds them as repository secrets for the
pipeline above.

### A missing preview comment is a signal, not the norm

The App went silent for about 19 hours — no deployment of any kind between
2026-08-20T21:53:47Z and 2026-08-21T16:54:56Z — which straddles the
`product-docs-mintlify` → `product-docs` rename. During it, merges to `main` did
not publish: the functional-review runbooks merged at 15:30Z were still 404 on
docs.extole.com hours later, until `POST /v1/project/update/{projectId}` was
called by hand.

It then recovered on its own and backfilled what it had missed, deploying
branches whose pushes were an hour or more old. Nothing in this repo or in the
Mintlify settings was changed to bring it back, so **the cause is unproven** —
the silence coincided with the rename, and it ended roughly 40 minutes after an
API-triggered preview build, but neither link is established.

The operational point: if you push a branch, open a PR, and no `mintlify[bot]`
comment arrives within a few minutes, do not assume you did something wrong and
do not wait it out. Check
`gh api repos/extole/product-docs/deployments --jq '.[0:3][]|"\(.created_at) \(.ref)"'`
— if the newest entry is hours old the App is stalled again. Use the API calls
above to unblock yourself, and say so, because while it is stalled **merging does
not publish**.

## Branch naming: no constraint here

Name branches however the tech repo's `tech-worktree-workflow` skill says — a bare ticket id (`ENG-12345`) or a short kebab-case slug. Nothing about the name affects the preview.

> **Do not carry the `v4.0.0_` prefix over from `extole/product-docs-readme`.** That prefix existed solely because ReadMe only mirrored branches named `<version>_<slug>`. This repo's default branch is `main` and has no versioning, so a `v4.0.0_` prefix here buys nothing and misdescribes the repo.

## What merging does and does not publish

- Merging to `main` triggers the Mintlify GitHub App to deploy the default branch.
- **It publishes docs.extole.com.** This repo now serves the live customer site, so a merge to `main` is a publish — review it as one.
- **It does not gate the AI assistants.** They can read an unmerged branch already: `extole_docs_search` / `extole_docs_get` with a `docsBranch` read this repository at that branch directly. Pushing is enough; no PR and no preview build are required.

## Scope

- Applies to the content tabs (`guides/`, `product/`, `technical/`, `news/`) and `docs.json`.
- The **API Reference** tab is generated by Mintlify from the OpenAPI bundles in `api-reference/`, which are **written by CI and must not be hand-edited**. `sync-to-mintlify.yml` in [extole/openapi](https://github.com/extole/openapi) copies them here after pluribus `master` changes the REST layer, opens a PR, waits for `validate`, merges it, and publishes the site. The bundles originate in pluribus; `extole/openapi` extracts them and is the direct upstream of this directory.
- Branches named **`openapi-preview-*`** belong to that same pipeline: a pluribus pull request that changes the REST layer gets one, carrying its bundles, so its API reference can be previewed before it merges. The preview link is posted on the pluribus PR. Do not push to, rename, or merge those branches by hand — they are deleted when their pluribus PR closes.
- Applies no matter what opens the branch/PR: a human, Cursor, Codex, Claude Code, or an automated agent. Any tool that changes a page here owes a clean `validate`.
