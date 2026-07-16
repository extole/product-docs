---
title: Investigating Missing Rewards and Attribution
---
# **Overview**

When a customer reports that they didn't receive an expected reward, your goal is to determine where the reward journey stopped.

Most issues fall into one of these categories:

- The qualifying event never occurred.
- The event hasn't been processed yet.
- The event wasn't attributed to the referral program.
- The participant wasn't eligible.
- The reward rule didn't evaluate successfully.
- The reward was created but hasn't been delivered.

This is a guide on how to address these questions from your customers. If you are looking for more information on why a WISMR may occur, please review <Anchor target="_blank" href="doc:wismr-101-understanding-customer-reward-inquiries">**WISMR 101: Understanding Missing Reward Requests**</Anchor>​.

For more info on the User Support section as a whole, check out [**Preparing Your Support Team for Extole**](doc:leveraging-user-support-pages).

# **Investigation Workflow**

<br />

**Before You Begin**

Collect the following information before investigating:

- Participant email address(es)
- Approximate date and time of the qualifying action
- Expected reward
- Referral, order, or account ID, if available
- Campaign or program name
- Screenshots or error messages

This information will help you locate the participant and reconstruct their referral journey.

## **Step 1: Confirm the Qualifying Action**

Verify that the participant completed the action your campaign rewards:

- Purchase
- Signup
- Trial start
- Account opening
- Account funding

If the required action has not occurred, no reward can be issued.

Also verify whether enough time has passed for event processing. Depending on your integration, events may be processed in real time, hourly, or through scheduled batch uploads.

## **Step 2: Open the Participant Profile**

Locate the participant using their email address.

From the participant profile, review both the **Activity** tab and **Show Steps**.

For investigations, **Show Steps** is the primary troubleshooting tool because it displays the participant's complete event timeline, including:

- Referral clicks
- Campaign attribution
- Qualifying events
- Reward evaluations
- Internal processing events
- Unattributed events

Always review events from the earliest event forward.

## **Step 3: Verify Referral Attribution**

Determine whether the qualifying event belongs to a referral journey. A successful referral journey usually follows this sequence:

1. Referral link clicked
2. Referral context established
3. Signup or registration
4. Purchase or other qualifying event
5. Reward evaluation

If the qualifying event occurred before the referral was established, it cannot be associated with the referral program.

**Referral attribution is not retroactive.**

## **Step 4: Look for Unattributed Events**

An event may have been received by Extole but not associated with a referral. These events typically:

- Have no Campaign
- Have no Journey
- Have no Program
- Display **Quality = NONE**

This indicates that Extole processed the event but could not associate it with a referral journey.

Without referral attribution, reward rules cannot evaluate the event.

## **Step 5: Verify Reward Configuration**

Navigate to **Campaign → Rules** to confirm that:

- The qualifying event is configured.
- The rule includes a reward.
- The reward rule is active.

If no reward is attached to the event, or if the event doesn't satisfy the configured rule conditions, a reward will not be created.

## **Step 6: Review Eligibility**

Even when attribution succeeds, participants must still satisfy the campaign's eligibility requirements.

Common examples include:

- New customers only
- Minimum purchase amount
- Qualifying products
- Eligible account types
- Campaign audience restrictions
- Geographic requirements

If any eligibility requirement isn't met, reward evaluation stops.

## **Step 7: Determine Whether the Reward Was Created**

If attribution, configuration, and eligibility all appear correct, determine whether the reward exists.

### **Reward Exists**

If the reward has already been created, investigate delivery.

Common causes of delayed delivery include:

- Reward provider processing
- Email delivery delays
- Spam or junk filtering

### **Reward Doesn't Exist**

Review the participant timeline and reward evaluation to determine which condition prevented reward creation.

# **Understanding Activity vs. Show Steps**

Both views provide participant information, but they serve different purposes.

| Activity                              | Show Steps                                         |
| ------------------------------------- | -------------------------------------------------- |
| Displays attributed referral activity | Displays the complete event timeline               |
| Used for day-to-day reporting         | Used for troubleshooting                           |
| Shows successful referral events      | Includes attributed and unattributed events        |
| Does not display internal processing  | Displays internal processing and reward evaluation |

When troubleshooting, always rely on **Show Steps**.

# **Common Investigation Outcomes**

## <br />**The Qualifying Event Never Occurred**

The participant hasn't completed the required action, so no reward can be issued until the qualifying event occurs.

## **The Qualifying Event Is Still Processing**

The event has not yet been processed by Extole - wait until the next processing cycle before continuing the investigation.

## **The Event Wasn't Attributed**

The participant completed the qualifying action before referral attribution existed or never entered the referral journey. Events without attribution cannot generate rewards.

## **The Participant Isn't Eligible**

The participant failed one or more eligibility requirements configured for the campaign.

## **The Reward Rule Didn't Evaluate Successfully**

Review the reward rule configuration and determine which condition failed.

## **The Reward Exists but Hasn't Been Delivered**

The reward has already been created, meaning that the issue is likely related to delivery rather than reward generation.

# **Explaining the Outcome to the Customer**

After identifying the cause, communicate the result in clear, non-technical language.

For example:

> We reviewed your referral activity and found that the qualifying purchase occurred before the referral link was used. Because the referral wasn't established until after the purchase, the purchase couldn't be associated with the referral program and wasn't eligible for a reward.

Or:

> We confirmed that your reward has been created successfully and is currently being processed by our reward provider. Delivery may take a little longer to complete.

Avoid using internal terminology such as **Quality**, **Show Steps**, or **rule evaluation** when communicating with customers.

# **Investigation Checklist**

Before escalating to Extole Support, confirm that you have verified:

✓ The participant completed the qualifying action.

✓ Enough time has passed for event processing.

✓ The participant timeline has been reviewed in Show Steps.

✓ Referral attribution exists.

✓ The qualifying event occurred after attribution.

✓ The reward rule is configured correctly.

✓ Eligibility requirements are satisfied.

✓ The reward has or has not been created.

✓ Reward delivery status has been confirmed.

If all of these checks have been completed and the issue remains unresolved, contact Extole Support at [support@extole.com](mailto:support@extole.com) and include your investigation findings.
