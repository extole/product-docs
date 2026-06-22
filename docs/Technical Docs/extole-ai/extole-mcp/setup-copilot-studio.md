---
title: Microsoft Copilot Studio
excerpt: >-
  Connect Microsoft Copilot Studio agents to Extole and manage referral programs
  through Microsoft's AI platform.
---
Connect Extole to a Copilot Studio agent and manage referral programs through Microsoft's AI platform.

Microsoft Copilot Studio lets you build custom agents for your organization. By connecting an agent to the Extole MCP server, you can give that agent the ability to run Extole reports, query program configuration, and manage rewards — surfacing Extole capabilities inside any experience you build in Copilot Studio.

> 📘 Who this is for
>
> This guide is for teams building Copilot Studio agents, not for end users. If you're looking to connect a personal AI tool, see the guides for [Claude Desktop](doc:setup-claude), [Cursor](doc:setup-cursor), or [ChatGPT](doc:setup-chatgpt).

***

## Requirements

To follow this guide you'll need:

- Access to [Microsoft Copilot Studio](https://copilotstudio.microsoft.com/)
- **Generative orchestration** enabled on your agent. In Copilot Studio, open your agent's settings and enable **Generative (preview)** under **Orchestration**.
- An active Extole user account with appropriate permissions
- MCP access enabled for your Extole organization (contact your Extole administrator if unsure)

***

## Setup

Copilot Studio supports two setup paths: the MCP onboarding wizard (recommended) and a custom Power Apps connector. The wizard is sufficient for most teams.

***

### Option 1: MCP onboarding wizard (Recommended)

**Step 1: Open your agent's Tools page**

In Copilot Studio, navigate to your agent and select the **Tools** tab.

**Step 2: Add a new tool**

Click **Add a tool**, then **New tool**, then select **Model Context Protocol**. The MCP onboarding wizard opens.

**Step 3: Configure the server**

Fill in the following fields:

- **Server name** — `Extole`
- **Server description** — `Access Extole referral program data, reports, and management tools`
- **Server URL**:

```
https://mcp.extole.com
```

**Step 4: Configure authentication**

Choose your authentication method:

***

**OAuth 2.0 (Recommended)**

Select **OAuth 2.0**, then select **Dynamic discovery** as the type. Copilot Studio will automatically discover the Extole OAuth endpoints and register itself. Click **Create**.

A callback URL will appear — copy it. You'll need to register it with Extole's OAuth configuration. Contact your Extole administrator to complete this step.

***

**API key**

Select **API key** as the authentication type.

- **Type** — `Header`
- **Header name** — `Authorization`

Click **Create**. When prompted to create a connection, enter your Extole API key in the format `Bearer <YOUR_API_KEY>`.

To generate an API key, navigate to **My.Extole > Settings > API Tokens**.

***

**Step 5: Add the server to your agent**

On the **Add tool** dialog, select **Create a new connection** (or pick an existing one) and click **Add to agent**.

Copilot Studio will connect to the Extole MCP server and make all available tools discoverable by your agent.

***

### Option 2: Custom Power Apps connector

Use this path if your organization requires a custom connector registered in Power Apps, or if you need to apply data loss prevention (DLP) policies.

**Step 1: Open your agent's Tools page**

In Copilot Studio, navigate to your agent and select **Tools > Add a tool > New tool > Custom connector**. You'll be taken to Power Apps.

**Step 2: Create a new custom connector**

In Power Apps, select **New custom connector > Import OpenAPI file**.

**Step 3: Import the Extole MCP schema**

Create a file named `extole-mcp.yaml` with the following content and import it:

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

**Step 4: Complete setup in Power Apps**

Follow the Power Apps prompts to configure authentication (API key or OAuth 2.0) and finish creating the connector. Then return to Copilot Studio and add it as a tool to your agent.

***

## Using the MCP in your agent

Once connected, the Extole MCP tools are automatically available for your agent to use. Your agent will call them when a user's message requires Extole data or an action.

Example prompts your agent can handle:

> _"Show me the performance summary for our refer-a-friend program."_

> _"What's the current reward for advocates in the summer campaign?"_

Copilot Studio dynamically reflects any changes you make to the Extole MCP server — new tools or resources appear automatically without reconfiguring the agent.

> **Write operations** — Actions that modify programs, rewards, or campaign components execute immediately under the authenticated user's Extole permissions and are recorded in the Extole change log. Ensure your agent's prompt instructions make clear when write operations will occur so users can confirm before proceeding.

***

## Data policies

Access to the Extole MCP server in Copilot Studio is governed by Power Platform connectors. If your organization has data loss prevention (DLP) policies applied to Power Platform, those policies also apply to Extole MCP tool calls. Contact your Power Platform administrator if you need to allowlist the Extole connector.
