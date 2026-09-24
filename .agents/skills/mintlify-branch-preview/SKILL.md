---
name: mintlify-branch-preview
description: Must be read before opening a branch or pull request in this repo, and whenever someone needs to see how a page will render.
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

**The reverse is not caught.** A page file that is valid MDX but appears in no `docs.json` group passes validation with exit 0 — it simply ships unreachable, with no build signal and no CI failure. Measured 2026-08-21 against `mint@latest`, and six troubleshooting pages then shipped exactly that way. `python3 scripts/check_navigation.py` reports it, along with paths that do not mirror their navigation group; run it alongside `validate`.

**And a page can pass `validate`, render in `mint dev`, and still 404 on the hosted preview.** The hosted build is stricter than both local tools, and it fails one page rather than the run — so `validate` is green, **Mintlify Deployment** is green, and the page you edited is the only one missing. Measured 2026-09-21: adding a `<Warning>` containing an indented markdown bullet list and a `×` (U+00D7) to `creative-image-asset-guide.mdx` left that one path 404 on `https://extole-<branch>.mintlify.site` while every unedited sibling in the same group answered 200; `npx mint@latest validate` reported `success build validation passed` and `npx mint@latest dev` served the page with the callout rendered. Rewriting the callout as plain paragraphs with ASCII `x` fixed it on the next push. So **curl the preview path of every page you touched** — a green deployment check is not the same claim, and the failure signature is indistinguishable from a page you forgot to add to `docs.json`.

**Indented content inside a callout is not caught either, and it takes the whole page down.** Write the body of a `<Warning>`, `<Info>`, `<Tip>` or `<Note>` flush to the left margin, the way the existing pages do. Indent it two spaces — the shape most editors and most other MDX sites accept — and `npx mint@latest validate` still reports `success build validation passed` with 0 errors and 0 warnings, `npx mint@latest dev` still serves the page at `200` with the new section in it, the PR's `validate` check still passes, and the hosted preview returns **404 for that one page** while every other page on the same branch serves normally. So the only signal is fetching your own page on the preview and finding it missing, which reads like a preview that has not finished building. Measured 2026-09-17 on `guides/flow-campaigns/how-to-set-up-reward-rules`: one commit that changed nothing but the indentation of a callout body turned that 404 into a rendered page. Fetch the page you edited, not just the preview root, before you call a preview good.

## Local preview

```bash
npx mint@latest dev        # http://localhost:3000
```

Renders the whole site from the working tree — the fastest way to check heading structure, the on-page TOC, callout components, image paths, and where a page landed in the sidebar.

### `dev` is also the only way to census a rendering defect

`validate` proves the MDX parses, not that the page says what it says. Nothing in CI reads the rendered HTML, so a defect that is legal MDX ships silently and is only visible to someone who opens the page. Drive the dev server over every page and grep the HTML for the defect's own marker:

```bash
npx mint@latest dev &                     # wait for / to answer 200
find guides product technical news runbooks -name '*.mdx' | sed 's/\.mdx$//' \
  | xargs -P 4 -I{} sh -c 'echo "$(curl -s --max-time 180 http://localhost:3000/{} | grep -c "katex-mathml") {}"'
```

Three things that bite. Count the rows against the file count and check every page returned 200 — a sweep against a dead server reports zero of everything, which reads exactly like a clean result. Do not wrap `mint dev` in `timeout`; it dies mid-sweep. And `curl` it once per page with a couple of retries, because the server compiles each page on first request.

Measured 2026-09-21 on `docs/dollar-amounts-render-as-math`: 432 pages swept in about six minutes, 22 of them publishing accidental LaTeX (see the `\$` rule in [`.mintlify/AGENTS.md`](../../../.mintlify/AGENTS.md)), 0 after the fix. `validate` was green throughout, before and after.

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
characters. A `/` in the branch name becomes a `-`:
`docs/loyalty-content-gaps` is served at
`extole-docs-loyalty-content-gaps.mintlify.site`.

### A preview URL in a request names a branch that already exists

Review feedback usually arrives as the preview link the reviewer was reading
("here are some updates to make to this doc: extole-docs-…mintlify.site/…").
That link is not a page on the live site — it is somebody's open branch, so the
edits belong as a commit on that branch, not on a new one off `main`. A second
PR against the same pages splits the review and races the first one to merge.

Map the host back before you plan. Strip the `extole-` prefix, then resolve the
rest against the real branch list rather than assuming — the `/` collapse above
means `docs/loyalty-content-gaps` and `docs-loyalty-content-gaps` are the same
host:

```bash
git ls-remote --heads origin | grep -i loyalty-content-gaps
gh pr list --repo extole/product-docs --state open --head docs/loyalty-content-gaps
```

Then `git fetch origin <branch>`, commit, push, and say on the PR what you
changed. The preview host is unchanged, so the reviewer's own link shows the
edits once **Mintlify Deployment** goes green — about 90 seconds after
`validate`.

**Read that branch's newest commits before you plan, and fetch it again before
you push.** A reviewer going through a large branch sends several rounds of
feedback within a few minutes, and each one is worked separately, so the page
you were sent can already carry somebody else's fix. On 2026-09-17 the
`docs/loyalty-content-gaps` branch took five commits between 22:03 and 22:15,
and the sentence flagged at 22:05 was rewritten at 22:13 by the round before
it:

```bash
git log --format='%h %ad %s' --date=iso -5 origin/<branch>
git show origin/<branch>:<path/to/page.mdx>
```

Read the page at the branch tip, not the preview HTML the reviewer linked —
the deployed copy lags the branch. Then rebase onto the tip and push; what is
left to do is usually smaller and more specific than the request implies.

`MINTLIFY_API_KEY` and `MINTLIFY_PROJECT_ID` come from the Mintlify dashboard's
API keys page; `extole/openapi` holds them as repository secrets for the
pipeline above.

### Read the host backwards when somebody sends you one

A request that arrives as a preview URL — "updates to this doc: `extole-<something>.mintlify.site/…`"
— is feedback on a **branch**, and the host names it. Strip the `extole-` prefix; what is left is
the branch with its slashes flattened to hyphens, so more than one branch name can produce it.
`git ls-remote --heads origin` and pick the one that exists:
`extole-docs-loyalty-content-gaps` is `docs/loyalty-content-gaps`, not `loyalty-content-gaps`.

Then check `main` before you plan. The page may not be there at all — a preview host serves pages
that have never been published, so `git grep` on `main` returns nothing and the page is neither
missing nor deleted. Read it with `git show origin/<branch>:<path>`.

Feedback on a page in that state is a commit onto that branch, and a comment on its open pull
request saying what changed. A second pull request off `main` for the same page duplicates work
that is already in somebody's review queue, and it cannot be previewed at the URL the request
came from.

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

### A preview can 404 on the one page the branch changed — or on the whole host

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

It also happens to the **entire host**, not just the changed page, so a 404 at
`/` is not evidence that the branch failed to deploy. Measured on
[#88](https://github.com/extole/product-docs/pull/88) (2026-09-09), 40 minutes
after a 🟢 Ready comment and a passing `Mintlify Deployment` check, and still
404 on six probes over two minutes:

| On `extole-newsletters-june-august-2026.mintlify.site` | Status |
|---|---|
| `/` | **404** |
| the changed page, HTML | **404** |
| the same path with `.md` appended | 200, carrying the new entries |
| `/llms.txt` | 200 |
| `extole-sup-68406-prefer-journey-campaign-id`, another branch, same paths | 200 |

`gh api repos/extole/product-docs/deployments` listed the branch as the newest
deployment, at the timestamp the bot reported. So the deployment is real, the
build contains the edit, and only the HTML route is dead — the cause is still
unproven and there is nothing to retry.

What to do: prove the page a different way and say the link is lying rather than
letting a reviewer read the 404 as a broken page. `npx mint@latest dev` renders
the branch locally, and appending `.md` to the preview URL returns the built copy
of that page — enough to confirm the deployment really contains your edit. When a
reviewer needs to *see* it, screenshot the local render and put the picture in the
pull request: `nix-shell -p chromium` supplies a browser, `liberation_ttf` plus a
`fonts.conf` under `FONTCONFIG_FILE` supplies the fonts the pod does not have, and
`npx mint@latest dev` must be driven with puppeteer rather than chromium's own
`--screenshot --virtual-time-budget`, which never settles against the dev server's
live-reload socket.

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
