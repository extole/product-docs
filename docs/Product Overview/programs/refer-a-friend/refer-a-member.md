---
title: Refer a Member
excerpt: >-
  Let your members help you acquire new, high-quality members through trusted
  online and in-branch referrals.
deprecated: false
hidden: true
metadata:
  robots: index
---
## Overview

Refer a Member is Extole’s pre-configured referral program for credit unions and banks. The program type is built for the CU customer lifecycle (for example Account Opened, Direct Deposit, Debit Card Usage, Account Qualified) and ships with credit-union-specific steps, intelligent defaults, all within Flow Builder so you can make adjustments and launch quickly.

## Key features

**CU-specific flow & intelligent defaults**
Preconfigured steps for account open → account qualification, sensible pending/qualification defaults, and built-in logic to handle CU member events so launches are faster and more predictable.

**In-Branch Referral Portal**
A simple portal employees use to record in-person referrals. Branch staff enter existing member (advocate) info, and new member info, which creates the referral relationship and ensures correct attribution and rewarding.

**Printable Form**
A first-class share channel for members who prefer offline sharing: advocates can download a prefilled printable referral form to give to friends and family. Also, a new member who prefers to open an account in-person can bring the printed form to the branch; the form can optionally be pre-populated with the advocate's and friend's information to help with referral tracking.

**Flexible rewards & fulfillment**
Supports multiple reward issuers and reward types (gift cards, account credit, and more). Account credit workflows are supported via outbound integrations/webhooks so clients can fulfill and confirm rewards reliably.

**Promotions, emails & reminders**
CU-specific program communications are included (advocate/friend invitations, authentication, welcome, and reminder emails). Reminder emails are particularly useful to help new members complete the additional qualification steps after account open.

**Rules, safety, & fraud prevention**
Built-in rules for entry and qualification help prevent fraud while keeping qualification simple.

**Partner Integrations**  
You can use our partner integrations with [Q2](https://partners.extole.com/q2), [Banno](https://partners.extole.com/banno-digital-banking), and [Candescent](https://partners.extole.com/candescent) to easily connect Extole to your existing digital banking systems. Extole also supports a wide range of additional integration methods—including API-based, file-based, and client-side options, so you can launch a referral program using whichever approach best fits your environment.

## Referral Journey

Share — Advocates share using the embedded/microsite/overlay experiences, Printable Form, or In-Branch Portal.

Capture — Extole captures account_opened and account_qualified either via real-time tags/APIs or via file/SFTP prehandlers that map bank feeds into events.

Attribute & qualify — Lookback windows, audiences and quality rules attribute the correct advocate and validate qualification.

Issue reward — When qualification is met the reward is issued; account credit flows typically use an outbound webhook so the CU fulfills the reward and notifies Extole of completion.

Implementation notes & best practices

Start with the Refer a Member theme in the Program Picker — it contains defaults tuned for CUs (account open → fund → pending → qualified).

Make in-branch flows simple — ~50% of CU accounts open in branch; include the In-Branch Portal or Printable Form and keep forms minimal to reduce errors.

Use prehandlers for file feeds — when banks provide batched files, we recommend prehandlers to extract and emit account_opened and account_qualified events.

Configure lookback & anti-fraud rules early — default rules help prevent self-referrals; add security checks (e.g., MaxMind) as needed.

Plan reward fulfillment — prefer account credit for operational efficiency; coordinate the reward issuer/integration during discovery.
