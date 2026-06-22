---
title: "Tracking Conversions with a Mobile App"
slug: tracking-conversions-with-a-mobile-app
excerpt: "In the modern cross-channel world, friends frequently see share messages on their mobile devices and go on to convert."
hidden: false
intercom_source_id: 10772208
---

In the modern cross-channel world, friends frequently see share messages on their mobile devices and go on to convert.

If the friend's journey involves downloading a mobile app as part of their conversion process, then it's important to track the friend's referral journey from the time they receive their email to the time they convert—regardless of whether that conversion is an app download, registration in the app, or other action inside of the mobile app.

There are three main ways to track the journey of an app download and installation.

# Overview

- 

[Friend Registration](#friend-registration) - Have the friend register on a website on their phone before proceeding to download the app.
- 

[Friend Promo Code](#friend-promo-code) - Provide the friend a promotional code they can enter inside of the app.
- 

[Mobile Analytics Integration](#mobile-analytics) - Use a mobile product like TUNE (formerly MAT), Yozio, Branch Metrics to automatically track the conversion.

# Friend Registration
![image](https://extole-5ef307a0e5b1.intercom-attachments-1.com/i/o/syy27wia/1421734595/80d93e4b78daa37635f17377c1b9/restricted-return_to%3Dhttps-3A-2F-2Fsuccess_extole_com-2Fhc-2Fen-us-2Farticle_attachments-2F202634708-2FRegistration-Page.png?expires=1782259200&signature=274f53913ecd81b052c308301c77677fb6a908a8bd0983725c5aa67202a99334&req=dSQlF859mYRWXPMW3nq%2BgZHup6NL6dD70v9RCs00pw2wXCxbaUTdX%2FGwqWSH%0AP9hDYE0f1gL%2FwxAApKJ7O3%2FgEzg%3D%0A)

1. The friend receives a referral email or sees a referral link on your website or social media. The friend taps on the link and is taken to a website landing page. This page has Extole tags on it and will display a promo code to the friend.

2. The friend registers with their name and email on the website. When the friend registers it makes a registration call to Extole using either a page tag or REST API. A unique ID, such as account number, should be passed as the partner conversion ID.

See: [How to Track a Friend Registration Step](https://intercom.help/extole-9fe74198ce07/en/articles/10772211)

3. Direct the user to the app download page for their device so they can download and install the app.

4. After downloading, the friend will launch the app.

5. When the friend launches the app for the first time, they will be presented with the login page. When they log in to the mobile app for the first time, track the conversion event with Extole.

See: [Create Registration/Conversion Endpoint](https://success.extole.com/hc/en-us/articles/201898406)

6. If Extole is providing a gift card to the friend, it will be automatically mailed. If the app is applying a credit or other internal reward, it can be applied. The advocate will earn their gift card or promo code in an email.

# Friend Promo Code
![image](https://extole-5ef307a0e5b1.intercom-attachments-1.com/i/o/syy27wia/1421734596/73750b444c0b026ceecdc42993b4/restricted-return_to%3Dhttps-3A-2F-2Fsuccess_extole_com-2Fhc-2Fen-us-2Farticle_attachments-2F202634738-2FPromo-Code.png?expires=1782259200&signature=c0586b13eb2109ad06fc535d14d2e1b3ffc278be036553f926d11f26e5c09fc0&req=dSQlF859mYRWX%2FMW3nq%2BgR8VBIEpKgaCM7awC6kluvev%2FMyuMR5ICP2Tc6JN%0ACuE9AtCwherz1t9bHq%2F1B7IfVDY%3D%0A)

1. The friend receives a referral email or sees a referral link on your website or social media. The friend taps on the link and is taken to a website landing page.

2. This page has Extole tags on it and will display a promo code to the friend. They will then be directed to the app download page for their device so they can download and install the app.

3. After downloading, the friend will launch the app.

4. When the friend launches the app for the first time they will be presented with the login page.

5. The friend goes to the "My Account -> Apply Promo" menu and enters the promo code. This sends a conversion event to Extole and passes a unique ID for the account and the promo code. Extole returns with a success.

See: [Create Registration/Conversion Endpoint](https://success.extole.com/hc/en-us/articles/201898406)

6. If Extole is providing a gift card to the friend, it will be automatically mailed. If the app is applying a credit or other internal reward, it can be applied. The advocate will earn their gift card or promo code in an email.

# Mobile Analytics Integration
![image](https://extole-5ef307a0e5b1.intercom-attachments-1.com/i/o/syy27wia/1421734597/0874267c643cd266d85b88f976e7/restricted-return_to%3Dhttps-3A-2F-2Fsuccess_extole_com-2Fhc-2Fen-us-2Farticle_attachments-2F202559387-2FMAT-Conversions.png?expires=1782259200&signature=9f86b6be486cf979741f008ba36c4ded720e939153d2dfd675bb5d9eb7594953&req=dSQlF859mYRWXvMW3nq%2BgdnOB%2BKZ8LSKHgV3QB2B3%2FVKsvVu4MpnG%2BUEcb%2BH%0AFnve4d%2FYQHUCl2g4ISPF4Z0gxo0%3D%0A)

1. The friend receives a referral email or sees a referral link on your website or social media. The friend taps on the link. The link first goes to the Extole Share Link to begin tracking and then redirects to the mobile analytics link.

2. The mobile analytics link provided by TUNE, Yozio, Branch Metrics, etc. stores the Extole tracking identifier and takes the friend to the correct app store.

3. After downloading, the friend will launch the app.

4. When the friend launches the app for the first time, or after registration, a tracking call is made to your mobile analytics software. The software uses device fingerprinting to reconcile the phone with the one that clicked on the link. The software is then able to find Extole's tracking identifier and make a callback to Extole to track the conversion.

5. If Extole is providing a gift card to the friend, it will be automatically mailed. If the app is applying a credit or other internal reward, it can be applied. The advocate will earn their gift card or promo code in an email.

See: [TUNE (Formerly MAT) Integration](https://success.extole.com/hc/en-us/articles/206943037)
