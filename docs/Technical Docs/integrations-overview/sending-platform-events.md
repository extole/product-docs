---
title: "Send Platform Events to Extole"
excerpt: "Deliver a platform's lifecycle events to the Extole Events API from a server-side extension, with a durable outbox, retries, and verification.\n"
---

# Overview

An inbound integration has two halves. Inside Extole, an integration campaign maps arriving platform events onto canonical business events — see [Create an Integration with the Management API](doc:management-api-integration). Outside Extole, something in the platform has to send those events. This page is the sending half, and it applies to any platform that can run server-side code: an ecommerce extension, a plugin, a middleware service, or a scheduled job.

Sending happens server-side. An event carries an access token, and any token placed in storefront templates, theme files, or browser code is published to everyone who visits the site. Platforms whose events can only be produced in the browser belong on the JavaScript SDK instead.

## What the Sender Needs

Hold these as configuration rather than constants in code, so a token rotates and a program label changes without a code release:

| Setting | Purpose |
| :------ | :------ |
| Event endpoint | `https://events.extole.io/v6/events` in production. |
| Access Token | A server-side Extole access token, created in the [Security Center](https://my.extole.com/security-center), that authorizes event submission. Store it encrypted or in protected server configuration. Never send events with a token that can also manage campaigns and components. |
| Program label | Targets events at the installed integration. Read the current label from the integration's configuration view. |
| Platform identifier | The store URL, site identifier, or tenant that produced the event. |
| Status or state mapping | The platform's own status identifiers that mean the event happened. |
| Request timeout | A short network timeout for the delivery worker. |
| Retry policy | Backoff and maximum attempts for temporary failures. |

Status identifiers are per-installation configuration on most platforms. Read them from the platform being integrated rather than copying numeric identifiers from another installation, where the same number means something else.

## Do Not Block the Platform's Own Workflow

Send events from a worker, not from the hook that observed them. The hook's job is to persist a sanitized record and return; a separate worker delivers it. An Extole timeout or a network failure must never fail a checkout, block an order-status transition, or slow a page the customer is waiting on.

## Build the Event Payload

An event carries the platform's own event name and a flat `data` object holding the fields the integration maps:

```json
{
  "event_name": "platform_order_created",
  "data": {
    "email": "customer@example.com",
    "first_name": "Alex",
    "last_name": "Morgan",
    "order_id": "10042",
    "total": 42.5,
    "customer_id": "customer-9001",
    "store_url": "https://shop.example.com",
    "labels": "example-integration"
  }
}
```

Two details in that payload are the ones that go wrong. `labels` belongs inside `data`, and it holds the current program label from the integration view rather than a value copied from another account. And every source key is read by name: the integration's data components look for the keys the partner page names, so a renamed key arrives as an event with that field missing rather than as an error.

Send what the integration maps and nothing more. Payment-card data, passwords, session identifiers, and unrelated metadata have no mapped destination and become a liability the moment they are stored.

## Choose the Endpoint

Events go to `https://events.extole.io`, the host the Server to Extole API reference publishes for the event endpoints. Extole's other server-side calls — retrieving a person, reading rewards, and everything in the [Management API](doc:rest-apis) — go to `api.extole.io`, so a sender talks to both hosts. Partner pages that document the earlier `https://api.extole.io/v5/events` path still work and do not need to be changed; point a new sender at `events.extole.io/v6/events`.

Use `/v6/events` while building the sender: it responds synchronously, so the worker can verify what Extole did with each event. For sustained high-volume delivery, evaluate `/v6/async-events` and update the worker's verification and retry behavior for asynchronous processing, since acceptance no longer means the event has been processed.

```bash
curl --request POST "https://events.extole.io/v6/events" \
  --header "Authorization: Bearer $EVENTS_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data @event.json
```

## Deliver Through an Outbox

Queue every event locally before sending it. An outbox record holds:

- A local delivery identifier.
- The platform entity identifier, such as the order or account.
- The platform event name.
- The sanitized payload.
- The attempt count and next-attempt time.
- The last HTTP status and a redacted error.
- The delivered time.

Treat `2xx` as accepted. Retry temporary network failures, `429`, and retryable `5xx` responses with bounded exponential backoff. Do not retry authentication or validation failures indefinitely: those fail identically forever and bury the retryable failures that matter.

Use the entity identifier together with the event name as the local idempotency key. Platforms re-fire hooks and record repeated status history, so a sender without that key delivers the same lifecycle event several times. Extole deduplicates too, on the field mapped as the unique partner event key, but a duplicate suppressed locally never becomes an event someone has to explain.

## Protect the Integration

- Restrict sender configuration to platform administrators.
- Keep the access token out of templates, browser code, logs, and event data.
- Redact authorization headers in transport logs.
- Validate and normalize emails, identifiers, URLs, and numeric values before sending.
- Verify HTTPS certificates.
- Allow token rotation without reinstalling the extension.

## Verify What Arrives

Send one event synchronously and follow it through to the business event it produced. The response returns a `person_id`; read that person's steps for the campaign:

```bash
curl --get "https://api.extole.io/v5/persons/$PERSON_ID/steps" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --data-urlencode "campaign_ids=$CAMPAIGN_ID" \
  --data-urlencode "names=converted"
```

Confirm that the step carries the canonical event name rather than the platform's, that the transaction identifier and value match the source record, that the person keys resolve, and that sending the same source identifier twice produces a duplicate outcome rather than a second conversion. Repeat for every event the integration accepts, not only the first one.

## When Extole Accepts the Event but No Business Event Appears

A `2xx` means the event was accepted, not that it matched anything. Check, in this order:

1. The current program label is inside `data.labels`.
2. The platform event name matches the name on the integration's `input_event` trigger rule exactly.
3. The integration campaign is published.
4. The event carries enough identity data to resolve a person.
5. The source keys match the ones the integration's data components read.

## Related Documentation

- [Integration Categories](doc:integration-categories)
- [Create an Integration with the Management API](doc:management-api-integration)
- [Integrating with Extole](doc:integrating-with-extole)
