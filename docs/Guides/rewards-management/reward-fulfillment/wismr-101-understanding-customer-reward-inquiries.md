---
title: 'WISMR 101: Understanding Missing Reward Requests'
---
A **WISMR** ("Where Is My Reward?") request occurs when a participant expected to receive a reward from your Extole program but did not.

Most WISMR requests are not caused by platform issues. Instead, they're typically the result of program configuration, eligibility requirements, event processing, or referral attribution.

This guide explains the most common reasons a reward may be missing and points you to the appropriate troubleshooting resources.

## What happens before a reward is issued?<br />

A participant receives a reward only after several conditions have been met. The simplified reward journey looks like this:

1. The participant enters the referral journey.
2. The referral is successfully attributed.
3. The qualifying action is completed (such as a purchase, signup, or account funding).
4. The event satisfies all program rules.
5. The reward is created.
6. The reward is delivered through the configured reward provider.

If any step in this process fails, the participant may not receive a reward.

## Common reasons a reward is missing<br />

### The qualifying event hasn't happened yet

Many programs reward customers only after a specific milestone has been completed. Examples include:

- First purchase
- Account funding
- Subscription activation
- Trial completion

Even if a participant has started the journey, the reward won't be created until the required event occurs.

### The event is still being processed

Depending on your integration, qualifying events may arrive in Extole:

- within minutes
- hourly
- through scheduled batch uploads

If the qualifying action happened recently, allow enough time for processing before investigating further.

### The participant isn't eligible

Many referral programs include eligibility requirements:

- new customers only
- minimum purchase amount
- qualifying products
- eligible account types
- geographic restrictions
- campaign-specific audiences

If one or more eligibility requirements aren't met, no reward is issued.

### The referral wasn't successfully attributed

Referral attribution connects a participant's qualifying action to the referral journey.

If the participant completed the qualifying action before referral attribution was established (or never used the referral link), the event cannot be credited to the referral program.

This is one of the most common causes of WISMR requests.

### The reward was created but hasn't been delivered

Sometimes the reward exists but delivery is delayed. Possible reasons include:

- email delivery delays
- spam or junk mail filtering
- third-party reward provider processing
- pending reward fulfillment
- failed quality rules

###

## How to investigate a WISMR request

<br />**Before opening an investigation**

Collecting complete information significantly reduces investigation time. Whenever possible, gather:

- participant email address
- approximate date and time of the qualifying action
- expected reward
- referral, order, or account ID
- screenshots or error messages
- campaign name (if applicable)

Once you've collected the necessary information, follow the investigation workflow to determine where the reward process stopped. The investigation guide walks through how to:

1. verify the qualifying event
2. confirm reward configuration
3. review participant activity
4. inspect referral attribution
5. determine whether rule conditions passed
6. identify delivery issues

➡ Continue with [Investigating Missing Rewards and Attribution](doc:how-to-investigate-a-wismr-request)​.

## FAQ

### <br />Why wasn't my referral counted?

The participant may not have completed the required qualifying action, the referral may not have been attributed, or eligibility requirements may not have been met.

See [Investigating Missing Rewards and Attribution](doc:how-to-investigate-a-wismr-request)​ for the complete investigation workflow.

### Why wasn't a reward issued?

Rewards are created only after:

- the qualifying event is received,
- referral attribution exists,
- all program rules pass, and
- the campaign is configured to issue a reward.

### Why does the customer see "Not Eligible"?

This usually indicates that one or more program eligibility requirements were not satisfied, such as customer status, purchase requirements, campaign eligibility, or promotion availability.

### Why don't Extole reports match our internal reports?

Different systems often measure different stages of the customer journey.

For example, your CRM may count every purchase, while Extole reports only attributed and qualified referral events. Differences in attribution windows, qualification rules, duplicate filtering, and reporting timeframes can also contribute to discrepancies.
