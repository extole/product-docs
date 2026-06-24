---
title: "Mobile App Sharing"
slug: mobile-app-sharing
excerpt: "# Overview"
hidden: false
intercom_source_id: 10772209
---

# Overview

If you have a mobile app, tap into the time your users are spending on mobile to increase referral program participation. This guide describes the typical in-app share experience customers are implementing using Extole's Referral API and Apple's built-in iOS sharing capabilities.

# A Typical In-App Sharing Experience

The creative content served within your app is served through Extole's Marketer Control interface to allow flexibility in updating in the future. Here are four basic steps to follow:

- 

**Get and Store Token:** Get a unique token identifier for the device
- 

**Prefetch the Content:** Make a single request to Extole to create/update a profile on the user and get dynamically targeted content for calls-to-action, share sheets, etc.
- 

**Track Impression Events:** When a user sees a call to action or sharing experience, send an impression event to Extole so you have robust analytics for your program.
- 

**Share Event:** Use the sharing built into the phone for each share channel to distribute the link and content associated with that channel and send a share intent to Extole so you have robust analytics for your program.

To get details please see the [Extole Developer Center](https://dev.extole.com/docs/mobile-api).
