---
title: "Functional Review: Input / Runtime Event Validation"
slug: functional-review-input-runtime-event-validation
excerpt: "# 1. Input Events Count"
hidden: true
intercom_source_id: 15483552
---

# 1. Input Events Count

Run this report to answer both questions:

- 

Are all expected configured input events firing?
- 

Are unexpected input events arriving that the program does not consume?

After submitting this report, proceed with the next sanity-check report without asking or stopping, even if this report fails or remains pending.
## Report type
t1owor6ia18bia3ur7zg

Do **not** submit INPUT_EVENTS_COUNT as a report_type. It is a display/report-use label only.

The report type t1owor6ia18bia3ur7zg is used for both:

- 

Input Events Count
- 

Input Events with Triggered Steps

The difference is the parameter shape.
## Required parameters
time_range=LAST_MONTH
container=all
period=NONE
event_names=All
campaign_id=<campaign_id>
dimensions=EVENT_NAME
## Purpose

Purpose

Compare raw inbound event_name values returned by the report against the graph-derived trigger event list.

Expected raw event names must come from the Input Event trigger rule settings, especially triggerEventNames / eventNames. Do not infer expected raw event names from the business-event component name.

For each business-event / targetable-step component:

1. Open its triggerRules.

2. Find the Input Event rule.

3. Extract configured triggerEventNames / eventNames from the rule settings.

4. Use those values as expected raw inbound event names.

5. Record the mapping:

business_event_component_name -> triggerEventNames/eventNames -> required data fields -> rules/actions

Then calculate:

expected_trigger_events = triggerEventNames/eventNames from the graph

actual_input_events = event_name values returned by Input Events Count

missing_expected_trigger_events = expected_trigger_events - actual_input_events

unexpected_input_events = actual_input_events - expected_trigger_events

When similar names exist, do not treat them as equivalent without graph evidence.

Example:

- treatment_completed component name is not automatically the same as appointment_completed raw input event.

- product_bonus component name is not automatically the same as order_completed raw input event.

## Look for

No inbound events for the program in the review window.

Expected event type missing while similar events still arrive.

Event volume dropped to zero compared with prior sanity-check evidence or expected recent behavior.

Configured live step appears in the flow but has no supporting inbound events.

Inbound events arriving that nothing in the program consumes.

Production-like activity in sandbox or test containers, including real users, live identifiers, or meaningful volume that should be production-only.
## Severity guide

No events for the program, or missing key expected event types → **Issue**.

Unexpected inbound events that are not consumed by the program → **Watch** or **Issue**, depending on volume and whether they can affect rewards, attribution, or user experience.

Production-like traffic in test containers → **Watch** or **Issue**, depending on volume and whether rewards or PII are involved.

Quiet week or single-day dip in production → **Watch**.
## 2. Input Events with Triggered Steps

Run this report when you need event-to-step mapping, triggered-step evidence, or daily event distribution.

After submitting this report, proceed with the next sanity-check report without asking or stopping, even if this report fails or remains pending.
## Report type

t1owor6ia18bia3ur7zg

## Required parameters

time_range=LAST_MONTH
container=all
period=DAY
event_names=All
campaign_id=<campaign_id>
dimensions=EVENT_NAME

## Purpose

Use this report to validate raw-event-to-step mapping.

For each expected triggerEventName from the graph-derived expectation manifest:

1. Confirm the raw inbound event appears.

2. Confirm it maps to the intended configured business-event / targetable-step.

3. Confirm event activity is continuous or reasonable for the program’s expected traffic pattern.

4. Flag raw inbound events that do not map to any configured step in this program.

5. Flag configured triggerEventNames with no triggered-step evidence.

Do not use this report to redefine expected event names. Expected event names still come from the campaign graph trigger rules.

## Look for

Inbound volume with no matching triggered steps for this program.

Configured live step appears in the flow but has no supporting triggered-step records.

Expected event activity appears only on isolated days when it should be continuous.

Unexpected event spikes, drop-offs, or event names.

Production-like activity in sandbox or test containers, including real users, live identifiers, or meaningful volume that should be production-only.
## Severity guide

Inbound events with no matching triggered steps for key configured flows → **Issue**.

Configured live steps with no supporting triggered-step records → **Issue** or **Needs investigation**, depending on whether the event is expected in the review window.

Unexpected spikes or drop-offs without explanation → **Watch**.

Production-like traffic in test containers → **Watch** or **Issue**, depending on volume and whether rewards or PII are involved.
# 3. Input Records

## Mappings

Id=event.id;Client Id=event.clientId;Event Time=event.eventTime;Person Id=person(event.personId).id;Container=event.container;Name=event.name;Api Type=event.apiType;data=event.data;

Use this exact mapping for Input Records:

`data=event.data;`

DO NOT ADD ADDITIONAL MAPPING

Do not replace `data=event.data` with hand-picked `event.data.<field>` mappings derived from configured data components. Field-specific mappings can hide unexpected fields, missing fields, null values, malformed values, and event-type-specific payload differences.

If additional convenience columns are needed, they may be added only in addition to `data=event.data`, not instead of it.

## Reports

- 

CONFIGURABLE_INPUT_RECORDS

## Required parameters

- 

time_range=LAST_MONTH
- 

container=all

Get event_names from the campaign graph and use as a string in the report.

The triggerEventNames is the one you need for this report, not the component name.

Run Input Records using the graph-derived triggerEventNames / eventNames, not business-event component names.

Input Records validates the raw event payload sent by the client. It must be used to confirm that the data fields required by the flow are present and compatible with the flow-builder rules.

For `event_names`, use only graph-derived raw input trigger names from `triggerEventNames` / `eventNames` settings. Do not use journey names, business-event component names, content component names, action names, or display names unless the trigger rule explicitly configures the same value as a raw input event name.

## Look for

Required data fields missing on samples for events that should carry them.

Required data fields present but malformed or incompatible with flow-builder expectations.

Validate field presence and format for fields used by configured data components and rules:

- timestamp fields parse as timestamps, for example appointment_start and appointment_end

- date fields parse as expected dates, for example client_dob

- numeric fields parse as numbers, for example value and current_total

- identifier fields are non-empty strings, for example appointment_id, order_id, membership_id, client_id, location_id

- rule-dependent fields are present and usable, for example product_name for product-name exclusion rules

- idempotency or unique partner keys are present where the flow expects deduplication or uniqueness

Distinguish:

- missing field

- null value

- blank string

- malformed value

- wrong type

- unexpected format

Note

Findings are sample-based; say so in the summary.

For each sampled event type, report:

- sample count checked

- expected fields

- observed fields

- missing fields

- malformed fields

- confidence level

Do not expose raw customer payloads or PII in the final response. Summarize field-level validation instead.
