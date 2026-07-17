---
title: "Functional Review: Conversion & Reward Validation"
slug: functional-review-conversion-reward-validation
excerpt: "Validate Conversion Audit outcomes and earned rewards against graph-derived earning steps."
hidden: true
---

Validate processed conversion/outcome evidence and earned rewards for one live program. V10 flow-builder is the primary target; V8/legacy campaigns run these reports best-effort with reward-capable steps derived from V8 controller configuration (see [Overview](doc:functional-review-overview)).

> 🚧 **Execution rules apply.** Follow the queue, hard stop, expectation manifest, and completion gate in [Report Execution + Runtime Checks](doc:functional-review-report-execution-runtime-checks) before recording any finding.
>
> After submitting each report below, proceed with the next queued report without asking or stopping, even if this report fails or remains pending.

---

## 4. Conversion Audit

**Answers**

- Are processed campaign outcomes healthy for the configured earning path?
- Do low-quality, self-share, or attribution patterns explain funnel drop-offs?

### Report

| Field | Value |
|---|---|
| Lookup by display name | `Conversion Audit` |
| Underlying type | typically `CONFIGURABLE_EVENTS` |
| Notes | Do **not** hand-build a new `CONFIGURABLE_EVENTS` report or override the template `mappings` unless the configured report template is unavailable. The configured **Conversion Audit** template already contains the required diagnostic mappings. |

### Required parameters

```text
campaign_id=<campaign>
program_label=<program_label>
time_range=LAST_MONTH
container=all
step_names=<step_names>
```

### Expect from graph — `step_names`

`step_names` must be a comma-separated string of business-event step names that can result in a reward.

Include **every** earning/root business-event step whose configured path can issue or contribute to a reward. Sort the names **alphabetically** before joining them with commas. Deterministic derivation matters: the report reuse cache keys on the exact parameter string, so an inconsistent set or ordering forces a full re-run of this multi-hour report on every review.

“Uncertain” means an earning/root step whose reward impact is unclear from the graph — **not** “include every inbound or funnel step.” Default **exclude** pure click, share, landing, and destination steps unless that step’s path directly grants, qualifies, or earns a reward.

Do **not** include:

- raw inbound input event names unless they are also the configured business-event step name
- reward event names
- email event names
- webhook event names
- frontend zone or page events
- system events
- pure click / share / landing / destination steps (for example `share_click`, `share_event`, `share_destination`, friend landing) unless the graph shows that step directly grants or qualifies a reward
- steps that only incentivize analytics or funnel signals with no reward / earn / qualify path

Derive `step_names` from the campaign graph, **not** from Input Events Count, Conversion Audit output, or high-volume event names. On a V8/legacy campaign, derive them the same way from the built controller/step configuration — reward-capable earning/root steps only.

Examples:

```text
# Good — reward-capable earning/root steps only (alphabetical)
step_names="offline_purchase,reward_evaluation_completed,signed_up"

# Bad — dilutes Conversion Audit with non-reward funnel steps
step_names="offline_purchase,share_click,share_event,signed_up"
```

> ❗️ Do **not** use reward event names. Use the earning/root business step names from the campaign graph.
>
> `step_names=#{{step_names}}` should be passed as a string.

> ❗️ **Fail-closed — over-broad `step_names` is invalid execution.**
>
> If Conversion Audit was submitted with non-reward funnel steps (for example `share_click` / `share_event`) mixed into `step_names`, treat that run as **Invalid execution** for reward-path conclusions. Discard Pending/Approved mix from that run for reward health, resubmit with reward-capable steps only (alphabetical), and use the corrected report before judging outcomes.

### Submission guidance

1. Inspect the campaign graph.
2. Derive `step_names` from configured business-event / targetable-step names that can result in a reward: include every reward-capable earning/root step (include uncertain earning steps only), exclude pure click/share/landing unless they directly grant or qualify a reward, then sort alphabetically.
3. Find the configured report type whose display name is `Conversion Audit`.
4. Submit that configured report type using the required parameters above.
5. Do not override `mappings`; rely on the configured report template mappings.

### Flag if

- High share of low-quality conversions:
  - above ~25% → **Watch**
  - above ~40% → **Issue**, unless explained
- Self-share or advocate clicked own link patterns
- Attribution reasons that explain funnel drop-offs:
  - referred path never completed
  - unexpected direct-only mix

Pair with **Promotion sources** when attribution mix may explain the audit.

### Important distinction

Conversion Audit validates processed campaign events and conversion/outcome evidence. Its Event Name values are **not** necessarily raw client-sent input event names.

Use:

- Input Events Count / Input Records for raw inbound client event names
- Conversion Audit for processed campaign event or outcome evidence

Do not say the client sent a Conversion Audit Event Name unless that same event name is also present in Input Events Count or Input Records.

---

## 5. Earned Rewards

**Answers**

- Do outcomes in the window have matching earned or issued rewards?
- Are rewards stuck in failed / trying-to-fulfill, or unfulfilled longer than expected?

### Report

| Field | Value |
|---|---|
| Report type | `CONFIGURABLE_REWARDS` |
| Display name | Rewards |

### Required parameters

```text
campaign_id=<campaign>
time_range=LAST_MONTH
container=all
```

### Flag if

- Outcomes in the window without matching earned or issued rewards → **Issue**
- Material share of rewards stuck in failed or trying-to-fulfill → **Issue**
- Earned rewards unfulfilled longer than typical for the supplier type:
  - digital gift card: more than ~24 hours → **Watch**

One failed reward on a test person is not a program-level issue; look at rates and volume.
