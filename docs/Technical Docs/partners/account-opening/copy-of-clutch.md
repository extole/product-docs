---
title: MANTL
excerpt: >-
  MANTL accelerates digital account opening with a streamlined platform built
  for scalability. 
deprecated: false
hidden: false
metadata:
  robots: index
---
Follow this three-step process for integrating MANTL with Extole to automatically attribute, verify, and reward prospects and members when they open an account.

# Prerequisites

| Requirement              | Description                                          |
| :----------------------- | :--------------------------------------------------- |
| Google Tag Manager (GTM) | You must have a GTM account to use this integration. |

# Step 1: Tag your account opening flow

Use Google Tag Manager (GTM) to add Extole's core tag to all of your account opening pages. The core tag is an async tag used for attribution and serving confirmation messages when prospects click on an Extole link.

<Callout icon="📘" theme="info">
  Learn more about [Extole's Javascript tags](https://docs.extole.com/docs/javascript-sdk)
</Callout>

## Add the Extole core tag to all of your account opening pages

You can find your core tag in the [Extole platform](https://my.extole.com/tech-center/tag-generator) (Tech Center > Tag Generator.) It will look something like this:

```javascript
<script type="text/javascript" src="https://share.{{your_company}}.org/core.js" async />
```

# Step 2: Set up UTM tracking parameters in your Extole campaign

When a prospect clicks on an Extole link, Extole will append a unique advocate or offer code as a UTM parameter in the URL. On redirect, MANTL will store and update all UTM parameters throughout the application lifecycle. To append the Extole code as a UTM parameter:

1. Navigate to `Share Link Behavior` in your Extole Flow campaign
2. Set the `Destination for Clicks on Share Links` to your specific online account opening URL.
3. Append the advocate's referral code to your tracking parameters by updating the `utm_term` variable with the following value:

```Text value
{[ advocateCode ]}
```

<Callout icon="📘" theme="info">
  If you are already using the `utm_term` parameter, you can use a different UTM parameter to pass the `advocate_code` .&#x20;
</Callout>

# Step 3: Send new account openings to Extole's SFTP server

In order for Extole to track whether the referral resulted in a qualified opened account, you'll need to push <Anchor target="_blank" href="https://storage.googleapis.com/mantl-reports-documentation-production/schema/reports_documentation.html">MANTL's Simplified Acquisition report</Anchor> to <Anchor target="_blank" href="https://docs.extole.com/update/docs/extoles-sftp-server">Extole's SFTP Server</Anchor> on a daily basis. Extole will extract the `email`, `first_name,` `last_name`,  `utm_term_first_touch`,  `account_created_at`,  and `account_type` columns to determine whether someone used a referral code to open their account. Alternatively, you can push this data into your core or data warehouse and send Extole a <Anchor target="_blank" href="https://docs.extole.com/update/docs/file-based-events">daily events file</Anchor> of users who have opened accounts with your institution.

<br />
