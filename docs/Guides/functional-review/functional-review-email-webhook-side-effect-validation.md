---
title: "Functional Review: Email / Webhook / Side-Effect Validation"
slug: functional-review-email-webhook-side-effect-validation
excerpt: "# 5. Promotion sources"
hidden: true
intercom_source_id: 15436200
---

# 5. Promotion sources

## Reports

- 

TOP_PROMOTION_SOURCES_V2

## Required parameters

- 

campaign_id=<campaign>
- 

time_range=LAST_MONTH
- 

container=all

## Look for

- 

Unusually high Direct share when referral-driven traffic is expected:

  - 

rough guide: Direct above ~70% of attributed promotion events with referral steps configured

- 

Financial- or loan-style programs where attribution likely needs **click** signal:

  - 

promotion_clicked
  - 

share click

Flag when traffic is mostly **view** only.
# 6. Webhook and outbound events

Webhook reports are only applicable when the client has configured webhooks.

Always check webhook configuration before selecting Webhook Events, Webhook Event Metrics, Webhook Dispatch Results, or Webhook Dispatch Result Metrics.
​
## Reports

- 

WEBHOOK_EVENTS
- 

WEBHOOK_DISPATCH_RESULT_EVENTS

## Required parameters

- 

time_range=LAST_MONTH

## Look for

- 

Webhook firing but failing:

  - 

failure rate above ~5% over more than ~50 attempts → **Issue**

- 

Webhook configured on the program but zero dispatches in the window → **Watch**
- 

Failures dominated by 4xx or 5xx → **Issue**

# 7. Email Deliverability

## Reports

- 

EMAIL_DELIVERABILITY

## Optional cross-check

- 

EMAIL_DELIVERABILITY

## Required parameters

- 

campaign_id=<campaign>
- 

time_range=LAST_MONTH
- 

container=all

## Look for

- 

Expected program emails not sending while related steps fired → **Issue**
- 

Bounce or failure rate materially above baseline:

  - 

rough guide: above ~5% → **Watch**
  - 

above ~10% → **Issue** when volume is non-trivial

- 

High suppressions explained by list hygiene → note only
- 

Suppressions plus send failures elsewhere → **Watch**

Distinguish one-off test bounces from program-level deliverability problems.
# Output format

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

If any required condition is unmet, the item is not reviewed and must appear under Evidence Gaps or Execution Errors.

Do not convert an assistant execution error into a campaign finding.

Do not treat a failed, invalid, pending, empty, or needs-discovery item as reviewed.

Before producing output, verify:

- INPUT_EVENTS_COUNT attempted

- INPUT_EVENTS_WITH_TRIGGERED_STEPS attempted

- CONFIGURABLE_INPUT_RECORDS attempted

- Conversion Audit attempted

- CONFIGURABLE_REWARDS attempted

- TOP_PROMOTION_SOURCES_V2 attempted

- WEBHOOK_EVENTS attempted

- WEBHOOK_DISPATCH_RESULT_EVENTS attempted

- EMAIL_DELIVERABILITY attempted

- campaign graph/configuration reviewed for each checklist item

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

## Deliver a short report with

- 

**Header** — client, program, review window, start and end dates, campaign id, V10 confirmed
- 

**Summary** — review verdict and one paragraph
- 

**Findings by section** — observation, report links, flags, recommended next step
- 

**Evidence gaps** — anything not checked, failed, pending, or not available from reports
- 

Execution errors — assistant/tool execution mistakes, invalid parameters, missing required mappings, omitted graph-derived parameters, or incorrect rerun handling

When event/runtime behavior is reviewed, the final report must also separate:

1. Expected raw trigger events

- source: campaign graph triggerEventNames / eventNames

2. Actual raw inbound events

- source: Input Events Count / Input Records

3. Processed campaign events / outcomes

- source: Conversion Audit, Rewards, Email, Webhook reports

4. Event mapping gaps

- expected trigger events with no inbound evidence

- inbound events with no configured step mapping

- processed outcomes with unclear raw-event evidence

5. Data validation gaps

- expected fields

- missing fields

- malformed fields

- sample count checked

Use thousands separators on counts.

Prefer step and program names over internal ids in prose.
# Review verdict definitions

| Verdict | Meaning |
|---|---|
| **Pass** | No material runtime flags found |
| **Watch** | Non-blocking anomaly or low-confidence concern worth monitoring |
| **Issue** | Evidence of a material problem that may affect users, rewards, tracking, emails, or integrations |
| **Needs investigation** | Reports are missing, inconclusive, contradictory, or there is not enough traffic to conclude |
