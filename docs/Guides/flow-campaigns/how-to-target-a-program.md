---
title: "How to Target a Program"
excerpt: "Set up program targeting using Extole’s upgraded Flow Builder.\n"
---


>

> 💡 **Important Note:** This guide only applies to flow campaigns that use Extole's upgraded Flow Builder. Check for the flow icon next to your campaign name.

>

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/1672188849/7a88b85b6ea138efdd09eb8eec64/Screenshot+2025-08-15+at+08_43_12.png?expires=1778306400&signature=9af864122d5366777003bb96b5fb81da2855e0ac2920d9346e353efbf40ee6f7&req=dSYgFMh2lYlbUPMW3nq%2BgY%2BXbUHXydVeJLc9LVWfkrwfxpaYE7JVbbtS1j1E%0A5uzksR%2FqQj5QbtfVnf%2BHW4lFnnQ%3D%0A)

>

## Overview

> Targeting in Extole helps ensure the **right participants enter the right campaign at the right time**. Whether you're using domain targeting, audience membership, profile attributes, or custom rules, targeting keeps your campaigns relevant and efficient.

>

> This guide explains how to use Extole's **targeting scenarios**, how to configure rules, and how to decide when and where to apply targeting in your campaign flows.

## Why Use Targeting?

> Targeting in Extole determines:

- Who can see campaign marketing placements
- Who qualifies to enter a campaign
- When they qualify
- Which campaign takes priority if multiple apply
- How participant journeys are maintained over time

> Targeted campaigns to deliver **more personalized, effective, and efficient programs**. Here's why it's worth the effort:

- **Reach the right people** – Tailor campaigns to specific segments (e.g. new customers, loyal advocates, employees), so you’re always speaking to the right audience with the right message.
- **Improve performance** – Targeted campaigns often convert better because they're more relevant. That means higher participation, more referrals, and stronger ROI.
- **Avoid conflicts** – If multiple campaigns are live, targeting ensures people enter the most appropriate one, preventing confusion or double participation.
- **Protect your budget** – Targeting helps prevent rewards from going to ineligible or fraudulent participants, keeping your spend focused on legitimate activity.
- **Test and optimize** – With separate, targeted flows, you can A/B test messaging, incentives, or timing to continuously improve results.

## Targeting Scenarios

> **Targeting scenarios** are pre-configured sets of rules that you can apply within each flow of your campaign. These appear at the top of each flow in the Flow Builder.

> You can:

- Use default or prebuilt scenarios
- Swap between scenarios
- Add or modify rules to suit your business goals

### Default Targeting

- **Includes:** All participants in the US and Canada
- **Excludes:** Suspicious traffic (via built-in fraud filters)
- Use this if your campaign is open to most users by default.

> To include a broader audience (e.g., international users), use the **Everyone** scenario, which removes country restrictions.

>

### Audience Targeting

> Use this to include or exclude specific audiences defined in your **My Audiences** page.

- **Ideal for:** Employees, VIP customers, loyalty members, etc.
- **Enforces fraud filters:** Yes
- **Where to apply:**

  - **Marketing flow**: Controls visibility of CTAs
  - **Participation or Share flows**: Controls who can participate or refer

### Domain Targeting

> Restricts visibility of campaign content to specific domains.

- **Variants:**

  - US/Canada only
  - No country restrictions

- **Domains managed in:** Tech Center
- **Enforces fraud filters:** Yes
- **Where to apply:**

  - **Marketing flow**: Only show CTAs on selected domains

### Eligible Referrer Targeting

> Use this on friend journeys to ensure the person who referred them passes the requirements configured for the advocate share journey.

- **Ideal for:** Referral or Ambassador campaigns with requirements for who can share. When a friend interacts with the campaign, we will check their referrer against those requirements.
- **Journey for Referrer Check:** This is the only setting you must configure for this scenario. Pick the journey with the targeting rules you want applied to the referrer (e.g., eligible audience, allowed countries).
- **Enforces fraud filters:** Yes
- **Where to apply:**

  - **New customer flow**: Only allow a friend to participate if their advocate passes the targeting rules of the chosen journey

## Understanding Targeting Rules

> Targeting rules are grouped into **Entry Rules** and **Ongoing Rules**. Both types must be met for a participant to qualify and remain in the journey.

>

### Entry Rules

> These define who can **enter** a campaign. If any entry rule fails, the participant will not start the journey.

>

### Ongoing Rules

> These must continue to be true **after entry**. If an ongoing rule fails, the participant will be **removed from the journey**, and their future actions will not qualify.

## How to Update Targeting in Flow Builder

> To modify targeting for a specific part of your campaign, you’ll use the **Flow Builder**. Each flow—Marketing, Participation, Share, etc.—can have its own targeting scenario.

>

### Step 1: Open the Flow Builder

> **Open the campaign's Flow Builder.** From the Programs page, find the campaign where you want to update targeting and click Manage Flow.

>

### Step 2: Select the Flow

> **Find the Flow to Edit.** In the Flow Builder, choose the specific flow (e.g., **Marketing**, **Share**) that you want to modify.

>

### Step 3: Update the Targeting

1. **Remove the existing targeting scenario.** If a default or existing scenario is already applied, click the **Remove** (trash can) icon to delete it.
2. **Click “+ New Targeting Scenario”.** This will open a list of available targeting scenarios.
3. **Choose a targeting scenario.** Select from prebuilt options like:

  - **Audience Targeting**
  - **Domain Targeting**
  - **Everyone**

4. **Configure scenario details.** Depending on the scenario, you may need to define specific inputs:

  - **If using Audience:** Choose the audience from the drop-down list of available audiences (from **My Audiences**).
  - **If using Domain:** Select the domain from your list of verified domains (from **Tech Center**).

5. **Add or modify rules (optional).** You can further customize the targeting scenario by adding Entry or Ongoing Rules. All rules must pass for participants to qualify.

  - **Example**: For your **Audience** targeting, you may want to specify that audience members must also be new customers who haven't made a purchase in the last 180 days. In this case, you could add the **Is New Customer** rule to the scenario's entry rules.

### Step 4: Publish Your Changes

> Once you've finished making updates to your campaign's targeting, don't forget to **Publish your campaign**.

## Best Practices

- **Test before going live:** Always validate that the right participants qualify after you update targeting.
- **Be specific:** The more tailored your rules are, the more relevant your campaign will be to participants.
- **Use naming conventions:** Label your scenarios clearly (e.g., "Employees Only", "CA Customers") to stay organized.
- **Ensure continuity:** If you are using various targeting scenarios for each of your campaign flows, make sure you are applying changes and customizations to all of them. *Example: If you change the country restrictions in the marketing flow's targeting, you will also want to make the same update to the targeting in your share flow.*

## Targeting Rules

### Audience & Membership Rules

- **Member of Audience** – Participant belongs to a defined audience
- **Is Not Part of Audience** – Participant is excluded from a specific audience

### Event-Based Rules

- **Input Event Matches Event Names** – Event name matches exactly
- **Event Contains Parameter** – Event has a specific data key/value
- **Event Data Contains Program Label** – Determines targeting based on a label in the event
- **Event Matches Program Domain** – Event originates from a specific domain
- **Event Value Greater Than** – Event includes a value above threshold
- **Event Value Less Than** – Event includes a value below threshold
- **Transaction Value Greater Than** – Participant qualifies if their purchase meets a minimum amount

### Profile-Based Rules

- **Profile Contains Parameter** – A specific attribute exists in the participant’s profile
- **Has Email Address** – Participant must have a valid email
- **Valid Email Filter** – Both referrer and friend must have valid emails

### Behavior & History Rules

- **Has Taken Action** – Participant completed an event (purchase, signup, etc.)
- **Has Not Taken Action** – Participant has not completed a defined event
- **Has Previously Qualified** – Participant passed the same rule set in the past
- **Is New Customer** – Participant has not made a qualifying action in the last 180 days

### Fraud Prevention & Traffic Filtering

> Built-in rules designed to block spam, fraud, and poor-quality traffic.

> **Configuration options:**

- **Blocked Subnetworks** – Prevent traffic from known IP ranges

  - Format: CIDR (e.g., `192.168.0.0/16`)

- **Blocked Referrer Sites** – Block traffic from unwanted sources

  - Format: Domain and path only (no protocol, e.g., `badsite.com/path`)
