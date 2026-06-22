---
title: Fiserv DNA
deprecated: false
hidden: true
metadata:
  robots: index
---
## Connect to SFTP

<br />

## Prepare your file

Production files must be&#x20;

- CSV files encoded as UTF-8.
- File Naming Convention: \[ClientNum].\[MMDD].\[Seq].MEMBREFER\_\[YYYYMMDD]
- | Segment     | Meaning                          | Example     |
  | ----------- | -------------------------------- | ----------- |
  | `ClientNum` | Fiserv client number             | `1578`      |
  | `MMDD`      | Month and day of file generation | `0507`      |
  | `Seq`       | Sequence or batch number         | `10917`     |
  | `MEMBREFER` | Static file type label           | `MEMBREFER` |
  | `YYYYMMDD`  | Full file date                   | `20260507`  |

### Sample File

| Field          | Description                | Example              |
| -------------- | -------------------------- | -------------------- |
| EVENT\_NAME    | Extole event to create     | `account_opened`     |
| FIRST\_NAME    | Member first name          | `John`               |
| LAST\_NAME     | Member last name           | `Jones`              |
| EMAIL          | Member email address       | `JJONES@EXAMPLE.COM` |
| DNA\_ACCOUNT   | Core account identifier    | `300000000000`       |
| OPEN\_DATE     | Account open date          | `2026-05-21`         |
| BALANCE        | Current account balance    | `65000.00`           |
| DESC-ABRV      | Product abbreviation       | `CD5`                |
| BIRTH\_DATE    | Member birth date          | `19680720`           |
| PERSON\_NUMBER | Internal member identifier | `1234`               |

<br />