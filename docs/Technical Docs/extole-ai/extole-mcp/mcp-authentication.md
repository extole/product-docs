---
title: MCP Authentication
excerpt: Choose between OAuth and API key authentication for Extole MCP clients.
hidden: false
---
Choose how to authenticate MCP clients with Extole: OAuth for streamlined setup or API keys for manual control.

The Extole MCP Server supports two authentication methods:

|  | OAuth 2.0 | API key |
|--|-----------|---------|
| Best for | Individual users who want quick, secure setup | Admins managing keys centrally, or automated workflows |
| Setup complexity | Low — browser-based flow | Medium — manual configuration |
| Key management | Automatic | Manual |
| Permissions | Uses your Extole permissions | Uses the key creator's permissions |

## OAuth 2.0 authentication

OAuth lets MCP clients connect to Extole without requiring you to manually create and manage API keys. When you connect, Extole creates an access token on your behalf and links it to your user account.

The flow uses OAuth 2.1 with PKCE (Proof Key for Code Exchange) for secure, user-delegated access.

### Requirements

- You must have an active Extole user account with appropriate permissions.

### How it works

1. Add the MCP server URL to your AI client.
2. The client triggers the OAuth flow.
3. Your browser opens to an Extole authorization page.
4. Review the requested permissions and click **Authorize**.
5. Extole creates an access token scoped to your user account and links it to the MCP client.

After authorization, all MCP requests use your Extole permissions and access controls.

### MCP server URL

```
https://mcp.extole.com/toolsets/extole/mcp
```

### Token scopes

- **Read-only** — can run reports and query program state; cannot make changes
- **Read/write** — can read and modify programs, rewards, and campaign components
- **Superuser** — full access, equivalent to an Extole administrator

### Revoking access

To revoke access, navigate to **My.Extole > Settings > API Tokens** and delete the token associated with the client.

---

## API key authentication

Use this method when:

- You need to manage keys centrally across your organization
- You're setting up automated workflows or CI/CD pipelines
- You want to use a service account rather than individual user credentials
- Your MCP client doesn't support OAuth

### How it works

1. Generate an API key in My.Extole under **Settings > API Tokens**.
2. Configure the key in your MCP client's settings.
3. The client includes the key as a Bearer token in all requests to Extole.

### Configuration

```
https://mcp.extole.com/toolsets/extole/mcp
```

Pass the key as an `Authorization: Bearer <YOUR_API_KEY>` header.

---

## Troubleshooting

**Authorization flow doesn't start** — Verify your MCP client supports OAuth 2.1 with PKCE and that you're using the correct server URL.

**Queries succeed but return no data** — Confirm your Extole user account has permission to access the programs or reports you're querying.

**API key authentication fails** — Verify the key is active and hasn't been revoked.