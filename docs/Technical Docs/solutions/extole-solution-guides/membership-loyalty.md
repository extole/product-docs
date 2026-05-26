---
title: Membership & Loyalty
excerpt: >-
  Set up a membership and loyalty referral program with branded links, website
  tags, signup and purchase tracking, rewards, mobile integration, and optional
  enhancements.
---

## Overview

[//]: # "What steps are required for setting up a membership and loyalty referral program with Extole?"

Use this guide to set up a membership and loyalty referral program that tracks signups and purchases, then rewards advocates and friends.

1. Brand your Program
2. Tag your Website
3. Reward your Customers
4. Design your Experience (done by your creative team)
5. Add to your Mobile App

[//]: ___

<Image alt="Membership Referral Steps" align="center" src="https://files.readme.io/fe6a9c15d75ed947c4f104572d3b40edf971ae0437591464e56c108a276cb003-e22cc1e-Membership_-_General.png">
  Membership Referral Steps
</Image>

## Brand your Program

[//]: # "How do I brand my membership and loyalty referral program with Extole?"

### Create a CNAME for your Domain

> 📘 Task Duration
>
> This task will typically take an IT/Ops engineering team 10–15 minutes to complete.

Create a CNAME (a DNS record that points one domain to another) for your domain so you can create branded <Glossary>Promotion Link</Glossary>s and <Glossary>Share Link</Glossary>s.

To set up your CNAME, please complete the steps outlined in [Extole DNS Requirements](doc:extole-dns-requirements).

### Send from Your Branded Email

<ImproveOpenRatesCallout />

The referral program will send program emails from you to your customers:

* Welcome Email
* Advocate Stats Email
* Earned Reward Email

The from address for this will typically be something similar to `do-not-reply@mycompany.com`. Once this email has been identified, Extole can check if it is configured to allow Extole to send emails from this address.

For details on how to update your SPF (Sender Policy Framework) DNS records and install Extole DKIM (DomainKeys Identified Mail) keys, reference [Extole DNS Requirements](doc:extole-dns-requirements).

> 📘 Related Content
>
> * [Find your domain in the settings page of My Extole](https://my.extole.com/settings)
> * [How to set up your program domain](https://success.extole.com/hc/en-us/articles/115012548127-Program-Domain-Set-Up)

[//]: ___

## Tag your Website

Extole works with your site using lightweight JavaScript tags. The core tag must be included on every page of your site and contains Extole's JavaScript Library.

Extole tags can go anywhere in the HTML of the page and do not need to be loaded in any specific order. They are asynchronous to ensure fast page loading.

Marketing tags display <Glossary>CTA</Glossary>s (calls to action) inline on your page. These tags reference a specific `span` tag by `id` and should be placed in the HTML where they will appear.

### Add the Core Tag (Extole's JavaScript Library)

Extole's JavaScript library must be placed on all of your pages using the core tag. This tag is used to activate the Extole system and ensures that any other Extole tags on your page work properly.

The core tag can be found under your program’s branded domain (refer.brand.com). If you haven't set up your branded domain yet, you can load the tag from the Extole unbranded domain.

Find your active referral domain and use that for your core tag. It will look like `brand.extole.io` (unbranded) or `refer.brand.com` (branded).

```javascript Extole Core Tag
<!-- BRANDED -->
<script type="text/javascript" src="https://refer.brand.com/core.js" fetchpriority="high" async></script>

<!-- UNBRANDED -->
<script type="text/javascript" src="https://brand.extole.io/core.js" fetchpriority="high" async></script>
```

### Add Marketing Tags

Extole displays <Glossary>CTA</Glossary>s that promote the program. For example, a `global_header` CTA can add a banner at the top of the screen that says “Refer a friend.” When a customer selects the banner, it opens the <Glossary>Share Experience</Glossary>.

Marketing tags tell Extole where to show CTAs on your website. These tags also enable tracking so you can see which placements drive participation.

Extole recommends emailing advocates a promotion code they can use to apply credits to their account. If your membership program applies account credits automatically instead, restrict sharing to logged-in advocates and include advocate information in the marketing tags.  

An Extole campaign comes with these standard marketing tag names:

* `global_header`
* `global_footer`
* `product`
* `confirmation`
* `overlay`

You can create additional marketing tags for pages such as your blog or help center. As you get started, contact your Customer Success Manager for help creating these tags.

#### Marketing Tag Placement

Add a `span` element to the page where the content should appear. You typically add this element through your CMS or site code. Inline tags require this element; `overlay` and `confirmation` tags do not.

```javascript Span ID
<span id="extole_zone_global_header"></span>
```

Additionally, there is the `script` tag that loads the targeted content from the program and inserts it onto the page in the `span` tag.

**Below is an example of a `global_header` tag**:

```javascript Global Header CTA
<span id="extole_zone_global_header"></span>
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'global_header',
     element_id: 'extole_zone_global_header',
     data: {
       "partner_user_id":"00O40000004SA1AA", // DYNAMIC VALUE
       "email": "april@advocate.com",  // DYNAMIC VALUE
       "first_name": "April",  // DYNAMIC VALUE
       "last_name": "Advocate"  // DYNAMIC VALUE
     }     
  });
</script>
```

> 🚧 Important Note
>
> Extole uses the visitor's name, email, and ID to personalize their experience. This data also helps match advocates and friends for rewards, customize emails and shares, and recognize when a different person uses the same browser on a shared device.

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Field
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `first_name`
        *recommended*
      </td>

      <td>
        This should be passed to a marketing tag if the advocate is logged in and their first name is known.
      </td>
    </tr>

    <tr>
      <td>
        `last_name`\
        *recommended*
      </td>

      <td>
        This should be passed to a marketing tag if the advocate is logged in and their last name is known.
      </td>
    </tr>

    <tr>
      <td>
        `email`\
        *recommended*
      </td>

      <td>
        This should be passed to a marketing tag if the advocate is logged in and their email is known.
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`\
        *recommended*
      </td>

      <td>
        This should be passed to a marketing tag if the advocate is logged in. This is your unique identifier for this person such as an account id or member ID.
      </td>
    </tr>
  </tbody>
</Table>

### Track Signups and Purchases

#### Track Signups with Registration Tags

Because your business model requires the friend to create an account, track new account creation with a **registration tag** on your post-signup page. This tag captures that the friend signed up and is eligible for their reward. 

The registration tag passes information about the new customer so Extole can attribute the account to a referral when possible, run quality rules, and run reward rules. This supports accurate tracking when the lead completes a purchase.

Fire this tag only when the created account is **new**. This keeps rewards focused on new customer memberships. 

```javascript Registration Tag
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'registration',
     data: {
       "first_name":"Julio",  // DYNAMIC VALUE
       "last_name":"Friend", // DYNAMIC VALUE
       "email":"julio@friend.com", // DYNAMIC VALUE
       "partner_user_id":"00O40000004SQbO", // DYNAMIC VALUE
       "advocate_code":"ref3lb" // IF USED
     }
  });
</script>
```

> 🚧 Important Note
>
> Make certain that you fire the Extole tag for **all new registrations** so that Extole will correctly attribute registrations and manage the fraud and business rules. Please provide all customer information so that our customer support tools can be used to handle inquiries.

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Field
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `first_name`
      </td>

      <td>
        The first name of the person signing up.
      </td>
    </tr>

    <tr>
      <td>
        `last_name`
      </td>

      <td>
        The last name of the person signing up.
      </td>
    </tr>

    <tr>
      <td>
        `email`\
        **required**
      </td>

      <td>
        The email address of the person signing up.
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`\
        **required**
      </td>

      <td>
        Your unique identifier for this person signing up such as an account ID or member ID.
      </td>
    </tr>

    <tr>
      <td>
        `advocate_code`\
        *recommended*
      </td>

      <td>
        On the registration tag, this is the advocate code that the friend enters to track back to the original advocate. *Must be used on advocate code programs.*
      </td>
    </tr>
  </tbody>
</Table>

#### Track Purchase Events with Conversion Tags

Reward the **advocate** after their friend purchases, not after signup. To do this, add the **conversion tag** to your order thank-you page so Extole receives the purchase event.

The conversion tag passes information about the purchase to allow Extole to attribute the conversion to a referral when possible, run quality rules, and run reward rules. Extole will discard the conversions that are not attributed to a referral after processing rules.

> 🚧 Important Note
>
> Make certain that you fire the Extole tag for **all conversions** so that Extole will correctly attribute conversions and manage the fraud and business rules.

```javascript Conversion Tag
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'conversion',
     data: {
       "first_name":"Julio", // DYNAMIC VALUE
       "last_name":"Friend", // DYNAMIC VALUE
       "email":"julio@friend.com", // DYNAMIC VALUE
       "partner_user_id":"00O40000004SQbO", // DYNAMIC VALUE
       "partner_conversion_id":"00O415320037eWy", // DYNAMIC VALUE
       "cart_value":"20.00", // DYNAMIC VALUE
       "coupon_code":"QA754AZ" // DYNAMIC VALUE
     }
  });
</script>
```

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Field
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `first_name`
      </td>

      <td>
        The first name of the person making the purchase.
      </td>
    </tr>

    <tr>
      <td>
        `last_name`
      </td>

      <td>
        The last name of the person making the purchase.
      </td>
    </tr>

    <tr>
      <td>
        `email`\
        **required**
      </td>

      <td>
        The email address of the person making the purchase.
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`
      </td>

      <td>
        Your unique identifier for this person making the purchase such as an account ID or member ID.
      </td>
    </tr>

    <tr>
      <td>
        `partner_conversion_id`\
        **required**
      </td>

      <td>
        Your order number that uniquely identifies this transaction. Used for customer support tools.
      </td>
    </tr>

    <tr>
      <td>
        `cart_value`\
        **required**
      </td>

      <td>
        On the conversion tag, this is the value of the purchase. Ideally this is the gross cart value before coupons have been applied.
      </td>
    </tr>

    <tr>
      <td>
        `coupon_code`
      </td>

      <td>
        The coupon code that used to make the purchase.
      </td>
    </tr>
  </tbody>
</Table>

#### Track Purchases In Store / Offline

After registration, your new customer's first purchase might be made in store or after a home setup. The conversion, therefore, will need to be sent via an API call that occurs after the offline purchase or via a file delivered through an SFTP connection.

##### Create Extole API Keys

Extole requires API calls from account systems to authenticate with an API identifier in the request header (OAuth key).

Your keys are managed through the [My Extole Security Center](https://my.extole.com/security-center).

Create your first key via the "Create New Access Token" button. My Extole will temporarily display the newly created random key for you.

<Image alt="My Extole Security Center showing the Create New Access Token button" align="center" src="https://files.readme.io/234c9f82ab10c5732e0d7355d542b045aa94a63f946d7afd08c4ef75f3937981-4592d5c-New-Access-Token.png" />

Once your API key is created, you can test successful authentication using the Client API method:

```curl
curl -H "Authorization: Bearer XXXX" https://api.extole.io/v2/me/clients

[
  {
    "client_id": "1",
    "name": "Demo"
  }
]
```

##### Event API Call

Send an API request to Extole for each purchase that occurs in store. You can send the same order by tag and API because Extole automatically deduplicates events based on the order ID.

```json Event API Call
POST https://api.extole.io/v5/events
Authorization: Bearer XXX

{
  "event_name": "purchased",
  "data": {
    "first_name": "Julio",
    "last_name": "Friend",
    "email": "julio@friend.com",
    "partner_user_id": "00O40000004SQbO",
    "order_id": "122948302lala",
    "cart_value": "10000.00"
  }
}
```
```shell Response
{
  "id":"6747711822563808783"
}
```

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Field
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `first_name`
        *recommended*
      </td>

      <td>
        The first name of the person who made the conversion.  

        E.g. Julio
      </td>
    </tr>

    <tr>
      <td>
        `last_name`\
        *recommended*
      </td>

      <td>
        The last name of the person who made the conversion.  

        E.g. Jones
      </td>
    </tr>

    <tr>
      <td>
        `email`\
        **required**
      </td>

      <td>
        The email address of the person who made the conversion.  

        E.g. [julio@friend.com](mailto:julio@friend.com)
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`\
        *recommended*\
        (can be renamed to your id, such as `member_id` or `user_id`)
      </td>

      <td>
        Your unique identifier for this person who made the conversion, such as the member ID. This value should match the value sent in the registration tag.  

        E.g. 00O4000099PDZ1AA
      </td>
    </tr>

    <tr>
      <td>
        `order_id`\
        **required**
      </td>

      <td>
        On the purchased event, this is your order number that uniquely identifies the purchase event.  

        E.g. 122948302lala
      </td>
    </tr>

    <tr>
      <td>
        `cart_value`\
        *recommended*
      </td>

      <td>
        On the purchased event, this indicates the value that will be shown in the Extole dashboard.  

        E.g. 10000.00
      </td>
    </tr>
  </tbody>
</Table>

> 📘 Additional Fields
>
> In addition to the fields above, you can add fields to any event.  
>
> Additional fields added on can be used for:
>
> * Reward Tiering
> * Customer Segmentation
> * Reporting

| Response Field | Description                                                             |
| :------------- | :---------------------------------------------------------------------- |
| `id`           | Indicates the API input event at Extole that can be used for debugging. |

[//]: ___

## Reward your Customers

[//]: # "How do set up rewards for my membership and loyalty referral program with Extole?"

Deliver the advocate reward directly into their account after the friend purchase is approved. Deliver the friend code through an overlay or email after the friend signs up to become a customer. Extole's quality rules automatically approve or decline friend purchases.

### Reward Friends

The friend coupon codes are uploaded into My Extole by your marketing team. You may need to create an easy process for them to generate batches of one-time-use or multi-use coupon codes.

Extole can be configured to pass these coupon codes into your friend landing URL using your parameter to display the coupon code to the friend.

You will then go into My Extole > Rewards to create and upload rewards. 

### Reward using Webhooks

#### Issue Account Credits via Webhook

When an approved conversion occurs, Extole tracks an issued account credit to the account. Configure Extole to make a real-time API call to your system when a reward needs to be issued.

In My Extole, provide a web service name, URL, and shared secret. After each reward is earned, Extole makes an outbound API call to the service name you provided. Never publish a real shared secret or bearer token in documentation or client-side code.

```json Account Credits via Webhook
POST https://YOURWEBHOOK
Authorization: Bearer REPLACE_WITH_SHARED_SECRET
Content-Type: application/json

{
    "type": "reward_earned",
    "event_id": "qb3jju459ugjr2aojk5e",
    "event_time": "2020-05-29T14:14:18.548Z",
    "reward_id": "bf67905b4e1b41daf39c30f0",
    "reward_supplier_name": "Advocate Account Credit",
    "reward_supplier_id": "701e681a9e46c8b6778f3452",
    "partner_reward_supplier_id": "Advocate Account Credit",
    "reward_supplier_type": "CUSTOM_REWARD",
    "person_id": "6816411215104951917",
    "partner_user_id": "1036950000",
    "face_value": 50,
    "face_value_type": "USD",
    "data": [
      "recipient_email": "april@advocate.com"
    ],
    "message": null,
    "schema_version": 1
}
```

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Input Field
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `type`
      </td>

      <td>
        This is the type of event triggering the webhook. When you configure your webhook, select which events to send. The most common event is `reward_earned`.
      </td>
    </tr>

    <tr>
      <td>
        `event_id`
      </td>

      <td>
        Extole’s unique identifier for the webhook event.
      </td>
    </tr>

    <tr>
      <td>
        `event_time`
      </td>

      <td>
        The time stamp of when Extole created the webhook event.
      </td>
    </tr>

    <tr>
      <td>
        `reward_id`
      </td>

      <td>
        The Extole unique identifier for the reward that has been issued.
      </td>
    </tr>

    <tr>
      <td>
        `reward_supplier_name`
      </td>

      <td>
        The friend name for the reward configured in My Extole. This name can be changed by the Marketer.
      </td>
    </tr>

    <tr>
      <td>
        `reward_supplier_id`
      </td>

      <td>
        Extole’s unique identifier for the reward supplier. This will not change, but Extole recommends using the partner reward supplier ID.
      </td>
    </tr>

    <tr>
      <td>
        `partner_reward_supplier_id`
      </td>

      <td>
        This is defined by you and can be any string that helps you identify the reward that you are delivering in your system. Since you are trying to apply account credits to advocate accounts, you might want to make this something like ‘extole\_account\_credit’. If this is not passed, all reward types will be returned.
      </td>
    </tr>

    <tr>
      <td>
        `reward_supplier_type`
      </td>

      <td>
        This is the type of reward going out which will be:\
        `CUSTOM_REWARD` - account credits\
        `MANUAL_COUPON` - coupon code\
        `TANGO_V2` - gift card
      </td>
    </tr>

    <tr>
      <td>
        `person_id`
      </td>

      <td>
        The Extole ID associated with the person who the reward should be delivered to. This can be used to look up more information about that person.
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`
      </td>

      <td>
        A unique identifier providing the reward to the recipient. It is important that all marketing tags include the `partner_user_id`.
      </td>
    </tr>

    <tr>
      <td>
        face\_value
      </td>

      <td>
        The face value of the reward.
      </td>
    </tr>

    <tr>
      <td>
        `face_value_type`
      </td>

      <td>
        The face value type, which could be:\
        3-digit currency symbol (USD, GBP, EUR, etc.)\
        `PERCENT_OFF` (indicates the reward is a percentage off coupon)\
        `CREDITS` (indicates the reward is account credits)
      </td>
    </tr>

    <tr>
      <td>
        `data.recipient_email`
      </td>

      <td>
        The email address of the reward recipient. The `data` object can contain other configurable data about the person or event that caused the reward.
      </td>
    </tr>
  </tbody>
</Table>

### Reward using APIs

#### Issue Account Credits via API

Extole can make rewards available through an API. Schedule a process on your side to call the Extole Rewards API regularly, retrieve rewards earned by each consumer, and apply those rewards to each account.

```json Example: Rewards API Call
POST https://api.extole.io/v2/rewards?state=earned&reward_supplier_type=custom-reward
Authorization: Bearer XXXX
Content-Type: application/json

[
  {
    "reward_id": "6626084585458921557",
    "cause_event_id": "6625713485380188505",
    "reward_supplier_id": "fd6d46833d459fb13071e261",
    "campaign_id": "6624279975852929111",
    "person_id": "6620831314790485965",
    "partner_user_id": "06e2077f-80af-4b67-89cb-2fddd7de0f4f",
    "email": "buttonjanea@aol.com",
    "state": "EARNED",
    "face_value": 9,
    "face_value_type": "USD",
    "partner_reward_id": null,
    "created_at": "2018-11-20T15:12:18.461-08:00"
  }
]
```
```text Response
```

> 🚧 Important Notes
>
> In the call above replace `XXXX` with your access token.

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Input Fields
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `state`
        *recommended*
      </td>

      <td>
        This allows you to filter to all of the rewards that you should be fulfilling.
      </td>
    </tr>

    <tr>
      <td>
        `reward_supplier_type`\
        *recommended*
      </td>

      <td>
        This selects the type of reward Extole will return. Since you are trying to apply account credits to advocate accounts, make sure to specify custom-reward to avoid getting back any friend coupon codes that might be issued.
      </td>
    </tr>
  </tbody>
</Table>

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Output Fields
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `reward_id`
      </td>

      <td>
        The Extole unique identifier for the reward that has been issued.
      </td>
    </tr>

    <tr>
      <td>
        `partner_reward_supplier_id`
      </td>

      <td>
        This is defined by you and can be any string that helps you identify the reward that you are delivering in your system. Since you are trying to apply account credits to advocate accounts, you might want to make this something like ‘extole\_account\_credit’. If this is not passed, all reward types will be returned.
      </td>
    </tr>

    <tr>
      <td>
        `person_id`
      </td>

      <td>
        The ID associated with the person who the reward should be delivered to. This can be used to look up more information about that person.
      </td>
    </tr>

    <tr>
      <td>
        `email`
      </td>

      <td>
        The email address of the intended recipient.
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`
      </td>

      <td>
        A unique identifier that tells you which recipient should receive the reward. Include `partner_user_id` in all marketing tags.
      </td>
    </tr>

    <tr>
      <td>
        `state`
      </td>

      <td>
        This is the state the reward is in. If no state is specified in the API call, all states will return: redeemed, fulfilled, sent, earned, failed, canceled. You should pass "earned" as a parameter in the call to filter by all rewards that need to be fulfilled.
      </td>
    </tr>

    <tr>
      <td>
        `face_value`
      </td>

      <td>
        The face value of the reward.
      </td>
    </tr>

    <tr>
      <td>
        `face_value_type`
      </td>

      <td>
        The face value type, which could be:  

        * 3-digit currency symbol (USD, GBP, EUR, etc.)  
        * PERCENT\_OFF (indicates the reward is a percentage off coupon)  
        * CREDITS (indicates the reward is account credits)
      </td>
    </tr>

    <tr>
      <td>
        `partner_reward_id`
      </td>

      <td>
        This is a reward id that can be specified by you when the reward is created. For account credits, this will likely always be null.
      </td>
    </tr>
  </tbody>
</Table>

#### Fulfill Events via API

Let Extole know that rewards have been fulfilled via an API. Schedule a process on your side that will call into the Extole Events API on a regular basis to share the rewards that have been fulfilled.

```json Example: Events API Call
POST https://api.extole.io/v5/events
{
  "event_name": "reward_fulfilled",
  "data": {
    "reward_id" : "bf67905b4e1b41daf39c30f0",
    "partner_reward_id" : "RewardId123459",
    "message": "successful fulfillment"
  }
}
```
```shell Response
{
  "id":"6747711822563808783"
}
```

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Input Field
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `event_name`
      </td>

      <td>
        `reward_fulfilled`\
        `reward_canceled`
      </td>
    </tr>

    <tr>
      <td>
        `reward_id`
      </td>

      <td>
        The Extole unique identifier for the reward that has been issued.
      </td>
    </tr>

    <tr>
      <td>
        `partner_reward_id`
      </td>

      <td>
        If you have a unique tracking or fulfillment identifier.
      </td>
    </tr>

    <tr>
      <td>
        `message`
      </td>

      <td>
        A reward fulfillment message that appears in customer support.
      </td>
    </tr>
  </tbody>
</Table>

| Response Field | Description                                                             |
| :------------- | :---------------------------------------------------------------------- |
| `id`           | Indicates the API input event at Extole that can be used for debugging. |

> 🚧 Response Field
>
> The API results can contain various IDs that will be ignored. The preferred method to reconcile with Extole is to use your Partner Conversion Id (order number).

### Reward using Files (SFTP)

#### Issue Account Credits via File

When an approved conversion occurs, Extole will track an issued account credit to the account. The earned rewards report will be automatically made available in your account on the Extole SFTP server on a daily basis.

The conversion file can be downloaded from the Extole SFTP system or pushed to your SFTP system.

> 📘 SFTP Resources
>
> [Using Extole's SFTP Server](doc:sftp-and-batch-file-conventions)

Our system uses the following naming convention:\
earned-reward-report-YYYY-MM-DDTHHMMSS.csv

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        CSV Column
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `reward_id`
      </td>

      <td>
        The Extole unique identifier for the reward. This will be used in the fulfillment file to indicate this reward has been fulfilled.
      </td>
    </tr>

    <tr>
      <td>
        `reward_state_transition_time`
      </td>

      <td>
        When the reward transitioned into this state (usually earned) as an ISO time format:\
        e.g. 2021-04-12T10:14:10.163-07:00.
      </td>
    </tr>

    <tr>
      <td>
        `face_value_type`
      </td>

      <td>
        Indicates the face value type such as “USD” or “GBP” or “Points"
      </td>
    </tr>

    <tr>
      <td>
        `face_value`
      </td>

      <td>
        Indicates the value of the reward for example a $50 reward would have a “face\_value\_type” of “USD” and a face value of “50”  

        e.g. 50
      </td>
    </tr>

    <tr>
      <td>
        `campaign_id`\
        *optional*
      </td>

      <td>
        The Extole Campaign Identifier.
      </td>
    </tr>

    <tr>
      <td>
        `campaign_name`\
        *optional*
      </td>

      <td>
        The Marketing Name for the campaign.
      </td>
    </tr>

    <tr>
      <td>
        `reward_supplier_type`
      </td>

      <td>
        The reward supplier type.  Most likely this will be `CUSTOM_REWARD` to indicate an account credit.
      </td>
    </tr>

    <tr>
      <td>
        `reward_supplier_id`\
        *optional*
      </td>

      <td>
        The Extole internal unique identifier for the reward supplier
      </td>
    </tr>

    <tr>
      <td>
        `partner_reward_supplier_id`
      </td>

      <td>
        The reward identifier configured in My Extole. This can be set to any string desired, for example:  

        E.g. `QA-FRIEND-REWARD`
      </td>
    </tr>

    <tr>
      <td>
        `passed_through_reward_state`
      </td>

      <td>
        This indicates the reward passed through this state, but typically the report is set to only return `EARNED` rewards.
      </td>
    </tr>

    <tr>
      <td>
        `current_reward_state`
      </td>

      <td>
        The reward's current state.  Typically the report is set to only return rewards currently in the `EARNED` state.
      </td>
    </tr>

    <tr>
      <td>
        `reward_name`
      </td>

      <td>
        The marketer-friendly name of the reward.  

        E.g. Friend $50 Reward
      </td>
    </tr>

    <tr>
      <td>
        `person_id`
      </td>

      <td>
        The Extole unique identifier for the person.
      </td>
    </tr>

    <tr>
      <td>
        `email`
      </td>

      <td>
        The email address of the recipient of this reward.
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`
      </td>

      <td>
        The `partner_user_id` of the recipient of this reward.  This is your ID for the person, and this ID would have been passed into the program on a tag or event.
      </td>
    </tr>

    <tr>
      <td>
        `first_name`
      </td>

      <td>
        The first name of the person earning the reward.
      </td>
    </tr>

    <tr>
      <td>
        `last_name`
      </td>

      <td>
        The last name of the person earning the reward.
      </td>
    </tr>
  </tbody>
</Table>

#### Fulfill Rewards via File

After the rewards have been fulfilled, you can upload a response file back to the Extole SFTP to transition the reward to fulfilled.

| CSV Column          | Description                                                            |
| :------------------ | :--------------------------------------------------------------------- |
| `event_name`        | `reward_fulfilled`                                                     |
| `reward_id`         | The Extole unique identifier for the reward, which can be ignored.     |
| `email`             | The email address of the person who received the reward.               |
| `partner_reward_id` | A unique fulfillment or tracking ID for the reward in your system.     |
| `message`           | A unique message that displays with the fulfillment in Extole support. |

[//]: ___

## Design your Experience

[//]: # "How do I customize my membership and loyalty referral program with Extole?"

Your entire referral consumer experience can be configured in the My Extole Campaign Editor. This part of setting up the solution can be done entirely by your marketing and creative team and doesn't require technical involvement. Each template is a comprehensive guide for your designer or marketer to customize.

<Image title="Screen Shot 2022-07-28 at 10.32.12 AM.png" alt="My Extole Campaign Editor showing marketer-controlled creative editing options" align="center" src="https://files.readme.io/9a368b70caadecd9a0c101fa6e8beaf512ffd99b631984a7550c2bab8f138235-6724323-Screen_Shot_2022-07-28_at_10.32.12_AM.png">
  Marketer Control Editing
</Image>

[//]: ___

## Integrate with your Mobile App

[//]: # "How do I integrate my membership and loyalty referral program with my mobile app?"

If you have a mobile app, connect it to Extole's API so that:

1. Clicks on shared links from mobile devices open the right landing experience for new customer registration.
2. Extole receives mobile registrations and conversions so advocates can be rewarded.
3. Mobile menu items and account screens include the right CTAs.
4. Customers can share from the app or through native mobile sharing dialogs.

See [Headless and Mobile API](doc:mobile-api) for implementation details.

## Optional: Recommended Additional Steps

### Add Web Analytics Tracking Parameters

[//]: # "How do I add web analytics tracking parameters to my retail referral program with Extole?"

You can set up Extole to send web tracking information to web and email analytics tools with URL parameters, such as UTMs (tracking parameters used by analytics tools). 

URL parameters for Google Analytics, Adobe Analytics, etc. can typically be added directly by your marketing or IT team within Extole's Campaign Editor. 

Within Campaign Edit, configure two URLs: one for the Advocate and one for the Friend.

#### Promote Destination

You can find this under the Advocate tab in Campaign Edit. This controls the behavior of your <Glossary>Promotion Link</Glossary>s. 

When advocates click a promotion link, you can choose to send them to:

* An Extole-hosted zone (such as the advocate Microsite)
* An external URL that you host

In the Advanced settings, you can edit the UTM parameters that are automatically included in the URL.

<Table align={["left","left","left","left"]}>
  <thead>
    <tr>
      <th>
        Parameter
      </th>

      <th>
        Type
      </th>

      <th>
        Description
      </th>

      <th>
        Default Value
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `utm_campaign`
      </td>

      <td>
        dynamic
      </td>

      <td>
        The specific marketing campaign
      </td>

      <td>
        The label of your Extole program  

        Example: `refer-a-friend`
      </td>
    </tr>

    <tr>
      <td>
        `utm_medium`
      </td>

      <td>
        dynamic
      </td>

      <td>
        Type of traffic
      </td>

      <td>
        The channel where the promotion was clicked  

        Examples: `EMAIL`, `WEB`
      </td>
    </tr>

    <tr>
      <td>
        `utm_source`
      </td>

      <td>
        static
      </td>

      <td>
        Where the traffic is coming from
      </td>

      <td>
        `extole_advocate`
      </td>
    </tr>

    <tr>
      <td>
        `utm_content`
      </td>

      <td>
        dynamic
      </td>

      <td>
        The specific promotion
      </td>

      <td>
        The name of the on-site or email promotion that sourced the click
      </td>
    </tr>
  </tbody>
</Table>

#### Share Destination

You can find this under the Friend tab in Campaign Edit. This controls the behavior of your <Glossary>Share Link</Glossary>s. 

When friends click a share link, you can choose to send them to:

* An Extole-hosted zone (such as the Friend Landing Experience Microsite)
* An external URL that you host

In the Advanced settings, you can edit the UTM parameters that are automatically included in the URL.

<Table align={["left","left","left","left"]}>
  <thead>
    <tr>
      <th>
        Parameter
      </th>

      <th>
        Type
      </th>

      <th>
        Description
      </th>

      <th>
        Default Value
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `utm_campaign`
      </td>

      <td>
        dynamic
      </td>

      <td>
        The specific marketing campaign
      </td>

      <td>
        The label of your Extole program  

        Example: `refer-a-friend`
      </td>
    </tr>

    <tr>
      <td>
        `utm_medium`
      </td>

      <td>
        dynamic
      </td>

      <td>
        Type of traffic
      </td>

      <td>
        The share channel used  

        Examples: `EMAIL`, `SHARE_LINK`, `FACEBOOK`
      </td>
    </tr>

    <tr>
      <td>
        `utm_source`
      </td>

      <td>
        static
      </td>

      <td>
        Where the traffic is coming from
      </td>

      <td>
        `extole_friend`
      </td>
    </tr>

    <tr>
      <td>
        `utm_content`
      </td>

      <td>
        dynamic
      </td>

      <td>
        Type of product
      </td>

      <td>
        The product ID
      </td>
    </tr>
  </tbody>
</Table>

### Embed the Advocate Stats Dashboard Directly onto a Page

[//]: # "How do I embed the advocate stats dashboard directly onto a page for my membership and loyalty referral program with Extole?"

To show an advocate stats dashboard on a page after the user is logged in, such as the My Account page, verify the user and tell Extole who they are. 

Complete these two steps:

1. Add an **advocate\_stats\_embedded** tag, which looks exactly like a marketing tag, to the page where you want to serve the creative.
2. Verify consumers so that their data displays: [Verifying Consumers](http://dev.extole.com/docs/verifying-consumers)

[//]: ___

### Embed a Share Experience Directly onto a Page

[//]: # "How do I embed share experience directly onto a page for my membership and loyalty referral program with Extole?"

To embed a sharing experience on a dedicated referral page or account page, use the same structure as a marketing tag and set the zone to `referral_page` or `account_page`.

[//]: ___

### Enable Product Sharing

[//]: # "How do I enable product sharing for my membership and loyalty referral program with Extole?"

If you want to enable your advocates to share specific products, then the product marketing tag may be placed on your category and product pages to allow advocates to share specific categories or products. Extole will read the [Facebook OpenGraph](https://developers.facebook.com/docs/sharing/webmasters#markup) meta tags off of the page and incorporate the product name, description, and image into the share message.

[//]: ___

## Optional: Additional Steps

These steps are not required for most retail experiences, but they may apply to your program.

### Creating your own Advocate Code or Link

[//]: # "How do I create advocate codes or links for my membership and loyalty referral program with Extole?"

Extole automatically creates a unique code for every advocate who joins the program. If you want to create your own customer codes, take these steps: 

1. Create an API access token in My Extole Security Center.
2. Identify the advocate by creating or updating their person profile with `POST /v5/persons` or `PUT /v5/persons/{person_id}`.
3. Check whether the advocate already has a share code with `GET /v5/persons/{person_id}/shareables`.
4. Create a share code with `POST /v5/persons/{person_id}/shareables`.  

[//]: ___

### Use your Opt-out List

[//]: # "How can I use the opt-out list from my membership and loyalty referral program with Extole?"

All emails sent by Extole are CAN-SPAM compliant and honor customer preferences. Referral programs are typically treated as their own email segment, separate from the normal marketing opt-out list, making this step optional. Each email sent to an advocate or friend includes an unsubscribe link, managed by Extole, that opts the customer out of the referral program.

If you need to do a more complex opt-out synchronization, Extole can check your opt-out list with a webhook API or you can upload a list of opt-outs to Extole's SFTP server.

1. Extole Opt-out Check: [Opt Out API](https://docs.extole.com/reference/check-opt-out-status) 
2. File-based Opt-Out List Management: [Opt Out Files](http://dev.extole.com/docs/opt-out-list-management)

[//]: ___

### Upload an SSL Certificate for your Branded Domain

[//]: # "How do I upload an SSL certificate for my membership and loyalty referral program branded domain?"

When you create your branded domain at Extole and notify your CSM, Extole automatically procures a certificate from Let's Encrypt for your domain.

[//]: ___

### Verify Advocate Codes

[//]: # "How do I verify advocate codes for my membership and loyalty referral program with Extole?"

When a potential customer becomes a member of your business, they may go directly to your site and enter an advocate code they received from a friend instead of clicking a referral link. 

A valid advocate code tells Extole to capture the signup and run quality rules for the friend reward. 

If you want your implementation to give customers immediate feedback when they apply a code, call Extole from the code capture field to check whether the code is a valid referral code. 

<Image title="Screen Shot 2016-09-18 at 10.45.11 AM.png" alt="Referral code entry form with a field for entering an advocate code" align="center" width="60% " src="https://files.readme.io/2a70d57cbb1958889db695c4151d19fbc90134bfc6d67ce7763cdd802fecaa63-f09dda3-Screen_Shot_2016-09-18_at_10.45.11_AM.png" />

Implement the code below only if you want to tell the user whether the code is valid before they sign up, similar to a coupon code button on a cart page. 

```javascript Advocate Code Capture Tag
// SCENARIO: A person submitted an advocate code. Verify it is valid, then apply a coupon.

function promptForAdvocateCode() {
    // TODO - implemented by client
}

submitAdvocateCode("ADVOCATE_CODE", function (error, response) {

    if (error) {
        // handle error
        return;
    }

    isRewardable(function (error, response) {
        if (error) {
            //handle error
            return
        }
        applyReward();
    });
});

function isRewardable(callback) {
    extole.require(["core-root:///shared/person-rewardable-service.js"], function (personRewardableService) {
        personRewardableService.isRewardable(callback);
    });
}

function submitAdvocateCode(advocateCode, callback) {
    extole.require(["core-root:///shared/person-relationship-service.js"], function (personRelationShipService) {
        personRelationShipService.createRelationship(advocateCode, callback);
    });
}
```

[//]: ___