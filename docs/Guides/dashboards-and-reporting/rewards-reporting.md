---
title: "Rewards Reporting"
slug: rewards-reporting
excerpt: "# Overview"
hidden: false
intercom_source_id: 10772082
---

# Overview

This article describes how you can easily pull data on your rewards configured for your programs. In particular, the following two reports are covered:

- 

Rewards By State Report
- 

Rewards Report

# Rewards By State Report

The **Rewards By State report** gives you a count of the rewards that entered a specific state in a given time range.

## Use Cases

For example, you may want to know how many rewards were earned in Q1, or how many rewards have been redeemed since the launch of your program, or how many rewards failed to send last month.![rewards_by_state.png](https://extole-5ef307a0e5b1.intercom-attachments-7.com/i/o/syy27wia/1421734019/6b7870b2adf1585c283c311baf41/360070425573?expires=1782259200&signature=608dfcccb70dfbdf7171584a6dd64893f644b1639c070ee197b27fbd9b3d4a4c&req=dSQlF859mYFeUPMW3nq%2BgeYq8T%2BG%2FD7969lJMblQwF%2BilrvNNpsdZDNMrStd%0AW%2Bo3xY7jvhxD3Od5sRic5dHXbeU%3D%0A)
# Rewards Report

The **Rewards report** gives you a list of the rewards that entered a specific state in the given time range.

## Use Cases

For example, you may want to know which rewards have been redeemed or which rewards were earned during a particular time period. You could also be looking for information about the people who have redeemed an advocate reward or earned account credits.![rewards_report.png](https://extole-5ef307a0e5b1.intercom-attachments-7.com/i/o/syy27wia/1421734018/1d70542f057f1043ee803fc42550/360069366354?expires=1782259200&signature=08fb25afcfd1968ce28faac860cef9ae8ddaa1081b38fb6d46b0f9b0618f26f1&req=dSQlF859mYFeUfMW3nq%2BgYsL2Qu37MNlcDrwBfMIEqnBmmpxfq6GOLUOdTCc%0Akqyc%2Bc4uJnbseoklOdX4TJC4KFY%3D%0A)

# Configuration

Both the Rewards By State and Rewards reports contain the following configuration options.

## Filters

- 

**Time Range:** The range of data that will be in the report
- 

**Period (only available for the Rewards by State report):** The way that your data will be grouped

  - 

If you set your time range to "Last Month" and your period to "Week," this will count the data from the last month, grouped by week

- 

**Container:** The place(s) you want to see data from

  - 

You can choose to show data from all containers, from just your production container, or just from a given test container

- 

**Program Label:** The program that you want to analyze rewards for

  - 

If you don't specify a program, you'll get data on all programs

- 

**Campaign ID:** The campaign that you want to analyze rewards for

  - 

If you don't specify a campaign, you'll get data on all campaigns within the program you specify (or within all programs if you don't specify a program)

- 

**Reward Type:** The type of reward you want to analyze (coupon, custom reward, Tango gift card, etc.)
- 

**Reward Supplier ID:** Extole's unique ID for the system that is issuing the reward

  - 

To find a particular Reward Supplier ID, navigate to [your Rewards page](https://my.extole.com/account-rewards), click on the reward you're looking for, and copy the string at the end of the URL after the #

- 

**Reward States: **The particular state(s) of rewards that you're interested in (e.g. earned, fulfilled, redeemed, etc.)

  - 

[Please see our Help Center article here for more on reward states](https://success.extole.com/hc/en-us/articles/360001560447-Supported-Rewards-and-Reward-States)

- 

**"Only Show Rewards Currently In This State":** When toggled on, this will only show rewards that are *currently* in the state you have specified above

## Advanced

- 

**Formats:** Available file formats
- 

**Dimensions (only available for the Rewards by State report): A**nother way to group the output of the report (e.g. by program, by campaign, etc.)
- 

**"Extended Person Details" (only available for the Rewards report): **When toggled on, this gives you the email, partner user id, and first and last name of the person the reward is associated with

# Output

## Rewards by State Report

For a given reward, you'll see the period you configured (e.g. month), the start and end time of that period (e.g., 1/1/2022 – 2/1/2022), the program label* (e.g. Refer A Friend), and the campaign* it's associated with (e.g., January Refer A Friend Campaign).

****If specified in Dimensions***

You'll also get the following:

- 

**Reward Supplier ID:** Extole's unique identifier for the system that is issuing the reward

  - 

*Please specify Reward Supplier ID in Dimensions to see this in the output*

- 

**Reward Supplier Type: **The type of reward (coupon, custom reward, gift card, etc.)

  - 

*Please specify Reward Supplier Type in Dimensions to see this in the output*

- 

**Reward State: **The particular state(s) you specified (e.g. earned, fulfilled, redeemed, etc.)

  - 

*Please specify Reward State in Dimensions to see this in the output*

- 

**Count: **the number of rewards that match the specified criteria

## Rewards Report

- 

**Reward ID:** Extole's unique identifier for the reward
- 

**Partner Reward ID:** Your unique identifier for the individual reward, specified when the individual reward is created in your own internal system
- 

**Face Value Type:** Indicates if the reward is in USD, GBP, EUR, points, percent off, etc.
- 

**Face Value:** Indicates the value of the reward in USD, GBP, EUR, points, percent off, etc.
- 

**Campaign ID:** The campaign the reward is associated with
- 

**Reward Supplier Type: **The type of reward (coupon, custom reward, gift card, etc.)
- 

**Reward Supplier ID:** Extole's unique identifier for the system that is issuing the reward
- 

**Partner Reward Supplier ID:** A unique identifier for your own internal system that is issuing the reward
- 

**Reward State:** The particular state(s) you specified (e.g. earned, fulfilled, redeemed, etc.)
- 

**Current Reward State: **The current state of the reward
- 

**Reward Name:** The name of the reward

  - 

Coupon: The name of the coupon pool at the time the reward was issued
  - 

Gift card: The gift card SKU
  - 

Account: The name of the account credit at the time the reward was issued

- 

**Person ID**: **The email address of the person the reward is associated with
- 

**Email**: **The email address of the person the reward is associated with
- 

**Partner User ID**: **Your unique identifier for the person the reward is associated with
- 

**First Name**:** The first name of the person the reward is associated with
- 

**Last Name**: **The last name of the person the reward is associated with

***If "Extended Person Details" is toggled on*
