---
title: Microsoft Copilot
excerpt: Connect Extole to Microsoft 365 Copilot Chat or Copilot Studio
---
Connect Extole to Microsoft's AI platforms so your teams can manage referral programs using natural language — either directly in Microsoft 365 Copilot Chat or as part of a custom Copilot Studio agent.

There are two integration paths depending on your use case:

- **Microsoft 365 Copilot Chat** — Admins configure a federated connector in the M365 Admin Center. Extole data becomes available as a real-time source in Copilot Chat across your organization. Best for teams who want reporting and query access inside Copilot without building a custom agent.
- **Copilot Studio** — Agent builders connect Extole MCP tools to a custom agent. Best for teams building purpose-built Copilot experiences that can also write back to Extole (update rewards, modify programs, etc.).

---

## Microsoft 365 Copilot Chat

Microsoft 365 Copilot supports **federated connectors** — real-time data connections configured by admins in the M365 Admin Center. Once connected, Extole data is available as a source in Copilot Chat for all authorized users. No per-user setup required.

> **Note:** Federated connectors currently support **read-only** tools (search, fetch, query). Use Copilot Studio if you need write access to Extole programs.

> **Who this is for:** This section is for **Microsoft 365 Global Administrators or AI Administrators**. Individual users do not need to configure anything.

### Requirements

- A Microsoft 365 Copilot license
- Global Administrator or AI Administrator role in the M365 Admin Center
- MCP access enabled for your Extole organization (contact your Extole administrator if unsure)

### Step 1: Register Extole's OAuth app in the Teams Developer Portal

Before creating the connector, register Extole's MCP server as an OAuth client in the Teams Developer Portal.

1. Sign in to the [Teams Developer Portal](https://dev.teams.microsoft.com/).
2. Select **Tools > OAuth Client Registration**.
3. Select **+ New OAuth connection**.
4. Fill in the following fields:

| Field | Value |
|---|---|
| **Name** | `Extole` |
| **Client ID** | Contact your Extole administrator |
| **Client secret** | Contact your Extole administrator |
| **Authorization endpoint** | Contact your Extole administrator |
| **Token endpoint** | Contact your Extole administrator |
| **Refresh endpoint** | Contact your Extole administrator |
| **Scopes** | `read` |

5. If your OAuth provider supports it, enable **Proof Key for Code Exchange (PKCE)**.
6. Select **Save**.

After saving, copy the **OAuth client registration ID** — you'll need it in the next step.

> **OAuth redirect URI:** If your OAuth provider requires a redirect URI during app registration, use: `https://teams.microsoft.com/api/platform/v1.0/oAuthRedirect`

### Step 2: Create the connector in the M365 Admin Center

1. Sign in to the [Microsoft 365 Admin Center](https://admin.microsoft.com/).
2. In the left pane, select **Copilot > Connectors**.
3. Select the **Gallery** tab.
4. Under **Created by your org**, find the **Create a new connector** tile and select **Add**.
5. On the **Custom connector** page, under **Connect to MCP server**, select **Add**.
6. Fill in the connector details:

| Field | Value |
|---|---|
| **Display name** | `Extole` |
| **Base URL** | `https://mcp.extole.com` |
| **OAuth registration ID** | From the Teams Developer Portal (Step 1) |

7. Select **Save**.

### Step 3: Roll out to users

After creation, the connector appears in the **Your Connections** list. To deploy it:

1. Select the Extole connector.
2. Select **Staged rollout** to test with specific users or groups first, or select **Deploy to all users** to release tenant-wide.

Changes can take up to 15 minutes to take effect.

### Using Extole in Copilot Chat

Once deployed, users can ask Copilot questions that draw on Extole data:

> *"Show me the performance summary for our refer-a-friend program this month."*

> *"What's the current advocate reward in the holiday campaign?"*

> *"How many successful referrals did we get last quarter?"*

Copilot queries the Extole MCP server in real time and returns results in the conversation.

---

## Copilot Studio

Microsoft Copilot Studio lets you build custom agents for your organization. By connecting an agent to the Extole MCP server, you can give that agent the ability to run Extole reports, query program configuration, and manage rewards — including write operations such as updating rewards or campaign components.

> **Who this is for:** This section is for teams building Copilot Studio agents. If you want Extole available in Copilot Chat without building a custom agent, use the Federated Connector path above.

### Requirements

- Access to [Microsoft Copilot Studio](https://copilotstudio.microsoft.com/)
- **Generative orchestration** enabled on your agent. In Copilot Studio, open your agent's settings and enable **Generative (preview)** under **Orchestration**.
- An active Extole user account with appropriate permissions
- MCP access enabled for your Extole organization (contact your Extole administrator if unsure)

### Setup

Copilot Studio supports two setup paths: the MCP onboarding wizard (recommended) and a custom Power Apps connector.

---

#### Option 1: MCP onboarding wizard (Recommended)

**Step 1: Open your agent's Tools page**

In Copilot Studio, navigate to your agent and select the **Tools** tab.

**Step 2: Add a new tool**

Click **Add a tool**, then **New tool**, then select **Model Context Protocol**. The MCP onboarding wizard opens.

**Step 3: Configure the server**

Fill in the following fields:

- **Server name** — `Extole`
- **Server description** — `Access Extole referral program data, reports, and management tools`
- **Server URL**: `https://mcp.extole.com`

**Step 4: Configure authentication**

Select **OAuth 2.0**, then select **Dynamic discovery** as the type. Copilot Studio will automatically discover the Extole OAuth endpoints and register itself. Click **Create**.

A callback URL will appear — copy it. You'll need to register it with Extole's OAuth configuration. Contact your Extole administrator to complete this step.

**Step 5: Add the server to your agent**

On the **Add tool** dialog, select **Create a new connection** and click **Add to agent**. Copilot Studio connects to the Extole MCP server and makes all available tools discoverable by your agent.

---

#### Option 2: Custom Power Apps connector

Use this path if your organization requires a custom connector registered in Power Apps, or if you need to apply data loss prevention (DLP) policies.

In Copilot Studio, navigate to your agent and select **Tools > Add a tool > New tool > Custom connector**. In Power Apps, select **New custom connector > Import OpenAPI file** and import the following schema as `extole-mcp.yaml`:

```yaml
swagger: '2.0'
info:
  title: Extole MCP
  description: Access Extole referral program tools via MCP
  version: 1.0.0
host: mcp.extole.com
basePath: /
schemes:
  - https
paths:
  /mcp:
    post:
      summary: Extole MCP Server
      x-ms-agentic-protocol: mcp-streamable-1.0
      operationId: InvokeMCP
      responses:
        '200':
          description: Success
```

Follow the Power Apps prompts to configure OAuth 2.0 authentication and finish creating the connector. Then return to Copilot Studio and add it as a tool to your agent.

---

### Using the MCP in your agent

Once connected, the Extole MCP tools are automatically available for your agent to use.

> *"Show me the performance summary for our refer-a-friend program."*

> *"What's the current reward for advocates in the summer campaign?"*

> *"Increase the friend reward in campaign X to $15."*

> **Write operations:** Actions that modify programs, rewards, or campaign components execute immediately under the authenticated user's Extole permissions and are recorded in the Extole change log. Ensure your agent's prompt instructions make clear when write operations will occur so users can confirm before proceeding.

---

## Data policies

**Copilot Chat (Federated Connectors):** Access is governed by the M365 Admin Center connector settings. Admins control which users or groups can access the Extole connector and can disable it at any time.

**Copilot Studio:** Access is governed by Power Platform connectors. If your organization has data loss prevention (DLP) policies applied to Power Platform, those policies also apply to Extole MCP tool calls. Contact your Power Platform administrator if you need to allowlist the Extole connector.