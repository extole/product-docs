---
title: "Braze"
excerpt: "Set up a connection between your Extole programs and Braze's customer-engagement platform.\n"
---

## Overview

[//]: # "Does Extole integrate with Braze?"

Integrating Extole and Braze allows you to pull valuable customer insights from your Extole programs into Braze, empowering you to create more personalized marketing campaigns that boost customer acquisition, engagement, and loyalty. You can also dynamically pull Extole content attributes, such as personalized share codes and links, into Braze communications to turn every customer into a brand advocate.

<Anchor label="Learn more about Braze" target="_blank" href="https://www.braze.com/" />

## Extole Chat and Client API Contract

Braze is a maintained outbound library integration. It is not built from the custom integration template.

When Extole Chat is asked to create a Braze integration:

1. Confirm whether the account already has an active Braze integration. Extend that one when it matches; otherwise continue.
2. Discover the maintained source with `GET /v1/components/duplicatable?having_any_types=integration-v10.0` and select the component named `braze`.
3. Install it the same way the Partners page does: `POST /v1/components/{SOURCE_COMPONENT_ID}/duplicate` with no `target_campaign_id`. That call creates a new `INTEGRATION` campaign whose program label is `braze` and copies the library tree, including the Braze `/users/track` webhook.
4. Do not rebuild Braze from `custom_integration`. Do not invent inbound business events, input-event rules, or ecommerce field capture for Braze.
5. Create a webhook client key only when the requester supplies the Braze REST API key:

```bash
curl -s -X POST -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Braze Integration",
    "type": "WEBHOOK",
    "algorithm": "PASSWORD",
    "key": "'"${BRAZE_REST_API_KEY}"'",
    "partner_key_id": "braze"
  }' \
  "${EXTOLE_API_HOST}/v2/settings/security/keys"
```

6. Configure the installed integration component settings:

| Setting | Purpose |
| :------ | :------ |
| `clientKeyId` | The webhook client key that holds the Braze REST API key. |
| `brazeRestUrl` | Braze REST host for the account's instance, for example `https://rest.iad-01.braze.com`. |
| `externalIdKey` | Expression that identifies the person in Braze. Default is `context.person.email`. |
| `rewardStates` | Reward states forwarded to Braze. Default is `["FULFILLED"]`. |
| `triggerEventNames` | Extra Extole step events forwarded through the generic event child. |
| `enabled` | Master enable for the integration and its webhook. |

7. Read `/v6/webhooks` after install. The event-tracking webhook must target `{brazeRestUrl}/users/track`, carry the `internal:braze:event` tag, and resolve `client_key_id` from `clientKeyId`.
8. Publish the campaign when validation succeeds, unless the requester asked for a draft.
9. Report what remains for a person: Braze REST API key with `users.track`, Braze instance URL, external id mapping, and any extra events or reward states beyond the defaults. Do not offer to replace a marketing program's converted or shipped business events after installing Braze — this integration forwards Extole activity outbound; it does not replace inbound conversion mapping.

The maintained library ships these child controllers under the Braze integration component:

| Child | Listens for | Sends to Braze |
| :---- | :---------- | :------------- |
| `extole_share_link_created` | `advocate_code_created` shareable events | Custom event plus share link attribute |
| `extole_shared` | `shared` step events | Journey-scoped shared event |
| `extole_subscribed` | `opted_in` | Email subscribe attribute `opted_in` |
| `extole_unsubscribed` | `opted_out` | Email subscribe attribute `unsubscribed` |
| `extole_reward` | Reward state changes in `rewardStates` | `extole_reward_{STATE}` event |
| `extole_event` | Events listed in `triggerEventNames` | Prefixed Extole event payload |

[//]: ___

## Prerequisites

[//]: # "What are the requirements for integrating Extole with Braze?"

The table below lists the prerequisites you need to complete this partnership integration.

| Requirement        | Description                                                                                                                        |
| :----------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| Braze Account      | A Braze account is required in order to take advantage of this partnership.                                                        |
| Braze REST API Key | A Braze REST API key with `users.track` permissions can be created within your Braze Settings > REST API Key > Create New API Key. |
| Braze API URL      | Your Braze API URL is specific to your Braze Instance. You can find it [here](https://www.braze.com/docs/api/basics/#endpoints).   |

[//]: ___

## Use Cases

[//]: # "How can I leverage the Extole integration with Braze?"

The following use cases showcase a few ways you can leverage Extole’s integration with Braze. Work with your Extole implementation and customer success managers to develop an option that fits your company’s specific needs.

* Leverage custom events from your referral and engagement programs to trigger a Braze campaign or Canvas
* Create custom segments, dashboards, and reporting using data from your Extole-powered programs
* Automatically unsubscribe or subscribe users to your marketing list in Braze

[//]: ___

## Integration

Complete the following steps to quickly get your integration up and running. Your Extole implementation and customer success managers will support you through this process and answer any questions you may have.

### Create a Key in Extole

In your My Extole account, go to the Security Center and complete the following steps.

Create a new key by clicking the + New Key button.\
Provide the necessary information for the key:

Key Name = Braze Integration\
Key Type = Webhook\
Partner Key ID = N/A\
Algorithm = password\
Key = Your Braze Rest API Key

Save the key.

![](https://files.readme.io/cf654412922ca8461d8655cb52995316410aad0d5c412952108c1388a13d0a7d-0a00e27-image.png)

### Connect to Your Braze Account

1. Select the Braze integration on the [Partners](https://my.extole.com/partners) page of your My Extole account.
2. Within the Braze integration, hit the Install button to initiate the connection between Extole and Braze.
3. Fill out the required fields, starting with the Braze REST API key. The Braze REST API key can be created in your Braze account and should have the `users.track` option selected. This can be created within your Braze Settings > REST API Key > Create New API Key.
4. Enter your Braze API URL. This URL depends on which instance your Braze account is provisioned to. You can find it [here](https://www.braze.com/docs/api/basics/#endpoints).
5. Add any additional Extole events you'd like to send to Braze beyond the defaults. The default events, event properties, and user attributes are described in the [Extole Events table](https://docs.extole.com/docs/braze#extole-program-events) below.
6. Add any additional Reward states you'd like to send to Braze beyond the default `FULFILLED` state. Refer to the [Extole Rewards table](https://docs.extole.com/docs/braze#extole-rewards) below for a description of all available reward states.
7. Select your Braze External ID key mapping, which is how Extole updates user profiles in Braze. You can map the Braze External ID key to Extole's`email_address`or `partner_user_id`for the user.
8. Complete the connection by saving your settings. Once this is done, Extole events will be able to flow into your Braze account.

### Extole Program Events

Below are the default events, event properties, and user attributes Extole will send into Braze. In addition to the default events listed here, you can add any other Extole events to your integration. Please work with your Extole Implementation or Customer Success Manager to identify and add any additional events you would like to send to Braze.

<Table align={["left","left","left","left"]}>
  <thead>
    <tr>
      <th>
        Event Name
      </th>

      <th>
        Event Definition
      </th>

      <th>
        Event Properties
      </th>

      <th>
        User Attributes
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `extole_share_link_created`
      </td>

      <td>
        A participant creates their share link by entering their email in the Extole Share Experience.
      </td>

      <td>
        Email\
        Funnel (advocate or friend)\
        Program
      </td>

      <td>
        Email\
        External ID\
        Share link
      </td>
    </tr>

    <tr>
      <td>
        `extole_shared`
      </td>

      <td>
        A participant shares their referral link with a friend.
      </td>

      <td>
        Email\
        Funnel (advocate or friend)\
        Program\
        Share channel
      </td>

      <td>
        Email\
        First name\
        Last name
      </td>
    </tr>

    <tr>
      <td>
        `extole_outcome` - The outcome is dynamic based on the configuration of your program (e.g., `extole_shipped`, `extole_converted`, etc.)
      </td>

      <td>
        A participant has converted or completed the desired outcome event configured for the program.
      </td>

      <td>
        Dynamic per program
      </td>

      <td>
        Email\
        First name\
        Last name
      </td>
    </tr>
  </tbody>
</Table>

### Extole Subscription States

Below are the default subscription states Extole will send into Braze. 

<Table align={["left","left","left","left"]}>
  <thead>
    <tr>
      <th>
        State
      </th>

      <th>
        Definition
      </th>

      <th>
        Data
      </th>

      <th>
        User Attributes
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `subscribed`
      </td>

      <td>
        A participant has opted-in to receive marketing messages.
      </td>

      <td>
        NA
      </td>

      <td>
        Email\
        List type\
        External ID\
        Email subscribe (opted in)
      </td>
    </tr>

    <tr>
      <td>
        `unsubscribed`
      </td>

      <td>
        A participant has opted-out of receiving Extole email communications.
      </td>

      <td>
        Email\
        External ID\
        Subscription state (unsubscribed)\
        Subscription group ID
      </td>

      <td>
        List type
      </td>
    </tr>
  </tbody>
</Table>

### Extole Rewards

By default, Extole will send reward events in the `FULFILLED` state to Braze so that you can trigger reward notifications via a Braze campaign or canvas. See the table below for additional reward states you may be interested in sending from Extole to Braze.

<Table align={["left","left","left","left"]}>
  <thead>
    <tr>
      <th>
        Reward State (Event Name)
      </th>

      <th>
        Definition
      </th>

      <th>
        Event Properties
      </th>

      <th>
        User Attributes
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `FULFILLED` - Default
      </td>

      <td>
        The reward has been assigned a value (e.g., coupon, gift card, etc.) by an Extole reward supplier.
      </td>

      <td>
        Email\
        Face value\
        Coupon code\
        Face value type
      </td>

      <td>
        Email\
        First name\
        Last name
      </td>
    </tr>

    <tr>
      <td>
        `EARNED`
      </td>

      <td>
        A reward has been created and associated with a person.
      </td>

      <td>
        Email\
        Face value\
        Coupon code\
        Face value type
      </td>

      <td>
        Email\
        First name\
        Last name
      </td>
    </tr>

    <tr>
      <td>
        `SENT`
      </td>

      <td>
        The reward has been fulfilled and has been sent either via email or on a device to the recipient.
      </td>

      <td>
        Email\
        Face value\
        Coupon code\
        Face value type
      </td>

      <td>
        Email\
        First name\
        Last name
      </td>
    </tr>

    <tr>
      <td>
        `REDEEMED`
      </td>

      <td>
        The reward has been used by the recipient, as evidenced in a conversion or  redemption event sent to Extole.
      </td>

      <td>
        Email\
        Face value\
        Coupon code\
        Face value type
      </td>

      <td>
        Email\
        First name\
        Last name
      </td>
    </tr>

    <tr>
      <td>
        `FAILED`
      </td>

      <td>
        An issue has prevented the reward from being issued or sent, requiring attention.
      </td>

      <td>
        Email\
        Face value\
        Coupon code\
        Face value type
      </td>

      <td>
        Email\
        First name\
        Last name
      </td>
    </tr>

    <tr>
      <td>
        `CANCELED`
      </td>

      <td>
        The reward has been deactivated and will return to inventory.
      </td>

      <td>
        Email\
        Face value\
        Face value type
      </td>

      <td>
        Email\
        First name\
        Last name
      </td>
    </tr>

    <tr>
      <td>
        `REVOKED`
      </td>

      <td>
        The fulfilled reward has been invalidated. For example, Extole requested a gift card from a supplier and then subsequently determined that the card was sent in error. If the supplier supports revoking the reward, we would request the funds back and the reward would no longer be valid.
      </td>

      <td>
        Email\
        Face value\
        Face value type
      </td>

      <td>
        Email\
        First name\
        Last name
      </td>
    </tr>
  </tbody>
</Table>

## Customization

### Find and Create Users in Braze

For certain use cases, such as a new email or SMS subscription where Extole does not have an external id (user id) for the user, Extole can check for the user's identifier using Braze's Export User by Identifier endpoint. If the user exists within Braze, Extole will add and update any profile attributes. If the request does not return a user profile, Extole will instead use the User Track endpoint to create a User Alias with the user's email address as the Alias Name.

## Using this Integration

[//]: # "How do I use the Extole integration with Braze?"

After connecting your accounts, events will automatically begin flowing from Extole to Braze without any action on your part. A live view of events being sent to Braze can be found in Extole’s Outbound Webhook Center for troubleshooting. 

![](https://files.readme.io/b743a3b1fdcab7760e996b0cc7471b6607f0e4fc2686016faed197a1b01cab5e-e9550ed-Screen_Shot_2022-04-19_at_5.16.47_PM.png "Screen Shot 2022-04-19 at 5.16.47 PM.png")

[//]: ___
