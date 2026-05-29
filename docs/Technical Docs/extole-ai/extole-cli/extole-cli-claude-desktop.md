---
title: Claude Desktop
excerpt: >-
  Configure Claude Desktop to use the Extole CLI as an MCP tool source in one
  command.
hidden: false
---
The Extole CLI can configure Claude Desktop as an MCP client in one command, without manual JSON editing.

## Prerequisites

- [Extole CLI](doc:extole-cli) installed and authenticated
- [Claude Desktop](https://claude.ai/download) installed

## Setup

**Step 1: Run the setup command**

```bash
extole serve setup
```

This detects your Claude Desktop config file and writes the Extole MCP server entry automatically.

**Step 2: Restart Claude Desktop**

Quit and relaunch Claude Desktop.

**Step 3: Verify**

Open a new chat and ask about your programs:

> *"What programs are active right now?"*

Claude will invoke the Extole CLI tools and return results directly in the chat.

## How it works

`extole serve` runs the CLI as an MCP stdio server. Claude Desktop spawns it automatically on launch and can call any CLI command as a tool — no separate Extole account or OAuth flow required beyond your existing CLI token.

## Removing the integration

```bash
extole serve remove
```

This removes the Extole entry from Claude Desktop's config. Restart Claude Desktop to apply.

## Troubleshooting

**Tools not appearing after restart** — Run `extole serve setup` again to ensure the config was written correctly, then restart Claude Desktop.

**Auth errors** — Run `extole auth status` to confirm your token is valid.