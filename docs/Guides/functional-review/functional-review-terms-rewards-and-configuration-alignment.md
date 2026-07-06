---
title: "Functional Review: Terms, Rewards, and Configuration Alignment"
slug: functional-review-terms-rewards-and-configuration-alignment
excerpt: "Use this guide to run the Terms/rewards/configuration-alignment portion of a **functional review** on **one live V10 referral or rewards program**: inspect the active Terms creative/component and compare available user-facing reward languag"
hidden: true
intercom_source_id: 15433477
---

Use this guide to run the Terms/rewards/configuration-alignment portion of a **functional review** on **one live V10 referral or rewards program**: inspect the active Terms creative/component and compare available user-facing reward language against the rewards, limits, geography, and qualifying conditions actually configured in the campaign flow.

This part can be performed while reports are generating since it does not rely on report outputs, but requires Terms copy analysis vs campaign configuration.
## Scope

- 

**One program only** — provide a program label, for example refer-a-friend, or a campaign id.
- 

**V10 flow-builder programs only.** Legacy controller-only programs need a different review path.
- 

Configuration is authoritative for “what should happen”; Terms check is supplemental.
- 

Do not perform legal review.
- 

Only check whether available user-facing reward promises match configured reward amount, limits, geography, and qualifying conditions.

## What you need before you start

- 

Client access, with the correct client selected in My.Extole or chat.
- 

Program label or LIVE campaign id.
- 

Optional: rendered Terms page, if available.

## ## Constraints

- Do not use `extole_account_overview` as Terms evidence.

- `extole_account_overview` may only be used for high-level account discovery, such as identifying that a Terms component may exist.

- Before making any Terms finding, the reviewer must fetch the selected live campaign using `extole_campaign_get` with `built = true`.

- Terms copy must come from the active built Terms component’s `termsCopy` variable, usually `components[n].variables[m].values.en`.

- Do not declare Terms copy unavailable, empty, matching, mismatching, or reviewed based on `extole_account_overview`.

- If the built campaign fetch is not performed, fails, or does not expose an active Terms component `termsCopy`, return `Needs investigation`.

- This may run while sanity-check reports are generating.

- Do not analyze report outputs or give an overall sanity-check verdict.

- Inspect only the active Terms creative/component.

- Use built `termsCopy` from the active Terms component itself as the primary Terms source.

- Fetch the full built campaign configuration, for example `extole_campaign_get` with `built = true`, before declaring Terms copy unavailable.

- Do not use campaign overview, root-level variables, inherited variables, repeated experience variables, or raw component settings as the primary Terms source when the active Terms component has built `termsCopy`.

- Do not rely on `built_values` from raw component-setting APIs alone; the active built Terms copy may live in the built campaign `components[n].variables[m].values.<locale>` structure.

- If sources disagree, prefer the active Terms component built `termsCopy` and record the mismatch as diagnostic context.

- Always record the Terms source path used in Evidence.

- Do not require a separately rendered Terms page unless it is already available.

- Do not evaluate each Terms variable separately when a usable built `termsCopy` value is available.

- Evaluate Terms variables only when the available built `termsCopy` contains unresolved placeholders, is empty, or cannot be retrieved.

- Compare reward language in available built `termsCopy` against the rewards actually issued by the campaign flow.

- Use reward configuration as source of truth for issued rewards, not campaign name.

- Follow active reward components, issuers, suppliers, reward-bank settings, and fulfillment configuration as needed.

- Ignore disabled reward flows unless their Terms impact is explicit.

- If available built `termsCopy` or issued reward value cannot be resolved, return `Needs investigation`, not `Issue`.
## Sources

- `extole_campaign_get` with `built = true` to retrieve built `termsCopy` from the active Terms component

- `extole_campaign_overview_get` only to identify campaign/component structure when needed

- active Terms component `termsCopy`, usually `components[n].variables[m].values.en`

- rendered Terms page, if available

- live program configuration:

- rules

- caps

- country lists

- reward components

- issuers

- suppliers

- reward-bank settings

- fulfillment configuration

No report submission required.
## Terms copy source

### Built Terms copy retrieval path

For Terms analysis, use the active **built Terms component** copy as the primary Terms source. Do not rely on campaign overview or raw component settings as the primary Terms evidence.

Preferred retrieval path:

### Built Terms copy retrieval path

Hard stop: do not make a Terms finding unless the active built Terms component `termsCopy` source path is recorded.

`extole_campaign_overview_get` may be used only to identify candidate campaign/component structure. It is not Terms evidence.

If the active built Terms component `termsCopy` cannot be retrieved from the full built campaign configuration, return `Needs investigation` and list the evidence gap.

1. Fetch the selected campaign with full built configuration enabled, for example `extole_campaign_get` with `built = true`.

2. Find the active Terms component in the built campaign, usually a component named `terms` with type `content-v10.0`.

3. Inside that active Terms component, search its `variables` array for a variable where `name = termsCopy`.

4. Use the locale-specific value from that variable, usually `values.en`, as the available Terms copy.

5. Record the exact component source path used, for example:

`built campaign → components[7] terms/content-v10.0 → variables[4] termsCopy → values.en`

Important source-order rule:

- Prefer `termsCopy` from the active Terms component itself.

- Do not use campaign overview as the Terms copy source. Campaign overview may identify the Terms component, but it may not expose the active built Terms copy.

- Do not use root-level, inherited, or repeated `termsCopy` values as the primary source when the active Terms component has its own built `termsCopy`.

- Do not use raw component-setting APIs, such as component setting list/get, as the primary source when built Terms component `termsCopy` is available. Raw settings may expose source, inherited, or unbuilt template values that differ from the active built campaign copy.

- Do not rely on `built_values` from raw component-setting APIs alone.

- If root, campaign-level, related experience, or raw component settings disagree with the active Terms component `termsCopy`, use the active Terms component value for the functional review and record the discrepancy only as diagnostic context.

If the active Terms component cannot be identified:

1. Search the built campaign for components named `terms` or components with a Terms content type/zone.

2. Search those candidate components for `variables[].name = termsCopy`.

3. If multiple candidates exist, prefer the enabled/live Terms component associated with the active campaign experience.

4. Only if no active Terms component can be resolved, search the full built campaign for any `termsCopy` variable and Terms markers such as Terms heading, company name, site URL, or reward phrase.

5. If no built Terms component `termsCopy` can be retrieved, record an Evidence Gap: `Built active Terms component termsCopy could not be retrieved`.

Do not record this evidence gap if only campaign overview was checked. Continue retrieval using the full built campaign configuration first.

Use the available built `termsCopy` value from the active Terms component as the Terms copy for review. Do not require a separately rendered or final creative output unless it is already available.

If multiple Terms copy values are available, prefer the value associated with the active Terms component for the live campaign. Do not evaluate inactive, draft, archived, or disabled Terms creatives unless they appear to affect the live user-facing Terms experience.

If built `termsCopy` is unavailable, empty, inaccessible, or clearly not associated with the active Terms component, record an Evidence Gap and return `Needs investigation`.

Do not infer final Terms language by manually assembling unrelated variables unless the available built `termsCopy` contains unresolved placeholders and the placeholder values are directly available in the same active Terms component/configuration.

If resolving placeholders requires assumptions, unavailable build logic, runtime rendering, personalization, localization, or external creative rendering, do not infer the final copy. Record the limitation as an Evidence Gap and return `Needs investigation`.
## Core configuration-alignment principle

The campaign graph/configuration defines what the program is configured to do.

Do not assume reward amounts, reward triggers, limits, geography, eligibility rules, or qualifying conditions from campaign names or generic program patterns.

Use the graph and live configuration to define expected behavior, then compare the active available termsCopy against that behavior.

Interpret missing or unclear Terms evidence carefully:

- 

available termsCopy available + configured rewards resolved = compare directly
- 

available termsCopy unavailable = Needs investigation
- 

available termsCopy contains unresolved placeholders that cannot be resolved from the same active Terms configuration = Needs investigation
- 

issued reward value cannot be resolved = Needs investigation
- 

Terms promise does not match configured reward behavior = Issue
- 

Terms omit a configured limit or condition that materially affects user-facing expectations = Watch or Issue, depending on impact

## 1. Terms creative description vs actual rules and configurations

## Sources

- `extole_campaign_get` with `built = true` to retrieve built `termsCopy` from the active Terms component

- `extole_campaign_overview_get` only to identify campaign/component structure when needed

- active Terms component `termsCopy`, usually `components[n].variables[m].values.en`

- rendered Terms page, if available

- live program configuration:

- rules

- caps

- country lists

No report submission required.
## Look for

- 

Annual or share caps configured but no evidence limits ever apply, informational unless launch requires proof
- 

Country restrictions in config incompatible with observed traffic or geo mix
- 

Available Terms copy disagrees with live reward amounts, caps, or geography → **Issue**
- 

Rendered Terms page, if available, disagrees with live reward amounts, caps, or geography → **Issue**
- 

Terms say the reward is earned after one condition, but the configured reward rule uses a different condition
- 

Terms promise advocate and friend rewards, but only one side appears configured

Configuration is authoritative for “what should happen”; Terms check is supplemental. Do not perform legal review. Only check whether available user-facing reward promises match configured reward amount, limits, geography, and qualifying conditions.
## 2. Terms and limits

Inspect the active Terms creative/component and its available termsCopy content.

Prefer the termsCopy associated with the active Terms creative/component for the live campaign.

Do not evaluate each Terms variable separately unless the available termsCopy contains unresolved placeholders, is empty, or cannot be retrieved.
## Look for

- 

Reward amount in Terms does not match configured issued reward amount
- 

Reward type in Terms does not match configured issued reward type
- 

Terms mention reward limits that are not configured
- 

Configured caps or limits are missing from Terms when they materially affect the user-facing promise
- 

Country restrictions in Terms do not match configured country lists
- 

Terms describe a qualifying action that differs from the configured trigger or condition
- 

Terms promise both advocate and friend rewards, but only one side appears configured
- 

Terms mention only one side of the reward, but both advocate and friend rewards are configured
- 

Available termsCopy contains unresolved placeholders
- 

Available termsCopy cannot be retrieved
- 

Available termsCopy cannot be confidently associated with the active Terms creative/component

## Severity guide

- 

Available Terms copy disagrees with live reward amounts, caps, geography, or qualifying conditions → **Issue**
- 

Rendered Terms page, if available, disagrees with live reward amounts, caps, geography, or qualifying conditions → **Issue**
- 

Available termsCopy contains unresolved placeholders that cannot be resolved from the same active Terms configuration → **Needs investigation**
- 

Available termsCopy cannot be retrieved → **Needs investigation**
- 

Available termsCopy cannot be confidently associated with the active Terms creative/component → **Needs investigation**
- 

Configured limit exists but Terms impact is unclear → **Watch**
- 

Annual or share caps configured but no evidence limits ever apply → informational unless launch requires proof

## 3. Reward components inspected

Compare reward language in available termsCopy against the rewards actually issued by the campaign flow.

Use reward configuration as source of truth for issued rewards, not campaign name.

Follow active reward components, issuers, suppliers, reward-bank settings, and fulfillment configuration as needed.

Ignore disabled reward flows unless their Terms impact is explicit.
## Inspect

- 

active reward components
- 

reward issuers
- 

reward suppliers
- 

reward-bank settings
- 

fulfillment configuration
- 

advocate reward flow
- 

friend reward flow
- 

trigger and condition logic
- 

disabled reward flows only when their Terms impact is explicit

## Look for

- 

Terms promise an advocate reward, but no advocate reward appears configured
- 

Terms promise a friend reward, but no friend reward appears configured
- 

Configured advocate reward amount differs from Terms
- 

Configured friend reward amount differs from Terms
- 

Configured reward supplier/type differs from Terms
- 

Campaign name suggests one reward type, but actual reward configuration issues another type
- 

Fulfillment configuration changes the reward behavior described in Terms
- 

Active reward flow uses different trigger/condition logic than Terms describe

## 4. Advocate reward: Terms vs issued

Use reward configuration as source of truth for issued rewards.
## Compare

- 

advocate reward language in available termsCopy
- 

configured advocate reward component
- 

configured advocate reward amount
- 

configured advocate reward type
- 

configured advocate reward supplier
- 

configured advocate reward trigger
- 

configured advocate reward conditions
- 

configured advocate reward limits or caps

## Result

Record:

- 

Terms advocate reward promise
- 

configured advocate reward actually issued
- 

whether the reward amount matches
- 

whether the reward type matches
- 

whether the trigger/condition matches
- 

whether limits/caps match
- 

finding:

  - 

**Pass**
  - 

**Watch**
  - 

**Issue**
  - 

**Needs investigation**

## 5. Friend reward: Terms vs issued

Use reward configuration as source of truth for issued rewards.
## Compare

- 

friend reward language in available termsCopy
- 

configured friend reward component
- 

configured friend reward amount
- 

configured friend reward type
- 

configured friend reward supplier
- 

configured friend reward trigger
- 

configured friend reward conditions
- 

configured friend reward limits or caps

## Result

Record:

- 

Terms friend reward promise
- 

configured friend reward actually issued
- 

whether the reward amount matches
- 

whether the reward type matches
- 

whether the trigger/condition matches
- 

whether limits/caps match
- 

finding:

  - 

**Pass**
  - 

**Watch**
  - 

**Issue**
  - 

**Needs investigation**

## 6. Trigger and condition mismatches

Compare reward language in available termsCopy against the configured reward trigger and condition logic.
## Look for

- 

Terms say the reward is earned after one condition, but the configured reward rule uses a different condition
- 

Terms describe a purchase, application, approval, account opening, or other action that does not match the configured trigger
- 

Terms say both people receive rewards at the same stage, but configured rewards trigger at different stages
- 

Terms imply immediate reward, but configured reward requires delayed fulfillment or a later event
- 

Terms imply automatic qualification, but configured reward has eligibility filters or limits
- 

Terms omit a material configured exclusion, cap, or geography condition

## Severity guide

- 

User-facing Terms promise a reward earlier or more broadly than configuration allows → **Issue**
- 

Terms are ambiguous but configuration appears reasonable → **Watch**
- 

Trigger/condition cannot be resolved from available Terms copy or configuration → **Needs investigation**

## Output format

Deliver a short report with:

- 

**Header** — client, program, campaign id, V10 confirmed
- 

**Summary** — configuration-alignment result and one paragraph
- 

**Terms component inspected**
- 

**Available Terms copy inspected** — yes/no
- 

**Reward components inspected**
- 

**Advocate reward: Terms vs issued**
- 

**Friend reward: Terms vs issued**
- 

**Trigger/condition mismatches**
- 

**Evidence gaps** — anything not checked, unavailable, unresolved, or inconclusive
- 

**Result** — Pass / Watch / Issue / Needs investigation
- 

**Evidence**

Do not give an overall sanity-check verdict from this doc alone.

For Terms evidence, include:

- campaign id

- active Terms component id/name

- source type: built active Terms component `termsCopy`

- locale inspected

- exact source path, for example `components[7].variables[4].values.en`

- whether campaign overview was used only for component discovery

- whether raw component settings were checked and whether they matched or differed, if relevant
## Evidence gaps

If any item cannot be checked, include an **Evidence Gaps** section listing:

- 

missing item
- 

current status
- 

error or reason unavailable
- 

whether the gap changes the result

Common evidence gaps:

- 

active Terms creative/component could not be identified
- 

available termsCopy could not be retrieved
- 

available termsCopy is empty or inaccessible
- 

available termsCopy contains unresolved placeholders that cannot be resolved from the same active Terms configuration
- 

multiple conflicting termsCopy values are available and the active one cannot be determined
- 

rendered Terms page unavailable
- 

rendered Terms page differs from available termsCopy, but the source of the difference cannot be resolved
- 

issued reward value could not be resolved
- 

reward supplier or fulfillment configuration could not be resolved
- 

active reward component could not be identified
- 

trigger or condition logic could not be resolved
- 

- built active Terms component `termsCopy` could not be retrieved after checking the full built campaign configuration
- 

only campaign overview was available, and full built campaign configuration could not be fetched
- 

active Terms component could not be distinguished from root-level, inherited, repeated, draft, archived, or disabled Terms copy values

If available termsCopy or issued reward value cannot be resolved, return Needs investigation, not Issue.

If available termsCopy cannot be confidently read or associated with the active Terms creative/component, return Needs investigation, not Issue.

Only mark Issue when readable Terms copy materially conflicts with configured rewards, limits, geography, or qualifying conditions.
## Result definitions

Result

Meaning

**Pass**

No material configuration-alignment flags found

**Watch**

Non-blocking anomaly or low-confidence concern worth monitoring

**Issue**

Evidence of a material mismatch between user-facing Terms and configured rewards, limits, geography, or qualifying conditions

**Needs investigation**

Available Terms copy, issued reward value, configuration, or trigger/condition evidence is missing, inconclusive, or contradictory
