---
title: "Build a Reward Fulfillment Integration"
excerpt: "Create the supplier type, support campaign, supplier templates, reward webhooks, report runner, and event stream for a partner that fulfills rewards.\n"
---

This page is one part of the Management API integration guide. Start at [Create an Integration with the Management API](doc:management-api-integration) for the build paths and the creation contract.

## Build a Reward Fulfillment Integration

A reward fulfillment partner needs everything an outbound partner needs plus a supply side: a component type for the partner's own reward suppliers, a support campaign holding one template per product the partner sells, and webhooks typed `REWARD` that fire only for rewards from those suppliers. [Integration Categories](doc:integration-categories) describes the model; this section is the order to build it in.

### The Finished Shape

Compare against this before reporting a build complete:

```text
root
└── example                       integration-v10.x
    ├── rewardSuppliers           MULTI_SOCKET → example-reward-supplier-v10.0
    │   └── one installed template per product the partner sells
    └── views                     MULTI_SOCKET
        ├── configuration         config-view-v10.0           credential and account settings
        ├── reward-suppliers      config-view-v10.0           the supplier socket
        ├── report-runner-view    report-runner-view-v10.0    the reward activity chart
        └── event-streams         event-stream-view-v10.0     the live feed of reward events

Support campaign
└── one template per product      example-reward-supplier-v10.0
    └── a reward supplier attached to the template

Resources attached by component_ids
├── one REWARD webhook per product, plus the status webhook   → the integration component
├── a report runner                                           → the report-runner view
└── an event stream                                           → the event-stream view
```

**Four views, not two.** A build that stops at the configuration and supplier views has left out the two surfaces a marketer opens to see whether fulfillment is working, and they are the ones that look most obviously broken when missing: the activity tab reports that no report runner is configured, and there is no reward feed at all. The report runner and the event stream are each created after their view exists and after the campaign is republished, so they are the last things built and the easiest to drop.

Install the maintained source when the duplicatable listing has one: the install carries the whole shape, including the support campaign it subscribes to, and the sequence below then serves as the checklist for confirming the install matches the partner page.

Confirm the source's type before installing it. A partner that once shipped a legacy integration still exposes that older source under the same partner name, and a name match alone will install the wrong generation. A source typed `integration-v1` or any other pre-v10 type is not the maintained v10 integration; when it is the only source available, build the v10 shape below and say that the only source on offer was legacy.

**A missing library source is a normal starting condition for a client-local build, not a blocker.**
Most accounts can duplicate only the sources they are subscribed to, so a partner the documentation
describes may have no source here at all. That is what the sequence below is for: the API creates every
piece — the component type, the support campaign, the templates, the integration, and the webhooks.

The exception is a request to make the partner installable for every client. That needs a registered,
Extole-owned integration component, which a client-local build does not produce. Build and validate the
shape in the development account when asked — it will appear on that account's own Integrations page
once its non-root component carries the tags described in
[Create an Integration with the Management API](doc:management-api-integration) — then publish or request
publication of the reusable component before calling the partner an installable integration.

Build in this order, because each step's prerequisite is the step before it.

### Create the Supplier Component Type

The socket must accept this partner's suppliers and nothing else, so create a component type parented to the platform reward-supplier type:

```bash
curl --request POST "$EXTOLE_API_HOST/v1/component-types" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "example-reward-supplier-v10.0",
    "display_name": "Example Reward Supplier",
    "parent": "reward-supplier-v10.0",
    "schema": "{}"
  }'
```

`schema` is required even when the type adds no rules of its own, and it is a JSON string rather than an object. An empty schema keeps whatever the parent requires, which is the point of parenting.

Reusing the platform type instead lets any partner's supplier install into this integration, and reusing an unrelated type leaves the socket filter meaningless. The type has to exist before any template can carry it; a template created untyped satisfies no socket filter and no later attempt to type it in place reliably succeeds.

### Create the Support Campaign and Its Supplier Templates

Create a `CONFIGURATION` campaign with program type `campaign-component` to hold the templates:

```bash
curl --request POST "$EXTOLE_API_HOST/v2/campaigns" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "Example Support",
    "description": "Reward supplier templates installed into the Example integration.",
    "campaign_type": "CONFIGURATION",
    "program_type": "campaign-component"
  }'
```

Create one component per product variant the partner page names, typed with the supplier type, and give each the settings a client configures — value, the partner's program and account identifiers, payment terms — plus the value-mode toggle and its bounds:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$SUPPORT_CAMPAIGN_ID/version/$SUPPORT_CAMPAIGN_VERSION/components" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "example-virtual",
    "display_name": "Example Virtual Prepaid Card",
    "description": "Send virtual prepaid cards from the Example marketplace.",
    "types": ["example-reward-supplier-v10.0"],
    "component_ids": ["'"$SUPPORT_ROOT_COMPONENT_ID"'"],
    "tags": ["internal:example-virtual"],
    "variables": [
      { "name": "rewardSupplierId", "type": "REWARD_SUPPLIER_ID", "values": { "default": null }, "tags": ["importance:expert"] },
      { "name": "faceValue", "display_name": "Face Value", "type": "STRING", "values": { "default": "0" }, "tags": ["importance:basic"] },
      { "name": "clientProgramNumber", "display_name": "Client Program Number", "type": "STRING", "values": { "default": "" }, "tags": ["importance:basic"] },
      { "name": "paymentType", "display_name": "Payment Type", "type": "ENUM", "allowed_values": ["ACH_DEBIT", "DRAW_DOWN"], "values": { "default": "ACH_DEBIT" }, "tags": ["importance:basic"] },
      { "name": "enabled", "type": "BOOLEAN", "values": { "default": false }, "tags": ["importance:expert"] }
    ]
  }'
```

Two shapes in that body are worth reading closely, because getting either wrong produces an error that names the wrong culprit. A component's settings arrive under `variables` on a create — `settings` is the sub-path you add one setting to later, not a property of the create — and every value sits under `values.default`, never a bare `value`.

The `rewardSupplierId` setting is not optional decoration. The platform's own reward-supplier type declares a schema requiring a setting by that name, so a template created without it is rejected for schema validation with a message about an array item that satisfies no subschema and no mention of the field it wanted. Read a type with `GET /v1/component-types/$TYPE_NAME` when a typed create is refused that way: the schema names what it requires, and the requirement is inherited by every type you derive from it.

Name each template with the same token you will use in its tag, so that a template named `example-virtual` carries the tag `internal:example-virtual`. The Rewards page resolves a supplier back to the template a marketer configures by looking for a component tagged `internal:` plus that template's own name, so a template named for the product and tagged for the partner is a supplier the rewards UI cannot place, however correct the rest of it is.

Setting types come from the platform's fixed vocabulary, not from the mathematical nature of the value. There is no `DECIMAL` or `DOUBLE`, and a create request naming one is rejected as malformed JSON on the `variables` property. Supplier templates use these:

| Setting | Type |
| :------ | :--- |
| Reward value | `STRING` |
| Cash-back percentage, minimum, and maximum | `INTEGER` |
| Value-mode toggle and enabled flag | `BOOLEAN` |
| Partner program number, account identifier | `STRING` |
| Payment terms | `ENUM` with `allowed_values` — not `enum_values`, which is rejected |
| Supplier identifier | `REWARD_SUPPLIER_ID` |
| Logo | `IMAGE` |

Build exactly the variants the page names. Inventing a variant produces a supplier a client can configure and the partner cannot fulfill; omitting one silently removes a product from the integration.

Give every template its own `rewardSupplierLogo` setting, sourced the way [Give the Integration a Logo That Resolves](doc:integration-component-model) describes: copy the built URL from the registered supplier template when one exists, or upload the file when you have it. A template without one is a product that appears as a blank tile next to products that show their artwork.

Then attach a reward supplier to each template. A bundled component declares this as an `elements.reward_suppliers` block in its `component.json`, but that block is a build-layer construct: `elements` is not a property of the component create request, and sending it is rejected as an unrecognized property. Through the API a reward supplier is a component-scoped resource of its own, created the same way a webhook is — with `component_ids` naming the template it belongs to:

```bash
curl --request POST "$EXTOLE_API_HOST/v2/reward-suppliers/custom-rewards" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "javascript@buildtime:context.getVariableContext().get(\"component.displayName\")",
    "type": "LOYALTY_POINTS",
    "display_type": "Example Virtual Cards",
    "enabled": "javascript@buildtime:context.getVariableContext().get(\"enabled\")",
    "tags": ["internal:example-variant"],
    "face_value_type": "USD",
    "face_value_algorithm_type": "javascript@buildtime:(context.getVariableContext().get(\"dynamicValue\") ? \"CASH_BACK\" : \"FIXED\")",
    "face_value": "javascript@buildtime:context.getVariableContext().get(\"faceValue\")",
    "cash_back_percentage": "javascript@buildtime:context.getVariableContext().get(\"cashBackPercentage\") / 100",
    "cash_back_min": "javascript@buildtime:context.getVariableContext().get(\"cashBackMin\")",
    "cash_back_max": "javascript@buildtime:context.getVariableContext().get(\"cashBackMax\")",
    "data": {
      "clientProgramNumber": "javascript@buildtime:context.getVariableContext().get(\"clientProgramNumber\")",
      "financialAccountId": "javascript@buildtime:context.getVariableContext().get(\"financialAccountId\")"
    },
    "component_ids": ["'"$TEMPLATE_COMPONENT_ID"'"]
  }'
```

A supplier's `component_ids` reference resolves only after the campaign has been published at least once, exactly as a webhook's does; until then the create fails with `invalid_component_reference`. Order the work around that rather than against it: create all the templates, publish the support campaign once, then create every supplier. Publishing between each template turns one publish into several and burns the version each time.

The endpoint is the one for the supplier kind you are creating — a partner that fulfills its own products uses the custom-reward endpoint — and `type` there is the custom reward kind, which is separate from the component type the template carries.

Four parts of that supplier carry weight beyond their own value:

- The **tag** identifies the product variant. It is how the order webhook finds the suppliers it serves and how the template resolves its own supplier identifier, so a template whose tag differs from the one its webhook filters on is a supplier no webhook will ever fulfill.
- The **display type** names the product as a marketer sees it — "Example Virtual Cards" rather than the generic kind. Omit it and the supplier falls back to the generic custom-reward type, which is the one condition that decides whether the partner's products appear as their own choices when a marketer creates a reward. Every variant that shares a product gets the same display type; variants that are different products get different ones.
- The **data map** carries the identifiers the order request needs. A request handler cannot read a setting on a component it does not own, so anything the partner endpoint requires per supplier belongs here.
- The **face-value algorithm** is resolved from the client's toggle rather than fixed in the template, with the percentage stored as a fraction and bounded by the minimum and maximum.

Give each template a `REWARD_SUPPLIER_ID` setting resolving its own element by that tag, so rules and reports can reference the supplier:

```javascript
javascript@buildtime: (function() { let filteredElements = Java.from(context.getComponent().createElementsQuery().withType('REWARD_SUPPLIER').withTag('internal:example-variant').list()); return filteredElements && filteredElements.length > 0 ? filteredElements[0].getId() : null; })();
```

Those two conventions are also what puts the partner's products in front of a marketer. When an account builds its own supplier templates rather than installing them from a library, the Rewards page reaches them by display type: it lists the display types the account's suppliers use, and for each one follows the supplier back to its component and then to the component tagged `internal:` plus that component's name. Templates built without a display type, or named differently from their tag, exist and work when a program references them directly, yet never appear among the choices offered when someone creates a reward.

Confirm both before moving on. `GET /v6/reward-suppliers/display-types` should list one entry per product the partner sells alongside the generic custom-reward type, and each built supplier from `GET /v6/reward-suppliers` should name a component whose own name matches its `internal:` tag. Renaming a template afterwards is a normal correction, but it changes the published campaign, so publish again once the names line up.

Default each template's `enabled` setting to `false`. A template describes a product the partner can fulfill, not a reward the account has decided to give, and the rewards list shows enabled suppliers only — so a template that ships enabled appears among the account's live rewards as though someone had created it, while the create-a-reward flow, which asks for disabled ones too, shows it either way. Enabling it is the marketer's act after installing it and filling in the program and account numbers. Check it with `GET /v6/reward-suppliers/built`: the partner's products should be absent by default and present under `include_disabled=true`.

### Create the Integration and Its Sockets

Create the `INTEGRATION` campaign, root, and model component as described in [Create the Integration Campaign](doc:integration-component-model) and [Create the Component Model](doc:integration-component-model), with the partner's account identifier and a `CLIENT_KEY` credential setting. Then add the supplier socket, filtered to the type created above:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components/$INTEGRATION_COMPONENT_ID/settings" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "rewardSuppliers",
    "display_name": "Reward Suppliers",
    "description": "Example reward suppliers for this integration.",
    "type": "MULTI_SOCKET",
    "filters": [
      {
        "type": "COMPONENT_TYPE",
        "component_type": "example-reward-supplier-v10.0"
      }
    ]
  }'
```

Add a `views` socket whose filters accept every view type the integration uses — the configuration type plus the report-runner and event-stream types — rather than only the configuration type.

Then subscribe the integration to the support campaign, so its templates are installable into the supplier socket. That subscription is its own resource too, naming the client that owns the templates, the path to the subscribed component, and the integration component that subscribes:

```bash
curl --request POST "$EXTOLE_API_HOST/v1/component-subscriptions" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "client_id": "'"$CLIENT_ID"'",
    "component_path": "Example Support:/",
    "component_ids": ["'"$INTEGRATION_COMPONENT_ID"'"]
  }'
```

Without it the supplier socket accepts the right type and has nothing to offer, which reads in the admin as an integration whose products were never built.

`CLIENT_ID` is this account's own client identifier, and `GET /v2/me` returns it for the token you are holding. Read it rather than reusing one from an example: subscribing on behalf of a client you are not authenticated as is refused with `access_denied`, which looks like a permissions problem with the endpoint and is really a wrong account in the body. The integration campaign also has to have been published at least once before it can subscribe, exactly as its webhooks and suppliers do — an unpublished integration component fails the subscription with `invalid_component_reference` naming the component you just created.

The report-runner and event-stream views are each empty until their element exists, and those elements follow the same rule as the supplier: what a bundle declares inline under `elements`, the API creates as its own resource attached with `component_ids`.

| Element a bundle declares | API resource |
| :------------------------ | :----------- |
| `reward_suppliers` | `POST /v2/reward-suppliers/custom-rewards` |
| `webhooks` | `POST /v6/webhooks`, with filters added per type afterwards |
| `report_runners` | `POST /v7/report-runners` |
| `event_streams` | `POST /v6/event-streams`, with filters added afterwards |

Attach each of those two to the **view** component that displays it, not to the integration component. Both views resolve what to show by querying their own component for an element of the matching kind, so a report runner hung off the integration leaves the tab reporting that no report runner is configured even though one exists in the account.

#### Build the Report Behind the Activity Tab

A report runner is a scheduled report, a set of parameter values for it, and an attachment to the view that charts it:

```bash
curl --request POST "$EXTOLE_API_HOST/v7/report-runners" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "type": "SCHEDULED",
    "name": "Partner Example Reward Revenue Report",
    "report_type": "'"$REPORT_TYPE_ID"'",
    "formats": ["CSV", "JSON"],
    "scopes": ["CLIENT_SUPERUSER"],
    "tags": ["partner-graph"],
    "frequency": "WEEKLY",
    "schedule_start_date": "2026-04-01T00:00:00-06:00",
    "enabled": true,
    "execution_policy": "AWAIT_DATA",
    "parameters": {
      "container": "production",
      "time_range": "ALL_TIME",
      "campaign_states": "ALL",
      "visit_type": "NEW_TO_CLIENT",
      "unattributed_events": "false",
      "quality": "ALL",
      "mappings": "date=START_DATE(event.eventTime, period:\"DAY\"); count=group_count(event.id, step_name:\"converted\"); revenue=GROUP_SUM(event.data.amount, step_name:\"converted\")"
    },
    "component_ids": ["'"$VIEW_COMPONENT_ID"'"]
  }'
```

A scheduled runner needs `schedule_start_date`, and a runner's type is fixed once created: a runner made as `REFRESHING` cannot be turned into a scheduled one, and an update that tries reports the wrong type rather than the wrong field. Delete it and create the runner you meant.

`report_type` is an account-scoped identifier rather than a readable constant, so read the account's types with `GET /v6/report-types` and match on display name. Two properties decide whether a type will work, and neither is its name:

- The **parameters it declares** are the only ones the runner may send, and their values come from the type's own enumerations. A time range is `ALL_TIME`, not `all_time`; a locale list accepts only locales the account declares; a required parameter left out and an invented parameter both come back as the same invalid-format rejection on `parameters` as a whole, so add parameters one at a time when one is refused rather than rewriting the set.
- The **mappings dialect** it accepts decides what your expression may say. A type whose `mappings` parameter is row-shaped rejects the grouping functions — `group_count`, `GROUP_SUM` — that a charted activity report is built from; a metric-shaped one accepts them. Read the parameter's type before writing the expression, and choose the parent by that rather than by a display name that sounds close.

Accounts differ here, and an account that lacks a suitable type is a normal case rather than a dead end. Create one: a configured report type is a saved set of parameter defaults over a parent type.

```bash
curl --request POST "$EXTOLE_API_HOST/v6/report-types" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "display_name": "Example Reward Revenue",
    "description": "Reward activity and revenue for the Example integration.",
    "type": "CONFIGURED",
    "parent_report_type_id": "'"$PARENT_REPORT_TYPE_ID"'",
    "categories": ["Customer Activity"],
    "scopes": ["CLIENT_SUPERUSER"],
    "allowed_scopes": ["CLIENT_ADMIN", "CLIENT_SUPERUSER"],
    "visibility": "PUBLIC",
    "formats": ["CSV", "JSON"],
    "parameters": [
      { "name": "mappings", "default_value": "date=START_DATE(event.eventTime, period:\"DAY\"); count=group_count(event.id, step_name:\"converted\")" },
      { "name": "container", "default_value": "production" }
    ]
  }'
```

The `parameters` list must name **every** parameter the parent declares, giving an empty default to the ones you do not set. Listing only the ones you care about reads as deleting the rest and is rejected as an attempt to remove static parameters, which is the one error here that sounds unrelated to what you sent.

Republish the campaign after creating the views and before creating their elements. The `component_ids` reference resolves against the published campaign, so a resource created against a view component added since the last publish is rejected with `invalid_component_reference` — the same rule that governs webhooks and suppliers, and the easiest one to trip over here because the view was created minutes earlier in the same session.

An event stream's filters are created under the stream and carry a `type` discriminator in the body rather than a path segment, which is the opposite of how reward webhook filters work:

```bash
curl --request POST "$EXTOLE_API_HOST/v6/event-streams/$EVENT_STREAM_ID/filters" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"type": "EVENT_TYPE", "event_types": ["REWARD", "SEND_REWARD"]}'

curl --request POST "$EXTOLE_API_HOST/v6/event-streams/$EVENT_STREAM_ID/filters" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"type": "APPLICATION_TYPE", "app_types": ["example"]}'
```

Without those filters the tab shows every event in the account rather than the integration's reward activity, which looks like a working feed and is not one.

A view points at its element through a setting typed `STRING` — `reportRunnerId` on the report view, `eventStreamId` on the event-stream view. There is no `REPORT_RUNNER_ID` or `EVENT_STREAM_ID` setting type, and naming one is rejected as malformed JSON with the invented type echoed back as the invalid value. The setting holds no literal identifier either: its default is a buildtime query that asks the view's own component for the element it owns, so the view keeps working when the element is recreated.

```json
{
  "name": "reportRunnerId",
  "display_name": "Report Runner ID",
  "type": "STRING",
  "values": {
    "default": "javascript@buildtime:(function(){ let elements = Java.from(context.getComponent().createElementsQuery().withType('REPORT_RUNNER').list()); return elements && elements.length > 0 ? elements[0].getId() : null; })()"
  },
  "tags": ["importance:expert"]
}
```

The event-stream view uses the same expression with `withType('EVENT_STREAM')`. This is also why the element belongs on the view: the query only ever looks at the component the setting lives on.

Give the report-runner view a `reportColumnsMapping` setting as well, typed `JSON`. Its default is the mapping serialized as a string and escaped; a nested object is refused as `variable_value_invalid_type`, which reports the value as invalid for the type it plainly is. It maps the report's columns onto a chart, and every column it names has to be one the runner's `mappings` expression produces — the axis column and each series column by exactly the name the expression assigns:

```json
{
  "chart": { "type": "line" },
  "xAxis": { "column": "date", "type": "datetime" },
  "series": [
    { "name": "Count", "column": "count", "aggregation": "sum" },
    { "name": "Total Spend", "column": "revenue", "aggregation": "sum" }
  ]
}
```

Without the setting the tab has a report behind it and nothing to draw; with a column the report does not produce, it draws an empty axis. Write the mappings expression and this setting together.

Name the event stream for the component that owns it and tag it with the partner's app type, which is how the feed is recognised as this integration's rather than a stream someone left in the account:

```json
{
  "name": "javascript@buildtime:context.getComponent().getName() + ' Reward Events'",
  "description": "A live feed of reward events produced by the Example integration. The feed runs for 1 hour by default. Refresh the feed to poll for new events.",
  "tags": ["internal:app_type=example"],
  "component_ids": ["$VIEW_COMPONENT_ID"]
}
```

A reward integration ships four views: a configuration view for the credential and account settings, a configuration view whose `settingsToDisplay` names the supplier socket and whose status reports in progress while no supplier is installed, a report-runner view charting reward activity, and an event-stream view filtered to the reward event types and the partner's app type.

The supplier view's status is the one expression worth copying rather than composing. It reports in progress until a supplier exists anywhere under the integration, and it reaches for the suppliers themselves instead of counting children, which is a proxy that goes wrong as soon as the tree gains a view:

```javascript
javascript@buildtime:(function () {
  let children = Java.from(context.getComponent().getParent().getChildren());
  let rewardSupplierIds = [];
  children.forEach(function (child) {
    Java.from(child.createElementsQuery().withType("REWARD_SUPPLIER").list())
      .forEach(function (rewardSupplier) { rewardSupplierIds.push(rewardSupplier.getId()); });
  });
  return rewardSupplierIds.length > 0 ? '' : 'IN_PROGRESS';
}());
```

Wrap every Java collection in `Java.from` before iterating it, as both loops above do. An expression that walks one directly builds into nothing, and because settings are evaluated as part of the create, the whole component is refused with `campaign_build_failed` naming the variable rather than the mistake.

Order is a setting, not the order you happened to create them in. Give every view an `order` setting typed `INTEGER`, lowest first, with configuration at the front. Views without it arrange themselves arbitrarily, so a marketer can meet the reward activity chart before the tab that asks for credentials.

Every one of them is a view, and the platform's view type requires three settings by name: `title`, `status`, and `settingsToDisplay` — the last typed `STRING_LIST`, not `JSON`. A view created without all three, or with `settingsToDisplay` typed as JSON, is rejected for type validation against three subschemas none of which the error names. Build each view from the body in [Add a Configuration View](doc:integration-component-model), which carries all three, and attach it with `installed_into_socket` — `socket_name` is not a property of a component create.

### Create the Reward Webhooks

Create one webhook per partner order endpoint plus one status check, all typed `REWARD` and attached to the integration component through `component_ids`. As with any component-scoped webhook, the campaign must have been published once before these can be created.

Create the webhook first, without filters. `POST /v6/webhooks` has no filters property — a bundled component declares `webhook_filters` inline, but that is build-layer syntax and the API rejects it:

```json
{
  "type": "REWARD",
  "default_method": "POST",
  "url": "https://api.example.com/rewards/v1/submitOrder",
  "client_key_id": "javascript@buildtime:context.getVariableContext().get(\"clientKeyId\")",
  "tags": ["internal:example-variant", "internal:app_type=example", "internal:app_data:event_type=reward"],
  "retry_intervals": [1800, 3600, 10800],
  "component_ids": ["INTEGRATION_COMPONENT_ID"]
}
```

Then add each filter through its own typed endpoint under the created webhook. The supplier filter takes a buildtime expression resolving the suppliers under the integration's children that carry the variant tag; the state filter takes the reward states the webhook acts on:

`POST /v4/webhooks/reward/{webhook_id}/filters/supplier`:

```json
{
  "reward_supplier_ids": "javascript@buildtime:(function(){ let children = Java.from(context.getComponent().getChildren()); let allRewardSuppliers = []; children.forEach(function(child) { let rewardSuppliers = Java.from(child.createElementsQuery().withType('REWARD_SUPPLIER').withTag('internal:example-variant').list()); rewardSuppliers.forEach(function(rewardSupplier) { allRewardSuppliers.push(rewardSupplier.getId()); }); }); return allRewardSuppliers; })()"
}
```

`POST /v4/webhooks/reward/{webhook_id}/filters/state`:

```json
{
  "states": ["EARNED"]
}
```

The four filter kinds each have their own path segment — `supplier`, `state`, `tags`, and `expression` — and `GET /v4/webhooks/reward/{webhook_id}/filters` lists what a webhook currently has.

Reward states are a closed vocabulary and the two a reward integration needs are `EARNED` for the order webhooks and `FULFILL_FAILED` for the status check. A state the platform does not define comes back as malformed JSON rather than as an unknown value, and `FAILED` exists — so a near miss is accepted and quietly changes which rewards the webhook fires on.

Omitting either filter is the failure worth guarding against. Without the supplier filter the webhook attempts to fulfill every reward in the account through one partner endpoint; without the state filter it re-orders rewards that are already fulfilled.

The request handler builds the partner order from the reward, the supplier's data map, and the person's profile. Its field-level body comes from the partner's own developer documentation, which this documentation set links to rather than reproduces. Not having that body in hand does not stop the build: the webhook, its filters, its client key, and its retry schedule are the shape, and a handler that assembles the documented fields is a starting point to be reviewed against the partner's API. Create the webhooks with the best handler the available documentation supports and report the handler bodies as requiring partner-side verification. Leaving the webhooks uncreated because the exact payload was not on hand produces an integration with suppliers that can never be fulfilled, which is a worse answer than a handler that needs review. The response handler reads the partner's result and does one of three things: mark the reward fulfilled with the partner's identifier and any delivered value, leave it for the next retry when the partner reports the order as still processing, or fail it when the partner rejects it. A handler that always fulfills hides partner rejections behind rewards that were never delivered.

The status-check webhook covers products that do not complete synchronously. It filters on every variant's suppliers and on the fulfillment-failed state, and its retry schedule escalates from hours to days out to about a month, because a physical fulfillment can take weeks. Order webhooks keep the short schedule above; a status check on that schedule exhausts its retries long before the partner finishes.

### Attach the Credential and Verify

Create the client key only once the partner's secret exists — for a partner that authenticates with certificates, that means the certificate material, not a placeholder — then set the credential setting on the integration component. Leave the setting null and report it outstanding when the secret has not arrived; the rest of the shape does not depend on it.

Before calling the build done, read back and confirm:

- The supplier type exists with the platform reward-supplier type as its parent.
- The support campaign holds one correctly typed template per product the partner page names, each with a reward supplier attached to it, a variant tag, and its data map.
- The supplier socket filters to the partner's type, and the views socket accepts every view type in use.
- Each webhook is type `REWARD`, carries both filters, resolves a non-empty supplier list, and uses the retry schedule its purpose requires.
- The report-runner and event-stream views each resolve to an actual element on that view. Read the built campaign and confirm the identifiers are non-null: an empty tab is the symptom of an element that was never created or was attached to the wrong component, and neither shows up as a failed call.
- The account identifier is set and the credential is either configured or reported outstanding.
