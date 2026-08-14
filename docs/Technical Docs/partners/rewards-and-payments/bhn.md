---
title: BHN (Blackhawk Network)
excerpt: >
  Integrate with BHN to reward program participants with open loop and closed
  loop products from BHN's robust catalogue.
---
## Overview

With the Extole and BHN integration, you can drive customer acquisition, generate brand advocacy, and build long-term loyalty with your customers. This powerful integration automates reward fulfillment with real-time reward delivery and offers a wide variety of reward options from Virtual Prepaid Cards to Physical Reloadable Cards for your referral and engagement programs.

## Prerequisites

| Requirement                                    | Description                                                                                                                                                                                                                                                                                                                                                                                           |
| :--------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Enterprise Hawk Marketplace Account            | You must have an Enterprise Hawk Marketplace account in order to leverage this integration.                                                                                                                                                                                                                                                                                                           |
| BHN Merchant ID                                | The unique identifier associated with your BHN account.                                                                                                                                                                                                                                                                                                                                               |
| BHN Client Program Number                      | The unique identifier associated with your BHN program.                                                                                                                                                                                                                                                                                                                                               |
| BHN Payment Method                             | The method you will use to fund your BHN program. Options include ACH and Draw Down.                                                                                                                                                                                                                                                                                                                  |
| BHN FAID Number                                | If you have separate financial accounts within your BHN program, please provide the FAID number where orders should be placed.                                                                                                                                                                                                                                                                        |
| BHN Pre-Production and Production Certificates | The certificates needed to generate your Client Key ID to connect to your BHN pre-production (if applicable) and production environments. Send the password protected certificates to support\@extole.com, or request through your Extole team.                                                                                                                                                       |
| Extole Webhook IP Address                      | The IP address that Extole uses to place orders through the Hawk Marketplace API is listed under [Develop Behind Your Firewall](doc:develop-behind-your-firewall#outbound-file-transfers-and-webhooks). |

## Available Products

### Virtual Prepaid Cards

Virtual Prepaid Cards are a great contactless payment option when you need something fast. They can be used for online and phone purchases anywhere Debit Mastercard and Visa Debit Cards are accepted.Virtual Prepaid Mastercard cards can also be added to popular mobile wallets like Apple Pay, Samsung Pay, and Google Pay.

### Physical Reloadable Prepaid Cards

Reloadable prepaid cards are ideal for companies who want to reward their recipients multiple times throughout the year. They can be used to incentivize program participation by creating cards specific to certain categories, like health and wellness. Additionally, they can be personalized with a company logo and a recognition message to strengthen relationships.

### Virtual Closed Loop (eGift Cards) & Tango Rewards (Reward Link & Disbursement Link)

BHN’s virtual closed loop in addition to Tango's Disbursement (Card Transfer, ACH, PayPal) & Reward Link solutions offer fast, flexible reward delivery for any audience. Choose from eGift cards from popular merchants (Target, Amazon, etc.) or curate digital gift card experiences that can be personalized and branded. These solutions make it easy to drive engagement, loyalty, or compensation at scale, with global reach and real-time delivery.

### Compatible with Reward Bank

BHN card products can also be used within Extole's Reward Bank. Reward Bank gives your advocates a single place to collect and redeem multiple referral rewards. <Anchor label="Learn more about Reward Bank" target="_blank" href="https://www.extole.com/platform/reward-bank/">Learn more about Reward Bank</Anchor>.

## Integration Model

BHN is an outbound reward fulfillment integration: Extole orders cards from BHN when a program participant earns a reward, and BHN's response moves that reward to fulfilled or failed. BHN sends no activity into Extole, so the integration carries no business events.

Each card product is a reward supplier that you install when you create a reward, and you install one per reward you offer. The integration supplies four of them — virtual prepaid cards, physical single-load prepaid cards, physical reloadable prepaid cards, and eGift cards — and each carries its own value, client program number, financial account, and payment type.

Extole calls five Hawk Marketplace endpoints, all on `https://api.blackhawknetwork.com`:

| Purpose                                | Endpoint                                                        |
| :------------------------------------- | :-------------------------------------------------------------- |
| Order a virtual prepaid card           | `/rewardsOrderProcessing/v1/submitVirtualIndividual`             |
| Order a physical single-load card      | `/rewardsOrderProcessing/v1/submitOpenLoopPersonalizedIndividual` |
| Order a physical reloadable card       | `/rewardsOrderProcessing/v1/submitOpenLoopPersonalizedIndividual` |
| Order an eGift card                    | `/rewardsOrderProcessing/v1/submitEgiftIndividual`               |
| Check the status of a submitted order  | `/rewardsOrderProcessing/v1/orderInfo/byKeys`                    |

Order calls are retried over a few hours. The status check runs on a much longer schedule, escalating out to roughly a month, because physical cards are manufactured and mailed rather than delivered instantly.

Ordering a reloadable card is the only call Extole makes for it. The order carries the reward's value, so the card arrives loaded, and BHN's separate <Anchor label="SubmitFunding" target="_blank" href="https://developer.blackhawknetwork.com/hawkmarketplace/reference/dosubmitfunding">`submitFunding`</Anchor> operation — the one that adds money to a card already issued — is not part of this integration. From Extole's side a reloadable card therefore behaves like a single-load card that happens to support reloading later. A program that needs to add value to a card it previously issued does that outside Extole, through BHN directly.

### Reward Connection Contract

Create five `REWARD` webhooks, one for each endpoint above. Each order webhook filters to its matching supplier variant and to `EARNED`, uses `POST`, and has retry intervals `[1800, 3600, 10800]`. The status webhook filters to all four BHN supplier variants and to `FULFILL_FAILED`; its retry intervals are:

```json
[10800, 10800, 86400, 86400, 86400, 86400, 86400, 86400, 86400, 86400, 86400, 86400, 259200, 259200, 259200, 864000, 1296000, 2592000]
```

The exact supplier tags are `internal:bhn-virtual`, `internal:bhn-physical-single-load`, `internal:bhn-physical-reloadable`, and `internal:bhn-egift-card`. Template names use the same tokens without the `internal:` prefix.

#### Map BHN Order Statuses

The status webhook reads `orderStatus` from BHN's <Anchor label="Order Status Reference" target="_blank" href="https://developer.blackhawknetwork.com/hawkmarketplace/docs/get-order-information">Order Status Reference</Anchor>. Map it as follows:

| BHN `orderStatus` | Treat as | Why |
| :---------------- | :------- | :-- |
| `Complete` | Fulfilled | BHN's own final status for a successfully delivered order. |
| `Shipped` | Fulfilled, physical products only | BHN has been notified the card shipped, and moves the order to `Complete` overnight. Real-time eGift and Virtual products never ship, so this status cannot arrive for them. |
| `Cancelled`, `Declined`, `Error`, `Failure` | Failed, terminal | Each is final. Do not retry: the order will not progress, and `Failure` in particular means a real-time order that must be resubmitted as a new order rather than re-checked. |
| `Funding Hold`, `Settlement Error`, `Not All Records Funded`, `Not All Records Reversed`, `Not All Records Processed` | Failed, needs attention | The order is stuck on payment or partially processed. Retrying the status check will not clear it; it needs someone to look at the funding account. |
| `In Process`, `Funding Posted`, `Successfully Sent To Processor` | Still processing | Keep checking until the retry schedule is exhausted. |

`Funding Posted` is the one to get right. It means BHN received the order and will fulfill it shortly — not that the card reached anyone. Marking a reward fulfilled on `Funding Posted` closes it before delivery, so a card that is later cancelled or declined stays recorded as delivered and no retry ever corrects it.

Because the terminal statuses differ by product, define the mapping per supplier rather than once for all four. A physical order passes through `Shipped` on its way to `Complete`; a real-time eGift or Virtual order reaches `Complete` or `Failure` and never sees `Shipped` at all.

Both credentials sit on the integration: the Merchant ID is a plain setting, and the API credential is a client key that Extole generates from the certificates BHN issues you, so it cannot be self-configured.

The integration carries four tabs, and all four are part of the shape rather than optional extras:

| Tab | View type | What it shows |
| :-- | :-------- | :------------ |
| Configuration | `config-view-v10.0` | The Merchant ID and the BHN client key. |
| Reward Suppliers | `config-view-v10.0` | The supplier socket, reporting in progress until a product is installed. |
| Reward Activity | `report-runner-view-v10.0` | A scheduled reward revenue report charting BHN fulfillment. |
| Reward Events | `event-stream-view-v10.0` | A live feed of BHN reward events, tagged `internal:app_type=bhn`. |

The integration's registered image key is `blackhawkNetwork`, and it is not derived from the partner's name or this page's slug. The image key feeds the partner detail view; the tile on the Integrations page comes from the logo setting instead, and BHN's artwork is already published on the registered `bhn` component for both the integration and its four reward products.

Only the v10 integration is current. Build or install that one; the earlier flavor is not a fallback when something in the v10 shape is inconvenient.

### Reward Activity Report Contract

The Reward Activity tab owns one enabled, scheduled report runner. Its account-local report type is named `Reward Revenue`; find that name through `GET /v6/report-types`, and use the returned identifier rather than carrying an identifier from another account. If this account has no type by that name, create a configured type from a parent that accepts metric mappings, with the defaults below, before creating the runner.

| Runner property | Required value |
| :-------------- | :------------- |
| Name | `Partner BHN Reward Revenue Report` |
| Type | `SCHEDULED` |
| Formats | `JSON`, `CSV` |
| Frequency | `WEEKLY` |
| Schedule start | A future timestamp chosen when the runner is created, in ISO-8601 with an offset. A start date in the past leaves the runner enabled and never running. |
| Scopes | `CLIENT_SUPERUSER` |
| Tags | `internal:category:Performance & Metrics`, `partner-graph` |
| Execution policy | `AWAIT_DATA` |
| Attachment | The Reward Activity view, not the integration component |

Its parameters are part of the product contract:

```json
{
  "container": "production",
  "mappings": "date=START_DATE(event.eventTime, period:\"DAY\"); reason=event.data.referral_reason; coupon_used=BOOLEAN_FORMAT(event.data.coupon_codes!=\"null\",\"COUPON USED\",\"NO COUPON USED\");quality=event.quality; count=group_count(event.id, step_name:\"converted\");hidden(reward_id)=LAST(COLLECTION(PERSON(event.data.related_person_id).steps, filter:rootEventId==event.rootEventId, filter: stepName==\"reward_earned\"),sortBy: eventDate).data.reward_id; revenue=GROUP_SUM(event.data.amount, step_name:\"converted\");rewarded=BOOLEAN_FORMAT(reward_id == \"null\",\"UNREWARDED\",\"REWARDED\")",
  "locales": "ALL",
  "time_range": "all_time",
  "campaign_states": "ALL",
  "visit_type": "NEW_TO_CLIENT",
  "unattributed_events": "false",
  "include_totals": "false",
  "quality": "ALL"
}
```

Do not substitute a reward-earned count or reward face value for this mapping: this report charts the conversion revenue and reward relationship that BHN program managers use. The Reward Activity view's `reportColumnsMapping` must use the `date`, `count`, and `revenue` columns this mapping emits.

```json
{
  "chart": { "type": "line" },
  "xAxis": { "column": "date", "type": "datetime" },
  "series": [
    { "name": "Count", "column": "count", "aggregation": "sum" },
    { "name": "Total Spend", "column": "revenue", "aggregation": "sum" }
  ]
}
```

For how this category is built in general terms, see [Integration Categories](doc:integration-categories), [Build a Reward Fulfillment Integration](doc:integration-build-reward-fulfillment) for the sequence, and [Create the Integration Campaign and Component Model](doc:integration-component-model) for the campaign, component, and display metadata every path needs.

## Integration

Complete the following steps to quickly get your integration up and running. Your Extole and BHN teams will support you through this process and answer any questions you may have.

### Enable the BHN Integration

Your Extole team will help you with this process.

1. Select the BHN integration on the Partners center of your My Extole account.
2. Within the BHN integration, hit the Install button to initiate the connection between Extole and BNH.
3. Several required fields will appear where you'll need to provide information such as the Merchant ID and Client Key ID. Your Merchant ID is a unique identifier, provided by your BHN team, that identifies your business within their system. The Client Key ID will be configured by your Extole team.
4. Complete the connection by applying the changes.

### Set up the BHN Reward Supplier from your Rewards page

1. Go to Rewards page in your My Extole account and hit **+ New Reward**.
2. Select the Reward Type—Virtual Card or Physical Card.
3. Specify the name of the reward, the value of the reward, and the Client Program Number and FAID (optional) supplied by your BHN team. You can also get your program number and FAID from the Hawk Marketplace Portal.
4. Select the appropriate Payment Type. Confirm your preferred payment method (ACH Debit or Drawdown) and complete the necessary documentation for setup. This step can be confirmed with your BHN team.
5. Save the configuration and use the newly created reward.

Once the integration is complete, you will be able to see rewards flow in real-time in your My Extole account.


<Image alt="The BHN integration in My Extole showing rewards flowing in real time after setup" src="https://files.readme.io/e465eb6a6fbb58207f2416c21bbe94857c33c8392aa3a3aaecc818c32db3e6a6-1fce53b34f2397e80f7e6a32ee733bfa7eef33fa8717b2c1fddbe950e110dcb8-Screenshot_2024-09-23_at_7.28.10_AM.png" align="center" />


## FAQs

### How can I understand the status of a reward in the Extole platform?

Extole leverages HTTP status codes from BHN API responses to update the status of a card order (aka reward) in the Extole platform. You can use the Extole platform to understand if a reward has been submitted to BHN, if it's been processed and sent to the recipient, or if the reward failed. Refer to the table below for additional information on reward stages in the Extole platform.


<Image alt="Table of Extole reward states mapped from BHN API responses" src="https://files.readme.io/20b5ce8d8ef27ba0362a3bc3266908f35bc75219a9ca702c23f9706dc18fbeb0-77754c9577a4269e8c0b6e247f33fc60754eae832d7eb791659f6fe5a5d7c56f-Screenshot_2025-01-29_at_12.25.21_PM.png" align="center" width="700px" />


Refer to BHN's Developer Documentation for more detailed information on card ordering and response codes for <Anchor label="physical prepaid cards" target="_blank" href="https://developer.blackhawknetwork.com/hawkmarketplace/docs/placing-prepaid-card-personalized-individual-orders#submitting-the-order">physical prepaid cards</Anchor>, <Anchor label="re-loadable cards" target="_blank" href="https://developer.blackhawknetwork.com/hawkmarketplace/docs/reloadable-personalized-prepaid-card-orders#responses">re-loadable cards</Anchor>, and <Anchor label="digital prepaid cards" target="_blank" href="https://developer.blackhawknetwork.com/hawkmarketplace/docs/placing-prepaid-card-personalized-individual-orders#submitting-the-order">digital prepaid cards</Anchor>.

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Reward State in Extole
      </th>

      <th>
        Definition
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `EARNED`
      </td>

      <td>
        Extole has submitted a card order to BHN and is waiting on confirmation from BHN whether the order has been processed or has failed.
      </td>
    </tr>

    <tr>
      <td>
        `TRYING TO FULFILL`
      </td>

      <td>
        BHN has responded to Extole's order request and is processing the card order.

        -Physical Prepaid Single Load cards take up to 2-3 business days to process.

        -Physical Prepaid Re-Loadable Cards take up to 2-3 business days to process the initial card order, and then 24 hours for any subsequent re-loads.

        -Digital Prepaid Single Load Cards take up to 24 hours to process.
      </td>
    </tr>

    <tr>
      <td>
        `SENT`/ `FULFILLED`
      </td>

      <td>
        BHN has successfully processed the order and has sent the card to the recipient via email/post. Physical cards take an additional 7-10 business days to arrive in the mail.
      </td>
    </tr>

    <tr>
      <td>
        `FAILED`
      </td>

      <td>
        BHN was not able to process the order, either due to an improperly formatted request (400), a duplicate request ID (409), or a system error (500).

        Extole's monitoring system will automatically detect failures and triage them into tickets for resolution via the Extole support team. In the case of a 409 (duplicate request ID), Extole Support may re-send the request to BHN with an updated request ID. In the case of a 400 or 500, Extole will reach out to the BHN account manager to cancel the reward and then submit a new order to BHN for processing.
      </td>
    </tr>

    <tr>
      <td>
        `CANCELED/REVOKED`
      </td>

      <td>
        An order has been manually canceled or revoked inside of the Extole platform. This is a manual operation done by the Extole customer support team. Any order canceled in the Extole platform also to be canceled in the BHN Program Modeler patform.
      </td>
    </tr>
  </tbody>
</Table>

### How do I cancel a reward?

By default rewards that are in an `EARNED`, `TRYING TO FULFILL`, or `SENT/FULFILLED` state have either already been delivered to the recipient or are in processing and cannot be canceled inside of the Extole platform. In some cases, you may be able to manually intervene in the BHN platform and attempt to reverse the reward if the recipient has not redeemed the card yet. Please read the following steps to attempt to reverse the reward order in BHN's Program Modeler:

1. Look up the order number for the reward in the Extole platform. The Order number is the `Partner ID` located on the Reward event.

   ![The Partner ID field on a reward event in My Extole, used as the BHN order number](https://files.readme.io/4f1074794c1ec074572cbe8f85bb89d995a1ceb96a365bc76460087d66a96b61-3b82f9cbc43ed16d71e9b5d041dfaea03432a0a386fa6bf73c1a518c0c43f29d-image_2.png)



2. Log in to BHN's program modeler and look up the order number to see if it can reversed. For reloadable cards, reversals must be submitted within the 10‑day window of ordering. For single‑load cards, the card must be unused and at least 30 days prior to expiration.

3. Once you've reversed the reward, navigate back to the Reward in the Extole system and select`Mark as Revoked`if the reward had already been fulfilled, or `CANCEL` if it was in processing.

![The reward actions menu in My Extole with Mark as Revoked and Cancel](https://files.readme.io/5a6dab10439e205aac86884156b97223f34f74dc2194c3fea42d24c133bef5e4-f2f82069cc204caf20dbc8642b6f86ca0f93a0481c5afa8a66d64e4b72ec3764-Screenshot_2025-04-18_at_8.32.38_AM.png)

<br />
