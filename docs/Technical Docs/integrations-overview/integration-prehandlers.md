---
title: "Normalize Inbound Events with a Prehandler"
excerpt: "Reshape a partner's own webhook at ingest — rename the event, flatten the payload, scope it to one integration — so a partner whose wire format you cannot change can post directly to Extole.\n"
---

This page is one part of the Management API integration guide. Start at [Create an Integration with the Management API](doc:management-api-integration) for the build paths and the creation contract.

# Overview

A prehandler is a rule that runs against an inbound event **before** the platform decides what the event is. It sees the untouched HTTP request, and it can rename the event, add and remove data, set the app type, and set the sandbox. Everything downstream — the `input_event` trigger rules in [Map Inbound Partner Events](doc:integration-inbound-events), the data components, the business events — sees only what the prehandler left behind.

That ordering is the whole point. An `input_event` rule matches an event name, and a data component reads a field out of the event's data. Both assume the event already arrived with an Extole-shaped name and an Extole-readable payload. A prehandler is how it comes to have them.

## Decide Whether This Integration Needs One

The question is not what the partner sends. It is **who controls the shape of what is sent**.

| Who sends the event | What they can do | Prehandler |
| :------------------ | :--------------- | :--------- |
| An extension, plugin, or service written for this integration | Post `POST /v6/events` with the canonical `event_name` and flat data keys | Not needed |
| The partner's own webhook, with a payload shape the partner defines | Post exactly what the partner decided to post, and nothing else | **Required** |

`POST /v6/events` takes `event_name` as a required field of the request body. A partner webhook does not have one. Some platforms name the event in a body field of their own choosing, such as `type` or `topic`; others carry it only in a header, or only implicitly in which endpoint you registered for it. None of them flatten their payload into the keys an integration's data components read. There are only two ways to reconcile that, and they are not equivalent:

- **A prehandler**, which does the reshaping inside Extole. The partner points its webhook at Extole and the integration is finished.
- **A translation service the customer builds and hosts**, which receives the partner's webhook, reshapes it, and posts the result. The integration is finished only after the customer completes an engineering project that no part of this guide describes.

Choose the second only when the customer has asked for it. Writing setup instructions that tell a customer to stand up a webhook receiver is not a completed integration; it is an integration with its hardest step moved into the instructions. If you take that path, say so plainly and say why, rather than leaving it for the reader to discover in the configuration tab.

## Give the Partner a URL It Can Post To

A partner's webhook configuration usually accepts a URL and nothing else — no body template and no headers. The named form of the Events API is built for that:

```
https://api.extole.io/v6/events/example_webhook?access_token=$EVENTS_API_ACCESS_TOKEN
```

Two properties make it work where `POST /v6/events` does not. The last path segment becomes the event name, so you choose the wire name rather than asking the partner to send one. And the request body becomes the event's data as it arrived, with no required fields, so the partner's own envelope — its event type, its field names, its nesting — is accepted whole and reaches the prehandler intact.

Name the segment after the partner's wire event rather than the canonical one, `example_webhook` rather than `converted`, because producing the canonical name is the prehandler's job. Then match that segment with an `EVENT_NAME_MATCH` condition. It is the one condition guaranteed to hold, because you chose the value.

The access token authorizes the delivery. Extole reads it from the `access_token` query parameter, an `Authorization` header, or a cookie, in that order, and a partner that can only set a URL has the query parameter. Create the token in the <Anchor label="Security Center" target="_blank" href="https://my.extole.com/security-center">Security Center</Anchor> as described in [Send Platform Events to Extole](doc:sending-platform-events), and authorize it for event submission only — never a token that can also manage campaigns and components.

One field in the partner's body is inspected at the API boundary: a top-level `event_time`, which must parse as a date or the delivery is rejected as `invalid_event_time_format`. Nothing else in the body is read until the prehandler runs.

### Request Signatures Are Not Verified

The token in the URL authenticates an inbound event. Extole does not verify a partner's request-signature header — `Stripe-Signature`, `X-Shopify-Hmac-Sha256`, or any other — on packaged and client-local integrations alike.

**The partner's webhook signing secret is therefore not required, and the build is not blocked on obtaining it.** Say so when someone offers to go find it. Matching a signature header in a condition recognizes the partner's traffic rather than authenticating it, and it works from the header being present rather than from its contents.

Treat the endpoint URL as the credential it carries. Register it in the partner's webhook configuration, keep it out of shared documents, and rotate the token as you would any other server-side token. When a customer's security review calls for cryptographic verification of the partner's signature, raise it as a requirement rather than composing a verification script in a prehandler.

## Prerequisites

- A server-side access token authorized to manage prehandlers. Creating one is an administrative operation, not a campaign edit.
- A published integration campaign with its model component, built through [Create the Integration Campaign and Component Model](doc:integration-component-model).
- The production API host in `EXTOLE_API_HOST`.
- A real sample of the partner's webhook: the body, and the headers it arrives with. The headers matter as much as the body, and a payload example copied from partner documentation usually omits them.

## Required Parameters

| Parameter | Purpose |
| :-------- | :------ |
| `MANAGEMENT_API_ACCESS_TOKEN` | Bearer token on every call. |
| `EVENTS_API_ACCESS_TOKEN` | Authorizes the partner's deliveries to the named endpoint above. A separate, event-submission-only token. |
| `EXTOLE_API_HOST` | Production host. |
| `INTEGRATION_COMPONENT_ID` | The model component the prehandler is scoped to, which is also the component whose settings its scripts can read. |

## Create the Prehandler

A prehandler is a name, an ordered pair of condition and action lists, and a reference to the component it belongs to:

```bash
curl --request POST "$EXTOLE_API_HOST/v6/prehandlers" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "example_v10_order_completed_to_converted",
    "description": "Renames the Example order webhook to the canonical converted event and flattens its payload.",
    "enabled": true,
    "order": 0,
    "conditions": [
      { "type": "EVENT_NAME_MATCH", "event_names": ["example_webhook"] },
      { "type": "EXPRESSION", "expression": "javascript@runtime:(function(){ var body = context.getProcessedRawEvent().getData(); return body.get(\"type\") === \"order.completed\"; })();" }
    ],
    "actions": [
      { "type": "EXPRESSION", "expression": "javascript@runtime:(function(){ var builder = context.getEventBuilder(); var body = context.getProcessedRawEvent().getData(); var data = body.get(\"data\"); if (!data) { return; } var order = data.get(\"order\"); if (!order) { return; } builder.withEventName(\"converted\"); builder.addData(\"partner_conversion_id\", order.get(\"id\")); builder.addData(\"partner_user_id\", order.get(\"customer_id\")); builder.addData(\"cart_value\", order.get(\"total_amount\")); builder.addData(\"email\", order.get(\"customer_email\")); })();" }
    ],
    "component_references": [{ "component_id": "'"$INTEGRATION_COMPONENT_ID"'" }]
  }'
```

Three fields decide whether it does anything at all, and each defaults to the value that does nothing:

- **`enabled` defaults to `false`.** A prehandler created without it is stored, listed, and never run. This is a common reason a prehandler that plainly exists has no effect.
- **`order` defaults to `0`**, and prehandlers run in ascending order. When one prehandler sets the app type another reads, or one renames an event another matches by name, the order is the dependency between them and not a formality.
- **Conditions are ANDed, and an empty condition list matches everything.** A prehandler with no conditions runs its actions against every event in the account, including web events that have nothing to do with the partner. Always give it at least one condition.

Names are unique per client and accept only alphanumeric characters, dashes, dots, and underscores. A name with a space in it is rejected as `prehandler_name_contains_illegal_character`, and a repeat is rejected as `prehandler_name_duplicated`. Follow the packaged convention and name it after the component, the generation, and the transformation — `example_v10_order_created_to_conversion_event` — so the prehandler list reads as a set of transformations rather than a set of scripts.

### Choose the Conditions

| `type` | Fields | Matches on |
| :----- | :----- | :--------- |
| `EVENT_NAME_MATCH` | `event_names` | The event name as it arrived, which for a partner webhook is the path segment you gave it. |
| `HTTP_HEADER_MATCH` | `http_headers`, `http_header_names` | Presence of a header, or a header with one of a set of values. Narrows an endpoint that receives more than one kind of traffic. |
| `DATA_EXISTS` | `data_keys` | Presence of a key in the event data. |
| `EXPRESSION` | `expression` | Anything the script context can reach. |
| `BLOCK_MATCH` | `considered_block_list_types` | The event matching an account block list. |
| `JAVASCRIPT_V1` | `javascript` | Same as `EXPRESSION`, with a bare function body instead of an evaluatable. |

Recognize the partner before you reshape anything. When the partner posts to the named endpoint above, the path segment is that recognition, and an `EVENT_NAME_MATCH` on it keeps the prehandler from firing on unrelated traffic. A header condition adds a second signal where one is warranted: a webhook almost always carries a partner-specific header — a request signature, the sending store or account domain, a delivery identifier. Take the header name from the partner's webhook documentation, and read a real delivery to confirm it arrives, because header lists in partner documentation are frequently incomplete.

When an account holds two instances of the same integration, that is not enough on its own: both instances answer the same event name and see the same header. Add an expression condition comparing a value in the request — the sending store URL, the partner account identifier, whatever the payload or headers carry — against the corresponding setting on this instance's component. This is how the packaged integrations scope a shared partner app to one installation.

`EXPRESSION` and `JAVASCRIPT_V1` do the same work through different fields. `EXPRESSION` takes an evaluatable string beginning `javascript@runtime:`; `JAVASCRIPT_V1` takes a bare function body under a `javascript` key. Bundled components use `EXPRESSION`, and matching them keeps a client-local build comparable to a packaged one.

### Choose the Actions

| `type` | Fields | Does |
| :----- | :----- | :--- |
| `EXPRESSION` | `expression` | Anything the builder exposes. The only action type that can rename an event. |
| `SET_DATA` | `data`, `default_data`, `delete_data` | Sets, defaults, and removes data keys. Values are evaluatable expressions. |
| `MAP_DATA_ATTRIBUTES` | `data_attribute_mappings` | Copies `source_attribute` to `attribute`, with an optional `default_value`. |
| `SET_SANDBOX` | `sandbox_id` | Routes the event to a sandbox. |
| `JAVASCRIPT_V1` | `javascript` | As `EXPRESSION`, with a bare function body. |

Use `MAP_DATA_ATTRIBUTES` when the transformation is a flat rename and `EXPRESSION` when it is not. A partner payload that nests its interesting fields — an order object under a `data` key, a line-item array to be summed, an amount in minor units to be divided — needs an expression, because the mapping types address top-level keys.

## What the Scripts Can Reach

Both conditions and actions receive a context object. A condition returns a boolean; an action returns nothing and works through the builder.

| Call | Returns | Use for |
| :--- | :------ | :------ |
| `context.getRawEvent()` | The untouched HTTP request | `getHttpRequestBody()`, `getHttpHeaders()`, `getHttpParameters()`, `getHttpCookies()`, `getUrl()`, `getSourceIps()`, `getHttpRequestMethod()`, `getRawEventId()` |
| `context.getProcessedRawEvent()` | The parsed event | `getEventName()`, `getData()`, `getVerifiedData()`, `getAppType()`, `getAppData()`, `getSandbox()`, `getDeviceId()`, `getPageId()`, `getEventTime()` |
| `context.getVariable(name)` | A setting on the referenced component | Reading this integration instance's own configuration |
| `context.getCandidatePerson()` | The person, **or null** | Identity already resolved at this point |
| `context.log(message)` | — | A line in the event's log messages |
| `context.getGlobalServices()` | The shared service set | `getJsonService()`, `getStringService()`, `getDateService()`, `getNotificationService()`, and the rest |
| `context.getEventBuilder()` | The builder, **actions only** | Every mutation below |

The builder is where an action does its work:

| Builder call | Changes |
| :----------- | :------ |
| `withEventName(name)` | The event name every downstream rule matches on |
| `addData(name, value)` / `addData(map)` | Event data, which is what data components read |
| `removeData(name)` / `addVerifiedData(name, value)` | Event data, removed or marked verified |
| `withAppType(type)` / `withDefaultAppType(type)` | The app type, which scopes event streams and reporting |
| `addAppData(name, value)` / `removeAppData(name)` | App data |
| `withSandbox(id)` / `withEventTime(time)` / `withClientDomain(domain)` | Routing and provenance |
| `withDeviceId(id)` / `withPageId(id)` / `withDeviceType(type)` / `withDeviceOs(os)` | Device attribution |
| `addJwt(jwt)` / `addSourceGeoIp(ip)` / `removeSourceGeoIp(ip)` | Identity and geolocation inputs |

`getHttpHeaders()` returns each header as an array of values, so a single-valued header is read as `getHttpHeaders().get("x-example-signature")[0]`. `getData()` returns a map, and the packaged prehandler scripts read it both as `data.get("field_name")` and as `data.field_name`. Use the explicit `.get(name)` form, which works in both places.

`getCandidatePerson()` returns null on anonymous and first-touch traffic. Calling a method on it without a guard is the most common cause of the `prehandler_action_execution_failure` alerts described in the prehandler alert runbook, and it fails on exactly the traffic a new integration sees first.

## Scope It to the Integration Component

`component_references` attaches the prehandler to the component it belongs to. This is not bookkeeping: the reference is what gives `context.getVariable(name)` something to read, so a prehandler that consults its integration's settings only works when it is attached to that integration.

An external element carries **at most one** component reference; a second is rejected as `external_elements_cannot_have_multiple_references`. The reference resolves against the **published** campaign, exactly as it does for the report runner and event stream in [Add the Activity and Event Views](doc:integration-activity-views), so publish the campaign before creating the prehandler and expect `invalid_component_reference` if you do not.

`component_ids` is accepted and echoed back alongside `component_references`, but it is deprecated. Send `component_references`.

## Nothing Validates the Script

The create call checks that a name is present and legal, that a referenced component resolves, and that each condition and action carries the field its type requires. **It does not check that the script runs.** An expression calling a method that does not exist is accepted with a `200`, and so is one that is not valid JavaScript. Both are stored, both report themselves as enabled, and neither does anything.

The failure surfaces only when an event arrives, as a `prehandler_condition_execution_failure` or `prehandler_action_execution_failure` notification. Event processing continues either way — a prehandler that throws does not reject the event, it just leaves it unmodified — so the visible symptom is an integration that receives events and creates no steps.

Send a real event and read the result. A prehandler is never finished at the create call.

## Point the Trigger Rule at the Name the Prehandler Produces

Because prehandlers run first, the `input_event` rule in [Map Inbound Partner Events](doc:integration-inbound-events) should list the **canonical** event name when a prehandler renames the event, not the partner's wire name. Listing the wire name there is a rule that will never match, and it looks correct in the tree.

The same applies to data components. Their `valueExpression` reads the event as the prehandler left it, so a mapping written against the partner's raw nesting captures nothing once the prehandler has flattened it. Write the prehandler and the data mappings against one agreed shape, and prefer flattening in the prehandler so the data components stay simple.

## Error Handling

| Response | Cause | What to do |
| :------- | :---- | :--------- |
| `prehandler_name_missing` | No `name`. | Send one. |
| `prehandler_name_contains_illegal_character` | The name has a space or other punctuation. | Use alphanumeric, dash, dot, and underscore only. |
| `prehandler_name_duplicated` | A prehandler of that name exists for the client. | Read the list before creating; names are account-wide, not campaign-scoped. |
| `invalid_component_reference` | The referenced component is not in a published campaign. | Publish the campaign, then create the prehandler. |
| `external_elements_cannot_have_multiple_references` | More than one component reference. | Reference one component. |
| `prehandler_condition_is_empty` | An `HTTP_HEADER_MATCH` with neither headers nor header names. | Send at least one. |
| `prehandler_build_failed` | A buildtime evaluatable in `name`, `enabled`, or `order` failed to compile. | Fix the expression; runtime expressions in conditions and actions are not covered by this check. |
| A `200` and no behavior | The prehandler is disabled, its conditions never match, or its script throws. | Check `enabled` first, then the conditions, then the runtime notifications. |

## Confirm It Runs

Read the built form, which shows `enabled`, `order`, and the evaluated name as the runtime sees them rather than as source expressions:

```bash
curl --request GET "$EXTOLE_API_HOST/v6/prehandlers/$PREHANDLER_ID/built" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN"
```

Then send a copy of the partner's real webhook, headers included, and confirm three things in order: that a step was created on the canonical business event, that every field the data components map is populated, and that no prehandler failure notification was raised. A step created with empty data means the prehandler matched and its mapping is wrong; no step at all means it did not match, or never ran.
