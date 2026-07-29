---
title: "Create an Integration With the Client API"
excerpt: "Create, configure, publish, verify, and maintain a reusable Extole integration through the Client API without uploading a component bundle.\n"
---

# Overview

Use the Client API to create an integration campaign and its component hierarchy directly in Extole. This workflow is intended for Extole Chat, installers, and operational services that must build an integration without adding a bundle to the creative repository.

An API-created integration is still a component-based integration. It must use the same reusable component types, typed sockets, business-event templates, views, naming conventions, and validation rules as a bundled v10 integration.

Examples in this guide use a generic partner named `example`. Substitute the real partner name, event names, and field names from that partner's own documentation.

Where a partner-specific page exists in this documentation set, read it first: it carries the wire contract for that platform — event names, payload fields, and status mapping — while this guide carries the build sequence that applies to every platform. Partner pages are published under the partner's name as the page slug, so retrieve the page directly by that slug rather than relying on a keyword search to surface it.

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
8. Map every persisted field explicitly, in the same run that creates the business events. Assign key types based on field semantics, not field spelling. A business event with an empty `data` socket captures nothing and is not a finished event.
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

## Set Integration Display Metadata

The `integration-v10.0` type requires eight settings: `short.description`, `about`, `documentation.url`, `external.url`, `external.integration.url`, `categories`, `logo`, and `imageKey`. The type checks that they are present, not that their values are usable, so a component that passes validation can still render as an unnamed tile with a broken image.

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

Compute setup instructions at build time so the installer reads the values this campaign actually uses rather than values copied from another account:

```json
{
  "name": "exampleSetupInstructions",
  "type": "STRING",
  "display_name": "Example Extension Setup",
  "description": "Connection details for the server-side Example extension.",
  "tags": ["category:configuration", "importance:basic"],
  "priority": "20",
  "values": {
    "default": "javascript@buildtime:(function(){ return \"Extole event endpoint: https://events.extole.io/v6/events\\nProgram label: \" + context.getProgramLabel() + \"\\nEvent names: example_order_created, example_order_shipped, example_order_canceled\"; })()"
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

Put the current program label inside `data`.

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

## Reference Structure for an Order Lifecycle Integration

Most commerce platforms map onto the same three canonical events. Use this as the starting shape and adjust it to the events the partner actually emits:

| Canonical event | Reusable template | Partner input event | Captured fields |
| :-------------- | :---------------- | :------------------ | :-------------- |
| `converted` | `template_transacted_business_event` | The partner's order-created or order-qualified event | `partner_conversion_id`, `cart_value`, `partner_user_id`, `email`, `first_name`, `last_name`, `coupon_code`, and any store or account identifier |
| `shipped` | `template_tracked_business_event` | The partner's shipment event | `partner_conversion_id`, `partner_user_id`, `email`, `first_name`, `last_name` |
| `canceled` | `template_tracked_business_event` | The partner's cancellation event, plus any legacy spelling a live sender still emits | `partner_conversion_id`, `partner_user_id`, `email`, `first_name`, `last_name` |

A complete integration of this shape contains one integration model component, three business events, one `input_event` rule per event, one data component per captured field on each event, and one configuration view displaying the partner account setting and the computed setup instructions. It is inbound-only: no reward-supplier socket, reward webhook, or webhook client key.

Platforms with a different lifecycle keep the same construction and change the event set. A lending or account platform maps to `account_opened`, `application_approved`, and `funded`; a subscription platform maps to `converted`, `renewed`, and `canceled`. The canonical name always describes the business outcome, never the partner's transport name.
