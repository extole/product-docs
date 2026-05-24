---
title: "Clutch"
---

Follow this three-step process for integrating Clutch with Extole to automatically attribute, verify, and reward prospects and members when they open an account.

## Prerequisites

| Requirement              | Description                                          |
| :----------------------- | :--------------------------------------------------- |
| Google Tag Manager (GTM) | You must have a GTM account to use this integration. |

## Step 1: Set up URL tracking parameters

To ensure prospects land on the correct page with the necessary tracking data, you'll need to make the following updates:

1. Submit a request to your team at Clutch to push the `utm_content` parameter into your data layer. Map this parameter to`advocate_code` in GTM.
2. In your Extole Flow Campaign, navigate to `Share Link Behavior`
3. Set the `Destination for Clicks on Share Links` to your specific online account URL.
4. Append the advocate's referral code to your tracking parameters by updating the `utm_content` variable with the following value:

```Text value
{[ advocateCode ]}
```

<Image align="center" width="300px" src="https://files.readme.io/bec5211ad9f0aa8261e6df4eeb5d98e6eb683a13f2b605d7e0494227eaa77dce-9b6bac5d4e54762b7930e5afe9ad7b2436bc33105dbea5a9142ee93599550c61-Screenshot_2026-03-09_at_11.28.52AM.png" />

<Callout icon="📘" theme="info">
  If you are already using the `utm_content` parameter, Extole can pass the `advocate_code` as `utm_term` instead. Request this customization with your Extole team, then map to the `utm_term `parameter in your GTM.
</Callout>

## Step 2: Tag your account opening flow

Use Google Tag Manager (GTM) to deploy Extole's core and event tags. Core tags are used for attribution and serving confirmation messages throughout the OAO flow. Event tags are used to enforce quality rules and track key conversion milestones throughout the account opening process.

<Callout icon="📘" theme="info">
  Learn more about [Extole's Javascript tags](https://docs.extole.com/docs/javascript-sdk)
</Callout>

### Add the Extole core tag to all of your account opening pages

You can find your core tag in the [Extole platform](https://my.extole.com/tech-center/tag-generator) (Tech Center > Tag Generator.) It will look something like this:

```javascript
<script type="text/javascript" src="https://share.{{your_company}}.org/core.js" async />
```

### Add tags to fire events

Fire Extole's `application_started`tag on the first application page using Clutch's custom event trigger `WC - Landing Page`.

```javascript
<script type="text/javascript">
    (function(c,b,f,k,a){c[b]=c[b]||{};for(c[b].q=c[b].q||[];a<k.length;)f(k[a++],c[b])})(window,"extole",function (c,b){b[c]=b[c]||function (){b.q.push([c,arguments])}},["createZone"],0);
    extole.createZone({
        name: "application_started",
        data: {
            "application_id": {{DAO - App ID}},
            "advocate_code": {{advocate_code}}
        }
    });
</script>
```

Fire Extole's `application_submitted` tag when the prospect/member completes their application using Clutch's custom event trigger `WC - DAO - App Submission`.

```javascript
<script type="text/javascript">
    (function(c,b,f,k,a){c[b]=c[b]||{};for(c[b].q=c[b].q||[];a<k.length;)f(k[a++],c[b])})(window,"extole",function (c,b){b[c]=b[c]||function (){b.q.push([c,arguments])}},["createZone"],0);
    extole.createZone({
        name: "application_submitted",
        data: {
            "application_id": {{DAO - App ID}},
            "advocate_code": {{advocate_code}}
        }
    });
</script>
```

<br />

## Step 3: Send account openings from Clutch to Extole via SFTP

Forward your daily export file from Clutch to Extole's SFTP server to notify Extole of **account openings**. Extole will extract and process the data for any columns marked in **bold** in the table below.

<Callout icon="📘" theme="info">
  Learn how to connect to [Extole's SFTP server](https://docs.extole.com/docs/extoles-sftp-server).
</Callout>

<Callout icon="🚧" theme="warn">
  If you are using Clutch's in-branch and online account opening products, you can use the daily extract file to track all account opening events for your Extole campaign. If you are only using Clutch for online account openings, you will need to send in-branch openings as a seperate file.
</Callout>

| column header             | sample value                             |
| :------------------------ | :--------------------------------------- |
| **application_id**        | **0008c146-2d6e-44aa-ae93-e16c1decf095** |
| **applicant_name**        | **John Smith**                           |
| **applicant_email**       | **[jsmith101@gmail.com]()**              |
| **member_nr**             | **55579**                                |
| **product_name**          | **Premium Share Account**                |
| **product_type**          | **savings**                              |
| **is_new_member**         | **TRUE**                                 |
| **account_status**        | **CREATED**                              |
| **account_created_at**    | **2024-11-12T16:11:46.629Z**             |
| **utm_content**           | **jsmith101** (`advocate_code`)          |
| applicant_id              | b407904b-1269-43ac-858a-40e4255ad60d     |
| account_nr                | 0000690616 S 1200 Premium Share Account  |
| applicant_phone           | +13868063214                             |
| applicant_address         | 1405 POINT ST APT 1706                   |
| applicant_zipCode         | 21231                                    |
| applicant_city            | Baltimore                                |
| applicant_state           | MD                                       |
| applicant_employer        | Any                                      |
| applicant_job_title       | null                                     |
| eligibility_criteria      | null                                     |
| eligibility_detail        | null                                     |
| funding_type              | CREDIT_CARD                              |
| funding_amnt              | 100                                      |
| application_origin        | CONSUMER                                 |
| branch_name               | null                                     |
| branch_user_id            | null                                     |
| employee_name             | null                                     |
| application_status        | ACCEPTED                                 |
| funding_status            | COMPLETED                                |
| application_created_at    | 2024-11-12T16:06:59.794Z                 |
| application_updated_at    | 2024-11-12T16:11:46.62Z                  |
| received_aan              | FALSE                                    |
| aan_created_at            | null                                     |
| aan_reason                | null                                     |
| utm_source                | null                                     |
| utm_medium                | null                                     |
| utm_campaign              | null                                     |
| utm_term                  | null                                     |
| funding_started_at        | 2024-11-12T16:08:12.395Z                 |
| funding_authorized_at     | 2024-11-12T16:11:15.981Z                 |
| fraud_check_approved_at   | 2024-11-12T16:11:17.666Z                 |
| account_booked_to_core_at | 2024-11-12T16:11:46.845Z                 |
| user_id                   | b9e7cee6-b845-4216-886a-9f7f44343c91     |
| session_id                | 1731421638956                            |

<br />
