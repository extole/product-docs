---
title: How to Set Up Bonus Rewards on a Specific Referral Count (2nd, 3rd, 5th, etc.)
excerpt: Set up bonus rewards when advocates generate multiple referrals in a campaign
deprecated: false
hidden: false
metadata:
  robots: index
---
**Important Note:** This guide only applies to flow campaigns that use Extole's upgraded Flow Builder. Check for the flow icon next to your campaign name.

## Overview

Some programs want to reward an Advocate with something extra once they've referred a certain number of distinct friends who convert — for example, a bonus on top of the standard referral reward when the Advocate hits their 2nd, 3rd, and 5th successful referral.

This is a one-time milestone reward per count, not a recurring "every Nth" reward. This guide covers how to configure that correctly in the upgraded Flow Builder.

## Before You Begin: The Rule to Use (and the One to Avoid)

There's no single native "fire exactly once at the Nth occurrence" rule. The supported pattern is to publish your own counting event to the Advocate, then gate each bonus reward with a Has Taken Action rule set to an Exact Count.

Two rules look similar but do very different things — picking the wrong one is the most common mistake here:

| Rule                              | What it actually checks                                                                            | Use for this setup?                                                                  |
| :-------------------------------- | :------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| **Has Taken Action**              | Counts occurrences of an event on the same profile you're evaluating the reward for (the Advocate) | ✅ Yes — this is what counts "how many friends has this Advocate referred"            |
| **Other Person Has Taken Action** | Checks whether the counterpart in a single relationship (one specific Friend) took an action       | ❌ No — this only tells you about one Friend, not the Advocate's total referral count |

## Step 1: Create a New Advocate Journey

1. Go to the Programs page, find your campaign, and click Manage Flow.
2. At the top of the page, click the Advocate.
3. Under Journey, click + New Journey.
4. Choose Template Journey and rename it Bonus Rewards.
5. Publish the campaign so the journey is available on the campaign.

## Step 2: Add a Business Event to Count Referrals

This event needs to publish to the Advocate every time a Friend converts — so you add it directly from the Friend's Converted event, not by building a new journey under the Advocate role from scratch.

1. Find the Friend's Converted event (or whichever event should be counted).
2. Hover on that step and click the + icon.
3. Choose the Advocate Role and the new Journey “Bonus Rewards”.
4. Choose a template event (ex Challenge Accepted) and rename it to something clear, like Bonus Rewards Counter.

## Step 3: Add a Reward for Each Milestone

For each milestone (2nd, 3rd, 5th referral, or whatever tiers you need):

1. Hover over the new event and click + New Reward for the Advocate Role.
2. [Add a new reward](https://docs.extole.com/docs/how-to-add-a-new-reward) and name it something like 2nd Referral Bonus Reward.
3. Configure the face value/reward supplier for that milestone (bonuses can differ in value per tier).
4. Don’t forget to update any reward emails if you want an email to be triggered.

## Step 4: Add Has Taken Action step

For each milestone reward:

1. Open the reward and click + New Reward Rule.
2. Choose Has Taken Action.
3. Set Business Event to the Bonus Rewards Counter event from Step 1.
4. Set Exact Count to the milestone number (2, 3, or 5).
5. Click Apply.
6. Adjust any other rules as necessary like Reward Limit, IP Fraud, etc.

Repeat Steps 2–4 for each milestone reward.

## Step 5: Test Before Publishing

During testing, make sure to refer and convert enough distinct Friends under one Advocate profile to walk through each milestone, and confirm:

- No extra bonus fires on the 1st referral
- The 2nd-referral bonus fires exactly once, on the 2nd distinct Friend conversion
- The 3rd- and 5th-referral bonuses behave the same way
- No bonus fires on referrals in between milestones (e.g., the 4th) unless you've intentionally configured one

## Troubleshooting

- **Bonus never fires.** Check the counter Business Event's trigger rules. It should say it is Triggered by the Publish Converted to Advocate event (name may differ slightly based on your specific event).
- **Bonus fires on every referral instead of just the milestone.** Confirm you used Exact Count on Has Taken Action, not a minimum/threshold-style count.
- **Bonus counts don't seem to reflect distinct Friends.** Double check the rule is plain Has Taken Action (checked against the Advocate) and not Other Person Has Taken Action (checked against a single Friend in one relationship). See the table above.

***

### Related Resources

- [How to Add a New Business Event](https://docs.extole.com/docs/how-to-add-a-new-business-event)
- [How to Set Up a Reward](https://docs.extole.com/docs/how-to-set-up-a-reward)
- [How to Set Up Reward Rules](https://docs.extole.com/docs/how-to-set-up-reward-rules)
- [Configure Common Reward Scenarios for Credit Unions and Banks](https://docs.extole.com/docs/configure-common-reward-scenarios-for-credit-unions-and-banks)

<br />
