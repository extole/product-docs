---
title: How to Create a Reward That Triggers on Event Data
deprecated: false
hidden: false
metadata:
  robots: index
---
<Callout icon="📘" theme="info">
  ### Important Note

  Applies to **flow campaigns built on Extole's upgraded Flow Builder** (look for the flow
  icon next to the campaign name on the **Programs** page).
</Callout>

## What you're trying to do

You want a reward to be issued **only when the triggering event carries certain data** — for
example, only reward when the purchase event includes `product_id = SKU-123`, or only when
`product_type = subscription`, or only when the cart contains a specific item.

In Extole this is done with a **data-comparison rule** that reads a parameter off the incoming
event and compares it to a value. You attach that rule to the reward (or to the business event
that drives the reward) so the engine only pays out when the data matches.

## How rewards and rules fit together

A reward in Flow Builder fires through a chain:

```
Incoming event (carries data: product_id, cart_value, ...)
   -> business event is created (subject to Trigger Rules + Quality Rules)
   -> Reward evaluates its Reward Rules
   -> if ALL reward rules pass -> reward issued
```

So "trigger a reward on data" means **adding a data condition somewhere in that chain**. You have
two natural places to put it, and the choice matters:

| Where you add the rule                   | Effect when the data does **not** match                         | Use when                                                                     |
| ---------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Reward Rule** (on the Reward node)     | The business event is still recorded, but **no reward is sent** | You still want to track the event/conversion for reporting, just not pay out |
| **Trigger Rule** (on the business event) | The business event is **not created at all**                    | You don't even want to record the event unless the data matches              |

For most "only reward when product X" requests, a **Reward Rule** is the right choice — you keep
full event tracking and only gate the payout.

The rule type you'll use in both places is **Event Data Comparison**.

***

## Option A — Gate the reward with a Reward Rule (recommended)

This issues the reward only when the event data matches, while still recording the event.

1. Go to the **Programs** page and find your campaign.
2. Click the **Manage Flow** icon for that campaign.
3. In Flow Builder, find the **Reward** you want to gate (e.g. the advocate reward on<br />friend conversion, or a reward-for-action outcome).
4. Scroll to the **Reward Rules** section for that reward.
5. Click **+ New Reward Rule** and choose **Event Data Comparison**.
6. Configure the comparison:
   - **Event Data Parameter** — the parameter name as it arrives on the event, e.g. `product_id`
     (or `product_type`, `account_type`, `order_value`).
   - **Comparison** — one of: _Equals, Does not equal, Is blank, Is not blank, Contains, Does not
     contain, Matches Regex, Does not match Regex_.
   - **Value** — the value (or regex) to compare against, e.g. `SKU-123`.
7. Give the rule a **descriptive name** like `Only reward for SKU-123` so it's easy to
   read in troubleshooting.
8. Click **Apply** to save.

Remember: **all** reward rules on a reward must pass for the reward to be granted (they combine
with **AND**). Don't add a data rule that unintentionally blocks the default risk/limit rules.

### Example: reward only for a specific product

- Event Data Parameter: `product_id`
- Comparison: **Equals**
- Value: `SKU-123`

Only events whose payload includes `"product_id": "SKU-123"` will issue the reward.

***

## Option B — Suppress the event entirely with a Trigger Rule

Use this when you don't even want to create the business event unless the data matches (e.g. only
record a conversion at all when `product_type = subscription`).

1. **Programs** → **Manage Flow** → open the **business event** step (e.g. _Converted_).
2. Turn on the **advanced filter** to reveal **Trigger Rules** (Trigger Rules are hidden until the
   advanced filter is on).
3. Click to add a **Trigger Rule** → **Event Data Comparison**.
4. Configure **Event Data Parameter**, **Comparison**, and **Value** exactly as in Option A.
5. **Apply**.

If the incoming event fails the trigger rule, Extole **does not create the business event**, so no
downstream reward, email, or reporting step happens for it.

***

## Common data patterns

| You want to…                                 | Comparison         | Value                     |
| -------------------------------------------- | ------------------ | ------------------------- |
| Reward only for one product                  | **Equals**         | `SKU-123`                 |
| Reward for anything except a product         | **Does not equal** | `SKU-123`                 |
| Reward only when a product id is present     | **Is not blank**   | _(none)_                  |
| Reward when a cart/SKU list contains an item | **Contains**       | `SKU-123`                 |
| Reward for a family of SKUs                  | **Matches Regex**  | `^SHOE-(RUN\|TRAIL)-\d+$` |

> **Multiple items / arrays.** If your event sends a list of products (e.g. a cart of SKUs in one
> field), use **Contains** or **Matches Regex** rather than **Equals**, since the field holds more
> than a single value.

> **More than a value check.** For richer logic (combinations of fields, math, nested data), use a
> **Rule Group** to build OR logic, or a **Custom Expression Rule** for a custom boolean expression.
> Custom Expression Rules are typically configured with Extole's technical services team.

***

## Prerequisite: the data must actually be on the event

A data rule can only compare a parameter that is **sent on the event**. Before configuring the
rule, confirm your integration includes the field:

- **JS tag / API:** include the parameter in the event `data`, e.g.
  `{ "event_name": "conversion", "data": { "product_id": "SKU-123", "cart_value": "129.00" } }`.
- **Batch file:** include a column for the parameter and map it to event data.

The **Event Data Parameter** name in the rule must match the parameter name you send, exactly
(names are case/spelling sensitive). If the field isn't present, **Equals** will fail and
**Is blank** will pass.

***

## Test before you publish

1. Use a **sandbox** or an **admin test user** to send a matching and a non-matching event.
2. Confirm the matching event issues the reward and the non-matching one does not.
3. If a reward you expected didn't issue, open the participant in **User Support** and expand the
   reward's rules to see exactly which rule failed.
4. Publish once the behavior is confirmed.

***

## Troubleshooting

- **Reward never issues, even for matching data.** Check that the parameter name in the rule
  matches the parameter you send (spelling/case), and that the value matches the comparison type
  (e.g. **Equals** is exact — capitalization and punctuation must match).
- **Reward issues for everything.** The data rule may not be on the reward — confirm it's listed
  under that reward's **Reward Rules**, not on a different reward or event.
- **Event isn't even recorded.** You may have added the rule as a **Trigger Rule** (which suppresses
  event creation) when you meant a **Reward Rule** (which only gates payout). Move it accordingly.
- **List/array field never equals.** Switch **Equals** to **Contains** or **Matches Regex**.

***

## Related Help Center articles

- [How to Set Up Reward Rules](https://success.extole.com/en/articles/12010895-how-to-set-up-reward-rules)
- [Common Trigger Rules](https://success.extole.com/en/articles/13015994-common-trigger-rules) — full reference for Event Data Comparison and other rule types
- [How to Set Up Business Event Rules](https://success.extole.com/en/articles/12020840-how-to-set-up-business-event-rules)
- [Configuring the Rules of Your Program](https://success.extole.com/en/articles/10772175-configuring-the-rules-of-your-program)
- [How to Set Up a Reward for Action Offer Program](https://success.extole.com/en/articles/13612885-how-to-set-up-a-reward-for-action-offer-program)

<br />
