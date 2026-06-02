---
title: Claude Code
excerpt: >-
  Connect Claude Code to Extole and manage your referral programs from the
  terminal.
hidden: false
---
Connect your Extole programs to Claude Code and manage referrals from the terminal.

Claude Code is the command-line version of Anthropic's Claude. Once connected to Extole, you can run reports, inspect program configuration, and make changes to your programs in any Claude Code session.

> Looking for Claude Desktop? If you prefer the desktop app, see the [Claude Desktop guide](doc:setup-claude) instead.

---

## Requirements

Every person who wants to use the Extole MCP must complete setup individually.

You'll need:

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- An active Extole user account

---

## Setup

Choose your authentication method. See the [MCP authentication guide](doc:mcp-authentication) if you're not sure which to use.

---

### Option 1: Extole CLI (Quickest)

If you have the [Extole CLI](doc:extole-cli) installed, one command configures Claude Code automatically:

```bash
extole serve setup
```

Start a new Claude Code session and you're ready. To remove the registration: `extole serve remove`.

---

### Option 2: OAuth via CLI

**Step 1: Add the Extole MCP server**

```bash
claude mcp add --transport http extole https://mcp.extole.com
```

**Step 2: Start a new Claude Code session**

```bash
claude
```

**Step 3: Authenticate with Extole**

1. Run `/mcp` to open the MCP servers list.
2. Navigate to the Extole entry and select it.
3. Press **Enter** to select **Authenticate**.
4. Your browser will open to an Extole authorization page.
5. Review the permissions and click **Authorize**.

**Step 4: Verify**

The Extole server should show as connected in the `/mcp` list.

---

### Option 3: Access Token

**Step 1: Get your access token**

Generate one at the [My.Extole Security Center](https://my.extole.com/security-center#access-token).

**Step 2: Edit your Claude Code MCP config**

Add the following to `.mcp.json` (project-level) or `~/.claude/mcp.json` (global):

```json
{
  "mcpServers": {
    "Extole": {
      "type": "http",
      "url": "https://mcp.extole.com",
      "headers": {
        "Authorization": "Bearer ${EXTOLE_ACCESS_TOKEN}"
      }
    }
  }
}
```

Set `EXTOLE_ACCESS_TOKEN` in your shell environment to keep credentials out of version control.

**Step 3: Start a new Claude Code session**

```bash
claude
```

The Extole MCP server will load automatically.

---

## Using the MCP

Once connected, interact with your Extole programs in any Claude Code session:

> *"Pull the conversion report for my refer-a-friend program for the past 30 days."*

> *"What's the current advocate reward in the holiday campaign?"*

> *"Update the friend coupon value in campaign X to 15% off."*

To pre-approve all Extole tools, start Claude Code with:

```bash
claude --allowed-tools 'mcp__extole__*'
```

> **Write operations** — Actions that modify programs, rewards, or campaign components execute immediately under your Extole permissions and are recorded in the Extole change log.