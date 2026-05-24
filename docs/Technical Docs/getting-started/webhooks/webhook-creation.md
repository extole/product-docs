---
title: "Webhook Creation"
excerpt: "Customize the format and authentication method of your webhooks as needed.\n"
---

## Overview

[//]: # "How does Extole user webhooks?"

Extole webhooks submit real-time data about your participants and their journey through programs to your own HTTPS endpoints. Extole webhooks support a variety of authentication methods and can be customized to format the request body in as needed. Our Support Team is available and equipped to help you customize your webhooks.

[//]: ___

<Image align="center" alt="Customer webhooks in the context of a sample journey." caption="Customer webhooks in the context of a sample journey." title="webhooks.png" src="https://files.readme.io/73e8481fa887ec00db6de8942590f08890714df459b9f45a557dd8e33aece0f8-d11a10a-webhooks.png" />

## Webhook Configuration

[//]: # "How do I configure webhooks in Extole?"

Webhooks require configuration within the Extole platform. You may configure your Extole account to use webhooks by logging in and going to <Anchor label="Tech Center" target="_blank" href="https://my.extole.com/tech-center">Tech Center</Anchor> > <Anchor label="Outbound Webhooks" target="_blank" href="https://my.extole.com/tech-center/outbound-webhooks">Outbound Webhooks</Anchor>.

You need to provide the information required for the webhook to know where and how to send your data. At the most basic level, you can configure your webhooks by including:

* Name: How we will refer to the webhook in My Extole
* Client Key: The secret / key used to verify the authenticity of the Extole integration. Client Keys can be created by navigating to the <Anchor label="Security Center" target="_blank" href="https://my.extole.com/security-center">Security Center</Anchor>, clicking + New Key.
* The payload URL: The destination URL the webhook will GET or POST to.
* Description: An optional description for your webhook.

Advanced configuration is also optionally available to allow you more control over the structure and format of the data you’d like to receive in the request. If you need changes to the payload, the events, or the Advanced configuration, please contact your customer success or implementation manager. You can also let your Extole Team know what data you'd like to receive in the request and they can set this up for you.

[//]: ___

## Client Keys & Security

[//]: # "How do I create client keys for webhooks?"

In the My Extole Security Center you can easily create Client Keys for your webhooks. We support HS256 signing, Password, Basic, OAuth, and a variety of vendor-specific variations of OAuth.

These authorization options are configurable within the [Security Center](https://my.extole.com/security-center) in your My Extole account under the Keys section.

[//]: ___

![](https://files.readme.io/f8eed9fb99041fa6c2be2927cb01deaa96090cbb718ba7406df9ee49dbfeef10-7b34069-Screen_Shot_2022-12-14_at_12.15.29_PM.png)

## Webhook Signature Validation

> 🚧 HMAC Validation in Node.js
>
> **We do not recommend using webhook signature validation with Node.js**. Node.js has a habit of changing integer formatting when processing `application/json` responses. Special care should be taken if using Node.js to process the request.

The webhook signs the body of each webhook post with a client-specified secret key, specified with the webhook. The signature is passed as the header `X-Extole-Signature` when the event is posted.

![](https://files.readme.io/ef224ec621750ea77cd6db89af5a5b7bf34e910da52a908f4ed7cdca1e50cf53-b350edc-NewWebook.png "NewWebook.png")

The signature is a hash against the exact string sent in the HTTP request. It does not include the headers and it is not pretty-formatted. It looks like this:

```text
{"type":"reward_earned","event_id":"qb3jju459ugjr2aojk5e","event_time":"2020-05-29T14:14:18.548Z","reward_id":"bf67905b4e1b41daf39c30f0","reward_supplier_name":"Advocate Account Credit","reward_supplier_id":"701e681a9e46c8b6778f3452","partner_reward_supplier_id":"Advocate Account Credit","reward_supplier_type":"CUSTOM_REWARD","person_id": "6816411215104951917","partner_user_id":"1036950000","face_value":50,"face_value_type":"USD","message":null,"schema_version":1}
```

The signature can be calculated against the String of JSON using HMAC256:

```java
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import javax.xml.bind.DatatypeConverter;

private static final String HMAC_SHA_256 = "HmacSHA256";

public String encode(String message, String secretKey) throws Exception {
  Mac algorithm = Mac.getInstance(HMAC_SHA_256);
  SecretKeySpec secretKeySpec = new SecretKeySpec(secretKey.getBytes(), HMAC_SHA_256);
  algorithm.init(secretKeySpec);
  return DatatypeConverter.printHexBinary(algorithm.doFinal(message.getBytes())).toLowerCase();
}
```
```ruby
signature = 'sha1='
  + OpenSSL::HMAC.hexdigest(OpenSSL::Digest.new('sha1'),
    secret, post_body)
```

## Webhook Live View

[//]: # "Where can I see the data and events sent by webhooks?"

Once you have a webhook configured, you'll be able to see a detailed view of it from the [Outbound Webhooks](https://my.extole.com/tech-center/outbound-webhooks) page. Here you will see the top-level details of your webhook as well as a live view of the events happening.

[//]: ___

![](https://files.readme.io/f72286f094cd1f3b1e4684a6ff7f5fb03d6ecdc89575b186fb64e7a0b557bd54-e34327f-webhook-live-view.png)

## Handling 5xx Responses

Webhooks occasionally encounter temporary service disruptions or issues on the receiving (client) side. A response code in the 5xx range (e.g., 500 Internal Server Error, 503 Service Unavailable) indicates a server-side error and must be handled by the client system.

### Receiving A 5xx Response

When you receive a 5xx response, the webhook delivery will be retried based on a predefined retry schedule. However, retries are not guaranteed indefinitely.

You will receive alerts from the Extole system if persistent failures are detected. These alerts are intended to help your engineering team respond promptly to issues in your infrastructure or downstream services.

**It is your responsibility to monitor these alerts and take corrective actions (e.g., fix application errors, scale resources, restore service availability)**.

### Recommendations

1. Implement logging and alerting on your webhook server to capture and diagnose all 5xx responses.
2. Ensure your system can handle concurrent retries or fallback gracefully.
3. Avoid long response times, which may result in timeouts and trigger retries.

By handling 5xx errors effectively on your end, you ensure minimal data loss and uninterrupted integration with Extole's systems. For assistance setting up alert forwarding or retry configuration details, please contact your Extole implementation manager.
