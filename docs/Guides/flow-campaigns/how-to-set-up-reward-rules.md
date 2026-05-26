---
title: "How to Set Up Reward Rules"
excerpt: "Configure reward rules to ensure the right people are getting rewarded using Extole’s upgraded Flow Builder.\n"
---


>

> 💡 **Important Note:** This guide only applies to flow campaigns that use Extole's upgraded Flow Builder. Check for the flow icon next to your campaign name.

>

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/1672188849/7a88b85b6ea138efdd09eb8eec64/Screenshot+2025-08-15+at+08_43_12.png?expires=1778306400&signature=9af864122d5366777003bb96b5fb81da2855e0ac2920d9346e353efbf40ee6f7&req=dSYgFMh2lYlbUPMW3nq%2BgY%2BXbUHXydVeJLc9LVWfkrwfxpaYE7JVbbtS1j1E%0A5uzksR%2FqQj5QbtfVnf%2BHW4lFnnQ%3D%0A)

>

# Overview

> **Reward rules** define the conditions under which a participant earns a reward in your campaign. These rules ensure that:

- **Only eligible participants** are rewarded
- **Qualifying actions** are clearly defined
- **Rewards are delivered** at the right time and under the right conditions

> Every default Extole campaign includes a set of preconfigured reward rules based on industry best practices. However, you can **adjust, remove, or add rules** to better fit your business goals.

>

> This guide walks you through how to locate, configure, and manage reward rules using the Flow Builder.  
​

![](https://downloads.intercomcdn.com/i/o/syy27wia/1783986904/057e2c58e8b25a7ee203c36f461a/image.png?expires=1778306400&signature=2c2a29086632dcfae829195eab1208e2b4a4e1336fa39d3b66b9110de2914d76&req=dScvFcB2m4hfXfMW3nq%2BgcVhvWKDnulAlTYggB8LrUY65mOs5VSvlS60XDUz%0AwvHDPXNEOuCcKhejSrm78%2B2rETk%3D%0A)

# How to Manage Rewards in Flow Builder

### Step 1: Navigate to the Reward in Flow Builder

1. Go to the **Programs** page.
2. Locate the campaign you want to edit.
3. Click the **Manage Flow** icon for that campaign.
4. In the Flow Builder, find the **Reward** node for the flow.
5. Scroll to the **Reward Rules** section for the specific reward you'd like to configure.

### Step 2: View and Edit Existing Reward Rules

1. Click on any existing reward rule to open its configuration panel.
2. Adjust settings as needed for that specific rule.
3. Click **Apply** to save your changes.

> **Example:**  
For the **Annual Reward Value Limit** rule, you can set:

- **Total Value** – Maximum reward value per person per tax year
- **Tax Year Starting Month and Day** – Defines when the yearly limit resets

### Step 3: Add a New Reward Rule

1. In the **Reward Rules** section, click **+ New Reward Rule**
2. Choose from a list of available rules
3. Configure the selected rule
4. Click **Apply** to save

> You can add multiple reward rules. All rules must pass for the reward to be granted.

# Best Practices

- **Start with defaults:** Extole’s preconfigured rules cover common risk and reward scenarios.
- **Be specific:** Tailor rules to your business objectives and reward strategy.
- **Use pending periods:** Add time buffers for validations like fraud checks or return windows.
- **Layer rules carefully:** All rules must pass for the reward to be granted—avoid unnecessary blockers.
- **Test thoroughly:** Before going live, simulate typical participant journeys to confirm the reward logic works as expected.

# Common Reward Rules (with examples)

### Reward Limits & Eligibility

- **Annual Reward Value Limit:** Prevents a participant from earning more than a set amount per tax year.
- **Reward Limit:** Restricts how many times a participant can earn a reward within a given period.
- **Pending Period:** Delays the reward until a pending period ends and all other conditions have been met. *Example: A friend only receives a reward for opening an account after it has been open for 60 days.*

>

> Annual Reward Value Limit and Reward Limit are both on by default when creating new campaigns, however it's unlikely you would use both at the same time. Make sure to remove the one you don't need.

>

### Fraud & Risk Prevention

- **Business Event Quality:** Ensures the event triggering the reward is legitimate and high quality.
- **Has Email Address:** Only allows rewards for participants with a valid email.
- **Risk Evaluation:** Evaluates the email domain and IP of the person to detect risk signals.
- **Other Person Risk Evaluation:** Evaluates the advocate or friend in a two-person program.

### Relationship Rules

- **Has Not Been Rewarded For Relationship:** Ensures rewards are given only once per unique participant relationship  
​ *Example: An advocate can’t earn multiple rewards for referring the same friend.*

### Event-Based Rules

- **Event Value Greater Than / Less Than:** Rewards are only issued if a value (e.g., order amount) meets the criteria.  
​ *Example: Order value must be over $200.*

### Behavior & Action Rules

- **Has Taken Action / Has Not Taken Action:** Reward based on whether a participant has completed (or not completed) specific actions.  
​ *Example: Only reward if the person has completed a sign-up.*
- **Is New Customer:** Only rewards people who haven’t made a purchase in the last 180 days.

### Audience Membership

- **Member of Audience / Is Not Part Of Audience:** Include or exclude participants based on audience membership.  
​ *Example: Only reward VIP customers or loyalty members.*

### Profile Rules

- **Profile Contains Parameter:** Checks the participant’s profile for a specific attribute before issuing a reward.  
​ *Example: Only reward users with a profile tag like `"tier": "gold"`.*

### Related Person Rules

- **Other Person Has Taken Action:** Ensures that the related person (e.g., the advocate in a referral campaign) has completed a required action.  
​ *Example: Only reward the friend if the advocate has also signed up.*
