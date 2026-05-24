---
title: "Common Trigger Rules"
excerpt: "Understand the trigger rules available when building campaigns on Flow Builder\n"
---


>

> 💡 **Important Note:** This guide only applies to flow campaigns that use Extole's upgraded Flow Builder. Check for the flow icon next to your campaign name.

>

 ![](https://downloads.intercomcdn.com/i/o/syy27wia/1867809866/68dce6a82db953635b80ac0f0bea/Screenshot%2B2025-08-15%2Bat%2B08_43_12.png?expires=1778306400&signature=4ef776cb751042bd088dc20486904bd4a9f39c1500c46a9620e978162d626a20&req=dSghEcF%2BlIlZX%2FMW3nq%2BgeI9F0jfT94nVwMQhzBHiGlIvp7O3680ce4G%2Bp2%2B%0AcbxMF6ckeBMcMlJ5gjgV%2FFKhxTw%3D%0A)

>

# **Overview**

> **Trigger rules** are a type of **[Business Event Rule](doc:how-to-set-up-business-event-rules)** that let you control precisely which incoming events from your systems create or process business events inside Extole. Use them to decide *when* Extole should record a business event based on event payloads, a person’s past behavior, audience membership, or technical context. If an input event **fails trigger rules**, Extole **does not** create the business event at all.​

>

### **Examples:**

- When we send an event called free_trial_started, create a Free Trial Started event.
- Only track conversions when "product_type": "subscription".
- When a person converts, add them to the “eligible customers” audience.
- Only track an account_opened program event if the person previously signed up in that program.

> Some of these rules can also be implemented as **[Reward Rules](doc:how-to-set-up-reward-rules)**, **[Quality Rules](doc:default-business-event-quality-rules)**, or **[Targeting Scenarios](doc:how-to-target-a-program#h_2b6a567239)** and are indicated as such below.

# **Event-based rules**

> These rules evaluate the data contained in the incoming business event.

>

## **Event Data Comparison**

> Compare event parameters against a value using string logic or patterns. This is the preferred rule for general event-data comparisons.

>

> **Examples:**

- Trigger the conversion only if product_type **equals** subscription.
- Trigger the account open event only if is_employee **equals** No.
- Trigger only if order_value **is not blank** and matches a regex.

> **Configuration:**

- **Event Data Parameter**: parameter from the incoming event (e.g., product_type, order_value).
- **Comparison**: Equals, Does not equal, Is blank, Is not blank, Contains, Does not contain, Matches Regex, Does not match Regex.
- **Value**: the value to compare against or a regex.

> **Where It Can Be Used:**

- **Trigger Rule:** If the event does not satisfy this rule, don't create the event at all
- **Quality Rule:** If the event doesn't satisfy this rule, create it, but it will be low quality
- **Reward Rules:** If the event doesn't satisfy this rule, don't send a reward
- **Targeting Scenario:** If the event satisfies this rule, target to a specific program

## **Input Event Matches Event Names**

> Matches the input event’s name (the name you send via tag, API, or file) against the event name on the flow step.

>

> **Example:** Trigger event when we receive an event with the input name free_trial_started

>

> **Configuration:**

- The name that you call the larger flow step is the same as the input event name passed. If you change the name here, it will expect the default input event name to change as well.
- This will be used on most incoming events in your flow campaign

> **Where It Can Be Used:**

- **Trigger Rule:** If the event does not satisfy this rule, don't create the event at all

>

> **Key Term: Input event name** — the name you send to Extole via tag, API, or batch file (for example: converted, free_trial_started, account_qualified). Many trigger rules match against this name.

# **Behavior & History Rules**

> These rules look at a person’s past actions and decide if an event should trigger.

>

## **Has Taken Action**

> Checks whether a person has performed a specific past business event (purchase, signup, deposit, etc.).

>

> **Examples**

- Trigger only if the person previously signed up in this campaign.
- Trigger only if the person completed 10 direct deposits in the last 60 days.

> **Configuration:**

- **Business Event**: the past event to count.
- **Minimum Count / Exact Count**: the minimum or exact number of occurrences required.
- **Recent Activity Window**: only count actions within this timeframe.
- **Minimum Action Age**: exclude actions more recent than this threshold.
- **Quality**: High / Low / Any.
- **Scope**: is this rule checked on the Journey, Campaign, Program, Any Attributed Program, or Client-wide.
- **Value Conditions**: compare numeric values from past steps (e.g., total_deposits > 1000).

> **Where It Can Be Used:**

- **Trigger Rule:** If the event does not satisfy this rule, don't create the event at all
- **Quality Rule:** If the event doesn't satisfy this rule, create it, but it will be low quality
- **Reward Rules:** If the event doesn't satisfy this rule, don't send a reward
- **Targeting Scenario**: Only enter a journey if there is a previous action

>

> **Note:** To count more than 2 business events on a person profile reliably, an **idempotency key** or **event value** is required in business event data.

## **Has Not Taken Action**

> Checks that a person has **not** performed a specific action. By default this is Exact Count = 0.

>

> **Example:** Trigger the reward only if the person has not had a cancelled event in the last 30 days.

>

> **Configuration:** Same options as **Has Taken Action**, but typically with **Exact Count = 0**.

>

> **Where It Can Be Used:**

- **Trigger Rule:** If the event does not satisfy this rule, don't create the event at all
- **Quality Rule:** If the event doesn't satisfy this rule, create it, but it will be low quality
- **Reward Rules:** If the event doesn't satisfy this rule, don't send a reward
- **Targeting Scenario:** Only enter a journey if there is a previous action

# **Person & audience rules**

> Evaluate a person’s profile data or audience membership.

>

## **Person Data Comparison**

> Compare attributes on a person profile with string logic or regex, similar to Event Data Comparison.

>

> **Example:** Trigger event if the person’s tier contains "gold", "silver", or "bronze".

>

> **Configuration:**

- **Person Data Parameter**: parameter from the user's profile (e.g., tier).
- **Comparison**: Equals, Does not equal, Is blank, Is not blank, Contains, Does not contain, Matches Regex, Does not match Regex.
- **Value**: the value to compare against or a regex.

> **Where It Can Be Used:**

- **Quality Rule:** If the event doesn't satisfy this rule, create it, but it will be low quality
- **Reward Rules:** If the event doesn't satisfy this rule, don't send a reward
- **Targeting Scenario:** If the event satisfies this rule, target to a specific program

## **Audience Membership Event**

> Triggers when a person **joins** or **leaves** an audience.

>

> **Examples:**

- Send onboarding emails to new audience members.
- Move participants between loyalty tiers automatically.
- Trigger campaigns based on audience entry or removal.

> **Where It Can Be Used:**

- **Trigger Rule:** If the event does not satisfy this rule, don't create the event at all

>

> This is usually used instead of Input Event Matches Event Names. Do **not** configure both for the same business event, they conflict and a business event will not be created.

# **Technical integration rules**

> Rules that help filter events by source or actor.

>

## **Performed by a Client Admin**

> Trigger only events that were performed by a client admin.

>

> **Example:** Require makegood events to originate from the Extole platform.

>

> **Where It Can Be Used:**

- **Trigger Rule:** If the event does not satisfy this rule, don't create the event at all

## **Performed by a Consumer**

> Trigger only events performed by consumers (not admins).

>

> **Example:** Verified consumer flows, e.g., JWT-based consumer authentication.

>

> **Where It Can Be Used:**

- **Trigger Rule:** If the event does not satisfy this rule, don't create the event at all

# **Logic & evaluation rules**

## **Rule Group**

> Group multiple rules together to create **OR** logic.

>

> **Configuration:**

- By default, multiple rules are combined with **AND**.
- Add the Rule Group with a descriptive name and then add the additional rules nested within it.

> **Example:** Trigger if cart_value < 50 **OR** product_type = subscription.

## **Custom Expression Rule**

> Evaluate a custom boolean expression for maximum flexibility.

>

> **Configuration:** Usually configured by Extole’s technical services team.

# Legacy rules

## **Event Contains Parameter *(legacy)***

> A legacy rule that checks whether an incoming event includes a specific parameter with an exact value.

>

> **Example:** Trigger only if the event includes "product_type": "subscription".

>

> **Configuration:**

- Exact value match — capitalization and punctuation must match.
- Use only for simple presence/exact-value checks (SKU, region, event type). Use **Event Data Comparison** for new configurations.

## **Profile Contains Parameter *(legacy)**

> Checks whether the person profile contains a specific parameter/value.

>

> **Example:** Trigger conversion only if "tier": "gold" appears on the profile.

>

> **Configuration:**

- Exact value match — capitalization and punctuation must match.
- Use only for simple presence/exact-value checks (SKU, region, event type). Use **Person Data Comparison** for new configurations.

>

# **Tips for managing business rules**

- **Use descriptive rule names** to make troubleshooting and handoffs much easier.
- **Test** new configurations in sandbox or with admin users before publishing.
- **Remember the default logic** uses **AND** unless you use a Rule Group.
- **Document assumptions**: note which system writes which event names and which fields are required. This prevents misconfigurations when integrations change.

>
