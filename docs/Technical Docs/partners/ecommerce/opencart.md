---
title: "OpenCart"
excerpt: "Track order activity from your OpenCart storefront in Extole for attribution, rewarding, reporting, and segmentation.\n"
---

## Overview

Launch programs like Refer A Friend, Drop A Hint, and Welcome Offer on an OpenCart storefront. The Extole and OpenCart integration reports order activity as it happens — orders placed, shipped, and canceled — so your programs can attribute referrals, reward participants at the right moment, and report on the revenue they drive.

The integration is inbound: OpenCart tells Extole what happened in the store. It does not create OpenCart coupons, issue rewards inside the store, or send any data back to OpenCart. Rewards for OpenCart programs are fulfilled by whichever reward supplier your program uses.

OpenCart has no packaged Extole app. Your store sends events through a server-side OpenCart extension that listens to the store's own order events, which means this integration involves a developer once, at setup. Everything after that is configured in My Extole and in the OpenCart admin.

## Prerequisites

| Requirement | Description |
| :---------- | :---------- |
| Extole account | Install and publish the OpenCart integration in your Extole account. |
| OpenCart 4.x store | A store you can install a server-side extension into. |
| OpenCart administrator access | Needed to install the extension and configure its event, status, and credential settings. |
| Developer resource | Someone to build or install the OpenCart extension that sends the events. |
| Event-ingestion credential | A server-side Extole credential authorized to submit events, generated in the [Security Center](https://my.extole.com/security-center). Do not use a Client API management token. |
| Order-status decisions | The OpenCart statuses that mean an order is converted, shipped, and canceled in your store. |
| HTTPS connectivity | The OpenCart server must be able to reach the Extole Event API. |

## Integration

### Step 1: Configure the Extole Integration

Open the installed OpenCart integration in My Extole and select **Configuration**.

1. Enter your public store base URL in **OpenCart Store URL**.
2. Save the integration.
3. Copy the endpoint, current program label, and event names from **OpenCart Extension Setup**. Your extension needs all three.

The integration view never displays or stores the event-ingestion credential. Keep that secret only in protected server-side OpenCart configuration.

### Step 2: Install the OpenCart Extension

Install the events as a normal OpenCart extension rather than by editing core files, so an OpenCart upgrade does not silently remove your integration. The extension registers two listeners against the store's publisher-subscriber event system:

| OpenCart trigger | What it observes |
| :--------------- | :--------------- |
| `catalog/model/checkout/order.addOrder/after` | A new order was created. |
| `catalog/model/checkout/order.addHistory/after` | An order moved to a new status. |

Register both in the extension's `install()` method and remove both in `uninstall()`. After installing, open **Extensions** > **Events** in the OpenCart admin and confirm that both listeners are present and enabled.

OpenCart's event APIs and route syntax have changed across 4.x releases, so verify the trigger paths, the listener signature, and the registration call against the release your store runs. The <Anchor label="OpenCart Events documentation" target="_blank" href="https://docs.opencart.com/developer-guide/events">OpenCart Events documentation</Anchor> is the reference for both.

For how the extension should deliver events — the payload, the credential, the outbox, retries, and verification — see [Send Platform Events to Extole](doc:sending-platform-events).

### Step 3: Map Your Order Statuses

OpenCart status identifiers are store configuration, and the same number means different things in different stores. Configure identifiers rather than comparing localized status names, and take them from this store:

1. Load the store's current order statuses.
2. Choose the statuses that mean the order is a valid conversion.
3. Choose the statuses that mean the order shipped or was fulfilled.
4. Choose the statuses that mean the order was canceled.
5. Avoid mapping one status to more than one lifecycle event unless you have a reason to.
6. Test every configured transition.

If creating an order in your store already represents a completed, valid purchase, report the conversion from order creation. If your store creates orders before payment or another qualification completes, report it instead when the order first reaches a qualifying status — otherwise programs reward purchases that were never paid for.

### Step 4: Verify the Integration

Test in a non-production OpenCart store before going live:

1. Confirm both listeners under **Extensions** > **Events**.
2. Create a qualifying test order and confirm one order-created event.
3. Move an order to each configured shipped status and confirm one shipped event.
4. Move a separate order to each configured canceled status and confirm one canceled event.
5. Repeat a status transition and confirm no duplicate is delivered.
6. Simulate an Extole timeout and confirm checkout and status changes still succeed.

Then confirm what Extole recorded, as described in [Send Platform Events to Extole](doc:sending-platform-events).

## Event Contract

Each OpenCart event becomes one reusable Extole business event:

| OpenCart event | Extole business event | Notes |
| :------------- | :-------------------- | :---- |
| `opencart_order_created` | `converted` | Carries the order total as the transaction value. |
| `opencart_order_shipped` | `shipped` | Fulfillment milestone. |
| `opencart_order_canceled` | `canceled` | Cancellation milestone. |
| `opencart_order_cancelled` | `canceled` | Legacy spelling, accepted as an input alias only. |

Use `opencart_order_canceled` for new implementations, and keep the double-l spelling only while an existing sender depends on it.

## Data Parameters

Extole reads these OpenCart fields by name from the event, so send them exactly as spelled. A renamed key arrives as an event with that field missing.

| Extole field | OpenCart field | Role |
| :----------- | :------------- | :--- |
| `partner_conversion_id` | `order_id` | Identifies the transaction and deduplicates repeated outcomes for the same order. |
| `cart_value` | `total` | The order value used for revenue reporting and value-based rewards. |
| `partner_user_id` | `customer_id` | Identifies the customer in your store. |
| `email` | `email` | Person identity. |
| `first_name` | `first_name` | Person detail. |
| `last_name` | `last_name` | Person detail. |
| `coupon_code` | `coupon_code` | The code used on the order, when one was. |
| `store_url` | `store_url` | Identifies the store that produced the event. |

The shipped and canceled events carry the order identifier, the customer identifier, and the person's name and email. They do not carry a value, because the value was already reported at conversion.

## Troubleshooting

### The OpenCart Listener Does Not Run

- Confirm the extension is installed and enabled.
- Confirm the listener appears under **Extensions** > **Events**.
- Check the trigger path and action syntax against the installed OpenCart release.
- Check **System** > **Maintenance** > **Error Logs**.
- Confirm the catalog listener class and method are reachable.

### Shipped or Canceled Is Reported More Than Once

- Map statuses by identifier rather than by name.
- Record one delivery per order and event name.
- Ignore repeated history entries for a status already reported.
- Confirm the store does not map one status to two lifecycle events.

### Conversions Are Reported Before Payment

Stop reporting the conversion from order creation. Configure the statuses that qualify as a conversion and report it when an order first reaches one of them.

### Extole Accepts the Event but Nothing Appears in the Program

The event was accepted without matching the integration. Work through the checklist in [Send Platform Events to Extole](doc:sending-platform-events), starting with the program label.

## Related Documentation

- [Send Platform Events to Extole](doc:sending-platform-events)
- [Integration Categories](doc:integration-categories)
- [Create an Integration With the Client API](doc:client-api-integration)
- [Map Inbound Partner Events](doc:integration-inbound-events)
- <Anchor label="OpenCart Events" target="_blank" href="https://docs.opencart.com/developer-guide/events">OpenCart Events</Anchor>
