---
title: Reward Bank Configuration Guide
excerpt: >-
  By following this guide, you can effectively configure and manage the Reward
  Bank feature, providing users with a flexible and engaging rewards
  experience.  For an overview of the Reward Bank and its key components, see
  the [Reward Bank Overview](./reward-bank).
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
## Integration Steps

### Reward Bank Extension Configuration

> 👍 Improved Email Configuration Coming Soon
>
> Currently, you may need assistance from Support to configure Earned Reward Emails to direct users to the Reward Bank, and to ensure redemption emails are properly triggered.
>
> This limitation will soon be addressed—our team is working on making this functionality fully self-service as part of the out-of-the-box Reward Bank experience.

> 📘 Important Configuration Note
>
> When adding the Reward Bank to the referral flow, ensure all other components are updated to work coherently with it.
>
> For example, webhooks (for triggering rewards), controllers, and any other logic or dependencies tied to reward processing. Failing to update these may result in unexpected behavior or failed reward delivery.

1. #### Configure Dynamic Reward for Redemption
   Create new reward suppliers for redemption rewards with a dynamic 100% back value from the [Account Rewards](https://my.extole.com/account-rewards)  page. These rewards will later be used to configure rewards that users can use to redeem the accumulated rewards (see "[Select Redemption Options](#select-redemption-options)  " section).  
   The "Minimum amount per reward a user can earn" can either be left empty or set to the brand’s minimum requirement (e.g., $0.01 for an Amazon gift card).  
   The "Maximum amount per reward a user can earn" should align with the brand's limit (e.g., $2,000 for an Amazon gift card) or the maximum value of rewards that can be redeemed at a time (this setting will be configured later in the Reward Bank extension).
2. #### Install the Reward Bank Extension:

* Navigate to the **Partners** page > **Extensions** in your Extole account
* Locate and install the **Reward Bank Extension**

<Image align="center" border={false} src="https://files.readme.io/ddb5fc0b32c4d99794c35415a6eb67cb40c4746118e4a8aef597c1377189f7ca-Screenshot_2025-04-14_at_16.40.24.png" />

3. #### Add and Configure Collectible Rewards:

Collectible rewards are the rewards earned for each activity (ex. 15 points when you download the app, or $25 when your referred friend joins).

Collectible rewards are set up and managed only within the Reward Bank extension. If a reward supplier is removed from the system, any rewards issued by that supplier will no longer be available for customers to redeem. Existing rewards can be updated, or new ones can be added as needed.

* Click + New Collectible Reward
* Assign a unique name to the reward; Include the reward value to differentiate (e.g., "Collectible Reward $15")
* Add value and choose the denomination that aligns with your program flow.
* Enable the reward by toggling the "Enable" switch
* Dynamic Value (Optional):  
  Enable the dynamic toggle for percentage-based rewards (e.g., earning a 10% gift card commission on a purchase).  
  Configure the cashback percentage, and set the minimum and maximum dynamic reward amounts that a user can earn per transaction. The reward value will be rounded to two decimal places.  
  Please ensure the maximum is set to a valid amount. The setting is **required** for dynamic rewards. Set the highest amount a user can earn per transaction, based on your campaign rules or reward type limits.

You will use these rewards later on in your campaigns to link them to the rewardable events. See the "Update Program" section for more details on how to integrate these rewards into your promotional strategies.

<Image align="center" border={false} src="https://files.readme.io/80b9ffb24233c8f3c43a68c003693ddebbc3ec6c22d0f1032f93744153ac93c6-image.png" />

<Image align="center" border={false} width="500px" src="https://files.readme.io/66f6b6433ffa7b8705ae700ca7f533edc8858a92facbe3ccda080630d9c1e2de-image.png" />

<br />

4. #### Select Redemption Options:

Redemption options is where you will choose what type of rewards the Collectible points can be redeemed for, such as an Amazon or Visa Gift Card.

Choose previously configured dynamic rewards, not a specific reward amount.

An example of the dynamic reward configuration:

<Image align="center" border={false} width="500px" src="https://files.readme.io/64dcd422f221557f41eb97ab20993175f1e6a981946502ff27fcc99342a9fa79-Screenshot_2025-04-01_at_16.33.34.png" />

5. #### Configure Redemption Parameters:

**Value Limits:**

Set minimum and maximum for monetary redemption amounts. These are based on the dollar amount of the rewards and should align with the maximum reward limits in place by the gift card provider.  
Best Practice: Align with brand limits (e.g., $2,000 for Amazon gift cards)  
Setting to 0 disables specific limits.

**Redemption Rate:**

Define the ratio of earned reward value to dollars, which by default is 1:1, meaning 1 point equals 1 dollar.

Example: With a 10-point ratio, users earn $1 for every 10 points

<Image align="center" border={false} width="500px" src="https://files.readme.io/5947636d41b2040d7d97c7aa83f226a04e8b6e0339f4860167843ad8f3d65bf1-image.png" />

6. #### Save Changes:
   Scroll to the top and save all configuration modifications\ <br />
   ### Customize Reward Bank Creatives
7. #### Update Redemption Emails:
   The Bankable Rewards Redemption Email is sent to customers after they redeem a reward—except for cases where our partner handles the email communication. Click to customize the email templates to match your design preferences, then click ‘Apply’ to save your changes.

<br />

<Image align="center" border={true} src="https://files.readme.io/fd32d0ca637bb638b8f3b3c7dfa84a75c697804bbd89c88fae49f769196dce65-Redemption_Email.png" className="border" />

<br />

8. #### Customize Redemption Center Appearance:

To customize the appearance of the Redemption Center, use the available variables by selecting the "Redemption Center" bundle and clicking 'Apply' to save your changes.  
The "Redemption Center Microsite" simply redirects to the Redemption Center zone, so you only need to update one of them.

<Image border={false} src="https://files.readme.io/fa8e66af7a64065dc9265bf370b78305c84a2758ed31469d214f13f645ca93d1-Screenshot_2025-05-08_at_15.57.33.png" />

<Image align="center" border={false} src="https://files.readme.io/77b82780d8dbfccb107a41302acd95019f36e6e83ead023f642418d7c0f97dae-Reward_Bank.png" />

9. #### Configure Tango Template

This applies only when using Tango Rewards.

To enable the use of Tango Rewards for redemptions, please follow these steps:

* Configure a generic template in the [Tango Rewards Genius](https://www.tangocard.com/rewards-genius-redirect) , or reuse an existing one if it does not contain any hardcoded values.
* Click Reward Bank Tango Gift Card Configuration
* Add the Gift Card Template ID
* Hit 'Apply' to save your changes.

  <Image border={false} src="https://files.readme.io/5bda341cbc63d6d017a844c4a9a3b6bacb62041d31dc63a7fcc74a0e1a0e3a1d-Screenshot_at_Apr_08_14-02-40.png" />

  <Image border={false} src="https://files.readme.io/ba3fe98b9223227625030d201f5ff63d7fd0d47b37e54c5db874fbdb67deb644-Screenshot_at_Apr_08_14-03-16.png" />

### Update Program

10. #### Add Collectible Rewards to the Campaign:

Link the Collectible Rewards to the 'Rules' section of your campaign. For more details on how to add or update the rewards, refer to [Configuring the Rules of Your Program](https://docs.extole.com/docs/configuring-the-rules-of-your-program)

11. #### Update Earned Reward Emails (Optional):

When a customer earns a Collectible Reward, they will receive the Earned Reward email with a link to the Redemption Center. Reach out to Extole Support to configure this email to direct users to the Redemption Center.  
If you have multiple banks, **please contact the Extole Support Team** to configure the email links to target the correct integration (for more details, refer to the **Multiple Reward Banks:** section).  
Extole JWT (JSON Web Tokens) can be used to authenticate users to the Reward Bank via email. Set an appropriate expiration timeframe for the tokens—typically between 1 to 3 years, depending on your reward program’s objectives. For assistance with JWT configuration and email integration, **please contact Extole Support**.

12. #### Publish the campaign.

## Multiple Reward Banks:

For different programs and varying reward types, set up multiple Reward Bank extensions.  Give each Reward Bank a unique name to make identification easier.

When using multiple integrations, include `target=campaign_id:<REWARD_BANK_CAMPAIGN_ID>` in the links leading to the Reward Bank to ensure correct functionality.

Example link:  
`https://test.extole.io/zone/bankable_rewards_redemption_center?target=campaign_id:<CAMPAIGN_ID>&jwt=<JWT_TOKEN>`

## Reporting

Run the following reports to track Reward Bank activity:

**[Reward Bank Redeemed Rewards](https://my.extole.com/reports?category=rewards\&report_type=ssl86aaz9oxefvdlkd7#/)** : Includes the rewards that have been redeemed, along with the associated collectible rewards.

**[Reward Bank Rewards Audit](https://my.extole.com/reports?category=rewards\&report_type=stb2as31j0jpuu091f66#/)** : Provides a detailed log of all collectible Reward Bank rewards, including their current statuses and history.

**[Reward Bank Rewards Summary](https://my.extole.com/reports?category=performance\&metrics\&report_type=ssjvon10iaczu8odl9b7#/)** : Offers an overview of the total reward activity, summarizing key metrics and redemption trends.

## Access Reward Bank

You can provide users access to the Reward Bank either as a standalone page or embedded within your own page:

* Recemption Center - embedable version
* Recemption Center Microsite - standalone page

<Image border={false} src="https://files.readme.io/dcd6243c856849b95c3223b04b6d408d23891b0f67d53e8e1c074547e269d3bf-Screenshot_2025-05-08_at_15.57.33.png" />

The user must access it as a [verified consumer](https://docs.extole.com/docs/verifying-consumers#levels-of-verification).

In case of emails that leads to standalone page, the verification is handled via a JWT token.  
The JWT can be generated within the email creative and appended to the Reward Bank link to authorize the zone call. Example of the link: `https://<Program_Domain>/zone/redemption_center_microsite?jwt=<JWT_KEY>`

Examples:

**Embedded version**

<Image align="center" border={false} width="600px" src="https://files.readme.io/d5cceab42b38acf9716f777811be2e65458f7515bec2ad6999254fdd4c4640bf-image.png" />

**Standalone microsite**

<Image border={false} src="https://files.readme.io/f2a8fdd3a5498a3d02f37bb3b7ff1bb37c746bd457aacc2bd92115cb34d0bff8-Screenshot_2025-04-22_at_15.13.38.png" />

## Headless Integration

For advanced integration scenarios, use the following Reward Bank API endpoints via the Extole Customer API.

To successfully call these endpoints, replace the`client` with your program domain. For example, if Test Company were to call this endpoint, the URL would be:`https://testcompany.extole.io/zone/bankable_rewards`.  
You can find your program domain in the [Tech Center](https://my.extole.com/tech-center) of the <Glossary>My Extole</Glossary> .

### Retrieve Bankable Rewards

A verified JWT or access token is required to retrieve the bankable reward.

```curl
GET <https://client.extole.io/zone/bankable_rewards>
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <VERIFIED CONSUMER ACCESS TOKEN>' \
```

**Example of Response**

```json
[
  {  
    "eligible_rewards": [
      {
        "reward_id": "a1cb349f29057e12025d7a73",  
        "reward_supplier_id": "0c50221129ae1d7231637ae0",
        "face_value": "10.00",  
        "face_value_type": "POINTS"  
      },
      {
        "reward_id": "f8de452d70123a34019b6c8d",  
        "reward_supplier_id": "0c50221129ae1d7231637ae0",
        "face_value": "10.00",  
        "face_value_type": "POINTS"  
      },
    ],  
    "redemption_suppliers": [  
      {  
        "reward_supplier_id": "b6da278e30069f11018e6b96",  
        "name": "Reward 1",  
        "type": "ACCOUNT_CREDIT"  
      },  
      {  
        "reward_supplier_id": "b3e4f4bbb7965e08269f9302",  
        "name": "Reward 2",  
        "type": "ACCOUNT_CREDIT"  
      }  
    ],  
    "redemption_history": [
       {
        "reward_id": "c3d9b56f70481e2301f7a4b2",  
        "reward_supplier_id": "b6da278e30069f11018e6b96",
        "face_value": "20.00",  
        "face_value_type": "USD"  
      }
    ],  
    "reward_parameters": {  
      "face_value_type": [  
        "USD"  
      ],  
      "max_amount": 1000,  
      "min_amount": 0,  
      "ratio_of_value_to_dollars": 1  
    }  
  }
]
```

### Redeem Bankable Rewards

A verified JWT or access token is required to retrieve the bankable reward.

```curl
POST <https://client.extole.io/api/v6/events>
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <VERIFIED CONSUMER ACCESS TOKEN>' \
```

Body:

```json
{
    "event_name": "redeem_rewards",
    "data": {
        "rewards": ["<REWARD ID TO REDEEM>"],
        "reward_supplier_id": "<REWARD SUPPLIER ID USED FOR REDEMPTION>"
     }
}
```

**Example of Response**

```json
[
  {  
		"id":"7436077304245789573" 
  }
]
```

## Appendix:

### Tremendous Rewards

* Tremendous rewards require additional customization in the redemption emails (checkout Customize Reward Bank Creatives > Update Redemption Emails section for details).  
  **Please submit a request to the Support Team for assistance.**

* Additionally, **reach out to Support** to help update/configure the necessary webhooks for the newly added Tremendous rewards on your account.

### Makegood Events Compatibility

The Reward Bank does not support makegood events created from the [Create Event](https://my.extole.com/create-event)  page.

**Alternative Methods for Issuing Additional Rewards:**

* Use [API](https://docs.extole.com/reference/post-generic-event)  events
* Use [file-based](https://docs.extole.com/docs/file-based-events)  events

**Forcing Makegood Events Compatibility:**

To ensure the makegood events compatible with the Reward Bank, use prehandlers to update the "sandbox" parameter:

**Prehandler Condition:**

```json Javascript Function
context.getProcessedRawEvent().getData().get('sandbox') != null && context.getProcessedRawEvent().getData().get('channel') != null && context.getProcessedRawEvent().getData().get('channel').toLowerCase() == "manual"
```

**Prehandler JavaScript Action:**

```json Javascript Function
var sandbox = context.getProcessedRawEvent().getData().get('sandbox');

if (sandbox != null && sandbox.toLowerCase().indexOf('campaign') > -1 && sandbox.toLowerCase().indexOf('production') > -1) {
    var extractedId = sandbox.match(/\d+/)[0];
    context.log(" extractedId ----------->" + extractedId);
    context.getEventBuilder().removeData(sandbox);
    context.getEventBuilder().addData('sandbox', 'production-production');
    context.getEventBuilder().addData('target', 'campaign_id:' + extractedId);
    context.getEventBuilder().addData('journey.campaign_id', extractedId);
}
```

## Notifications

Subscribe to notifications to monitor the redemption process:

| **Parameter**          | **Value**                                                                                |
| ---------------------- | ---------------------------------------------------------------------------------------- |
| **Tags**               | `reward-bank`, `component:<reward bank name` (for filtering specific bank notifications) |
| **Notification Level** | SOME (Warning)                                                                           |

<br />

<Image border={false} src="https://files.readme.io/50616e6867db33f9988b4a04d4453747fb619698ec20d6f220f514f03d64f6fa-image.png" />

<br />

<Image border={false} src="https://files.readme.io/a8770c44da043159fc476812acdb4d76397fa9ad462f35df9ce2090db089a65e-image.png" />