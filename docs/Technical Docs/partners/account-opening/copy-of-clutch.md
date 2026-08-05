---
title: MANTL
deprecated: false
hidden: true
metadata:
  robots: index
---
Follow this three-step process for integrating MANTL with Extole to automatically attribute, verify, and reward prospects and members when they open an account.

## Prerequisites

| Requirement              | Description                                          |
| :----------------------- | :--------------------------------------------------- |
| Google Tag Manager (GTM) | You must have a GTM account to use this integration. |

## Step 1: Tag your account opening flow

Use Google Tag Manager (GTM) to deploy Extole's core and event tags. Core tags are used for attribution and serving confirmation messages throughout the OAO flow. Event tags are used to enforce quality rules and track key conversion milestones throughout the account opening process.

<Callout icon="📘" theme="info">
  Learn more about [Extole's Javascript tags](https://docs.extole.com/docs/javascript-sdk)
</Callout>

### Add the Extole core tag to all of your account opening pages

You can find your core tag in the [Extole platform](https://my.extole.com/tech-center/tag-generator) (Tech Center > Tag Generator.) It will look something like this:

```javascript
<script type="text/javascript" src="https://share.{{your_company}}.org/core.js" async />
```

## Step 2: Set up UTM tracking parameters in your Extole campaign<br />

When a prospect clicks on an Extole link, Extole can append their advocate or offer code as a dynamic UTM parameter in the URL. MANTL stores all UTM parameters throughout the lifecycle of the application. To append the Extole code as a UTM parameter:

1. Navigate to `Share Link Behavior` in your Extole Flow campaign
2. Set the `Destination for Clicks on Share Links` to your specific online account opening URL.
3. Append the advocate's referral code to your tracking parameters by updating the `utm_term` variable with the following value:

```Text value
{[ advocateCode ]}
```

<Callout icon="📘" theme="info">
  If you are already using the `utm_term` parameter, you can use a different UTM parameter to pass the `advocate_code` .&#x20;
</Callout>

## Step 3: Push&#x20;

<br />

<br />
