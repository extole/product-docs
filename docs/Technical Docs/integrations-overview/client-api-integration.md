---
title: "Create an Integration With the Client API"
excerpt: "Choose the build path for an integration, follow the creation contract, and gather what every path needs.\n"
---

# Overview

Use the Client API to create an integration campaign and its component hierarchy directly in Extole. This workflow is intended for Extole Chat, installers, and operational services that must build an integration without adding a bundle to the creative repository.

An API-created integration is still a component-based integration. It must use the same reusable component types, typed sockets, business-event templates, views, naming conventions, and validation rules as a bundled v10 integration.

## Decide Whether This Is an Install or a Client-Local Build

Creating an integration-shaped campaign and installing a registered integration are different outcomes.
The distinction matters whenever the requester expects the result on the My Extole
<Anchor label="Integrations page" target="_blank" href="https://my.extole.com/integrations">Integrations page</Anchor>.

| Requested outcome | Correct action | What makes it appear |
| :---------------- | :------------- | :------------------- |
| A registered integration every client can find and install | Publish the partner's integration component to the Extole-owned library. | An Extole-owned component tagged `internal:type:integration` and `internal:self-managed`. |
| An installed instance for this client | Duplicate the library source, or build the campaign and component tree below. | A non-root component owned by this client, tagged `internal:type:integration` and `internal:self-managed`. |
| A development-account build to inspect, configure, or test through campaign and component APIs | Create the campaign and component tree directly. | The same client-owned component; it is visible to this client only. |

The Integrations page selects built components by the tag `internal:type:integration`. Among those, it
treats a component as this client's installed integration when the component's source client is this
client, and as an available type to install when the source client is Extole. Two further conditions
decide whether a client-owned component shows up at all:

- **Root components are excluded.** The integration component must be a child of the campaign root,
  never the root component itself.
- **Without `internal:self-managed` the entry renders as unavailable** rather than installed.

The tags that decide visibility therefore sit on the non-root integration component. A build that
follows the component model below is visible; one that puts the integration tags only on the campaign,
or only on the root component, is not.

`internal:integration-component-name:<component-name>` is a separate, older convention. Library bundles
carry it on the integration campaign so an installed copy can be traced back to the component it came
from, and this guide keeps it for parity with those bundles. The Integrations page does not read it, so
setting it does not make a build appear and omitting it does not hide one. Do not reach for it to fix a
build that is missing from the page — check the component's tags, its owner, and whether it is the root.

Building the tree in one account does not register a new partner for anyone else. When the request is
for a new installable partner that every client can see, build and validate the shape in the
development account first, then publish the reusable component to the Extole-owned library, and say
plainly that the account-local build is not yet an installable integration.

Examples in this guide use a generic partner named `example`. Substitute the real partner name, event names, and field names from that partner's own documentation.

Where a partner-specific page exists in this documentation set, read it first: it carries the wire contract for that platform — event names, payload fields, and status mapping — while this guide carries the build sequence that applies to every platform. Partner pages are published under the partner's name as the page slug, so retrieve the page directly by that slug rather than relying on a keyword search to surface it.

## Choose the Integration Category First

Place the platform in a category before creating anything. [Integration Categories](doc:integration-categories) describes what each category contains and how to recognize it; this guide carries the API sequence that builds it. Pick the path from discovery, not from habit.

| Category | When it applies | Build path |
| :------- | :-------------- | :--------- |
| Outbound library install | The duplicatable listing already has an integration component whose name matches the partner. | Duplicate that library component with no target campaign, reshape it to the finished shape on the partner page, then attach webhooks and credentials. Follow [Build an Outbound Library Integration](doc:integration-build-outbound) below. |
| Reward fulfillment | The partner supplies gift cards, prepaid cards, points, or payouts that Extole orders when a reward is earned. | Install the maintained source when one exists; otherwise build the supplier type, the support campaign of supplier templates, and the integration with its `REWARD` webhooks. Follow [Build a Reward Fulfillment Integration](doc:integration-build-reward-fulfillment) below. |
| Inbound custom build | No maintained source exists for the partner, or the request is an inbound platform that maps wire events onto canonical business events. | Create an `INTEGRATION` campaign from the custom integration template, then add business events, trigger rules, data capture, and views. This is a client-local build unless a registered integration component is published separately. |

Before creating anything, query the duplicatable listing for integration components and look for one whose name matches the partner. Match on the component name, not on a fixed type version: the integration type is revised over time, so a source may be typed `integration-v10.0`, `integration-v10.1`, or a later revision, and a query pinned to one revision reports a maintained partner as missing. Prefer that name match over building from `custom_integration`. Rebuilding a maintained partner from the custom template produces a campaign that looks related and does none of the partner's webhook or credential work.

A request that adds inbound scope to a maintained outbound partner uses both paths: install the library source first, then add business events to the installed campaign using the inbound sequence.

## Where the Rest of This Guide Lives

This page carries what every build path shares. The sequences themselves are separate pages, each short
enough to be retrieved whole:

| Page | Use it for |
| :--- | :--------- |
| [Create the Integration Campaign and Component Model](doc:integration-component-model) | The campaign, root, and integration component; display metadata and the logo the admin renders; typed sockets and the configuration view. Every path needs this page. |
| [Build an Outbound Library Integration](doc:integration-build-outbound) | Installing a maintained partner source and reshaping it, then attaching its outbound webhooks and credential. |
| [Build a Reward Fulfillment Integration](doc:integration-build-reward-fulfillment) | A partner that fulfills rewards: supplier type, support campaign, supplier templates, reward webhooks, report runner, and event stream. |
| [Map Inbound Partner Events](doc:integration-inbound-events) | Business events, input event rules, and event data for an integration that receives partner events. |
| [Validate and Publish an Integration](doc:integration-validation) | Gating outbound resources, the validation checklist, and connecting the integration to a program. |

Read the page for the path you are on rather than working from this one alone. A build that stops after
the campaign and the integration component has created the container and none of the integration.

## Extole Chat Creation Contract

Extole Chat must follow these rules when it creates or changes an integration:

1. Confirm the client, environment, partner platform and version, inbound and outbound scope, event contract, credential owner, and publication approval before making changes.
2. Read the partner's current documentation and verify version-specific event hooks. Do not infer hook names or payload shapes from another platform.
3. Inspect the target client before creating resources. Reuse an active integration when its campaign and component identity match the request, extend it, and report that. Archived campaigns are not candidates for reuse: they receive no events and hold no program label against a new campaign, so their presence is not a reason to restore one, to pick a different label, or to ask the requester which path to take instead of building what they asked for.
4. Discover first whether a maintained integration source already exists for the partner, matching on component name across every current `integration-v10.x` type rather than on one pinned revision. When it does, install that source by duplicating it into a new campaign, then reshape it to the partner page's finished tree and webhook set before configuring credentials. Only when no maintained partner integration exists should Chat build from the custom integration template. Do not save library component identifiers in prompts or documentation.
5. Treat the calls that complete a reshape — creating a component type, deleting an unused library child, publishing, and creating a webhook — as part of the create instruction. Attempt them; when one is refused because it requires a higher mode, raise the mode and continue. A mode that is available but not currently active is not a missing authorization, so never report a shape gap as outside what you are allowed to do without having tried and been refused. Stopping after a raw library install, or reporting a known gap as someone else's step, leaves the requester with an integration the partner page does not describe.
6. Use campaign-version-scoped mutation endpoints. Refresh the latest campaign version after every mutation.
7. Use reusable business-event, rule, and data components. Do not create a custom controller when a reusable template implements the behavior.
8. Keep partner input event names distinct from canonical Extole business event names.
9. Map every persisted field explicitly, in the same run that creates the business events. Assign key types based on field semantics, not field spelling. A business event with an empty `data` socket captures nothing and is not a finished event.
10. Add a `views` socket and at least one configuration view. The view must expose the settings required to complete partner setup.
11. Create reward suppliers, client keys, or webhooks only when an approved outbound flow uses them. A reward fulfillment partner is such a flow: its suppliers, `REWARD` webhooks, and credential setting are the integration, not extras added to an inbound build.
12. Build and inspect the complete campaign before publishing. Test every inbound event and every configured outbound path.
13. Keep a resource ledger containing campaign, component, external resource, and test identifiers. Use it for verification and cleanup.
14. Never put access tokens, secrets, or private client values in documentation, component descriptions, logs, or example payloads.
15. Report partial results as incomplete. Do not describe a draft, disabled webhook, placeholder URL, or unverified event as production-ready.

## Gather Requirements

Collect these values before calling the API:

| Value | Requirement |
| :---- | :---------- |
| Client API access token | Server-side token authorized to manage campaigns and components. |
| Management API host | The production host for campaign and component calls, held in `EXTOLE_API_HOST`. |
| Event API host | The production host for event submission, held in `EXTOLE_EVENT_API_HOST`. |
| Partner platform and version | Determines event hooks, payloads, and authentication options. |
| Integration name and component name | Human-readable campaign name and stable lowercase component name. |
| Program label | Unique, stable label used to target events to the integration. |
| Inbound event contract | Partner event names, identity fields, unique identifiers, and values. |
| Canonical business events | Extole names such as `converted`, `shipped`, or `canceled`. |
| Field mapping | Explicit source-to-destination mapping for every captured field. |
| Partner configuration | Store URL, account identifier, endpoint, status mapping, or equivalent settings. |
| Outbound requirements | Destination, trigger, authentication, retry contract, and owning program, when outbound behavior is required. |
| Publication approval | Confirmation that the target client and environment may be changed. |

Management calls and event submission use different hosts. Every example in this guide reads them from these variables:

```bash
EXTOLE_API_HOST=https://api.extole.io
EXTOLE_EVENT_API_HOST=https://events.extole.io
```

Use separate credentials for integration management and event ingestion. The partner application must not receive the Client API management token.

## Use Roll-Forward Campaign Versions

Campaign mutations create a new version. A version used by one successful request is stale for the next request.

Refresh the version before every version-scoped mutation:

```bash
CAMPAIGN_VERSION=$(
  curl --silent --show-error --fail-with-body \
    "$EXTOLE_API_HOST/v2/campaigns/$CAMPAIGN_ID" \
    --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" |
  jq --raw-output '.version'
)
```

Use the singular path segment `/version/{version}`:

```text
/v2/campaigns/{campaign_id}/version/{version}/components
```

Do not use `/versions/`. If the API returns `stale_version` or `concurrent_update`, retrieve the campaign again, reconcile the latest state, and retry only the intended mutation.

## Discover Reusable Components

Find templates at execution time through the duplicatable-components endpoint. This endpoint returns components that the current client can duplicate, including components made available through subscriptions and grants.

```bash
curl --get "$EXTOLE_API_HOST/v1/components/duplicatable" \
  --header "Authorization: Bearer $CLIENT_API_ACCESS_TOKEN" \
  --data-urlencode "name=template_transacted_business_event" \
  --data-urlencode "version_state=PUBLISHED" \
  --data-urlencode "having_any_types=business-event-v10.0" \
  --data-urlencode "show_all=true"
```

After the target component and socket exist, add `target_component_id` and `target_setting_name` to return only components compatible with that socket. Do not use the deprecated `target_socket_name` parameter. Narrowing this way is the reliable form of the query, because a widely used source such as `input_event` also appears once for every campaign that already installed a copy of it.

Use these reusable sources:

| Component | Program label | Purpose |
| :-------- | :------------ | :------ |
| `template_transacted_business_event` | `business-events` | Revenue or transaction outcome. |
| `template_tracked_business_event` | `business-events` | Non-revenue lifecycle milestone. |
| `input_event` | `rules` | Matches one or more partner input event names. |
| `business_event_data` | `business-events` | Captures one mapped field. |
| `event_id` | `business-events` | Captures the Extole event identifier when required. |

Validate each candidate's type before duplicating it, and prefer the v10 type when a legacy version of the same name is also returned.

Several results with the same name and the same v10 type are copies of one maintained source, one per campaign that installed it, not a choice between different behaviors. Narrow by the target socket and duplicate the maintained source; that is not the ambiguity worth stopping for. Stop when discovery returns no published match of the required type, or when two genuinely different components could satisfy the request and choosing wrongly would change behavior.

## Record the Result

The creation response must include:

- Environment and client.
- Campaign identifier, current version, state, and program label.
- Root and model component identifiers.
- Canonical business events and partner trigger names.
- Field mappings and key types.
- View components and displayed settings.
- External resources created, or an explicit statement that none were required.
- Programs whose business events were replaced or added to, or an explicit statement that the integration is not yet connected to a program.
- Test event identifiers and verification results.
- Documentation URL.
- Remaining manual partner steps.

Do not claim the integration is complete while partner-side installation, credentials, status mapping, or end-to-end tests remain outstanding.
