---
name: product-docs-placement
description: Decide which tab and group a new or moved docs.extole.com page belongs in. Use before creating a new page, converting a draft into a page, adding a path to docs.json, or when a page was added under guides/ and may belong in technical/ or product/ instead. Covers the actor test (who performs the work), the split when a topic has both a My Extole click-path and an integration mechanism, and how to pick the nav group. Do not default to Guides.
---

# Product-docs placement

Choose the **tab and group before writing the page**. Placement is a content decision,
not a `docs.json` afterthought. Guides is the largest tab and the wrong default.

Writing standards: [`.mintlify/AGENTS.md`](../../../.mintlify/AGENTS.md). Authoring
workflow (once the path is chosen): [`product-docs-authoring`](../product-docs-authoring/SKILL.md).

## The actor test

Pick the tab by **who performs the work**, not by the topic, the support ticket, or
whether the title starts with "How to" / "Why".

| Tab | Path | Who acts | Typical pages |
|---|---|---|---|
| **Guides** | `guides/` | A marketer or operator in **My Extole** | Campaign setup, creative, audiences, rewards, reporting, QA, strategy, in-app notifications |
| **Technical Docs** | `technical/` | An **integration owner** — site, app, tags, domains, data, or partner systems | SDKs, REST, files, webhooks, zone/tag mechanics, targeting parameters, SSL/DNS, partner integrations, symptom-to-cause troubleshooting |
| **Product Docs** | `product/` | A reader learning **what a capability is** | Product and program overviews, concepts, best-practice framing. Not the click-path and not the implementation. |
| **News** | `news/` | — | Announcements. Not evergreen pages. |
| **Runbooks** | `runbooks/` | Extole's own reviewers | Hidden operational checklists. Not customer pages. |
| **API Reference** | `api-reference/` | — | Generated from OpenAPI. Do not add ordinary pages. |

A page belongs in Technical Docs when the reader has to change a site tag, a zone
request, a domain, a certificate, an SDK, a webhook, or a request parameter — even
when the symptom showed up on a campaign. Guides is for work that is finished
inside My Extole.

## Do not default to Guides

These are not reasons to put a page in `guides/`:

- The question came from a marketer or from support.
- The title is a how-to or a "why does this happen".
- The topic is programs, campaigns, CTAs, or share experiences.
- A neighbouring Guides page exists, including **Platform Overview > Technical Items**
  and **Notifications & Troubleshooting**. Those groups are inherited from the
  migration; they are not a licence to add more technical pages there.
- Matching neighbours is for **page structure and house style**, not for the tab.

The corpus is mixed on purpose of history. New pages follow the actor test, not
the nearest existing file.

## Split when both actors are real

Some topics have a My Extole click-path **and** a platform mechanism. Do not fold
the mechanism into the Guides page.

- Put the **mechanism, diagnosis, and request/tag/domain work** in Technical Docs.
- If a marketer also needs a click-path, write a **short** Guides page that states
  the symptom, the setting to change, and links to the technical page.
- One page that explains zone candidate selection, journey pinning, or targeting
  hints does **not** belong under Programs & Campaigns, Asset Guides, or
  Managing Campaigns — those groups are campaign-editor how-tos.

**Example.** Several live programs can open the same share experience because they
publish one zone name and an existing journey is matched before a new one starts.
That page goes in Technical Docs. A Managing Campaigns page, if one is needed,
is only "set a distinct **CTA Popup Zone Name** per program" plus a link.

**Example.** Creatives not rendering on a branded domain, a certificate missing
on the program domain, events that record but never attribute — integration
diagnosis. Technical Docs, not Guides troubleshooting.

**Counter-example.** How to pause a campaign, push a test campaign live, or QA a
referral program in My Extole — Guides.

**Counter-example.** What a Welcome Offer is, or an events/rewards overview —
Product Docs.

## Pick the group inside the tab

After the tab, use an **existing** group whose neighbours answer the same kind of
question. Prefer that over a new group.

- Integration how-to (SDK, REST, files, webhooks, extensions) → **Platform Integrations**.
- Custom inbound/outbound/reward integrations → **Building Custom Integrations**.
- Partner product → **Partners**, under that partner's group.
- DNS, SSL, tokens, SSO, firewall, test-data exclusion → **Operational Tasks**.
- Symptom-to-cause diagnosis that an integration owner runs → **Troubleshooting**
  under Technical Docs (`technical/troubleshooting/`) when that group exists;
  otherwise the operational or integration group that already owns the system.
  Do not add these to Guides > Notifications & Troubleshooting.
- Marketer click-path → the matching Guides group (Programs & Campaigns,
  Rewards Management, Dashboards and Reporting, …).

Create a new group only when no existing group is honest about the reader and
the job. Adding a group is a navigation change; keep it in the same PR and say
why in the description.

## Place it in `docs.json`

The filesystem path must start with the tab you chose (`guides/…`, `technical/…`,
`product/…`). Then add that path, without `.mdx`, to the matching
`navigation.tabs[] → groups[] → pages[]` entry. A valid page missing from
`docs.json` ships unreachable; `mint validate` will not catch it.

If you move or rename a page that has already published, add an old-URL → new-path
entry to `url-map.json`. Skip that for a page that has never been on `main`.

## Before you write

Answer these, then pick the path:

1. **Who acts?** Marketer in My Extole, integration owner, or a reader of concepts?
2. **Would this be done without touching site tags, domains, SDKs, or request
   parameters?** If no, it is not a Guides page.
3. **Are there two actors?** If yes, split; do not hide the mechanism in Guides.
4. **Am I copying a misplaced neighbour?** If the nearest file fails the actor
   test, do not join it.

State the chosen path (and the split, if any) before drafting. If the tab is
genuinely ambiguous, prefer Technical Docs for mechanism and diagnosis, and
flag the choice in the PR rather than defaulting to Guides.
