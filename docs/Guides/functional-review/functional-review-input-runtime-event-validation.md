---
title: "Functional Review: Input / Runtime Event Validation"
slug: functional-review-input-runtime-event-validation
excerpt: "Validate inbound input events, event-to-step mapping, and Input Records payloads against the campaign graph."
hidden: true
---

Validate raw inbound events and payloads for one live V10 program.

> 🚧 **Execution rules apply.** Follow the queue, hard stop, expectation manifest, and completion gate in [Report Execution + Runtime Checks](doc:functional-review-report-execution-runtime-checks) before recording any finding.
>
> After submitting each report below, proceed with the next queued report without asking or stopping, even if this report fails or remains pending.

After Input Records completes, continue with [Event Data Rule Alignment](doc:functional-review-event-data-rule-alignment).

---

## 1. Input Events Count

**Answers**

- Are all expected configured input events firing?
- Are unexpected input events arriving that the program does not consume?

### Report

| Field | Value |
|---|---|
| Report type | `t1owor6ia18bia3ur7zg` |
| Display name | Input Events Count |
| Notes | Do **not** submit `INPUT_EVENTS_COUNT` as a `report_type`. It is a display/report-use label only. |

### Required parameters

```text
time_range=LAST_MONTH
container=all
period=NONE
event_names=All
campaign_id=<campaign_id>
dimensions=EVENT_NAME
```

### Expect from graph

Expected raw event names must come from Input Event trigger rule settings — especially `triggerEventNames` / `eventNames`.

Do **not** infer expected raw event names from the business-event component name.

For each business-event / targetable-step component:

1. Open its `triggerRules`.
2. Find the Input Event rule.
3. Extract configured `triggerEventNames` / `eventNames`.
4. Use those values as expected raw inbound event names.
5. Record the mapping:

```text
business_event_component_name -> triggerEventNames/eventNames -> required data fields -> rules/actions
```

### Compare

```text
expected_trigger_events = triggerEventNames/eventNames from the graph
actual_input_events = event_name values returned by Input Events Count
missing_expected_trigger_events = expected_trigger_events - actual_input_events
unexpected_input_events = actual_input_events - expected_trigger_events
```

When similar names exist, do not treat them as equivalent without graph evidence.

Examples:

- `treatment_completed` component name is not automatically the same as `appointment_completed` raw input event
- `product_bonus` component name is not automatically the same as `order_completed` raw input event

### Flag if

- No inbound events for the program in the review window
- Expected event type missing while similar events still arrive
- Event volume dropped to zero compared with prior sanity-check evidence or expected recent behavior
- Configured live step appears in the flow but has no supporting inbound events
- Inbound events arriving that nothing in the program consumes
- Production-like activity in sandbox or test containers

### Severity

| Finding | Severity |
|---|---|
| No events for the program, or missing key expected event types | **Issue** |
| Unexpected inbound events not consumed by the program | **Watch** or **Issue**, depending on volume and whether they can affect rewards, attribution, or UX |
| Production-like traffic in test containers | **Watch** or **Issue**, depending on volume and whether rewards or PII are involved |
| Quiet week or single-day dip in production | **Watch** |

---

## 2. Input Events with Triggered Steps

**Answers**

- Does each expected raw inbound event map to the intended business-event / targetable-step?
- Is event activity continuous or reasonable for the program’s traffic pattern?

### Report

| Field | Value |
|---|---|
| Report type | `INPUT_EVENTS_WITH_TRIGGERED_STEPS` |
| Display name | Input Events with Triggered Steps |

### Required parameters

```text
time_range=LAST_MONTH
container=all
period=DAY
event_names=All
campaign_id=<campaign_id>
dimensions=EVENT_NAME
```

### Expect from graph

Use each expected `triggerEventName` from the graph-derived expectation manifest. Do **not** use this report to redefine expected event names.

### Compare

For each expected `triggerEventName`:

1. Confirm the raw inbound event appears.
2. Confirm it maps to the intended configured business-event / targetable-step.
3. Confirm event activity is continuous or reasonable for the program’s expected traffic pattern.
4. Flag raw inbound events that do not map to any configured step in this program.
5. Flag configured `triggerEventNames` with no triggered-step evidence.

### Flag if

- Inbound volume with no matching triggered steps for this program
- Configured live step appears in the flow but has no supporting triggered-step records
- Expected event activity appears only on isolated days when it should be continuous
- Unexpected event spikes, drop-offs, or event names
- Production-like activity in sandbox or test containers

### Severity

| Finding | Severity |
|---|---|
| Inbound events with no matching triggered steps for key configured flows | **Issue** |
| Configured live steps with no supporting triggered-step records | **Issue** or **Needs investigation**, depending on whether the event is expected in the review window |
| Unexpected spikes or drop-offs without explanation | **Watch** |
| Production-like traffic in test containers | **Watch** or **Issue**, depending on volume and whether rewards or PII are involved |

---

## 3. Input Records

**Answers**

- Are the data fields required by the flow present on raw client payloads?
- Are those fields compatible with flow-builder rules (type, format, non-empty where required)?

### Report

| Field | Value |
|---|---|
| Report type | `CONFIGURABLE_INPUT_RECORDS` |
| Display name | Input Records |

### Required parameters

```text
time_range=LAST_MONTH
container=all
event_names=<graph-derived triggerEventNames / eventNames as a string>
```

> ❗️ For `event_names`, use only graph-derived raw input trigger names from `triggerEventNames` / `eventNames`. Do **not** use journey names, business-event component names, content component names, action names, or display names unless the trigger rule explicitly configures the same value as a raw input event name.

### Required mapping

Use this exact mapping:

```text
Id=event.id;Client Id=event.clientId;Event Time=event.eventTime;Person Id=person(event.personId).id;Container=event.container;Name=event.name;Api Type=event.apiType;data=event.data;
```

> ❗️ **`data=event.data;` is mandatory.**
>
> Do **not** replace `data=event.data` with hand-picked `event.data.<field>` mappings derived from configured data components. Field-specific mappings can hide unexpected fields, missing fields, null values, malformed values, and event-type-specific payload differences.
>
> If additional convenience columns are needed, add them only **in addition to** `data=event.data`, not instead of it.

### Expect from graph

Input Records validates the raw event payload sent by the client. Confirm that data fields required by the flow are present and compatible with flow-builder rules.

### Flag if

Required data fields missing on samples for events that should carry them, or present but malformed/incompatible.

Validate field presence and format for fields used by configured data components and rules:

- timestamp fields parse as timestamps (for example `appointment_start`, `appointment_end`)
- date fields parse as expected dates (for example `client_dob`)
- numeric fields parse as numbers (for example `value`, `current_total`)
- identifier fields are non-empty strings (for example `appointment_id`, `order_id`, `membership_id`, `client_id`, `location_id`)
- rule-dependent fields are present and usable (for example `product_name` for product-name exclusion rules)
- idempotency or unique partner keys are present where the flow expects deduplication or uniqueness

Distinguish in findings:

- missing field
- null value
- blank string
- malformed value
- wrong type
- unexpected format

### Required sample summary

Findings are sample-based; say so in the summary.

For each sampled event type, report:

- sample count checked
- expected fields
- observed fields
- missing fields
- malformed fields
- confidence level

> ❗️ Do not expose raw customer payloads or PII in the final response. Summarize field-level validation instead.

### Next step

After Input Records is downloaded, run [Event Data Rule Alignment](doc:functional-review-event-data-rule-alignment) to compare sampled `event.data` against trigger/quality/reward rule conditions.
