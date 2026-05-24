---
title: "How to Approve Failed Rewards"
excerpt: "Investigate and approve failed rewards on behalf of your customers  in Extole's User Support for flow campaigns.\n"
---


>

> 💡 **Important Note:** This guide only applies to flow campaigns that use Extole's upgraded Flow Builder. Check for the flow icon next to your campaign name.

>

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/1672188849/7a88b85b6ea138efdd09eb8eec64/Screenshot+2025-08-15+at+08_43_12.png?expires=1778306400&signature=9af864122d5366777003bb96b5fb81da2855e0ac2920d9346e353efbf40ee6f7&req=dSYgFMh2lYlbUPMW3nq%2BgY%2BXbUHXydVeJLc9LVWfkrwfxpaYE7JVbbtS1j1E%0A5uzksR%2FqQj5QbtfVnf%2BHW4lFnnQ%3D%0A)

## Overview

> Sometimes, a participant qualifies for a reward but doesn’t receive it due to a **reward rule failure**. If, after review, you decide the reward **should still be issued**, you can manually approve it from the participant's profile.

>

> Common reasons for failed rewards include:

- **Fraud prevention rules** (e.g., high-risk IP or email)
- **Low-quality business event** (e.g., Converted event failed quality rules due to self-referral)
- **Business logic** (e.g., minimum purchase value not met)

> This guide walks you through how to locate and approve a failed reward issued from a Flow campaign.

## How to Approve Rewards

### Step 1: Search for the Participant

1. Navigate to the **People Search** or **Event Live View** in your Extole dashboard.
2. Enter the participant’s **email address** to locate their profile.
3. Click into the profile to see their campaign activity and rewards.

### Step 2: Locate the Failed Reward

1. Scroll to the **Rewards** section on the person’s profile.
2. Identify the **failed reward** associated with the campaign and event in question.
3. Expand the reward to confirm it matches the participant’s inquiry (e.g., campaign name, reward type, date issued).

### Step 3: Review Rule Results and Reward Status

1. Expand the rules for the failed reward to see further details.
2. Review which **rules passed**, **failed**, or are still **pending**.

  - **Pending Rule Example**: A 7-day waiting period hasn't elapsed yet.
  - **Failed Rule Example**: The person’s risk score exceeded the threshold.

3. Evaluate whether the failure was justified or if the reward should still be honored.
4. If all the rules passed, double check the status of the reward itself by clicking on the reward link. In some instances, a successfully earned reward can get stuck in the "Trying to Fulfill" state due to insufficient funds, a depleted coupon pool, etc.

  - To resolve this, you will need to fund the reward supplier in your Rewards Center and then go back to person's profile and hit the **Re-evaluate** button on the reward.

### Step 4: Approve the Reward

1. If you choose to override the failure, click the **Approve** button.
2. A confirmation modal will appear. Enter a **note** explaining the reason for approval. **Example note:** ​`"Approved due to support escalation — customer provided valid proof of purchase."`
3. Click **Confirm**.

> Once approved:

- The reward’s **status** will update to **Reward Earned**.
- Your note and user info will be recorded.
- All rules will now appear as **passing** in the reward details.

## Important Considerations

- Manual approval won’t work if:

  - The campaign has been stopped or archived
  - The reward was deleted
  - The reward supplier has insufficient funds or inventory

- If required data (e.g., name, order ID) is missing and can't be added, **you may need to [issue a manual reward](doc:how-to-issue-a-manual-reward)** instead.
