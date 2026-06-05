---
title: Extole CLI
excerpt: >-
  A command-line tool for interacting from the terminal and integrating into
  scripts and AI tools.
hidden: false
---
The Extole CLI is a command-line tool for developers who want to interact with Extole from the terminal or integrate Extole operations into scripts and automation pipelines. It also includes a built-in MCP server so Claude Desktop and Claude Code can call any CLI command as a tool.

## Prerequisites

- Node.js 18 or later
- An Extole Access Token ([https://my.extole.com/security-center](https://my.extole.com/security-center))

## Install

```bash
npm install -g github:cduskin-cpu/extole-cli
```

Verify:

```bash
extole --version
```

## Authenticate

Save your token (account name is auto-detected from the token):

```bash
extole auth login --token TOKEN
```

Save with an explicit account name:

```bash
extole auth login --token TOKEN --account acme --set-default
```

For scripts and CI, prefer environment variables over flags as tokens passed on the command line are visible in shell history:

```bash
export EXTOLE_TOKEN=your-token-here
export EXTOLE_ACCOUNT=acme
```

Manage multiple accounts:

```bash
extole auth list         # see all saved accounts
extole auth default acme # switch default
extole auth status       # verify token + connectivity
```

## Commands

| Domain                   | Commands                                              | What they do                                                                                                                                                                       |
| ------------------------ | ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Auth**                 | `extole auth *`, `extole ping`, `extole whoami`       | Manage credentials, switch between accounts, verify token validity and expiry                                                                                                      |
| **Events & People**      | `extole events fire`                                  | Fire events -- sandbox by default (safe), `--live` for production. Trace campaign routing with `--trace`                                                                           |
|                          | `extole events listen`                                | Tail live inbound events in real time with filters by type, person, or source                                                                                                      |
|                          | `extole events report <event_id>`                     | Look up a past event by ID                                                                                                                                                         |
|                          | `extole person get/steps/relationships/stats`         | Look up a person's profile, step history, referral graph, and network stats                                                                                                        |
|                          | `extole person rewards`                               | Rewards for a specific person                                                                                                                                                      |
|                          | `extole person report`                                | Full profile events report for a person                                                                                                                                            |
| **Rewards**              | `extole rewards`                                      | Look up rewards by person, get full details, history, fulfillments, sends, redeems, and cancels                                                                                    |
|                          | `extole rewards state-summary`                        | Account-wide reward counts by state, bucketed over time                                                                                                                            |
|                          | `extole rewards find-coupon`                          | Reverse-lookup: given a coupon code, find who received it and its current state                                                                                                    |
|                          | `extole wismr`                                        | Full reward-issuance diagnostic -- walks a person's rewards, shows state history, the rule that fired, the supplier that minted it, and a diagnosis with the most likely next step |
| **Reward Suppliers**     | `extole reward-suppliers`                             | List configured suppliers (Tango, PayPal, manual coupon batches, etc.) with face values                                                                                            |
|                          | `extole reward-suppliers get`                         | Full supplier detail, including limits, expiry, and tags                                                                                                                           |
|                          | `extole reward-suppliers coupons`                     | For manual-coupon suppliers: count, inventory preview, and depletion warnings                                                                                                      |
| **Components**           | `extole components`                                   | List, inspect, and traverse campaign components and their type hierarchy                                                                                                           |
|                          | `extole components create/set/deploy/delete`          | Create integration components, patch settings, deploy bundles, and delete components _(write)_                                                                                     |
| **Webhooks**             | `extole webhooks`                                     | List, inspect, create, attach, and delete webhooks                                                                                                                                 |
|                          | `extole webhooks dispatches/dispatch-results/listen`  | Inspect dispatch history, HTTP response outcomes, and tail live results in real time                                                                                               |
|                          | `extole webhooks trace`                               | Temporarily wire a URL to a campaign event and tail dispatch results                                                                                                               |
| **Campaigns & Programs** | `extole programs`                                     | List programs by state and type                                                                                                                                                    |
|                          | `extole campaigns quality-rules/reward-rules/maxmind` | Inspect quality rules, reward rules, and MaxMind fraud-scoring settings per campaign                                                                                               |
| **Audiences**            | `extole audiences list/get/members`                   | List audiences, view size, and page through members                                                                                                                                |
|                          | `extole audiences history`                            | View recent add/remove/replace/sync runs; tail with `--listen`                                                                                                                     |
| **Reports**              | `extole reports recommended/types/describe`           | Discover available reports and inspect their parameters before running                                                                                                             |
|                          | `extole reports run/status/download`                  | Run a report, check completion, and stream results to stdout                                                                                                                       |
| **Notifications**        | `extole notifications`                                | View recent platform alerts (webhook failures, integration errors); tail with `--listen`                                                                                           |
| **Health**               | `extole health`                                       | Email domain deliverability checks (SPF, DMARC, DKIM, MX) and program domain resolution                                                                                            |
|                          | `extole health provision-dkim`                        | Provision DKIM keys for an email domain via SendGrid _(write)_                                                                                                                     |
| **Share Links**          | `extole share-links list`                             | List share links for a person                                                                                                                                                      |
|                          | `extole share-links lookup`                           | Reverse-lookup: given a share code or URL, find the owning person and program                                                                                                      |
| **Zones**                | `extole zones`                                        | List embed zone names, get the core.js script tag, and retrieve embed snippets                                                                                                     |
|                          | `extole zones call`                                   | POST to a zone to test FRONTEND\_CONTROLLER pipelines without a browser                                                                                                            |
| **API**                  | `extole api <path>`                                   | Authenticated access to any Extole endpoint -- GET by default, supports `--method`, `--body`                                                                                       |

Run `extole --help` or `extole <command> --help` for full options on any command.

## Output conventions

- Human-readable by default; add `--json` on any command for machine-readable output
- `--compact` strips nulls and empty fields
- `--verbose` logs each HTTP request to stderr
- Data goes to stdout, status to stderr -- fully pipeable

## AI integration

The CLI includes a built-in MCP server that connects Claude Desktop and Claude Code without manual config file editing:

```bash
extole serve setup   # auto-configure Claude Desktop and Claude Code
extole serve remove  # remove the registration
```

The CLI also exposes an AI assistant with deep knowledge of the Extole API. Uses your stored Extole token -- no separate login required:

```bash
extole chat "why would a purchase event not trigger a reward?"
extole chat "what endpoint filters person steps by cause event id?"
```

## Source

[github.com/cduskin-cpu/extole-cli](https://github.com/cduskin-cpu/extole-cli)
