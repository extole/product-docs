---
title: "Configure Common Reward Scenarios for Credit Unions and Banks"
excerpt: "💡 Important Note: This guide only applies to flow campaigns that use Extole's upgraded Flow Builder. Check for the flow icon next to your campaign name.\n"
---


>

> 💡 **Important Note:** This guide only applies to flow campaigns that use Extole's upgraded Flow Builder. Check for the flow icon next to your campaign name.

>

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/2112632465/88f0ece8ae0f8a56831a5e7031d2/Screenshot-2B2025-08-15-2Bat-2B08_43_12.png?expires=1778306400&signature=2c40483e32b87852dc2016280e87bbefa6d67c051a5c36f85b87fd2737017c2d&req=diEmFM99n4VZXPMW3nq%2BgVWxyDC04WKpNDSZyZIyxGFnJ8FzeCJwCL9guX8f%0Aij9KigbYO6C%2F0%2BUt2ojSl7GAt6U%3D%0A)

# Overview

> This article outlines common reward configuration patterns used by credit unions and banks in Flow Builder. These scenarios reflect typical event structures and qualification ownership models when the **client is managing the qualifications.**

> Use this guide to determine which reward rule setup best aligns with your data flow and reward requirements.

>

# **Before You Begin: Who Handles Qualification?**

> In most bank and credit union implementations, the FI performs qualification on their side and sends an **"account qualified"** event to Extole.

> If Extole is evaluating qualification logic (10 direct deposits, $1,000 reward balance), additional reward rules are required.

>

# **Scenario 1: Rewards Sent Immediately upon Account Qualification - No Time Limit**

## **Overview**

> The bank or CU performs all qualification checks internally and sends an **"account qualified"** event once the account meets their criteria. The reward is triggered immediately upon receipt of this event.

>

> This is the most common implementation.

>

## **Flow Builder Configuration**

1. **[Add a reward](doc:how-to-add-a-new-reward)** on the **"Account Qualified"** event.

  1. Advocate and friend rewards are enabled by default in Extole’s Refer a Member template with this configuration

2. Adjust any other **[reward rules](doc:how-to-set-up-reward-rules)** (Annual Reward Value Limit, etc)

## **When to Use This Setup**

- The bank or CU owns qualification logic.
- No pending period or time-bound validation is required in Extole.

>

# **Scenario 2: Rewards Sent X Days after Account Opening**

## **Overview**

> The bank or CU sends an **"Account Opened"** event, but does not send a qualification event. Extole determines qualification based on a required pending period, such as keeping the account open for 90 days. The reward is delayed until the pending period has elapsed.

>

> **This is often paired with an event like Account Closed (see Preventing Rewards with Negative Outcomes below).**

>

## **Flow Builder Configuration**

1. **[Add a reward](doc:how-to-add-a-new-reward)** on the **"Account Opened"** event.
2. Click into the Reward and + New Reward Rule
3. Choose **Pending Period** and click Add
4. Under Pending Period, choose the length of time that will delay the reward

  1. By default it will start the pending period from the event of the reward, which in most cases is **Account Opened**
  2. Update the name and description of this rule to call out the time period (ex. “90 Day Pending Period)

5. Adjust any other **[reward rules](doc:how-to-set-up-reward-rules)** (Annual Reward Value Limit, etc)

>

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/2112631115/3857c08c340386e1bca3e8a6da58/20cd7bc2-abb5-4bd6-af76-4cb0fa549a73?expires=1778306400&signature=11dfd565241effb1e66ddf73528266ae024af636d9177e255da6fb6750d99284&req=diEmFM99nIBeXPMW3nq%2BgWSwby4lfDDH6887YDTA9Rn7jxmBCrjdnr2V2jgj%0AUf55ni9lyBmiUJZxl4G4M0afXn8%3D%0A)

>

## **Preventing Rewards for Negative Outcomes**

> A common use case with this scenario is to also include an event that disqualifies a person from reward. For example, you will earn a reward if you opened an account and did not close the account within 90 days.

> If the client sends negative lifecycle events such as **"Account Closed"**, you can combine:

- **Pending Period**, and
- **Has Not Taken Action**

> Use **Has Not Taken Action** to ensure that if the negative event occurs within the defined pending period, the reward rule fails and the reward is not issued.

## **Flow Builder Configuration**

1. **[Add a new business event](doc:how-to-add-a-new-business-event)** and rename it to match the input event (example “account_closed”
2. Add the reward and pending period as indicated above
3. Click into the Reward and + New Reward Rule

  1. For friend rewards, choose **Has Not Taken Action**
  2. For advocate rewards, choose **Other Person Has Not Taken Action**

4. Update the name and description to describe the rule (ex. Has Not Closed Account)
5. Choose the Business Event that disqualifies them for reward (ex. Account Closed) and the Recent Activity Window (matches pending period)
6. Adjust any other **[reward rules](doc:how-to-set-up-reward-rules)** (Annual Reward Value Limit, etc)

>

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/2112631116/3f059e3860dc53b3428d760158cb/1969a18a-3f44-4f7a-8f7b-a829c29f7c9a?expires=1778306400&signature=6be8a0d503a5aa7898e115a7ef6fdcbd6e93ef17b28ca29858acbf937d3f1f4b&req=diEmFM99nIBeX%2FMW3nq%2BgbqInq2IIkW9nd8UNb%2BWRVRcKWr4ggvRTfEhXw7K%0ALxc0RQWuEZkhOl%2BDxYVD4C0wBY4%3D%0A)

## **When to Use This Setup**

- The bank or CU does not send a qualification event.
- A holding period is required before issuing rewards.
- A negative event is sent to Extole that should disqualify the participant from reward

>

# **Scenario 3: Rewards Sent Immediately upon Account Qualification - Specific Time Limit**

## **Overview**

> This is a similar set up as Scenario 1, however, qualification must occur within a **defined time frame**. For example, the account must be qualified within 90 days of account opening.

>

> Once the qualification event is received and validated within the time window, the reward is sent immediately. If the Account Qualified event is sent more than 90 days after account opening, the reward will not be sent.

>

## **Flow Builder Configuration**

1. **[Add a reward](doc:how-to-add-a-new-reward)** on the **"Account Qualified"** event.

  1. Advocate and friend rewards are enabled by default on Account Qualified in Extole’s Refer a Member template

2. Click into the Reward and + New Reward Rule
3. For friend rewards, choose **Has Taken Action** and for advocate rewards, choose **Other Person Has Taken Action**

  1. Update the name and description to describe the rule (ex. Has Opened Account in Last 90 Days)
  2. Choose the Business Event that qualifies them for reward (ex. **Account Opened**) and the Recent Activity Window (period of time since the account was opened)

4. Adjust any other **[reward rules](doc:how-to-set-up-reward-rules)** (Annual Reward Value Limit, etc)

## **When to Use This Setup**

- The bank or CU sends a qualification event.
- Qualification must occur within a defined time window.
- Rewards should be issued immediately after qualification, but not if it’s passed the defined window

>

# **Sending Different Rewards Based on Account Type**

> In some programs, the reward varies based on account type, such as checking versus mortgage. The preferred method is to create multiple business events each with their own associated reward.

>

> The three primary configurations needed are creating events for each product type opened, adjusting the Input Event trigger rule to use Account Opened, and adding a trigger rule to only trigger if it’s a specific product type that is opened.

>

## **Flow Builder Configuration**

1. **[Add a new business event](doc:how-to-add-a-new-business-event)** and rename it to match the event that is happening

  1. "Mortgage Account Opened"
  2. "Checking Account Opened"

2. Under the **Data** section, click + New Data and choose Business Event Data

  1. Rename the data to match the column / parameter name exactly (ex. Product Type)

3. Under the **Trigger Rules** section, click into the “Triggered By..” rule

  1. By default this will match the name of the business event, but in most cases both events are being triggered by the same account opened event. 
  2. Find the **Trigger Event Names** value and click the three dots
  3. Under “ **Values** ” delete the default value that is there (ex. mortgage_account_opened), and **add account_opened**

    1. This means that the event will be triggered by the account opened input event

  4. Save and apply changes

4. Go back to the business event and under **Trigger Rules**, click + New Rule

  1. Add **Event Data Comparison** and rename the rule to align with the product type
  2. **Event Parameter** is the name of that column in the file we are looking for (ex. product_type) and the **value** is the exact match it will look for (ex. Mortgage)

5. **[Add any associated rewards](doc:how-to-add-a-new-reward)** or other qualifying events that should be triggered
6. Follow these steps for as many different products as you’d like.

## **Summary: Choosing the Right Configuration**

| > **Scenario** | > **Events Sent by Client** | > **Reward Rule** | > **Reward Timing** |
| --- | --- | --- | --- |
| > Qualify immediately on Account Qualified | > Account Qualified | > None | > Immediate |
| > Pending period qualification | > Account Opening only (+ optional Account Closed) | > Pending Period (+ optional Has Not Taken Action) | > After waiting period (if no closure happened) |
| > Time-bound qualification | > Account Opening + Account Qualified | > Has Taken Action with Recent Activity Window | > Immediate after validation as long as within activity window |

>
