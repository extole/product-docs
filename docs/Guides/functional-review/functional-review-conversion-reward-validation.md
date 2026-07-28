---
title: "Functional Review: Conversion & Reward Validation"
slug: functional-review-conversion-reward-validation
excerpt: "Validate Conversion Audit outcomes and earned rewards against graph-derived earning steps."
hidden: true
---

Validate processed conversion/outcome evidence and earned rewards for one live program. V10 flow-builder is the primary target; V8/legacy campaigns run these reports best-effort with enabled reward-owning steps derived from V8 controller configuration (see [Overview](doc:functional-review-overview)).

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

`step_names` is a comma-separated string of the business-event steps that own an **enabled** reward action. It is **not** the campaign's full business-event / funnel list.

**The test for including a step** — apply it to every business-event / targetable step, one step at a time:

1. Open that step's built `actions` (and, on V8, the equivalent controller actions).
2. Find an action whose type is earn-reward, qualify, or incentivize.
3. Confirm that action is enabled (`enabled: true`).
4. Include the step **only if** steps 2 and 3 both pass. Otherwise exclude it.

The step's **name is irrelevant**. A `share_clicked` or landing step that owns an enabled reward action is **in**. A `shared`, `canceled`, `advocate_created`, or other funnel step with **no** earn-reward / qualify / incentivize action of its own is **out**, even when it sits on the path toward a reward, cancels a prior outcome, or appears in Input Events Count. Include the step that actually owns the enabled reward action, not an upstream, cancel, or "root" step just because a downstream step rewards.

**Before submit — justify each name.** For every value in `step_names`, you must be able to point to the specific enabled earn-reward / qualify / incentivize action on that step. If you cannot, remove the name. Do **not** submit a "complete funnel" list of business-event steps.

**Disabled reward actions** — if the step owns an earn-reward, qualify, or incentivize action but that action is disabled (`enabled: false`), **do not** put the step in `step_names`. Record each such step in the review output (step name, action type, and that the reward is disabled) so a human can see rewards that are configured but off. Do not treat a disabled reward as an earning path for this report.

Sort the included names **alphabetically**, then join them with commas. Deterministic derivation matters: the report reuse cache keys on the exact parameter string, so an inconsistent set or ordering forces a full re-run of this multi-hour report on every review.

Do **not** include in `step_names`:

- the full set of business-event / targetable steps on the campaign (that is the most common invalid pattern)
- cancel / opt-out / revoke style steps such as `canceled` unless that step itself owns an enabled earn-reward / qualify / incentivize action (it almost never does)
- raw inbound input event names, unless the same name is also an enabled reward-owning business-event step
- reward event names
- email event names
- webhook event names
- frontend zone or page events
- system events
- steps that only feed analytics or funnel signals
- upstream / root steps that lead toward a reward but do not own an earn-reward, qualify, or incentivize action themselves (for example a `shared` or `advocate_created` step whose reward is granted by a later step)
- steps whose only earn-reward / qualify / incentivize actions are disabled — list these in the review output instead

Derive `step_names` **only** from the per-step action test above. Do **not** derive the set from Input Events Count, Conversion Audit output, high-volume event names, journey diagrams, or "every business event on the program." On a V8/legacy campaign, apply the same action+enabled test to the built controller/step configuration.

Examples:

```text
# Good — every step owns an enabled reward action, including a rewarded share step (alphabetical)
step_names="converted,share_clicked,signed_up"

# Bad — full funnel dump (HostGator-style). `canceled` and `shared` almost never own a reward action.
# Do not copy every business-event step into Event Names / step_names.
step_names="canceled,converted,share_clicked,shared,signed_up"

# Bad — `advocate_created` and `shared` own no reward action; a later step grants the reward, not these
step_names="advocate_created,converted,share_clicked,shared,signed_up"

# Bad — `signed_up` owns a reward action that is disabled; do not put it in step_names
# (list `signed_up` + disabled reward in the review output instead)
step_names="converted,share_clicked,signed_up"   # invalid when signed_up's reward is disabled
# Correct for that graph:
step_names="converted,share_clicked"
```

The good/bad split turns on the graph, not the name: `share_clicked` belongs **only** when this campaign configures an **enabled** reward action on it. Drop the step when it owns no reward action, or when every reward action on it is disabled. Names like `canceled` or `shared` are **not** shortcuts for inclusion.

> ❗️ Do **not** use reward event names. Use the enabled reward-owning business-event step names from the campaign graph.
>
> `step_names=#{{step_names}}` should be passed as a string.

> ❗️ **Fail-closed — including a step that owns no enabled reward action is invalid execution.**
>
> If Conversion Audit was submitted with any step that owns no enabled earn-reward / qualify / incentivize action (for example `canceled`, an upstream `shared` or `advocate_created` step, a plain funnel step, or a step whose reward action is disabled), treat that run as **Invalid execution** for reward-path conclusions. Discard the Pending/Approved mix from that run for reward health, resubmit with only enabled reward-owning steps (alphabetical), and use the corrected report before judging outcomes.

### Submission guidance

1. Inspect the campaign graph.
2. For each business-event / targetable step, read its `actions`. Keep the step in `step_names` **only if** it has an earn-reward, qualify, or incentivize action with `enabled: true`. If it has such an action with `enabled: false`, omit it from `step_names` and record it in the review output as a disabled reward. Drop every other step — including `canceled`, `shared`, and other funnel names — regardless of how common they are on RAF programs. Sort the kept step names alphabetically.
3. Self-check: for each kept name, note the enabled reward action that justified it. If any name lacks that justification, remove it before submit.
4. Find the configured report type whose display name is `Conversion Audit`.
5. Submit that configured report type using the required parameters above. The UI label may say **Event Names**; still pass only the justified `step_names` set — never the full business-event list.
6. Do not override `mappings`; rely on the configured report template mappings.

### Flag if

- Business-event steps with a disabled earn-reward, qualify, or incentivize action (list each step and note the reward is disabled) → **Watch** (or **Issue** when the live program is expected to pay on that path)
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
