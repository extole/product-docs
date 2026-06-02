---
title: Cursor
excerpt: >-
  Connect Cursor to Extole and manage your referral programs alongside your
  code.
hidden: false
---
Connect your Extole programs to Cursor and manage referrals alongside your code.

Cursor is an AI-powered code editor. Once connected to Extole, you can pull program data, check reward configurations, and make changes from Cursor's AI chat — useful when building integrations or automations on top of Extole.

---

## Requirements

Every person who wants to use the Extole MCP must complete setup individually.

You'll need:

- [Cursor](https://cursor.sh/) 0.43 or later
- An active Extole user account

---

## Setup

Choose your authentication method. See the [MCP authentication guide](doc:mcp-authentication) if you're not sure which to use.

---

### Option 1: OAuth (Recommended)

**Step 1: Open MCP settings**

In Cursor, go to **Cursor > Settings > Cursor Settings**, then click **Tools & Integrations**.

**Step 2: Add a new MCP server**

Click **New MCP Server** under **MCP Tools**.

**Step 3: Configure the server**

Paste the following into `mcp.json`:

```json
{
  "mcpServers": {
    "Extole": {
      "url": "https://mcp.extole.com"
    }
  }
}
```

Save the file.

**Step 4: Authorize the connection**

Click **Connect** next to the Extole MCP entry. Your browser will open to an Extole authorization page. Review the permissions and click **Authorize**.

**Step 5: Verify**

The Extole MCP server should appear as connected in **Tools & Integrations**.

---

### Option 2: Access Token

**Step 1: Get your access token**

Generate one at the [My.Extole Security Center](https://my.extole.com/security-center#access-token).

**Step 2: Open MCP settings**

In Cursor, go to **Cursor > Settings > Cursor Settings**, then click **Tools & Integrations** and click **New MCP Server**.

**Step 3: Configure the server**

Paste the following into `mcp.json`:

```json
{
  "mcpServers": {
    "Extole": {
      "url": "https://mcp.extole.com",
      "headers": {
        "Authorization": "Bearer <YOUR_ACCESS_TOKEN>"
      }
    }
  }
}
```

Replace `<YOUR_ACCESS_TOKEN>` with your Extole access token. Save the file.

**Step 4: Verify**

Check the server status in **Tools & Integrations**. It should show as connected.

---

## Using the MCP

Open the AI chat panel and select **Agent** mode, then enter a prompt:

> *"What's the current conversion rate on our refer-a-friend program?"*

> *"Show me the reward configuration for the friend offer in campaign X."*

> *"Update the advocate reward in the spring campaign to $25."*

Cursor will prompt you to approve each MCP tool call. Click **Run tool** to proceed. You can enable [Yolo mode](https://docs.cursor.com/chat/agent#yolo-mode) to auto-approve tool calls — useful in trusted workflows, but review carefully before enabling for write operations.

> **Write operations** — Actions that modify programs, rewards, or campaign components execute immediately under your Extole permissions and are recorded in the Extole change log.

---

## Troubleshooting

**Tools not appearing** — Restart Cursor after saving `mcp.json`. Verify the JSON is valid.

**"Unauthorized"** — Confirm the `Bearer ` prefix is present before your token, or re-authorize via OAuth.