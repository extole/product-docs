---
title: "Create an Integration With the Client API"
excerpt: "Create, configure, publish, verify, and maintain a reusable Extole integration through the Client API without uploading a component bundle.\n"
---

# Overview

Use the Client API to create an integration campaign and its component hierarchy directly in Extole. This workflow is intended for Extole Chat, installers, and operational services that must build an integration without adding a bundle to the creative repository.

An API-created integration is still a component-based integration. It must use the same reusable component types, typed sockets, business-event templates, views, naming conventions, and validation rules as a bundled v10 integration.

Examples in this guide use a generic partner named `example`. Substitute the real partner name, event names, and field names from that partner's own documentation.

Where a partner-specific page exists in this documentation set, read it first: it carries the wire contract for that platform — event names, payload fields, and status mapping — while this guide carries the build sequence that applies to every platform. Partner pages are published under the partner's name as the page slug, so retrieve the page directly by that slug rather than relying on a keyword search to surface it.

## Choose the Integration Category First

Place the platform in a category before creating anything. [Integration Categories](doc:integration-categories) describes what each category contains and how to recognize it; this guide carries the API sequence that builds it. Pick the path from discovery, not from habit.

| Category | When it applies | Build path |
| :------- | :-------------- | :--------- |
| Outbound library install | The duplicatable listing already has an integration component whose name matches the partner. | Duplicate that library component with no target campaign, reshape it to the finished shape on the partner page, then attach webhooks and credentials. Follow **Build an Outbound Library Integration** below. |
| Reward fulfillment | The partner supplies gift cards, prepaid cards, points, or payouts that Extole orders when a reward is earned. | Install the maintained source when one exists; otherwise build the supplier type, the support campaign of supplier templates, and the integration with its `REWARD` webhooks. Follow **Build a Reward Fulfillment Integration** below. |
| Inbound custom build | No maintained source exists for the partner, or the request is an inbound platform that maps wire events onto canonical business events. | Create an `INTEGRATION` campaign from the custom integration template, then add business events, trigger rules, data capture, and views. Follow the rest of this guide. |

Before creating anything, query the duplicatable listing for integration components and look for one whose name matches the partner. Match on the component name, not on a fixed type version: the integration type is revised over time, so a source may be typed `integration-v10.0`, `integration-v10.1`, or a later revision, and a query pinned to one revision reports a maintained partner as missing. Prefer that name match over building from `custom_integration`. Rebuilding a maintained partner from the custom template produces a campaign that looks related and does none of the partner's webhook or credential work.

A request that adds inbound scope to a maintained outbound partner uses both paths: install the library source first, then add business events to the installed campaign using the inbound sequence.

## Build an Outbound Library Integration

An outbound partner starts from its maintained library source. Installing is one call; the finished shape is what the partner page defines. Every step below runs against a partner-agnostic contract, so substitute the component name, endpoints, and tag namespace from the partner page.

### Confirm the Finished Shape

Read the partner page before the first mutation. It describes the finished integration in product terms, and each statement maps to something the install must contain:

| What the partner page states | What the finished install contains |
| :--------------------------- | :--------------------------------- |
| The activity the integration forwards | One child per listed activity, and no child forwarding activity the page does not list |
| The partner endpoints Extole calls | One webhook per endpoint, each tagged by purpose |
| That program campaigns attach partner data to their own events | A typed data-item child of the integration component |
| That the integration exposes its outbound connections as settings | One `WEBHOOK_ID` setting per webhook, resolved by tag |
| The account URL and credential the partner requires | The matching settings on the integration component |

Run that comparison against an integration that already exists in the account, not only against a fresh install. Reading a live integration back and reporting it as already in the requested state, without checking it line by line against the page's description, is what makes an unfinished install permanent — the integration exists, so nobody looks again.

Read that list as exhaustive rather than as a minimum. A library source ships the union of what every account might want, so it commonly installs children the page does not list and only one of the webhooks the page names. Deleting the extra children and creating the missing webhooks is the reshape; an install left in its raw shape forwards activity the partner page never claimed and omits endpoints it did.

### Create Missing Component Types

A partner page can require a component type the account has never used, and a typed child cannot be created before its type exists. Check the type, and create it when it is missing:

```bash
curl -s -H "Authorization: Bearer ${TOKEN}" \
  "${EXTOLE_API_HOST}/v1/component-types/${PARTNER_COMPONENT_NAME}-data"

curl -s -X POST -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"name":"'"${PARTNER_COMPONENT_NAME}"'-data","display_name":"Partner Data Item","schema":"{}"}' \
  "${EXTOLE_API_HOST}/v1/component-types"
```

Omit `parent`. Creating the child with an empty `types` array instead is not the finished shape: an untyped component satisfies no socket filter and no template lookup.

### Install the Library Source

A library install is the same action the Partners page Install button performs: `POST /v1/components/{SOURCE_COMPONENT_ID}/duplicate` without `target_campaign_id`. Omitting the target campaign creates a new root integration campaign that copies the library tree, including its webhooks and child controllers.

Send a body carrying at least one property — a request with no body is rejected as `missing_request_body`. Use `component_display_name` for a display override; `display_name` is not a property of this request and is rejected as an unrecognized property. Omit `target_campaign_id` rather than sending it as null, which is rejected as `invalid_null`: the attribute may be omitted but not nullified.

```bash
SOURCE_COMPONENT_ID=$(curl -s -H "Authorization: Bearer ${TOKEN}" \
  "${EXTOLE_API_HOST}/v1/components/duplicatable?having_any_types=integration-v10.0,integration-v10.1" \
  | jq -r --arg name "${PARTNER_COMPONENT_NAME}" '.[] | select(.name==$name) | .id' | head -n 1)

curl -s -X POST -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"component_display_name":"Partner"}' \
  "${EXTOLE_API_HOST}/v1/components/${SOURCE_COMPONENT_ID}/duplicate"
```

Prefer the maintained library source over an account's own installed copy, which the same query also returns. List every integration type revision the account has, and when a partner the partner page describes as maintained does not appear, re-run the query with no type filter before concluding that no source exists.

### Reshape the Install

The reshape uses these calls. Refresh the campaign version before each version-scoped call:

| Action | Call |
| :----- | :--- |
| Delete a library child | `DELETE /v2/campaigns/{campaign_id}/version/{version}/components/{component_id}` |
| Create a child | `POST /v2/campaigns/{campaign_id}/version/{version}/components` |
| Add or change a setting | `POST /v2/campaigns/{campaign_id}/version/{version}/components/{component_id}/settings` |
| Create a webhook | `POST /v6/webhooks` |
| Publish the campaign | `POST /v2/campaigns/{campaign_id}/version/{version}/publish` |

Bring the installed tree to the partner page's shape in one pass:

- Delete the library children the partner page does not keep. Refresh the campaign version between deletes.
- Create the children it adds, including any typed data template.
- Remove parent settings that belonged to a deleted child. A trigger-event-name setting left behind after its controller is gone describes behavior the integration no longer has.
- Set one `WEBHOOK_ID` setting per partner endpoint, resolved by webhook tag rather than by identifier, so the setting survives a rebuild:

```javascript
javascript@buildtime: (function() { var filteredElements = Java.from(context.getComponent().createElementsQuery().withType('WEBHOOK').withTag('internal:partner:event').list()); return filteredElements && filteredElements.length > 0 ? filteredElements[0].getId() : null; })();
```

A partner data template is a typed child of the integration component, created through `component_ids` with no socket. Its install expression is what lets a marketing campaign attach partner actions from the template, by anchoring the source component's unanchored step data onto the target event:

```javascript
javascript@installtime:const sourceData = Java.from(context.getSourceComponent().getUnanchoredStepData());
let targetSteps = Java.from(context.getTargetComponent().getSteps());
const stepName = context.getVariableContext().get("step");

if (stepName !== undefined && stepName !== null) {
    targetSteps = targetSteps.filter(function (step) {
        return step.getName() === stepName;
    });
}


if (targetSteps.length) {
    for (var i = 0; i < sourceData.length; i++) {
        targetSteps[0].anchor(sourceData[i]);
    }

    return;
}
```

### Publish Before Attaching Component-Scoped Webhooks

A webhook whose name or URL expression calls `context.getComponent()` must be created with `component_ids` naming the integration component, and that reference resolves only after the campaign has been published at least once. Until then, `POST /v6/webhooks` returns `invalid_component_reference`, and creating the same webhook without `component_ids` fails because the expressions have no component to read.

Treat that publish as part of the create path rather than a separate decision raised on its own. Publish the campaign, create the webhook, and return the campaign to draft afterwards only when the requester asked for a draft. When your own rules require approval before anything goes live, ask for it once, in the same message as the plan, rather than stopping earlier and reporting the shape as unfinishable.

A published integration campaign has no supported route back to a draft — it has no stop or unpublish action. Do not archive the campaign to approximate one: archiving takes the integration out of use entirely, which is not what a draft request asked for. Say that the campaign is published, and that finishing the shape required it.

Publishing validates every webhook the campaign already owns, so a setting that feeds an existing webhook URL must resolve to something valid first. An account-URL setting left empty produces an invalid destination, campaign validation rejects the publish, and the second webhook can never be attached. Keep a valid placeholder host in that setting — the library's own default is one — until the real host arrives.

```bash
curl -s -X POST -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "javascript@buildtime:context.getComponent().getName() + '"'"'_message_trigger'"'"'",
    "url": "javascript@buildtime:context.getVariableContext().get(\"partnerRestUrl\") + \"/partner/endpoint/path\"",
    "type": "GENERIC",
    "default_method": "POST",
    "enabled": "javascript@buildtime:context.getVariableContext().get('"'"'enabled'"'"')",
    "client_key_id": "javascript@buildtime:context.getVariableContext().get(\"clientKeyId\")",
    "request": "javascript@runtime:context.createRequestBuilderWithDefaults().withUserAgent('"'"'partner-Extole-Integration/1.0'"'"').build();",
    "retry_intervals": [1, 30, 60],
    "tags": ["internal:partner:campaign", "internal:partner"],
    "component_ids": ["'"${INTEGRATION_COMPONENT_ID}"'"]
  }' \
  "${EXTOLE_API_HOST}/v6/webhooks"
```

Name each webhook for the endpoint it calls — an ingestion endpoint and a message-trigger endpoint are separate webhooks with separate tags. Tag every webhook by purpose, because the tags are what the `WEBHOOK_ID` settings resolve: an untagged webhook produces a setting that evaluates to null and an integration that silently sends nothing.

When the account URL setting may be stored without a scheme, build the URL expression to add `https://` rather than assuming the stored value carries it.

### Attach the Credential

Create a webhook client key only when the requester has supplied the partner's API secret, then set the credential setting on the integration component. Missing credentials do not block the reshape: finish the tree, webhooks, and settings, leave the credential setting null, and report which values remain outstanding.

The account URL is different from the secret. Blanking it to signal "not yet configured" breaks the publish that the rest of the reshape depends on, so leave a valid placeholder host in place and report it as a value the requester still has to replace.

### Verify the Install

Read the campaign and its `/v6/webhooks` entries back before calling the build done. Confirm the tree matches the partner page, every typed child carries its type, each webhook exists with its tags and resolved URL, and each `WEBHOOK_ID` setting resolves to a webhook identifier.

Do not add inbound business-event scaffolding to an outbound install. An outbound integration reports program activity rather than producing it, so it never supersedes a marketing program's `converted` or `shipped` events, and offering to swap them after an install misrepresents what was built. Report which credentials and partner-side permissions remain and which Extole events the integration already forwards.

## Build a Reward Fulfillment Integration

A reward fulfillment partner needs everything an outbound partner needs plus a supply side: a component type for the partner's own reward suppliers, a support campaign holding one template per product the partner sells, and webhooks typed `REWARD` that fire only for rewards from those suppliers. [Integration Categories](doc:integration-categories) describes the model; this section is the order to build it in.

Install the maintained source when the duplicatable listing has one: the install carries the whole shape, including the support campaign it subscribes to, and the sequence below then serves as the checklist for confirming the install matches the partner page.

Confirm the source's type before installing it. A partner that once shipped a legacy integration still exposes that older source under the same partner name, and a name match alone will install the wrong generation. A source typed `integration-v1` or any other pre-v10 type is not the maintained v10 integration; when it is the only source available, build the v10 shape below and say that the only source on offer was legacy.

**A missing library source is a normal starting condition, not a blocker.** Most accounts can duplicate only the sources they are subscribed to, so a partner the documentation describes may have no source here at all. That is what the sequence below is for. Build it: the API creates every piece — the component type, the support campaign, the templates, the integration, and the webhooks. Reporting that the partner must first be made available to the account, when no one has asked for a library source and the whole shape can be created directly, is a refusal dressed as a prerequisite.

Build in this order, because each step's prerequisite is the step before it.

### Create the Supplier Component Type

The socket must accept this partner's suppliers and nothing else, so create a component type parented to the platform reward-supplier type:

```bash
curl --request POST "$EXTOLE_API_HOST/v1/component-types" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "example-reward-supplier-v10.0",
    "display_name": "Example Reward Supplier",
    "parent": "reward-supplier-v10.0"
  }'
```

Reusing the platform type instead lets any partner's supplier install into this integration, and reusing an unrelated type leaves the socket filter meaningless. The type has to exist before any template can carry it; a template created untyped satisfies no socket filter and no later attempt to type it in place reliably succeeds.

### Create the Support Campaign and Its Supplier Templates

Create a `CONFIGURATION` campaign with program type `campaign-component` to hold the templates:

```bash
curl --request POST "$EXTOLE_API_HOST/v2/campaigns" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "Example Support",
    "description": "Reward supplier templates installed into the Example integration.",
    "campaign_type": "CONFIGURATION",
    "program_type": "campaign-component"
  }'
```

Create one component per product variant the partner page names, typed with the supplier type, and give each the settings a client configures — value, the partner's program and account identifiers, payment terms — plus the value-mode toggle and its bounds.

Setting types come from the platform's fixed vocabulary, not from the mathematical nature of the value. There is no `DECIMAL` or `DOUBLE`, and a create request naming one is rejected as malformed JSON on the `variables` property. Supplier templates use these:

| Setting | Type |
| :------ | :--- |
| Reward value | `STRING` |
| Cash-back percentage, minimum, and maximum | `INTEGER` |
| Value-mode toggle and enabled flag | `BOOLEAN` |
| Partner program number, account identifier | `STRING` |
| Payment terms | `ENUM` with `allowed_values` — not `enum_values`, which is rejected |
| Supplier identifier | `REWARD_SUPPLIER_ID` |
| Logo | `IMAGE` | Build exactly the variants the page names. Inventing a variant produces a supplier a client can configure and the partner cannot fulfill; omitting one silently removes a product from the integration.

Then attach a reward supplier to each template. A bundled component declares this as an `elements.reward_suppliers` block in its `component.json`, but that block is a build-layer construct: `elements` is not a property of the component create request, and sending it is rejected as an unrecognized property. Through the API a reward supplier is a component-scoped resource of its own, created the same way a webhook is — with `component_ids` naming the template it belongs to:

```bash
curl --request POST "$EXTOLE_API_HOST/v2/reward-suppliers/custom-rewards" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "javascript@buildtime:context.getVariableContext().get(\"component.displayName\")",
    "type": "LOYALTY_POINTS",
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

Three parts of that supplier carry weight beyond their own value:

- The **tag** identifies the product variant. It is how the order webhook finds the suppliers it serves and how the template resolves its own supplier identifier, so a template whose tag differs from the one its webhook filters on is a supplier no webhook will ever fulfill.
- The **data map** carries the identifiers the order request needs. A request handler cannot read a setting on a component it does not own, so anything the partner endpoint requires per supplier belongs here.
- The **face-value algorithm** is resolved from the client's toggle rather than fixed in the template, with the percentage stored as a fraction and bounded by the minimum and maximum.

Give each template a `REWARD_SUPPLIER_ID` setting resolving its own element by that tag, so rules and reports can reference the supplier:

```javascript
javascript@buildtime: (function() { let filteredElements = Java.from(context.getComponent().createElementsQuery().withType('REWARD_SUPPLIER').withTag('internal:example-variant').list()); return filteredElements && filteredElements.length > 0 ? filteredElements[0].getId() : null; })();
```

### Create the Integration and Its Sockets

Create the `INTEGRATION` campaign, root, and model component as described in **Create the Integration Campaign** and **Create the Component Model**, with the partner's account identifier and a `CLIENT_KEY` credential setting. Then add the supplier socket, filtered to the type created above:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components/$INTEGRATION_COMPONENT_ID/settings" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
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

Add a `views` socket whose filters accept every view type the integration uses — the configuration type plus the report-runner and event-stream types — rather than only the configuration type, and subscribe the integration to the support campaign so its templates are installable into the supplier socket.

The report-runner and event-stream views each need their element to exist before the view will validate, and those elements follow the same rule as the supplier: what a bundle declares inline under `elements`, the API creates as its own resource attached with `component_ids`.

| Element a bundle declares | API resource |
| :------------------------ | :----------- |
| `reward_suppliers` | `POST /v2/reward-suppliers/custom-rewards` |
| `webhooks` | `POST /v6/webhooks`, with filters added per type afterwards |
| `report_runners` | `POST /v7/report-runners` |
| `event_streams` | `POST /v6/event-streams` |

A reward integration ships four views: a configuration view for the credential and account settings, a configuration view whose `settingsToDisplay` names the supplier socket and whose status reports in progress while no supplier is installed, a report-runner view charting reward activity, and an event-stream view filtered to the reward event types and the partner's app type. Order them so configuration comes first.

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

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v4/webhooks/reward/$WEBHOOK_ID/filters/supplier" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "reward_supplier_ids": "javascript@buildtime:(function(){ let children = Java.from(context.getComponent().getChildren()); let allRewardSuppliers = []; children.forEach(function(child) { let rewardSuppliers = Java.from(child.createElementsQuery().withType('"'"'REWARD_SUPPLIER'"'"').withTag('"'"'internal:example-variant'"'"').list()); rewardSuppliers.forEach(function(rewardSupplier) { allRewardSuppliers.push(rewardSupplier.getId()); }); }); return allRewardSuppliers; })()"
  }'

curl --request POST \
  "$EXTOLE_API_HOST/v4/webhooks/reward/$WEBHOOK_ID/filters/state" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{"states": ["EARNED"]}'
```

The four filter kinds each have their own path segment — `supplier`, `state`, `tags`, and `expression` — and `GET /v4/webhooks/reward/{webhook_id}/filters` lists what a webhook currently has.

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
- The account identifier is set and the credential is either configured or reported outstanding.

## What the Inbound Custom Workflow Creates

A complete inbound custom integration contains:

```text
root
└── partner                     integration-v10.x
    ├── businessEvents          MULTI_SOCKET → business-event-v10.0
    │   ├── converted           template_transacted_business_event
    │   │   ├── triggerRules
    │   │   │   └── input_event
    │   │   └── data
    │   │       ├── partner_conversion_id
    │   │       ├── cart_value
    │   │       └── other mapped fields
    │   ├── shipped             template_tracked_business_event
    │   └── canceled            template_tracked_business_event
    └── views                   MULTI_SOCKET → view-v10.0
        └── configuration       config-view-v10.0
```

The partner event name belongs in an `input_event` trigger rule. The canonical Extole event name belongs on the reusable business-event component. Do not rename the Extole business event to match the partner wire event.

## Extole Chat Creation Contract

Extole Chat must follow these rules when it creates or changes an integration:

1. Confirm the client, environment, partner platform and version, inbound and outbound scope, event contract, credential owner, and publication approval before making changes.
2. Read the partner's current documentation and verify version-specific event hooks. Do not infer hook names or payload shapes from another platform.
3. Inspect the target client before creating resources. Reuse an active integration when its campaign and component identity match the request, extend it, and report that. Archived campaigns are not candidates for reuse: they receive no events and hold no program label against a new campaign, so their presence is not a reason to restore one, to pick a different label, or to ask the requester which path to take instead of building what they asked for.
4. Discover first whether a maintained integration source already exists for the partner, matching on component name across every current `integration-v10.x` type rather than on one pinned revision. When it does, install that source by duplicating it into a new campaign, then reshape it to the partner page's finished tree and webhook set before configuring credentials. Only when no maintained partner integration exists should Chat build from the custom integration template. Do not save library component identifiers in prompts or documentation.
5. Treat the calls that complete a reshape — creating a component type, deleting an unused library child, publishing, and creating a webhook — as part of the create instruction. Attempt them; when one is refused because it requires a higher mode, raise the mode and continue. A mode that is available but not currently active is not a missing authorization, so never report a shape gap as outside what you are allowed to do without having tried and been refused. Stopping after a raw library install, or reporting a known gap as someone else's step, leaves the requester with an integration the partner page does not describe.
6. Use campaign-version-scoped mutation endpoints. Refresh the latest campaign version after every mutation.
7. Use reusable business-event, rule, and data components. Do not create a custom controller when a reusable template implements the behavior.
8. Keep partner input event names distinct from canonical Extole business event names.
9. Map every persisted field explicitly, in the same run that creates the business events. Assign key types based on field semantics, not field spelling. A business event with an empty `data` socket captures nothing and is not a finished event.
10. Add a `views` socket and at least one configuration view. The view must expose the settings required to complete partner setup.
11. Create reward suppliers, client keys, or webhooks only when an approved outbound flow uses them. A reward fulfillment partner is such a flow: its suppliers, `REWARD` webhooks, and credential setting are the integration, not extras added to an inbound build.
12. Build and inspect the complete campaign before publishing. Test every inbound event and every configured outbound path.
13. Keep a resource ledger containing campaign, component, external resource, and test identifiers. Use it for verification and cleanup.
14. Never put access tokens, secrets, or private client values in documentation, component descriptions, logs, or example payloads.
15. Report partial results as incomplete. Do not describe a draft, disabled webhook, placeholder URL, or unverified event as production-ready.

## Gather Requirements

Collect these values before calling the API:

| Value | Requirement |
| :---- | :---------- |
| Client API access token | Server-side token authorized to manage campaigns and components. |
| Management API host | The production host for campaign and component calls, held in `EXTOLE_API_HOST`. |
| Event API host | The production host for event submission, held in `EXTOLE_EVENT_API_HOST`. |
| Partner platform and version | Determines event hooks, payloads, and authentication options. |
| Integration name and component name | Human-readable campaign name and stable lowercase component name. |
| Program label | Unique, stable label used to target events to the integration. |
| Inbound event contract | Partner event names, identity fields, unique identifiers, and values. |
| Canonical business events | Extole names such as `converted`, `shipped`, or `canceled`. |
| Field mapping | Explicit source-to-destination mapping for every captured field. |
| Partner configuration | Store URL, account identifier, endpoint, status mapping, or equivalent settings. |
| Outbound requirements | Destination, trigger, authentication, retry contract, and owning program, when outbound behavior is required. |
| Publication approval | Confirmation that the target client and environment may be changed. |

Management calls and event submission use different hosts. Every example in this guide reads them from these variables:

```bash
EXTOLE_API_HOST=https://api.extole.io
EXTOLE_EVENT_API_HOST=https://events.extole.io
```

Use separate credentials for integration management and event ingestion. The partner application must not receive the Client API management token.

## Use Roll-Forward Campaign Versions

Campaign mutations create a new version. A version used by one successful request is stale for the next request.

Refresh the version before every version-scoped mutation:

```bash
CAMPAIGN_VERSION=$(
  curl --silent --show-error --fail-with-body \
    "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID" \
    --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" |
  jq --raw-output '.version'
)
```

Use the singular path segment `/version/{version}`:

```text
/v2/campaigns/{campaign_id}/version/{version}/components
```

Do not use `/versions/`. If the API returns `stale_version` or `concurrent_update`, retrieve the campaign again, reconcile the latest state, and retry only the intended mutation.

## Discover Reusable Components

Find templates at execution time through the duplicatable-components endpoint. This endpoint returns components that the current client can duplicate, including components made available through subscriptions and grants.

```bash
curl --get "$EXTOLE_API_HOST/v1/components/duplicatable" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --data-urlencode "name=template_transacted_business_event" \
  --data-urlencode "version_state=PUBLISHED" \
  --data-urlencode "having_any_types=business-event-v10.0" \
  --data-urlencode "show_all=true"
```

After the target component and socket exist, add `target_component_id` and `target_setting_name` to return only components compatible with that socket. Do not use the deprecated `target_socket_name` parameter. Narrowing this way is the reliable form of the query, because a widely used source such as `input_event` also appears once for every campaign that already installed a copy of it.

Use these reusable sources:

| Component | Program label | Purpose |
| :-------- | :------------ | :------ |
| `template_transacted_business_event` | `business-events` | Revenue or transaction outcome. |
| `template_tracked_business_event` | `business-events` | Non-revenue lifecycle milestone. |
| `input_event` | `rules` | Matches one or more partner input event names. |
| `business_event_data` | `business-events` | Captures one mapped field. |
| `event_id` | `business-events` | Captures the Extole event identifier when required. |

Validate each candidate's type before duplicating it, and prefer the v10 type when a legacy version of the same name is also returned.

Several results with the same name and the same v10 type are copies of one maintained source, one per campaign that installed it, not a choice between different behaviors. Narrow by the target socket and duplicate the maintained source; that is not the ambiguity worth stopping for. Stop when discovery returns no published match of the required type, or when two genuinely different components could satisfy the request and choosing wrongly would change behavior.

## Create the Integration Campaign

Create an `INTEGRATION` campaign with the `integration` program type. Add campaign tags that identify the integration model component.

```bash
curl --request POST "$EXTOLE_API_HOST/v2/campaigns" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "Example Integration",
    "description": "Receives partner lifecycle events and maps them to Extole business events.",
    "campaign_type": "INTEGRATION",
    "program_type": "integration",
    "tags": [
      "internal:type:integration",
      "internal:integration-component-name:example"
    ]
  }'
```

Record the returned campaign identifier and version. Campaign creation also creates a default `PROGRAM` label equal to the campaign identifier.

Replace the default with a unique, readable program label when the integration contract defines one:

```bash
curl --request POST "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/labels" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "example-integration",
    "type": "PROGRAM"
  }'
```

A campaign has one active `PROGRAM` label. Creating a new one replaces the previous program label. Always read the current campaign response and pass that value in test and partner event payloads.

## Create the Component Model

Create a root component following the Custom Integration Template conventions:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "root",
    "description": "Declares campaign-level variables and cross-campaign inheritance.",
    "tags": [
      "internal:type:integration",
      "internal:self-managed"
    ]
  }'
```

Record `ROOT_COMPONENT_ID`, refresh the campaign version, and create the model component:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "example",
    "display_name": "Example",
    "description": "Receives Example lifecycle events.",
    "types": [
      "integration-v10.0"
    ],
    "component_ids": [
      "'"$ROOT_COMPONENT_ID"'"
    ],
    "tags": [
      "internal:type:integration",
      "internal:self-managed"
    ],
    "variables": [
      {
        "name": "short.description",
        "type": "STRING",
        "values": {
          "default": "Connect Example lifecycle events to Extole."
        },
        "tags": [
          "internal:ui-display"
        ]
      },
      {
        "name": "about",
        "type": "STRING",
        "values": {
          "default": "This integration receives Example events and maps them to Extole business events."
        },
        "tags": [
          "internal:ui-display"
        ]
      },
      {
        "name": "documentation.url",
        "type": "STRING",
        "values": {
          "default": "https://docs.extole.com/docs/example"
        },
        "tags": [
          "internal:ui-display"
        ]
      }
    ]
  }'
```

Use `variables` when creating a component. Do not send a `settings` property in `CampaignComponentCreateRequest`.

Type the model component with the current integration type. `integration-v10.0` is the long-standing revision, and later revisions such as `integration-v10.1` exist; when extending an installed source, keep the type it already carries rather than downgrading it to match this example.

## Set Integration Display Metadata

The integration type requires eight settings: `short.description`, `about`, `documentation.url`, `external.url`, `external.integration.url`, `categories`, `logo`, and `imageKey`. The type checks that they are present, not that their values are usable, so a component that passes validation can still render as an unnamed tile with a broken image.

| Setting | Value convention |
| :------ | :--------------- |
| `short.description` | One sentence for the integration tile. |
| `about` | A short paragraph describing what the integration receives and sends. |
| `documentation.url` | The partner-facing documentation page for this integration. Not this build guide. |
| `external.url` | The partner's own product site. |
| `external.integration.url` | The partner's marketplace or extension listing, or an empty string when the partner has none. |
| `categories` | A single category string already used by other integrations, such as `eCommerce Platform`. The admin groups integrations by exact value, so a new spelling or a list-shaped value creates an orphan category. |
| `logo` | Type `IMAGE`. An image URL, or a buildtime expression resolving an uploaded asset, such as `spel@buildtime:context.getAsset('example').getUrl()`. The admin binds this value directly to an image source; a bare name renders the placeholder image. |
| `imageKey` | The stable key identifying the integration image. |

Tag all eight with `internal:ui-display`. That tag means the setting describes the integration tile, and the admin hides tagged settings from the settings list.

Add partner configuration variables separately, and never tag them `internal:ui-display` — a partner setting carrying that tag disappears from the configuration view even when `settingsToDisplay` names it, which is the most common reason a freshly built integration looks empty on its configuration tab. Give each one a display name, description, type, default, `importance:basic`, and a priority that orders it in the view. Prefix partner-specific configuration settings with the integration component name — `exampleAccountUrl`, `exampleSetupInstructions` — so they stay unambiguous when read from the parent component.

Setup instructions tell the partner-side installer what to send and where. Give them the event endpoint, the event names, the payload fields, the credential rule, and the documentation link. Leave the program label out: it is an Extole-side targeting device, not something the partner configures, and printing it invites senders to hard-code a value that belongs to this campaign alone.

Compute the instructions at build time so the installer reads the values this campaign actually uses rather than values copied from another account:

```json
{
  "name": "exampleSetupInstructions",
  "type": "STRING",
  "display_name": "Example Extension Setup",
  "description": "Connection details for the server-side Example extension.",
  "tags": ["category:configuration", "importance:basic"],
  "priority": "20",
  "values": {
    "default": "javascript@buildtime:(function(){ return \"Extole event endpoint: https://events.extole.io/v6/events\\nEvent names: example_order_created, example_order_shipped, example_order_canceled\\nUse a server-side event-ingestion credential. Do not use a management token in the partner application.\"; })()"
  }
}
```

Never place a credential value in a setting that the configuration view displays.

## Add Typed Sockets

Add a `businessEvents` multi-socket to the integration component:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components/$INTEGRATION_COMPONENT_ID/settings" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "businessEvents",
    "display_name": "Business Events",
    "description": "Reusable business events produced from partner input events.",
    "type": "MULTI_SOCKET",
    "filters": [
      {
        "type": "COMPONENT_TYPE",
        "component_type": "business-event-v10.0"
      }
    ]
  }'
```

Add a `views` multi-socket:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components/$INTEGRATION_COMPONENT_ID/settings" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "views",
    "display_name": "Views",
    "description": "Views rendered in the integration UI.",
    "type": "MULTI_SOCKET",
    "filters": [
      {
        "type": "COMPONENT_TYPE",
        "component_type": "view-v10.0"
      }
    ]
  }'
```

Socket filters are part of the model contract. Do not create an untyped socket or attach a component that does not satisfy its filter.

## Add a Configuration View

Create a `config-view-v10.0` child and attach it to the integration model component:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "configuration",
    "display_name": "Configuration",
    "description": "Configuration view for the Example integration.",
    "types": [
      "config-view-v10.0"
    ],
    "installed_into_socket": "views",
    "component_ids": [
      "'"$INTEGRATION_COMPONENT_ID"'"
    ],
    "variables": [
      {
        "name": "order",
        "type": "INTEGER",
        "values": {
          "default": 1
        }
      },
      {
        "name": "title",
        "type": "STRING",
        "values": {
          "default": "Configuration"
        }
      },
      {
        "name": "status",
        "type": "STRING",
        "values": {
          "default": "javascript@buildtime:context.getComponent().getParent().getVariableValue(\"exampleAccountUrl\") ? \"READY\" : \"IN_PROGRESS\""
        }
      },
      {
        "name": "settingsToDisplay",
        "type": "STRING_LIST",
        "values": {
          "default": [
            "exampleAccountUrl",
            "exampleSetupInstructions"
          ]
        }
      }
    ]
  }'
```

`component_ids` must identify the parent model component. Without it, the platform may try to install the view into the root component, which does not own the `views` socket.

The `settingsToDisplay` values are names of settings on the parent integration model component. Naming a setting here is necessary but not sufficient: the setting itself must be visible in the settings list, which means it must not carry `internal:ui-display`. Read the built integration back and confirm each named setting appears with its display name before calling the configuration surface done. A hardcoded `status` leaves the tab permanently marked in progress; the buildtime expression above returns `READY` only once the settings Extole can verify are complete. Explain any partner-side checks that the status cannot verify.

Include a parent information setting that gives the installer the endpoint, current program label, partner event names, documentation URL, and credential handling rule. Do not put a credential value in this setting.

## Add Reusable Business Events

Choose the template by business meaning:

- Use `template_transacted_business_event` when the event carries transaction value or represents the program outcome.
- Use `template_tracked_business_event` for lifecycle milestones without transaction value.

Duplicate the source component into the model component's `businessEvents` socket:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v1/components/$BUSINESS_EVENT_TEMPLATE_ID/duplicate" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "target_campaign_id": "'"$CAMPAIGN_ID"'",
    "target_component_absolute_name": "/example",
    "target_setting_name": "businessEvents",
    "component_name": "converted",
    "component_display_name": "Converted",
    "description": "Records a completed partner transaction.",
    "variables": [
      {
        "name": "eventName",
        "type": "STRING",
        "values": {
          "default": "converted"
        }
      },
      {
        "name": "aliases",
        "type": "STRING_LIST",
        "values": {
          "default": [
            "conversion",
            "customer",
            "outcome",
            "transacted"
          ]
        }
      },
      {
        "name": "singularNounName",
        "type": "STRING",
        "values": {
          "default": "Conversion"
        }
      },
      {
        "name": "adminUIIcon",
        "type": "STRING",
        "values": {
          "default": "fa-regular fa-shopping-cart"
        }
      },
      {
        "name": "pluralNounName",
        "type": "STRING",
        "values": {
          "default": "Conversions"
        }
      },
      {
        "name": "rateName",
        "type": "STRING",
        "values": {
          "default": "Conversion Rate"
        }
      },
      {
        "name": "sequence",
        "type": "STRING",
        "values": {
          "default": "103.2"
        }
      },
      {
        "name": "dataCapturePolicy",
        "type": "ENUM",
        "values": {
          "default": "NO_ADDITIONAL_DATA"
        }
      }
    ]
  }'
```

Use the canonical v10 name that matches the business outcome. Examples include `converted`, `shipped`, `canceled`, `returned`, `account_opened`, and `application_approved`. Do not use a transport-specific name such as `partner_order_created` as the business-event component name.

Create one business-event instance per canonical event. Do not create duplicate legacy controllers alongside the reusable component.

Set `sequence` so the events sort in lifecycle order, with the outcome event first and later milestones after it. The value orders steps within the funnel; the exact numbers matter only relative to one another.

Set the reporting names on every duplicate. `singularNounName`, `pluralNounName`, and `rateName` are what reports and the admin funnel display. The templates ship with generic values — a tracked template calls everything "Tracked Events" with a "Tracked Event Rate", and `singularNounName` defaults to an expression that echoes the display name — so two events duplicated from the same template report under identical labels until you override them. Give each canonical event its own noun and rate names, and give each an `adminUIIcon` that reads as its outcome. No two events in one integration should share an icon.

Set `aliases` to the alias set the platform already uses for that canonical event. Aliases are additional names that this business event matches, and platform consumers subscribe to them: an extension or downstream integration listening for `outcome` sees a `converted` event only because `converted` carries that alias. Read the alias set from an existing program's business event of the same name rather than inventing one. Bundled programs use these:

| Canonical event | Aliases |
| :-------------- | :------ |
| `converted` | `conversion`, `customer`, `outcome`, `transacted` |
| `account_qualified` | `customer`, `outcome` |
| `account_opened` | `customer` |
| `shipped`, `canceled` | none |

Do not add partner-flavored aliases, and do not clear an alias set the template or canonical event provides. The same alias must never appear on two business events in one campaign: the match becomes ambiguous, and the event that wins is not something the configuration expresses.

Inspect the duplicated component's evaluated `journeyName` and `roleName` values. Do not hardcode one pair for every integration: these values depend on whether the event is associated with a campaign journey and on the surrounding role and journey hierarchy. Preserve the reusable template's defaults unless the integration contract requires different values, and record the published values during verification.

## Configure Input Event Rules

Duplicate `input_event` from the `rules` program into each business event's `triggerRules` socket:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v1/components/$INPUT_EVENT_TEMPLATE_ID/duplicate" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "target_campaign_id": "'"$CAMPAIGN_ID"'",
    "target_component_absolute_name": "/example/converted",
    "target_setting_name": "triggerRules",
    "variables": [
      {
        "name": "triggerEventNames",
        "type": "STRING_LIST",
        "values": {
          "default": [
            "partner_order_created"
          ]
        }
      }
    ]
  }'
```

Keep the duplicated rule under its source name `input_event`. Library components and bundled programs all do, so a reader recognizes the trigger by its position in the business event rather than by a component name that restates the event it listens for. The partner event name belongs in `triggerEventNames`.

Add a legacy partner event alias only when a real sender still emits it. Document the preferred spelling and migration plan.

## Configure Event Data

Data capture is the part of the integration that carries meaning. Without it an inbound event produces a step with no transaction identifier, no person key, and no value, so nothing downstream can deduplicate, attribute, reward, or report on it. Create the data components in the same run as the business events they belong to. An integration whose `data` sockets are empty is not built, however complete its tree looks.

Take the field names from the partner's documented payload. When a partner-specific page exists in this documentation set, its payload example is the contract; otherwise use the partner's own developer documentation. Ask the requester for a sample payload only when neither source defines the field, and create the identity and deduplication fields that are defined rather than deferring the whole mapping.

Define a mapping before creating data components:

| Extole field | Partner field | Required | Key type | Persist type |
| :----------- | :------------ | :------- | :------- | :----------- |
| `partner_conversion_id` | Transaction identifier | Yes for transaction events | `UNIQUE_PARTNER_EVENT_KEY` | `STEP` |
| `partner_user_id` | Customer identifier | Recommended | `PARTNER_PROFILE_KEY` | `STEP` |
| `cart_value` | Transaction amount | Recommended for revenue events | `VALUE` | `STEP` |
| `email` | Email address | Required when no other identity is sufficient | `NONE` | `STEP` |
| `first_name` | First name | Optional | `NONE` | `STEP` |
| `last_name` | Last name | Optional | `NONE` | `STEP` |
| `coupon_code` | Applied coupon | Optional | `NONE` | `STEP` |

Duplicate one `business_event_data` component into the business event's `data` socket for each field:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v1/components/$BUSINESS_EVENT_DATA_TEMPLATE_ID/duplicate" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "target_campaign_id": "'"$CAMPAIGN_ID"'",
    "target_component_absolute_name": "/example/converted",
    "target_setting_name": "data",
    "component_name": "partner_conversion_id",
    "variables": [
      {
        "name": "name",
        "type": "STRING",
        "values": {
          "default": "partner_conversion_id"
        }
      },
      {
        "name": "valueExpression",
        "type": "STRING",
        "values": {
          "default": "javascript@runtime:context.getCauseEvent().getData()['order_id']"
        }
      },
      {
        "name": "scope",
        "type": "ENUM",
        "values": {
          "default": "PRIVATE"
        }
      },
      {
        "name": "persistTypes",
        "type": "ENUM_LIST",
        "values": {
          "default": [
            "STEP"
          ]
        }
      },
      {
        "name": "keyType",
        "type": "ENUM",
        "values": {
          "default": "UNIQUE_PARTNER_EVENT_KEY"
        }
      }
    ]
  }'
```

Set `valueExpression` explicitly when the partner field and Extole field have distinct names. Verify the expression against a real sanitized partner payload. Do not rely on the data component's name-derived default when the source field differs.

Use `NO_ADDITIONAL_DATA` when the event must store only declared fields. Capture the minimum data needed for identity, deduplication, attribution, rules, and reporting.

Every business event needs its own data components — a field captured on one event is not visible on another. At minimum, each event captures the partner transaction identifier as `UNIQUE_PARTNER_EVENT_KEY` and the partner customer identifier as `PARTNER_PROFILE_KEY`, plus whatever identity the partner sends. Revenue events additionally capture the amount as `VALUE`. Repeat the identity set on lifecycle events such as `shipped` and `canceled`: they arrive independently and must resolve to the same person and the same original transaction.

## Gate Outbound Resources

This section applies to an inbound custom build that someone proposes to extend outbound. The webhooks and credential an outbound library install ships with are already part of its finished shape and are not gated here.

Inbound event mapping does not require a reward supplier, webhook, or webhook client key.

Create outbound resources only when all of these conditions are true:

- The requested scope includes a defined outbound use case.
- A program action or reward rule produces the event or reward.
- The destination endpoint and authentication contract exist.
- Retry, idempotency, error handling, and ownership are defined.
- The integration or program has a configuration surface for required values.
- The path can be tested before it is enabled.

A reward-supplier socket does not connect a partner. A reward supplier models fulfillment inventory or behavior. A webhook is the HTTP transport. Creating either resource without the other program wiring leaves unused external resources and misleading configuration.

When outbound scope is later removed, archive resources in dependency order:

1. Disable the webhook.
2. Remove webhook filters and component references.
3. Archive the webhook.
4. Remove reward-supplier references from rules and components.
5. Archive the reward supplier.
6. Remove and archive the client key after all active references are gone.
7. Remove unused component settings and sockets.
8. Publish and verify the resulting campaign.

## Validate Before Publishing

Inspect the latest campaign and built components. Confirm:

- Campaign type is `INTEGRATION` and program type is `integration`.
- Campaign tags identify the model component.
- The root and integration model components exist, the model component carrying an `integration-v10.x` type.
- `businessEvents` accepts `business-event-v10.0`.
- Each canonical event is a duplicated reusable template.
- Each event has an `input_event` rule with the expected partner event names.
- Each event has its own reporting names and no two events share a noun or rate name.
- No alias appears on more than one business event.
- Every business event has data components in its `data` socket, and every data component has the intended source expression and key type.
- The eight required integration display settings hold usable values: a resolvable logo, a category that other integrations already use, and a partner-facing documentation URL.
- No legacy custom controller duplicates a reusable business event.
- `views` accepts `view-v10.0`.
- The configuration view is attached to the model component.
- `settingsToDisplay` references existing parent settings.
- No unrequested reward supplier, webhook, client key, or socket exists.

Publish the explicit version that was validated:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/publish" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{}'
```

Treat a successful publish as model validation, not end-to-end verification.

## Verify Inbound Events

Send a synchronous test event through `POST /v6/events` on the event host. Event submission uses a different host and a different credential from the management calls above, so a caller that can create campaigns is not necessarily able to submit events. When the calling context has no event credential, hand the request below to whoever does, together with the values the resulting step must contain, and report the integration as built but unverified.

Put the current program label inside `data` to target this campaign during the test. The label is a testing convenience and does not belong in the partner's own payload or setup instructions.

```bash
curl --request POST "$EXTOLE_EVENT_API_HOST/v6/events" \
  --header "Authorization: Bearer $EVENT_INGESTION_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "event_name": "partner_order_created",
    "data": {
      "email": "test@example.com",
      "order_id": "test-order-001",
      "total": 42.50,
      "customer_id": "test-customer-001",
      "labels": "'"$PROGRAM_LABEL"'"
    }
  }'
```

Use the returned `person_id` to list the person's resulting events:

```bash
curl --get "$EXTOLE_API_HOST/v5/persons/$PERSON_ID/steps" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --data-urlencode "campaign_ids=$CAMPAIGN_ID" \
  --data-urlencode "names=converted"
```

Confirm the canonical event name and every mapped value. Use a new unique identifier for each repeat test unless duplicate handling is the behavior under test.

Test:

- Every preferred partner input event.
- Every supported legacy alias.
- Missing required identity.
- A repeated unique partner event identifier.
- Invalid amount and status values.
- Partner retry behavior.
- Campaign targeting with the current program label.
- Configuration view contents and status.

## Offer to Connect the Integration to a Program

A finished integration receives partner events and turns them into business events inside its own campaign. The marketing programs in the account still run on the business events their theme shipped with — a generic `converted` on the friend journey, for example — which listen for the platform's default events, not the partner's. Until those two halves are joined, the integration produces activity that no program acts on.

Close the build by proposing two things and doing neither without an answer:

1. Publish the integration campaign, which is what makes the inbound endpoint accept events.
2. Install the integration's business events into a marketing campaign.

For the second, name the campaign candidates, list the partner events by canonical name, and say for each one whether it supersedes an event the program already has or adds one the program lacks. A partner `converted` supersedes the theme's `converted` on the same journey; `shipped` and `canceled` are usually additions.

On approval, work through the target campaign's journey socket:

- Duplicate each partner business event from the integration into the socket that holds the program's equivalent event, using the same duplication call as the rest of this guide with the integration's component as the source.
- Remove the superseded default event after its replacement is installed, so the journey does not carry two events with the same canonical name.
- Add the partner events the program lacks into the same socket.
- Refresh the campaign version between mutations, then read the built campaign and confirm the journey lists the expected events in lifecycle order.

This changes a program's funnel, so it is never a silent step. Name the campaign and the events before touching them, and report afterwards which events were replaced, which were added, and what the program's journey now contains.

## Record the Result

The creation response must include:

- Environment and client.
- Campaign identifier, current version, state, and program label.
- Root and model component identifiers.
- Canonical business events and partner trigger names.
- Field mappings and key types.
- View components and displayed settings.
- External resources created, or an explicit statement that none were required.
- Programs whose business events were replaced or added to, or an explicit statement that the integration is not yet connected to a program.
- Test event identifiers and verification results.
- Documentation URL.
- Remaining manual partner steps.

Do not claim the integration is complete while partner-side installation, credentials, status mapping, or end-to-end tests remain outstanding.

## Reference Structure for an Order Lifecycle Integration

Most commerce platforms map onto the same three canonical events. Use this as the starting shape and adjust it to the events the partner actually emits:

| Canonical event | Reusable template | Partner input event | Captured fields |
| :-------------- | :---------------- | :------------------ | :-------------- |
| `converted` | `template_transacted_business_event` | The partner's order-created or order-qualified event | `partner_conversion_id`, `cart_value`, `partner_user_id`, `email`, `first_name`, `last_name`, `coupon_code`, and any store or account identifier |
| `shipped` | `template_tracked_business_event` | The partner's shipment event | `partner_conversion_id`, `partner_user_id`, `email`, `first_name`, `last_name` |
| `canceled` | `template_tracked_business_event` | The partner's cancellation event, plus any legacy spelling a live sender still emits | `partner_conversion_id`, `partner_user_id`, `email`, `first_name`, `last_name` |

A complete integration of this shape contains one integration model component, three business events, one `input_event` rule per event, one data component per captured field on each event, and one configuration view displaying the partner account setting and the computed setup instructions. It is inbound-only: no reward-supplier socket, reward webhook, or webhook client key.

Platforms with a different lifecycle keep the same construction and change the event set. A lending or account platform maps to `account_opened`, `application_approved`, and `funded`; a subscription platform maps to `converted`, `renewed`, and `canceled`. The canonical name always describes the business outcome, never the partner's transport name.
