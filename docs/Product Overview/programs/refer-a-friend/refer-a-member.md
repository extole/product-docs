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

<Image align="center" border={false} width="500px" src="https://files.readme.io/7368c4b24ce1e22c3580c202a6bf8296d2bd8b6015a9557ebbbeaa171dd768af-Screenshot_2025-12-12_at_2.34.02_AM.png" />

## Key features

**CU-specific flow & intelligent defaults**
Preconfigured steps for account open → account qualification, sensible pending/qualification defaults, and built-in logic to handle CU member events so launches are faster and more predictable.

**In-Branch Referral Portal**
A simple portal employees use to record in-person referrals. Branch staff enter existing member (advocate) info, and new member info, which creates the referral relationship and ensures correct attribution and rewarding.

<Image align="center" border={false} width="500px" src="https://files.readme.io/e864894c3dfa6a8f883257dcf53a9669a8c236f43c5909036b8682d4af1334f8-Screenshot_2025-12-12_at_2.35.41_AM.png" />

**Printable Form**
A first-class share channel for members who prefer offline sharing: advocates can download a prefilled printable referral form to give to friends and family. Also, a new member who prefers to open an account in-person can bring the printed form to the branch; the form can optionally be pre-populated with the advocate's and friend's information to help with referral tracking.

<Image align="center" border={false} width="500px" src="https://files.readme.io/d5a86bfc2b00b640834a22a3985c704744e0f740dadb79b0baeb0f66825e3a87-Screenshot_2025-12-12_at_2.30.05_AM.png" />

**Flexible rewards & fulfillment**
Supports multiple reward issuers and reward types (gift cards, account credit, and more). Account credit workflows are supported via outbound integrations/webhooks so clients can fulfill and confirm rewards reliably.

**Promotions, emails & reminders**
CU-specific program communications are included (advocate/friend invitations, authentication, welcome, and reminder emails). Reminder emails are particularly useful to help new members complete the additional qualification steps after account open.

**Rules, safety, & fraud prevention**
Built-in rules for entry and qualification help prevent fraud while keeping qualification simple.

**Partner Integrations**  
You can use our partner integrations with [Q2](https://partners.extole.com/q2), [Banno](https://partners.extole.com/banno-digital-banking), and [Candescent](https://partners.extole.com/candescent) to easily connect Extole to your existing digital banking systems. Extole also supports a wide range of additional integration methods—including API-based, file-based, and client-side options, so you can launch a referral program using whichever approach best fits your environment.

<Image align="center" border={false} width="700px" src="https://files.readme.io/7a6fc318f5213c799078451a2108c56706e415b3ab6383091d174d7ae2d53de1-Screenshot_2025-12-11_at_1.29.14_AM.png" />

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
