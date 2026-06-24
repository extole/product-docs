---
title: "Delivering Share Messages"
slug: delivering-share-messages
excerpt: "# Overview"
hidden: false
intercom_source_id: 10772058
---

# Overview

Extole gives your advocates the ability to share your brand and specific products right on your site. Advocates can share with their friends through a variety of social channels, email, or a personal share link. When your advocates share via email, their message is sent from their email address.

Extole follows industry best practices, and identifies who is sending an email, how the email is routed, and whether the email is compliant with opt-out management and CAN-SPAM. This is so that all major email providers will properly consider your advocate's emails valid and clean. This has the added bonus of ensuring that your emails are compliant with regulations, have high deliverability rates, and don't end up in a spam folder or Gmail's "promotions" tab. We do this by using three main email validation methods: SPF, DKIM and DMARC.

All Extole share emails come from the sharing advocate's email address or via referral-mail.com. Our Client Services Managers work with you to make sure your emails follow industry best practices and end up where your advocates intend: their friend's primary email inbox.

# Managing Your Opt-Out List

Messages sent from your referral program include an opt-out link so that they are compliant with CAN-SPAM. You must sync your program's opt-out list with Extole on a regular basis. For more information, check out our article on [Opt-Out List Management](https://success.extole.com/hc/en-us/articles/201898346-Opt-Out-List-Management).

# Sender Policy Framework (SPF)

Extole uses SPF header records. The SPF system is designed to ensure that all email headers contain a valid return path to sending domain. Extole sends a return-path header with a bounce-back address. This way, if delivery fails, the email can be tracked through our email service.

The return-path header looks similar to:Return-Path: <bounces+uniqueid-fromaddress@email.referral-mail.com>

You can read more about SPF at [http://www.openspf.org](http://www.openspf.org)

# DomainKeys Identified Mail (DKIM)

Extole includes a DKIM signature. The DKIM system is designed to let an email sender sign the contents of an email message. This ensures that the contents of a message were generated from a specific domain and have not been tampered with.

Extole's DKIM signature looks similar to this:

DKIM-Signature: v=1; a=rsa-sha1; c=relaxed; d=referral-mail.com; h=from
 :to:subject:mime-version:content-type; s=smtpapi; bh=0W+D+OmGSGw
 AB17vNm0RcF6JNWY=; b=NoF/Ottn532gq5dp3RoeHo6R0QNEeOo2DAONj2GANlD
 AVDwPcEtyoQYXyb331AoPYfjyAqO0dmHY2RaLbVQuDFslQx2zPOnU7YpPCphRw1l
 F0x4C2WFboP+Vc93BdEu/iiGcgB73s6X1Cgyn4AjT1ZeXRM/mzZmW8KnavqFPVa4
 =

You can read more about DKIM at [http://www.dkim.org/](http://www.dkim.org/)

# Domain-Based Message Authentication, Reporting, and Conformance (DMARC)

DMARC provides additional requirements on top of SPF and DKIM to make sure that email senders are conforming to industry standards by reliably protecting email recipients. The main rule applied by DMARC ensures that the domain used in the "from:" header is the same as the domain protected by SPF and DKIM, even though SPF and DKIM don't require this.

By default, Extole emails do not conform to DMARC since sharing messages are "from" an advocate. A typical message from **[advocate@examplemail.com](mailto:advocate@examplemail.com)** would look like the following:

From: advocate@examplemail.com
Return-Path: <bounces+uniqueid-advocate=examplemail.com@email.referral-mail.com>

In the above example, the SPF and DKIM protection applies to the Extole email domain "email.referral-mail.com". Email systems like Gmail will display this information in a "via" element, while other email systems might not:

![GmailViaExample_2014-03-17_15-45-38.png](https://extole-5ef307a0e5b1.intercom-attachments-7.com/i/o/syy27wia/1421733551/98e2dacb603d5d9c364acbc1fd48/upload_15037685207268088782?expires=1782324000&signature=c72b4540aa0a447cb29812b32ac086d115a59484e072228ee95b17237af7fb7a&req=dSQlF859noRaWPMW3nq%2BgUUbnG%2FJBOiBREIOHbZsHLR2prndbo6O8NTBvSEY%0Ae653HAiDWFw1gnRedKWZCpEH0Ts%3D%0A)

Extole recommends the "via" approach, as it results in higher delivery rates for share messages. This approach also keeps with the spirit of the email system - the advocate is sending this message personally, and your referral program is facilitating it.

DMARC compliance requires updating the "from:" address to match the Extole domain of "email.referral-mail.com". The best option is to set your "from:" address to be **"[advocate@examplemail.com](mailto:advocate@examplemail.com) <[do-not-reply@email.referral-mail.com](mailto:do-not-reply@email.referral-mail.com)>**".

Doing this will make your emails fully SPF, DKIM, and DMARC compliant. Share messages will appear without the "via" element in Gmail:

![FromReferralMail_2014-03-17_16-31-19.png](https://extole-5ef307a0e5b1.intercom-attachments-7.com/i/o/syy27wia/1421733552/b1ab18f5466f796bbea3a17840d0/upload_7485174986293780507?expires=1782324000&signature=6d9cd6653ef8a9f7c348705f783616d7059dc1111c9246cea8a9ab2bb027eedd&req=dSQlF859noRaW%2FMW3nq%2BgdD2sKGbHV8C577Rid4lNrrSK%2BCupBPZ5jESB0rS%0AsjWFo0AHPRLhDA1bTkA4QCCTkzk%3D%0A)

You can read more about DMARC at [http://www.dmarc.org/](http://www.dmarc.org/)

# Frequently Asked Questions

## Why does my subject make my message become spam or promotional?

The email sent from an advocate to a friend should be as close to a personal email as possible. The more you put banners, marketing, and other promotional materials into the email, the greater the likelihood that the email will be interpreted as a promotional message.

We've seen subjects like "Welcome to the Refer a Friend Program, where you can earn money…" go to the junk folder, while the same message with a subject of "Welcome to the Refer a Friend Program, where you can earn rewards…" goes to the primary inbox. Our Client Services Managers will help you decide on the most effective subject line.

## Why are messages marked as spam when people at my company share?

Sometimes messages in Gmail get filtered into the spam folder saying: "Be careful with this message. Our systems couldn't verify that this message was really sent by yourcompany.com. You might want to avoid clicking links or replying with personal information."

![BeCarefulwithThisMessage_2014-01-13_11-30-33.jpg](https://extole-5ef307a0e5b1.intercom-attachments-7.com/i/o/syy27wia/1421733557/8d4aa7b5cd1651df7231fdc3b259/upload_17488369953841889802?expires=1782324000&signature=846428bbbf982abd52816008599e4f305ffa06786a99dfd270be651ca661c38d&req=dSQlF859noRaXvMW3nq%2Bge77V3n4c0ezr%2FL8Ux%2Bv8b7dnl3pv8FI9L8dGfz9%0AHk8kKdFjk5iQi8uqvUQ743h0jaA%3D%0A)

This is most likely caused because your corporate email has a very restrictive SPF record set. Normally, the SPF record is designed to validate against the return-path header in the message. Extole uses a valid return-path with an SPF record.

Some email services, like Gmail, check the SPF record at the domain of the "from:" header. If your corporate domain explicitly fails (-all) domains which are not in the passing list, this message will appear. Most SPF records either provide neutral guidance or a soft fail (~all) for domains not listed, but your company may have a more aggressive configuration.

This won't affect advocates sending from Gmail, Yahoo Mail, Hotmail, etc., but there are two ways you can remove this message from your corporate emails:

- 

(Recommended) You can have your IT add Extole's email IP into the list of valid IPs in your corporate SPF record.
- 

You can change the "from:" address of your sharing message so that instead of coming from an advocate's provided email, it will come from "My Company Share Program <[do-not-reply@email.referral-mail.com](mailto:do-not-reply@email.referral-mail.com)>". This will cause your messages to go into the "promotional" tab of Gmail's inbox.

## Why is Gmail warning that this message couldn't be verified as sent by Gmail?

Sometimes messages in Gmail get filtered into the spam folder saying: "Be careful with this message. Our systems couldn't verify that this message was really sent by gmail.com. You might want to avoid clicking on links or replying with personal information."![image](https://extole-5ef307a0e5b1.intercom-attachments-1.com/i/o/syy27wia/1421733550/5a48838b7d4f20ad907d419ceb3b/restricted-return_to%3Dhttps-3A-2F-2Fsuccess_extole_com-2Fhc-2Fen-us-2Farticle_attachments-2F202361448-2FCouldntVerify.png?expires=1782324000&signature=eba7d8df240d97fde08ac9d366f769e494096abb98d181eaefaf10470bfa98e9&req=dSQlF859noRaWfMW3nq%2BgfttfW6qHjSbGyjzjDd4XorJ74iwP%2BckfdPrDP3C%0AFS4%2BLEvwdrSTTLpccOawc7fgdvY%3D%0A)

This is most likely caused because the Advocate has incorrectly entered his email address and Gmail is able to detect that it is not a valid Gmail address. For example if an advocates email is "[ilovetoshare@gmail.com](mailto:ilovetoshare@gmail.com)" but the advocate incorrectly enters "[lovetoshare@gmail.com](mailto:lovetoshare@gmail.com)" (The 'i' is missing at the start), Gmail may detect that there is no such email address inside of Gmail and will show this warning message.
