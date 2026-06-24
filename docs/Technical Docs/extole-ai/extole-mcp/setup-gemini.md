---
title: Using the Extole MCP in Gemini Enterprise
excerpt: >-
  Connect Gemini CLI to Extole and manage your referral programs from the
  terminal.
---
Connect your Extole programs to Google's Gemini CLI and manage referrals from the terminal.

Gemini CLI is Google's open-source AI agent for the terminal. Once connected to the Extole MCP server, you can run performance reports, query program configuration, and make changes directly from any Gemini CLI session.

---

## Requirements

You'll need:

- [Gemini CLI](https://github.com/google-gemini/gemini-cli) installed
- An active Extole user account
- MCP access enabled for your Extole organization (contact your administrator if unsure)

---

## Setup

Choose your authentication method. See the [MCP authentication guide](doc:mcp-authentication) if you're not sure which to use.

---

### Option 1: OAuth (Recommended)

Gemini CLI supports automatic OAuth discovery — it detects that the server requires authentication and opens your browser to complete the flow.

**Using the CLI command:**

```bash
gemini mcp add --transport http extole https://mcp.extole.com
```

**Or manually**, add the following to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "Extole": {
      "httpUrl": "https://mcp.extole.com"
    }
  }
}
```

**Authorize the connection:**

Start a new Gemini CLI session and run `/mcp auth` to trigger the OAuth flow:

```
/mcp auth Extole
```

Your browser will open to an Extole authorization page. Review the permissions and click **Authorize**. Extole creates an access token linked to your user account, stored at `~/.gemini/mcp-oauth-tokens.json`.

**Verify:**

```
/mcp
```

The Extole server should show as `CONNECTED` with its available tools listed.

---

### Option 2: API Key

**Using the CLI command:**

```bash
gemini mcp add --transport http extole https://mcp.extole.com --header "Authorization: Bearer <YOUR_API_KEY>"
```

**Or manually**, add the following to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "Extole": {
      "httpUrl": "https://mcp.extole.com",
      "headers": {
        "Authorization": "Bearer <YOUR_API_KEY>"
      }
    }
  }
}
```

Replace `<YOUR_API_KEY>` with your Extole API key. To generate one, navigate to **My.Extole > Settings > API Tokens**.

To keep credentials out of your config file, reference an environment variable:

```json
{
  "mcpServers": {
    "Extole": {
      "httpUrl": "https://mcp.extole.com",
      "headers": {
        "Authorization": "Bearer ${EXTOLE_API_KEY}"
      }
    }
  }
}
```

Then set `EXTOLE_API_KEY` in your shell.

---

## Using the MCP

Once connected, Gemini CLI will automatically use Extole tools when your prompt requires them.

Enter a prompt such as:

> *"Show me the performance report for my refer-a-friend program for the past 30 days."*

> *"What's the current advocate reward in the holiday campaign?"*

> *"Update the friend coupon value in campaign X to 15% off."*

The first time Gemini uses an Extole tool, it will ask for confirmation. You can respond:

- **Proceed once** — approve this call only
- **Always allow this tool** — pre-approve this specific tool going forward
- **Always allow this server** — pre-approve all Extole tools

To pre-approve all Extole tools without prompts, add `"trust": true` to your config:

```json
{
  "mcpServers": {
    "Extole": {
      "httpUrl": "https://mcp.extole.com",
      "trust": true
    }
  }
}
```

> **Write operations** — Actions that modify programs, rewards, or campaign components execute immediately under your Extole permissions and are recorded in the Extole change log. Review tool calls carefully before approving write operations.

---

## Troubleshooting

**Server shows as DISCONNECTED** — Run `/mcp` to see the error. Verify your config JSON is valid and that `https://mcp.extole.com` is reachable from your machine.

**OAuth flow doesn't open a browser** — OAuth requires a local browser and redirect access to `http://localhost:7777/oauth/callback`. It won't work in headless or remote SSH environments without X11 forwarding. Use API key authentication instead.

**Tools not appearing after connecting** — Run `/mcp reload` to force re-discovery of tools from the server.

**Unauthorized errors with API key** — Confirm the `Bearer ` prefix is present before your token value, and that the key is active in My.Extole.