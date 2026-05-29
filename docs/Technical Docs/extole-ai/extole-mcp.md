---
title: Extole MCP
deprecated: false
hidden: false
metadata:
  robots: index
---
he Extole MCP server implements the [Model Context Protocol](https://modelcontextprotocol.io/) (MCP), a standard that lets AI clients discover and invoke external tools. By connecting your AI client to Extole MCP, you can monitor and manage your Extole programs through natural language — without logging into My.Extole.

## What you can do

**Read operations**

- Run and retrieve performance, participant, reward, and conversion reports
- Query program status, configuration, and component structure
- Look up reward status and participant history
- Retrieve change logs and audit history

**Write operations**

- Modify reward values and program settings
- Create or update campaign components
- Trigger program actions (issue a reward, update a participant)

All write operations are executed under your own user permissions and logged with full attribution in the Extole change log — including the AI tool and user that initiated the action.

## How it works

Extole MCP is a remote MCP server using streamable HTTP transport. Your AI client connects to the server, discovers available tools, and invokes them on your behalf using your access token. No data leaves the secure Extole infrastructure.

**MCP server URL:** `https://mcp.extole.com/toolsets/extole/mcp`

## Authentication

Access requires an Extole client access token. Tokens are scoped to one of three permission levels:

| Scope      | Description                                               |
| ---------- | --------------------------------------------------------- |
| Read-only  | Can query reports, programs, participants, and history    |
| Read/Write | Can also modify program settings, rewards, and components |
| Superuser  | Full access, including administrative operations          |

Tokens are issued per user. Every action taken through MCP is attributed to the token's owner in the Extole change log.

To obtain a token, contact your Extole Customer Success Manager or account team.

## Supported clients

- [Claude (Anthropic)](setup-claude.md)
- [ChatGPT](setup-chatgpt.md)
- [Cursor](setup-cursor.md)
- [Codex (OpenAI)](setup-codex.md)
- Any MCP-compatible client

## Security

- All requests are executed under the authenticated user's permissions — the same access controls as My.Extole
- Write operations are rate-limited and logged with source attribution (user, tool, timestamp, and originating prompt where available)
- Tokens can be revoked at any time from My.Extole

<br />
