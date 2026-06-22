---
title: Fiserv DNA
deprecated: false
hidden: true
metadata:
  robots: index
---
Deliver event files from Fiserv to Extole to automatically qualify referral participants and issue customer rewards.

## Overview

Fiserv securely transfers daily event files to Extole via SFTP. These files contain records of members who have successfully met the qualification criteria defined for your specific referral program.

## Connecting to Extole's SFTP Server

Use the following configuration when setting up Extole in Fiserv's SFTP program. More about Extole's SFTP: [https://docs.extole.com/docs/extoles-sftp-server](https://docs.extole.com/docs/extoles-sftp-server "https://docs.extole.com/docs/extoles-sftp-server")&#x20;

|                |                                                   |
| -------------- | ------------------------------------------------- |
| Host           | [sftp.extole.io](sftp.extole.io "sftp.extole.io") |
| Port           | 22                                                |
| Protocol       | SFTP                                              |
| Authentication | SSH Public Key                                    |
| Username       | Provided by Extole                                |

### SSH Key Setup

&#x20;Fiserv will generate a standard SSH public/private key pair and provide the public key to Extole. Extole will then add this public key directly into the Extole platform

## File Specifications<br />

### File Naming

Files can follow the standard Fiserv naming convention:

- \[ClientNum].\[MMDD].\[Seq].MEMBREFER\_\[YYYYMMDD]

Example:

- 1578.0507.10917.MEMBREFER\_20260507

### File Delivery&#x20;

|                       |         |
| --------------------- | ------- |
| Frequency             | Daily   |
| Delivery Method       | SFTP    |
| Destination Directory | /events |

### File Format

Qualification events can be sent as separate files. For example, you can deliver files for milestones like `account_opened`, `qualifying_account_balance_reached`, `loan_funded`, or `credit_card_activated`.<br /><br />Files can include additional column headers to run run certain reward rules, such as product type, deposit amounts, etc.&#x20;

> 📘 Files must be delivered as standard CSVs with UTF-8 encoding. A header row similar to the columns below is required.

#### Sample Account Opened File

| Column          |   Required? | Description                              | Example              |
| --------------- | ----------: | ---------------------------------------- | -------------------- |
| `EVENT_NAME`    |         Yes | Event name Extole should create          | `account_opened`     |
| `FIRST_NAME`    | Recommended | Member first name                        | `John`               |
| `LAST_NAME`     | Recommended | Member last name                         | `Jones`              |
| `EMAIL`         | Recommended | Member email address                     | `JJONES@EXAMPLE.COM` |
| `DNA_ACCOUNT`   | Recommended | Core account identifier                  | `300000000000`       |
| `OPEN_DATE`     | Recommended | Account open date in `YYYY-MM-DD` format | `2026-05-21`         |
| `BALANCE`       |    Optional | Account balance                          | `250.00`             |
| `DESC-ABRV`     |    Optional | Product or description abbreviation      | `CD5`                |
| `PERSON_NUMBER` | Recommended | Member or person identifier              | `1234`               |

<br />

<br />

<br />

<br />
