---
title: Extole MCP Server
excerpt: >-
  Connect your AI tools to Extole and manage your referral programs using
  natural language.
deprecated: false
hidden: false
metadata:
  robots: index
---
Connect your AI tools to Extole and manage your referral programs using natural language.

The Extole MCP (Model Context Protocol) Server lets you use whatever AI tool you already work in — Claude, ChatGPT, Cursor, or any MCP-compatible client — to monitor and manage your Extole programs without logging into My.Extole.

## What you can do

Once connected, your AI client can:

- **Run reports** — pull performance data, participant history, reward status, and conversion reports
- **Query program configuration** — inspect program status, component structure, and campaign settings
- **Answer support questions** — investigate issues with rewards not received
- **Review change history** — retrieve audit logs and see what changed, when, and by whom

All actions execute under your own Extole permissions and are attributed to you in the Extole change log — whether the change was made through the UI, the API, or your AI tool.

## Authentication

The Extole MCP Server supports two authentication methods:

- **OAuth 2.0** — Recommended. Browser-based flow; no manual key management required. Uses authorization code with PKCE for secure, user-delegated access.
- **API key** — Manual setup for centralized key management or automated workflows.

See the [MCP authentication guide](doc:mcp-authentication) for details on choosing and configuring either method.

## Security and access control

- **User-scoped access** — All MCP requests execute as the authenticated user, subject to the same permissions as My.Extole.
- **Token scopes** — Tokens can be issued with explicit scopes: superuser, read/write, or read-only.
- **Change attribution** — Every action taken via MCP is recorded in the Extole change log with the originating user, tool, and timestamp.
- **Token revocation** — Users and admins can revoke MCP access at any time from My.Extole.

## MCP server URL

```
https://mcp.extole.com/toolsets/extole/mcp
```

## Get started

Follow the setup guide for your AI client:

| Client | Description |
|--------|-------------|
| [Claude Desktop](doc:setup-claude) | Desktop app version of Anthropic's Claude |
| [Claude Code](doc:setup-claude-code) | Command-line Claude for agentic workflows |
| [Cursor](doc:setup-cursor) | AI-powered code editor |
| [ChatGPT](doc:setup-chatgpt) | OpenAI's AI assistant |
| [Codex](doc:setup-codex) | OpenAI Codex CLI for automation and scripting |