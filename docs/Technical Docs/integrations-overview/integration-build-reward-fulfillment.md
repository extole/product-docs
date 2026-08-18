---
title: "Build a Reward Fulfillment Integration"
excerpt: "Create the supplier type, support campaign, supplier templates, and reward webhooks for a partner that fulfills rewards, and give its activity and event views their reward-specific values.\n"
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
├── one REWARD webhook per order endpoint, plus the status check → the integration component
├── a report runner                                           → the report-runner view
└── an event stream                                           → the event-stream view
```

**Four views, not two.** A build that stops at the configuration and supplier views has left out the two surfaces a marketer opens to see whether fulfillment is working, and they are the ones that look most obviously broken when missing: the activity tab reports that no report runner is configured, and there is no reward feed at all. The report runner and the event stream are each created after their view exists and after the campaign is republished, so they are the last things built and the easiest to drop.

**The component names above are literal.** Only `example` stands in for the partner. Name the four views `configuration`, `reward-suppliers`, `report-runner-view`, and `event-streams`, and the integration campaign and its support campaign after the partner and the generation they implement, as in `Example V10` and `Example V10 Support`. Descriptive substitutes such as `reward-activity` for `report-runner-view`, or `Example Reward Supplier Templates` for the support campaign, build a working integration that no longer diffs against the packaged one, which is how a client-local build is checked when a marketer reports that a tab looks wrong. The user-facing tab labels come from each view's `title`, so renaming the component changes nothing a marketer sees and everything about whether the build can be compared.

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

The dependencies here are real, but they are not one straight chain, and reading them as one puts the thing that was asked for last. Only three orderings are forced: the component type must exist before any template can carry it and before the supplier socket can filter on it; the support campaign and its templates must exist before the integration can subscribe to them; and the integration campaign must have been published once before it can subscribe or attach resources.

Create the integration campaign and its component as soon as the component type exists — before the support campaign, not after it. It depends on neither the support campaign nor the templates, and it is the deliverable. A build interrupted partway through the scaffolding otherwise leaves the account holding a support campaign, a set of templates, and no integration, which is indistinguishable from nothing having been built. The sections below are written in the order you configure them and assume the integration campaign already exists.

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

This is scaffolding for the integration, so [the integration campaign](#create-the-integration-and-its-sockets) should already exist before you start it. The templates here are what that integration subscribes to.

Create a `CONFIGURATION` campaign with program type `campaign-component` to hold the templates, named for the integration it supports so the pair reads as one unit in the campaign list:

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
      { "name": "dynamicValue", "display_name": "Percentage Of Purchase", "type": "BOOLEAN", "values": { "default": false }, "tags": ["importance:basic"] },
      { "name": "cashBackPercentage", "display_name": "Cash Back Percentage", "type": "INTEGER", "values": { "default": 0 }, "tags": ["importance:basic"] },
      { "name": "cashBackMin", "display_name": "Minimum Reward Value", "type": "INTEGER", "values": { "default": 0 }, "tags": ["importance:basic"] },
      { "name": "cashBackMax", "display_name": "Maximum Reward Value", "type": "INTEGER", "values": { "default": 0 }, "tags": ["importance:basic"] },
      { "name": "clientProgramNumber", "display_name": "Client Program Number", "type": "STRING", "values": { "default": "" }, "tags": ["importance:basic"] },
      { "name": "financialAccountId", "display_name": "Financial Account ID", "type": "STRING", "values": { "default": "" }, "tags": ["importance:basic"] },
      { "name": "paymentType", "display_name": "Payment Type", "type": "ENUM", "allowed_values": ["ACH_DEBIT", "DRAW_DOWN"], "values": { "default": "ACH_DEBIT" }, "tags": ["importance:basic"] },
      { "name": "rewardSupplierLogo", "type": "IMAGE", "values": { "default": null }, "tags": ["importance:expert"] },
      { "name": "enabled", "type": "BOOLEAN", "values": { "default": false }, "tags": ["importance:expert"] }
    ]
  }'
```

Two shapes in that body are worth reading closely, because getting either wrong produces an error that names the wrong culprit. A component's settings arrive under `variables` on a create — `settings` is the sub-path you add one setting to later, not a property of the create — and every value sits under `values.default`, never a bare `value`.

Declare every setting the supplier's expressions will read. The supplier created below resolves `dynamicValue`, `cashBackPercentage`, `cashBackMin`, `cashBackMax`, and `financialAccountId` from this template, and a buildtime expression reading a setting the component does not declare returns null rather than failing: the face-value algorithm falls back to the wrong branch and the partner's account identifier leaves the order request empty. Add the setting or drop the expression — do not leave one referring to the other.

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

The publish is one call, and it takes the version you are publishing:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$SUPPORT_CAMPAIGN_ID/version/$SUPPORT_CAMPAIGN_VERSION/publish" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN"
```

Read `$SUPPORT_CAMPAIGN_VERSION` from the support campaign immediately before publishing rather than counting your own writes: every component and settings call increments it, so a version computed from memory is usually one behind. That operation is **not carried in the OpenAPI specification**, so a reference lookup for it returns nothing found — which is a gap in the specification and not evidence that publishing is unavailable. This page and [Validate and Publish an Integration](doc:integration-validation) are its documentation; take the call from here rather than searching for a published operation that does not exist, and note that `POST /v2/campaigns/{campaignId}/publish` is the specification's variant of the same action.

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

Create the `INTEGRATION` campaign, root, and model component as described in [Create the Integration Campaign](doc:integration-component-model) and [Create the Component Model](doc:integration-component-model). Declare the credential settings under the names the partner page uses — for BHN that is `merchantId` (`STRING`) and `clientKeyId` (`CLIENT_KEY`). A prefixed invention such as `bhnMerchantId` is a different setting, and webhook `client_key_id` expressions plus request handlers that call `context.getVariable("merchantId")` will read null. Then add the supplier socket, filtered to the type created above:

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

The last two rows are the same build every integration does, whatever the partner sells, so they have their own page rather than a reward-flavored copy here.

#### Give the Reward Activity Tab Its Report and Feed

A reward integration ships four views: a configuration view for the credential and account settings, a configuration view whose `settingsToDisplay` names the supplier socket and whose status reports in progress while no supplier is installed, a report-runner view charting reward activity, and an event-stream view filtered to the reward event types and the partner's app type.

Build the last two from [Add the Activity and Event Views](doc:integration-activity-views), which carries the view bodies, the settings the view type requires, the ordering, the republish that has to precede an element attaching, and the report-type lookup. Three values on those views are reward-specific.

The runner's `mappings` expression counts reward activity and the revenue behind it:

```text
date=START_DATE(event.eventTime, period:"DAY"); count=group_count(event.id, step_name:"converted"); revenue=GROUP_SUM(event.data.amount, step_name:"converted")
```

The view's `reportColumnsMapping` names the columns that expression produces. It describes this chart:

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

The setting holds that object serialized as an escaped JSON string, which is the form to put in `values.default`. Sending the object itself is rejected as `variable_value_invalid_type`:

```text
"{\"chart\":{\"type\":\"line\"},\"xAxis\":{\"column\":\"date\",\"type\":\"datetime\"},\"series\":[{\"name\":\"Count\",\"column\":\"count\",\"aggregation\":\"sum\"},{\"name\":\"Total Spend\",\"column\":\"revenue\",\"aggregation\":\"sum\"}]}"
```

The event stream carries an event-type filter as well as the application-type filter every stream gets, so the feed shows fulfillment activity rather than every event in the account. `$EVENT_STREAM_ID` is what the stream create returned:

```bash
curl --request POST "$EXTOLE_API_HOST/v6/event-streams/$EVENT_STREAM_ID/filters" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"type": "EVENT_TYPE", "event_types": ["REWARD", "SEND_REWARD"]}'
```

Where the partner page publishes a report runner contract, that contract is literal. Copy its name, schedule, formats, tags, scopes, execution policy, and every parameter and mapping expression, looking up only the account-local report type and component identifiers. A runner with a plausible count or revenue mapping is not equivalent to the partner's report.

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

Wrap every Java collection in `Java.from` before iterating it, as both loops in that expression do. An expression that walks one directly builds into nothing, and because settings are evaluated as part of the create, the whole component is refused with `campaign_build_failed` naming the variable rather than the mistake.

### Create the Reward Webhooks

Create one webhook per partner order endpoint plus one status check, all typed `REWARD` and attached to the integration component through `component_ids`. As with any component-scoped webhook, the campaign must have been published once before these can be created.

Create the webhook first, without filters. `POST /v6/webhooks` has no filters property — a bundled component declares `webhook_filters` inline, but that is build-layer syntax and the API rejects it. `name` is required and is not defaulted from the URL or the type; a body without it is rejected with `webhook_missing_name`:

```json
{
  "name": "Example Virtual Prepaid Card Order",
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

The request handler builds the partner order from the reward, the supplier's data map, and the person's profile. When the partner page publishes that body — BHN does — write it onto the webhook as `request` and write the matching `response_handler`. Those are properties of `POST /v6/webhooks` and of a later `PUT /v6/webhooks/{id}`. A webhook whose `request` is still `javascript@runtime:context.createRequestBuilderWithDefaults().build()` and whose `response_handler` is null has no fulfillment path.

The runtime those handlers run in is:

| Need | Call |
| :-- | :-- |
| The reward being fulfilled | `context.getReward()` |
| A setting on the integration | `context.getVariable("merchantId")` |
| An empty request | `context.createRequestBuilder()` |
| Headers and JSON | `.addHeader(...)`, `.withBody(JSON.stringify(body))`, `.build()` |
| Mark processing, not delivered | `context.createFulfillRewardCommandEventBuilder().withSuccess(false).send()` |
| Mark delivered | `.withSuccess(true).withPartnerRewardId(partnerId).send()` |
| Mark failed | `context.createFailedRewardCommandEventBuilder().withMessage(...).send()` |
| Ask the dispatcher to try again | return `"RETRY"` |
| Finish this attempt | return `"OK"` |

Order webhooks commonly fulfill with `withSuccess(false)` so the status-check webhook can close the reward later. A handler that always fulfills with `withSuccess(true)` hides partner rejections behind rewards that were never delivered.

Leave the webhook **disabled** only while a required credential or the partner page's payload contract is still missing. Once both are present, `PUT` the handlers and set `enabled` to true. Do not report that the runtime methods above are unpublished, and do not wait for a packaged script from engineering when the partner page already names the body.

The status-check webhook covers products that do not complete synchronously. It filters on every variant's suppliers and on the fulfillment-failed state, and its retry schedule escalates from hours to days out to about a month, because a physical fulfillment can take weeks. Order webhooks keep the short schedule above; a status check on that schedule exhausts its retries long before the partner finishes.

### Attach the Credential and Verify

Create the client key only once the partner's secret exists — for a partner that authenticates with certificates, that means the certificate material, not a placeholder — then set the credential setting on the integration component. Leave the setting null and report it outstanding when the secret has not arrived; the rest of the shape does not depend on it.

Before calling the build done, read back and confirm:

- The supplier type exists with the platform reward-supplier type as its parent.
- The support campaign holds one correctly typed template per product the partner page names, each with a reward supplier attached to it, a variant tag, and its data map.
- The supplier socket filters to the partner's type, and the views socket accepts every view type in use.
- Each webhook is type `REWARD`, carries both filters, resolves a non-empty supplier list, and uses the retry schedule its purpose requires.
- Each webhook's `request` and `response_handler` match the partner page, and `enabled` is true once the credential setting is populated. An empty default request builder is not the partner page's handler.
- The webhook count matches the partner's order endpoints plus one status check — not the number of products. Several products ordered through one endpoint share one webhook, and its supplier filter resolves every variant that endpoint serves.
- The report-runner and event-stream views each resolve to an actual element on that view. Read the built campaign and confirm `reportRunnerId` and `eventStreamId` are non-null: an empty tab is the symptom of an element that was never created or was attached to the wrong component, and neither shows up as a failed call. A view whose `reportColumnsMapping` is set but whose `reportRunnerId` is null is the common half-built case — the chart is described and has nothing to chart.
- The integration component's `logo` resolves to the partner's actual artwork — the registered component's URL, a file the partner supplied, or the logo published on the partner's own site — and you fetched that URL and saw an image come back. A favicon, a product screenshot from Extole's documentation, or any address that answers with an error page satisfies the setting's type and renders a broken tile, so it is a build left unfinished rather than a build with artwork.
- The account identifier is set and the credential is either configured or reported outstanding.
