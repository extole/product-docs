---
name: product-docs-placement
description: Decide where a docs.extole.com page belongs — which tab, which group, and which file path — and whether new content should be a new page, an addition to an existing page, or a link to a page in another tab. Use before creating a page, before adding a section to an existing page, before adding a path to docs.json, before renaming or creating a navigation group, and when reviewing a PR that does any of those. Covers the three-tab model (Product Docs answers what and why, Guides answers how in My Extole, Technical Docs answers how it works and how to implement or diagnose it), the tests that pick the tab, the group each tab holds, the groups inherited from the migration that must not grow, and the path-mirrors-navigation invariant. Guides is the largest tab and the wrong default.
---

# Product-docs placement

Placement is a content decision made **before** drafting, not a `docs.json` afterthought. It
decides three things in order: the tab, the group inside the tab, and whether the content is
a new page at all. Writing standards live in [`.mintlify/AGENTS.md`](../../../.mintlify/AGENTS.md);
the authoring workflow, once the path is chosen, is
[`product-docs-authoring`](../product-docs-authoring/SKILL.md).

## The three customer tabs answer three different questions

One topic can legitimately have up to three pages, one per tab, each written for a different
reader and linking to the other two. It never has two pages in one tab, and it never has the
same content copied into two tabs.

| Tab | Path | The question it answers | Reader | What the page contains |
|---|---|---|---|---|
| **Product Docs** | `product/` | *What is this and why would I want it?* | Someone evaluating, learning, or explaining Extole — no My Extole login assumed | Definitions, program types, capabilities, benefits, strategy framing. No numbered steps, no UI labels, no request forms. |
| **Guides** | `guides/` | *How do I do it in My Extole?* | A marketer or operator with a login | Numbered steps with bold UI labels, ending inside My Extole |
| **Technical Docs** | `technical/` | *How does it work, and how do I implement or diagnose it outside My Extole?* | An integration owner: site, app, tags, domains, data, partner systems | Mechanisms, identifiers, request forms, tags, files, DNS, certificates, SDKs, webhooks, partner consoles, symptom-to-cause diagnosis |

The other three tabs are not for ordinary pages:

| Tab | Path | Holds |
|---|---|---|
| **News** | `news/` | Newsletters and Recent Releases. Dated announcements that link to the evergreen page; never the only place a feature is documented. |
| **API Reference** | `api-reference/` | Generated from the OpenAPI bundles that CI syncs from `extole/openapi`. The one hand-authored group is **Getting Started** (overview, authentication, errors), for material that applies to every API. A how-to for one feature over REST is a Technical Docs page under **Platform Integrations > REST APIs**. |
| **Runbooks** | `runbooks/` | Extole's own review checklists, `noindex`, listed in a `hidden: true` group so Mintlify serves them by path. Not customer pages. |

## Pick the tab

Answer these in order and stop at the first that decides:

1. **Does the reader perform steps?** No steps, no UI labels, no request forms → **Product
   Docs**. A page that explains what Advocate Tiers are, or why Extole matches a friend to
   the advocate who referred them, is Product. If it is dated news rather than evergreen →
   **News**.
2. **Are all the steps inside My Extole?** Every step is a click in the application → **Guides**.
3. **Does any step leave My Extole?** A site tag, a zone request, a DNS record, a certificate,
   an SFTP upload, an API call, an SDK, a webhook endpoint, a partner's console → **Technical
   Docs**, even when the symptom showed up on a campaign and even when a marketer asked.
4. **Does it explain a platform mechanism in terms the reader acts on?** Identifiers, ordering,
   parameters, request forms — targeting, identity resolution, journey pinning, attribution,
   profile scopes → **Technical Docs**. The same mechanism described in outcomes and benefits,
   with nothing to act on, is Product.

**Both marketer and integration owner are real readers** for many topics. Do not fold the
mechanism into the Guides page. Put the mechanism, the diagnosis, and every request, tag,
domain, or file detail in Technical Docs. If the marketer also has a My Extole action, write a
**short** Guides page: the symptom, the setting to change, a link to the technical page.

**Examples.**

- Several live programs open the same share experience because they publish one zone name and
  an existing journey is matched first → Technical Docs (Troubleshooting). A Guides page, if
  needed, is "set a distinct **CTA Popup Zone Name** per program" plus the link.
- A webhook payload omits fields the person has no value for → Technical Docs (Platform
  Integrations > Webhooks), because the reader is writing the consumer of that payload.
- How to pause a campaign, push a test campaign live, QA a program in My Extole → Guides.
- What a Welcome Offer is; how rewards and quality rules relate → Product Docs.
- Authenticate against any Extole API; the error envelope every endpoint returns → API
  Reference > Getting Started. Write campaign component settings over REST → Technical Docs
  > Platform Integrations > REST APIs.

## What is not a reason to choose Guides

- The question came from a marketer, a CSM, or a support ticket.
- The title is a how-to or a "why does this happen".
- The topic is programs, campaigns, CTAs, or share experiences.
- A neighbouring Guides page already covers something similar. Several Guides groups hold
  technical pages inherited from the migration (listed below). They are not a licence to add
  more. Match neighbours for page structure and house style, never to choose the tab.

## Additions to an existing page follow the same test

The test applies to a new section as much as to a new page. Decide by the content being added,
not by the page the reader happened to land on:

- An addition that explains a mechanism or names a request form belongs on the Technical Docs
  counterpart, even when the page in hand is a Guides page. Add it there, and give the Guides
  page a one-line pointer if the reader needs it.
- An addition that is a My Extole click-path belongs on the Guides counterpart.
- Never grow a page in one of the inherited groups below with more of the content that made it
  misplaced. A misplaced page with three new sections is three times harder to move.

## Do not duplicate across tabs

Before writing, search the corpus for the topic (`grep -ril <term> guides product technical`).
If a page in another tab already covers it, link to that page instead of restating it. If the
existing page is in the wrong tab, do not write a correctly placed copy beside it — that leaves
two pages to reconcile. Write the new page where it belongs, link the old one to it, and say in
the PR that the old page is now a candidate for removal.

The corpus currently carries the same topic in more than one tab in several places (A/B
testing in all three tabs, ADA compliance in Product and Guides, a glossary in each of Product
and Guides, single sign-on in Guides and Technical, an SSL stub in Guides pointing at the
Technical page). Do not add to them.

## Pick the group inside the tab

Use an existing leaf group whose neighbours answer the same kind of question for the same
reader. A page sitting loose at a group root beside subgroups is the shape the Guides reorg had
to undo; add a page to a leaf unless the group has no subgroups.

### Technical Docs

| Group | Holds | Status |
|---|---|---|
| Integration Overview | Orientation, key concepts, and platform mechanisms that span surfaces: identity resolution, profile data scopes, how events attach to people | Grows |
| Extole AI Tools | The Extole MCP server and CLI: setup per coding tool, what they can do | Grows |
| Platform Integrations | Implementing against one surface: JavaScript SDK, Mobile SDKs, REST APIs, Files, Webhooks, Extensions | Grows |
| Partners | One page per partner product, under its category | Grows |
| Building Packaged Integrations | Building and publishing a reusable partner integration with the Management API. Being renamed to Building Partner Integrations in an open PR; its files still sit under `building-custom-integrations/` | Grows; do not rename again without the move |
| Solutions | Industry launch guides that mix tagging, branding, rewards, and opt-ins for a launch team, plus the Go Extole app | Inherited; do not add |
| Operational Tasks | Account-level work an integration owner or admin does: DNS, SSL, tokens, SSO, firewall, opt-out lists, test-data exclusion | Grows. Its **Program Testing** subgroup holds My Extole A/B click-paths that duplicate Guides; do not add there |
| Troubleshooting | Symptom-to-cause diagnosis an integration owner runs | Grows |

### Guides

| Group | Holds | Status |
|---|---|---|
| Platform Overview | Getting started in My Extole, key concepts, program and campaign flows, QA checklists | Grows for My Extole orientation only. Its **Implementing your Referral Program > Technical Items** subgroup, its loose SFTP and event-upload pages, and its **Targeting** page are integration content inherited from the migration; do not add there |
| Programs & Campaigns | Creating, editing, managing, and QAing campaigns; asset guides for Extole experiences; program-type how-tos | Grows |
| Dashboards and Reporting | Dashboards, metrics, running and configuring reports, report types | Grows. Its **Integrating Reports** subgroup (SFTP conventions, the asynchronous reporting API) is integration content; do not add there |
| Audiences & Segmentation | Building and managing audiences and segments in My Extole | Grows |
| Rewards Management | Reward setup, rules, fulfillment, and investigation in My Extole | Grows |
| Strategy & Best Practices | What to run and why, as actions a marketer takes in their program: offers, promotions, share channels, optimization | Grows |
| Flow Campaigns | Flow Builder how-tos: business events, trigger rules, rewards, targeting a program | Grows |
| User Management | Team members, roles, SSO sign-in, multiple instances | Grows |
| Notifications & Troubleshooting | My Extole notifications, login, browser support, status page | Inherited; do not add diagnosis here. Its **Troubleshooting** subgroup holds one quick-reference page; symptom-to-cause pages go to Technical Docs |
| Compliance & Policies | The client-facing compliance commitments: DPA, data subject rights, cookie handling, ADA | Inherited; overlaps Product Docs > Security & Compliance. Do not add to either until the docs team picks one |

### Product Docs

| Group | Holds | Status |
|---|---|---|
| Extole Overview | What Extole is, terms, your Extole team | Grows |
| Product Overview | One subgroup per capability area: Programs, Content, People, Events, Rewards, Data, Integration & Launch, Security & Compliance. Concept pages only | Grows. **Integration & Launch** overlaps Technical Docs > Integration Overview and **Security & Compliance** overlaps Guides > Compliance & Policies; do not add to either overlap until the docs team picks one |
| Best Practices | Strategy framing with no My Extole steps: reward strategy by industry, when to test | Grows |

Create a new group only when no existing group is honest about the reader and the job. Adding
a group is a navigation change: keep it in the same PR and say why in the description.

## Path, navigation, and URL are one thing

Mintlify derives the URL from the file path, and this repo keeps the file path equal to the
navigation position: `<tab dir>/<group slug>/<subgroup slug>/<page>.mdx`, with `&` slugified
as `and` (`programs-and-campaigns`). So:

- A new page's path starts with the tab you chose and follows the group chain you chose. Then
  add that path, without `.mdx`, to the matching `navigation.tabs[] → groups[] → pages[]`
  entry in `docs.json`.
- **Renaming a navigation group is a URL change for every page in it.** Do it with the
  directory move and an `url-map.json` redirect per published page, in one PR, or do not do
  it. A group renamed in `docs.json` alone leaves the sidebar and the URLs disagreeing.
- Moving or renaming a page that has published needs an old-URL → new-path entry in
  `url-map.json`. A page that has never been on `main` needs none.
- A valid page absent from `docs.json` passes `mint validate` and ships unreachable: it serves
  at its URL but appears in no sidebar and no search. Six troubleshooting pages shipped that
  way. Run the check below before opening the PR.

## Before you write

State the answers, then the path:

1. **Who acts, and where?** No steps → Product. Steps inside My Extole → Guides. Any step
   outside it, or a mechanism the reader acts on → Technical.
2. **Does a page on this already exist in another tab?** Link, do not copy.
3. **Are two readers real?** Split; the mechanism goes to Technical.
4. **Is the nearest existing page in an inherited group?** Do not join it, and do not grow it.
5. **Is this an addition to an existing page?** Place the addition by its own content.

If the tab is still ambiguous, prefer Technical Docs for mechanism and diagnosis, Product Docs
for a page with no steps, and flag the choice in the PR rather than defaulting to Guides.

## Verification

```bash
python3 scripts/check_navigation.py
```

It reports pages absent from `docs.json`, navigation entries with no file, and pages whose path
does not mirror their navigation position, and exits non-zero on any finding. `npx mint@latest
validate` catches only the second of the three. The corpus carries findings of its own from the
migration and from a group renamed without its move; those are the move pass's list. Your
change introduces none: compare the report against `main` and account for every new line.
