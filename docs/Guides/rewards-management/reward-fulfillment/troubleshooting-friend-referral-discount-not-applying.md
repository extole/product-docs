---
title: "Troubleshooting a Friend's Referral Discount Not Applying"
excerpt: "---"
---

---

**Description:** How to investigate and resolve the common support case where a referred friend reports that their refer-a-friend discount is not being applied automatically to their order.

## Overview

One of the most common refer-a-friend support questions is a referred friend saying their discount "isn't applying" or "didn't come up automatically" at checkout. In most cases the discount was never activated because the friend's referral was never **attributed** — not because the coupon itself is broken. This guide explains how attribution works, how to confirm what happened on the friend's profile, and the order in which to resolve it.

## How Friend Discount Attribution Works

A friend earns the referral discount by **clicking the referral link** an advocate shared with them. That click records a `share_click` event and starts the friend's referral journey, which is what makes the friend discount available.

Two conditions matter:

- **Opening the email is not the same as clicking.** The friend must actually click the referral button or link. An email open — including one logged by an email security scanner or inbox pre-fetch — does not create a `share_click`.
- **Cookies and browser session matter.** Attribution relies on first-party cookies set when the friend clicks the link. If cookies are disabled, or the friend clicks in one browser and then checks out in a different browser, device, or private window, the referral can be lost. For how referral cookies work, see [Extole Cookie Handling](doc:extole-cookie-handling).

If there is no recorded click, Extole never reached the point where the friend discount could be activated.

## Diagnose in the Platform

Look the friend up under **User Support** and confirm what actually happened before deciding on a fix:

1. Search for the friend by email and open their profile.
2. In the **Activity** section, look for a `share_click` and the friend's landing, sign-up, or conversion events. If referral emails were delivered and opened but there is **no `share_click`**, the referral was never attributed.
3. In the **Rewards** section, check whether any friend coupon or discount was issued. If none is present, no discount code exists to apply yet.

For related reward-status checks, see [How to Investigate a WISMR Request](doc:how-to-investigate-a-wismr-request).

## Common Causes

| What you see | Likely cause |
| --- | --- |
| Emails delivered and opened, but no `share_click` | The friend opened the email but never clicked the referral button, or a scanner logged the open |
| A `share_click` exists but on a different browser/device than checkout | Cookies were disabled or cleared, or the friend switched browsers between clicking and buying |
| The friend clicked and landed, but the discount is missing at checkout | The coupon may not be appended to the destination URL or applied at checkout — a technical or configuration issue (see When to Contact Extole) |

## Resolution Steps

Work through these in order and stop as soon as the discount applies:

1. **Have the friend retry the link in one browser session.** Ask them to reopen the most recent referral email, click the main referral button in a normal browser with cookies enabled, and continue shopping in that same session without switching browsers or devices.
2. **Send the advocate's share link directly.** If the discount still does not appear, open the advocate's profile, copy their share link, and send it to the friend to use. This gives the friend a clean, attributable path to the offer.
3. **Confirm eligibility, then issue a replacement.** If the discount still does not apply, confirm the friend is eligible and manually create the referral so a replacement friend reward is issued. See [How to Manually Create a Referral or other Event](doc:how-to-manually-create-a-referral-or-other-event).

Creating a replacement reward issues real value, so complete step 3 only after you have confirmed the specific friend and that they are eligible.

## When to Contact Extole

Contact Extole support if the friend clicked the referral link and the referral is attributed correctly but no discount was issued, or if the coupon appears in the referral link but is not applied at checkout. Include the friend's email, the advocate's email, and the approximate time of the click so the referral can be located.

## Related Articles

- [How to Investigate a WISMR Request](doc:how-to-investigate-a-wismr-request)
- [WISMR 101: Understanding Customer Reward Inquiries](doc:wismr-101-understanding-customer-reward-inquiries)
- [How to Manually Create a Referral or other Event](doc:how-to-manually-create-a-referral-or-other-event)
- [Extole Cookie Handling](doc:extole-cookie-handling)
