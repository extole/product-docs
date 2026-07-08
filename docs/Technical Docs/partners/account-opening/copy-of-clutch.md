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
  ###

  Learn more about [Extole's Javascript tags](https://docs.extole.com/docs/javascript-sdk)
</Callout>

### Add the Extole core tag to all of your account opening pages

You can find your core tag in the [Extole platform](https://my.extole.com/tech-center/tag-generator) (Tech Center > Tag Generator.) It will look something like this:

```javascript
<script type="text/javascript" src="https://share.{{your_company}}.org/core.js" async />
```

### Add tags to fire events

Fire Extole's `application_submitted` tag when the prospect/member completes their application.&#x20;

```javascript
<script type="text/javascript">
    (function(c,b,f,k,a){c[b]=c[b]||{};for(c[b].q=c[b].q||[];a<k.length;)f(k[a++],c[b])})(window,"extole",function (c,b){b[c]=b[c]||function (){b.q.push([c,arguments])}},["createZone"],0);
    extole.createZone({
        name: "application_submitted",
        data: {
            "person_id": {{person_id}},
      			"application_id": {{application_id}},
						"external_core_id": {{external_core_id}}
        }
    });
</script>
```

## Step 2: Set up a webhook in MANTL to notify Extole of account openings<br />

Extole should be notified once the account has been opened. The webhook response body should include the person ID and application ID.

[https://api.mantl.com/rest/docs#/webhooks/postapplication\_booked](https://api.mantl.com/rest/docs#/webhooks/postapplication_booked "https://api.mantl.com/rest/docs#/webhooks/postapplication_booked") <br />[https://dev.extole.com/reference/create-event](https://dev.extole.com/reference/create-event "https://dev.extole.com/reference/create-event")

## Step 3: Extole connects to MANTL to retrieve customer identifier

Extole will then use the MANTL Accounts API to retrieve the members email address and additional information for reward qualification and fulfillment

&#x20;[https://api.mantl.com/rest/docs#/Accounts/getAccount](https://api.mantl.com/rest/docs#/Accounts/getAccount "https://api.mantl.com/rest/docs#/Accounts/getAccount")&#x20;
