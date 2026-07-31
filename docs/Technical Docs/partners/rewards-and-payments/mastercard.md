---
title: Mastercard Implementation Guide
excerpt: Referral in a Box
deprecated: false
hidden: true
metadata:
  robots: index
---
## Overview

This guide describes the end-to-end implementation process for launching the Mastercard **Referral in a Box** solution powered by Extole.

The standard implementation takes approximately four weeks, followed by a pilot campaign and reward fulfillment period.

| Step       | Description                                   | Primary Owner                               |
| ---------- | --------------------------------------------- | ------------------------------------------- |
| Step 0     | Account Provisioning                          | Extole                                      |
| Step 1     | Brand the Referral Program                    | Financial Institution                       |
| Step 2     | Configure Referral Experience                 | Extole + Financial Institution              |
| Step 3     | Review, QA & Certification                    | Mastercard + Extole + Financial Institution |
| Step 4     | Upload Target Audience & Launch Campaign      | Financial Institution + Mastercard          |
| Step 5     | Qualification Processing & Reward Fulfillment | Financial Institution + Extole + Mastercard |
| Post Pilot | Reporting & Production Transition             | All Parties                                 |

***

# Step 0

# Account Provisioning

Once Mastercard executes a Statement of Work (SOW) with a participating Financial Institution, Extole will provision a dedicated Extole account and create a new referral campaign.

## Extole Responsibilities

Extole will:

- Provision a new Extole account and invite the Mastercard delivery team
- Create a new Referral in a Box campaign with
  - Pre-configured emails, experiences, events, and rules&#x20;

Once the account has been provisioned, implementation begins with campaign branding.

***

# Step 1: Brand the Referral Program

Each Financial Institution customizes the referral experience so it appears as a seamless extension of its own brand.

## White-label Referral Emails and Links

Configure branded domains for:

- Referral landing pages
- Referral sharing links
- Transa

Refer to the Extole DNS Requirements documentation:

[https://docs.extole.com/docs/extole-dns-requirements](https://docs.extole.com/docs/extole-dns-requirements)

***

## Campaign Configuration Template

CCreative Asset Requirements

For complete specifications, refer to:

[https://docs.extole.com/docs/creative-image-asset-guide](https://docs.extole.com/docs/creative-image-asset-guide)

***

# Step 2

# Configure the Referral Experience

The referral experience can be deployed using one of two implementation options.

***

## Option A

## Extole Hosted Experience (Recommended)

Extole hosts the complete referral experience.

The Financial Institution simply links customers to the hosted experience from:

- Website
- Online Banking
- Mobile Banking
- Email Campaigns
- SMS Campaigns

This option requires the least implementation effort.

***

## Option B

## Embedded Experience

The referral experience can also be embedded directly into an existing website using Extole JavaScript zones.

Two independent experiences are available.

| Zone                               | Purpose                                                  |
| ---------------------------------- | -------------------------------------------------------- |
| Embedded Share Experience          | Existing customers share referrals                       |
| Embedded Friend Landing Experience | Referred friends register after clicking a referral link |

***

### Embedded Friend Landing Experience

Displays the registration experience shown to referred friends.

```html
<span id="extole_zone_embedded_friend_landing_experience"></span>

<script type="text/javascript">
(function(c,b,f,k,a){
    c[b]=c[b]||{};
    for(c[b].q=c[b].q||[];a<k.length;)
        f(k[a++],c[b]);
})(window,"extole",function(c,b){
    b[c]=b[c]||function(){
        b.q.push([c,arguments]);
    };
},["createZone"],0);

extole.createZone({
    name: "embedded_friend_landing_experience",
    element_id: "extole_zone_embedded_friend_landing_experience"
});
</script>
```

When the page loads, Extole dynamically renders the Friend Landing Experience inside the specified HTML element.

***

### Embedded Share Experience

Displays the sharing experience for advocates.

```html
<span id="extole_zone_embedded_share_experience"></span>

<script type="text/javascript">
(function(c,b,f,k,a){
    c[b]=c[b]||{};
    for(c[b].q=c[b].q||[];a<k.length;)
        f(k[a++],c[b]);
})(window,"extole",function(c,b){
    b[c]=b[c]||function(){
        b.q.push([c,arguments]);
    };
},["createZone"],0);

extole.createZone({
    name: "embedded_share_experience",
    element_id: "extole_zone_embedded_share_experience"
});
</script>
```

When the page loads, Extole injects the complete advocate sharing experience into the page.

***

## Creating Campaign Entry Links

Extole Promo Links should be created for every campaign entry point.

Typical entry points include:

- Website
- Online Banking
- Mobile Banking
- Email
- SMS

Documentation:

[https://docs.extole.com/docs/how-to-create-a-promo-link](https://docs.extole.com/docs/how-to-create-a-promo-link)

***

# Step 3

# Review, QA & Certification

Before launch, Mastercard, Extole, and the Financial Institution complete end-to-end testing using sample campaign data.

Testing validates:

- Invitation emails
- Referral sharing
- Friend registration
- Qualification processing
- Referral matching
- Reward generation

***

## Sample Audience File

| First Name | Last Name | Email                                                           |
| ---------- | --------- | --------------------------------------------------------------- |
| John       | Smith     | [john.smith@testbank.com](mailto:john.smith@testbank.com)       |
| Sarah      | Jones     | [sarah.jones@testbank.com](mailto:sarah.jones@testbank.com)     |
| Michael    | Brown     | [michael.brown@testbank.com](mailto:michael.brown@testbank.com) |

***

## Qualification Event File

Qualification events should follow Extole's standard file-based event format.

| first_name | last_name | email                                                           | event_time (ISO 8601) | event_name                       |
| ---------- | --------- | --------------------------------------------------------------- | --------------------- | -------------------------------- |
| John       | Smith     | [john.smith@testbank.com](mailto:john.smith@testbank.com)       | 2026-09-15T14:32:18Z  | account_opened                   |
| Sarah      | Jones     | [sarah.jones@testbank.com](mailto:sarah.jones@testbank.com)     | 2026-09-20T09:15:42Z  | account_closed                   |
| Michael    | Brown     | [michael.brown@testbank.com](mailto:michael.brown@testbank.com) | 2026-09-25T18:05:11Z  | ten_debit_transactions_completed |

Supported event names:

- account_opened
- account_closed
- ten_debit_transactions_completed

***

## Account Qualified File

Financial Institutions may alternatively submit a single qualification file.

| first_name | last_name | email                                                     | event_time (ISO 8601) | event_name        |
| ---------- | --------- | --------------------------------------------------------- | --------------------- | ----------------- |
| John       | Smith     | [john.smith@testbank.com](mailto:john.smith@testbank.com) | 2026-09-30T15:10:42Z  | account_qualified |

***

## QA Certification

Implementation is considered complete once:

- Invitation emails are delivered successfully
- Referral links function correctly
- Friend registrations are captured
- Qualification files process successfully
- Rewards move into the Earned state
- Mastercard validates the Earned Rewards Report

***

# Step 4

# Upload Target Audience & Launch Campaign

After implementation has been approved, Mastercard launches the referral campaign using an audience provided by the Financial Institution.

To protect customer payment information, Extole never receives or stores PAN data.

***

## Step 4.1

### Financial Institution Generates Target Audience

Prepare a list containing:

| Field      | Required |
| ---------- | -------- |
| First Name | ✓        |
| Last Name  | ✓        |
| Email      | ✓        |
| PAN        | ✓        |

***

## Step 4.2

### Upload Through Mastercard Digital Enablement (MDE)

The Financial Institution securely uploads the audience file through Mastercard Digital Enablement (MDE).

***

## Step 4.3

### Mastercard Removes PAN Data

Mastercard removes the PAN column before uploading the audience to Extole.

The resulting file contains:

| First Name | Last Name | Email                                                     |
| ---------- | --------- | --------------------------------------------------------- |
| John       | Smith     | [john.smith@testbank.com](mailto:john.smith@testbank.com) |

***

## Step 4.4

### Mastercard Uploads Audience to Extole

Mastercard imports the sanitized audience into Extole.

***

## Step 4.5

### Campaign Launch

Extole sends invitation emails to all eligible customers.

Customers can:

- Join the referral program
- Generate referral links
- Refer friends
- Track referral progress

***

# Step 5

# Qualification Processing & Reward Fulfillment

After the campaign launches, Extole must receive qualification data to determine which referrals have satisfied the campaign requirements.

Financial Institutions have two supported integration options.

***

## Option A

### Event-Based Qualification

Submit standard qualification event files containing:

- account_opened
- account_closed
- ten_debit_transactions_completed

Each event should follow Extole's standard event format.

***

## Option B

### Account Qualified File

Instead of sending multiple events, the Financial Institution may submit a single Account Qualified file once customers satisfy all qualification requirements.

***

## Referral Matching

When qualification data is received, Extole matches referrals using the email address collected during the Friend Landing Experience.

Once qualification requirements are satisfied:

- Advocate rewards move to **Earned**
- Friend rewards move to **Earned**

***

## Earned Rewards Report

Mastercard can export the standard Extole Earned Rewards Report.

The report follows the standard Credit Union Earned Rewards file format documented here:

[https://docs.extole.com/docs/file-based-events#credit-union-earned-rewards-file-example](https://docs.extole.com/docs/file-based-events#credit-union-earned-rewards-file-example)

Representative fields include:

| Advocate First Name | Advocate Last Name | Advocate Email                                | Friend First Name | Friend Last Name | Friend Email                                    | Reward Name     | Reward Value | Reward Type      | Earned Date | Status |
| ------------------- | ------------------ | --------------------------------------------- | ----------------- | ---------------- | ----------------------------------------------- | --------------- | ------------ | ---------------- | ----------- | ------ |
| John                | Smith              | [john@testbank.com](mailto:john@testbank.com) | Sarah             | Jones            | [sarah@testbank.com](mailto:sarah@testbank.com) | Advocate Reward | $100         | Statement Credit | 2026-09-30  | Earned |

***

## PAN Enrichment

The Earned Rewards Report intentionally does not contain PAN information.

The fulfillment process is:

1. Mastercard exports the Earned Rewards Report from Extole.
2. Mastercard sends the report to the Financial Institution.
3. The Financial Institution adds PAN information for each eligible cardholder.
4. The enriched report is returned to Mastercard.
5. Mastercard processes reward fulfillment.

***

# After the Pilot Period

## Update the Referral Experience

Once the campaign pilot period concludes, the referral experience should be updated so that new customers can no longer participate while existing participants can continue viewing their referral status.

Using Extole's composable experiences, this typically involves:

- Disabling the Friend Landing Experience lead capture form
- Disabling the Share Experience
- Updating campaign messaging to indicate the pilot has concluded
- Leaving referral history and reward status visible for existing participants

This allows the campaign to remain accessible while preventing new referrals.

***

## Export Reports

Before the pilot campaign ends, Mastercard and the Financial Institution should export all reporting required to evaluate campaign performance.

Recommended reports include:

- Campaign Summary
- Referral Funnel
- Shares
- Referrals
- Referral Conversion Rate
- Advocate Performance
- Earned Rewards
- Pending Rewards
- Customer Activity

***

## Campaign Retention

The pilot campaign will remain available in the Extole platform for **30 days** following the conclusion of the pilot.

This evaluation period allows time for:

- Final reporting
- Outstanding reward fulfillment
- Internal review
- Subscription decision

If the Financial Institution elects not to continue, the campaign may be archived after the evaluation period.

***

## Transition to an Annual Subscription

Financial Institutions that continue beyond the pilot should transition from manual file exchanges to automated production integrations.

### Qualification Processing

Qualification events should be automated using:

- Secure SFTP
- Extole Events API

### Reward Fulfillment

Reward fulfillment should also be automated using:

- Secure SFTP
- Reward Fulfillment APIs (where applicable)

Automating both qualification processing and reward fulfillment enables near real-time referral processing and eliminates manual operational work.

***

# Appendix A

# Implementation Timeline

| Week         | Activity                                                                     |
| ------------ | ---------------------------------------------------------------------------- |
| Week 1       | Account provisioning, DNS configuration, branding, creative asset collection |
| Week 2       | Referral experience configuration and campaign setup                         |
| Week 3       | QA, certification, and end-to-end testing                                    |
| Week 4       | Audience upload and campaign launch                                          |
| Pilot Period | Qualification processing and reward fulfillment                              |
| Post Pilot   | Reporting, evaluation, and production transition                             |

***

# Appendix B

# File Exchange Summary

| File                        | From                  | To         | Frequency                  |
| --------------------------- | --------------------- | ---------- | -------------------------- |
| Target Audience             | Financial Institution | Mastercard | Once before launch         |
| Sanitized Audience          | Mastercard            | Extole     | Once before launch         |
| Qualification Event Files   | Financial Institution | Extole     | Daily / Weekly / On Demand |
| Account Qualified File      | Financial Institution | Extole     | Optional                   |
| Earned Rewards Report       | Extole                | Mastercard | As Needed                  |
| PAN-Enriched Rewards Report | Financial Institution | Mastercard | As Needed                  |

***

# Appendix C

# Reference Documentation

| Topic                | Documentation                                                                                                                                                                      |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DNS Requirements     | [https://docs.extole.com/docs/extole-dns-requirements](https://docs.extole.com/docs/extole-dns-requirements)                                                                       |
| Creative Asset Guide | [https://docs.extole.com/docs/creative-image-asset-guide](https://docs.extole.com/docs/creative-image-asset-guide)                                                                 |
| Promo Links          | [https://docs.extole.com/docs/how-to-create-a-promo-link](https://docs.extole.com/docs/how-to-create-a-promo-link)                                                                 |
| File-Based Events    | [https://docs.extole.com/docs/file-based-events](https://docs.extole.com/docs/file-based-events)                                                                                   |
| Earned Rewards File  | [https://docs.extole.com/docs/file-based-events#credit-union-earned-rewards-file-example](https://docs.extole.com/docs/file-based-events#credit-union-earned-rewards-file-example) |

## <br />

<br />

<br />
