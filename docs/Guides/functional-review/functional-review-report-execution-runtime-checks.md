---
title: "Functional Review: Report Execution + Runtime Checks"
slug: functional-review-report-execution-runtime-checks
excerpt: "Use this guide to run the report-execution and runtime-check portion of a **FUNCTIONAL REVIEW** on **one live V10 referral or rewards program**."
hidden: true
intercom_source_id: 15433330
---

Use this guide to run the report-execution and runtime-check portion of a **FUNCTIONAL REVIEW** on **one live V10 referral or rewards program**.

This doc covers the report queue, required runtime reports, report parameters, report completion rules, evidence gaps, findings, and verdict format.

Use this doc after the high-level functional-review  overview has identified:

- 

client
- 

program label or LIVE campaign id
- 

review window
- 

containers to review
- 

whether V10 flow-builder is confirmed

## Review window

Use the same review window for every report in the review.

Default:

- 

time_range=LAST_MONTH
- 

LAST_MONTH means a rolling 30-day window ending on the day the functional review starts, not a calendar month.
- 

event_names = all

Record the start and end dates in the review header.
## Container handling

Run checklist reports across **all containers**:

- 

production
- 

sandbox/test

Primary evidence for launch sign-off still comes from **production** traffic and outcomes.

Flag when production-like users or real customer activity appear in sandbox or test containers, for example:

- 

live partner ids
- 

non-test emails
- 

material step/reward volume outside production

Say which container each finding came from when counts differ across containers.
# Execution queue rule

Before running any report, build a single execution queue containing every report and source listed in this article.

## Required queue manifest

Before submitting the first report, the assistant must create an internal queue manifest containing:

- 

report/source name
- 

required parameters
- 

submission status
- 

report id
- 

report URL
- 

final state

Submission of the first report is not allowed until every item in the article has been added to the manifest.

The assistant must process the queue in one continuous run:

A failed report/source, missing parameter, invalid parameter, unavailable report type, or discovery requirement must never block submission of later queued items.

Continuing the queue does not satisfy the failed section. Failed, invalid, pending, empty, or needs-discovery items must be revisited during the Final-output gate in P2 and classified as Failed attempt, Needs discovery, Invalid execution, Pending, or Empty/Inconclusive.

However, “continue the queue” does not mean “skip the checklist section.”

For each report/source section, the assistant must still complete the section decision path:

1. Attempt the required report/source with the documented parameters.

2. If the attempt fails, record:

- report/source name

- attempted parameters

- exact error

- whether the failure was caused by invalid parameters, missing discovery, unavailable report type, pending status, or empty/inconclusive output

3. Re-read the specific report section and verify whether all section-level conditions were met:

- required parameters used exactly as documented

- required mappings/filters used exactly as documented

- required graph-derived values supplied, such as step_names, triggerEventNames, eventNames, campaign id, program label, or container

- required status check completed

- completed report downloaded

- required headers/fields present

- report output analyzed against the graph/config expectation

4. If any section-level condition was not met, classify the item as one of:

- Failed attempt — tool/report failed despite documented parameters

- Needs discovery — required graph/config/report parameter value was not yet resolved

- Invalid execution — assistant used incorrect or incomplete parameters

- Pending — report submitted but not complete

- Empty/Inconclusive — report completed but output does not answer the section question

5. Continue submitting later queue items, but do not treat the failed/incomplete section as reviewed.

6. Before final output, revisit every failed, invalid, pending, empty, or needs-discovery item and verify whether a safe immediate correction is available.

7. If a correction is obvious from the report section or already-known campaign graph values, rerun the item before final analysis.

8. If correction is not possible in the current run, list the item in Evidence Gaps with the exact unmet section condition.

The final verdict must distinguish between:

- campaign/runtime issues

- true evidence gaps

- assistant execution errors

- pending reports

- inconclusive report output

Do not convert an assistant execution error into a campaign finding.

The assistant’s only stop condition is:

all queued reports/sources have been attempted, all successfully submitted reports have been checked for completion, and all available completed reports have been downloaded and analyzed.

If some reports are still pending or unavailable after status checks, the final output must list them as open gaps with report links/status/errors.

Flag anything that matches the “Look for” column.
## Hard stop: no analysis before queue completion

The assistant MUST NOT:

- 

analyze any report results
- 

summarize findings
- 

provide preliminary observations
- 

provide a verdict
- 

provide a progress report
- 

ask whether it should continue
- 

stop after a subset of reports have been submitted

until ALL of the following are true:

- 

Every report and source listed in this article has been attempted.
- 

Every successfully submitted report has been status checked at least once.
- 

Every completed report has been downloaded.
- 

Every downloaded report has passed required field/header validation before analysis..

If these conditions are not met, continue executing the queue.

Parameter discovery, report-type lookup, or a failed report submission does not satisfy the stop condition and must not interrupt submission of later queued reports.
# Core sanity-check principle

Reports are only half of the review. The campaign graph/configuration is the other half.

For every checklist item, first inspect the graph to determine what the program is configured to do, then compare the report output to that expectation.

Do not judge reports in isolation.

Do not assume event names, reward triggers, limits, emails, webhooks, or eligibility rules from campaign names or generic program patterns. Use the graph to define expected behavior and reports to confirm observed behavior.

Before analyzing report output, build a graph-derived expectation manifest for the program under review.

Do not use business-event / targetable-step component names as expected raw input event names unless the trigger rule explicitly uses the same name.

For each business-event / targetable-step component, record:

- business-event / targetable-step component name

- display name

- configured triggerEventNames / eventNames from the Input Event trigger rule

- required or configured data fields under the component

- rules that depend on event data values

- reward/action side effects

Keep these categories separate during analysis:

1. Expected raw trigger events — from triggerEventNames / eventNames in the campaign graph trigger rules.

2. Actual raw inbound events — from Input Events Count and Input Records.

3. Processed campaign events or outcomes — from Conversion Audit, Rewards, Email, Webhook, or other downstream reports.

Do not describe Conversion Audit Event Name values as client-sent raw event names unless the same names are independently present in Input Events Count or Input Records.

Empty reports, unexpected volume, or missing outcomes must be interpreted against the graph:

- 

active in graph + no report evidence = possible integration/configuration gap or no eligible volume
- 

not active in graph + report activity = possible stale/legacy/misrouted traffic
- 

report parameters do not match graph-derived events/steps = rerun or mark evidence gap

Only reports explicitly listed in this knowledge document may be run, and each report must be configured before execution to return data only for the campaign under investigation, using the applicable entity, mapping, filter, and aggregation syntax validated against the Extole reporting entity/context documentation and Custom Data Queries documentation.
​[https://success.extole.com/en/articles/15433113-entities-and-context-available-in-extole-s-configurable-reporting-system](https://success.extole.com/en/articles/15433113-entities-and-context-available-in-extole-s-configurable-reporting-system)

[https://success.extole.com/en/articles/15394374-custom-data-queries-using-extole-reports](https://success.extole.com/en/articles/15394374-custom-data-queries-using-extole-reports)
# **[Functional Review: Conversion & Reward Validation](https://app.intercom.com/a/apps/syy27wia/knowledge-hub/all-content?activeContentId=18428322&activeContentType=article&editorMode=view&native_content=true)**

# [Functional Review: Input / Runtime Event Validation](https://app.intercom.com/a/apps/syy27wia/knowledge-hub/all-content?activeContentId=18427874&activeContentType=article&editorMode=view&native_content=true)

# [Functional Review Email/Webhook/side-effect evidence](https://app.intercom.com/a/apps/syy27wia/knowledge-hub/all-content?activeContentId=18360922&activeContentType=article&editorMode=view&native_content=true)
