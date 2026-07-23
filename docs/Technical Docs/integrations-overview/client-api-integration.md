---
title: "Create an Integration With the Client API"
excerpt: "Create, configure, publish, verify, and maintain a reusable Extole integration through the Client API without uploading a component bundle.\n"
---

# Overview

Use the Client API to create an integration campaign and its component hierarchy directly in Extole. This workflow is intended for Extole Chat, installers, and operational services that must build an integration without adding a bundle to the creative repository.

An API-created integration is still a component-based integration. It must use the same reusable component types, typed sockets, business-event templates, views, naming conventions, and validation rules as a bundled v10 integration.

The OpenCart integration is the reference implementation used throughout this guide. It receives partner order events and maps them to the canonical Extole business events `converted`, `shipped`, and `canceled`.

## What the Workflow Creates

A complete inbound integration contains:

```text
root
└── partner                     integration-v10.0
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
3. Inspect the target client before creating resources. Reuse the existing integration when its campaign and component identity match the request.
4. Discover reusable components by name, program label, type, and published state. Do not save library component identifiers in prompts or documentation.
5. Use campaign-version-scoped mutation endpoints. Refresh the latest campaign version after every mutation.
6. Use reusable business-event, rule, and data components. Do not create a custom controller when a reusable template implements the behavior.
7. Keep partner input event names distinct from canonical Extole business event names.
8. Map every persisted field explicitly. Assign key types based on field semantics, not field spelling.
9. Add a `views` socket and at least one configuration view. The view must expose the settings required to complete partner setup.
10. Create reward suppliers, client keys, or webhooks only when an approved outbound flow uses them.
11. Build and inspect the complete campaign before publishing. Test every inbound event and every configured outbound path.
12. Keep a resource ledger containing campaign, component, external resource, and test identifiers. Use it for verification and cleanup.
13. Never put access tokens, secrets, or private client values in documentation, component descriptions, logs, or example payloads.
14. Report partial results as incomplete. Do not describe a draft, disabled webhook, placeholder URL, or unverified event as production-ready.

## Gather Requirements

Collect these values before calling the API:

| Value | Requirement |
| :---- | :---------- |
| Client API access token | Server-side token authorized to manage campaigns and components. |
| Management API host | Use `https://api.extole.io` for production campaign and component calls. |
| Event API host | Use `https://events.extole.io` for production event submission. |
| Partner platform and version | Determines event hooks, payloads, and authentication options. |
| Integration name and component name | Human-readable campaign name and stable lowercase component name. |
| Program label | Unique, stable label used to target events to the integration. |
| Inbound event contract | Partner event names, identity fields, unique identifiers, and values. |
| Canonical business events | Extole names such as `converted`, `shipped`, or `canceled`. |
| Field mapping | Explicit source-to-destination mapping for every captured field. |
| Partner configuration | Store URL, account identifier, endpoint, status mapping, or equivalent settings. |
| Outbound requirements | Destination, trigger, authentication, retry contract, and owning program, when outbound behavior is required. |
| Publication approval | Confirmation that the target client and environment may be changed. |

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

Find templates at execution time. Filter published components by source name, then confirm `program_label`, `types`, state, and ownership in the response.

```bash
curl --get "$EXTOLE_API_HOST/v1/components" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --data-urlencode "name=template_transacted_business_event" \
  --data-urlencode "owner=EXTOLE" \
  --data-urlencode "version_state=PUBLISHED" \
  --data-urlencode "show_all=true" \
  --data-urlencode "include_subscribed=true"
```

Use these reusable sources:

| Component | Program label | Purpose |
| :-------- | :------------ | :------ |
| `template_transacted_business_event` | `business-events` | Revenue or transaction outcome. |
| `template_tracked_business_event` | `business-events` | Non-revenue lifecycle milestone. |
| `input_event` | `rules` | Matches one or more partner input event names. |
| `business_event_data` | `business-events` | Captures one mapped field. |
| `event_id` | `business-events` | Captures the Extole event identifier when required. |

Stop if discovery returns no exact published match or multiple ambiguous matches. Do not choose the first result without validating its program label and type.

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

Add partner configuration variables separately. Give each variable a clear display name, description, type, default, importance tag, and priority.

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
          "default": "IN_PROGRESS"
        }
      },
      {
        "name": "settingsToDisplay",
        "type": "STRING_LIST",
        "values": {
          "default": [
            "partnerAccountUrl",
            "partnerSetupInstructions"
          ]
        }
      }
    ]
  }'
```

`component_ids` must identify the parent model component. Without it, the platform may try to install the view into the root component, which does not own the `views` socket.

The `settingsToDisplay` values are names of settings on the parent integration model component. Use a buildtime `status` expression to return `READY` only when the settings Extole can verify are complete. Explain any partner-side checks that the status cannot verify.

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

Add a legacy partner event alias only when a real sender still emits it. Document the preferred spelling and migration plan.

## Configure Event Data

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

## Gate Outbound Resources

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
- The root and `integration-v10.0` model components exist.
- `businessEvents` accepts `business-event-v10.0`.
- Each canonical event is a duplicated reusable template.
- Each event has an `input_event` rule with the expected partner event names.
- Every data component has the intended source expression and key type.
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

Send a synchronous test event through `POST /v6/events`. Put the current program label inside `data`.

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

## Record the Result

The creation response must include:

- Environment and client.
- Campaign identifier, current version, state, and program label.
- Root and model component identifiers.
- Canonical business events and partner trigger names.
- Field mappings and key types.
- View components and displayed settings.
- External resources created, or an explicit statement that none were required.
- Test event identifiers and verification results.
- Documentation URL.
- Remaining manual partner steps.

Do not claim the integration is complete while partner-side installation, credentials, status mapping, or end-to-end tests remain outstanding.

## OpenCart Reference Structure

The OpenCart reference uses this model:

| Canonical event | Reusable template | Partner input event | Captured fields |
| :-------------- | :---------------- | :------------------ | :-------------- |
| `converted` | `template_transacted_business_event` | `opencart_order_created` | `partner_conversion_id`, `cart_value`, `partner_user_id`, `email`, `first_name`, `last_name`, `coupon_code`, `store_url` |
| `shipped` | `template_tracked_business_event` | `opencart_order_shipped` | `partner_conversion_id`, `partner_user_id`, `email`, `first_name`, `last_name` |
| `canceled` | `template_tracked_business_event` | `opencart_order_canceled`; legacy `opencart_order_cancelled` | `partner_conversion_id`, `partner_user_id`, `email`, `first_name`, `last_name` |

Its configuration view displays the OpenCart store URL and partner setup instructions. The integration is inbound-only. It does not contain a reward-supplier socket, reward webhook, or webhook client key.
