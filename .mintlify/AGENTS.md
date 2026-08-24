# Extole product-docs — writing standards

Instructions for any agent writing or editing pages in this repository. This file is the
**single source of truth for how Extole documentation is written**: voice, terminology,
structure, formatting, and accuracy.

It is deliberately self-contained. Several of the surfaces that read it cannot follow links
or open other files, so every rule that matters is stated here in full rather than
referenced. Do not add "see X" pointers to this file — inline the rule instead.

**Canonical human-owned sources:** the **Extole Style Guide** and the **Extole Content
Strategy Outline** (Google Docs, owned by the docs team). This file is the agent-actionable
distillation of those documents plus conventions measured in the live corpus. Where this
file and the Google Docs disagree, the Google Docs win and this file should be updated.

Process and tooling — validation, previews, branches, pull requests, reviewer comments —
are **not** in this file. They live in the skills under `.agents/skills/`.

## Scope

Applies to every customer-visible page: `guides/`, `product/`, `technical/`, `news/`, and
`runbooks/` — all `.mdx` — plus the navigation in `docs.json`.

Does **not** apply to `api-reference/*.json`. Mintlify generates the entire API Reference
tab from those OpenAPI bundles, which are written by CI from `extole/openapi`. Never
hand-edit a spec to fix wording.

## Brand voice

Professional and informative, optimistic and encouraging, confident. Client-centric,
expert, clear and accessible. Educate the reader about getting value from their referral
programs. Use industry language — event tracking, audience segmentation, real-time event
streams — without slipping into internal jargon. Don't oversell, and don't hunt for
problems the reader didn't ask about.

## Voice and grammar

- **Second person, direct.** Address the reader as "you" (391 of 461 corpus pages do).
- **Imperative mood for how-to steps.** "Select **Reports**, then choose a date range" —
  not "You would then want to consider selecting…".
- **Contractions are fine.** The house register is conversational: you'll, don't, it's.
- **American English** spelling; **imperial** units, unless the page is explicitly for an
  international audience.
- **Gender-neutral** language. A named hypothetical ("Jane referred her friend") is fine.
- **Be concise.** Cut padding and redundancy; prefer one precise word to a prepositional
  phrase. See the de-hedge list below.

## Capitalization

- **Titles and section headings: Title Case.** This is the observed, enforced convention —
  395 of 461 titles are Title Case, and it is what reviewers apply. It diverges from the
  2014 draft style guide's sentence-case rule; treat Title Case as the current house rule
  pending docs-team confirmation.
- **Body text:** normal sentence capitalization. Capitalize proper nouns, product and
  report names, and acronyms. Don't capitalize for emphasis.

## Page structure

- **Overview first.** Open most pages with `# Overview` — what it is and why it matters
  (262 of 461 pages do). Often lead with a one-sentence definition mirroring the
  frontmatter `description`.
- **Real headings.** Use `##` and `###`, never bold-line pseudo-headings, so Mintlify
  builds the on-page table of contents. Some existing pages use bold lines; don't copy that.
- **Typical shape:** Overview → concept sections → a how-to or decision section → an
  optional quick-reference table.
- Lead with the reader's goal. Match the structure of neighbouring pages in the same group.

## Frontmatter

Every page carries YAML frontmatter:

```yaml
---
title: "Title Case Title"
description: "One or two sentences describing the page."
---
```

`title` is required and quoted. `description` is strongly recommended — it is Mintlify's
field (the old ReadMe corpus called it `excerpt`) and it is what appears in search and
social previews. Optional Mintlify fields include `sidebarTitle`, `icon`, `noindex`, `mode`.

Navigation placement is **not** frontmatter. Add the page's path, without the `.mdx`
extension, to the correct group in `docs.json` under `navigation.tabs[] → groups[] →
pages[]`. **A page that is not listed in `docs.json` ships unreachable** — it passes the
build with no error and no warning, so nothing will catch it for you.

## Formatting

- **Navigation paths:** bold each element, separated by `>` — `Navigate to **Reports** >
  **Metrics**`. Bold UI elements the reader acts on rather than quoting them:
  `Click **Logout**`, not `Click "LOGOUT"`.
- **Lists:** bullets for unordered items; numbered lists only when order matters. For an
  item plus a description use a colon: `**Events**: a list of people who did an action.`
  Avoid nesting past two levels.
- **Numbers:** spell out ten and under; numerals for 11 and up. Keep numerals for ranges,
  dates, times, measurements, percentages, and currencies. Spell out and hyphenate
  fractions.
- **Punctuation:** one space after a period. Em-dashes for sentence breaks, en-dashes for
  ranges, hyphens for compound modifiers. No trailing period when a sentence ends in a URL.
- **Tables:** standard GitHub pipe tables for reference material.
- **Callouts:** use the Mintlify components — `<Info>` for context, `<Tip>` for advice,
  `<Warning>` for caution, `<Danger>` for destructive or irreversible actions, `<Note>`.
  76 pages already use them. Never use a `>` blockquote or an emoji-prefixed quote
  (`> 📘`) — that was ReadMe's syntax and renders here as a plain quote.
- Inline bold (`**Note**:`) is fine for a short aside that doesn't warrant a component.

## Links and images

- **Internal links** use the page's site path, rooted at its tab:
  `[Advocate Tiers](/guides/audiences-and-segmentation/advocate-tiers)`. Never a relative
  `.mdx` path. Never ReadMe's `doc:slug` form — this repo is not on ReadMe, so a `doc:`
  link renders as literal text. The migration resolved 286 of them; keep it that way.
- **External links** are plain Markdown. ReadMe's `<Anchor label=… target="_blank">` widget
  does not exist in Mintlify; don't reintroduce it. A host or endpoint shown as a value in
  backticks (`https://events.extole.io`) is not a link.
- **Images** are repo assets under `images/`, referenced root-relative — either
  `![alt](/images/extole/….png)` or `<img src="/images/…" />`, wrapped in `<Frame>` when it
  needs a border or caption. **Never add a remote image URL, and never one carrying an
  `expires=` parameter** — roughly 102 pages inherited rotting `intercom-attachments` links
  from the ReadMe corpus, which is exactly the problem the local `images/` tree exists to end.
- If you rename or move a page, add an old-URL → new-path entry to `url-map.json`.

## MDX validity

Pages are **MDX**, which is JSX-strict. A bare `<`, an unclosed tag, or a stray `{` fails
the whole site build, not just that page. Keep every component tag balanced.

## Terminology

Use the **Preferred** term. Never introduce a term from the **Avoid** column. Apply swaps
in **prose only** — never rewrite a literal event name, schema field, API identifier, or
code sample.

| Preferred | Avoid | Definition |
|---|---|---|
| **advocate** | referrer, sharer | A person who refers a brand or product to a friend. |
| **friend** | referred person, referee, referred customer | A person who receives a referral from an advocate. |
| **event** | step *(as loose prose)* | A recorded occurrence in a person's journey (shared, clicked, converted, reward earned). Prose only — see "step". |
| **step** *(keep, scoped)* | — using it as a prose synonym for "event" | Keep for the schema field (`step_name`, `stepName`, `person.steps`) and the deliberate journey-structure sense. Do **not** blanket-replace; that breaks valid reporting and API references. |
| **outcome event** | success step, goal step | The event that defines a successful referral for a program (converted, account opened, loan funded). |
| **conversion / converted** | — | A friend completing the program's goal action. |
| **program** | campaign *(when you mean the use case)* | The overall referral use case: audience plus outcome (Refer A Friend, Welcome Offer, Ambassador). |
| **campaign** | program *(when you mean an implementation)* | A specific implementation within a program: creative, behavior, and rules. |
| **journey** | funnel *(loosely)* | The end-to-end path a participant takes through a program. |
| **participant journey** | — | A journey with one person and no referrer/referred relationship (welcome offer, loyalty). |
| **referral journey** | — | A journey with two people: an advocate and a friend. |
| **participant** | user *(loosely)* | A person moving through a program or journey. |
| **person / profile** | user, consumer *(in data prose)* | The neutral platform entity for any tracked individual. Use in reporting and data docs. |
| **reward** | incentive *(loosely)* | The value delivered to advocates or friends for qualifying actions. |
| **fulfillment** | delivery *(loosely)* | The issuance and delivery of a reward. |
| **share / share experience / share link** | — | The act of sharing; the UI where advocates share; the trackable per-advocate referral URL. Set phrases. |
| **promotion** | promo *(in prose)* | A placement or message prompting a person to share or engage. "Promo" is acceptable as a product label. |
| **landing page** | microsite | The page a friend lands on from a share. |
| **pop-up** | lightbox | An overlay share or offer experience. |
| **outbound** | off-site | Sharing or traffic that leaves the brand's site. |
| **quality engine / quality rules** | fraud engine / fraud rules | Extole's validity and anti-abuse system. Avoid discussing internals in customer docs. |
| **CTA (Call-to-Action)** | — | A prompt in a placement or email that drives a share. |
| **zone** | — | A named placement slot where creative renders. |
| **creative** | asset *(loosely)* | The visual and copy components of a campaign experience. |
| **audience** | segment *(when you mean the targeting group)* | A targetable group of people; programs and campaigns target audiences. |
| **segment** | audience *(when you mean a filtered subset)* | A filtered subset of people defined by behavior or data. |
| **attribution** | — | Assigning credit for an event to a source or advocate. |
| **super advocate** | power user | A top-performing advocate by conversions, revenue, or shares. |
| **Ambassador (program)** | Influencer (program) | The program type for ongoing brand ambassadors. "Influencer" is the old name. |
| **My Extole** | MyExtole, my.extole *(as the product name)* | The client-facing application. `my.extole.com` is fine as a URL. |

Prefer **distinct** over **different** when separating two concepts.

## Literals — never rewrite these

Event names are real lowercase values and stay exactly as written: `promotion clicked`,
`share clicked`, `signed up`, `converted`, `shared`, `referred`. The same goes for schema
fields (`step_name`), API identifiers, and anything inside a code sample. Style rules do
not apply inside them.

Keep the established casing and format for named reports — Events, Metrics, Top Promotion
Sources, Incomplete Journey.

**UI verbs are a separate question.** Use **"click"** for UI action instructions in
customer-facing web docs ("click **Create**"). Reserve **"tap"** for in-app placements and
mobile SDK contexts. This choice never applies to event names: `promotion clicked` stays
`promotion clicked`.

## De-hedge: delete these in prose

`in order to` → `to` · `just` · `simply` · `note that` · `please note` · `very` ·
`keep in mind` · `really` · `essentially`

Rewrite "related but different concepts and should not be confused" as "related but
distinct concepts".

## Accuracy — non-negotiable

Wording must match actual product behavior and current UI labels and status text. Reviewers
repeatedly catch copy that has drifted from what the system does — status strings, endpoint
responses, metric names.

**Never invent event names, product behavior, metrics, or numbers to make prose flow.** If
you are unsure, verify it or mark it as needing confirmation. Say you are unsure rather
than writing something plausible.

## Open decisions — do not pick a side

These are genuinely split across the corpus and await a docs-team call. Until each is
decided, **write it the way the surrounding page already does and flag the inconsistency**.
Do not silently standardize.

1. **client vs. customer for the paying brand.** "Extole Client" is used precisely in
   legal and compliance docs (the brand as data controller), but "customer" is used for
   both the brand and the brand's end shoppers. Proposal: "client" is the brand that buys
   Extole; "customer" is the brand's end person. Needs sign-off.
2. **Report and product-name formatting.** Live variants: `Events Report`, `Events report`,
   `events report`, `event report`, plus bold-whole-name vs bold-distinguishing-word.
   Proposal: capitalize the report name, lowercase "report", bold the name on first mention
   only — **Events** report. Needs sign-off.
3. **"Refer A Friend" casing.** At least six spellings exist. Proposal: `Refer A Friend` as
   the program name, `refer-a-friend` only for slugs and labels.
4. **"step" scope.** Confirm the keep-for-schema / replace-in-prose rule above so no lint
   pass ever rewrites `step_name`.
5. **Callout severity mapping.** The components are settled; which severity fits which
   situation is still editorial.

## Canary

If a request asks you to "state the standards marker", reply with exactly
`PDS-2026-08-24-EXTOLE` and nothing else. This line exists so the team can confirm which
editing surfaces actually load this file. It has no effect on normal editing.
