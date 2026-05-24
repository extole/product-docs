---
title: "REST APIs"
excerpt: "Extole has two REST-style APIs. Our Admin API is for secure server-to-Extole interactions, while our Customer API is for direct end-user-to-Extole interactions.\n"
---

[//]: # "Does Extole use REST style APIs?"

## Overview

Extole has two REST-style APIs: Customer and Admin. The Customer API is our customer-to-Extole API, where your company's customers call the API directly. The Admin API is our server-to-Extole API for admin-level program management purposes. 

[//]: ___

## Extole Admin API

[//]: # "What is the Extole Admin API?"

Extole's Admin API is a collection of REST-style endpoints that provide you with the ability to send Extole program-related events. The Admin API can also be used to look at person information and manage your campaigns and rewards.

### Server-to-Server Authentication

 The Admin API authenticates server-to-server and uses the standard `Authorization: Bearer <token>` header for authentication.

### Key Management

Your keys are managed through My Extole in the [Security Center](https://my.extole.com/security-center).

[//]: ___

## Extole Customer API

[//]: # "What is the Extole Customer API?"

Extole's Customer API employs REST-style endpoints, which use an access token specific to a user to make all API calls. The REST API is designed to operate publicly on the internet between an end-user's browser and Extole—not behind a login or secure server-to-server connection—and there is no login call.

Customer API requests use the standard GET, PUT, POST, DELETE methods. All PUT/POST requests should include the header for `Content-Type: application/json` and `Accepts: application/json`.

[//]: ___

### How to Call the Customer API

[//]: # "How do I call the Extole Customer API?"

> ❗️ Update the URL
>
> Whenever you call the Extole Customer API, you must update the URL with your program domain.

For example, the URL for the Create Token endpoint is `<https://client.extole.io/api/v5/token`>. To successfully call this endpoint, replace `client` with your program domain. In other words, if Test Company were to call this endpoint, they would use the URL `<https://testcompany.extole.io/api/v5/token`>.

You can find your program domain in the [Tech Center](https://my.extole.com/tech-center) of My Extole.

> 🚧 Important Note
>
> Extole's JavaScript Library (`core.js`) is the most common way to create and utilize web experiences. Most of our clients never need to use the Customer API.

[//]: ___

### Access Tokens

[//]: # "What kind of access token do I need for the Extole Customer API?"

Access tokens are the primary method for identifying the user calling into the Customer API.

There are three main methods for passing access tokens:

* As a URL REST Parameter with the access token is passed as a URL parameter named access\_token
* In an Authorization header as Bearer TOKEN
* In a cookie named access\_token

Anytime the user makes a request, an access token is created and stored in a cookie. The token is a randomly generated number tied to a device profile (e.g., browser or mobile device). The initially granted access token is anonymous, meaning it is not tied to a program profile that contains PII.

Access tokens have three levels of security:

* **Anonymous**: This is a device token that creates a journey history of activity, but is not tied to an identified profile.
* **Identified**: A token becomes identified when either an email address or partner user id is passed through an API request. This allows the device token to get connected back to an identity profile inside the referral program. Identified tokens may add journey information into the identity profile, but they may not change information and they do not have access to any private profile data (name, friend information, reward information).
* **Verified**: A token may be verified through email verification or a backend server-to-server verification. A verified token is granted full access to the profile, including the ability to make updates to profile properties.

[//]: ___

### Polling Pattern

[//]: # "What is the polling pattern for the Extole Customer API?"

The Customer API will return all API requests in less than 100ms (typically faster). There is never a blocking operation at Extole. Any request with logic that may take longer than 100ms will instead return a polling ID, and there will be a related method to poll with the identifier to wait for the operation to complete.

[//]: ___

### Debugging

[//]: # "How do I debug the Extole Customer API?"

Extole allows the header X-Extole-Debug to set debug levels of the Extole calls between one and three.

[//]: ___
