---
title: "Create an Integration with the Client API"
excerpt: "Use Extole's Client API to create, configure, publish, and verify a reusable integration without uploading a component bundle.\n"
---

## Overview

Use the Client API to create an integration campaign and configure its behavior directly in Extole. This approach is useful when an integration is created by an installer, an AI agent, or an operational service instead of being packaged and uploaded as a creative bundle.

The workflow creates a campaign, installs the Custom Integration Template, and adds reusable business events to the integration. Each business event listens for an external input event and captures the fields required by the program.

## Prerequisites

Prepare the following values before calling the API:

| Value | Description |
| :---- | :---------- |
| Client API access token | A token with permission to manage campaigns and components. |
| Extole API host | Use `https://api.extole.io` for production or the host for your environment. |
| Integration name | The name displayed for the integration campaign. |
| External event names | The event names emitted by the partner platform. |
| Field mapping | The partner fields that identify the person, transaction, amount, and optional attributes. |

Keep the access token on the server that creates the integration. Do not expose it in browser code or documentation examples.

## Create The Campaign

Create an `INTEGRATION` campaign with the `integration` program type.

```bash
curl --request POST "$EXTOLE_API_HOST/v2/campaigns" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "Example Integration",
    "campaign_type": "INTEGRATION",
    "program_type": "integration"
  }'
```

Record the returned `campaign_id`. Use it in every subsequent campaign-scoped request.

Add a `PROGRAM` label to the campaign. The label lets incoming events target the integration.

```bash
curl --request POST "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/labels" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "example-integration",
    "type": "PROGRAM"
  }'
```

## Install The Custom Integration Template

Create the root component and the integration component through the component API. The exact component settings depend on the installation experience, but the integration component should have a stable absolute name such as `/example`.

Add a `businessEvents` multi-socket to the integration component. Configure the socket to accept `business-event-v10.0` components.

```json
{
  "name": "businessEvents",
  "type": "MULTI_SOCKET",
  "filters": [
    {
      "component_type": "business-event-v10.0",
      "type": "COMPONENT_TYPE"
    }
  ]
}
```

Create the socket with:

```bash
curl --request POST "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/components/$INTEGRATION_COMPONENT_ID/settings" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "businessEvents",
    "type": "MULTI_SOCKET",
    "filters": [
      {
        "component_type": "business-event-v10.0",
        "type": "COMPONENT_TYPE"
      }
    ]
  }'
```

## Add Reusable Business Events

Find the reusable business-event templates from the `business-events` library. Use the transacted template for an outcome that represents a purchase or other revenue event. Use the tracked template for a milestone such as shipment or cancellation.

Duplicate the selected template into the integration component's `businessEvents` socket.

```bash
curl --request POST "$EXTOLE_API_HOST/v1/components/$BUSINESS_EVENT_TEMPLATE_ID/duplicate" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "target_campaign_id": "$CAMPAIGN_ID",
    "target_component_absolute_name": "/example",
    "target_setting_name": "businessEvents",
    "component_name": "conversion",
    "variables": [
      {
        "name": "eventName",
        "type": "STRING",
        "values": {
          "default": "conversion"
        }
      },
      {
        "name": "aliases",
        "type": "STRING_LIST",
        "values": {
          "default": [
            "conversion"
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
          "default": "1"
        }
      }
    ]
  }'
```

The variable names are settings exposed by the reusable template. Set `adminUIIcon` when the event needs a specific icon. Set `dataCapturePolicy` to `NO_ADDITIONAL_DATA` when the integration should store only the fields explicitly configured on the event.

Create each event as a separate component instance. For example:

| Component name | Template | External event |
| :------------- | :-------- | :-------------- |
| `conversion` | `template_transacted_business_event` | `order_created` |
| `ship` | `template_tracked_business_event` | `order_shipped` |
| `return` | `template_tracked_business_event` | `order_cancelled` |

## Configure Input Event Rules

Find the reusable `input_event` rule component and duplicate it into the `triggerRules` socket of each business event. Override `triggerEventNames` with the partner event name.

```bash
curl --request POST "$EXTOLE_API_HOST/v1/components/$INPUT_EVENT_TEMPLATE_ID/duplicate" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "target_campaign_id": "$CAMPAIGN_ID",
    "target_component_absolute_name": "/example/conversion",
    "target_setting_name": "triggerRules",
    "variables": [
      {
        "name": "triggerEventNames",
        "type": "STRING_LIST",
        "values": {
          "default": [
            "order_created"
          ]
        }
      }
    ]
  }'
```

Do not create a standalone controller for an event that has a reusable business-event template. The duplicated business-event component owns the controller, trigger rule, flow event, and event metadata.

## Configure Event Data

Find the reusable `business_event_data` component and duplicate one instance for each field that the event must capture. Install the data components into the business event's `data` socket.

```bash
curl --request POST "$EXTOLE_API_HOST/v1/components/$BUSINESS_EVENT_DATA_TEMPLATE_ID/duplicate" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "target_campaign_id": "$CAMPAIGN_ID",
    "target_component_absolute_name": "/example/conversion",
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

The reusable data component initially derives the source field from its `name`. When the partner field has a distinct name, update `valueExpression` after duplication.

```bash
curl --request PUT "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/components/$DATA_COMPONENT_ID/settings/valueExpression" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "source": "LOCAL",
    "values": {
      "default": "javascript@runtime:context.getCauseEvent().getData()['\''order_id'\'']"
    }
  }'
```

Use a field mapping that matches the partner payload. A commerce integration commonly maps `order_id` to `partner_conversion_id`, an order amount to `cart_value`, and a customer identifier to `partner_user_id`.

Use these key types for the common fields:

| Extole field | Purpose | Key type |
| :----------- | :------ | :------- |
| `partner_conversion_id` | Uniquely identifies the transaction and prevents duplicate outcomes. | `UNIQUE_PARTNER_EVENT_KEY` |
| `partner_user_id` | Identifies the person in the partner system. | `PARTNER_PROFILE_KEY` |
| `cart_value` | Stores the transaction value. | `VALUE` |
| `email`, `first_name`, `last_name` | Identifies and describes the person. | `NONE` |

## Add An Outbound Reward Webhook

Create a reward webhook that calls the partner's coupon or promotion endpoint when a reward is issued.

```bash
curl --request POST "$EXTOLE_API_HOST/v6/webhooks" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "Example Coupon Webhook",
    "type": "REWARD",
    "url": "https://partner.example.com/extole/rewards"
  }'
```

Use a publicly reachable HTTPS URL when creating the webhook. After the reward supplier component is configured, update the webhook URL, request, and response handlers with the required build-time and runtime expressions.

```bash
curl --request PUT "$EXTOLE_API_HOST/v6/webhooks/$WEBHOOK_ID" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "url": "https://partner.example.com/extole/rewards",
    "request": "$REWARD_REQUEST_EXPRESSION",
    "response_handler": "$REWARD_RESPONSE_HANDLER_EXPRESSION"
  }'
```

The partner endpoint should authenticate the request, create or reserve a coupon, and return the coupon code in the response format expected by the configured reward supplier. Verify the response contract with the partner before enabling the webhook.

## Publish The Campaign

Publish only after the component hierarchy, input rules, data mappings, reward supplier, and webhook have been validated.

```bash
curl --request POST "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/publish" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{}'
```

The publish operation validates and builds the campaign. Resolve any validation error before sending production events.

## Verify The Integration

Send a synchronous test event through `POST /v6/events`. Include the campaign program label so the event targets the integration.

```bash
curl --request POST "$EXTOLE_API_HOST/v6/events" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "event_name": "order_created",
    "data": {
      "email": "test@example.com",
      "order_id": "test-order-001",
      "total": 42.50,
      "customer_id": "test-customer-001",
      "labels": "example-integration"
    }
  }'
```

Use the returned `person_id` to list the person's events:

```bash
curl --get "$EXTOLE_API_HOST/v5/persons/$PERSON_ID/steps" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --data-urlencode "stepName=conversion"
```

Confirm that the expected event exists and that its data contains the mapped `partner_conversion_id`, `cart_value`, and `partner_user_id` values. Test every configured inbound event and verify the outbound webhook with a partner test account before enabling production traffic.
