---
title: "Entities and Context Available in Extole's Configurable Reporting System"
slug: entities-and-context-available-in-extole-s-configurable-reporting-system
excerpt: "Reference for the entities and fields available in Extole's configurable reporting system, and how to access them in report mappings.\n"
hidden: false
intercom_source_id: 15433113
---

# Overview

Use this document alongside [Custom Data Queries using Extole Reports](doc:custom-data-queries-using-extole-reports), which covers expression syntax and functions.

In a report mapping, the primary row record is accessed as `event.*`. Which entity that is depends on the report type.

# StepRecord

**Used in:** Events, Metrics reports · **Access:** `event.*`

One step in the referral lifecycle recorded on a person's profile. Examples: a share, a click, a conversion, a reward earned. Steps carry quality signals, attribution, and device context on top of the raw event data.

| Field | Description |
| --- | --- |
| `id` | Step record ID |
| `clientId` | Client that owns this record |
| `personId` | Person who performed the step |
| `name` | Step name — e.g. `converted`, `shared`, `signup` |
| `primaryStepName` | Primary name, excluding aliases |
| `eventTime` | When the step occurred |
| `requestTime` | When the request was received |
| `programLabel` | Program this step belongs to |
| `campaignId` | Campaign context (may be null) |
| `container` | Environment container — e.g. `production` |
| `quality` | Quality signal: `HIGH`, `LOW`, etc. |
| `visitType` | `NEW_TO_CLIENT`, `EXISTING_CLIENT`, `NORMAL`, etc. |
| `attribution` | `ALL`, `REFERRED`, `NOT_REFERRED`, etc. |
| `firstSiteVisit` | Whether this was the person's first site visit |
| `rootEventId` | Root event in the causal chain |
| `journeyName` | Journey this step belongs to (may be null) |
| `variant` | A/B test variant (may be null) |
| `deviceType` | Mobile, Desktop, Other |
| `deviceOs` | Operating system |
| `appType` | `WEB`, `MOBILE`, etc. |
| `data` | Custom key-value data on the step |

Common data keys: `amount`, `source`, `channel`, `locale`, `country`, `partner_user_id`, `api_type`.

**Mapping examples:**

```
# Basic fields
Id=event.id; Person=event.personId; Step=event.name; Amount=event.data.amount;

# Keys that contain dots must be quoted
Share Message=event.data."share.message";

# Null-safe data field
Amount=default(event.data.amount, value:"0");

# Filter to high-quality referred conversions
# (in Filters parameter)
event.quality=="HIGH";event.visitType=="NEW_TO_CLIENT"
```

In a **Metrics** report, `step_name` scopes the aggregation to a specific step:

```
Unique Converters=group_count_distinct(event.personId, step_name:"converted"); Total Revenue=group_sum(event.data.amount, step_name:"converted", quality:"HIGH");
```

# InputRecord

**Used in:** Input Records, Input Record Metrics reports · **Access:** `event.*`

A raw inbound event from a client integration, before it is processed into a step. Captures the original payload and the device and network context at request time.

| Field | Description |
| --- | --- |
| `id` | Input record ID |
| `clientId` | Client that owns this record |
| `personId` | Person associated with the event |
| `name` | Event name — e.g. `purchase`, `signup` |
| `eventTime` | When the event occurred |
| `requestTime` | When the request was received |
| `container` | Environment container |
| `locale` | Locale at event time |
| `apiType` | API access method |
| `userId` | Client-side user identifier (may be null) |
| `userAgent` | Browser or client user-agent string (may be null) |
| `ipAddress` | Client IP address (may be null) |
| `deviceType` | Device type |
| `deviceOs` | Operating system |
| `appType` | Application type |
| `data` | Custom key-value payload from the client |
| `httpHeaders` | HTTP headers from the inbound request |

**Mapping examples:**

```
# Basic fields
Event Name=event.name; API Type=event.apiType; Device=device_type(user_agent:event.userAgent); OS=device_type(user_agent:event.userAgent, mode:"OS_TYPE");

# Count all input events by name in an Input Record Metrics report
name=event.name; api_type=event.apiType; count=group_count_distinct(event.id, name:"all");

# Count a specific event per person per day
day=end_date(event.eventTime, period:"DAY"); person_id=person(event.personId).id; count=group_count_distinct(event.id, name:"purchase");
```

# Person

**Function:** `person(personId)` · e.g. `person(event.personId).email`

The full profile for one participant. A person accumulates steps, rewards, and referral relationships over time. Use the `PERSON_COLLECTION` function to filter and aggregate data from the collection fields.

| Field | Description |
| --- | --- |
| `id` | Internal person ID |
| `email` | Email address |
| `normalizedEmail` | Lowercased, normalized email |
| `firstName` | First name |
| `lastName` | Last name |
| `locale` | Preferred locale |
| `partnerUserId` | External user ID from the client |
| `blocked` | Whether this person is blocked from participating |
| `data` | Custom person-level data |
| `steps` | All steps recorded on this profile (`PersonStep[]`) |
| `rewards` | All rewards linked to this profile (`PersonReward[]`) |
| `shareables` | Referral links owned by this person (`Shareable[]`) |
| `journeys` | Journey participation records (`PersonJourney[]`) |
| `recentAssociatedFriends` | Friends this person has referred (`PersonReferral[]`) |
| `recentAssociatedAdvocates` | Advocates who referred this person (`PersonReferral[]`) |
| `audienceMemberships` | Audience segments this person belongs to |
| `recentRequestContexts` | Recent device and geo snapshots (`RequestContext[]`) |

**Mapping examples:**

```
# Basic person fields
Email=person(event.personId).email; First Name=person(event.personId).firstName; Last Name=person(event.personId).lastName; Partner ID=person(event.personId).partnerUserId;

# Custom person data
Tier=person(event.personId).data.tier;
```

Use `person_collection` to aggregate from profile collections. It is more memory-efficient than `collection` for large profiles.

```
# Count converted steps on the profile
Conversions=person_collection(person(event.personId).id, collection:"steps", filter:stepName=="converted", extracting:eventId, reduce:"count");

# Sum high-quality conversion values
Total Value=person_collection(person(event.personId).id, collection:"steps", filter:stepName=="converted" and quality=="HIGH", extracting:value, reduce:"sum");

# Count primary (non-alias) steps only
Primary Steps=person_collection(person(event.personId).id, collection:"steps", filter:aliasName=="false", extracting:eventId, reduce:"count");
```

Use `FIRST` or `LAST` with `sortBy` to extract a single step:

```
# Campaign of the person's first application step
hidden(first_app)=FIRST(COLLECTION(PERSON(event.personId).steps, filter:stepName=="application_started"), sortBy:"createdDate"); First App Campaign=campaign(property(first_app).campaignId).campaignName;
```

# PersonStep

One step on the person's timeline, accessible via `person.steps`.

| Field | Description |
| --- | --- |
| `stepName` | Step name |
| `eventDate` | When the step occurred |
| `createdDate` | When the record was persisted |
| `campaignId` | Campaign context |
| `programLabel` | Program label |
| `eventId` | Consumer event ID for this step |
| `rootEventId` | Root event ID |
| `quality` | Quality signal |
| `value` | Numeric value attached to the step |
| `aliasName` | Whether this step name is an alias |
| `container` | Environment container |
| `journeyName` | Journey name |
| `data` | Step-level custom data |

# PersonReward

One reward on the person's profile, accessible via `person.rewards`.

| Field | Description |
| --- | --- |
| `rewardId` | Platform reward ID |
| `name` | Reward slot name |
| `personRole` | `advocate`, `friend`, etc. |
| `faceValue` | Reward face value |
| `faceValueType` | `POINTS`, `CREDIT`, `COUPON_CODE`, etc. |
| `state` | Current reward state |
| `dateEarned` | When the reward was earned |
| `rewardSupplierId` | Supplier ID |
| `campaignId` | Campaign context |
| `programLabel` | Program label |
| `expiryDate` | Expiry date (may be null) |
| `data` | Custom reward data |

# PersonReferral

One referral relationship, accessible via `person.recentAssociatedFriends` or `person.recentAssociatedAdvocates`.

| Field | Description |
| --- | --- |
| `otherPersonId` | The other person in this referral pair |
| `mySide` | This person's role in the relationship |
| `reason` | How the referral was established |
| `createdDate` | When the referral was established |
| `displaced` | Whether this referral was replaced by a later one |
| `container` | Environment container |

# RequestContext

One device and geo snapshot, accessible via `person.recentRequestContexts`.

| Field | Description |
| --- | --- |
| `deviceId` | Device fingerprint ID |
| `createdAt` | When this snapshot was captured |
| `geoIp.ipAddress` | IP address |
| `geoIp.country.isoCode` | Country ISO code |
| `geoIp.country.name` | Country name |
| `geoIp.state.isoCode` | State ISO code |
| `geoIp.state.name` | State name |
| `geoIp.city.name` | City name |
| `geoIp.zipCode` | Postal code |

**Mapping example:**

```
# Last known zip code and city for the person
Zip=LAST(COLLECTION(PERSON(event.personId).recentRequestContexts), sortBy:createdAt).geoIp.zip_code; City=LAST(COLLECTION(PERSON(event.personId).recentRequestContexts), sortBy:createdAt).geoIp.city.name;
```

# BuiltCampaign

**Function:** `campaign(campaignId)` · e.g. `campaign(event.campaignId).campaignName`

The latest published state of a campaign. Use this when you need the current name, state, or dates as of the most recent publish.

| Field | Description |
| --- | --- |
| `campaignId` | Campaign ID |
| `campaignName` | Display name |
| `programLabel` | URL-safe program slug |
| `programType` | Program type |
| `description` | Campaign description |
| `currentState` | `LIVE`, `PAUSED`, `STOPPED`, `ARCHIVED`, `ENDED`, `DRAFT` |
| `startDate` | Scheduled start date |
| `stopDate` | Scheduled stop date |
| `lastPublishedDate` | When the campaign was last published |
| `campaignType` | Campaign type |
| `tags` | Classification tags |

**Mapping examples:**

```
Campaign Name=campaign(event.campaignId).campaignName; Program=campaign(event.campaignId).programLabel; State=campaign(event.campaignId).currentState;
```

Use a `hidden()` column when you need multiple fields from the same campaign to avoid resolving it twice:

```
hidden(camp)=campaign(event.campaignId); Campaign Name=camp.campaignName; Campaign State=camp.currentState;
```

# CampaignSummary

**Function:** `campaign_summary(campaignId)` · e.g. `campaign_summary(event.campaignId).firstLaunchDate`

An aggregated view built from all known campaign state-change events. Use this instead of `campaign()` when you need historical milestone dates rather than the current snapshot.

| Field | Description |
| --- | --- |
| `campaignId` | Campaign ID |
| `campaignName` | Display name |
| `programLabel` | URL-safe program slug |
| `currentState` | Current lifecycle state |
| `firstLaunchDate` | When the campaign first went live |
| `lastStoppedDate` | When the campaign was last stopped |
| `lastPausedDate` | When the campaign was last paused |
| `lastArchivedDate` | When the campaign was last archived |
| `tags` | Classification tags |

**Mapping examples:**

```
# When you need when a campaign first launched, not just its current state
First Launch=campaign_summary(event.campaignId).firstLaunchDate; Last Stopped=campaign_summary(event.campaignId).lastStoppedDate;
```

# Client

**Function:** `client(clientId)` or `client()` (uses the event's client) · e.g. `client(event.clientId).shortName`

The brand account on the platform.

| Field | Description |
| --- | --- |
| `id` | Client ID |
| `name` | Full client name |
| `shortName` | Short identifier slug |
| `clientType` | `CUSTOMER`, `INTERNAL`, etc. |
| `timezone` | Client's configured timezone |
| `identityKey` | Identity key type used for this client |

Arbitrary client configuration values are accessed via `client_properties()` (no argument):

```
client_properties().vertical
```

**Mapping examples:**

```
Client=client(event.clientId).shortName; Timezone=client(event.clientId).timezone; Vertical=client_properties().vertical;
```

`client()` with no argument resolves to the event's own client, so both forms are equivalent in single-client reports:

```
Type=client().clientType;
```

When running a cross-client report from the Extole account, filter to real customers:

```
# Filters parameter
client(event.clientId).clientType=="CUSTOMER"
```

# RewardSummary

**Function:** `reward(rewardId)` · e.g. `reward(event.data.reward_id).currentState`

The full lifecycle of one reward instance, built from all known reward state-change events.

| Field | Description |
| --- | --- |
| `rewardId` | Platform reward ID |
| `personId` | Person who earned the reward |
| `faceValue` | Reward face value |
| `faceValueType` | `POINTS`, `CREDIT`, `COUPON_CODE`, etc. |
| `currentState` | `EARNED`, `FULFILLED`, `SENT`, `REDEEMED`, `FAILED`, `CANCELED`, `REVOKED` |
| `rewardSupplierId` | Supplier that issued this reward |
| `campaignId` | Campaign context |
| `program` | Program label |
| `partnerRewardId` | External reward identifier |
| `earnedStepEventContext.name` | Name of the step that triggered this reward |
| `earnedStepEventContext.eventTime` | When the triggering step occurred |
| `rewardEarnedDate` | When the reward was earned |
| `rewardFulfilledDate` | When the reward was fulfilled |
| `rewardSentDate` | When the reward was last sent |
| `rewardRedeemedDate` | When the reward was redeemed |
| `rewardFailedDate` | When the reward failed |
| `rewardCanceledDate` | When the reward was canceled |
| `rewardRevokedDate` | When the reward was revoked |
| `tags` | Classification tags |
| `data` | Custom reward data |

**Mapping examples:**

```
# From a Rewards report — reward_id is on the event data
State=reward(event.data.reward_id).currentState; Face Value=reward(event.data.reward_id).faceValue; Value Type=reward(event.data.reward_id).faceValueType; Earned On=reward(event.data.reward_id).rewardEarnedDate; Earning Step=reward(event.data.reward_id).earnedStepEventContext.name;
```

To sum total reward value issued across a step in a **Metrics** report:

```
Total Reward Value=group_sum(reward(event.data.reward_id).faceValue, step_name:"advocate_reward_earned");
```

# RewardSupplier

**Function:** `reward_supplier(rewardSupplierId)` · e.g. `reward_supplier(event.rewardSupplierId).displayType`

The configuration for how rewards are structured and issued.

| Field | Description |
| --- | --- |
| `rewardSupplierId` | Supplier ID |
| `name` | Display name |
| `type` | `COUPON`, `TANGO`, `PAYPAL_PAYOUTS`, `SALESFORCE_COUPON`, `CUSTOM`, etc. |
| `displayType` | UI display type |
| `faceValueType` | Value type |
| `faceValue` | Configured face value |
| `faceValueAlgorithmType` | How face value is calculated |
| `partnerRewardSupplierId` | External supplier identifier |

**Mapping example:**

```
Supplier Name=reward_supplier(event.rewardSupplierId).name; Supplier Type=reward_supplier(event.rewardSupplierId).type; Display Type=reward_supplier(event.rewardSupplierId).displayType;
```

# SupportSummary

**Function:** `support()` · e.g. `support().salesforceAccountId`

Account-level support and CRM metadata for the current client. No argument is required.

| Field | Description |
| --- | --- |
| `salesforceAccountId` | CRM account ID |
| `slackChannelName` | Internal Slack channel |
| `csmEmail` | Customer success manager email |
| `csmFirstName` | CSM first name |
| `csmLastName` | CSM last name |
| `supportEmail` | Support representative email |

**Mapping example:**

```
Salesforce ID=support().salesforceAccountId; CSM=concatenate(support().csmFirstName, " ", support().csmLastName);
```

# ConsumerEvent

**Function:** `event(eventId)` · e.g. `event(event.rootEventId).type`

The raw event object. Most reports use `StepRecord` or `InputRecord` as the primary row record; load the raw event when you need the full person sub-object or properties not available on the record.

| Field | Description |
| --- | --- |
| `id` | Event ID |
| `type` | Event type discriminator |
| `eventTime` | When the event occurred |
| `requestTime` | When the request was received |
| `rootEventId` | Root event in the causal chain |
| `causeEventId` | The event that directly caused this one |
| `data` | Arbitrary event data |
| `person` | The full Person profile |
| `clientContext.clientId` | Client ID at event time |
| `clientContext.clientShortName` | Client short name |
| `eventContext.appType` | Application type |
| `eventContext.userId` | Client-side user ID |
| `sandbox.container` | Environment container |

**StepConsumerEvent** adds: `name`, `aliases`, `firstSiteVisit`, `duplicate`, `partnerEventId`, `referralContext`, `selectedCampaignContext`.

**InputConsumerEvent** adds: `name`, `url`, `referrer`, `sourceIps`, `httpHeaders`, `httpCookies`, `labels`, `locale`.

**Mapping examples:**

```
# Load the root event to get its type or name
Root Event Type=event(event.rootEventId).type; Root Event Name=event(event.rootEventId).name;

# Access the person sub-object via the raw event
Person Email=event(event.id).person.email;
```

Two common cross-entity lookups worth knowing:

**From a step event, load the originating input record** (gives you `apiType`, `userAgent`, etc.):

```
API Type=input_record(event.rootEventId, event_time_name:event.eventTime).apiType; User Agent=input_record(event.rootEventId, event_time_name:event.eventTime).userAgent;
```

**From a reward event, load the step record that earned the reward** (gives you `visitType`, `quality`, etc.):

```
Visit Type=step_record(event.earnedStepEventContext.id, step_name:event.earnedStepEventContext.name, event_time_name:event.earnedStepEventContext.eventTime).visitType;
```

# AudienceMembershipRecord

**Used in:** Audience Memberships, Audience Memberships Metrics reports · **Access:** `event.*` (no join function — only reachable as the primary record of these two report types)

One audience membership change event: a person entering, updating, or leaving an audience segment.

| Field | Description |
| --- | --- |
| `type` | Event type — `AUDIENCE_MEMBERSHIP_CREATED`, `AUDIENCE_MEMBERSHIP_UPDATED`, or `AUDIENCE_MEMBERSHIP_DELETED` |
| `id` | Event ID |
| `clientId` | Client that owns this record |
| `eventTime` | When the membership change occurred |
| `requestTime` | When the request was received |
| `deviceProfileId` | Associated device profile (may be null) |
| `identityProfileId` | Associated identity profile (may be null) |
| `personId` | Person this membership belongs to |
| `container` | Environment container |
| `data` | Custom key-value event data |
| `appData` | Application-level event data |
| `audienceId` | Audience segment ID |
| `audienceName` | Audience segment display name |

# MessageSummary

**Used in:** Message Metrics reports · **Access:** `event.*` (no join function — only reachable as the primary record of this report type)

One outbound message (typically email) triggered by a campaign, with delivery and suppression outcome.

| Field | Description |
| --- | --- |
| `clientId` | Client that owns this record |
| `messageId` | Message ID |
| `zoneName` | Zone/campaign zone that triggered the message |
| `programLabel` | Program label (may be null) |
| `campaignId` | Parent campaign ID (may be null) |
| `container` | Environment container (may be null) |
| `optoutList` | Opt-out list name if the message was suppressed (may be null) |
| `normalizedEmailFrom` | Normalized sender email (may be null) |
| `normalizedEmailSentAs` | Normalized "sent as" email (may be null) |
| `normalizedEmailTo` | Normalized recipient email (may be null) |
| `emailTo` | Recipient email, original form (may be null) |
| `emailSubject` | Email subject line (may be null) |
| `doNotSendReason` | Reason the message was not sent, if applicable (may be null) |
| `status` | Message status — e.g. `SENT`, `FAILED`, `NOT_SENT` |
| `data` | Custom message data |
| `triggeredDate` | When the message was triggered |
| `sentDate` | When the message was sent (may be null) |
| `recipientId` | Recipient identifier, if known (may be null) |

# WebhookEvent

**Used in:** Webhook Events, Webhook Event Metrics reports · **Access:** `event.*` (no join function — only reachable as the primary record of these two report types)

One webhook trigger event — the event that queues a webhook dispatch, before the dispatch attempt itself.

| Field | Description |
| --- | --- |
| `eventId` | Webhook event ID |
| `clientId` | Client that owns this record |
| `eventTime` | When the webhook event was generated |
| `webhookId` | Webhook definition ID |
| `causeEventId` | ID of the event that triggered this webhook |
| `rootEventId` | Root event in the causal chain |
| `causeEventSequence` | Sequence position of the cause event |
| `data` | Webhook event payload (custom data) |

# WebhookDispatchResultEvent

**Used in:** Webhook Dispatch Results, Webhook Dispatch Result Metrics reports · **Access:** `event.*` (no join function — only reachable as the primary record of these two report types)

The outcome of one webhook dispatch attempt — the HTTP request Extole sent and the response received.

| Field | Description |
| --- | --- |
| `clientId` | Client that owns this record |
| `webhookId` | Webhook definition ID |
| `url` | Target webhook URL (may be null) |
| `eventTime` | When the dispatch attempt occurred |
| `attemptCount` | Number of retry attempts made |
| `configuredRetriesCount` | Maximum configured retries |
| `method` | HTTP method used — e.g. `POST` (may be null) |
| `requestBody` | Request body sent to the webhook endpoint (may be null) |
| `requestHeaders` | HTTP request headers sent |
| `responseStatusCode` | HTTP response status code received (may be null) |
| `responseBody` | Response body received (may be null) |
| `responseHeaders` | HTTP response headers received |
| `logMessages` | Dispatch attempt log messages |
| `tags` | Tags/labels assigned to this dispatch result |

# ClientEvent

**Used in:** Client Event Metrics reports · **Access:** `event.*` (no join function — only reachable as the primary record of this report type)

An operational or business event logged against a client account (e.g. a platform notice or account-level occurrence), distinct from a person's referral-program steps.

| Field | Description |
| --- | --- |
| `eventId` | Event ID |
| `eventType` | Event type classification |
| `clientId` | Client this event is logged against |
| `eventTime` | When the event occurred |
| `name` | Event name |
| `tags` | Classification tags — e.g. `TECHNICAL`, `BUSINESS_OPERATIONS` |
| `message` | Human-readable event message |
| `data` | Structured event data — each value has `value`, `type` (`STRING` or `ATTACHMENT`), and `scope` |
| `level` | Severity level — `INFO`, `WARN`, or `ERROR` |
| `userId` | User identifier, if applicable (may be null) |
| `scope` | Visibility scope of the event |
