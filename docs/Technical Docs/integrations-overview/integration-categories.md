---
title: "Integration Categories"
excerpt: "Place a partner platform in an integration category — inbound, outbound, or bidirectional — before building the integration.\n"
---

# Overview

An integration is a campaign whose component tree connects Extole to an outside system. Every integration belongs to a category, and the category decides the component model, the resources the integration needs, and which build sequence to follow in [Create an Integration With the Client API](doc:client-api-integration).

Two questions place any platform:

1. Does the platform send activity to Extole? The integration is inbound.
2. Does Extole send activity to the platform? The integration is outbound.

Answer both before creating anything. A platform that only receives Extole activity needs no business events, and a platform that only sends activity needs no webhooks or credentials.

## Category Summary

| Category | Direction | Platform types | What you create |
| :------- | :-------- | :------------- | :-------------- |
| Inbound | Platform to Extole | Commerce, core banking, account opening, subscription, point of sale | A campaign built from the custom integration template, with business events, trigger rules, data capture, and a configuration view |
| Outbound | Extole to platform | Marketing automation, messaging, customer data platforms, analytics | A duplicate of the maintained library source, reshaped to the finished shape on the partner page, with webhooks and a credential |
| Bidirectional | Both | Commerce and loyalty platforms that also accept rewards or coupons | The inbound model first, then outbound resources gated on an approved use case |

## Inbound Integrations

An inbound integration turns a platform's own event names into canonical Extole business events. The platform posts to the Event API from a server-side extension, a middleware service, or a file feed, and Extole maps each arriving event to a reusable business-event component.

Two vocabularies meet here and must not be conflated. The platform's wire event name belongs on the trigger rule that listens for it. The business event carries the canonical name the rest of the platform already understands — `converted`, `shipped`, `canceled`, `account_opened`, and the other names bundled programs use. Never rename a business event to match a platform's wire name.

Data capture is the integration. A business event with an empty `data` socket produces an event with no transaction identifier, no person key, and no value, so nothing downstream can deduplicate, attribute, reward, or report on it.

An inbound integration contains:

```text
root
└── integration                 integration-v10.0
    ├── partner configuration settings
    ├── businessEvents          MULTI_SOCKET → business-event-v10.0
    │   └── canonical event
    │       ├── triggerRules    → input_event rule carrying the platform's event names
    │       └── data            → one component per captured field
    └── views                   MULTI_SOCKET → view-v10.0
        └── configuration       config-view-v10.0
```

Inbound integrations need no reward supplier, webhook, or client key. Creating those resources for completeness leaves credentials and unused resources that someone later has to reconcile.

## Outbound Integrations

An outbound integration forwards Extole program activity to the platform. Child controllers listen for Extole events and call the platform's endpoints through webhooks, authenticated with a webhook client key that holds the platform's API credential.

Most outbound platforms ship as maintained library sources that an account can duplicate, which is the same action the Install button performs on the Partners page. The install is the starting point, not the finished integration: the library carries defaults for every account, while the partner page defines the finished shape for this platform — which forwarded events apply, which endpoints the integration calls, which settings hold credentials, and any reusable data template that marketing campaigns attach.

An outbound integration contains:

```text
root
└── integration                 integration-v10.0
    ├── one child per forwarded Extole event
    └── data-item template      partner data component type (when marketing campaigns attach partner actions)
```

The partner page's product description is the specification for that tree. The activity it says the integration forwards is the complete set of children, the endpoints it says Extole calls are the complete set of webhooks, and a statement that program campaigns attach partner data to their events means the integration carries a typed data template. A library source ships the union of what every account might want, so the install usually has more children and fewer webhooks than the finished integration.

Alongside the tree, the integration owns one webhook per platform endpoint. Each webhook is tagged by purpose, and the integration component holds a `WEBHOOK_ID` setting per webhook whose buildtime expression resolves the webhook by that tag. Marketing campaigns attach partner actions through those settings rather than by webhook identifier.

Outbound integrations do not replace a marketing program's business events. Installing one never supersedes a program's `converted` or `shipped` event, because the integration reports activity rather than producing it.

## Bidirectional Integrations

A platform that both sends outcomes and receives rewards or coupons combines the two models. Build the inbound half first and prove it, then add outbound resources only when the destination endpoint, authentication contract, retry and idempotency behavior, configuration surface, and a program action that produces the outbound event all exist.

A reward-supplier socket does not connect a platform. A reward supplier models fulfillment inventory or behavior, and a webhook is the HTTP transport. Creating either without the rest of the program wiring produces configuration that looks complete and does nothing.

## Placing a New Platform

Read the platform's own developer documentation and the partner page in this documentation set, when one exists, before choosing. Signals that place a platform quickly:

| Signal | Category |
| :----- | :------- |
| The platform documents webhooks, plugins, or extensions that post order or account activity | Inbound |
| The request describes a lifecycle to track — purchases, shipments, cancellations, account openings | Inbound |
| The platform documents an ingestion API for customer events, attributes, or subscriptions | Outbound |
| The request describes triggering messages, syncing audiences, or enriching profiles from Extole activity | Outbound |
| A maintained `integration-v10.0` component already exists for the platform in the duplicatable listing | Outbound library install, unless the request adds inbound scope |

Discovery decides the category, not habit. Rebuilding a maintained outbound platform from the custom integration template produces a campaign that looks related and performs none of the platform's webhook or credential work.

## Related Documentation

- [Create an Integration With the Client API](doc:client-api-integration)
- [Integrating with Extole](doc:integrating-with-extole)
- [Key Concepts](doc:key-concepts)
