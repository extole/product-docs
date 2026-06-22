---
title: Fiserv DNA
deprecated: false
hidden: true
metadata:
  robots: index
---
Deliver event files from Fiserv to Extole to automatically qualify and fulfill customer rewards.&#x20;

## Overview

Fiserv will provide a daily file containing members who have met the qualification criteria defined for the referral program.

The file should be:

Delivered daily<br />UTF-8 encoded CSV format<br />Include a header row<br />Sent to Extole's SFTP Events Processing directory<br />UTF-8 encoded CSV format<br />Include a header row

## Connecting to Extole's SFTP Server<br />

|                |                                                   |
| -------------- | ------------------------------------------------- |
| Host           | [sftp.extole.io](sftp.extole.io "sftp.extole.io") |
| Port           | 22                                                |
| Protocol       | SFTP                                              |
| Authentication | SSH Public Key                                    |
| Username       | Provided by Extole                                |

## SSH Key Setup

Fiserv should generate an SSH public/private key pair and provide the public key to Extole.

Extole will install the public key and provide confirmation when the account is ready for file transmission.

### File Delivery Schedule

|                       |         |
| --------------------- | ------- |
| Frequency             | Daily   |
| Delivery Method       | SFTP    |
| Destination Directory | /events |

## File Naming Convetion

<br />

Fiserv may use the following naming convention:

- \[ClientNum].\[MMDD].\[Seq].MEMBREFER\_\[YYYYMMDD]

Example:

- 1578.0507.10917.MEMBREFER\_20260507

## File Format

<br />

Files must be delivered as CSV with UTF-8 encoding.

A header row is required.

| Column          |   Required? | Description                              | Example              |
| --------------- | ----------: | ---------------------------------------- | -------------------- |
| `EVENT_NAME`    |         Yes | Event name Extole should create          | `account_qualified`  |
| `FIRST_NAME`    | Recommended | Member first name                        | `John`               |
| `LAST_NAME`     | Recommended | Member last name                         | `Jones`              |
| `EMAIL`         | Recommended | Member email address                     | `JJONES@EXAMPLE.COM` |
| `DNA_ACCOUNT`   | Recommended | Core account identifier                  | `300000000000`       |
| `OPEN_DATE`     | Recommended | Account open date in `YYYY-MM-DD` format | `2026-05-21`         |
| `BALANCE`       |    Optional | Account balance                          | `65000.00`           |
| `DESC-ABRV`     |    Optional | Product or description abbreviation      | `CD5`                |
| `BIRTH_DATE`    |    Optional | Birth date in `YYYYMMDD` format          | `19680720`           |
| `PERSON_NUMBER` | Recommended | Member or person identifier              | `1234`               |

Additional qualifiaction events can be sent as seperate files may be included as needed.

<br />

<br />

<br />
