---
title: GDPR / CCPA
excerpt: >-
  Learn about Extole's responsibility under the General Data Protection
  Regulation (GDPR) and California Consumer Protection Act (CCPA).
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
  pages:
    - type: basic
      slug: ada-compliance
      title: ADA Compliance
    - type: basic
      slug: iso-27001-certification
      title: ISO 27001 Certification
    - type: basic
      slug: cookie-handling
      title: Cookie Handling
---
## Overview

[//]: # "How does Extole comply with the General Data Protection Regulation (GDPR) and the California Consumer Protection Act (CCPA)?"

Under the General Data Protection Regulation (GDPR), Extole acts as data processor that processes data in accordance with services agreements and data processing agreements of the Extole Client that acts as the data controller. Under the California Consumer Protection Act (CCPA), Extole acts as a service provider that processes data in accordance with a business purpose defined in services agreements with the Extole Client that acts as the business.

[//]: ___

## Product Offerings

[//]: # "How does Extole handle processing and cookie consent?"

### Advocate Processing Consent

If your security team requires advocates to give consent for processing their data, you have to option to turn on a consent checkbox that would require the advocate to check prior to sharing. If the advocate does not click to consent, they will not be able to share.

### Friend Processing Consent

There might also be a security requirement that the friend needs to give data processing consent before being able to participate in the referral program. If this is the case, Extole has an option to turn on a MailTo email send where the advocate sends the referral email using their native mail client. This prevents Extole from being able to capture the friend's email address on share. It also prevents Extole from having visibility into the share message. The share experience is exactly the same, however, the Send Email button pops the mail application rather than sending using Extole.

### Cookie Consent

Cookie consent for referrals should be no different from cookie consent for your website. If you have a cookie consent part of your existing consumer experience, you can pass that consent to Extole.

The only time you will want to use Extole for cookie consent is if you have a standalone share page. In this case, you have the option to enable cookie consent on that microsite which will set consent on that person's profile. This will turn on a little floater on the bottom left-hand corner of the page where the user can accept the use of cookies.

[Learn more about cookie handling at Extole](https://docs.extole.com/docs/cookie-handling).

[//]: ___

## Data Subject Rights

[//]: # "What data subject rights does Extole adhere to?"

### Right to Access

Acting as a data processor, Extole provides APIs that allow you to make realtime requests for information available on any data subject, including profile information, referral events, quality scoring, customer journey information, advocates and relationships, and all other information collected on a data subject. You are responsible for the implementation of any realtime query system.

You may also request for Extole to provide this set of information through reporting based on service requests to the Extole Support team.

### Right to Data Portability

Acting as a data processor, Extole provides APIs that allow you to request information available on any or all data subjects, including profile information, referral events, quality scoring, customer journey information, advocate and relationships, and all other information collected on a data subject. You are responsible for the implementation of any full export system.

You may also request for Extole to provide this set of information through reporting based on service requests to the Extole Support team.

### Right to Correction

The data controller is able to update most profile information, relationship information, as well as override scoring algorithm through Extole's API.

Correction requests for historical event information, which is not editable through the API, must be made to the Extole Support team.

### Right to Erasure

You can make erasure requests to Extole either via email to the Support team or via API. 

Once a request is made, Extole will irreversibly psuedoanonymize the profile of the individual so that the profile is no longer connected to the individual through the program. If the individual re-engages with the referral program, a new profile is created, unrelated to the previous profile. Making another erasure request will successfully delete this new profile.

[//]: ___

## Data Processing

[//]: # "What is Extole's data processing agreement?"

### Data Processing Agreement

Extole is a certified under the EU-U.S. Data Privacy Framework Principles. [See the Extole Privacy Shield certification at Extole, Inc. Privacy Shield (Active)](https://www.privacyshield.gov/participant?id=a2zt0000000TOFPAA4&status=Active).

As part of Extole's GDPR readiness, Extole customers will have a choice to enter into our standard Data Processing Agreement (DPA) that includes the European Commission-approved Standard Contractual Clauses (Model Clauses). If you are an Extole customer and wish to enter into our DPA, please reach out to your Extole Customer Success Manager. 

[//]: ___

### Extole Sub-Processors

[//]: # "What are Extole's data sub-processors?"

A sub-processor is a third party data processor engaged by Extole who has or potentially will have access to or process Service Data. Extole engages different types of sub-processors to perform various functions as explained below.

#### Infrastructure Sub-Processors

Extole owns or controls access to the infrastructure that Extole uses to host Service Data. The Extole production systems are located in the United States.

| Entity Name              | Entity Type            |
| :----------------------- | :--------------------- |
| Amazon Web Services Inc. | Cloud Service Provider |

#### Service Sub-Processors

Extole works with certain third parties to provide specific functionality within the Services. These providers are the sub-processors set forth below. In order to provide the relevant functionality these sub-processors access Service Data. Their use is limited to the indicated Services.

[block:parameters]
{
  "data": {
    "h-0": "Entity Name",
    "h-1": "Purpose",
    "h-2": "Data Shared",
    "0-0": "Twilio",
    "0-1": "Extole uses Twilio (SendGrid) to send program emails to participants.",
    "0-2": "Email",
    "1-0": "Auth0",
    "1-1": "Extole may use Auth0 to allow for SSO (single sign-on) authentication of users.",
    "1-2": "Email  \nAdditional identifiers optionally passed by the client's IdP ",
    "2-0": "Tango Card",
    "2-1": "Extole may use Tango Card when delivering electronic gift card rewards through email to program participants.",
    "2-2": "Client Identifier  \nRecipient Email - person earning gift card  \nGift Card SKU  \nGift Card Value ",
    "3-0": "Tremendous",
    "3-1": "Extole may use Tremendous when delivering electronic gift card rewards through email to program participants.",
    "3-2": "Client Identifier  \nRecipient Email - person earning gift card  \nGift Card SKU  \nGift Card Value",
    "4-0": "Blackhawk Network",
    "4-1": "Extole may use Blackhawk Network when delivering electronic gift card rewards or USPS gift card rewards to program participants.",
    "4-2": "Client Identifier  \nRecipient Email - person earning gift card  \nRecipient Mailing Address  \nGift Card SKU  \nGift Card Value ",
    "5-0": "MaxMind",
    "5-1": "Extole may use MaxMind for the GeoIP database and minFraud services to augment Quality Rule decisions.",
    "5-2": "IP Address",
    "6-0": "Intercom",
    "6-1": "Extole uses Intercom to manage Tier 1 client requests from client organizations to Extole.",
    "6-2": "As part of Extole support servicing these requests, limited PII for a program may be shared through these tools.",
    "7-0": "Atlassian",
    "7-1": "Extole uses Atlassian JIRA to manage Tier 2 client requests from client organizations to Extole.",
    "7-2": "As part of Extole support servicing these requests, limited PII for a program may be shared through these tools.",
    "8-0": "Slack Technologies",
    "8-1": "Extole uses Slack to securely communicate internally or externally to a Client organization.",
    "8-2": "As part of Extole support servicing client requests, limited PII for a program may be shared through these tools.",
    "9-0": "Google",
    "9-1": "Extole uses Google Workspace for corporate intranet.",
    "9-2": "Extole intranet resources may contain client contact information."
  },
  "cols": 3,
  "rows": 10,
  "align": [
    "left",
    "left",
    "left"
  ]
}
[/block]


[//]: ___