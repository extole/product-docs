---
title: "Functional Review: Email / Webhook / Side-Effect Validation"
slug: functional-review-email-webhook-side-effect-validation
excerpt: "Validate promotion sources, webhook dispatch, and email deliverability for one live program."
hidden: true
---

Validate promotion attribution and outbound side effects for one live program. V10 flow-builder is the primary target; V8/legacy campaigns run these reports best-effort (see [Overview](doc:functional-review-overview)).

> 🚧 **Execution rules apply.** Follow the queue, hard stop, expectation manifest, completion gate, and output format in [Report Execution + Runtime Checks](doc:functional-review-report-execution-runtime-checks) before recording any finding.
>
> After submitting each report below, proceed with the next queued report without asking or stopping, even if this report fails or remains pending.

---

## 6. Promotion Sources

**Answers**

- Is Direct share unusually high when referral-driven traffic is expected?
- For click-sensitive programs, is traffic mostly view-only when click signal is required?

### Report

| Field | Value |
|---|---|
| Report type | `TOP_PROMOTION_SOURCES_V2` |

### Required parameters

```text
campaign_id=<campaign>
time_range=LAST_MONTH
container=all
```

### Flag if

- Unusually high Direct share when referral-driven traffic is expected:
  - rough guide: Direct above ~70% of attributed promotion events with referral steps configured
- Financial- or loan-style programs where attribution likely needs **click** signal (`promotion_clicked`, share click):
  - Flag when traffic is mostly **view** only

---

## 7. Webhook and Outbound Events

**Answers**

- Are configured webhooks dispatching?
- Are failure rates material?

> 📘 Webhook reports are only applicable when the client has configured webhooks.
>
> Always check webhook configuration before selecting Webhook Events, Webhook Event Metrics, Webhook Dispatch Results, or Webhook Dispatch Result Metrics.

### Reports

| Report type | When |
|---|---|
| `WEBHOOK_EVENTS` | Webhooks configured |
| `WEBHOOK_DISPATCH_RESULT_EVENTS` | Webhooks configured |

### Required parameters

```text
time_range=LAST_MONTH
```

### Flag if

- Webhook firing but failing:
  - failure rate above ~5% over more than ~50 attempts → **Issue**
- Webhook configured on the program but zero dispatches in the window → **Watch**
- Failures dominated by 4xx or 5xx → **Issue**

---

## 8. Email Deliverability

**Answers**

- Are expected program emails sending when related steps fire?
- Are bounce/failure/suppression rates program-level problems?

### Report

| Field | Value |
|---|---|
| Report type | `EMAIL_DELIVERABILITY` |

### Required parameters

```text
campaign_id=<campaign>
time_range=LAST_MONTH
container=all
```

### Flag if

- Expected program emails not sending while related steps fired → **Issue**
- Bounce or failure rate materially above baseline:
  - above ~5% → **Watch**
  - above ~10% → **Issue** when volume is non-trivial
- High suppressions explained by list hygiene → note only
- Suppressions plus send failures elsewhere → **Watch**

Distinguish one-off test bounces from program-level deliverability problems.

---

## Output

Use the output format, completion gate, and verdict definitions in [Report Execution + Runtime Checks](doc:functional-review-report-execution-runtime-checks). Do not produce a final Functional Review verdict from this doc alone.

> 🚧 **Pending is not terminal.** Every submitted report must reach a terminal state (completed or failed) before final output or ticket posting. Do not treat pending, queued, or running reports as evidence gaps — wait for completion and resume.
