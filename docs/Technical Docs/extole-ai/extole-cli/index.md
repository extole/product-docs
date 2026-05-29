---
title: Extole CLI
excerpt: >-
  A command-line tool for interacting from the terminal and integrating into
  scripts and AI tools.
hidden: false
---
The Extole CLI is a command-line tool for developers who want to interact with Extole from the terminal, or integrate Extole operations into scripts and automation pipelines. It also includes a built-in MCP server so Claude Desktop and Claude Code can call any CLI command as a tool.

## Prerequisites

- Node.js 18 or later
- An Extole Access Token ([contact your CSM](https://www.extole.com/contact))

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

Manage multiple accounts:

```bash
extole auth list         # see all saved accounts
extole auth default acme # switch default
extole auth status       # verify token + connectivity
```

All commands use the default account unless you pass `--account NAME` or set `EXTOLE_ACCOUNT=NAME` in your shell.

## Commands

| Command                               | What it does                                           |
| ------------------------------------- | ------------------------------------------------------ |
| `extole programs`                     | List active programs                                   |
| `extole rewards --email <email>`      | Look up rewards for a person                           |
| `extole wismr --email <email>`        | Full reward-issuance diagnostic ("Where Is My Reward") |
| `extole reports run --type <name>`    | Run a report                                           |
| `extole events fire <name> --live`    | Fire an event and trace which campaigns it reached     |
| `extole person steps --email <email>` | View a person's step history                           |
| `extole audiences list`               | List audiences                                         |
| `extole webhooks`                     | List webhooks                                          |
| `extole stream --event-type INPUT`    | Tail live inbound events                               |
| `extole notifications`                | View platform notifications                            |
| `extole health`                       | Email and domain deliverability checks                 |
| `extole components`                   | Inspect campaign components                            |
| `extole api <path>`                   | Direct API access (escape hatch)                       |

Run `extole --help` or `extole <command> --help` for full options.

## Output conventions

- Human-readable by default; add `--json` on any command for machine-readable output
- `--compact` strips nulls and empty fields
- `--verbose` logs each HTTP request to stderr
- Data goes to stdout, status to stderr — fully pipeable

## AI integration

The CLI includes a built-in MCP server that connects Claude Desktop and Claude Code without manual config file editing:

```bash
extole serve setup   # auto-configure Claude Desktop and Claude Code
extole serve remove  # remove the registration
```

The CLI also exposes an AI assistant with deep knowledge of the Extole API:

```bash
extole auth mcp-login  # one-time browser login
extole mcp "why would a purchase event not trigger a reward?"
```

## Source

[github.com/cduskin-cpu/extole-cli](https://github.com/cduskin-cpu/extole-cli)
