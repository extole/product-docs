---
title: "File-based Events"
excerpt: "Understand when to send event files to Extole, our file naming conventions, and more.\n"
---

## Overview

Extole supports regular file uploads to receive events that may have happened offline or are otherwise unable to be tracked through tags or API.

[//]: ___

## Example Events for Different Programs

[//]: # "What are examples of Extole events?"

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>
        ONLINE RETAIL
      </th>

      <th>
        PAID SUBSCRIPTION
      </th>

      <th>
        BANKING
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `purchased`
        `shipped`
        `canceled`
        `returned`
      </td>

      <td>
        `registered`\
        `subscribed`\
        `paid`\
        `canceled`
      </td>

      <td>
        `application_started`\
        `applied`\
        `opened`\
        `funded`\
        `transacted`\
        `closed`
      </td>
    </tr>
  </tbody>
</Table>

[//]: ___

## File Naming Conventions

[//]: # "What are Extole's file formatting standards and file naming conventions?"

The file should be uploaded to the Extole SFTP system at: `clientname@sftp.extole.io:/events`.

For details on using SFTP and the Extole SFTP Server, check out our article on [Using Extole's SFTP Server](https://docs.extole.com/docs/extoles-sftp-server).

You can also access the interface in My Extole to view file processing in the [Tech Center](https://my.extole.com/tech-center). This interface will allow you to upload, download, and view files and subscribe to failure alerts. 

## Event File Records

<Table align={["left","left","left"]}>
  <thead>
    <tr>
      <th>
        Column Name
      </th>

      <th>
        Required
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `event_name`
      </td>

      <td>
        Yes
      </td>

      <td>
        The type of event to create such as:\
        `purchased`\
        `shipped`\
        `opened`\
        `canceled`
      </td>
    </tr>

    <tr>
      <td>
        `email`
      </td>

      <td>
        Yes
      </td>

      <td>
        The email of the person who did the event (e.g. the email of the person who made the purchase, opened the account, etc.).
      </td>
    </tr>

    <tr>
      <td>
        `first_name`
      </td>

      <td>
        No
      </td>

      <td>
        The first name of the person who did the event.
      </td>
    </tr>

    <tr>
      <td>
        `last_name`
      </td>

      <td>
        No
      </td>

      <td>
        The last name of the person who did the event.
      </td>
    </tr>

    <tr>
      <td>
        `coupon_code`
      </td>

      <td>
        No
      </td>

      <td>
        The unique one-time use coupon code used in the event (e.g. in the purchase). This coupon code must have been issued as part of the Extole incentive.
      </td>
    </tr>

    <tr>
      <td>
        `event_time`
      </td>

      <td>
        No
      </td>

      <td>
        The date and time of the event as [ISO\_8601 format](https://www.w3.org/TR/NOTE-datetime). Generally this is`YYYY-MM-DDThh:mm:ssZ` (e.g. `2013-08-11T14:33:18-0700`). If not provided, Extole will use the processing time of the event file as the event time.
      </td>
    </tr>

    <tr>
      <td>
        `partner_event_id`\
        (renameable)
      </td>

      <td>
        No
      </td>

      <td>
        This is your unique identifier for the event. This could be an order number, confirmation number, or other unique identifier. Passing this is strongly recommended to make sure duplicate transactions are never created.
      </td>
    </tr>

    <tr>
      <td>
        `partner_user_id`\
        (renameable)
      </td>

      <td>
        No
      </td>

      <td>
        This is your unique identifier for the person who did the event. This is useful for ensuring that the event is tied to the proper user.
      </td>
    </tr>

    <tr>
      <td>
        `cart_value`
      </td>

      <td>
        No
      </td>

      <td>
        Revenue value of the transaction before coupons are applied, used for reporting.
      </td>
    </tr>

    <tr>
      <td>
        `container`
      </td>

      <td>
        No
      </td>

      <td>
        The container where the events should appear. Use `production` if you want the events to appear in your analytics, or `test`, which causes Extole to not summarize the data in the program and campaign summary analytics
      </td>
    </tr>
  </tbody>
</Table>

> 📘 Advocate Recognition
>
> You should provide all transactions to Extole and the transactions will be run through the Extole advocate recognition process to find referrals based on coupon code, friend email address, partner user ID, partner conversion ID.

> 📘 Configurable and Renameable Fields
>
> There are no "standard events" with Extole, only your specified business events. In other words, it's possible to send any event to Extole.
>
> All of the names of data elements for events can be renamed and additional data fields can be passed to be used for targeting, personalization, quality, and reward rules.

## Input File Example

Filename: `/events/events_20130619000000.csv`

```text Account Opened
event_name,email,member_id,event_time
account_opened,xy6492@akerd.com,AAA123,2013-06-19T10:12:53-0700
account_opened,ex2544@akerd.com,AAA124,2013-06-19T11:42:51-0700
account_opened,dx0129@akerd.com,AAA125,2013-06-19T12:16:12-0700
```
```text Account Qualified
event_name,email,member_id,event_time,value
account_qualified,xy6492@akerd.com,AAA123,2013-06-19T10:12:53-0700,25.23
account_qualified,ex2544@akerd.com,AAA124,2013-06-19T11:42:51-0700,21.00
account_qualified,dx0129@akerd.com,AAA125,2013-06-19T12:16:12-0700,722.00
```
```text Purchases
event_name,email,coupon_code,event_time,order_id,cart_value
purchase,xy6492@akerd.com,AAA123,2013-06-19T10:12:53-0700,00540000001PULM,20.34
purchase,ex2544@akerd.com,AAA124,2013-06-19T11:42:51-0700,00540000001O1fi,100.28
purchase,dx0129@akerd.com,AAA125,2013-06-19T12:16:12-0700,0064000000QP7SN,99.99
```

For additional details on file requirements, see our docs: [File Conventions](https://docs.extole.com/docs/extoles-sftp-server#file-conventions)

[//]: ___

## Credit Union Earned Rewards File Example

Credit unions will receive an earned rewards file from Extole via SFTP to verify members who should earn rewards. Once reviewed, credit unions can then send Extole a fulfilled file via SFTP so that we can transition the members' rewards to fulfilled.

* creditunion@sftp.extole.com:/dropbox
* rewards-report-YYYY-MM-DDTHHMMSS.csv

A sample file could look like this:

<Image align="center" src="https://files.readme.io/33f6842ece8e36bfac20230ed6e77ee5db0cd1a4847968d7204e63b71c1fc5cd-cu-rewards-screenshot.png" />

```Text Earned Rewards
Reward ID,Earned Date,Program,Email,First Name,Last Name,Account Number,Face Value,Face Value Type,Reward Name,Reward Supplier Id
a9d3d69dee0cf8e6117231d3,2024-07-16T13:41:28.823-07:00,refer-a-friend,jjones@mail.com,John,Jones,545413,50,USD,$50 Friend Account Credit Reward,ca48186930a57de0f951a7d6
```

<br />
