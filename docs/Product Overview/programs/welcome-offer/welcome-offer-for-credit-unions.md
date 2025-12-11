---
title: Welcome Offer for Credit Unions
excerpt: >-
  A credit-union-specific Welcome Offer program type with CU-focused business
  events, safe defaults, and creative tweaks so credit unions can launch faster.
deprecated: false
hidden: true
metadata:
  robots: index
---
# Welcome Offer — Credit Unions

> A credit-union-specific Welcome Offer program type with CU-focused business events, safe defaults, and creative tweaks so credit unions can launch faster with less Solutions help.

***

## Overview

The **Welcome Offer for Credit Unions** is a Flow Builder program type that reuses Extole’s standard Welcome Offer experience but is tailored for credit unions (CUs). It packages CU-specific business events, sensible default rules, and creative changes so marketers at credit unions can spin up a working welcome offer quickly and safely. The goal is to reduce the number of manual adjustments and eliminate the need for Solutions in the majority of launches.

**Why this exists**

* Matches common CU business events (Account Opened, Account Qualified, etc.).
* Ships with CU-friendly defaults (embedded experiences, pending periods, annual reward limits).
* Reduces creative and setup work by providing a CU theme and copy adjustments.

> If you’re unfamiliar with the standard Welcome Offer program, see the general Welcome Offer docs for basic flow, promotion, and reporting guidance.

***

## What’s included (high level)

* **Business events** reflecting credit union flows: `Account Opened`, `Account Qualified`, `Account Qualified Reward`, plus Promotion Viewed / Promotion Clicked / Signed Up events. These events include the data fields credit unions need (for example, `AccountId`). 
* **Program safety** defaults so multiple programs (RAM and Welcome Offer) interoperate safely; RAM is treated with higher priority by default.
* **Default Flow Builder rules** tuned for CUs (embedded welcome experience enabled, microsite disabled by default, 60-day pending period, annual reward limit).
* **Creative changes / CU theme**: welcome experience and emails are adjusted to feel credit-union specific rather than retail. A CU theme is created from the standard Welcome Offer theme.

***

## Key behaviors & defaults

### Business events & journeys

The CU Welcome Offer ships with event and journey support focused on account lifecycle:

* **Promotion Viewed / Promotion Clicked** — onsite promotions (overlay, banner), with embedded welcome experiences enabled by default.
* **Signed Up** — program sign-up behavior; base quality rule: has an email address.
* **Account Opened** — actions: Account Opened Welcome Email, Account Opened Reminder Email. Includes `AccountId`.
* **Account Qualified** — triggers publishing to the Account Qualified Reward.
* **Account Qualified Reward** — reward entries tied to Account Qualified, with CU reward rules.

### Default reward rules (CU-specific)

By default the program includes these reward constraints to keep CU programs safe and compliant:

* **Qualifying Account** — reward only for qualifying accounts.
* **Has Email Address** — participants must have email to receive reward communications.
* **Has Not Been Rewarded** — single reward per qualification as appropriate.
* **Risk Evaluation** — fraud checks to prevent abuse.
* **60-Day Pending Period** — a pending waiting period that starts from `Account Opened` (default: 60 days).
* **Total Annual Reward Limit** — default **$600** annual cap (note: planned update to $2,000 for 2026).

### Flow Builder defaults / creative

* **Embedded Welcome Experience enabled** (preferred for CUs).
* **Welcome Experience Microsite disabled by default** (avoids telling members they are leaving the CU website).
* CU theme and copy are provided so the welcome popup, emails, and reminders read as CU communications rather than retail marketing.

### Program safety with other programs

Program priority and default rules ensure safe interaction when a client runs multiple Welcome Offers (or RAM). RAM is set at higher priority than the CU Welcome Offer so that RAM journeys continue to operate as intended; runbook guidance is included to handle co-running programs.

***

## Launch & configuration (marketer workflow)

1. **Add a Welcome Offer** — choose the _Welcome Offer (Credit Unions)_ program type.
2. **Create a new program** — Flow Builder campaign with CU defaults pre-applied.
3. **Review business events** — ensure `Account Opened` and `Account Qualified` mappings match your account provisioning events and pass `AccountId`.
4. **Adjust creative if desired** — CU theme + email templates are provided; update copy or branding as needed.
5. **Review safety & reward caps** — verify pending period, qualification rules, and annual limits meet your regulatory and business requirements.
6. **Test RAM + WO interactions** — validate priority behavior if you run RAM or other programs.

***

## Success criteria & metrics

This feature is intended to deliver:

* Faster launches for credit unions with fewer customizations and less Solutions team involvement.
* Increased number of CU Welcome Offer launches and improved CU performance (account opens and Extole-influenced new customer rate).

Standard metrics surfaced in the Admin Tool for CU Welcome Offers include:

* Number of launches, days to launch, percent requiring Solutions help.
* Campaign metrics: Promotion Views, Promotion Clicks, Email Captures, Submit Rate, Purchases, Conversion Rate, and Extole-Influenced New Customer rate.

## Developer & product notes

* The CU **theme** is created from the default Welcome Offer theme and removes retail events while adding `Account Opened`, `Account Qualified`, and `Account Qualified Reward`.
* The default **New Customer (New Member)** journey priority is changed to `400` and the selector is adjusted to `Target` to meet CU requirements — this is important for correct program ordering.

***

## UX / UI & creative

* No new administrative UI is required for the BU events or defaults.
* Creative changes (emails, microsites, and the embedded welcome flow) are provided as a CU theme and can be adapted in the template editor. See the CU creative sub-document for sample layouts and copy.

***

## Scenarios & testing guidance (recommended)

* Verify `Signed Up` → `Account Opened` → `Account Qualified` flow with a test account and `AccountId` present.
* Confirm pending period behavior (60 days) and that qualifying deposits/funding trigger `Account Qualified`.
* Test interactions with RAM (both when friends have and haven’t engaged with RAM flows) to ensure expected priority behavior.

***

## Future directions

Planned/possible enhancements:

* In-branch portal support (moved to “Extensions” since it’s common across RAM and WO).
* Direct-mail/printed materials support and an option for a static promo code (e.g., `WELCOME2025`).
* Revisit program safety with pools (long-term solution for program priority).

***

## Examples & case studies

For reference on how standard Welcome Offers behave and typical CTA / reporting expectations, see the general Welcome Offer documentation and examples. The CU program reuses the same reporting and promotion patterns but with the CU event model and defaults applied.

***

## Quick contact

If you’re a marketer at a credit union and need help launching, follow the runbook linked above. For technical questions about Flow Builder implementations or changing priority/selector behavior, contact the Product/Engineering owners listed in the story.

<br />
