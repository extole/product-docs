---
title: "Functional Review: Event Data Rule Alignment"
slug: functional-review-event-data-rule-alignment
excerpt: "Compare Input Records event.data samples against trigger and quality rule conditions from the campaign graph."
hidden: true
intercom_source_id: 15851028
---

Use this guide during **Input / Runtime Event Validation** after Input Records has been run with the correct mapping.

> 🚧 **Execution rules apply.** Follow the queue, hard stop, expectation manifest, and completion gate in [Report Execution + Runtime Checks](doc:functional-review-report-execution-runtime-checks) before recording any finding.

This section closes the gap between:

1. **What the client sends** — raw `event.data` from Input Records
2. **What the campaign requires** — trigger and quality rule conditions on each business-event / targetable-step (for example **Event Data Comparison**)

Do not stop at field presence. Validate that sampled payloads **satisfy the configured rule logic**.

## Prerequisites

Before running this check:

1. Campaign graph is loaded for the program under review.
2. **Input Records** has been submitted with the exact mapping:

   `Id=event.id;Client Id=event.clientId;Event Time=event.eventTime;Person Id=person(event.personId).id;Container=event.container;Name=event.name;Api Type=event.apiType;data=event.data;`

3. Input Records used graph-derived `event_names` from `triggerEventNames` / `eventNames` — not business-event component names. On a V8/legacy campaign, use the legacy fallback names from [Input / Runtime Event Validation](doc:functional-review-input-runtime-event-validation).
4. A graph-derived expectation manifest exists (see [Input / Runtime Event Validation](doc:functional-review-input-runtime-event-validation)). On a V8/legacy campaign, the manifest is built from controller/step configuration and its rules are labeled configuration-derived candidates.

## Core principle

For every inbound input event type that can reach a configured business-event step:

```text
graph rule condition  ↔  sampled event.data from Input Records
```

Rules are authoritative. Input Records is evidence.

If a rule would fail on a sampled payload, record a finding even when the field is present and non-empty.

## Step 1 — Build the rule expectation manifest from the graph

For each business-event / targetable-step component under review:

1. Open `triggerRules` and any attached **Quality Rules** / **Reward Rules** that evaluate inbound event data.
2. For each rule that reads `event.data` (or cause-event data), record:

| Field | What to capture |
|-------|-----------------|
| `business_event_component` | Step / component name |
| `rule_phase` | `TRIGGER`, `QUALITY`, `REWARD`, or other |
| `rule_type` | e.g. Event Data Comparison, Expression, legacy data expression |
| `rule_name` | Display name or component id |
| `parameter` | Event data field path (e.g. `passed`, `status`, `product_type`, nested path if configured) |
| `comparison` | equals, does not equal, contains, does not contain, is blank, is not blank, matches regex, does not match regex |
| `expected_value` | Configured comparison value (string); blank for is_blank / is_not_blank |
| `effect_if_fail` | Trigger fail → step not created; Quality fail → low quality; Reward fail → no reward |
| `source_event_names` | Raw input names from the owning Input Event rule `triggerEventNames` / `eventNames` |
| `unique_partner_key` | Configured unique/partner/idempotency key field or expression used for dedup, read from campaign configuration (blank if none) |

### Event Data Comparison (required handling)

For each **Event Data Comparison** rule, treat configuration as a hard contract:

- **Event Data Parameter** → JSON field on inbound `event.data` (supports nested paths / JSONPath-style reads)
- **Comparison** → apply string logic exactly as configured
- **Value** → exact expected literal or regex pattern

Examples the review must enforce:

| Graph condition | Sample must satisfy |
|-----------------|---------------------|
| `passed` **equals** `true` | String value `"true"` after normalization (see below) |
| `status` **equals** `cancelled` | Exact string match — `"canceled"` is a **fail** |
| `product_type` **contains** `subscription` | Substring match on stringified value |
| `order_value` **is not blank** | Value present and non-empty after trim |
| `email_domain` **does not match regex** `...@blocked.com` | Regex evaluation on stringified value |

Do not treat similar strings as equivalent unless the rule uses **contains** or **regex**.  
`canceled` ≠ `cancelled` for **equals**.

### Other rule types

When the graph uses non–Event Data Comparison rules that still depend on event data:

- **Expression / SpEL rules** — extract the data paths and predicates referenced in the expression; validate samples against those predicates where feasible.
- **Legacy data expressions** — record key/value or jsonPath comparisons and apply the same sample-evaluation approach.

If a rule condition cannot be parsed into testable predicates, record **Needs investigation** for that rule — do not silently skip it.

## Partner event key consistency (configuration only)

> ❗️ **Config only.** This check is derived from the campaign graph/configuration alone. Inbound events do not label which field is the unique key. Do **not** infer or validate the key from Input Records or inbound payloads.

**Answers**

- Does this campaign configure more than one distinct unique/partner event key across its business/input events?
- Are earning/reward-path events missing a configured key where the flow expects dedup?

### Procedure

1. From the campaign configuration, for each business-event / input-event / targetable-step, extract the configured unique/partner event key (dedup/idempotency key field or expression). Record it as `unique_partner_key` on the Step 1 manifest.
2. Build the set of distinct non-blank configured keys across the campaign.
3. If more than one distinct key is configured, flag and record each key with its owning event(s).
4. Note any earning/reward-path event with no configured key where the flow expects deduplication or uniqueness.

### Flag if

- More than one distinct unique partner event key is configured across the campaign's events
- An earning/reward path event has no configured key where dedup is expected

### Severity

| Finding | Severity |
|---|---|
| More than one distinct configured unique/partner event key across the campaign | **Issue** |
| Missing key on an earning/reward path where dedup is expected | **Issue** |
| Key configuration cannot be resolved from the graph/config | **Needs investigation** |

### Required output

```text
Partner event keys (config only):
  Key: <configured key field/expression>
    Events: <component names>
  Key: <configured key field/expression>
    Events: <component names>
  Distinct key count: <n>
  Events with no key (where dedup expected): <component names or none>

Verdict: Pass | Issue | Needs investigation
```

## Step 2 — Pull evidence from Input Records

For each `source_event_name` in the manifest:

1. Filter Input Records samples to that event name.
2. Parse the `data` column as JSON for each sample.
3. Record sample count and time window covered.

Minimum sample targets:

- At least **5** recent samples per event type when volume allows
- If fewer than 5 exist, review all available samples and lower confidence accordingly

## Step 3 — Evaluate each sample against each applicable rule

For each sample and each rule on the manifest:

1. Read the configured **parameter** from `event.data` (support nested keys / dot paths).
2. Stringify the observed value the same way the platform does for Event Data Comparison.
3. Apply the configured **comparison** and **expected_value**.
4. Record **pass** or **fail** for that sample + rule pair.

### Normalization rules (Event Data Comparison)

Unless the graph rule explicitly requires otherwise:

- Compare using **string form** of observed vs expected values
- Trim whitespace before **equals** / **does not equal** unless regex says otherwise
- `true`, `"true"`, and boolean true should be noted in findings if types differ but stringify to the same result
- Distinguish in findings:
  - **missing parameter** — key absent from `event.data`
  - **null**
  - **blank string**
  - **wrong value** — present but fails comparison (e.g. `canceled` vs `cancelled`)
  - **wrong type that still stringifies incorrectly** — e.g. numeric `1` vs string `"true"`

### Phase-aware interpretation

| Rule phase | Sample fails rule | Finding |
|------------|-------------------|---------|
| **TRIGGER** | Payload would not create the step | **Issue** — integration sends data that cannot pass the trigger gate |
| **QUALITY** | Payload creates low-quality event | **Watch** or **Issue** depending on volume and reward impact |
| **REWARD** | Payload blocks reward | **Issue** if rewards are expected from this path |

## Step 4 — Cross-check with triggered-step evidence

After sample evaluation, compare against **Input Events with Triggered Steps**:

| Pattern | Likely meaning |
|---------|----------------|
| Inbound volume high, triggered-step volume low, many samples fail trigger rules | **Issue** — data/rule mismatch |
| Inbound volume high, triggered-step volume high, some samples fail quality rules | **Watch** — partial low-quality traffic |
| No inbound samples for a rule's source event | Evidence gap — cannot validate rule alignment |

Triggered-step gaps alone are not sufficient. Always attempt direct `event.data` vs rule comparison when Input Records samples exist.

## Look for

- Rule-dependent fields present but with **wrong literal value** (spelling, casing, boolean string)
- High share of samples failing the same trigger rule on the same event type
- Client always sends a field the rule never checks (unexpected extra fields — **Watch** only if it suggests integration drift)
- Graph expects a nested path but client sends flat structure (or vice versa)
- Regex rules with zero passing samples in the review window
- Trigger rules that gate the step but were omitted from the manifest

## Required output per event type

For each reviewed input event name, include:

```text
Event: <raw input event name>
Business event: <component name>
Samples reviewed: <n> (confidence: high/medium/low)

Rule: <rule name> (<phase>, Event Data Comparison)
  Parameter: <field>
  Expected: <comparison> <value>
  Results: <pass_count>/<sample_count> pass
  Failures:
    - wrong value: <observed> (expected <expected>) — <count> samples
    - missing: <count> samples
    - blank/null: <count> samples

Verdict: Pass | Watch | Issue | Needs investigation
```

Do not paste raw customer payloads or PII. Summarize field-level results only.

## Severity guide

| Finding | Severity |
|---------|----------|
| >25% of samples fail a **TRIGGER** Event Data Comparison on a live earning path | **Issue** |
| Any sample fails a trigger rule on a launch-critical path with low volume | **Issue** or **Needs investigation** |
| Spelling/value mismatch (`canceled` vs `cancelled`) on equals rule | **Issue** |
| 5–25% of samples fail trigger rules | **Watch** |
| Quality-rule-only failures with rewards still issuing on HIGH-quality path | **Watch** |
| Quality-rule failures blocking most rewards | **Issue** |
| Insufficient samples to evaluate a rule | **Needs investigation** |

## Evidence gaps

Record an evidence gap when:

- Input Records returned no samples for a graph-required source event
- Rule condition could not be parsed into testable predicates
- `data=event.data` mapping was not used (invalid execution — rerun Input Records)
- Sample count is zero for a high-volume event type that appears in Input Events Count

## Relationship to other runbooks

- Run **after** Input Records is downloaded ([Input / Runtime Event Validation](doc:functional-review-input-runtime-event-validation)); **before** [Conversion & Reward Validation](doc:functional-review-conversion-reward-validation) conclusions.
- Findings here inform Conversion Audit interpretation (missing outcomes may be caused by trigger-rule data mismatch, not missing integrations).
- Do not replace Terms alignment or email/webhook checks.

## Example finding (illustrative)

**Event:** `account_opened`  
**Rule:** Event Data Comparison — `passed` equals `true` (TRIGGER)  
**Samples:** 20  
**Results:** 14/20 pass; 6/20 have `passed: false`  
**Verdict:** **Issue** — 30% of account_opened events would fail the trigger gate and not create the configured step.
