---
title: "Map Inbound Partner Events"
excerpt: "Add reusable business events, input event rules, and event data to an integration that receives partner events, then verify what arrives.\n"
---

This page is one part of the Client API integration guide. Start at [Create an Integration With the Client API](doc:client-api-integration) for the build paths and the creation contract.

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

This tree receives events; it does not produce them. The extension, service, or feed that sends them from the partner platform is built against [Send Platform Events to Extole](doc:sending-platform-events), and an inbound integration is finished only when both halves exist.

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
