---
title: "OpenCart"
excerpt: "Configure an OpenCart 4.x extension to send order lifecycle events to reusable Extole business events.\n"
---

# Overview

The OpenCart integration sends order lifecycle events from a server-side OpenCart 4.x extension to Extole. Extole maps the partner input events to reusable `converted`, `shipped`, and `canceled` business-event components for attribution, reporting, rules, and program actions.

This integration is inbound-only. It does not create OpenCart coupons and does not include a reward supplier, reward webhook, webhook client key, or reward-supplier socket.

The integration uses OpenCart's publisher-subscriber event system. Read the <Anchor label="OpenCart Events documentation" target="_blank" href="https://docs.opencart.com/developer-guide/events">OpenCart Events documentation</Anchor> before implementing the extension, and verify event routes and listener signatures against the installed OpenCart version.

## Current Component Structure

The Extole integration uses this component model:

```text
root
└── opencart                    integration-v10.0
    ├── opencartStoreUrl
    ├── opencartSetupInstructions
    ├── businessEvents          MULTI_SOCKET → business-event-v10.0
    │   ├── converted
    │   │   ├── triggerRules → input_event
    │   │   └── data → eight business_event_data components
    │   ├── shipped
    │   │   ├── triggerRules → input_event
    │   │   └── data → five business_event_data components
    │   └── canceled
    │       ├── triggerRules → input_event
    │       └── data → five business_event_data components
    └── views                   MULTI_SOCKET → view-v10.0
        └── configuration       config-view-v10.0
```

The configuration view displays the OpenCart store URL and extension setup information. Its status is `IN_PROGRESS` until the store URL is configured.

## Event Contract

The deployed model uses these events:

| OpenCart input event | Extole business event | Reusable template |
| :------------------- | :-------------------- | :---------------- |
| `opencart_order_created` | `converted` | `template_transacted_business_event` |
| `opencart_order_shipped` | `shipped` | `template_tracked_business_event` |
| `opencart_order_canceled` | `canceled` | `template_tracked_business_event` |
| `opencart_order_cancelled` | `canceled` | Legacy input alias only |

Use `opencart_order_canceled` for new implementations. Keep `opencart_order_cancelled` only while an existing sender requires the legacy spelling.

The `opencart_order_created` event creates a `converted` event. Emit it only when the OpenCart order satisfies the program's definition of a valid conversion. If the store creates an order before payment or other qualification is complete, defer this event until the order reaches a configured qualifying status.

## Prerequisites

| Requirement | Description |
| :---------- | :---------- |
| OpenCart 4.x store | Install and enable a server-side extension that can register event listeners and send HTTPS requests. |
| OpenCart administrator access | Install the extension and configure event, status, and credential settings. |
| Extole integration campaign | Publish the OpenCart component structure described on this page. |
| Event-ingestion credential | Use a server-side Extole credential authorized to submit events. Do not use the Client API management token. |
| Current program label | Target events to the integration's active `PROGRAM` label. |
| Order-status mapping | Identify the OpenCart status identifiers that mean converted, shipped, and canceled for this store. |
| HTTPS connectivity | Allow the OpenCart server to reach the Extole Event API. |
| Retry storage | Queue or outbox storage for requests that cannot be delivered immediately. |

OpenCart status identifiers are store configuration. Do not copy numeric identifiers from another OpenCart installation.

## Configure the Extole Integration View

Open the installed OpenCart integration in My Extole and select **Configuration**.

1. Enter the public store base URL in **OpenCart Store URL**.
2. Save the integration.
3. Copy the endpoint, current program label, and event names from **OpenCart Extension Setup**.
4. Open the linked OpenCart documentation before installing the extension.

The integration view does not display or store the event-ingestion secret. Save that credential only in protected server-side OpenCart configuration.

## Create the OpenCart Extension

Create a normal OpenCart extension instead of modifying core files. The extension should contain:

- An administrator configuration page.
- An `install()` method that registers event listeners.
- An `uninstall()` method that removes every registered listener.
- Catalog-side listener methods.
- An order payload mapper.
- A durable queue or outbox.
- A delivery worker with retry and logging.

Store these settings:

| Setting | Purpose |
| :------ | :------ |
| Extole event endpoint | Production is `https://events.extole.io/v6/events`. |
| Event-ingestion credential | Authorizes server-to-server event submission. Store encrypted or in protected server configuration. |
| Program label | Targets events to the installed Extole integration. |
| Store URL | Identifies the OpenCart store. |
| Converted status identifiers | Optional when order creation itself is not a valid conversion. |
| Shipped status identifiers | Statuses that produce `opencart_order_shipped`. |
| Canceled status identifiers | Statuses that produce `opencart_order_canceled`. |
| Request timeout | A short network timeout used by the delivery worker. |
| Retry policy | Backoff and maximum attempts for temporary failures. |

## Register OpenCart Event Listeners

OpenCart event names follow the `namespace/action/stage` convention. Current OpenCart 4.x documentation uses a dot before the model method in the action path.

Register listeners in the extension's administrator-side `install()` method:

```php
<?php
namespace Opencart\Admin\Controller\Extension\Extole\Module;

class Extole extends \Opencart\System\Engine\Controller {
    public function install(): void {
        $this->load->model('setting/event');

        $this->model_setting_event->addEvent([
            'description' => 'Extole order created',
            'code' => 'extole_order_created',
            'trigger' => 'catalog/model/checkout/order.addOrder/after',
            'action' => 'extension/extole/events.onOrderCreated',
            'status' => 1,
            'sort_order' => 1
        ]);

        $this->model_setting_event->addEvent([
            'description' => 'Extole order status changed',
            'code' => 'extole_order_status_changed',
            'trigger' => 'catalog/model/checkout/order.addHistory/after',
            'action' => 'extension/extole/events.onOrderStatusChanged',
            'status' => 1,
            'sort_order' => 1
        ]);
    }

    public function uninstall(): void {
        $this->load->model('setting/event');
        $this->model_setting_event->deleteEventByCode('extole_order_created');
        $this->model_setting_event->deleteEventByCode('extole_order_status_changed');
    }
}
```

OpenCart event APIs have changed across 4.x releases. Confirm all of the following on the target store:

- `addEvent` accepts the object form shown above.
- The model action uses the dot method separator.
- The catalog listener action resolves to the extension class.
- The listener receives route, arguments, and output for an `after` event.

After installation, open **Extensions** > **Events** and confirm both listeners are present and enabled.

## Handle Order Events

An OpenCart `after` listener receives the route, method arguments, and method output:

```php
<?php
namespace Opencart\Catalog\Controller\Extension\Extole;

class Events extends \Opencart\System\Engine\Controller {
    public function onOrderCreated(string &$route, array &$arguments, mixed &$output): void {
        $orderId = (string) $output;
        $this->queueExtoleOrderEvent('opencart_order_created', $orderId);
    }

    public function onOrderStatusChanged(string &$route, array &$arguments, mixed &$output): void {
        $orderId = (string) ($arguments[0] ?? '');
        $orderStatusId = (int) ($arguments[1] ?? 0);

        if ($this->isShippedStatus($orderStatusId)) {
            $this->queueExtoleOrderEvent('opencart_order_shipped', $orderId);
        }

        if ($this->isCanceledStatus($orderStatusId)) {
            $this->queueExtoleOrderEvent('opencart_order_canceled', $orderId);
        }
    }
}
```

Treat this as a listener contract, not a complete extension. Implement `queueExtoleOrderEvent`, status lookup, configuration access, order loading, and delivery using the conventions of the installed OpenCart release.

Do not perform slow remote requests in the event listener. Persist a sanitized event record and let a worker send it to Extole. A temporary Extole or network failure must not fail checkout or prevent an OpenCart order-status transition.

## Map OpenCart Order Statuses

Configure status identifiers instead of comparing localized status names.

Use this decision flow:

1. Load the store's current order statuses.
2. Select one or more statuses that mean the order is a valid conversion.
3. Select one or more statuses that mean the order has shipped or been fulfilled.
4. Select one or more statuses that mean the order is canceled.
5. Reject overlapping mappings unless the store has an explicit reason for them.
6. Test every configured transition.

If order creation already represents a completed, valid transaction, emit `opencart_order_created` from `addOrder`. Otherwise, emit it once when `addHistory` first enters a qualifying converted status.

Persist a delivery marker for each order and Extole input event name. OpenCart can add repeated history records with the same status, and the extension must not enqueue the same lifecycle event repeatedly.

## Build the Event Payload

Send the OpenCart source fields expected by the Extole data components.

### Order Created

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
    "labels": "opencart-integration"
  }
}
```

### Order Shipped

```json
{
  "event_name": "opencart_order_shipped",
  "data": {
    "email": "customer@example.com",
    "first_name": "Alex",
    "last_name": "Morgan",
    "order_id": "10042",
    "customer_id": "customer-9001",
    "labels": "opencart-integration"
  }
}
```

### Order Canceled

```json
{
  "event_name": "opencart_order_canceled",
  "data": {
    "email": "customer@example.com",
    "first_name": "Alex",
    "last_name": "Morgan",
    "order_id": "10042",
    "customer_id": "customer-9001",
    "labels": "opencart-integration"
  }
}
```

Replace `opencart-integration` with the current program label shown in the integration view. The `labels` property belongs inside `data`.

Do not send payment-card data, passwords, session identifiers, or unrelated order metadata.

## Understand the Extole Data Mapping

The `converted` business event captures:

| Extole field | OpenCart source field | Key type |
| :----------- | :-------------------- | :------- |
| `partner_conversion_id` | `order_id` | `UNIQUE_PARTNER_EVENT_KEY` |
| `cart_value` | `total` | `VALUE` |
| `partner_user_id` | `customer_id` | `PARTNER_PROFILE_KEY` |
| `email` | `email` | `NONE` |
| `first_name` | `first_name` | `NONE` |
| `last_name` | `last_name` | `NONE` |
| `coupon_code` | `coupon_code` | `NONE` |
| `store_url` | `store_url` | `NONE` |

The `shipped` and `canceled` business events capture:

- `partner_conversion_id` from `order_id`.
- `partner_user_id` from `customer_id`.
- `email`.
- `first_name`.
- `last_name`.

All fields are implemented with reusable `business_event_data` components. Each source expression reads the matching key from the cause event. No prehandler or custom event controller performs this mapping.

## Send Events Securely

Send events from the OpenCart server:

```bash
curl --request POST "https://events.extole.io/v6/events" \
  --header "Authorization: Bearer $EVENT_INGESTION_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data @event.json
```

Use `/v6/events` during setup when the extension needs a synchronous response for verification. For sustained high-volume delivery, evaluate `/v6/async-events` and update the worker's verification and retry behavior for asynchronous processing.

Protect the integration by:

- Restricting configuration access to OpenCart administrators.
- Keeping the event-ingestion credential out of templates, browser code, logs, and event data.
- Redacting authorization headers in transport logs.
- Validating and normalizing email, identifiers, URLs, and numeric totals.
- Using HTTPS certificate verification.
- Rotating credentials without reinstalling the extension.

## Implement Delivery and Retry

Use an outbox or queue with these fields:

- Local delivery identifier.
- OpenCart order identifier.
- Extole input event name.
- Sanitized payload.
- Attempt count.
- Next-attempt time.
- Last HTTP status and redacted error.
- Delivered time.

Treat `2xx` as accepted. Retry temporary network failures, `429`, and retryable `5xx` responses with bounded exponential backoff. Do not retry permanent authentication or validation failures indefinitely.

Use the combination of order identifier and input event name as the local idempotency key. Extole also receives `order_id` as `partner_conversion_id`, which allows the business event to identify duplicate order outcomes.

## Verify the OpenCart Extension

Test in a non-production OpenCart environment:

1. Install and enable the extension.
2. Confirm both listeners under **Extensions** > **Events**.
3. Save the endpoint, event-ingestion credential, current program label, store URL, and status mappings.
4. Create a qualifying test order.
5. Confirm one queued `opencart_order_created` event.
6. Move the order to each configured shipped status and confirm one `opencart_order_shipped` event.
7. Move a separate order to each configured canceled status and confirm one `opencart_order_canceled` event.
8. Repeat a status transition and confirm the outbox does not create a duplicate delivery.
9. Simulate an Extole timeout and confirm checkout or status changes still succeed.
10. Confirm the worker retries and later marks the event delivered.
11. Confirm logs do not contain the authorization token or sensitive order data.

## Verify the Extole Events

Use the synchronous endpoint for the initial verification:

```bash
curl --request POST "https://events.extole.io/v6/events" \
  --header "Authorization: Bearer $EVENT_INGESTION_ACCESS_TOKEN" \
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
      "labels": "opencart-integration"
    }
  }'
```

Use the returned `person_id` to query the resulting event:

```bash
curl --get "https://api.extole.io/v5/persons/$PERSON_ID/steps" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --data-urlencode "campaign_ids=$CAMPAIGN_ID" \
  --data-urlencode "names=converted"
```

Confirm:

- The event name is `converted`.
- `partner_conversion_id` equals the OpenCart `order_id`.
- `cart_value` equals the OpenCart `total`.
- `partner_user_id` equals the OpenCart `customer_id`.
- Person and order fields match the source payload.
- A repeated `order_id` is handled as a duplicate outcome.

Repeat the test for `opencart_order_shipped` and `opencart_order_canceled`.

## Troubleshooting

### The OpenCart Listener Does Not Run

- Confirm the extension is installed and enabled.
- Confirm the listener appears under **Extensions** > **Events**.
- Check the exact event route and action syntax for the installed OpenCart version.
- Check **System** > **Maintenance** > **Error Logs**.
- Confirm the catalog listener class and method are accessible.

### Extole Accepts the Input but No Business Event Appears

- Confirm the current program label is inside `data.labels`.
- Confirm the input event name matches the configured `input_event` rule.
- Confirm the integration campaign is published.
- Confirm the event contains enough identity data.
- Confirm the data source keys match `order_id`, `total`, and `customer_id`.

### Shipped or Canceled Fires More Than Once

- Use status identifiers rather than names.
- Record one local delivery per order identifier and event name.
- Ignore repeated history entries for a status already delivered.
- Confirm the store does not map the same status to multiple lifecycle events.

### Converted Fires Before Payment

Disable order-created emission from `addOrder`. Configure qualifying converted status identifiers and emit `opencart_order_created` when `addHistory` first reaches one of those statuses.

## Related Documentation

- [Create an Integration With the Client API](doc:client-api-integration)
- <Anchor label="OpenCart Events" target="_blank" href="https://docs.opencart.com/developer-guide/events">OpenCart Events</Anchor>
