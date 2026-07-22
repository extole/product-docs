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

`step_names` is a comma-separated string of the business-event steps that own a reward action.

**The test for including a step** — apply it to every business-event / targetable step: include the step **if and only if that step owns an earn-reward, qualify, or incentivize action in the campaign graph**. The step's **name is irrelevant** — a `share_clicked` or landing step that owns a reward action is **in**; a `shared` or `advocate_created` step with no reward action of its own is **out**, even when it sits on the path toward a reward. Include the step that actually owns the reward action, not an upstream or "root" step just because a downstream step rewards.

Sort the names **alphabetically**, then join them with commas. Deterministic derivation matters: the report reuse cache keys on the exact parameter string, so an inconsistent set or ordering forces a full re-run of this multi-hour report on every review.

Do **not** include (none of these own a reward action):

- raw inbound input event names, unless the same name is also a reward-owning business-event step
- reward event names
- email event names
- webhook event names
- frontend zone or page events
- system events
- steps that only feed analytics or funnel signals
- upstream / root steps that lead toward a reward but do not own an earn-reward, qualify, or incentivize action themselves (for example a `shared` or `advocate_created` step whose reward is granted by a later step)

Derive `step_names` from the campaign graph by reading each step's actions and keeping the steps whose actions include earn-reward / qualify / incentivize. Do **not** derive the set from Input Events Count, Conversion Audit output, high-volume event names, or the campaign's full business-event step list. On a V8/legacy campaign, apply the same test to the built controller/step configuration.

Examples:

```text
# Good — every step owns a reward action, including a rewarded share step (alphabetical)
step_names="converted,share_clicked,signed_up"

# Bad — `advocate_created` and `shared` own no reward action; a later step grants the reward, not these
step_names="advocate_created,converted,share_clicked,shared,signed_up"
```

The good/bad split turns on the graph, not the name: `share_clicked` belongs **only** because this campaign configures a reward action on it. In a campaign where `share_clicked` owns no reward action, drop it.

> ❗️ Do **not** use reward event names. Use the reward-owning business-event step names from the campaign graph.
>
> `step_names=#{{step_names}}` should be passed as a string.

> ❗️ **Fail-closed — including a step that owns no reward action is invalid execution.**
>
> If Conversion Audit was submitted with any step that owns no earn-reward / qualify / incentivize action (for example an upstream `shared` or `advocate_created` step, or a plain funnel step), treat that run as **Invalid execution** for reward-path conclusions. Discard the Pending/Approved mix from that run for reward health, resubmit with only reward-owning steps (alphabetical), and use the corrected report before judging outcomes.

### Submission guidance

1. Inspect the campaign graph.
2. For each business-event / targetable step, read its actions. Keep the step **only if** its actions include an earn-reward, qualify, or incentivize action; drop every other step regardless of name. Sort the kept step names alphabetically.
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
