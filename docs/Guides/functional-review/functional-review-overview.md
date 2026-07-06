---
title: "Functional Review: Overview"
slug: functional-review-overview
excerpt: "Use this guide to run a functional review on one live V10 referral or rewards program."
hidden: true
intercom_source_id: 15384068
---

Use this guide to run a functional review on one live V10 referral or rewards program.

A functional review compares the live campaign configuration and runtime evidence against expected program behavior. It is typically used before launch, after a material program or integration change, or on a scheduled launch-review cadence.

## Scope

This review applies to one V10 flow-builder program at a time.

Provide either:

- program label, for example `refer-a-friend`

- live campaign id

Legacy controller-only programs require a different review path.

## Campaign selection

A functional review must run against one confirmed V10 flow-builder program.

Before report execution, identify the campaign/program scope:

1. If the user provides a program label or live campaign id, use that value.

2. If the user does not provide a campaign/program, discover the available campaign/program list before running reports.

3. If only one eligible V10 campaign exists, run the review against that campaign.

4. If multiple eligible V10 campaigns exist and the user cannot clarify, run the review against the most recently updated or most recently launched/live V10 campaign, and state this selection in the review header.

5. If both V8/legacy and V10 campaigns exist, exclude V8/legacy campaigns unless the user explicitly requested a legacy review path.

6. If no eligible V10 campaign can be confirmed, do not run the V10 functional review. Record an evidence gap: `No eligible V10 campaign could be confirmed`.

7. Do not run one functional review across multiple campaigns unless the user explicitly requested a multi-campaign review.

### Review-header note

When the campaign was selected automatically, include this in the review header:

> Campaign selection: No campaign was specified by the user. Available campaigns were reviewed. The functional review was run against the most recent eligible V10 campaign: `<campaign/program>`. Legacy/V8 campaigns were excluded because this review path applies to V10 flow-builder programs only.

## Default review window

Use a 30-day rolling window ending on the day the review starts.

Record the start and end dates in the review header. Use the same window for every report.

## Container handling

Run checklist reports across all containers, including production and sandbox/test.

Production traffic and outcomes remain the primary evidence for launch sign-off.

Flag production-like users or real customer activity in sandbox/test containers, including live partner ids, non-test emails, or meaningful step/reward volume outside production.

## Review principle

Reports are only half of the review. Campaign graph/configuration is the other half.

For each checklist item:

1. Inspect the campaign graph/configuration to determine expected behavior.

2. Run the relevant report or source.

3. Compare observed report output against the expected behavior.

4. Record findings, flags, evidence gaps, and recommended next steps.

Do not judge reports in isolation.

## Detailed review sections

Use these linked docs for the detailed steps:

- [Functional Review: Report Execution + Runtime Checks](functional-review-report-execution-runtime-checks)
- [Functional Review: Input / Runtime Event Validation](functional-review-input-runtime-event-validation)
- [Functional Review: Event Data Rule Alignment](functional-review-event-data-rule-alignment)
- [Functional Review: Conversion & Reward Validation](functional-review-conversion-reward-validation)
- [Functional Review: Email / Webhook / Side-Effect Validation](functional-review-email-webhook-side-effect-validation)
- [Functional Review: Terms, Rewards, and Configuration Alignment](functional-review-terms-rewards-and-configuration-alignment)

## Report completion gate

The consolidated review — and any posting of results to a Jira ticket — must wait until every submitted report in the queue has reached a terminal state (completed and downloaded, or failed with a recorded error). A report that is pending, queued, or running is not terminal. Never publish findings, a verdict, or a ticket comment while any queued report is still running; wait for the outstanding reports to complete and incorporate their output first.

## Report reuse window

Reports are expensive and reviews may be re-run while iterating. Before submitting a new report, reuse an existing report of the same type with the same parameters when one was created in the last 2 days, unless the requester explicitly asks for fresh data. Note in the review header when reused reports contributed evidence.

## Example chat prompt

Follow the report execution queue rules before analysis. Include report view links, evidence gaps, findings by section, and an overall verdict.

## Final verdict definitions

| Verdict | Meaning |
|---|---|
| Pass | No material runtime or configuration-alignment flags found |
| Watch | Non-blocking anomaly or low-confidence concern worth monitoring |
| Issue | Evidence of a material problem that may affect users, rewards, tracking, or integrations |
| Needs investigation | Reports are missing, inconclusive, contradictory, or there is not enough traffic to conclude |
