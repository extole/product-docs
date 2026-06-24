---
title: Using the Extole MCP in Gemini Enterprise
excerpt: >-
  Connect Gemini Enterprise to Extole and manage your referral programs with
  natural language.
---
Connect Extole to Gemini Enterprise so your organization's Gemini assistant can manage referral programs using natural language.

Gemini Enterprise supports custom MCP servers as data stores, letting you bring Extole directly into the Gemini assistant experience in the Google Cloud console. Once connected, users can run Extole performance reports, query program configuration, and manage rewards without leaving Gemini.

> Who this is for: This guide is for **Google Cloud administrators** with access to the Gemini Enterprise console. Setup is done once at the organization level and applies to all authorized users. Individual users do not need to configure anything.

---

## Requirements

Before you begin, you'll need:

- A **Gemini Enterprise** subscription (Standard, Plus, or Frontline edition)
- Access to the **Google Cloud console** with the **Discovery Engine Editor** role (`roles/discoveryengine.editor`) granted to your account
- The organization policy constraint for custom MCP data stores overridden
- **MCP access enabled** for your Extole organization
- Extole registered as an **OAuth client application** with your identity provider (Okta, Azure AD, Google, or similar)

---

## Step 1: Register with your identity provider

Before configuring Gemini Enterprise, register the integration as an OAuth client in your identity provider:

1. Set the **OAuth redirect URL** to:

```
https://vertexaisearch.cloud.google.com/oauth-redirect
```

2. Grant the necessary OAuth scopes. For Extole, use `read` for reports and queries, or `read write` for full access.

3. Note the **Client ID** and **Client Secret** for use in the next step.

Contact your Extole administrator if you need help with OAuth scope configuration.

---

## Step 2: Create the Extole MCP data store

1. In the Google Cloud console, navigate to **Gemini Enterprise**.

2. In the navigation menu, click **Data stores**, then click **Create data store**.

3. On the **Select a data source** page, search for **Custom MCP Server** and select the **Custom MCP Server (Preview)** card.

4. Click **Add MCP server**.

5. Fill in the **Authentication settings**:

| Field | Value |
|---|---|
| **MCP Server URL** | `https://mcp.extole.com` |
| **Authorization URL** | Contact your Extole administrator |
| **Token URL** | Contact your Extole administrator |
| **Client ID** | From your identity provider registration |
| **Client Secret** | From your identity provider registration |
| **Scopes** | `read` or `read write` |

6. Click **Login** and complete the sign-in flow.

7. Click **Continue**, then in the **MCP Server Description** field, enter:

```
Extole referral program data, reports, and management tools. Use these tools to retrieve program performance, query configurations, and manage rewards and campaigns.
```

8. Set the **Location** (Multi-region) and enter a **Data connector name** such as `Extole MCP`.

9. Click **Create**. Wait for the state to change to **Active** before proceeding.

---

## Step 3: Enable Extole tools

By default, all MCP tools are disabled after creation.

1. Open your new Extole MCP data store from the **Data stores** list.

2. Click **Actions > Reload custom actions**. Gemini Enterprise calls the Extole MCP server and lists available tools.

3. Select the tools you want to enable, then click **Enable actions**.

Enable read-only tools broadly and restrict write tools (such as reward or campaign updates) using role-based access controls.

---

## Step 4: Connect the data store to your app

1. In Gemini Enterprise, open your app (or create one if needed).

2. Navigate to **Data stores** in the app settings and click **Connect**.

3. Select the Extole MCP data store and save.

Once connected, the Gemini Enterprise assistant can use Extole tools in conversations.

---

## Using Extole in Gemini Enterprise

Once configured, users can ask the Gemini assistant questions that draw on Extole data and capabilities:

> *"Show me the performance summary for our refer-a-friend program this month."*

> *"What's the current advocate reward in the holiday campaign?"*

> *"Increase the friend reward in campaign X to $20."*

Gemini Enterprise will automatically call the appropriate Extole tool and return results in the conversation.

> **Write operations** Actions that modify programs, rewards, or campaign components execute immediately under the authenticated user's Extole permissions and are recorded in the Extole change log. Consider your organization's approval workflows before enabling write tools for broad user access.

---

## Data policies

Access to Extole MCP tools in Gemini Enterprise is governed by your Google Cloud IAM configuration and tool-level access controls in the Gemini Enterprise console. Admins can restrict which tools are available, limit access to specific user groups, and monitor usage through the Gemini Enterprise analytics dashboard.

The Extole MCP server uses the **Streamable HTTP** transport. Gemini Enterprise does not support the legacy Server-Sent Events (SSE) transport, so no additional transport configuration is needed.