---
title: "Configurable Report Types and Their Entities"
slug: configurable-report-types-and-their-entities
excerpt: "Which configurable report type to submit for each entity or event type, whether it supports records or metrics, and how to reach related entities from it.\n"
hidden: false
---

# Overview

Extole's configurable reporting framework has a fixed set of report types, each built on one primary entity — the record accessed as `event.*` in that report's [mapping expressions](doc:custom-data-queries-using-extole-reports). This page maps every configurable report type to its primary entity and tells you where that entity's fields are documented. For expression syntax, see [Custom Data Queries using Extole Reports](doc:custom-data-queries-using-extole-reports); for entity field references, see [Entities and Context Available in Extole's Configurable Reporting System](doc:entities-and-context-available-in-extole-s-configurable-reporting-system).

A report type is either a **records** report (one row per entity) or a **metrics** report (grouped counts/rates/sums over an entity, using `GROUP_*` mapping functions). Some entities back both a records and a metrics report type.

# Report Types by Entity

| Report type | Records or metrics | Primary entity (`event.*`) | Metrics property key |
| --- | --- | --- | --- |
| Events | Records | StepRecord | — |
| Metrics (`CONFIGURABLE_EVENT_METRICS`) | Metrics | StepRecord | `step_name` |
| Input Records | Records | InputRecord | — |
| Input Record Metrics | Metrics | InputRecord | `name` |
| Person | Records | Person | — |
| Rewards | Records | Reward event | — |
| Reward Metrics | Metrics | Reward event | — |
| Audience Memberships | Records | AudienceMembershipRecord | — |
| Audience Memberships Metrics | Metrics | AudienceMembershipRecord | — |
| Client Event Metrics | Metrics | ClientEvent | — |
| Message Metrics | Metrics | MessageSummary | — |
| Webhook Events | Records | WebhookEvent | — |
| Webhook Event Metrics | Metrics | WebhookEvent | — |
| Webhook Dispatch Results | Records | WebhookDispatchResultEvent | — |
| Webhook Dispatch Result Metrics | Metrics | WebhookDispatchResultEvent | — |

A blank metrics property key means the report type's `GROUP_*` mapping functions don't require a data-source property argument (unlike `step_name` for Metrics or `name` for Input Record Metrics) — see [Aggregation Functions](doc:custom-data-queries-using-extole-reports) for the full syntax.

**Rewards and Reward Metrics** report types run against the raw reward event, not the aggregated `RewardSummary` object — most reward questions are answered by joining to the full reward lifecycle with `reward(event.data.reward_id)`, documented under [RewardSummary](doc:entities-and-context-available-in-extole-s-configurable-reporting-system).

# Accessing Other Entities From a Report

Beyond its primary entity, any report type can reach related entities through join functions — `PERSON(personId)`, `CAMPAIGN(campaignId)`, `REWARD(rewardId)`, `CLIENT(clientId)`, and others documented in [Entity Lookup Functions](doc:custom-data-queries-using-extole-reports). For example, an Events report's primary entity is StepRecord, but a mapping on that report can still load the person's email with `PERSON(event.personId).email` or the campaign name with `CAMPAIGN(event.campaignId).campaignName`.

The five entities added to this reference for the report types above — AudienceMembershipRecord, MessageSummary, WebhookEvent, WebhookDispatchResultEvent, and ClientEvent — have **no join function**. Each is reachable only as `event.*` on its own report type, not as a lookup from another report's primary entity.

# Recommended, Pre-Built Reports

The report types on this page are the building blocks for **configurable** reports, where you write your own `mappings` and `filters`. Extole also offers pre-built, named reports for common questions — see [Report Types](doc:report-types) for the recommended reports catalog (advocate, rewards, and acquisition reports you can run without writing mapping expressions).
