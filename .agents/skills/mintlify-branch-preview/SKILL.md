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

The migration landed at 0/0, so treat anything else as something you introduced. `validate` fails on **warnings** as well as errors, so there is no "it's only a warning" tier here.

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

### What the comment costs you in time, and where its link actually points

Measured over the 25 pull requests #20 and #24–#50 (2026-08-20 → 2026-08-25), by
comparing each PR's `created_at` against its `mintlify[bot]` comment's
`created_at` and `updated_at`:

| | |
|---|---|
| Comment appears after the PR opens | **2–7 seconds**, on all 20 PRs outside the outage window below |
| Same comment is then **edited in place** to 🟢 Ready | 1m42s–4m02s later, median **2m19s** |
| Inside the 19-hour App outage (#24, #25, #26, #27, #31) | 1h23m–3h10m |
| Build ended 🔴 Failed, `Preview` cell `–`, no link at all | 5 of 25 (#26, #31, #40, #48, #49) |

Two consequences. The comment's arrival is not the signal you want — it is there
almost instantly, carrying a status that is stale within a minute; the second
timestamp is the one that means the link works, so re-read the comment rather
than trusting the notification email. And a 🔴 Failed build still posts a
comment, so "the bot commented" is not "there is a preview". Paul Davidson's
rule of thumb on the #dreams thread — "the Mintlify build process runs and adds a
preview link to the comments after about 15 minutes" — is the safe way to wait,
and the numbers above say the usual cost is nearer two and a half minutes with
the outage window as the long tail.

**The View Preview link deep-links the first changed page in path order, which
is usually not the page the PR is for.** On
[#34](https://github.com/extole/product-docs/pull/34) — a new 117-line page plus
four small cross-link edits — the bot linked
`.../technical-items/managing-your-branded-urls` (4 added lines) rather than
`.../technical-items/migrating-to-a-new-program-domain`, the page the PR exists
for; #46 and #50 pick their alphabetically-first changed page the same way, and
#42 and #45, which change only `docs.json` and the API bundles, link the site
root with no path at all. When you are sending someone a page to read, build the
URL yourself — the host is `extole-` plus the branch with slashes as hyphens, the
path is the page's path with `.mdx` dropped — and check it returns 200 before you
send it.

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

### A preview can 404 on the one page the branch changed

Measured on [#43](https://github.com/extole/product-docs/pull/43) (2026-08-24): the
bot reported the build 🟢 Ready and the **View Preview** link it posted — the
changed page — answered `404` for the next half hour, across two builds. Nothing
was wrong with the page:

| On the same preview host | Status |
|---|---|
| the changed page, HTML | **404** |
| the same path with `.md` appended | 200, serving the new copy |
| `/llms.txt` | lists the page |
| every unchanged sibling page, and the group index | 200 |
| another open PR's **changed** page, on its own preview host | 200 |

So this is not "changed pages cannot be previewed", and the cause is unproven. An
empty commit produced no new deployment, so retrying is not the move.

What to do: prove the page a different way and say the link is lying rather than
letting a reviewer read the 404 as a broken page. `npx mint@latest dev` renders
the branch locally, and appending `.md` to the preview URL returns the built copy
of that page — enough to confirm the deployment really contains your edit.

## Branch naming: no constraint here

Use a bare ticket id (`ENG-12345`) or a short kebab-case slug, matching the convention the tech repo uses. Nothing about the name affects the preview.

> **Do not carry the `v4.0.0_` prefix over from `extole/product-docs-readme`.** That prefix existed solely because ReadMe only mirrored branches named `<version>_<slug>`. This repo's default branch is `main` and has no versioning, so a `v4.0.0_` prefix here buys nothing and misdescribes the repo.

## What merging does and does not publish

- Merging to `main` triggers the Mintlify GitHub App to deploy the default branch.
- **It publishes docs.extole.com.** This repo now serves the live customer site, so a merge to `main` is a publish — review it as one.
- **It does not gate the AI assistants.** They can read an unmerged branch already: `extole_docs_search` / `extole_docs_get` with a `docsBranch` read this repository at that branch directly. Pushing is enough; no PR and no preview build are required.

## Scope

- Applies to the customer-visible content directories (`guides/`, `product/`, `technical/`, `news/`, `runbooks/`) and `docs.json`.
- The **API Reference** tab is generated by Mintlify from the OpenAPI bundles in `api-reference/`, which are **written by CI and must not be hand-edited**. `sync-to-mintlify.yml` in [extole/openapi](https://github.com/extole/openapi) copies them here after pluribus `master` changes the REST layer, opens a PR, waits for `validate`, merges it, and publishes the site. The bundles originate in pluribus; `extole/openapi` extracts them and is the direct upstream of this directory.
- Branches named **`openapi-preview-*`** belong to that same pipeline: a pluribus pull request that changes the REST layer gets one, carrying its bundles, so its API reference can be previewed before it merges. The preview link is posted on the pluribus PR. Do not push to, rename, or merge those branches by hand — they are deleted when their pluribus PR closes.
- Applies no matter what opens the branch/PR: a human, Cursor, Codex, Claude Code, or an automated agent. Any tool that changes a page here owes a clean `validate`.
