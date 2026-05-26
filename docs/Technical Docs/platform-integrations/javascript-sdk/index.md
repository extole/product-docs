---
title: "JavaScript SDK"
excerpt: "Extole's JavaScript SDK is integrated into your online experience by placing simple JavaScript tags on web pages to allow program optimization without additional development.\n"
---

## Overview

[//]: # "What are Extole tags?"

Our JavaScript SDK consists of three tag types:

1. **Core Tag**: Contains Extole's JavaScript library. It must be placed once on every page where Extole will operate.
2. **Marketing Tags**: Placed throughout your site to mark the locations where you want to serve promotional content like "Refer and Get $20."
3. **Event Tags**: Used to track and reward on specific user actions like register and purchase.

[//]: ___

## Core Tag

[//]: # "What is the core tag and how do I use it?"

Extole's JavaScript library must be placed on all of your pages using the core tag. This tag is used to activate the Extole system and ensures that any other Extole tags on your page work properly. It also detects when someone has come to your page through a referral and automatically serves the friend landing experience.

### Find and place your core tag

The Extole core tag may be placed anywhere on the page. This tags uses the `async` keyword to ensure fast page loading.

The core tag can be found under your program’s branded domain (`share.brand.com`). If you haven't set up your branded domain yet, you can load the tag from the Extole unbranded domain.

> 📘 Related Content
>
> * [Find your domain in the settings page of My Extole](https://my.extole.com/settings)
> * [How to set up your program domain](https://docs.extole.com/docs/program-domain-setup)

Find your active referral domain and use that for your core tag. It will look like `brand.extole.io` (unbranded) or `share.brand.com` (branded).

```javascript
<!-- BRANDED -->
<script type="text/javascript" src="https://share.brand.com/core.js" fetchpriority="high" async></script>

<!-- UNBRANDED -->
<script type="text/javascript" src="https://brand.extole.io/core.js" fetchpriority="high" async></script>
```
```text Injection
var extoleScript = document.createElement('script');
extoleScript.setAttribute('type', 'text/javascript');
extoleScript.setAttribute('async', 'async');
extoleScript.setAttribute('src', 'https://brand.extole.io/core.js');
document.getElementsByTagName('body')[0].appendChild(extoleScript);
```

[//]: ___

### Verify your core tag performance

Make sure your core tag is functioning properly by checking the Network tab of your Javascript Console for`/zones` in your program domain. If your campaign content displays as expected within the zone, you're good to go. 

#### Troubleshooting

Please reference the table below for troubleshooting issues with your core tag.

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>
        Problem
      </th>

      <th>
        Cause
      </th>

      <th>
        Solution
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        No CTAs load and errors mentioning CORS are visible in the console.
      </td>

      <td>
        Check the spelling of the core tag on the client's site matches spelling in the branded domain section of your [Tech Center](https://my.extole.com/tech-center).
      </td>

      <td>
        Go to the [Tech Center > Tag Generator](https://my.extole.com/tech-center/tag-generator) and copy the core tag.
      </td>
    </tr>

    <tr>
      <td>
        Seeing the error net: `ERR_CONNECTION_TIMED_OUT`\
        when trying to load the core tag.
      </td>

      <td>
        The program domain has not yet been created in your My Extole account.
      </td>

      <td>
        Create the program domain you are trying to use in your [Tech Center](https://my.extole.com/tech-center).
      </td>
    </tr>

    <tr>
      <td>
        Seeing the error net: `ERR_CERT_COMMON_NAME_INVALID`\
        when trying to load the CTA tag.  

        Running multiple DIG commands consecutively return different answers.
      </td>

      <td>
        The CNAME was not properly created. (Most likely created as an A record and not a CNAME.)
      </td>

      <td>
        You will have to create the record as a CNAME.
      </td>
    </tr>
  </tbody>
</Table>

## Marketing Tags

[//]: # "How do Extole marketing tags work and how do I add them to my site?"

In order to drive participation, Extole displays <Glossary>CTA</Glossary>s that promote the program. For example, the overlay CTA will add a floating element to the screen that will say something like “Refer a friend” and when clicked will show the share experience.

Marketing tags tell Extole where to serve CTAs onto your website. These CTAs are clickable entities that advertise your program to your customers and visitors. These marketing tags also enable tracking, so that you can know which marketing placements are driving participation in the program.

Your Extole referral campaign comes with standard marketing tags, which you can enable or disable in the Campaign Editor of your My Extole account.

A few marketing tag examples are:

* `global_header`
* `global_footer`
* `confirmation`
* `overlay`

It's easy to create additional marketing tags if you want to add CTAs to additional pages like your blog, help pages, and so on. As you're getting started, contact your Customer Success Manager to learn how to create these additional tags.

### Global header

The global header tag is placed in the header on all pages of your site, both desktop web and mobile web.

#### Example global header tag

```javascript
<span id="extole_zone_global_header"></span>
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'global_header',
     element_id: 'extole_zone_global_header'
  });
</script>
```

### Global footer

The global footer tag is placed in the footer on all pages of your site, both desktop web and mobile web.

#### Example global footer tag

```javascript
<span id="extole_zone_global_footer"></span>
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'global_footer',
     element_id: 'extole_zone_global_footer'
  });
</script>
```

### Product

The product tag is placed on your category page and product page to allow your customers to share specific categories or products. Extole will read the Facebook OpenGraph meta tags off of the page and incorporate the product name, description, and image into the share message.

#### Example product tag

```javascript
<span id="extole_zone_product"></span>
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'product',
     element_id: 'extole_zone_product'
  });
</script>
```

### Confirmation

The confirmation tag is placed on the order confirmation page. Since the customer has just made a purchase and their identity is known, you should pass in information about the customer.

#### Example confirmation tag

```javascript
<span id="extole_zone_confirmation"></span>
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'confirmation',
     element_id: 'extole_zone_confirmation',
     data: {
       "partner_user_id": INSERT_DYNAMIC_DATA,
       "email": INSERT_DYNAMIC_DATA,
       "first_name": INSERT_DYNAMIC_DATA,
       "last_name": INSERT_DYNAMIC_DATA,
     }     
  });
</script>
```

The following table details the customer information that should be passed into the confirmation tag.

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Confirmation Tag Field
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
        The person's first name. This is used for personalization and client customer support lookups.
      </td>
    </tr>

    <tr>
      <td>
        `last_name`\
        *recommended*
      </td>

      <td>
        The person's last name. This is used for customer support lookups.
      </td>
    </tr>

    <tr>
      <td>
        `email`\
        **required**
      </td>

      <td>
        The person's email address. This is used for quality detection (self referral, bad domains), referral matching, and optionally to trigger program alerts and promotions.
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`\
        *recommended*
      </td>

      <td>
        Your unique identifier for this person making the purchase such as an account ID or member ID. This is used to detect uniqueness, quality, and can help match if people switch emails.
      </td>
    </tr>
  </tbody>
</Table>

### Embedding the share experience on a referral page

In addition to <Glossary>CTA</Glossary>s, Extole also provides placements that will directly embed a <Glossary>Share Experience</Glossary> into a page on your site. It is valuable to have a dedicated referral page to capture SEO traffic for customers searching for your program. This page usually has a URL like this: `www.brand.com/share`.

#### Example embedded share experience tag

```javascript
<span id="extole_zone_embedded_share_experience"></span>
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'embedded_share_experience',
     element_id: 'extole_zone_embedded_share_experience'
  });
</script>
```

[//]: ___

## Add Event Tags

[//]: # "How do Extole event tags work and how do I add them to my site?"

### Registration

The Extole registration tag is used to track the flow when the friend initially creates an account but the actual conversion (purchase, account opening, etc.) takes place at a later time. The registration tag allows Extole to properly track the first step of the friend funnel and tie it back to the advocate.

> 👍 Registration Tag Usage
>
> The registration tag is typically **not** used in a retail referral program, but is common for consumer services, subscriptions, account openings, and lead generation.

> 📘 Partner User ID
>
> Partner user ID is used to uniquely identify the user. This way when a conversion is later sent to Extole with the same partner user ID, Extole is able to properly attribute it back to this friend and to the referral.

#### Example registration tag

```html
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'registration',
     data: {
       "first_name": INSERT_DYNAMIC_DATA,
       "last_name": INSERT_DYNAMIC_DATA,
       "email": INSERT_DYNAMIC_DATA,
       "partner_user_id": INSERT_DYNAMIC_DATA
     }
  });
</script>
```

The following table details the customer information that should be passed into the registration tag.

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Registration Tag Field
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
        The person's first name. This is used for personalization and client customer support lookups.
      </td>
    </tr>

    <tr>
      <td>
        `last_name`\
        *recommended*
      </td>

      <td>
        The person's last name. This is used for client customer support lookups.
      </td>
    </tr>

    <tr>
      <td>
        `email`\
        **required**
      </td>

      <td>
        The person's email address. This is used for quality detection (e.g., self referral, bad domains), referral matching, and optionally to trigger program alerts and promotions.
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`\
        *recommended*
      </td>

      <td>
        Your unique identifier for this person creating the account such as an account ID or member ID. This is used to detect uniqueness, quality, and can help match if people switch emails.
      </td>
    </tr>
  </tbody>
</Table>

### Conversion

Most programs reward advocates when a conversion event occurs, such as a purchase. This can be communicated to Extole by adding the conversion tag to the conversion confirmation page on your site.

The conversion tag should pass information about the conversion to allow Extole to run  applicable rules and attribute the conversion to a referral when possible.

> ❗️ Important Note
>
> Make certain that you fire the Extole tag for **all conversions** so that Extole will correctly attribute conversions and manage the fraud and business rules. Extole ignores conversions that are not attributed to a referral after processing rules.

> 📘 Order ID
>
> Order ID is used to uniquely identify the user's transaction. It is typically the order number of the purchase. Extole imposes a limit of 38 characters.
>
> By passing in order ID, this identifier can be used at the time of approval or cancelation.

#### Example conversion tag

```html
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'conversion',
     data: {
       "first_name":INSERT_DYNAMIC_DATA,
       "last_name":INSERT_DYNAMIC_DATA,
       "email":INSERT_DYNAMIC_DATA,
       "partner_user_id":INSERT_DYNAMIC_DATA,
       "order_id":INSERT_DYNAMIC_DATA,
       "cart_value":INSERT_DYNAMIC_DATA,
       "coupon_code":INSERT_DYNAMIC_DATA
     }
  });
</script>
```

> 🚧 Retail: Email in guest checkout
>
> Please note that a guest checkout flow is slightly different and the logic used to pass the email address on the conversion tag needs to accommodate both a logged in account as well as a guest checkout.

The following table details the customer information that should be passed into the conversion tag.

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Conversion Tag Field
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
        The person's first name. This is used for personalization and client customer support lookups.
      </td>
    </tr>

    <tr>
      <td>
        `last_name`\
        *recommended*
      </td>

      <td>
        The person's last name. This is used for client customer support lookups.
      </td>
    </tr>

    <tr>
      <td>
        `email`\
        **required**
      </td>

      <td>
        The person's email address. This is used for quality detection (self referral, bad domains), referral matching, and optionally to trigger program alerts and promotions.
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`\
        *recommended*
      </td>

      <td>
        Your unique identifier for this person making the purchase such as an account ID or member ID. This is used to detect uniqueness, quality, and can help match if people switch emails.
      </td>
    </tr>

    <tr>
      <td>
        `order_id`\
        **required**
      </td>

      <td>
        Your order number that uniquely identifies this transaction.
      </td>
    </tr>

    <tr>
      <td>
        `cart_value`\
        **required**
      </td>

      <td>
        The value of the purchase. Ideally this is the gross cart value before coupons have been applied. This is used to let you view and analyze the revenue generated from your referral program.
      </td>
    </tr>

    <tr>
      <td>
        `coupon_code`\
        **required if available**
      </td>

      <td>
        The coupon code that may have been used to make the purchase.
      </td>
    </tr>
  </tbody>
</Table>

[//]: ___
