---
title: "OpenCart"
excerpt: "Connect OpenCart order events to Extole business events and create OpenCart coupons from Extole rewards.\n"
---

## Overview

The OpenCart integration connects OpenCart order activity to reusable Extole business events. An OpenCart extension sends order events to Extole, where they can drive attribution, reporting, rewards, and audience rules. Extole reward webhooks send earned rewards back to an OpenCart coupon endpoint.

The integration uses OpenCart's event system. Configure subscribers for the order-created, order-shipped, and order-canceled lifecycle events. See the [OpenCart events documentation](https://docs.opencart.com/developer-guide/events) for the event publisher and subscriber model.

## Prerequisites

| Requirement | Description |
| :---------- | :---------- |
| OpenCart 4.x store | Install an extension that can subscribe to OpenCart events and make outbound HTTPS requests. |
| Extole account | Create or access the Extole program that will use the integration. |
| Extole Client API token | Use a server-side token with permission to create and publish campaigns and components. |
| OpenCart extension route | Provide a server-side route that authenticates Extole reward webhook requests and creates coupons. |
| HTTPS connectivity | Allow the OpenCart server to reach the Extole API and allow Extole to reach the coupon route. |

## Use Cases

- Track a purchase when an OpenCart order is created.
- Trigger post-purchase rewards after an order ships.
- Record a canceled order so program rules can exclude or reverse a pending outcome.
- Create a single-use OpenCart coupon when a participant earns a reward.
- Use order and customer data for reporting and audience rules.

## Integration

Create the integration with the [Client API integration guide](doc:client-api-integration), then apply the OpenCart-specific values below.

### Step 1: Create The Inbound Event Adapter

Create an OpenCart extension that subscribes to the lifecycle events relevant to your program. The adapter should:

1. Read the OpenCart event payload.
2. Select the event name `opencart_order_created`, `opencart_order_shipped`, or `opencart_order_cancelled`.
3. Send the event to `POST /v6/events`.
4. Include the OpenCart fields in the request `data` object.
5. Include the Extole program label in `labels`.

Use the following event contract:

| Extole event | OpenCart lifecycle | Business event template |
| :----------- | :----------------- | :----------------------- |
| `opencart_order_created` | Order created | `template_transacted_business_event` |
| `opencart_order_shipped` | Order shipped or fulfilled | `template_tracked_business_event` |
| `opencart_order_cancelled` | Order canceled | `template_tracked_business_event` |

Send the purchase event with the fields required by the conversion business event:

```json
{
  "event_name": "opencart_order_created",
  "data": {
    "email": "customer@example.com",
    "first_name": "Alex",
    "last_name": "Morgan",
    "order_id": "10042",
    "total": 42.5,
    "customer_id": "customer-9001",
    "coupon_code": "WELCOME10",
    "store_url": "https://shop.example.com",
    "labels": "example-integration"
  }
}
```

Send the shipment and cancellation events with `order_id`, `customer_id`, and the person fields available in the OpenCart payload.

### Step 2: Configure The Extole Event Mapping

Create one reusable business-event instance for each OpenCart lifecycle event. Configure the instances as follows:

| Extole data field | OpenCart source field | Key type |
| :---------------- | :-------------------- | :------- |
| `partner_conversion_id` | `order_id` | `UNIQUE_PARTNER_EVENT_KEY` |
| `cart_value` | `total` | `VALUE` |
| `partner_user_id` | `customer_id` | `PARTNER_PROFILE_KEY` |
| `email` | `email` | `NONE` |
| `first_name` | `first_name` | `NONE` |
| `last_name` | `last_name` | `NONE` |
| `coupon_code` | `coupon_code` | `NONE` |
| `store_url` | `store_url` | `NONE` |

Use the transacted template for `conversion` and the tracked template for `ship` and `return`. Duplicate the reusable `input_event` rule into each event's `triggerRules` socket:

```json
{
  "name": "triggerEventNames",
  "type": "STRING_LIST",
  "values": {
    "default": [
      "opencart_order_created"
    ]
  }
}
```

Duplicate a reusable `business_event_data` component into the `data` socket for each field. When the OpenCart field name differs from the Extole field name, set the data component's `valueExpression` to the source field:

```json
{
  "source": "LOCAL",
  "values": {
    "default": "javascript@runtime:context.getCauseEvent().getData()['order_id']"
  }
}
```

Apply the equivalent mappings for `total` and `customer_id`. Do not create custom controllers for these events. The reusable event component supplies the controller and its event metadata.

### Step 3: Create The Reward Webhook

Create a `REWARD` webhook with a publicly reachable HTTPS URL. The URL should point to an OpenCart extension route that accepts an authenticated reward request.

```json
{
  "name": "OpenCart Coupon Webhook",
  "type": "REWARD",
  "url": "https://shop.example.com/extension/example/reward"
}
```

Configure the OpenCart route to:

1. Verify the webhook authentication.
2. Validate the reward identifier and recipient.
3. Create a unique coupon code using OpenCart's coupon model or service.
4. Apply the configured discount, usage limit, expiration, and product restrictions.
5. Return the coupon code and the creation status.

Make coupon creation idempotent. Use the Extole reward or webhook event identifier as the idempotency key so a retry does not create multiple coupons for the same reward.

### Step 4: Configure And Publish The Campaign

Validate the component tree before publishing:

- The integration component contains the `businessEvents` multi-socket.
- The `conversion`, `ship`, and `return` components are installed in that socket.
- Each business event has an `input_event` rule in `triggerRules`.
- Each event has the expected data components in `data`.
- The reward supplier references the `REWARD` webhook.

Publish the campaign with `POST /v2/campaigns/{campaign_id}/publish`. Test the campaign in a non-production environment before enabling production traffic.

## Verify The Integration

Send a test `opencart_order_created` event through `POST /v6/events`:

```bash
curl --request POST "https://api.extole.io/v6/events" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "event_name": "opencart_order_created",
    "data": {
      "email": "test@example.com",
      "first_name": "OpenCart",
      "last_name": "Test",
      "order_id": "test-order-001",
      "total": 42.50,
      "customer_id": "test-customer-001",
      "coupon_code": "TEST10",
      "store_url": "https://shop.example.com",
      "labels": "example-integration"
    }
  }'
```

Use the returned `person_id` to query the person's events with `GET /v5/persons/{person_id}/steps`. Confirm that the `conversion` event contains:

- `partner_conversion_id` with the OpenCart `order_id`.
- `cart_value` with the OpenCart `total`.
- `partner_user_id` with the OpenCart `customer_id`.
- The person and order fields required by the program.

Repeat the test with `opencart_order_shipped` and `opencart_order_cancelled`. Finally, trigger a test reward and confirm that the OpenCart route creates one coupon and returns the expected response.
