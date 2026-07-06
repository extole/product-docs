---
title: Customer Appreciation Program
deprecated: false
hidden: false
metadata:
  robots: index
---
Customer Appreciation campaigns let you send a reward to a customer as a simple thank you — no referral or purchase required. Use this when you want to recognize loyal customers, say thanks after a support interaction, or run a one-off or batch reward send outside of your usual referral flow.

## Overview

A Customer Appreciation campaign uses the same **Program** structure as other Extole Offer campaigns, but is built around a template designed for direct reward sends. You can send rewards one at a time through **User Support**, or in bulk through **Batch Jobs**.

## Prerequisites

- Access to **My Extole**
- A reward set up and ready to attach to the campaign
- Gift card funds - if this is your first time rewarding with gift cards, reach out to your CSM to get an invoice.&#x20;

## Launch Steps

1. **Create the program.&#x20;**&#x46;rom My Extole, select **+ New Program** and choose the **Customer Appreciation** template.

2. **Create a new reward.** Navigate to the Rewards section and set up the reward you want to send (gift card, coupon, etc).

3. **Add the reward to the campaign.** In the campaign, click into the Customer Appreciation Reward and choose the new reward you've just created.

4. **Configure reward delivery.**
   - By default, a Tango gift card is enabled. Work with your CSM to create a new email template and add that template ID to the campaign.
   - If you're using **Tremendous** or **BHN** rewards instead, add the **Reward Emails** component to the **Reward Delivery** section of the flow and customize the emails there.

5. **Set campaign live.**
   - Once your campaign is set up, publish the campaign and set it live.

6. **Send a one-off reward.**
   - Go to **User Support**.
   - Select **Create Event**.
   - Choose the relevant program and campaign.
   - Enter the recipient's email address and first name (if your template uses it).

7. **Send batch rewards.**
   - Go to **Batch Jobs** and upload a CSV of recipients using the Customer Appreciation upload template (`event_name`, `email`, `first_name`).
   - If you rename the event from `customer_appreciation` to something else in the campaign, update the `event_name` value in your upload file to match.

     Example upload format:
     | event\_name                    | email                                             | first\_name |
     | ------------------------------ | ------------------------------------------------- | ----------- |
     | customer\_appreciation\_reward | [example@example.com](mailto:example@example.com) | Cate        |

8. **Confirm rewards were sent.** In **User Support**, look up the participant's profile. The reward should appear on their profile once issued.

## Things to Note

**Running Multiple Campaigns** If you create additional campaigns from this template (for example, a seasonal or promotional send), give each one a unique event name — e.g., `customer_appreciation_summer_promo` so batch uploads route to the correct campaign.

**Utilize Reward Bank** These types of offers fit very well with Extole's Reward Bank. Prompt customers to redeem their rewards before sending them out in bulk. Learn more here.&#x20;

## Related Resources

- Work with your CSM for reward template setup and gift card funding
- See your Batch Jobs documentation for full upload template requirements

<br />
