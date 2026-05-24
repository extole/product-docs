---
title: "Advanced Concepts"
excerpt: "Our JavaScript SDK supports a wide variety of custom use cases and can be tailored to fit the needs and goals of your company. Read about some of our more common advanced tagging scenarios.\n"
---

## Hosting your own CTA

[//]: # "How do I host my own call to action (CTA)?"

If you don't want Extole to fill in the content for a <Glossary>CTA</Glossary> but you still want to make the area or text clickable to pop the <Glossary>Share Experience</Glossary>, complete the following steps. 

**Step 1**\
Navigate to the Marketing tab of the Campaign Editor in your <Glossary>My Extole</Glossary> account.

 **Step 2**\
Disable the toggle for "Serve Creative" to prevent Extole from injecting any content. (Since you are hosting the CTA creative on your end, you do not need to configure any of the creative variables.)

**Step 3**\
Put HTML content onto your web page to display the CTA.

```html
<span class="button" id="extole-header-placement">Refer and get $15</span>
```

**Step 4**\
Insert the zone. Extole will not insert any content on the page, but will instead attach to the click event on the HTML element.

```html
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'global_header'
     element_id: 'extole-header-placement',     
  });
</script>
```

[//]: ___

## Sharing Product Details

[//]: # "How do add product details to Extole tags?"

**When using a placement on your product page, Extole can automatically read in the OpenGraph tags on the page. This means that all you need to do for product sharing is place the standard Extole product tag.**

If you do not have OpenGraph tags on the page (such as for a Single Page App) you need to pass the content information into Extole in the product tag.

**Example product tag**

```javascript
<span id="extole_zone_product"></span>
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

  extole.createZone({
    name: 'product',
    element_id: 'extole_zone_product',
    data: {
      "content": {
        "title":INSERT_DYNAMIC_DATA,
        "image_url":INSERT_DYNAMIC_DATA,
        "description":INSERT_DYNAMIC_DATA,
        "url":INSERT_DYNAMIC_DATA,
        "partner_content_id": INSERT_DYNAMIC_DATA
      }
    }
  });
</script>
```

The following table details the customer information that should be passed into the product tag.

| Product Tag Field            | Description                                                                                                                                                                         |
| :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `content.title`              | The title that appears for the content being shared.                                                                                                                                |
| `content.image_url`          | A public URL for the image of the content being shared.                                                                                                                             |
| `content.description`        | A description of the content.                                                                                                                                                       |
| `content.url`                | The URL of the content. When friends follow a share link, they will be taken back to the content URL instead of the campaign's default landing URL.                                 |
| `content.partner_content_id` | A unique identifier for the content (like an SKU).  This is used to make sure a unique <Glossary>Share Link</Glossary> is created for each piece of content an advocate is sharing. |

[//]: ___

## Sharing Behind Login

[//]: # "How do I make sharing only available behind login?"

When you place CTAs for the <Glossary>Share Experience</Glossary> on pages where the advocate is logged in, you can pass additional profile information about the advocate into the request to personalize the experience.

**Example my account tag**

```javascript
<span id="extole_zone_my_account"></span>
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'my_account',
     element_id: 'extole_zone_my_account',
     data: {
       "first_name":INSERT_DYNAMIC_DATA,
       "last_name":INSERT_DYNAMIC_DATA,
       "email":INSERT_DYNAMIC_DATA,
       "partner_user_id":INSERT_DYNAMIC_DATA,
       "profile_picture":INSERT_DYNAMIC_DATA
     }
  });
</script>
```

The following table details the customer information that should be passed into the my account tag.

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        My Account Tag Field
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
        The person's first name.
      </td>
    </tr>

    <tr>
      <td>
        `last_name`\
        *recommended*
      </td>

      <td>
        The person's last name.
      </td>
    </tr>

    <tr>
      <td>
        `email`\
        **required**
      </td>

      <td>
        The person's email address.
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`\
        *recommended*
      </td>

      <td>
        This is your unique identifier, such as an account ID or member ID.
      </td>
    </tr>
  </tbody>
</Table>

[//]: ___

## Embedding Stats Behind Login

[//]: # "How do I embed referral stats behind login?"

If your referral experience is behind a login and you want to pass the user in a verified context to show embedded stats, this can be done with JWT.  Learn about JWT and other ways for [Verifying Consumers](ref:verifying-consumers).

**Example embedded stats**

```javascript
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'embedded_stats'
     element_id: 'extole_zone_embedded_stats',
     jwt: '0000000000000000'
  });
</script>
```

[//]: ___

## Reporting Promotional Source

[//]: # "How do get the promotion source in Extole tags?"

Extole tags will pass the promotional source of the tag for reporting analytics at Extole. For example, the global header tag would display in reporting as "Global Header." 

It is possible, using tags, to pass in a promotional source that differs from the tag location. This could be used if a single tag, such as `global_header`, is used across multiple agent pages or store location pages and you wish to understand more details about the referral.

**Example promotional source**

```javascript
<script type="text/javascript">
  /* Start Extole */
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  /* End Extole */

   extole.createZone({
     name: 'global_header'
     element_id: 'extole-header-placement',
     data: {
       "source":"store_760"
     }
  });
</script>
```

[//]: ___

## Displaying the Right Language

There are two ways to display the right language to your customers:

1. Extole will read the browser settings of each user and display the correct language (if it exists).
2. You can send in the exact language you want to be displayed for that user based on their selected preferences on your site. 

In order to pass the right language to display, you need to pass the locale in the zone tag or API call for the onsite <Glossary>CTA</Glossary>. The updated tag should look something like following example:

```javascript
\<spanid="extole_zone_global_header"></span>

\<scripttype="text/javascript">

/_ Start Extole _/  
(function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||\[];a\<l.length;)k(l[a++],c[e])})  
(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);  
/_ End Extole _/

extole.createZone({ name: 'global_header', element_id: 'extole_zone_global_header',  
  data: {"locale":"en"}  
} }); </script>
```

When you pass the locale into the promotion or tag, that locale is stored on the user's profile for the next time they visit the site.

## Multiple Countries, Languages & Currencies

If you are running a multi-national program that also has a unique offer or currency, you will want to use locale to specify the language as well as a label for the currency, through on the zone tag:

```javascript
\<spanid="extole_zone_global_header"></span>

\<scripttype="text/javascript">

/_ Start Extole _/  
(function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||\[];a\<l.length;)k(l[a++],c[e])})  
(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);  
/_ End Extole _/

extole.createZone({ name: 'global_header', element_id: 'extole_zone_global_header',  
  data: {  
    "locale":"fr_FR";  
    "labels":"EU"  
} }); </script>
```

## Tagging Single Page Apps & Progressive Web Apps

[//]: # "How do I tag my single page app or progressive web app?"

When developing with a single page app, the HTML of the page is being dynamically modified by JavaScript. In this case, instead of identifying the location of the Extole <Glossary>CTA</Glossary> using an HTML element ID (which can only work once), tags can pass in the JavaScript object of the element where the content should appear.

**Example tag passing in JavaScript object**

```javascript
<span id="extole_zone_global_header"></span>
<script type="text/javascript">
  var headerPlacementElement = $("#extole_zone_global_header");
  
  <!-- Extole Magic Script -->
  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
  <!-- End Extole Magic Script -->

   extole.createZone({
     name: 'global_header',
     element: headerPlacementElement
  });
</script>
```

A similar example for ReactJS might look like this:

```javascript
// For HTML Tag:
// <span id="extole_zone_global_header" ref={extoleRef}></span>

const extoleRef = useRef()
useEffect(() => {

  (function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);

  window.extole.createZone({name: "global_footer", element: extoleRef.current});
}
```

[//]: ___

## Encrypting Tag Data

[//]: # "How do I encrypt tag data?"

Extole tags send information to your referral domain using SSL over AJAX requests. All information is encrypted in transit (under TLS) to Extole, followed by Extole encrypted information at rest using AES-256.

Extole tags do not support hashing of email addresses. Your program will normalize the email address against common fraud/quality issues (e.g., [advocate+1@gmail.com](mailto:advocate+1@gmail.com), [advocate@10minutemail.com](mailto:advocate@10minutemail.com)) as well as domain quality and requires access to the full and correct email address to automatically perform this normalization.

Extole only supports encryption at the transport layer. Your pages should load over SSL and tags will send the data to your program over SSL. Since all data utilized in the tags is data that is typically available for display on your website, there is no additional security exposure by only using transport-encryption.

[//]: ___

## Whitelisting Extole's Resources

[//]: # "How do whitelist Extole?"

If your site makes use of a Content Security Policy, you will need to add the Extole CDN domains and 3rd party domains that are utilized for scripts and content on your site.

Extole may utilize one of two CDN domains, either `extole.io` or `xtlo.net`.  Both are listed in the following CSP.

**CSP domains**

```text
default-src 'self' https://*.extole.io https://*.xtlo.net; 

style-src 'self' 'unsafe-inline' https://*.extole.io https://*.xtlo.net https://fonts.googleapis.com;

font-src 'self' https://*.extole.io https://*.xtlo.net https://fonts.gstatic.com;

script-src 'self' 'unsafe-eval' 'unsafe-inline' https://*.extole.io https://*.xtlo.net; 

connect-src 'self' https://*.extole.io https://*.xtlo.net;

img-src 'self' https://*.extole.io https://*.xtlo.net;
```

[//]: ___

## Adjusting Tag Loading Priority

[//]: # "How do tag loading priority?"

The standard Extole implementation prioritizes having minimal impact to your customers' page load times. Extole does this by using various browser and JavaScript features to load asynchronously and progressively. If your goal is to reduce any page flicker that may occur from loading content from Extole, you can change the way the Extole tags are implemented.

### Core tag

Typically customers will load the Extole core tag at end of the `body` element of a page like this:

```javascript
<script type="text/javascript"
src="https://refer.brand.com/core.js" async></script>
```

This means the core tag will not load until after the full page HTML DOM has been rendered and Extole will load asynchronously while other scripts continue to load. 

To increase the priority of loading the core Extole library the following steps can be taken:

 **Step 1**\
If you are using a tag manager, remove Extole from the tag manager and place it directly into your HTML.

**Step 2**\
Remove the `async` keyword from the tag. This will block the page from loading until the core tag has been fetched and run.

**Step 3**\
Make sure the script is loaded inside the `head` section of your HTML. When used in conjunction with removing the `async` keyword, this will prevent the page content (DOM) from loading until after the Extole script has been initialized.

### Marketing tags

When an Extole Marketing Tag is loaded, it will reference an HTML `element_id` or element on the page. If the element is available it will immediately insert content into it. If the element is not yet available on the page the tag will poll the page to see if the element appears later.

**Option 1**

If your page uses HTML to display the element the tag will look like `<span id="extole_zone_global_header"></span>`  and you should place the createZone tag in the HTML directly, immediately after the span tag, to cause the content to immediately load:

```html
<span id="extole_zone_global_header"></span>
<script type="text/javascript">
(function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
extole.createZone({
  name: 'global_header',
  element_id: 'extole_zone_global_header'
  });
</script>
```

**Option 2**

If you dynamically load content onto the page through Angular, JQuery, or other tools, you'll want to place `createZone` in your JavaScript as soon as the element is created.

```javascript
$( ".inner" ).append( "<p>Test</p>" );
var extoleHeader = $("<span>").attr('id','extole_zone_global_header);
$("#header_menu").append(extoleHeader);
(function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);

extole.createZone({
  name: 'global_header',
  element: extoleHeader
});
```

### createZone Method

The center of tagging with Extole is the `createZone` method. The `createZone` method is used to make a content request to Extole or to track an event in Extole.

Extole includes Magic Script inside each tag. The purpose of the Magic Script is to allow tagging to work before the Extole core tag has been fully loaded. The Magic Script says: "If Extole Core is already loaded, then send messages to Extole. If it is not loaded yet, then store the request so it can fire when Extole is loaded."

The Extole Magic Script should be included with all Extole tags.

```javascript
/* Start Extole */
(function(c,e,k,l,a){c[e]=c[e]||{};for(c[e].q=c[e].q||[];a<l.length;)k(l[a++],c[e])})(window,"extole",function(c,e){e[c]=e[c]||function(){e.q.push([c,arguments])}},["createZone"],0);
/* End Extole */
```

**`createZone`Parameters**

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Zone Field
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `zoneSettings`
        **required**
      </td>

      <td>
        **Plain Object**\
        A map of parameters passed into the zone creation.
      </td>
    </tr>

    <tr>
      <td>
        `createZoneDone`
      </td>

      <td>
        **Function(error,zone)**\
        An optional callback function when the zone request is complete.
      </td>
    </tr>
  </tbody>
</Table>

**`zoneSettings`**

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Zone Field
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `name`
        **required**
      </td>

      <td>
        **String**\
        The name of the zone that will be created and called. These are the names that appear in Extole's Campaign Editor.  

        Typically, tags include promotional CTA zones as well as registration and conversion zones.
      </td>
    </tr>

    <tr>
      <td>
        `element`
      </td>

      <td>
        **Element**\
        An HTML element where any content returned by the zone will be inserted. The element must already exist in the DOM to be able to pass it to Extole as an object. This typically makes sense for Single Page Apps or if you are doing direct development.  

        If the `createZone` tag does not include an `element` or `element_id`, the content will be appended to the end of the page. This is fine for overlays or tracking steps (registration/conversion).  

        Elements can be accessed using pure JavaScript or JQuery. For Example:\
        `document.getElementById("extoleCTA")`\
        `$("#extoleCTA")`
      </td>
    </tr>

    <tr>
      <td>
        `element_id`
      </td>

      <td>
        **String**\
        The ID attribute's value of the element you want to get.  

        An element ID attribute that can be targeted on the page where any content returned by the zone will be inserted. Extole will scan the page DOM on an interval looking for the element with the provided ID attribute. When the element is found, Extole will call the zone and insert the content into the element.  

        If the createZone tag does not include an `element` or `element_id` the content will be appended to the end of the page.  This is fine for overlays or tracking steps (registration/conversion).
      </td>
    </tr>

    <tr>
      <td>
        `data`
      </td>

      <td>
        **Plain Object**\
        An optional list of parameters that are passed into the zone to provide additional context about the person or the event (see table below).
      </td>
    </tr>
  </tbody>
</Table>

**`zoneSettings.data`**

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Zone Field
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
        **String**\
        The first name of the person making the zone request. This is typically the advocate on a CTA zone or the friend on a registration or conversion zone.
      </td>
    </tr>

    <tr>
      <td>
        `last_name`
      </td>

      <td>
        **String**\
        The last name of the person making the zone request. This is typically the advocate on a CTA zone or the friend on a registration or conversion zone.
      </td>
    </tr>

    <tr>
      <td>
        `email`
      </td>

      <td>
        **String**\
        The email of the person making the zone request. This is typically the advocate on a CTA zone or the friend on a registration or conversion zone.
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`
      </td>

      <td>
        **String**\
        A unique user identifier that is provided at the time of registration and conversion.  

        If the user ID is provided at registration, it may be used at conversion for successful tracking of the referral.
      </td>
    </tr>

    <tr>
      <td>
        `partner_conversion_id`
      </td>

      <td>
        **String**\
        A unique conversion identifier that is provided at the time of conversion.  

        If it is provided at conversion it may be used with approvals and fulfillments.
      </td>
    </tr>

    <tr>
      <td>
        `coupon_code`
      </td>

      <td>
        **String**\
        This is the coupon code. It is most commonly used on a registration or conversion tracking call. It will also be used as a method to tie the registration/conversion back to an advocate.
      </td>
    </tr>

    <tr>
      <td>
        `advocate_code`
      </td>

      <td>
        **String**\
        When using an Extole Advocate Code, you can pass the advocate code into any step for the friend (registration, conversion) to create the relationship between the advocate and the friend.
      </td>
    </tr>

    <tr>
      <td>
        `cart_value`
      </td>

      <td>
        **String**\
        Used on a conversion event to track the value of the purchase for revenue reporting.
      </td>
    </tr>
  </tbody>
</Table>

**`createZoneDone(error, zone)`**

This is the JavaScript method that is called when the createZone tag completes. Its use is entirely optional.

| Zone Field | Description                                                                        |
| :--------- | :--------------------------------------------------------------------------------- |
| `error`    | A JavaScript Error object which may contain `message`, `statusText`, and `status`. |
| `zone`     | The newly created Zone object.                                                     |

**`userService.logout()`**

Sometimes it may be required to trigger a logout of the user from the Extole system.  A logout will cause Extole to delete the access token and cookies from all domains, and additionally call the [Delete Token](doc:delete-token) Consumer API which invalidates the token server-side at Extole.

This function requires that the Extole Core JS Library has been loaded on the page.

```javascript
extole.require(['core-root:///common/user-service.js'], function (userService) {
    userService.logout();
});
```

[//]: ___
