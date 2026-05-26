---
title: "Default Business Event Quality Rules"
excerpt: "Guide to the common business event quality rules you can enable on your program\n"
---


>

> 💡 **Important Note:** This guide only applies to flow campaigns that use Extole's upgraded Flow Builder. Check for the flow icon next to your campaign name.

>

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/1672304321/925c13c89e7d220a9daa5543034e/Screenshot%2B2025-08-15%2Bat%2B08_43_12.png?expires=1778306400&signature=6b49e38fffd22147ddff1fd450c6b7cfe70a8e1b372a2756f4a5e6353fafb672&req=dSYgFMp%2BmYJdWPMW3nq%2BgcQUso3p53d7e2vDhkx6uEui3S68WuQRAoAy2Hek%0AM%2FMpcIy14ijb33Lkx11AFJnMRe8%3D%0A)

# Overview

> Quality Rules on a Business Event evaluate whether an event is high or low quality.

- **High-quality events** trigger the business event and may lead to rewards or emails.
- **Low-quality events** do not trigger the business event.

> Common use cases:

- Ensuring valid email addresses
- Checking for suspicious IP addresses
- Preventing self-referrals

# Business Event Quality Rules

> All flow campaigns come with default quality rules set up according to our best practices. For example, a standard referral campaign includes the following rules:

| > **Rule** | > **Business Events** | > **Description** |
| --- | --- | --- |
| > Share Email Limit | > Shared | > Limit the number of share emails a person can receive in a specified time. |
| > Mass Share Limit | > Shared | > Limit the number of times a person can share across all programs within a specified time. |
| > Valid Email Filter | > Shared, Share Clicked, Referral Signed Up, Converted | > Block events associated with invalid emails. |
| > Bot Click Prevention | > Share Clicked, Referral Signed Up | > Prevent bot-driven behavior by limiting the number and speed of clicks from a single user within a specified time. |
| > Is New Customer | > Share Clicked, Referral Signed Up | > Check that the person has not performed an action that makes them a customer in the last 180 days. |
| > Self Referral Prevention | > Share, Share Clicked, Referral Signed Up, Converted | > Prevent self-referral by email address, browser ID, and/or IP address. Within this rule, these specific requests can be toggled on or off. |

# Looking for Quality Rules on Rewards?

> These business event quality rules are specific to an event being low or high quality, but wouldn't include all rules like Annual Reward Limits. Learn more about **[Setting up Reward Rules here](doc:how-to-set-up-reward-rules)**.
