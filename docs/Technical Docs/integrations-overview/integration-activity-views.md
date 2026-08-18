---
title: "Add the Activity and Event Views"
excerpt: "Give every integration a report-runner view and an event-stream view, create the report runner and event stream behind them, and attach each element to the view that reads it.\n"
---

This page is one part of the Management API integration guide. Start at [Create an Integration with the Management API](doc:management-api-integration) for the build paths and the creation contract.

# Overview

Every partner integration exposes three surfaces, whatever the partner does. The configuration view built in [Create the Integration Campaign and Component Model](doc:integration-component-model) collects the settings that finish setup. This page builds the other two: a **report-runner view** charting what the integration has processed, and an **event-stream view** carrying a live feed of the events it produces.

They apply to every category. An inbound commerce platform charts orders and streams the events it maps; an outbound partner charts what Extole forwarded and streams the outbound activity; a reward fulfillment partner charts reward revenue and streams reward events. The partner decides what the report counts and what the stream filters to, never whether the tabs exist.

These two are the last pieces built and the easiest to drop, because each depends on the campaign being republished after its view exists. Neither absence shows up as a failed call. What a marketer sees instead is an integration whose activity tab reports that no report runner is configured, and no event feed at all — the two surfaces someone opens first when asking whether the integration is working.

## Prerequisites

- A server-side access token authorized to manage campaigns, components, report runners, and event streams.
- An integration campaign with its model component and a `views` socket, built through [Create the Integration Campaign and Component Model](doc:integration-component-model).
- The production API host in `EXTOLE_API_HOST`.
- The partner page for this integration, when one exists. It names what the report counts and which events the feed carries; where it publishes a report runner contract, that contract is literal.

## Required Parameters

| Parameter | Purpose |
| :-------- | :------ |
| `MANAGEMENT_API_ACCESS_TOKEN` | Bearer token on every call. |
| `EXTOLE_API_HOST` | Production host for campaign, component, report-runner, and event-stream calls. |
| `CAMPAIGN_ID` and `CAMPAIGN_VERSION` | The integration campaign and its current version, refreshed before every version-scoped mutation. |
| `INTEGRATION_COMPONENT_ID` | The model component that owns the `views` socket. |
| `REPORT_VIEW_COMPONENT_ID` | The report-runner view, used as the report runner's `component_ids`. |
| `EVENT_STREAM_VIEW_COMPONENT_ID` | The event-stream view, used as the event stream's `component_ids`. |
| `REPORT_TYPE_ID` | The account-scoped report type the runner executes. |
| `PARENT_REPORT_TYPE_ID` | The parent report type, needed only when the account has no suitable type and you configure one. |
| `SCHEDULE_START_DATE` | An ISO-8601 timestamp in the future, when the scheduled runner starts. |
| `EVENT_STREAM_ID` | Returned by the event-stream create, used when adding the stream's filters. |

## Create the Two View Components

Both views install into the `views` socket on the model component, and both are ordinary view components: the platform's view type requires `title`, `status`, and `settingsToDisplay` by name, with `settingsToDisplay` typed `STRING_LIST` rather than `JSON`. A view created without all three, or with `settingsToDisplay` typed as JSON, is rejected for type validation against three subschemas none of which the error names. Attach each with `installed_into_socket` — `socket_name` is not a property of a component create.

Name the components `report-runner-view` and `event-streams`. Those names are literal, and only the partner token in the surrounding tree varies. The tab labels a marketer reads come from each view's `title`, so a descriptive substitute such as `activity-chart` changes nothing anyone sees and everything about whether a client-local build can be compared against the packaged one when someone reports that a tab looks wrong.

Create the report-runner view:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "report-runner-view",
    "display_name": "Example Activity",
    "description": "Daily activity processed by the Example integration.",
    "types": ["report-runner-view-v10.0"],
    "installed_into_socket": "views",
    "component_ids": ["'"$INTEGRATION_COMPONENT_ID"'"],
    "variables": [
      { "name": "order", "type": "INTEGER", "values": { "default": 2 } },
      { "name": "title", "type": "STRING", "values": { "default": "Example Activity" } },
      { "name": "status", "type": "STRING", "values": { "default": "READY" } },
      { "name": "settingsToDisplay", "type": "STRING_LIST", "values": { "default": [] } },
      {
        "name": "reportRunnerId",
        "display_name": "Report Runner ID",
        "type": "STRING",
        "values": {
          "default": "javascript@buildtime:(function(){ let elements = Java.from(context.getComponent().createElementsQuery().withType(\"REPORT_RUNNER\").list()); return elements && elements.length > 0 ? elements[0].getId() : null; })()"
        },
        "tags": ["importance:expert"]
      }
    ]
  }'
```

Create the event-stream view the same way, with `withType("EVENT_STREAM")` in place of `withType("REPORT_RUNNER")`:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "event-streams",
    "display_name": "Example Events",
    "description": "Live feed of events produced by the Example integration.",
    "types": ["event-stream-view-v10.0"],
    "installed_into_socket": "views",
    "component_ids": ["'"$INTEGRATION_COMPONENT_ID"'"],
    "variables": [
      { "name": "order", "type": "INTEGER", "values": { "default": 3 } },
      { "name": "title", "type": "STRING", "values": { "default": "Example Events" } },
      { "name": "status", "type": "STRING", "values": { "default": "READY" } },
      { "name": "settingsToDisplay", "type": "STRING_LIST", "values": { "default": [] } },
      {
        "name": "eventStreamId",
        "display_name": "Event Stream ID",
        "type": "STRING",
        "values": {
          "default": "javascript@buildtime:(function(){ let elements = Java.from(context.getComponent().createElementsQuery().withType(\"EVENT_STREAM\").list()); return elements && elements.length > 0 ? elements[0].getId() : null; })()"
        },
        "tags": ["importance:expert"]
      }
    ]
  }'
```

A view points at its element through a setting typed `STRING` — `reportRunnerId` on the report view, `eventStreamId` on the event-stream view. There is no `REPORT_RUNNER_ID` or `EVENT_STREAM_ID` setting type, and naming one is rejected as malformed JSON with the invented type echoed back as the invalid value. The setting holds no literal identifier either: its default is a buildtime query asking the view's own component for the element it owns, so the view keeps working when the element is recreated.

Wrap every Java collection in `Java.from` before iterating it, as both expressions do. An expression that walks one directly builds into nothing, and because settings are evaluated as part of the create, the whole component is refused with `campaign_build_failed` naming the variable rather than the mistake.

Order is a setting, not the order you happened to create them in. Give every view an `order` typed `INTEGER`, lowest first, with configuration at the front. Views without it arrange themselves arbitrarily, so a marketer can meet the activity chart before the tab that asks for credentials.

### Map the Report's Columns to a Chart

Give the report-runner view a `reportColumnsMapping` setting as well, typed `JSON`. Its default is the mapping serialized as a string and escaped; a nested object is refused as `variable_value_invalid_type`, which reports the value as invalid for the type it plainly is. It maps the report's columns onto a chart, and every column it names has to be one the runner's `mappings` expression produces — the axis column and each series column by exactly the name the expression assigns:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components/$REPORT_VIEW_COMPONENT_ID/settings" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "reportColumnsMapping",
    "display_name": "Report columns mapping",
    "type": "JSON",
    "values": {
      "default": "{\"chart\":{\"type\":\"line\"},\"xAxis\":{\"column\":\"date\",\"type\":\"datetime\"},\"series\":[{\"name\":\"Count\",\"column\":\"count\",\"aggregation\":\"sum\"}]}"
    },
    "tags": ["importance:expert"]
  }'
```

Without the setting the tab has a report behind it and nothing to draw; with a column the report does not produce, it draws an empty axis. Write the mappings expression and this setting together.

## Republish Before Attaching Elements

What a bundled component declares inline under `elements`, the API creates as its own resource attached by `component_ids`:

| Element a bundle declares | API resource |
| :------------------------ | :----------- |
| `report_runners` | `POST /v7/report-runners` |
| `event_streams` | `POST /v6/event-streams`, with filters added afterward |

Attach each to the **view** component that displays it, not to the integration component. The report runner uses `$REPORT_VIEW_COMPONENT_ID`; the event stream uses `$EVENT_STREAM_VIEW_COMPONENT_ID`. Both views resolve what to show by querying their own component for an element of the matching kind, so a report runner hung off the integration — or off the event-stream view — leaves the tab reporting that no report runner is configured even though one exists in the account.

Republish the campaign after creating the views and before creating their elements. The `component_ids` reference resolves against the published campaign, so a resource created against a view component added since the last publish is rejected with `invalid_component_reference` — the same rule that governs webhooks and reward suppliers, and the easiest one to trip over here because the view was created minutes earlier in the same session.

That is the first of two publishes. The second, after both elements exist, is covered in [Republish Again So the Views Resolve Their Elements](#republish-again-so-the-views-resolve-their-elements) below, and skipping it leaves both tabs empty.

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/publish" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{}'
```

Read `$CAMPAIGN_VERSION` from the campaign immediately before publishing rather than counting your own writes: every component and settings call increments it. That operation is **not carried in the OpenAPI specification**, so a reference lookup returns nothing found — a gap in the specification rather than evidence that publishing is unavailable. This page and [Validate and Publish an Integration](doc:integration-validation) are its documentation.

## Build the Report Behind the Activity Tab

A report runner is a scheduled report, a set of parameter values for it, and an attachment to the view that charts it:

```bash
curl --request POST "$EXTOLE_API_HOST/v7/report-runners" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "type": "SCHEDULED",
    "name": "Partner Example Activity Report",
    "report_type": "'"$REPORT_TYPE_ID"'",
    "formats": ["CSV", "JSON"],
    "scopes": ["CLIENT_SUPERUSER"],
    "tags": ["partner-graph"],
    "frequency": "WEEKLY",
    "schedule_start_date": "'"$SCHEDULE_START_DATE"'",
    "enabled": true,
    "execution_policy": "AWAIT_DATA",
    "parameters": {
      "container": "production",
      "time_range": "ALL_TIME",
      "campaign_states": "ALL",
      "visit_type": "NEW_TO_CLIENT",
      "unattributed_events": "false",
      "quality": "ALL",
      "mappings": "date=START_DATE(event.eventTime, period:\"DAY\"); count=group_count(event.id, step_name:\"converted\")"
    },
    "component_ids": ["'"$REPORT_VIEW_COMPONENT_ID"'"]
  }'
```

The `mappings` expression is where the partner shows up. Count and group the events this integration actually produces — the canonical business events an inbound build maps to, the reward events a fulfillment partner generates, the outbound activity a library install forwards — and give each series a column the chart mapping can name. Where the partner page publishes a runner contract, copy it literally: its name, schedule, formats, tags, scopes, execution policy, and every parameter and mapping expression. A runner with a plausible count or revenue mapping is not equivalent to the partner's report.

A scheduled runner needs `schedule_start_date`, as an ISO-8601 timestamp with an offset chosen when you create the runner. Pick a date in the future — a start date already in the past is the reason a runner that reports itself as enabled never produces a report.

A runner's type is fixed once created: a runner made as `REFRESHING` cannot be turned into a scheduled one, and an update that tries reports the wrong type rather than the wrong field. Delete it and create the runner you meant.

### Choose or Create the Report Type

`report_type` is an account-scoped identifier rather than a readable constant, so read the account's types and match on display name. Ask for the ones you want rather than the whole catalog: a mature account holds a couple of hundred types and the unfiltered listing runs to roughly a megabyte, which no tool-mediated read will return.

```bash
curl --request GET "$EXTOLE_API_HOST/v6/report-types?display_name=Customer%20Activity" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN"
```

The listing accepts `display_name`, `search_query`, `report_type_id`, `tags`, `limit`, and `offset`. **The identifier you pass as `report_type` is the type's `name`** — an opaque string such as `r84a5841xf0hehbzsf6j`. There is no `id` field on a report type, so a projection that asks for one comes back as a list of nulls, which reads like an account with no usable types rather than the wrong field name. Read a single candidate in full with `GET /v6/report-types/{id}`, whose path segment takes that same `name` value, before choosing between types that share a display name.

An empty result is worth one more read before you act on it: a truncated or over-large response is not an absent type, and reporting the account as lacking a report type is how a build ends with an activity tab that says no report runner is configured while three usable types sit in the account. Two properties decide whether a type will work, and neither is its display name:

- The **parameters it declares** are the only ones the runner may send, and their values come from the type's own enumerations. A time range is `ALL_TIME`, not `all_time`; a locale list accepts only locales the account declares; a required parameter left out and an invented parameter both come back as the same invalid-format rejection on `parameters` as a whole, so add parameters one at a time when one is refused rather than rewriting the set.
- The **mappings dialect** it accepts decides what your expression may say. A type whose `mappings` parameter is row-shaped rejects the grouping functions — `group_count`, `GROUP_SUM` — that a charted activity report is built from; a metric-shaped one accepts them. Read the parameter's type before writing the expression, and choose the parent by that rather than by a display name that sounds close.

Accounts differ here, and an account that lacks a suitable type is a normal case rather than a dead end. Create one: a configured report type is a saved set of parameter defaults over a parent type.

```bash
curl --request POST "$EXTOLE_API_HOST/v6/report-types" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "display_name": "Example Activity",
    "description": "Activity processed by the Example integration.",
    "type": "CONFIGURED",
    "parent_report_type_id": "'"$PARENT_REPORT_TYPE_ID"'",
    "categories": ["Customer Activity"],
    "scopes": ["CLIENT_SUPERUSER"],
    "allowed_scopes": ["CLIENT_ADMIN", "CLIENT_SUPERUSER"],
    "visibility": "PUBLIC",
    "formats": ["CSV", "JSON"],
    "parameters": [
      { "name": "mappings", "default_value": "date=START_DATE(event.eventTime, period:\"DAY\"); count=group_count(event.id, step_name:\"converted\")" },
      { "name": "container", "default_value": "production" },
      { "name": "time_range", "default_value": "" },
      { "name": "campaign_states", "default_value": "" },
      { "name": "visit_type", "default_value": "" },
      { "name": "unattributed_events", "default_value": "" },
      { "name": "quality", "default_value": "" }
    ]
  }'
```

The `parameters` list must name **every** parameter the parent declares, giving an empty default to the ones you do not set. Listing only the ones you care about reads as deleting the rest and is rejected as an attempt to remove static parameters, which is the one error here that sounds unrelated to what you sent. Read the parent with `GET /v6/report-types` and copy its parameter names rather than working from the list above, which shows the shape and not one particular parent's set.

The list also has to cover everything the runner sends, because it works in both directions: a configured type declares what its runners may pass, so a runner sending `time_range` against a type that omits it is rejected the same way an invented parameter is. The runner created above sends seven parameters, which is why all seven appear here.

## Build the Event Stream Behind the Events Tab

An event stream's filters are created under the stream and carry a `type` discriminator in the body rather than a path segment, which is the opposite of how reward webhook filters work. Create the stream first, after the campaign republish above, then add each filter:

```bash
curl --request POST "$EXTOLE_API_HOST/v6/event-streams" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "javascript@buildtime:context.getComponent().getName() + '\'' Events'\''",
    "description": "A live feed of events produced by the Example integration. The feed runs for 1 hour by default. Refresh the feed to poll for new events.",
    "tags": ["internal:app_type=example"],
    "component_ids": ["'"$EVENT_STREAM_VIEW_COMPONENT_ID"'"]
  }'

curl --request POST "$EXTOLE_API_HOST/v6/event-streams/$EVENT_STREAM_ID/filters" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"type": "APPLICATION_TYPE", "app_types": ["example"]}'
```

Filter to this integration's own activity. The application-type filter narrows the feed to the partner's app type and belongs on every stream; add an `EVENT_TYPE` filter when the integration produces one recognizable class of event, as a reward fulfillment partner does with `{"type": "EVENT_TYPE", "event_types": ["REWARD", "SEND_REWARD"]}`. Without filters the tab shows every event in the account rather than the integration's, which looks like a working feed and is not one.

Name the stream for the view that owns it and tag it with the partner's app type, which is how the feed is recognized as this integration's rather than a stream someone left in the account.

## Republish Again So the Views Resolve Their Elements

Neither view stores the identifier you just created. Each carries a `javascript@buildtime` query that looks up the element attached to its own component:

```text
javascript@buildtime:(function(){ let elements = Java.from(context.getComponent().createElementsQuery().withType('REPORT_RUNNER').list()); return elements && elements.length > 0 ? elements[0].getId() : null; })();
```

The event-stream view carries the same query with `withType('EVENT_STREAM')`. Both evaluate when the campaign is built, and both return null when nothing of that type is attached yet — which is exactly the state at the publish above, because that publish is what made the views referenceable in the first place.

So the sequence is publish, create the elements, publish again:

```bash
CAMPAIGN_VERSION=$(
  curl --silent --show-error --fail-with-body \
    "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID" \
    --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" |
  jq --raw-output '.version'
)

curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/publish" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{}'
```

Refresh `$CAMPAIGN_VERSION` first. Creating the elements does not change the campaign, but anything else in the same session does, and the version that succeeded at the first publish is not the version to send at the second.

No call fails if you skip this. Both elements exist, both are attached, and every create returned success. What the omission costs shows up in two later places: the built `reportRunnerId` and `eventStreamId` are null, so [Confirm the Tabs Resolve](#confirm-the-tabs-resolve) fails, and a marketer opening the integration meets an activity tab reporting that no report runner is configured and no event feed at all. That gap between a clean set of responses and an empty pair of tabs is why the confirmation reads the built values instead of trusting the create calls.

## Error Handling

| Response | Cause | What to do |
| :------- | :---- | :--------- |
| `invalid_component_reference` | The report runner or event stream was created against a view added since the last publish. | Publish the campaign, then create the element with `component_ids`. |
| `campaign_build_failed` naming a variable | A buildtime expression iterated a Java collection without `Java.from`. | Wrap the collection and recreate the component. |
| `variable_value_invalid_type` on `reportColumnsMapping` | The default was sent as a nested object. | Send the mapping as an escaped JSON string. |
| Malformed JSON echoing an invented type | The element setting was typed `REPORT_RUNNER_ID` or `EVENT_STREAM_ID`. | Type both settings `STRING`. |
| Type validation against three subschemas | The view is missing `title`, `status`, or `settingsToDisplay`, or `settingsToDisplay` is typed `JSON`. | Send all three, with `settingsToDisplay` typed `STRING_LIST`. |
| Invalid format on `parameters` as a whole | The runner sent a parameter the report type does not declare, omitted a required one, or used a value outside the type's enumeration. | Read the type's declared parameters and add them one at a time. |
| An attempt to remove static parameters | A configured report type was created naming only some of the parent's parameters. | List every parameter the parent declares, with an empty default for the ones you do not set. |
| The runner reports itself enabled and produces nothing | `schedule_start_date` is in the past. | Recreate the runner with a future start date. |
| `reportRunnerId` or `eventStreamId` is null on a view whose element exists and is attached | The campaign was not published again after the element was created, so the view's buildtime query last evaluated against a component with nothing attached. | Refresh the version and publish again, then read the built value. |

## Confirm the Tabs Resolve

Read the built campaign and confirm `reportRunnerId` and `eventStreamId` are non-null. An empty tab is the symptom of an element that was never created, was attached to the wrong component, or exists and is attached but has not been through a publish since. None of the three shows up as a failed call. A view whose `reportColumnsMapping` is set but whose `reportRunnerId` is null is the common half-built case — the chart is described and has nothing to chart.

Read the **built** form specifically. The component's own definition holds the buildtime query rather than an identifier, so a view that looks unresolved in the campaign version is the normal state and says nothing about whether the tab works.

Confirm as well that the event stream carries its filters, and that every column the chart mapping names is one the runner's `mappings` expression produces. A stream with no filters and a chart with no matching columns both render as surfaces that exist and say nothing.
