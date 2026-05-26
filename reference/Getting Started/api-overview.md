---
title: API Overview
excerpt: >-
  Start with the right Extole API, authenticate your request, and make your
  first call.
hidden: false
---
Extole is the incentive operating system for enterprises. It is an event-driven platform that orchestrates offers, rewards, and incentive-driven customer journeys across programs, channels, and systems.

The platform ingests behavioral events from web, mobile, servers, batch systems, and integrations; runs them through a configurable rules and journey engine; resolves participant identity; issues rewards across the supported reward types; and reports on the outcome. These capabilities are exposed across three REST APIs:

- [Integration: Server to Extole](#integration-server-to-extole). Backend services submit events, manage persons, drive the reward lifecycle, render zones server-side, and run bulk data operations.
- [Integration: Consumer to Extole](#integration-consumer-to-extole). Browser and native-app surface; backs the Extole JavaScript and mobile SDKs.
- [Management API](#management-api). Configures campaigns, audiences, reward suppliers, and reports. Most operations available in the My Extole UI are reachable here as well.

## Architecture

Extole is event-driven. Behavioral events drive eligibility decisions, reward issuance, and updated participant profiles. Updated profiles feed back into the platform on the next event.

```
  Events  (API, JS SDK, Mobile SDKs, Files, Integrations)
     │
     ▼
  Campaigns  (Audiences, Targeting)
     │
     ▼
  Rules  (Quality, Time, Action)
     │
     ▼
  Rewards  (Points, Cash, Gift Cards, ...)
     │
     ▼
  Profile  (Status, Stats, History)
     │
     └─────► fed back into Campaigns for eligibility,
             targeting, and engagement on the next event
```

Events arrive from anywhere a participant touches the brand. Campaigns evaluate the event against an audience and the configured targeting. Rules and journey logic apply eligibility, quality, time, fraud, and action constraints. Rewards are issued, fulfilled, and tracked. The participant profile records the outcome and feeds the next event.

## Concepts

### Events

Behavioral signals published to Extole. Each event has a name and a data payload. Common types include conversion events (purchase, signup, subscribe), engagement events (share, click, open, view), and lifecycle events (refund, cancellation, account\_created). Brands can also define additional events or import events from other platforms.

### Campaigns

Configured incentive programs. A campaign packages its target audience, participant journeys, rules that govern eligibility and limits, and the actions Extole takes (rewards, emails, webhooks, rendered content). Brands run multiple campaigns at once. Campaigns can be launched, tested, and revised, either through the UI at my.extole.com or programmatically via the API.

### Rules

The configurable logic Extole applies to every event flowing through a campaign. Eligibility rules decide who can participate (audience membership, geographic limits, identity status, exclusion lists). Quality rules decide whether an event is legitimate (velocity checks, self-referral detection, fraud signals, device and identity checks). Time rules govern when an event counts (conversion windows, campaign dates, cooldowns, reward expiration). Action rules decide what happens next (reward issuance, reward tier, frequency limits, downstream messaging). Rules are configured per campaign in My Extole without engineering work.

### Rewards

Anything of value Extole grants, fulfills, redeems, cancels, or revokes for a participant. Supported types include gift cards, coupons, credits, points, cashback, and custom rewards fulfilled through the brand's own systems. Each reward moves through a state lifecycle (earned, fulfilled, redeemed) with terminal states for cancellations, failures, and revocations. Extole integrates with external fulfillment providers and exposes the full state history for monitoring and reporting.

### Persons

Extole's unified participant identity across channels (web, app, email, brand systems) and across roles. A single Person can be an advocate in one campaign, a friend in another, and a loyalty member in a third, simultaneously. The Person carries the consolidated identity, activity history, audience memberships, rewards, and relationships.

## The APIs

### Integration: Server to Extole

A REST API called from a brand's backend services. Covers event submission, person and reward management, server-side zone rendering, and bulk data operations through batches, files, and SFTP.

See the [Integration: Server to Extole reference](https://docs.extole.com/reference/getcurrentclientaccesstoken).

### Integration: Consumer to Extole

A REST API called from a brand's website and native apps; backs the Extole JavaScript and mobile SDKs. Covers event submission, consumer profile and reward access, and zone rendering on the participant's device. Uses consumer access tokens managed automatically by cookie or by the SDKs, distinct from the bearer access tokens used by the server-side APIs.

See the [Integration: Consumer to Extole reference](https://docs.extole.com/reference/getconsumertoken).

### Management API

A REST API for configuring the platform. Most operations available in the My Extole UI are reachable here as well.

See the [Management API reference](https://docs.extole.com/reference/listaudiences).
