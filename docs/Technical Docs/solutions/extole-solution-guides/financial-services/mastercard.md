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

***

# Step 0: Account Provisioning

Once Mastercard executes a Statement of Work (SOW) with a participating Financial Institution, Extole will provision a dedicated Extole account and create a new referral campaign with the appropriate emails, experiences, events, and rules.

<br />

# Step 1: Brand the Referral Program<br />

## White-Label Your Referral Program Domain (Optional)

An optional, but recommended step is to white-label the links and email sender domain used in your referral program to not only improve deliverability but to also ensure that customers trust to click and send share links to their friends.

| Default                            | Branded/White-Labeled             |
| ---------------------------------- | --------------------------------- |
| prosperitybank.extole.io/jsmith101 | refer.properitybank.com/jsmith101 |
| do-not-reply\@referral-mail.com    | do-not-reply\@prosperitybank.com  |

To white-list program links and emails, FI's can refer to: <Anchor target="_blank" href="https://docs.extole.com/docs/extole-dns-requirements">https://docs.extole.com/docs/extole-dns-requirements</Anchor>

***

## Brand Your Campaign

CCreative Asset Requirements

For complete specifications, refer to:

[https://docs.extole.com/docs/creative-image-asset-guide](https://docs.extole.com/docs/creative-image-asset-guide)

***

# Step 2: Set-Up Sharing & Lead Capture Experiences

There are two experiences where advocates and friends will interact with the referral program:

- `Share Experience` - where advocates can generate and share their referral link with friends, plus access referral history, program terms and conditions, etc.
- `Friend Landing Experience -` where referred friends will land after clicking on a referral. The landing experience incldues an email capture form where they can "redeem" their referral so that Extole can match referrals using their email address.

## Option A: Use Extole Hosted Experiences (No-tech)

For a no-tech option, Extole can host these experiences for you via branded Microsites which contain your logo, an image header, a body, the share widget, and a footer. If you're using the microsite option, you can proceed with Step #3.

### Advocate Microsite

![](https://files.readme.io/fcbfe5be6b56a3c0bbd4506a4e0e52968b494aa4c69c5341520c3173676628da-Advocate_Microsite.png)

### Friend Landing Microsite&#x20;

![](https://files.readme.io/b08e776b6103b64484b44b788902d4d27d8aa1f1182b3a41d180793be069ecf0-Friend_Landing_Microsite.png)

<br />

***

## Option B: Embed the experiences on your website (JavaScript SDK)<br />

### Embedded Share Experience

Displays the sharing experience for advocates onto a page that the FI hosts.


<Image src="https://files.readme.io/e63fb1f5622f70388188cfe29a2d8ce97d47d195de8194a2b98908e1be174458-Embedded_Share_Experience.png" align="center" caption="Embedded Share Experience = dotted border" />


<br />To embed the share experience, place Extole's core tag onto all pages of your marketing site. Make sure to replace `refer.brand.com` with your branded referral domain, which can be found in **Extole** > **Tech Center** > **Domains**.

```text
<script type="text/javascript" src="https://refer.brand.com/core.js" fetchpriority="high" async></script>
```

Then, place the embedded share experience tag onto the page where you'd like to embed the content:&#x20;

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

### Embedded Friend Landing Experience

Displays an email capture form that referred friends will complete when clicking on a share link.


<Image src="https://files.readme.io/2327ac229829661ce05573bf6695810a0dbb506880038822a53464f670f9cce5-Embedded_Landing_Experience.png" align="center" caption="Embedded Landing Experience = dotted border" />


To embed the friend landing experience, make sure you've already placed Extole's core tag onto all pages of your marketing site. Make sure to replace `refer.brand.com` with your branded referral domain, which can be found in **Extole** > **Tech Center** > **Domains**.

```text
<script type="text/javascript" src="https://refer.brand.com/core.js" fetchpriority="high" async></script>
```

Then, place the embedded friend landing experience tag onto the page where you'd like to embed the content:&#x20;

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

## Add promotion links to your site, digital banking, etc.

You can link to the embedded share experience or the advocate microsite with promotion links. Promotion links include tracking parameters so that you can you can track where and how people are sharing the referral program. Create a promotion link for each placement (website header, website footer) and place them in behind a Refer a Friend CTA, button, or banner on your site or digital banking app.

[https://docs.extole.com/docs/how-to-create-a-promo-link](https://docs.extole.com/docs/how-to-create-a-promo-link)

# Step 3: Review, approval, and QA&#x20;

<br />

### Compliance review and approval of campaign assets<br />

### Test campaign flow end to end

| QA Test Case                                                                                                                         | Owner       |
| ------------------------------------------------------------------------------------------------------------------------------------ | ----------- |
| Uploads Sample Audience file to Batch Jobs trigger promo email                                                                       | Mastercard  |
| Clicks on promo email and creates referral link. Shares referral link to friends testing all channels (Email, QR, social, SMS, etc.) | Mastercard  |
| Test friend experience by clicking on a referral link and submitting lead capture form.                                              | Mastercard  |
| Checks profles to ensure referral events are recorded.                                                                               | Extole      |
| Upload test qualification event files.                                                                                               | Mastercard  |
| Confirm events and earned rewards are recorded on Extole profiles.                                                                   | Extole      |
| Run and export Earned Rewards Report. Process for fulfillment.                                                                       | Mastercard  |

### Sample Audience File

| first_name | last_name | email                                                           |
| ---------- | --------- | --------------------------------------------------------------- |
| John       | Smith     | [john.smith@testbank.com](mailto:john.smith@testbank.com)       |
| Sarah      | Jones     | [sarah.jones@testbank.com](mailto:sarah.jones@testbank.com)     |
| Michael    | Brown     | [michael.brown@testbank.com](mailto:michael.brown@testbank.com) |

***

## Sample Qualification Event Files<br /><br />Option A: Extole does the qualification

If you want Extole to do the qualification, send the qualification critieria as individual events (`account opened`, `account_closed,` `transaction completed`)  to Extole. When qualification runs through Extole, you'll be able to be more agile in modifying your qualification rules in the future. You can also trigger communications or show progress using individual events (e.g send reminder if user opened their account but hasn't transacted yet.)<br /><br />Once event files are uploaded, Extole will match referrals and record earned rewards on advocate and friend profiles.

| event_name            | first_name | last_name | email                                                           | event_time           | type             |
| --------------------- | ---------- | --------- | --------------------------------------------------------------- | -------------------- | ---------------- |
| account_opened        | John       | Smith     | [john.smith@testbank.com](mailto:john.smith@testbank.com)       | 2026-09-15T14:32:18Z | Premium Checking |
| account_closed        | Sarah      | Jones     | [sarah.jones@testbank.com](mailto:sarah.jones@testbank.com)     | 2026-09-20T09:15:42Z |                  |
| transaction_completed | Michael    | Brown     | [michael.brown@testbank.com](mailto:michael.brown@testbank.com) | 2026-09-25T18:05:11Z | Debit            |

***

## Option B: FI does the qualification

Alternatively, if you'd like to do the qualification and just upload a list of qualified users, you can do so and Extoel will automatically match referrals and record earned rewards on advocate and friend profiles.

| event_name        | first_name | last_name | email                                                     | event_time           |
| ----------------- | ---------- | --------- | --------------------------------------------------------- | -------------------- |
| account_qualified | John       | Smith     | [john.smith@testbank.com](mailto:john.smith@testbank.com) | 2026-09-30T15:10:42Z |

***

# Step 4: Upload Target Audience & Launch Campaign

Upon receiving final approval for go-live, Mastercard launches the referral campaign by uploading the final target list to Extole Audiences to trigger the invitation emails.&#x20;

<br />

### Initial List Pull

FI pulls a list of all eligible customers and shares with Mastercard via MDE.

| Field      | Required |
| ---------- | -------- |
| First Name |          |
| Last Name  |          |
| Email      | ✓        |
| PAN        | ✓        |

***

## Remove PAN data and upload to Extole Audiences

<br />Mastercard removes the PAN column before uploading the audience to Extole, which triggers the invite email to send.

| Field      | Required |
| ---------- | -------- |
| First Name |          |
| Last Name  |          |
|            |          |
| Email      | ✓        |

<br />

## Step 5: Qualification Processing & Reward Fulfillment

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
