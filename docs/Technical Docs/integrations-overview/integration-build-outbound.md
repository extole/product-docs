---
title: "Build an Outbound Library Integration"
excerpt: "Install a maintained partner source, reshape it to the documented tree, and attach its outbound webhooks and credential.\n"
---

This page is one part of the Management API integration guide. Start at [Create an Integration with the Management API](doc:management-api-integration) for the build paths and the creation contract.

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

`POST /v6/webhooks`:

```json
{
  "name": "javascript@buildtime:context.getComponent().getName() + '_message_trigger'",
  "url": "javascript@buildtime:context.getVariableContext().get('partnerRestUrl') + '/partner/endpoint/path'",
  "type": "GENERIC",
  "default_method": "POST",
  "enabled": "javascript@buildtime:context.getVariableContext().get('enabled')",
  "client_key_id": "javascript@buildtime:context.getVariableContext().get('clientKeyId')",
  "request": "javascript@runtime:context.createRequestBuilderWithDefaults().withUserAgent('partner-Extole-Integration/1.0').build();",
  "retry_intervals": [1, 30, 60],
  "tags": ["internal:partner:campaign", "internal:partner"],
  "component_ids": ["INTEGRATION_COMPONENT_ID"]
}
```

Name each webhook for the endpoint it calls — an ingestion endpoint and a message-trigger endpoint are separate webhooks with separate tags. Tag every webhook by purpose, because the tags are what the `WEBHOOK_ID` settings resolve: an untagged webhook produces a setting that evaluates to null and an integration that silently sends nothing.

When the account URL setting may be stored without a scheme, build the URL expression to add `https://` rather than assuming the stored value carries it.

### Attach the Credential

Create a webhook client key only when the requester has supplied the partner's API secret, then set the credential setting on the integration component. Missing credentials do not block the reshape: finish the tree, webhooks, and settings, leave the credential setting null, and report which values remain outstanding.

The account URL is different from the secret. Blanking it to signal "not yet configured" breaks the publish that the rest of the reshape depends on, so leave a valid placeholder host in place and report it as a value the requester still has to replace.

### Verify the Install

Read the campaign and its `/v6/webhooks` entries back before calling the build done. Confirm the tree matches the partner page, every typed child carries its type, each webhook exists with its tags and resolved URL, and each `WEBHOOK_ID` setting resolves to a webhook identifier.

Do not add inbound business-event scaffolding to an outbound install. An outbound integration reports program activity rather than producing it, so it never supersedes a marketing program's `converted` or `shipped` events, and offering to swap them after an install misrepresents what was built. Report which credentials and partner-side permissions remain and which Extole events the integration already forwards.
