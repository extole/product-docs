---
title: "Custom Data Queries using Extole Reports"
slug: custom-data-queries-using-extole-reports
excerpt: "A complete reference for Extole's report mapping expression language — mappings, filters, sort order, and every available function.\n"
hidden: false
intercom_source_id: 15394374
---

# Overview

Extole's configurable reporting framework lets you define exactly what data a report returns, how it is shaped, and which rows are included — all through a mapping expression language passed as report parameters. This document is a complete reference for that language.

You set these expressions in the Advanced section of a report's configuration screen — see [Advanced Report Configuration](doc:advanced-report-configuration). To pick which report type to run, see [Configurable Report Types and Their Entities](doc:configurable-report-types-and-their-entities); for the fields each entity exposes, see [Entities and Context Available in Extole's Configurable Reporting System](doc:entities-and-context-available-in-extole-s-configurable-reporting-system). If a pre-built report already answers your question, check [Report Types](doc:report-types) first.

# Glossary

| Term | Description |
| --- | --- |
| **Data source** | The primary entity loaded per row (step record, input record, reward event, etc.) |
| **Mappings** | Semicolon-separated column definitions that specify column name and value expression |
| **Filters** | Boolean expressions that exclude rows from the result |
| **Sort order** | Comma-separated `ascending()`/`descending()` expressions |
| **Dimension column** | A column whose raw value is preserved per row (not aggregated) |
| **Grouping column** | A column that performs an aggregation; only valid in metrics report types |
| **Records report** | Lists individual entities; one row per record (Events, Input Records, Person, Rewards) |
| **Metrics report** | Groups and counts records; one row per unique combination of dimension values |

# Mapping Syntax

## Column Definition

```
column_name=expression;
```

Mappings are a semicolon-separated list of `name=expression` pairs. The column name appears as the header in the report output.

```
Id=event.id; Campaign Name=campaign(event.campaignId).campaignName; Conversion Count=group_count_distinct(event.personId, step_name:"converted");
```

## Hidden Columns

Prefix a column name with `hidden(...)` to compute an intermediate value without including it in the output. Hidden columns can be referenced by name in subsequent expressions.

```
hidden(Reward Id)=event.data.reward_id; Face Value=reward(Reward Id).faceValue;
```

## Accessing Event Properties

Direct property access on the primary record:

```
event.id
event.eventTime
event.personId
event.campaignId
event.data.someKey
event.data."nested.key.with.dots"
```

For deeply nested keys that contain dots in their name, wrap the key in double quotes:

```
event.data."share.message"
```

# Filter Syntax

Filters are semicolon-separated boolean expressions. All entries must be satisfied (implicit AND between statements).

```
expression operator value
```

**Operators:** `==`, `!=`, `>=`, `<=`, `>`, `<`, `like`, `not like`

**Values** are quoted strings or column references:

```
event.quality=="HIGH";event.campaignId!="null"
```

Multiple filters:

```
event.stepName=="converted";event.quality=="HIGH";event.visitType!="NORMAL"
```

Null checks:

```
event.data.amount!="null"
```

Within a `collection(...)` filter parameter, filters use `and`/`or`:

```
collection(person(event.personId).steps, filter:stepName=="converted" and quality=="HIGH")
```

# Sort Order

Comma-separated sort expressions applied in order:

```
ascending(event.eventTime)
descending(event.data.amount), ascending(event.personId)
```

# Functions Reference

## Attribute Access

### ATTRIBUTE / Direct Access

Returns a raw property from the event record. The `ATTRIBUTE()` wrapper is optional.

```
event.propertyName
ATTRIBUTE(event.propertyName)
event.data.keyName
ATTRIBUTE(event.data.keyName)
```

### PROPERTY

Extracts a named field from a JSON string value.

**Parameters:**
- `(anonymous)` — expression evaluating to a JSON string

**Returns:** String

```
property(step).campaignId
property(property(main_step).data).reward_id
```

### TO_JSON

Converts a column value to its JSON string representation. Useful for text-based searches on complex objects.

**Parameters:**
- `(anonymous)` — column to serialize

**Returns:** String

**Limitation:** requires a sub-field; `to_json(event)` is not supported.

```
to_json(event.data)
to_json(event.selectedCampaignContext)
```

## Scalar / Formatting Functions

### BOOLEAN_FORMAT

Evaluates a condition and returns one of two values.

**Parameters:**
- `(anonymous, 1st)` — condition expression
- `(anonymous, 2nd)` — value when condition is true
- `(anonymous, 3rd)` — value when condition is false

```
boolean_format(event.firstSiteVisit, "Y", "N")
boolean_format(event.quality == "HIGH", "PASSING", "SUSPICIOUS")
boolean_format(EVENT(event.id).name == "converted", "Y", "N")
boolean_format(event.data.amount > "10", "above_ten", "not_above_ten")
```

### NUMBER_FORMAT

Formats a numeric value to decimal with scale 2.

**Parameters:**
- `(anonymous)` — column with numeric value

```
number_format(event.data.amount)
```

### DATE_FORMAT

Formats a timestamp value.

**Parameters:**
- `(anonymous)` — column with timestamp
- `format` *(optional)* — date/time pattern string; defaults to `ISO_OFFSET_DATE_TIME`; special value `epoch` returns milliseconds since Unix epoch
- `timezone` *(optional)* — timezone to apply

```
date_format(event.eventTime)
date_format(event.eventTime, format:"yyyy-MM-dd")
date_format(event.eventTime, format:"yyyy/MM/dd", timezone:"UTC")
date_format(event.eventTime, format:"epoch")
date_format(event.eventTime, format:"yyyy-MM-dd'T'HH:mm:ss'['VV']'")
```

### DURATION_FORMAT

Formats a duration value. Parameters align with `DATE_FORMAT`.

### DEFAULT

Returns the base expression if non-null; otherwise returns the fallback.

**Parameters:**
- `(anonymous)` — primary expression
- `value` — fallback if primary is null

```
default(event.data.amount, value:"0")
default(event.data.channel, value:"direct")
```

### CONSTANT

Defines a literal constant value.

```
"some constant string"
CONSTANT("some constant string")
```

### CONCATENATE

Concatenates up to 256 values in sequence.

**Parameters:**
- `(anonymous, 0..255)` — values to join

```
concatenate(event.data.referral_link, CONSTANT("?source=test"))
concatenate(event.firstName, CONSTANT(" "), event.lastName)
```

### CONCATENATE_COLLECTION

Joins all elements of a collection into a single string.

**Parameters:**
- `(anonymous)` — collection expression
- `separator` *(optional, default: `,`)* — delimiter
- `unique` *(optional, default: `false`)* — `"true"` deduplicates values

```
concatenate_collection(collection(person(event.personId).steps, extracting:stepName), separator:" | ")
concatenate_collection(collection(person(event.personId).steps, extracting:stepName), unique:"true")
```

### REPLACE

Replaces occurrences of a pattern within a string.

**Parameters:**
- `(anonymous)` — source string
- `search` — pattern to find
- `replacement` — replacement string

```
replace(event.data.amount, search:".00", replacement:"")
```

### SPLIT

Transforms a delimited string into an array.

**Parameters:**
- `(anonymous)` — source string
- `separator` *(optional, default: `,`)* — delimiter

```
split(event.data.tags)
split(event.data.tags, separator:"|")
```

## Date / Period Functions

### START_DATE

Maps a timestamp to the start of the period it falls in.

**Parameters:**
- `(anonymous)` — timestamp column
- `period` — one of: `NONE`, `DAY`, `WEEK`, `MONTH`, `QUARTER`, `YEAR`, `TRAILING_WEEK`, `TRAILING_TWO_WEEKS`, `TRAILING_THREE_WEEKS`, `TRAILING_MONTH`

```
start_date(event.eventTime, period:"DAY")
start_date(event.eventTime, period:"WEEK")
start_date(event.eventTime, period:report_parameters().defaultPeriod)
```

### END_DATE

Maps a timestamp to the end of the period it falls in. Same parameters as `START_DATE`.

```
end_date(event.eventTime, period:"DAY")
end_date(event.eventTime, period:"MONTH")
```

### NOW

Returns the current timestamp at report execution time.

```
now()
```

## Entity Lookup Functions

These functions join to external entities by ID and expose their properties via dot notation.

### PERSON

Loads the full person profile.

**Parameters:**
- `(anonymous)` — column with person ID

**Returns:** `api.Person` properties

```
person(event.personId).email
person(event.personId).firstName
person(event.personId).lastName
person(event.personId).data.someKey
PERSON(event.data.related_person_id).normalizedEmail
```

Key Person properties: `id`, `email`, `normalizedEmail`, `firstName`, `lastName`, `locale`, `data`, `steps`, `rewards`, `friends`, `advocates`, `shareables`, `journeys`, `audienceMemberships`, `recentRequestContexts`.

### CAMPAIGN

Loads the latest state of a campaign.

**Parameters:**
- `(anonymous)` — column with campaign ID

**Returns:** `api.BuiltCampaign` properties

```
campaign(event.campaignId).campaignName
CAMPAIGN(event.campaignId).description
campaign(event.campaignId).state
```

Key Campaign properties: `id`, `name`, `campaignName`, `description`, `state`, `version`, `programLabel`, `tags`, `steps`, `rewardRules`.

### CAMPAIGN_SUMMARY

Builds an aggregated campaign state from all known client change events.

**Parameters:**
- `(anonymous)` — column with campaign ID

**Returns:** `api.CampaignSummary` properties

```
campaign_summary(event.campaignId).campaignName
```

### CLIENT

Loads the client model object. The join column is optional; defaults to the event's client.

**Parameters:**
- `(anonymous, optional)` — column with client ID

**Returns:** `api.Client` properties

```
client(event.clientId).clientType
client(event.clientId).shortName
CLIENT().shortName
CLIENT().clientType
```

### CLIENT_PROPERTIES

Loads the property map associated with the current client. No join column required.

**Returns:** name/value map; access specific properties by name

```
client_properties().vertical
client_properties().testProperty
CLIENT_PROPERTIES().client_property_name
```

### CLIENT_VERTICAL

Shortcut to extract a vertical attribute from a client.

```
CLIENT_VERTICAL(event.clientId).ATTRIBUTE
```

### EVENT

Loads a specific consumer event by ID.

**Parameters:**
- `(anonymous)` — column with consumer event ID

**Returns:** `api.ConsumerEvent` (or subtype: `StepConsumerEvent`, `RewardConsumerEvent`, `InputConsumerEvent`)

```
event(event.rootEventId).name
EVENT(event.id).person.email
EVENT(event.id).selectedCampaignContext.triggerResults
```

Key ConsumerEvent properties: `id`, `rootEventId`, `type`, `eventTime`, `person`, `data`, `sandbox`, `clientContext`.

Additional StepConsumerEvent properties: `name`, `stepName`, `campaignId`, `personId`, `visitType`, `quality`, `attribution`.

### REWARD

Combines all known reward events for a given reward ID into a single summary.

**Parameters:**
- `(anonymous)` — column with reward ID

**Returns:** `api.RewardSummary` properties

```
reward(event.data.reward_id).currentState
REWARD(event.data.reward_id).faceValue
reward(event.rewardId).supplierId
```

Key RewardSummary properties: `id`, `currentState`, `faceValue`, `supplierId`, `rewardType`, `partnerRewardId`, `email`, `data`. States: `EARNED`, `FULFILLED`, `SENT`, `REDEEMED`, `FAILED`, `CANCELED`, `REVOKED`.

### REWARD_SUPPLIER

Loads the reward supplier model.

**Parameters:**
- `(anonymous)` — column with reward supplier ID

**Returns:** `api.RewardSupplier` properties

```
reward_supplier(event.rewardSupplierId).displayType
REWARD_SUPPLIER(event.rewardSupplierId).name
reward_supplier(event.rewardSupplierId).type
```

### STEP_RECORD

Finds the step record for a given step consumer event.

**Parameters:**
- `(anonymous)` — column with step event ID
- `step_name` *(required)* — column with the step name
- `event_time_name` *(required)* — column with the step event time

**Returns:** `api.StepRecord` properties

```
step_record(event.earnedStepEventContext.id, step_name:event.earnedStepEventContext.name, event_time_name:event.earnedStepEventContext.eventTime).visitType
step_record(event.earnedStepEventContext.id, step_name:event.earnedStepEventContext.name, event_time_name:event.earnedStepEventContext.eventTime).data.amount
```

Key StepRecord properties: `id`, `clientId`, `eventTime`, `requestTime`, `personId`, `name`, `deviceType`, `attribution`, `visitType`, `quality`, `data`.

### INPUT_RECORD

Finds the input record corresponding to an input consumer event.

**Parameters:**
- `(anonymous)` — column with input consumer event ID
- `event_name` *(optional)* — column with event name; omit to match any name
- `event_time_name` *(required)* — column with event time

**Returns:** `api.InputRecord` properties

```
input_record(event.rootEventId, event_time_name:event.eventTime).name
input_record(event.rootEventId, event_name:"conversion", event_time_name:event.eventTime).apiType
INPUT_RECORD(event.rootEventId, event_time_name:event.eventTime).userAgent
```

Key InputRecord properties: `id`, `clientId`, `eventTime`, `personId`, `name`, `locale`, `apiType`, `appType`, `deviceType`, `userAgent`, `data`.

### DEVICE_TYPE

Parses a user agent and returns a device/browser/OS classification.

**Parameters:**
- `(anonymous, optional)` — consumer event ID (function joins to the full event to extract user agent)
- `user_agent` *(optional)* — explicit user agent string; use instead of the anonymous event ID
- `mode` *(optional)* — one of:
  - `DEVICE_TYPE` *(default)* — Mobile, Desktop, Other
  - `VERSIONED_DEVICE_TYPE` — e.g. Apple iPhone iOS 17.4.1, Desktop Mac OS X 10.15.7
  - `DETAILED_DEVICE_TYPE` — UNKNOWN, ROBOT, MOBILE, PHONE, DESKTOP, ROBOT_MOBILE, TABLET, TV
  - `BROWSER_TYPE` — e.g. Safari, Chrome, Edge, DuckDuckGo
  - `OS_TYPE` — e.g. Android, iOS, Linux, Tizen

```
device_type(event.rootEventId)
device_type(event.rootEventId, mode:"OS_TYPE")
device_type(user_agent:event.userAgent)
device_type(user_agent:event.userAgent, mode:"BROWSER_TYPE")
```

## Collection Functions

### COLLECTION

Filters and optionally extracts fields from a collection.

**Parameters:**
- `(anonymous)` — source collection expression
- `filter` *(optional, repeatable)* — filter predicate; use `and`/`or` within one `filter:` parameter, or supply multiple separate `filter:` parameters (all must match)
- `extracting` *(optional)* — extract a single field from each element

```
collection(person(event.personId).steps, filter:stepName=="converted")
collection(person(event.personId).steps, filter:stepName=="converted" and quality=="HIGH")
collection(person(event.personId).steps, extracting:stepName)
collection(event(event.id).selectedCampaignContext.triggerResults, filter:passed=="false")
COLLECTION(PERSON(event.personId).steps, filter:stepName=="transacted" AND campaignId!="null")
```

Multiple separate `filter:` arguments (implicit AND between them):

```
COLLECTION(EVENT(event.id).person.steps, filter:stepName=="legacy_incentivized" or stepName=="risk_evaluated", filter:stepName!="transacted")
```

### COUNT

Counts all elements in a collection. Used in records reports (not metrics); wraps a `COLLECTION` expression.

```
COUNT(COLLECTION(person(event.personId).steps))
COUNT(COLLECTION(person(event.personId).steps, filter:stepName=="converted"))
```

### COUNT_DISTINCT

Counts distinct values of the extracted field across a collection. Used in records reports (not metrics).

```
COUNT_DISTINCT(COLLECTION(person(event.personId).steps, filter:stepName=="signup"))
COUNT_DISTINCT(COLLECTION(person(event.personId).steps, filter:stepName=="invest_core" OR stepName=="signup" OR stepName=="failed", extracting:campaignId))
```

### PERSON_COLLECTION

Paginated, memory-efficient collection extraction from a person profile. Preferred over `COLLECTION` for person data.

**Parameters:**
- `(anonymous)` — person ID (must come from `person(id).id` to ensure identity resolution)
- `collection` *(required)* — one of: `steps`, `rewards`, `friends`, `advocates`, `shareables`, `journeys`, `audience_memberships`, `request_contexts`, `shares`, `data`
- `filter` *(optional)* — filter predicate
- `extracting` *(optional)* — field to extract from each element
- `reduce` *(optional)* — aggregation to apply: `sum`, `count`, `min`, `max`

```
person_collection(person(event.personId).id, collection:"steps", filter:stepName=="converted", extracting:eventId, reduce:"count")
person_collection(person(event.personId).id, collection:"steps", filter:aliasName=="false", extracting:eventId, reduce:"count")
person_collection(person(event.personId).id, collection:"steps", filter:stepName=="converted" and quality=="HIGH", extracting:value, reduce:"sum")
person_collection(person(event.personId).id, collection:"rewards", filter:currentState=="FULFILLED", reduce:"count")
```

### FIRST

Returns the first element of a collection, optionally after sorting.

**Parameters:**
- `(anonymous)` — source collection
- `sortBy` *(optional)* — field to sort by before selecting
- `(anonymous, 2nd)` — sub-property to extract from the selected element

```
first(collection(person(event.personId).steps, filter:stepName=="converted"), sortBy:eventDate).eventDate
first(collection(person(event.personId).steps, filter:stepName=="application_started"), sortBy:createdDate).campaignId
FIRST(EVENT(event.eventId).person.steps, sortBy:eventDate).stepName
```

### LAST

Returns the last element of a collection, optionally after sorting. Same parameters as `FIRST`.

```
last(collection(person(event.personId).steps, filter:stepName=="converted"), sortBy:eventDate).eventDate
LAST(EVENT(event.eventId).person.steps, sortBy:eventDate).partnerEventId
LAST(COLLECTION(PERSON(event.personId).recentRequestContexts), sortBy:createdAt).geoIp.ip_address
```

### INDEX

Returns the element at a specific position in a collection.

**Parameters:**
- `(anonymous)` — source collection
- `index` *(required)* — zero-based integer index
- `sortBy` *(optional)* — field to sort by before indexing

```
index(person(event.personId).steps, sortBy:eventDate, index:"0")
index(person(event.personId).steps, sortBy:eventDate, index:"2")
```

### EXPLODE

Expands an array into multiple rows — one row per element.

**Parameters:**
- `(anonymous)` — array expression

```
explode(event.arrayPropertyName)
EXPLODE(PERSON(event.personId).recentRequestContexts).geoIp.zip_code
EXPLODE(SPLIT(event.data.tags))
```

## Aggregation Functions (Metrics Reports Only)

These functions are only valid in metrics report types (e.g. `CONFIGURABLE_EVENT_METRICS`, Input Record Metrics, etc.).

### Advocate vs. Friend Funnel — event.personId Identity

`GROUP_*` functions load events matching the given `step_name`. The meaning of `event.personId` on those events depends on which side of the referral funnel the step belongs to. **Which steps belong to which funnel side is determined by the journey configuration in the campaign** — advocate-journey steps record the advocate as `event.personId`, friend-journey steps record the friend.

| Funnel side | Example steps | `event.personId` represents |
| --- | --- | --- |
| Advocate journey | `shared`, `email_sent` | The advocate (Advocate ID) |
| Friend journey | `share_clicked`, `converted`, `signup` | The friend |

If you want to measure advocate activity using a **friend-funnel step** (e.g. how many share clicks each advocate generated), group by `event.data.related_person_id`, not `event.personId`:

```
Advocate Id=event.data.related_person_id; Share Clicks=GROUP_COUNT_DISTINCT(event.id, step_name:"share_clicked");
```

If you mix advocate-side and friend-side steps in the same report, use `BOOLEAN_FORMAT` to pick the correct person ID conditionally:

```
Advocate Id=BOOLEAN_FORMAT(event.name=="SHARE_EVENT", event.personId, event.data.related_person_id);
```

Pulling `GROUP_COUNT_DISTINCT(event.personId, step_name:"shared")` and expecting it to represent advocates is correct — `shared` is an advocate-funnel step, so `event.personId` is the advocate. But pulling `GROUP_COUNT_DISTINCT(event.personId, step_name:"share_clicked")` gives you a count of unique friends, not advocates. Mix the two step names without accounting for this and the person IDs represent different populations in each column.

All aggregation functions share a common set of optional filter parameters in addition to their required ones:

| Parameter | Description |
| --- | --- |
| `step_name` | Step name to match (use `"ALL"` for any step; required for metrics on step records) |
| `name` | Input event name (required for input record metrics) |
| `names` | Comma-separated list of input event names |
| `audience_id` | Audience ID filter |
| `attribution` | `ALL`, `ATTRIBUTED`, `UNATTRIBUTED` |
| `quality` | `ALL`, `HIGH`, `LOW`, `NONE` |
| `visit_type` | `ALL`, `NEW_TO_CLIENT`, `NEW_TO_PROGRAM`, `NEW_TO_CAMPAIGN`, `NORMAL` |
| `channel` | Channel filter string |
| `source` | Source filter string |
| `time_range` | `CURRENT`, `ALL_TIME`, `SAME_PERIOD_PRIOR_TIME_RANGE`, `SAME_PERIOD_PRIOR_YEAR`, `SAME_PERIOD_PRIOR_QUARTER`, `SAME_PERIOD_PRIOR_MONTH`, `SAME_PERIOD_PRIOR_WEEK` |

### GROUP_COUNT

Counts the number of records matching the group.

```
GROUP_COUNT(event.id, step_name:"converted")
group_count(event.id, step_name:"ALL")
GROUP_COUNT(event.id, name:"call_to_action")
GROUP_COUNT(event.id, step_name:"converted", attribution:"ALL", quality:"HIGH", visit_type:"NEW_TO_CLIENT", channel:"email", source:"source", time_range:"ALL_TIME")
```

### GROUP_COUNT_DISTINCT

Counts distinct values of the given expression within the group.

```
GROUP_COUNT_DISTINCT(event.personId, step_name:"converted")
GROUP_COUNT_DISTINCT(event.id, step_name:"share_clicked", visit_type:"ALL")
group_count_distinct(event.id, name:"conversion")
GROUP_COUNT_DISTINCT(event.id, audience_id:"1")
GROUP_COUNT_DISTINCT(event.personId, step_name:"converted", attribution:"ALL", quality:"HIGH", visit_type:"NEW_TO_CLIENT", channel:"email", source:"source", time_range:"ALL_TIME")
```

### GROUP_SUM

Sums the values of the expression within the group.

```
GROUP_SUM(event.data.amount, step_name:"converted")
GROUP_SUM(reward(event.data.reward_id).faceValue, step_name:"advocate_reward_earned")
GROUP_SUM(event.amount, step_name:"converted", attribution:"ALL", quality:"HIGH", visit_type:"NEW_TO_CLIENT", channel:"email", source:"source", time_range:"ALL_TIME")
```

### GROUP_AVG

Averages the values of the expression within the group.

```
GROUP_AVG(event.data.amount, step_name:"converted")
```

### GROUP_MIN

Returns the minimum value within the group.

```
GROUP_MIN(event.eventTime, step_name:"converted")
GROUP_MIN(event.data.amount, step_name:"ALL")
```

### GROUP_MAX

Returns the maximum value within the group.

```
GROUP_MAX(event.eventTime, step_name:"converted")
GROUP_MAX(event.data.amount, step_name:"converted", quality:"HIGH")
```

### GROUP_FIRST

Returns the first occurrence of the expression within the group, ordered by event time.

```
GROUP_FIRST(PERSON(event.personId).email, step_name:"converted")
GROUP_FIRST(event.eventTime, step_name:"registered")
GROUP_FIRST(PERSON(event.personId).email, step_name:"converted", attribution:"ALL", quality:"HIGH", visit_type:"NEW_TO_CLIENT", channel:"email", source:"source", time_range:"ALL_TIME")
```

### GROUP_LAST

Returns the last occurrence of the expression within the group.

```
GROUP_LAST(event.amount, step_name:"converted")
GROUP_LAST(event.data.channel, step_name:"converted", attribution:"ALL")
GROUP_LAST(event.amount, step_name:"converted", attribution:"ALL", quality:"HIGH", visit_type:"NEW_TO_CLIENT", channel:"email", source:"source", time_range:"ALL_TIME")
```

### GROUP_CONCATENATE

Concatenates all values of the expression within the group.

```
GROUP_CONCATENATE(event.data.source, step_name:"converted")
```

## Arithmetic & Rate Functions

### SUM

Adds two expressions.

```
SUM(event.data.amount, event.data.bonus)
SUM(date_format(event.eventTime, format:"epoch"), date_format("604800000", format:"epoch"))
```

### SUBTRACT

Subtracts the second expression from the first.

```
SUBTRACT(event.data.endAmount, event.data.startAmount)
SUBTRACT(date_format(event.eventTime, format:"epoch"), "3888000000")
```

### RATE

Calculates a rate: value / denominator.

```
RATE(Convertors, Share Link Clickers)
RATE(event.data.amount, "3.333333333333")
```

### PERCENTAGE

Calculates a percentage: (value / total) * 100.

```
PERCENTAGE(Convertors, Share Link Clickers)
```

### BENCHMARK

Compares a rate to a benchmark threshold.

```
BENCHMARK(Convertors, Share Link Clickers, "150")
```

## Utility Functions

### MAP_DIMENSION

Maps a value to a dimension definition stored in the platform.

**Parameters:**
- `(anonymous)` — source value expression
- `dimension_name` — name of the dimension
- `program_label` — program label expression

```
MAP_DIMENSION(event.data.source, dimension_name:"source", program_label:event.programLabel)
```

### REPORT_PARAMETERS

Provides access to dynamic parameters passed at report execution time. Useful for parameterized templates.

```
report_parameters().defaultPeriod
report_parameters().defaultStepName
start_date(event.eventTime, period:report_parameters().defaultPeriod)
```

### GEO_IP

Extracts geo-location data from an IP address.

```
geo_ip(event.data.ip).country
geo_ip(event.data.ip).city
```

### SUPPORT

Provides access to support-related metadata for the event's client.

```
support().salesforceAccountId
```

### RISK_VALUE

Extracts a risk signal value.

```
risk_value(event.id).score
```

# Enums Reference

## Attribution

Controls which events are included based on attribution status.

| Value | Description |
| --- | --- |
| `ALL` | Attributed and unattributed events |
| `ATTRIBUTED` | Only events with attribution |
| `UNATTRIBUTED` | Only events without attribution |

## Visit Type

Segments events by whether the person is new to a given scope.

| Value | Description |
| --- | --- |
| `ALL` | All visit types |
| `NEW_TO_CLIENT` | First visit to this client |
| `NEW_TO_PROGRAM` | First visit to this program |
| `NEW_TO_CAMPAIGN` | First visit to this campaign |
| `NORMAL` | Returning visitor |

## Quality

Filters events by conversion quality signal.

| Value | Description |
| --- | --- |
| `ALL` | All quality levels |
| `HIGH` | High-quality conversions |
| `LOW` | Low-quality conversions |
| `NONE` | No quality signal |

## Time Period (for START_DATE / END_DATE)

| Value | Description |
| --- | --- |
| `NONE` | No period bucketing |
| `DAY` | Calendar day |
| `WEEK` | Calendar week |
| `MONTH` | Calendar month |
| `QUARTER` | Calendar quarter |
| `YEAR` | Calendar year |
| `TRAILING_WEEK` | Rolling 7-day window |
| `TRAILING_TWO_WEEKS` | Rolling 14-day window |
| `TRAILING_THREE_WEEKS` | Rolling 21-day window |
| `TRAILING_MONTH` | Rolling 30-day window |

## Column Time Range (for Aggregation Functions)

| Value | Description |
| --- | --- |
| `CURRENT` | Within the report's time range |
| `ALL_TIME` | All available history |
| `SAME_PERIOD_PRIOR_TIME_RANGE` | Same duration, immediately preceding |
| `SAME_PERIOD_PRIOR_YEAR` | Same period one year ago |
| `SAME_PERIOD_PRIOR_QUARTER` | Same period one quarter ago |
| `SAME_PERIOD_PRIOR_MONTH` | Same period one month ago |
| `SAME_PERIOD_PRIOR_WEEK` | Same period one week ago |

## Person Collection Names (for PERSON_COLLECTION)

| Value | Description |
| --- | --- |
| `steps` | Person's step records |
| `rewards` | Person's rewards |
| `friends` | Friends referred by this person |
| `advocates` | Advocates who referred this person |
| `shareables` | Shareable links/content |
| `journeys` | Journey memberships |
| `audience_memberships` | Audience segment memberships |
| `request_contexts` | Recent request context records |
| `shares` | Share events |
| `data` | Person data entries |

# Recipes

## Count Events by Step (Metrics Report)

```
step=event.stepName; count=group_count_distinct(event.id, step_name:"ALL"); unique_persons=group_count_distinct(event.personId, step_name:"ALL");
```

## Traffic Funnel With Attribution Filters

```
Share Link Clickers=GROUP_COUNT_DISTINCT(event.personId, step_name:"share_clicked", visit_type:"ALL"); Signups=GROUP_COUNT_DISTINCT(event.personId, step_name:"signup", visit_type:"NEW_TO_CLIENT"); Convertors=GROUP_COUNT_DISTINCT(event.personId, step_name:"converted", visit_type:"ALL"); Conversion Rate=RATE(Convertors, Share Link Clickers);
```

## Count Input Events by Name, App Type, and API Type

```
name=event.name; app_type=event.appType; api_type=event.apiType; count=group_count_distinct(event.id, name:"all");
```

## Daily Bucketing

```
Day=end_date(event.eventTime, period:"DAY"); Count=group_count_distinct(event.id, step_name:"converted");
```

## Person Details With Lookup

```
Email=person(event.personId).email; First Name=person(event.personId).firstName; Last Name=person(event.personId).lastName; Campaign Name=campaign(event.campaignId).campaignName;
```

## Conditional Column (Boolean Format)

```
quality_score=boolean_format(event.quality == "HIGH", "PASSING", "SUSPICIOUS"); Has Conversion=boolean_format(EVENT(event.id).name=="converted","Y","N");
```

## Add N Days Offset to a Timestamp (e.g. +7 Days)

```
offset_date=date_format(replace(concatenate(number_format(SUM(date_format(event.eventTime, format:"epoch"), date_format("604800000", format:"epoch"))), ""), search:".00", replacement:""))
```

## Extract Device Type From Input Record

```
Device=device_type(user_agent:event.userAgent); OS=device_type(user_agent:event.userAgent, mode:"OS_TYPE"); Browser=device_type(user_agent:event.userAgent, mode:"BROWSER_TYPE");
```

## Count Steps on a Person Profile

```
count_converted=person_collection(person(event.personId).id, collection:"steps", filter:stepName=="converted", extracting:eventId, reduce:"count")
```

## Sum Total Rewards Issued

```
reward_value=GROUP_SUM(reward(event.data.reward_id).faceValue, step_name:"advocate_reward_earned")
```

## Cross-Client API Type Breakdown (Run From Extole Account)

Report parameters:
- `target_client_ids`: `ALL_CLIENTS`
- `filters`: `client(event.clientId).clientType=="CUSTOMER"`

`mappings`:

```
API Type=INPUT_RECORD(event.rootEventId, event_time_name:event.eventTime).apiType; Client=CLIENT(event.clientId).shortName; Event Count=GROUP_COUNT_DISTINCT(event.id, step_name:"ALL");
```

## Check if a Referral Exists on a Person (With Hidden Intermediate)

```
hidden(step)=FIRST(COLLECTION(PERSON(event.personId).steps, filter:stepName=="application_started" or stepName=="share_clicked" or stepName=="share_email_delivered" and eventDate<=ACH_Event_Date and programLabel=="refer-a-friend"), sortBy:"createdDate"); Campaign Name=campaign(property(step).campaignId).campaignName;
```

## Compare a Step Date Against a Rolling 45-Day Window

```
ACH_Event_Date=event.eventTime; hidden(45_Days_Offset)=DATE_FORMAT(replace(concatenate(number_format(SUBTRACT(date_format(ACH_Event_Date, format:"epoch"), "3888000000")), ""), search:".00", replacement:""), format:"YYYY-MM-dd'T'hh:mm:ss", timezone:"Z"); Application Completed Within 45 Days=LAST(COLLECTION(PERSON(event.personId).steps, filter:stepName=="application_completed" and programLabel=="refer-a-friend" and eventDate>=45_Days_Offset and quality=="HIGH"), sortBy:"createdDate").eventDate;
```

## Parameterized Period (Using REPORT_PARAMETERS)

```
Period Start=start_date(event.eventTime, period:report_parameters().defaultPeriod); Step Count=group_count_distinct(event.id, step_name:report_parameters().defaultStepName);
```

## Client Vertical

```
vertical=CLIENT_PROPERTIES().vertical
```

## Null-Safe Data Extraction

```
Amount=default(event.data.amount, value:"0"); Channel=default(event.data.channel, value:"unknown");
```

## Null Check Filter

Column `Has_Share_Click` must not be absent:

```
Has_Share_Click!="null"
```

## Salesforce Account ID

```
salesforce_account_id=support().salesforceAccountId
```

## Count Steps on a Person Profile (Records Report)

Use `COUNT_DISTINCT(COLLECTION(...))` in records reports where `PERSON_COLLECTION` is not available:

```
count_signup=COUNT_DISTINCT(COLLECTION(person(event.personId).steps, filter:stepName=="signup"))
```

## Count Targeted Campaigns Across Multiple Step Names

Counts distinct campaigns touched by steps matching any of several step names:

```
campaign_count=COUNT_DISTINCT(COLLECTION(person(event.personId).steps, filter:stepName=="invest_core" OR stepName=="signup" OR stepName=="failed", extracting:campaignId))
```

## Count All Events (Any Step)

```
count=GROUP_COUNT(event.id, step_name:"ALL")
```

## Rate as a Fraction (e.g. 30%)

Pass `"3.333333333333"` as the denominator to compute 30%:

```
Reward Rate=RATE(event.data.amount, "3.333333333333")
```

## Input Record Metrics — Count by Name, App Type, and API Type

```
name=event.name; app_type=event.appType; api_type=event.apiType; count=group_count_distinct(event.id, name:"all");
```

## Input Record Metrics — Count a Specific Input Event per Person per Day

```
day=END_DATE(event.eventTime, period:"DAY"); person_id=person(event.personId).id; count=group_count_distinct(event.id, name:"terms");
```

## Metrics — Shares and Conversions per Person

```
person_email=person(event.personId).email; shares=group_count_distinct(event.id, step_name:"shared"); conversions=group_count_distinct(event.id, step_name:"converted");
```
