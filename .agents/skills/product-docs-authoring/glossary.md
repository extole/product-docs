# Extole product-docs terminology glossary

Preferred terms for Extole customer-facing documentation (`extole/product-docs` → docs.extole.com). This is the agent-actionable distillation used by the **product-docs-authoring** skill and the **product-docs-style** rule.

**Status: proposed — for docs-team ratification.** Counts come from ripgrep across the 461 pages in `docs/` (2026-07). Where the corpus is genuinely split, the term is listed under **Open decisions** below rather than given a verdict — those need a human call before an agent enforces them. The canonical human-owned sources are the **Extole Style Guide** and **Extole Content Strategy Outline** (Google Docs); this file defers to them and should be updated when they change.

## How an agent uses this

- Use the **Preferred** term. Do not introduce a term from the **Avoid** column.
- Apply swaps in **prose only**. Never rewrite a literal event name, schema field, API identifier, or code sample (see the caveats in the table).
- If a term is under **Open decisions**, do not silently pick a side — write it the way the surrounding page already does and flag the inconsistency to the user.

## Preferred terms

| Preferred | Avoid | Definition | Evidence / caveat |
|---|---|---|---|
| **advocate** | referrer, sharer | A person who refers a brand or product to a friend. | advocate ~1752 occ / 258 files; referrer 14, sharer 3. |
| **friend** | referred person, referee, referred customer | A person who receives a referral from an advocate. | friend ~1618 occ; "referred person" 3 occ (gloss only). |
| **event** | step *(as loose prose)* | A recorded occurrence in a person's journey (shared, clicked, converted, reward earned). | event ~2457 occ vs step 651. **Prose only** — see "step". |
| **step** *(keep, scoped)* | — using it as a prose synonym for "event" | Keep for the schema field (`step_name`, `stepName`, `person.steps`) and the deliberate journey-structure sense. | Do **not** blanket-replace; that would break valid reporting/API references. |
| **outcome event** | success step, goal step | The event that defines a successful referral for a program (converted, account opened, loan funded, …). | Newer precise reporting term; 11 occ / 5 files. |
| **conversion / converted** | — | A friend completing the program's goal action. | conversion 780, converted 102. |
| **program** | campaign *(when you mean the use case)* | The overall referral use case: audience + outcome (Refer A Friend, Welcome Offer, Ambassador…). | Distinct from campaign — see `programs-vs-campaigns.md`. |
| **campaign** | program *(when you mean an implementation)* | A specific implementation within a program: creative, behavior, and rules. | "Within a program, you will have one or multiple campaigns." |
| **journey** | funnel *(loosely)* | The end-to-end path a participant takes through a program. | 211 occ / 74 files. |
| **participant journey** | — | A journey with one person and no referrer/referred relationship (welcome offer, loyalty). | |
| **referral journey** | — | A journey with two people: an advocate and a friend. | |
| **participant** | user *(loosely)* | A person moving through a program or journey. | Also names a journey type. |
| **person / profile** | user, consumer *(in data prose)* | The neutral platform entity for any tracked individual. | Use in reporting/data docs. |
| **reward** | incentive *(loosely)* | The value delivered to advocates or friends for qualifying actions. | 3097 occ / 262 files. |
| **fulfillment** | delivery *(loosely)* | The issuance and delivery of a reward. | |
| **share / share experience / share link** | — | The act of sharing; the UI where advocates share; the trackable per-advocate referral URL. | Set phrases; "share experience" 210 occ. |
| **promotion** | promo *(in prose)* | A placement or message prompting a person to share or engage. | "Promo" acceptable as a product label. |
| **landing page** | microsite | The page a friend lands on from a share. | From the Extole Style Guide. |
| **pop-up** | lightbox | An overlay share/offer experience. | Style Guide (customer-facing). |
| **outbound** | off-site | Sharing/traffic that leaves the brand's site. | Style Guide. |
| **quality engine / quality rules** | fraud engine / fraud rules | Extole's validity/anti-abuse system. | Style Guide; avoid discussing internals in customer docs. |
| **CTA (Call-to-Action)** | — | A prompt in a placement/email that drives a share. | 532 occ. |
| **zone** | — | A named placement slot where creative renders. | 268 occ. |
| **creative** | asset *(loosely)* | The visual and copy components of a campaign experience. | 290 occ. |
| **audience** | segment *(when you mean the targeting group)* | A targetable group of people; programs/campaigns target audiences. | 436 occ. |
| **segment** | audience *(when you mean a filtered subset)* | A filtered subset of people defined by behavior or data. | 243 occ. |
| **attribution** | — | Assigning credit for an event to a source or advocate. | 56 occ. |
| **super advocate** | power user | A top-performing advocate by conversions, revenue, or shares. | 45 occ. |
| **Ambassador (program)** | Influencer (program) | The program type for ongoing brand ambassadors. | Official rename — "Influencer" is the old name. |
| **My Extole** | MyExtole, my.extole *(as the product name)* | The client-facing application. | 328 occ; `my.extole.com` is fine as the URL. |

## UI actions vs. event names — the important caveat

Use **"click"** for **UI action instructions** in customer-facing docs ("click **Create**") — most readers are on a computer. Reserve **"tap"** for in-app placements and mobile SDK contexts, where tapping is the actual gesture. This is a UI-verb choice only; it does **not** apply to **event names**: `promotion clicked`, `share clicked`, `signed up`, `converted`, `shared`, `referred` are literal lowercase event values and stay exactly as written. The reviewer's own suggestions used "promotion clicked" and "share clicked" — because they are events, not instructions.

## Open decisions — need a human call before an agent enforces them

These are genuinely split in the corpus. Listed here so the docs team can decide; until then, agents match the surrounding page and flag the inconsistency.

1. **client vs. customer for the paying brand.** "Extole Client" is used precisely in legal/compliance docs (the brand = data controller), but "customer" is used for *both* the brand and the brand's end shoppers. **Proposal:** "client" = the brand that buys Extole; "customer" = the brand's end person. Needs sign-off.
2. **Report / product-name formatting.** Live variants: `Events Report`, `Events report`, `events report`, `event report`; bold-whole-name vs bold-distinguishing-word (`**Events** report`) vs plain. **Proposal:** capitalize the report name, lowercase "report", bold the name on first mention only (e.g. **Events** report). Needs sign-off.
3. **"Refer A Friend" casing.** At least six spellings (`Refer A Friend`, `Refer a Friend`, `Refer-a-Friend`, `refer-a-friend`, …). **Proposal:** `Refer A Friend` as the program name; `refer-a-friend` only for slugs/labels.
4. **"step" scope confirmation.** Confirm the keep-for-schema / replace-in-prose rule (above) so a lint pass never rewrites `step_name`.
5. **Callout syntax.** None exists today (only `>` blockquotes and `**Note**:`). If admonitions are wanted, pick one ReadMe-compatible form.
6. **Headings vs bold-line pseudo-headings.** Newer pages use bold lines instead of `##`, which breaks ReadMe's TOC. **Proposal:** always use `##`.

## De-hedge lint targets (safe to remove in prose)

`in order to` → `to` (109 occ) · `just` (102) · `simply` (60) · `note that` (37) · `please note` (26) · `very` (25) · `keep in mind` (6) · `really` (6) · `essentially` (3). Also prefer **distinct** over **different** when separating two concepts.
