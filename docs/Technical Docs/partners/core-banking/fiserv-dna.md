---
title: Fiserv DNA
deprecated: false
hidden: true
metadata:
  robots: index
---
Deliver event files from Fiserv to Extole to automatically qualify and send customer rewards.&#x20;

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

### SSH Key Setup

Fiserv will generate an SSH public/private key pair and provide the public key to Extole.

Extole will configure the public key and provide confirmation when the account is ready for file transmission.

## File Setup

<br />

### File Naming

Fiserv may use the following naming convention:

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

Additional qualification events can be sent as seperate files.&#x20;

Files can include additional column headers to run referral qualification and reward rules.

> 📘 Files must be delivered as CSV with UTF-8 encoding. A header row is required.

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
