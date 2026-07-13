---
title: "Functional Review: Overview"
slug: functional-review-overview
excerpt: "Run a functional review on one live V10 referral or rewards program — scope, campaign selection, and review map."
hidden: true
---

Use this guide to run a functional review on **one live V10 referral or rewards program**.

A functional review compares live campaign configuration and runtime evidence against expected program behavior. Use it before launch, after a material program or integration change, or on a scheduled launch-review cadence.

> 📘 **Audience**
>
> These runbooks are written for both human reviewers and AI agents. Keep report IDs, parameters, mappings, severity thresholds, and fail-closed rules exact.

## Scope

- One V10 flow-builder program at a time
- Provide either a program label (for example `refer-a-friend`) or a live campaign id
- Legacy controller-only programs require a different review path

## Campaign selection

A functional review must run against one confirmed V10 flow-builder program.

Before report execution:

1. If the user provides a program label or live campaign id, use that value.
2. If the user does not provide a campaign/program, discover the available campaign/program list before running reports.
3. If only one eligible V10 campaign exists, run the review against that campaign.
4. If multiple eligible V10 campaigns exist and the user cannot clarify, run against the most recently updated or most recently launched/live V10 campaign, and state this selection in the review header.
5. If both V8/legacy and V10 campaigns exist, exclude V8/legacy campaigns unless the user explicitly requested a legacy review path.
6. If no eligible V10 campaign can be confirmed, do **not** run the V10 functional review. Record an evidence gap: `No eligible V10 campaign could be confirmed`.
7. Do not run one functional review across multiple campaigns unless the user explicitly requested a multi-campaign review.

### Review-header note

When the campaign was selected automatically, include this in the review header:

> Campaign selection: No campaign was specified by the user. Available campaigns were reviewed. The functional review was run against the most recent eligible V10 campaign: `<campaign/program>`. Legacy/V8 campaigns were excluded because this review path applies to V10 flow-builder programs only.

## Default review window

Use a 30-day rolling window ending on the day the review starts.

- Record the start and end dates in the review header
- Use the same window for every report
- Default report parameter: `time_range=LAST_MONTH` (rolling 30 days, not a calendar month)

## Container handling

Run checklist reports across **all containers**, including production and sandbox/test.

- Production traffic and outcomes are the primary evidence for launch sign-off
- Flag production-like users or real customer activity in sandbox/test containers (live partner ids, non-test emails, or meaningful step/reward volume outside production)
- Say which container each finding came from when counts differ

## Review principle

Reports are only half of the review. Campaign graph/configuration is the other half.

For each checklist item:

1. Inspect the campaign graph/configuration to determine expected behavior.
2. Run the relevant report or source.
3. Compare observed report output against the expected behavior.
4. Record findings, flags, evidence gaps, and recommended next steps.

> ❗️ **Do not judge reports in isolation.**

## Review map

Follow this order:

1. [Report Execution + Runtime Checks](doc:functional-review-report-execution-runtime-checks) — queue, hard stop, expectation manifest, completion gate, output format
2. [Input / Runtime Event Validation](doc:functional-review-input-runtime-event-validation) — Input Events Count, Triggered Steps, Input Records
3. [Event Data vs Rule Expectations](doc:functional-review-event-data-rule-alignment) — sample `event.data` vs graph rule conditions
4. [Conversion & Reward Validation](doc:functional-review-conversion-reward-validation) — Conversion Audit, Earned Rewards
5. [Email / Webhook / Side-Effect Validation](doc:functional-review-email-webhook-side-effect-validation) — Promotion sources, Webhooks, Email Deliverability
6. [Terms, Rewards, and Configuration Alignment](doc:functional-review-terms-rewards-and-configuration-alignment) — Terms copy vs configured rewards (can run while reports generate)

## Example chat prompt

Follow the report execution queue rules before analysis. Include report view links, evidence gaps, findings by section, and an overall verdict.

## Final verdict definitions

| Verdict | Meaning |
|---|---|
| Pass | No material runtime or configuration-alignment flags found |
| Watch | Non-blocking anomaly or low-confidence concern worth monitoring |
| Issue | Evidence of a material problem that may affect users, rewards, tracking, or integrations |
| Needs investigation | Reports are missing, inconclusive, contradictory, or there is not enough traffic to conclude |
