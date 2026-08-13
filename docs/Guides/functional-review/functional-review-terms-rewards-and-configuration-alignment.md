---
title: "Functional Review: Terms, Rewards, and Configuration Alignment"
slug: functional-review-terms-rewards-and-configuration-alignment
excerpt: "Compare active Terms copy against configured rewards, limits, geography, and qualifying conditions for one live program."
hidden: true
---

Use this guide for the Terms / rewards / configuration-alignment portion of a Functional Review on **one live referral or rewards program**.

Inspect the active Terms creative/component and compare available user-facing reward language against the rewards, limits, geography, and qualifying conditions actually configured in the campaign flow.

This part can run while reports are generating — it does not rely on report outputs.

> 🚧 **Execution rules apply for overall FR verdict.** Do not analyze report outputs or give an overall sanity-check verdict from this doc alone. See [Report Execution + Runtime Checks](doc:functional-review-report-execution-runtime-checks).

## Scope

- **One program only** — program label (for example `refer-a-friend`) or campaign id
- **V10 flow-builder is the primary target** — on a V8/legacy campaign, run this check best-effort against the active Terms creative in the built campaign (see the V8/legacy fallback below); campaign version never blocks the rest of the review
- Configuration is authoritative for “what should happen”; Terms check is supplemental
- Do **not** perform legal review
- Only check whether available user-facing reward promises match configured reward amount, limits, geography, and qualifying conditions

## What you need

- Client access, with the correct client selected
- Program label or LIVE campaign id
- Optional: rendered Terms page, if available

## Constraints

> ❗️ **Hard constraints**

- Do **not** use `extole_account_overview` as Terms evidence. It may only be used for high-level account discovery (for example identifying that a Terms component may exist).
- Before making any Terms finding, fetch the selected live campaign using `extole_campaign_get` with `built = true`.
- Terms copy must come from the active built Terms component’s `termsCopy` variable, usually `components[n].variables[m].values.en`.
- Do **not** declare Terms copy unavailable, empty, matching, mismatching, or reviewed based on `extole_account_overview`.
- If the built campaign fetch is not performed, fails, or does not expose an active Terms component `termsCopy`, apply the V8/legacy fallback below; if no usable Terms copy can be retrieved from the built configuration at all, return **Needs investigation** for this section.
- Inspect only the active Terms creative/component.
- Do not use campaign overview, root-level variables, inherited variables, repeated experience variables, or raw component settings as the primary Terms source when the active Terms component has built `termsCopy`.
- Do not rely on `built_values` from raw component-setting APIs alone.
- If sources disagree, prefer the active Terms component built `termsCopy` and record the mismatch as diagnostic context.
- Always record the Terms source path used in Evidence.
- Do not require a separately rendered Terms page unless it is already available.
- Do not evaluate each Terms variable separately when a usable built `termsCopy` value is available. Evaluate Terms variables only when `termsCopy` contains unresolved placeholders, is empty, or cannot be retrieved.
- Treat generic template defaults as unresolved placeholders, not as the client's Terms promise. Values such as `Your Company`, `https://www.yourcompany.com`, or a stock default reward amount (for example a `$20`/`$20` advocate/friend pair on a program whose configured rewards differ) that resolve from component variable defaults are template scaffolding. Never report a Terms/reward mismatch **Issue** based on template-default values — if only template defaults are available, record an Evidence Gap and return **Needs investigation**.
- Compare reward language in available built `termsCopy` against the rewards actually issued by the campaign flow.
- Use reward configuration as source of truth for issued rewards, not campaign name.
- Follow active reward components, issuers, suppliers, reward-bank settings, and fulfillment configuration as needed.
- Ignore disabled reward flows unless their Terms impact is explicit.
- If available built `termsCopy` or issued reward value cannot be resolved, return **Needs investigation**, not **Issue**.

## Sources

| Source | Role |
|---|---|
| `extole_campaign_get` with `built = true` | Primary — retrieve built `termsCopy` from the active Terms component |
| `extole_campaign_overview_get` | Discovery only — identify campaign/component structure |
| active Terms component `termsCopy` | Usually `components[n].variables[m].values.en` |
| rendered Terms page | Optional cross-check if already available |
| live program configuration | rules, caps, country lists, reward components, issuers, suppliers, reward-bank settings, fulfillment |

No report submission required.

## Built Terms copy retrieval path

> 🚧 **Hard stop:** do not make a Terms finding unless the Terms copy source path is recorded — the active built Terms component `termsCopy` on V10, or the built legacy Terms source on V8 (see the V8/legacy fallback below).
>
> If no usable Terms copy can be retrieved from the full built campaign configuration, return **Needs investigation** for this section and list the evidence gap.

Preferred retrieval path:

1. Fetch the selected campaign with full built configuration enabled — `extole_campaign_get` with `built = true`.
2. Find the active Terms component, usually named `terms` with type `content-v10.0`.
3. Inside that component, find `variables[]` where `name = termsCopy`.
4. Use the locale-specific value, usually `values.en`.
5. Record the exact source path, for example:

```text
built campaign → components[7] terms/content-v10.0 → variables[4] termsCopy → values.en
```

### Source-order rules

- Prefer `termsCopy` from the active Terms component itself
- Do not use campaign overview as the Terms copy source
- Do not use root-level, inherited, or repeated `termsCopy` values as the primary source when the active Terms component has its own built `termsCopy`
- Do not use raw component-setting APIs as the primary source when built Terms component `termsCopy` is available
- If root / campaign-level / related experience / raw settings disagree with active Terms `termsCopy`, use the active Terms value and record the discrepancy as diagnostic context only

### If the active Terms component cannot be identified

1. Search the built campaign for components named `terms` or Terms content type/zone.
2. Search those candidates for `variables[].name = termsCopy`.
3. If multiple candidates exist, prefer the enabled/live Terms component associated with the active campaign experience.
4. Only if no active Terms component can be resolved, search the full built campaign for any `termsCopy` and Terms markers.
5. If still unresolved, record Evidence Gap: `Built active Terms component termsCopy could not be retrieved`.

Do **not** record this evidence gap if only campaign overview was checked — continue with full built campaign first.

### V8/legacy fallback

A V8/legacy campaign usually has no `content-v10.0` Terms component. Do not stop at step 1 of the retrieval path:

1. Fetch the full built campaign (`extole_campaign_get` with `built = true`).
2. Look for the active Terms creative/content in the built V8 configuration — a Terms zone, Terms controller, or Terms creative content — and use its built copy as the Terms source.
3. Record the exact V8 source path used, labeled as a legacy Terms source, and note the lower confidence in Evidence.
4. Compare that copy against configured rewards, limits, geography, and qualifying conditions exactly as in the sections below.
5. Only if no usable Terms copy can be retrieved from the built V8 configuration, record the evidence gap and return **Needs investigation** — for this section only, not for the whole review.

Do not evaluate inactive, draft, archived, or disabled Terms creatives unless they appear to affect the live user-facing Terms experience.

Do not infer final Terms language by assembling unrelated variables unless available `termsCopy` contains unresolved placeholders and placeholder values are directly available in the same active Terms component. If resolving placeholders requires assumptions, unavailable build logic, runtime rendering, personalization, localization, or external creative rendering, record an Evidence Gap and return **Needs investigation**.

## Core configuration-alignment principle

The campaign graph/configuration defines what the program is configured to do. Do not assume reward amounts, triggers, limits, geography, eligibility, or qualifying conditions from campaign names or generic patterns.

| Situation | Result |
|---|---|
| `termsCopy` available + configured rewards resolved | compare directly |
| `termsCopy` unavailable | **Needs investigation** |
| `termsCopy` has unresolved placeholders that cannot be resolved from the same active Terms configuration | **Needs investigation** |
| issued reward value cannot be resolved | **Needs investigation** |
| Terms promise does not match configured reward behavior | **Issue** |
| Terms omit a configured limit or condition that materially affects user-facing expectations | **Watch** or **Issue**, depending on impact |

---

## 1. Terms vs configured rules

### Flag if

- Available Terms copy disagrees with live reward amounts, caps, or geography → **Issue**
- Rendered Terms page (if available) disagrees with live reward amounts, caps, or geography → **Issue**
- Terms say the reward is earned after one condition, but the configured reward rule uses a different condition
- Terms promise advocate and friend rewards, but only one side appears configured
- Country restrictions in config incompatible with observed traffic or geo mix
- Annual or share caps configured but no evidence limits ever apply → informational unless launch requires proof

---

## 2. Terms and limits

Prefer the `termsCopy` associated with the active Terms creative/component for the live campaign.

### Flag if

- Reward amount in Terms does not match configured issued reward amount
- Reward type in Terms does not match configured issued reward type
- Terms mention reward limits that are not configured
- Configured caps or limits are missing from Terms when they materially affect the user-facing promise
- Country restrictions in Terms do not match configured country lists
- Terms describe a qualifying action that differs from the configured trigger or condition
- Terms promise both advocate and friend rewards, but only one side appears configured (or the reverse)
- Available `termsCopy` contains unresolved placeholders, cannot be retrieved, or cannot be confidently associated with the active Terms creative/component
- Available `termsCopy` is only generic template defaults (for example `Your Company`, stock `$20`/`$20`) rather than client-specific Terms

### Severity

| Finding | Severity |
|---|---|
| Terms disagree with live reward amounts, caps, geography, or qualifying conditions | **Issue** |
| Rendered Terms page (if available) disagrees with live reward amounts, caps, geography, or qualifying conditions | **Issue** |
| Unresolved placeholders that cannot be resolved from the same active Terms configuration | **Needs investigation** |
| `termsCopy` cannot be retrieved or confidently associated | **Needs investigation** |
| Unresolved placeholders or generic template defaults in **any** configured locale, even when another locale resolves cleanly | **Needs investigation** for this section, recorded under Anomalies and concerns |
| Configured limit exists but Terms impact is unclear | **Watch** |
| Caps configured but no evidence limits ever apply | informational unless launch requires proof |

### Check every configured locale

`termsCopy` usually holds one value per locale (`values.en`, `values.fr`, `values.es`, …). Evaluate each configured locale, and report the result per locale.

A locale left as template scaffolding is a finding in its own right, not a footnote to a clean `en`: that locale's published Terms name another company and promise reward amounts the program does not issue. A resolved `en` does not discharge it, and the section verdict is set by the worst locale rather than by the primary one.

Record it under **Anomalies and concerns**, name the affected locales, and ask whether those locales are exposed to live traffic — that answer sets the real severity and only a human reviewer can supply it. Do not attempt to repair the copy as part of the review.

---

## 3. Reward components to inspect

Compare Terms reward language against rewards actually issued by the campaign flow.

Inspect:

- active reward components, issuers, suppliers
- reward-bank settings, fulfillment configuration
- advocate reward flow, friend reward flow
- trigger and condition logic
- disabled reward flows only when their Terms impact is explicit

### Flag if

- Terms promise an advocate/friend reward but none appears configured
- Configured advocate/friend reward amount, type, or supplier differs from Terms
- Campaign name suggests one reward type, but actual configuration issues another
- Fulfillment configuration changes the reward behavior described in Terms
- Active reward flow uses different trigger/condition logic than Terms describe

---

## 4–5. Advocate and Friend reward: Terms vs issued

Use reward configuration as source of truth for issued rewards.

For **each** of advocate and friend, compare and record:

| Dimension | Terms | Configured | Match? |
|---|---|---|---|
| reward amount | | | |
| reward type | | | |
| reward supplier | | | |
| trigger | | | |
| conditions | | | |
| limits / caps | | | |

**Finding:** Pass / Watch / Issue / Needs investigation

---

## 6. Trigger and condition mismatches

### Flag if

- Terms say the reward is earned after one condition, but the configured reward rule uses a different condition
- Terms describe a purchase, application, approval, account opening, or other action that does not match the configured trigger
- Terms say both people receive rewards at the same stage, but configured rewards trigger at different stages
- Terms imply immediate reward, but configured reward requires delayed fulfillment or a later event
- Terms imply automatic qualification, but configured reward has eligibility filters or limits
- Terms omit a material configured exclusion, cap, or geography condition

### Severity

| Finding | Severity |
|---|---|
| User-facing Terms promise a reward earlier or more broadly than configuration allows | **Issue** |
| Terms are ambiguous but configuration appears reasonable | **Watch** |
| Trigger/condition cannot be resolved from available Terms copy or configuration | **Needs investigation** |

---

## Output format

Deliver a short report with:

- **Header** — client, program, campaign id, V10 confirmed
- **Summary** — configuration-alignment result and one paragraph
- **Terms component inspected**
- **Available Terms copy inspected** — yes/no
- **Reward components inspected**
- **Advocate reward: Terms vs issued**
- **Friend reward: Terms vs issued**
- **Trigger/condition mismatches**
- **Evidence gaps**
- **Result** — Pass / Watch / Issue / Needs investigation
- **Evidence**

For Terms evidence, include:

- campaign id
- active Terms component id/name
- source type: built active Terms component `termsCopy`
- locale inspected
- exact source path (for example `components[7].variables[4].values.en`)
- whether campaign overview was used only for component discovery
- whether raw component settings were checked and whether they matched or differed, if relevant

Do **not** give an overall sanity-check verdict from this doc alone.

## Evidence gaps

If any item cannot be checked, list:

- missing item
- current status
- error or reason unavailable
- whether the gap changes the result

Common evidence gaps:

- active Terms creative/component could not be identified
- available `termsCopy` could not be retrieved, is empty, or inaccessible
- `termsCopy` contains unresolved placeholders that cannot be resolved from the same active Terms configuration
- multiple conflicting `termsCopy` values and the active one cannot be determined
- rendered Terms page unavailable, or differs from `termsCopy` with unresolved source of difference
- issued reward value, supplier, or fulfillment configuration could not be resolved
- active reward component could not be identified
- trigger or condition logic could not be resolved
- built active Terms component `termsCopy` could not be retrieved after checking the full built campaign configuration
- only campaign overview was available, and full built campaign configuration could not be fetched
- active Terms component could not be distinguished from root-level, inherited, repeated, draft, archived, or disabled Terms copy values

> ❗️ If available `termsCopy` or issued reward value cannot be resolved, return **Needs investigation**, not **Issue**.
>
> Only mark **Issue** when readable Terms copy materially conflicts with configured rewards, limits, geography, or qualifying conditions.

## Result definitions

| Result | Meaning |
|---|---|
| Pass | No material configuration-alignment flags found |
| Watch | Non-blocking anomaly or low-confidence concern worth monitoring |
| Issue | Material mismatch between user-facing Terms and configured rewards, limits, geography, or qualifying conditions |
| Needs investigation | Available Terms copy, issued reward value, configuration, or trigger/condition evidence is missing, inconclusive, or contradictory |
