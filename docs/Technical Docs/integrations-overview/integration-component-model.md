---
title: "Create the Integration Campaign and Component Model"
excerpt: "Create the campaign, root, and integration component, set the display metadata and logo the admin renders, and add typed sockets and a configuration view.\n"
---

This page is one part of the Management API integration guide. Start at [Create an Integration with the Management API](doc:management-api-integration) for the build paths and the creation contract.

## Create the Integration Campaign

Create an `INTEGRATION` campaign with the `integration` program type. The campaign tag below names the
integration component this campaign carries, matching what library bundles do so an installed copy can
be traced back to its source. It is not what puts the integration on the Integrations page; the
component tags created two sections down are.

```bash
curl --request POST "$EXTOLE_API_HOST/v2/campaigns" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "Example Integration",
    "description": "Receives partner lifecycle events and maps them to Extole business events.",
    "campaign_type": "INTEGRATION",
    "program_type": "integration",
    "tags": ["internal:integration-component-name:example"]
  }'
```

Record the returned campaign identifier and version. Campaign creation also creates a default `PROGRAM` label equal to the campaign identifier.

Replace the default with a unique, readable program label when the integration contract defines one:

```bash
curl --request POST "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/labels" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "example-integration",
    "type": "PROGRAM"
  }'
```

A campaign has one active `PROGRAM` label. Creating a new one replaces the previous program label. Always read the current campaign response and pass that value in test and partner event payloads.

## Create the Component Model

Create a root component following the Custom Integration Template conventions. Leave
`internal:type:integration` off the root: the Integrations page excludes root components, so the tag
does nothing there and the integration component created in the next step is what carries it.

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "root",
    "description": "Declares campaign-level variables and cross-campaign inheritance.",
    "tags": ["internal:self-managed"]
  }'
```

Record `ROOT_COMPONENT_ID`, refresh the campaign version, and create the model component:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "example",
    "display_name": "Example",
    "description": "Receives Example lifecycle events.",
    "types": [
      "integration-v10.0"
    ],
    "component_ids": [
      "'"$ROOT_COMPONENT_ID"'"
    ],
    "tags": [
      "internal:type:integration",
      "internal:self-managed"
    ],
    "variables": [
      {
        "name": "short.description",
        "type": "STRING",
        "values": {
          "default": "Connect Example lifecycle events to Extole."
        },
        "tags": [
          "internal:ui-display"
        ]
      },
      {
        "name": "about",
        "type": "STRING",
        "values": {
          "default": "This integration receives Example events and maps them to Extole business events."
        },
        "tags": [
          "internal:ui-display"
        ]
      },
      {
        "name": "documentation.url",
        "type": "STRING",
        "values": {
          "default": "https://docs.extole.com/docs/example"
        },
        "tags": [
          "internal:ui-display"
        ]
      },
      {
        "name": "external.url",
        "type": "STRING",
        "values": {
          "default": "https://www.example.com"
        },
        "tags": [
          "internal:ui-display"
        ]
      },
      {
        "name": "external.integration.url",
        "type": "STRING",
        "values": {
          "default": "https://marketplace.example.com/extole"
        },
        "tags": [
          "internal:ui-display"
        ]
      },
      {
        "name": "categories",
        "type": "STRING",
        "values": {
          "default": "eCommerce Platform"
        },
        "tags": [
          "internal:ui-display"
        ]
      },
      {
        "name": "logo",
        "type": "IMAGE",
        "values": {
          "default": "https://origin.xtlo.net/type=asset:clientShortName=example-components:originAssetId=tj9rg15cj0eu6mdf3b8c/example.png"
        },
        "tags": [
          "internal:ui-display"
        ]
      },
      {
        "name": "imageKey",
        "type": "STRING",
        "values": {
          "default": "example"
        },
        "tags": [
          "internal:ui-display"
        ]
      }
    ]
  }'
```

All eight display settings are in that one create request. The integration type requires every one of them, so a create that sends only a readable subset — a description and a documentation link, say — is rejected rather than partially accepted, and there is no later mutation that makes the component valid without them. The next section covers what each value should say.

Use `variables` when creating a component. Do not send a `settings` property in `CampaignComponentCreateRequest`.

Type the model component with the current integration type. `integration-v10.0` is the long-standing revision, and later revisions such as `integration-v10.1` exist; when extending an installed source, keep the type it already carries rather than downgrading it to match this example.

## Set Integration Display Metadata

The integration type requires eight settings: `short.description`, `about`, `documentation.url`, `external.url`, `external.integration.url`, `categories`, `logo`, and `imageKey`. The type checks that they are present, not that their values are usable, so a component that passes validation can still render as an unnamed tile with a broken image.

| Setting | Value convention |
| :------ | :--------------- |
| `short.description` | One sentence for the integration tile. |
| `about` | A short paragraph describing what the integration receives and sends. |
| `documentation.url` | The partner-facing documentation page for this integration. Not this build guide. |
| `external.url` | The partner's own product site. |
| `external.integration.url` | The partner's marketplace or extension listing, or an empty string when the partner has none. |
| `categories` | A single category string already used by other integrations, such as `eCommerce Platform`. The admin groups integrations by exact value, so a new spelling or a list-shaped value creates an orphan category. |
| `logo` | Type `IMAGE`. **This is the image the Integrations page renders.** Either an absolute image URL or a buildtime expression resolving an asset this component owns, such as `spel@buildtime:context.getAsset('example').getUrl()`. The admin binds the built value straight to an image source, so anything that is not a working URL after the build shows the grey Extole placeholder. |
| `imageKey` | The stable key the platform resolves to its own stored partner image, used by the older partner detail view. The partner page names it; it is not the partner's name lowercased or the page's slug. It does not render the integration tile, so it is never a substitute for `logo`. |

Tag all eight with `internal:ui-display`, exactly that string. That tag means the setting describes the integration tile, and the admin hides tagged settings from the settings list. A tag invented to mean the same thing — `internal:tile-metadata` and the like — leaves every display setting showing in the configuration list beside the partner's real settings.

Use the types the platform expects, not the ones the value suggests. `categories` is a `STRING` holding one category, and a `STRING_LIST` holding one category is a different value that groups the integration nowhere. Read a working integration's own settings before inventing either the type or the vocabulary.

### Give the Integration a Logo That Resolves

An integration with everything else in place and no working `logo` is the most common way a finished build looks broken: every other tile shows artwork and this one shows a grey placeholder. Treat the logo as part of the build, not as an optional flourish.

The Integrations page reads the **built** value of `logo`. Confirm what a component actually renders by reading the built listing rather than the source component:

```bash
curl --request GET \
  "$EXTOLE_API_HOST/v1/components/built?having_all_tags=internal:type:integration&limit=50" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN"
```

A resolved logo looks like an absolute URL on Extole's asset host:

```json
{
  "name": "logo",
  "type": "IMAGE",
  "values": { "default": "https://origin.xtlo.net/type=asset:clientShortName=example-components:originAssetId=tj9rg15cj0eu6mdf3b8c/example.png" }
}
```

When a registered component for this partner already exists, that built URL is the artwork to use: copy it verbatim into your component's `logo`. It is served from Extole's own asset host and is already what every client sees on the available-to-install tile for that partner, so it needs no upload and no file. Copy `rewardSupplierLogo` the same way for a reward integration.

Copy from `/v1/components/built`, never from `/v1/components`. The source listing returns the unresolved expression `spel@buildtime:context.getAsset('example').getUrl()`, and that expression names an asset your component does not own, so pasting it produces a setting that looks configured and resolves to nothing.

When you have the image file itself, upload it as multipart form data with the metadata in an `asset` part and the bytes in a `file` part:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/components/$INTEGRATION_COMPONENT_ID/assets" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --form 'asset={"name":"example","tags":[],"description":"Example Logo"};type=application/json' \
  --form "file=@example.png;type=image/png"
```

Then give the setting the buildtime expression that resolves it, `spel@buildtime:context.getAsset('example').getUrl()`, which builds into a hosted URL on the account's own asset domain. A reward integration carries a second asset the same way — `reward-supplier-logo`, exposed as a `rewardSupplierLogo` setting — and repeats that asset and setting on every supplier template, so a product shows its own artwork wherever a marketer meets it rather than only on the integration tile.

An empty value is not an option the platform offers. `logo` is typed `IMAGE`, and creating the component with `"default": ""` is rejected outright:

```json
{
  "code": "settings_build_failed",
  "parameters": { "errors": { "logo": {
    "code": "variable_value_invalid_type",
    "expected_types": ["IMAGE"],
    "details": "The value: is not valid for the type:IMAGE"
  } } }
}
```

Since the type also requires the setting to be present, there is no valid component without a real logo value. When that rejection arrives, go and find the registered component's built URL. Do not reach instead for the first image URL on the partner's documentation page — a screenshot or a favicon hotlinked from someone else's host is not the partner's logo, and it satisfies the API while still rendering wrong.

For a partner with no registered component anywhere and no supplied file, say plainly that the artwork is the one piece you cannot source, name the setting it belongs in, and let the requester supply the file rather than filling the gap with something that merely passes validation.

After setting it, read the component back from `/v1/components/built` and confirm `logo` holds an absolute URL on Extole's asset host. A value that is still an expression, or one pointing at a partner or documentation host, is a tile that renders wrong or not at all.

Add partner configuration variables separately, and never tag them `internal:ui-display` — a partner setting carrying that tag disappears from the configuration view even when `settingsToDisplay` names it, which is the most common reason a freshly built integration looks empty on its configuration tab. Give each one a display name, description, type, default, `importance:basic`, and a priority that orders it in the view. Prefix partner-specific configuration settings with the integration component name — `exampleAccountUrl`, `exampleSetupInstructions` — so they stay unambiguous when read from the parent component.

Setup instructions tell the partner-side installer what to send and where. Give them the event endpoint, the current program label, the event names, the payload fields, the credential rule, and the documentation link.

The program label belongs here because the sender cannot work without it: it is what targets an arriving event at this integration, and [Send Platform Events to Extole](doc:sending-platform-events) tells implementers to read the current label from this view. Take the value from the campaign you read in the previous step rather than typing a label from another account, and tell the installer to hold it as configuration rather than as a constant in code. Because the value is interpolated when the setting is created, replacing the campaign's `PROGRAM` label later means updating this setting too — otherwise the view keeps advertising a label that no longer targets anything.

Compute the instructions at build time so the installer reads the values this campaign actually uses rather than values copied from another account. Substitute the campaign's current program label for `PROGRAM_LABEL` before sending the request:

```json
{
  "name": "exampleSetupInstructions",
  "type": "STRING",
  "display_name": "Example Extension Setup",
  "description": "Connection details for the server-side Example extension.",
  "tags": ["category:configuration", "importance:basic"],
  "priority": "20",
  "values": {
    "default": "javascript@buildtime:(function(){ return \"Extole event endpoint: https://api.extole.io/v6/events\\nProgram label (send as data.labels): PROGRAM_LABEL\\nEvent names: example_order_created, example_order_shipped, example_order_canceled\\nUse a server-side access token from the Security Center. Do not use a token that can manage campaigns in the partner application.\"; })()"
  }
}
```

Never place a credential value in a setting that the configuration view displays.

## Add Typed Sockets

Add a `businessEvents` multi-socket to the integration component:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components/$INTEGRATION_COMPONENT_ID/settings" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "businessEvents",
    "display_name": "Business Events",
    "description": "Reusable business events produced from partner input events.",
    "type": "MULTI_SOCKET",
    "filters": [
      {
        "type": "COMPONENT_TYPE",
        "component_type": "business-event-v10.0"
      }
    ]
  }'
```

Add a `views` multi-socket:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components/$INTEGRATION_COMPONENT_ID/settings" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "views",
    "display_name": "Views",
    "description": "Views rendered in the integration UI.",
    "type": "MULTI_SOCKET",
    "filters": [
      {
        "type": "COMPONENT_TYPE",
        "component_type": "view-v10.0"
      }
    ]
  }'
```

Socket filters are part of the model contract. Do not create an untyped socket or attach a component that does not satisfy its filter.

## Add a Configuration View

Create a `config-view-v10.0` child and attach it to the integration model component:

```bash
curl --request POST \
  "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID/version/$CAMPAIGN_VERSION/components" \
  --header "Authorization: Bearer $MANAGEMENT_API_ACCESS_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "name": "configuration",
    "display_name": "Configuration",
    "description": "Configuration view for the Example integration.",
    "types": [
      "config-view-v10.0"
    ],
    "installed_into_socket": "views",
    "component_ids": [
      "'"$INTEGRATION_COMPONENT_ID"'"
    ],
    "variables": [
      {
        "name": "order",
        "type": "INTEGER",
        "values": {
          "default": 1
        }
      },
      {
        "name": "title",
        "type": "STRING",
        "values": {
          "default": "Configuration"
        }
      },
      {
        "name": "status",
        "type": "STRING",
        "values": {
          "default": "javascript@buildtime:context.getComponent().getParent().getVariableValue(\"exampleAccountUrl\") ? \"READY\" : \"IN_PROGRESS\""
        }
      },
      {
        "name": "settingsToDisplay",
        "type": "STRING_LIST",
        "values": {
          "default": [
            "exampleAccountUrl",
            "exampleSetupInstructions"
          ]
        }
      }
    ]
  }'
```

`component_ids` must identify the parent model component. Without it, the platform may try to install the view into the root component, which does not own the `views` socket.

The `settingsToDisplay` values are names of settings on the parent integration model component. Naming a setting here is necessary but not sufficient: the setting itself must be visible in the settings list, which means it must not carry `internal:ui-display`. Read the built integration back and confirm each named setting appears with its display name before calling the configuration surface done. A hardcoded `status` leaves the tab permanently marked in progress; the buildtime expression above returns `READY` only once the settings Extole can verify are complete. Explain any partner-side checks that the status cannot verify.

The information setting the installer reads is the `exampleSetupInstructions` built above, not a further one to invent: it already carries the endpoint, the current program label, the partner event names, the documentation URL, and the credential rule. Name it in `settingsToDisplay`, as the example does — a configuration view that omits it renders a tab with an account URL and nothing telling the installer what to send or where. Do not put a credential value in it.

Every name in `settingsToDisplay` must be a setting that exists on the parent integration component. A name with no matching parent setting fails validation, and the two names in the example resolve to the two partner settings created above.
