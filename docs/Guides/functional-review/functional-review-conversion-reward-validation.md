---
title: "Functional Review: Conversion & Reward Validation"
slug: functional-review-conversion-reward-validation
excerpt: "# 4. Conversion audit"
hidden: true
intercom_source_id: 15483834
---

# 4. Conversion audit

### Report type
​
Look up the configured report type with display name:
​
`Conversion Audit`
​
Do **not** hand-build a new `CONFIGURABLE_EVENTS` report or override the template `mappings` unless the configured report template is unavailable.
​
The configured **Conversion Audit** template already contains the required diagnostic mappings, including:

### Required parameters
​
- `campaign_id=<campaign>`
- `program_label=<program_label>`
- `time_range=LAST_MONTH`
- `container=all`
- `step_names=<step_names>`

`step_names` must be a comma-separated string of business-event step names that can result in a reward.

Only include earning/root business-event step names whose configured path can issue or contribute to a reward.

Do not include:
​
- raw inbound input event names unless they are also the configured business-event step name
- reward event names
- email event names
- webhook event names
- frontend zone or page events
- system events

Derive `step_names` from the campaign graph, not from Input Events Count, Conversion Audit output, or high-volume event names.

Examples:

`step_names="transacted,converted,purchased,outcome"`
​
Do **not** use reward event names. Use the earning/root business step names from the campaign graph.
​
`step_names=#{{step_names}}` should be passed as a string.

## Reports

- 

CONFIGURABLE_EVENTS

## Display name

- 

Conversion Audit

### Submission guidance
​
1. Inspect the campaign graph.
2. Derive `step_names` from configured business-event / targetable-step names that can result in a reward.
3. Find the configured report type whose display name is `Conversion Audit`.
4. Submit that configured report type using the required parameters above.
5. Do not override `mappings`; rely on the configured report template mappings.

## Look for

- 

High share of low-quality conversions:

  - 

rough guide: above ~25% → **Watch**
  - 

above ~40% → **Issue**, unless explained

- 

Self-share or advocate clicked own link patterns
- 

Attribution reasons that explain funnel drop-offs:

  - 

referred path never completed
  - 

unexpected direct-only mix

Pair with **Promotion sources** when attribution mix may explain the audit.

Important distinction

Conversion Audit validates processed campaign events and conversion/outcome evidence. Its Event Name values are not necessarily raw client-sent input event names.

Use:

- Input Events Count / Input Records for raw inbound client event names.

- Conversion Audit for processed campaign event or outcome evidence.

Do not say the client sent a Conversion Audit Event Name unless that same event name is also present in Input Events Count or Input Records.
# 5. Earned rewards

## Reports

- 

CONFIGURABLE_REWARDS

## Display names

- 

Rewards

## Required parameters

- 

campaign_id=<campaign>
- 

time_range=LAST_MONTH
- 

container=all

## Look for

- 

Outcomes in the window without matching earned or issued rewards → **Issue**
- 

Material share of rewards stuck in failed or trying-to-fulfill → **Issue**
- 

Earned rewards unfulfilled longer than typical for the supplier type:

  - 

digital gift card: more than ~24 hours → **Watch**

One failed reward on a test person is not a program-level issue; look at rates and volume.
