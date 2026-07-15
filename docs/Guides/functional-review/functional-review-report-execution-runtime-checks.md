---
title: "Functional Review: Report Execution + Runtime Checks"
slug: functional-review-report-execution-runtime-checks
excerpt: "Canonical execution rules for a Functional Review — queue, hard stop, expectation manifest, completion gate, and output format."
hidden: true
---

Use this guide for the **report-execution and runtime-check** portion of a Functional Review on **one live V10 referral or rewards program**.

This is the canonical execution-law doc. Check docs inherit these rules; do not skip them when loading only a single check page.

Use this after [Overview](doc:functional-review-overview) has identified:

- client
- program label or LIVE campaign id
- review window
- containers to review
- whether V10 flow-builder is confirmed

## Review window

Use the same review window for every report.

| Default | Value |
|---|---|
| `time_range` | `LAST_MONTH` |
| Meaning | Rolling 30-day window ending on the day the review starts (not a calendar month) |
| `event_names` | `all` (unless a check doc requires graph-derived names) |

Record start and end dates in the review header.

## Container handling

Run checklist reports across **all containers**:

- production
- sandbox/test

Primary evidence for launch sign-off still comes from **production** traffic and outcomes.

Flag production-like activity in sandbox/test, for example:

- live partner ids
- non-test emails
- material step/reward volume outside production

Say which container each finding came from when counts differ.

## Execution queue rule

Before running any report, build a single execution queue containing every report and source required by the review.

### Required queue manifest

Before submitting the first report, create an internal queue manifest with:

- report/source name
- required parameters
- submission status
- report id
- report URL
- final state

Submission of the first report is **not allowed** until every required item is in the manifest.

Process the queue in one continuous run:

- A failed report/source, missing parameter, invalid parameter, unavailable report type, or discovery requirement must **never** block submission of later queued items.
- Continuing the queue does **not** satisfy the failed section. Failed, invalid, pending, empty, or needs-discovery items must be revisited at the Final-output gate and classified as: Failed attempt, Needs discovery, Invalid execution, Pending, or Empty/Inconclusive.

> 🚧 **"Continue the queue" does not mean "skip the checklist section."**

For each report/source section, complete this decision path:

1. Attempt the required report/source with the documented parameters.
2. If the attempt fails, record: report/source name, attempted parameters, exact error, and failure cause (invalid parameters, missing discovery, unavailable report type, pending status, or empty/inconclusive output).
3. Re-read the specific report section and verify section-level conditions:
   - required parameters used exactly as documented
   - required mappings/filters used exactly as documented
   - required graph-derived values supplied (`step_names`, `triggerEventNames`, `eventNames`, campaign id, program label, container)
   - status check completed
   - completed report downloaded
   - required headers/fields present
   - report output analyzed against graph/config expectation
4. If any section-level condition was not met, classify as one of:
   - **Failed attempt** — tool/report failed despite documented parameters
   - **Needs discovery** — required graph/config/report parameter value was not yet resolved
   - **Invalid execution** — assistant used incorrect or incomplete parameters
   - **Pending** — report submitted but not complete
   - **Empty/Inconclusive** — report completed but output does not answer the section question
5. Continue submitting later queue items, but do **not** treat the failed/incomplete section as reviewed.
6. Before final output, revisit every failed, invalid, pending, empty, or needs-discovery item and check whether a safe immediate correction is available.
7. If a correction is obvious from the report section or already-known campaign graph values, rerun before final analysis.
8. If correction is not possible in the current run, list the item in Evidence Gaps with the exact unmet section condition.

The final verdict must distinguish between:

- campaign/runtime issues
- true evidence gaps
- assistant execution errors
- pending reports
- inconclusive report output

> ❗️ **Do not convert an assistant execution error into a campaign finding.**

**Only stop condition:** all queued reports/sources have been attempted, and every successfully submitted report has reached a terminal state — completed, downloaded, and analyzed, or failed with the exact error recorded.

> 🚧 **Pending is not a terminal state.**
>
> A report that is pending, queued, or running must be waited on — not written off as an evidence gap. If any submitted report is still pending, do **not** produce the final output; wait for the report completion callback (or re-check status) and resume the review when the report finishes. Only a report that terminally failed, or whose report type is genuinely unavailable, may appear in Evidence Gaps with report links/status/errors.

Flag anything that matches each check doc’s **Look for** / **Flag if** guidance.

## Hard stop: no analysis before queue completion

> 🚧 **Hard stop**
>
> The assistant MUST NOT analyze results, summarize findings, give preliminary observations, provide a verdict, provide a progress report, ask whether it should continue, or stop after a subset of reports — until **all** of the following are true:

- Every report and source listed for the review has been attempted
- Every successfully submitted report has reached a terminal state: completed, or failed with the exact error recorded. Pending, queued, or running is not terminal — wait for completion instead of proceeding
- Every completed report has been downloaded
- Every downloaded report has passed required field/header validation before analysis

If these conditions are not met, continue executing the queue, or wait for outstanding reports to complete. Posting results to a Jira ticket counts as analysis and is equally forbidden before these conditions are met.

Parameter discovery, report-type lookup, or a failed report submission does **not** satisfy the stop condition and must not interrupt submission of later queued reports.

## Core sanity-check principle

Reports are only half of the review. The campaign graph/configuration is the other half.

For every checklist item, first inspect the graph to determine what the program is configured to do, then compare the report output to that expectation.

> ❗️ **Do not judge reports in isolation.**
>
> Do not assume event names, reward triggers, limits, emails, webhooks, or eligibility rules from campaign names or generic program patterns. Use the graph to define expected behavior and reports to confirm observed behavior.

### Graph-derived expectation manifest

Before analyzing report output, build a graph-derived expectation manifest for the program under review.

Do **not** use business-event / targetable-step component names as expected raw input event names unless the trigger rule explicitly uses the same name.

For each business-event / targetable-step component, record:

- business-event / targetable-step component name
- display name
- configured `triggerEventNames` / `eventNames` from the Input Event trigger rule
- required or configured data fields under the component
- rules that depend on event data values
- reward/action side effects
- configured unique/partner event key (dedup/idempotency, config only) — fields whose `key_type` is `UNIQUE_PARTNER_EVENT_KEY` (from the built campaign)

Keep these categories separate during analysis:

1. **Expected raw trigger events** — from `triggerEventNames` / `eventNames` in campaign graph trigger rules
2. **Actual raw inbound events** — from Input Events Count and Input Records
3. **Processed campaign events or outcomes** — from Conversion Audit, Rewards, Email, Webhook, or other downstream reports

Do not describe Conversion Audit Event Name values as client-sent raw event names unless the same names are independently present in Input Events Count or Input Records.

Empty reports, unexpected volume, or missing outcomes must be interpreted against the graph:

| Pattern | Interpretation |
|---|---|
| active in graph + no report evidence | possible integration/configuration gap or no eligible volume |
| not active in graph + report activity | possible stale/legacy/misrouted traffic |
| report parameters do not match graph-derived events/steps | rerun or mark evidence gap |

Only reports explicitly listed in these Functional Review docs may be run. Each report must be scoped to the campaign under investigation using the applicable entity, mapping, filter, and aggregation syntax. See:

- [Entities and Context Available in Extole's Configurable Reporting System](doc:entities-and-context-available-in-extole-s-configurable-reporting-system)
- [Custom Data Queries Using Extole Reports](doc:custom-data-queries-using-extole-reports)

## Report reuse window

Before submitting a new report, reuse an existing report of the same type with the same parameters when one was created in the last **2 days**, unless the requester explicitly asks for fresh data. Note in the review header when reused reports contributed evidence.

## Profile identity and unique-key validation

A data field can be configured as a unique partner event key (`key_type = UNIQUE_PARTNER_EVENT_KEY`). Extole uses these keys for two jobs: to de-duplicate inbound events — two events sharing the value are treated as the same event — and to identify the person an event belongs to when no stronger identity, such as email, is present. A unique key must therefore be unique to one event or one person. This check is configuration-derived: run it from the built campaign so it holds even when no report is available.

Also check partner-key **consistency** across the campaign (more than one distinct configured key) in [Event Data Rule Alignment](doc:functional-review-event-data-rule-alignment) — Partner event key consistency (configuration only).

### Build the key manifest from the graph

For every business-event / targetable-step, read each data field's `key_type` from the built campaign (`extole_campaign_get` with `built: true`), and list the fields whose `key_type` is `UNIQUE_PARTNER_EVENT_KEY`. Do not read `key_type` from per-component settings — inherited or template values are unreliable; use the built campaign.

### What makes a valid unique key

- Valid — a value unique to a single event or person: an order id, transaction id, event id, sign-up id, partner user id, partner conversion id, membership id, or reward id.
- Almost never valid — a shared or low-cardinality attribute that many people or many events have in common:
  - postal / geographic: street address, city, state, zip, country
  - contact / personal: phone number, first name, last name, full name, date of birth
  - plan / product descriptors: product, plan, tier, package, speed, product combination
  - dates: event date, day
  - demographic / classification: customer class, segment, type, status
- Borderline — an account-level identifier (customer account number, loyalty id) used as the per-event key. It is unique to an account but not to an event, so when one account legitimately produces repeated events, de-duplication drops the repeats.

### Why a bad unique key is serious

When a shared attribute is a unique partner event key, two failure modes follow:

1. Profile contamination and misattribution. Distinct people who share the value — same city, same zip, same phone number — are identified as the same person, so their events merge onto one profile. An anonymous event that carries no email but does carry the shared attribute attaches to an existing identified profile that happens to match. People then receive events, audiences, or outcomes that are not theirs.
2. Event de-duplication collisions. Distinct events that share the value are treated as duplicates, so legitimate events are dropped and downstream counts, conversions, and rewards are under-recognized.

### Corroborate at runtime

Confirm a suspected bad key against the reports already in the queue:

- Input Records — the same unique-key value appears across multiple distinct person ids. A genuine unique key maps one value to one person.
- Input Records / Input Events — anonymous or email-less events resolve onto profiles that already have an email, or a small set of profiles absorbs a disproportionate share of events.
- Conversion Audit — attribution or profile merges that only make sense if separate people were identified as one.

### Severity guide

- A shared or low-cardinality attribute (address, city, state, zip, phone number, name, date, plan/product descriptor, demographic/class) configured as a unique partner event key → **Issue**. Report the step, the field, and the runtime corroboration when available.
- An account-level identifier used as the per-event unique key on a step where one account can produce repeated events → **Watch**.
- Every unique key is a genuinely per-event or per-person identifier → **Pass** for this check.

Record identity-key findings under Anomalies and concerns, and list the fields inspected under Evidence.

## Final-output gate / Completion gate

Before writing findings, evidence gaps, execution errors, or a verdict, verify every required report/source section individually.

For each required report/source, answer:

- Was the documented report/source attempted?
- Were the documented parameters used exactly as specified?
- Were required mappings/filters used exactly as documented?
- Were graph-derived parameters required by this section resolved and supplied?
- If the first attempt failed, was the failure due to campaign/data behavior or assistant execution?
- If assistant execution was wrong, was a corrected rerun attempted?
- If a corrected rerun was not attempted, why not?
- Was the report status checked?
- If complete, was it downloaded?
- If downloaded, did it contain the required fields?
- Was the result compared to graph/config expectations?

If any required condition is unmet, the item is **not reviewed** and must appear under Evidence Gaps or Execution Errors.

> ❗️ Do not convert an assistant execution error into a campaign finding.
>
> Do not treat a failed, invalid, pending, empty, or needs-discovery item as reviewed.

### Required attempt checklist

Before producing output, verify:

- INPUT_EVENTS_COUNT attempted
- INPUT_EVENTS_WITH_TRIGGERED_STEPS attempted
- CONFIGURABLE_INPUT_RECORDS attempted
- Event Data Rule Alignment attempted (after Input Records)
- Partner event key consistency checked (config only, Event Data Rule Alignment)
- Profile identity / unique-key hygiene checked (built campaign `key_type = UNIQUE_PARTNER_EVENT_KEY`)
- Conversion Audit attempted
- CONFIGURABLE_REWARDS attempted
- TOP_PROMOTION_SOURCES_V2 attempted
- WEBHOOK_EVENTS attempted (when webhooks configured)
- WEBHOOK_DISPATCH_RESULT_EVENTS attempted (when webhooks configured)
- EMAIL_DELIVERABILITY attempted
- campaign graph/configuration reviewed for each checklist item
- Terms alignment attempted (or listed as deferred with reason)
- every submitted report reached a terminal state (completed or failed) — no report is still pending, queued, or running
- every completed report downloaded
- every completed report analyzed

A pending report never satisfies this gate. If any submitted report is still pending, do not produce the final output or post to the ticket — wait for the report completion callback (or re-check status) and resume when every report is terminal.

If any checkbox cannot be marked complete after all reports are terminal, the output MUST contain an Evidence Gaps or Execution Errors section listing:

- missing item
- report id, if any
- current status
- error
- classification: Evidence Gap or Execution Error
- whether a corrected rerun was attempted

## Output format

Deliver a short report with:

- **Header** — client, program, review window, start and end dates, campaign id, V10 confirmed
- **Summary** — review verdict and one paragraph
- **Findings by section** — observation, report links, flags, recommended next step
- **Evidence gaps** — anything not checked, failed, pending, or not available from reports
- **Execution errors** — assistant/tool execution mistakes, invalid parameters, missing required mappings, omitted graph-derived parameters, or incorrect rerun handling

When event/runtime behavior is reviewed, the final report must also separate:

1. **Expected raw trigger events** — source: campaign graph `triggerEventNames` / `eventNames`
2. **Actual raw inbound events** — source: Input Events Count / Input Records
3. **Processed campaign events / outcomes** — source: Conversion Audit, Rewards, Email, Webhook reports
4. **Event mapping gaps** — expected trigger events with no inbound evidence; inbound events with no configured step mapping; processed outcomes with unclear raw-event evidence
5. **Data validation gaps** — expected fields, missing fields, malformed fields, sample count checked

Use thousands separators on counts. Prefer step and program names over internal ids in prose.

## Review verdict definitions

| Verdict | Meaning |
|---|---|
| Pass | No material runtime flags found |
| Watch | Non-blocking anomaly or low-confidence concern worth monitoring |
| Issue | Evidence of a material problem that may affect users, rewards, tracking, emails, or integrations |
| Needs investigation | Reports are missing, inconclusive, contradictory, or there is not enough traffic to conclude |

## Check docs

- [Input / Runtime Event Validation](doc:functional-review-input-runtime-event-validation)
- [Event Data Rule Alignment](doc:functional-review-event-data-rule-alignment)
- [Conversion & Reward Validation](doc:functional-review-conversion-reward-validation)
- [Email / Webhook / Side-Effect Validation](doc:functional-review-email-webhook-side-effect-validation)
- [Terms, Rewards, and Configuration Alignment](doc:functional-review-terms-rewards-and-configuration-alignment)
