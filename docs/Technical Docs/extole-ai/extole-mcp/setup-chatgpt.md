---
title: ChatGPT
excerpt: >-
  Connect ChatGPT to Extole and manage your referral programs with natural
  language.
hidden: false
---
Connect your Extole programs to ChatGPT and manage referrals with natural language.

ChatGPT supports MCP connections, letting you bring Extole directly into your ChatGPT conversations. Once connected, you can run reports, query program configuration, and make changes — without opening My.Extole.

---

## Requirements

Every person who wants to use the Extole MCP must complete setup individually.

You'll need:

- A ChatGPT plan that supports connectors (Pro, Plus, Team, Business, Enterprise, or Education)
- An active Extole user account

---

## Setup

Choose your authentication method. See the [MCP authentication guide](doc:mcp-authentication) if you're not sure which to use.

---

### Option 1: OAuth (Recommended)

**Step 1: Open connector settings**

In ChatGPT, navigate to **Settings > Apps & Connectors**.

**Step 2: Create a new connector**

Click **Create** next to **Advanced settings**.

**Step 3: Configure the connector**

- **Connector name** — `Extole`
- **Description** — `Manage Extole referral programs`
- **Server URL**:

```
https://mcp.extole.com
```

Click **Add**.

**Step 4: Authorize the connection**

ChatGPT will redirect you to an Extole authorization page. Review the permissions and click **Authorize**.

**Step 5: Verify the connection**

In a new chat, click the **+** icon and select the Extole connector to enable it.

---

### Option 2: Access Token

**Step 1: Get your access token**

Generate one at the [My.Extole Security Center](https://my.extole.com/security-center#access-token).

**Step 2: Open connector settings**

In ChatGPT, navigate to **Settings > Apps & Connectors** and click **Create** next to **Advanced settings**.

**Step 3: Configure the connector**

- **Connector name** — `Extole`
- **Description** — `Manage Extole referral programs`
- **Server URL**:

```
https://mcp.extole.com
```

- **Authentication**: Bearer token — enter your Extole access token

**Step 4: Verify the connection**

In a new chat, click the **+** icon and select the Extole connector.

---

## Using the MCP

Once the connector is enabled, interact with your Extole programs directly:

> *"Show me the performance summary for my refer-a-friend program this quarter."*

> *"What are the reward values currently set in my holiday campaign?"*

> *"Increase the friend reward in campaign X to $10."*

> **Write operations** — Actions that modify programs, rewards, or campaign components execute immediately under your Extole permissions and are recorded in the Extole change log.

---

## Troubleshooting

**Connector not showing** — Verify you're on a ChatGPT plan that supports connectors.

**"Unauthorized"** — Check that your access token is entered correctly, or re-authorize via OAuth.