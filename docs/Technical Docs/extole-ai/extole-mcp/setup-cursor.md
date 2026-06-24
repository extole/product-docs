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

- A version of [Cursor](https://cursor.sh/) that supports MCP (0.43+)
- An active Extole user account
- MCP access enabled for your Extole organization (contact your administrator if unsure)

---

## Setup

**Step 1: Open MCP settings**

In Cursor, go to **Cursor > Settings > Cursor Settings**, then click **Tools & Integrations** in the left nav.

**Step 2: Add a new MCP server**

Click **New MCP Server** under **MCP Tools**.

**Step 3: Configure the server**

Cursor will create an `mcp.json` file. Paste the following:

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

1. Click **Connect** next to the Extole MCP entry.
2. Your browser will open to an Extole authorization page.
3. Review the permissions and click **Authorize**.

Extole will create an access token linked to your user account.

**Step 5: Verify the connection**

The Extole MCP server should appear as connected in **Tools & Integrations**.

---

## Using the MCP

Once connected, use Extole tools from Cursor's AI chat panel.

**Step 1:** Open the AI chat panel and select **Agent** mode.

**Step 2:** Enter a prompt, such as:

> *"What's the current conversion rate on our refer-a-friend program?"*

> *"Show me the reward configuration for the friend offer in campaign X."*

> *"Update the advocate reward in the spring campaign to $25."*

**Step 3:** Cursor will prompt you to approve each MCP tool call. Click **Run tool** to proceed.

You can enable [Yolo mode](https://docs.cursor.com/chat/agent#yolo-mode) in Cursor to auto-approve tool calls without prompts — useful in trusted workflows, but review carefully before enabling for write operations.

> 🚧 Write operations
> Actions that modify programs, rewards, or campaign components execute immediately under your Extole permissions and are recorded in the Extole change log.