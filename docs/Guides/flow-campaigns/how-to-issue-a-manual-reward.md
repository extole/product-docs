---
title: "How to Issue a Manual Reward"
excerpt: "Create manual rewards on behalf of your customers in Extole's User Support for flow campaigns.\n"
---


>

> 💡 **Important Note:** This guide only applies to flow campaigns that use Extole's upgraded Flow Builder. Check for the flow icon next to your campaign name.

>

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/1672188849/7a88b85b6ea138efdd09eb8eec64/Screenshot+2025-08-15+at+08_43_12.png?expires=1778306400&signature=9af864122d5366777003bb96b5fb81da2855e0ac2920d9346e353efbf40ee6f7&req=dSYgFMh2lYlbUPMW3nq%2BgY%2BXbUHXydVeJLc9LVWfkrwfxpaYE7JVbbtS1j1E%0A5uzksR%2FqQj5QbtfVnf%2BHW4lFnnQ%3D%0A)

>

## Overview

> Manual rewards let you issue a reward **outside of standard campaign logic**, which is useful when:

- **A reward failed but cannot be approved** due to the campaign being stopped, the reward being deleted, or essential data missing. 
- The event that triggers the reward **failed to process** correctly.
- A customer or user **escalation** **needs a fast resolution.**
- You are trying to reward someone **outside typical criteria**.

> Manual rewards are created directly on the participant’s profile in flow campaigns. This guide explains how to issue them properly and ensure they include all required information.

## How to Manually Reward a Person

### Step 1: Locate the Participant's Profile

1. Navigate to Extole's **User Support**.
2. Use **People Search** or **Event Live View** to find the person.
3. Click into their **profile** to begin issuing a manual reward.

>

> Always confirm you’re on the correct profile — advocate vs. friend can be easy to mix up.

### Step 2: Investigate Before You Reward

> Before creating a manual reward, take a moment to review the participant’s history. This ensures you're not duplicating rewards or missing context.

>

> Things to Check:

- **Does the person already have a reward** for this campaign or referral?

  - If yes, was it already earned, failed, or still pending?

- **Did a rule failure cause the reward to be denied?**

  - If so, consider [approving the failed reward](doc:how-to-approve-failed-rewards) instead of issuing a new one.

>

> ⚠️ Issuing a manual reward without proper review can lead to:

- Duplicate rewards
- Reporting inconsistencies
- Violation of campaign rules (e.g., multiple rewards per person or relationship, exceeding the annual reward value limit, etc.)

### Step 3: Start the Manual Reward

1. In the participant’s profile, click the **+ New Reward** button.
2. The participant’s name and email will be prefilled at the top for reference.  
​![](https://downloads.intercomcdn.com/i/o/syy27wia/1851113551/add174047ca049c31c9b4fc17fc1/image.png?expires=1778306400&signature=d5564d9bbb70b5b558c47825c57d2e8b7d9681bde190d69c74c2fbb6ebefb98b&req=dSgiF8h%2FnoRaWPMW3nq%2BgcgnmflQWTgdmjHyzlvF9HC9GfsIn16gPMZiDAUg%0AeF4M8RlSmdX0j1xd8Ua8f6d%2FuT4%3D%0A)

### Step 4: Select Program, Campaign, and Reward

1. Use the dropdown menus to choose:

  - **Program**
  - **Campaign**
  - **Specific Reward**

2. Once selected, confirm you're issuing the correct reward by checking the **Reward Supplier Link** that appears below the reward field.

> If the reward you want to select is grayed out, the associated campaign may not be live or the reward may be missing a reward supplier.

>

### Step 5: Add a Reason for Manual Rewarding

> In the **Notes** field, document why this reward is being issued manually.

- **Example note:** `"Manual reward due to missing first/last name in original event. Verified eligibility."`

> This note will be saved in the reward details for future reference.

>

### Step 6: Add Related Person (if applicable)

> If the reward is part of a two-person program:

- Add the **email address of the related person** (e.g., the advocate in a friend reward).
- This helps prevent future duplicate rewards for the same referral relationship and reporting.

### Step 7: Include Additional Data (as needed)

> Some rewards require extra data to be fulfilled (e.g., shipping info, order ID, account number).

>

> In the **Additional Data** section, add any required fields:

| > Example Field Name | > Example Value |
| --- | --- |
| > `order_id` | > `12345678` |
| > `address` | > `"123 Main St, NY"` |

>

> **Tip**: Review the campaign’s flow using the Flow Builder to see what data is expected on the reward event. Typically, this is data being passed on the business event that triggers the reward. Matching this data ensures the reward issues correctly and appears uniformly in reporting.

![](https://downloads.intercomcdn.com/i/o/syy27wia/1851139247/2d1355ab3a1ed1088e0c47d48ccb/image.png?expires=1778306400&signature=8de54b01a2a500e312e1c4428dd31bad770308e977c4cbbc4809f7aed87d3e8d&req=dSgiF8h9lINbXvMW3nq%2BgcVJ09PYXnwQta0qvTKa9epJSZ9N7P4Zjz8pNxbt%0Ajb7hZ5fbnVyjOhomoeSNBedSeVg%3D%0A)

>

### Step 8: Choose Whether to Force Approve

> If you want the reward to go out **regardless of rule evaluation**:

- Toggle on **"Approve reward even if rules fail"**

> Use this option when the participant doesn’t meet normal conditions, but you want to honor the reward anyway

>

> If you want the system to still evaluate rules and **only send the reward if all rules pass**:

- Leave the "Approve reward even if rules fail" toggled **off**

> Use this option when you still want to honor the other rules of the program such as the reward cap and quality rules.

>

### Step 9: Create the Reward

1. Review all fields one last time.
2. Click **Create Reward**.

> The reward will appear in the participant’s profile and, if all requirements are met, will be issued.

## Best Practices

- **Investigate first** – Always review the campaign, event, and expected data before issuing.
- **Fill in all known data** – This improves reward delivery and reporting accuracy.
- **Be consistent** – Manual rewards should match the format and standards of automatically issued rewards.
- **Document clearly** – Your notes help teams understand why the reward was issued later.
- **Reward both users** - if this is a referral and you want to reward both advocate and friend, do this process twice for each profile.

## Troubleshooting

> If creating a manual reward fails, you may want to check the following:

- Your latest campaign changes have been published.
- The reward supplier associated with the reward is adequately funded.
