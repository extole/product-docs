---
title: Hubspot (Private Beta)
excerpt: >
  HubSpot is an AI-powered customer platform with all the software,
  integrations, and resources you need to connect your marketing, sales, and
  customer service.
deprecated: false
hidden: true
metadata:
  robots: index
---
> 📘 This Hubspot integration has not been released and is in private beta.

# Extole HubSpot App — Installation Guide

## Overview

Installation takes about 20–30 minutes and is performed by the Extole implementation team. The Extole team deploys the app to the client's HubSpot portal via the HubSpot CLI; the client then configures it through the app UI.

After completing these steps the app is fully operational:

- HubSpot record changes fire events to Extole in real time
- Referral attribution is captured at form submission and stored on the Contact record
- Share links are generated for new contacts and written back to HubSpot

**Intended audience:** Extole implementation team.

***

## Prerequisites

| Requirement                | Details                                                                                                                                                                                                           |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **HubSpot tier**           | Operations Hub **Professional** or higher — required for serverless functions. Starter tier cannot run this app.                                                                                                  |
| **HubSpot portal access**  | The Extole team needs CLI access to the client's portal. Either: (a) client adds an Extole team member as a portal admin, or (b) client generates a Personal Access Key (PAK) and shares it securely. See Step 0. |
| **Extole API token**       | Long-lived bearer token for the client's Extole account — generated in the Extole Security Center                                                                                                                 |
| **HubSpot-embedded forms** | Required for Manage Advocate Codes; Configure Events and Manage Share Links work without it                                                                                                                       |

### Personal Access Key (PAK)

If the client is providing a PAK rather than adding the Extole team member as a portal admin:

1. Client logs into HubSpot → **Settings → Integrations → Private Apps**
2. Create a new private app with the scopes listed in the app's `app-hsmeta.json`
3. Copy the access token and share it securely with the Extole team

***

## Step 0 — CLI Setup and Deploy

The HubSpot CLI is required to deploy the app to the client's portal and set the Extole API token as a portal secret.

### 0a — Configure the CLI for the client's portal

The HubSpot CLI requires a `hubspot.config.yml` in the project root. This file is gitignored — copy the example and fill in the client's values:

```bash
cp hubspot.config.example.yml hubspot.config.yml
```

Edit `hubspot.config.yml`:

- `name` / `defaultPortal` — a local alias for the client portal (e.g. `acme-corp`)
- `personalAccessKey` — the PAK from the client (or your own if added as portal admin)
- `portalId` — the client's HubSpot portal ID (visible in the URL when logged in)

### 0b — Deploy the app

```bash
hs project upload
```

This builds and deploys all app components to the client's portal. The app will appear under **Settings → Integrations** once deployed.

### 0c — Set the Extole API token

```bash
hs secret add EXTOLE_API_TOKEN
```

When prompted, paste the client's Extole API token. This stores the token as a portal-level secret accessible only to the app's serverless functions.

Verify the connection after deployment by opening the app and clicking **Test Connection** in the Configure Events tab.

***

## Step 1 — Create Contact Properties

The Manage Advocate Codes snippet and Manage Share Links feature write data to custom Contact properties. These must exist before using either feature.

In the **Configure Events** tab, find the **Properties** section:

1. Confirm the property names (defaults: `extole_advocate_code`, `extole_share_link`)
2. Click **Create Properties**

This creates the properties if they don't exist. The operation is idempotent — safe to run again.

| Property               | Purpose                                                                       |
| ---------------------- | ----------------------------------------------------------------------------- |
| `extole_advocate_code` | Advocate code captured at form submission; used for attribution               |
| `extole_share_link`    | Share link URL written back from Extole; displayed in HubSpot for the contact |

> If the client's Extole program uses `hubspotutk` for attribution (legacy), also create `extole_hubspotutk`. Most new implementations use the advocate code approach; skip this unless the program requires it.

***

## Step 2 — Configure Event Workflows

In the **Configure Events** tab, create one workflow per Extole event the client needs.

### Minimum recommended events

| Object  | Trigger                                           | Event Name                | Purpose                                                            |
| ------- | ------------------------------------------------- | ------------------------- | ------------------------------------------------------------------ |
| Contact | Record created                                    | `hubspot_contact_created` | Friend enters CRM — triggers advocate attribution lookup in Extole |
| Deal    | Record created                                    | `hubspot_deal_created`    | Opportunity opened                                                 |
| Deal    | Field changed to value: `dealstage` = `closedwon` | `hubspot_deal_closed_won` | Conversion — triggers advocate reward                              |

### Creating a workflow

1. Click **Add Workflow**
2. Set **Event Name** — the Extole event name (e.g. `hubspot_deal_closed_won`)
3. Set **Object** — Contact, Deal, Company, etc.
4. Set **Trigger**:
   - **Record created** — fires on any new record of that type
   - **Field changed** — fires any time the selected field changes
   - **Field changed to value** — fires when a field reaches a specific value (e.g. `dealstage` → `closedwon`)
5. Add **Field Mappings** — map HubSpot properties to Extole event payload keys. Default mappings are pre-filled per object type:
   - Contact: `email`, `contact_id`, `first_name`, `last_name`, `hubspotutk`
   - Deal: `deal_id`, `deal_name`, `amount`, `close_date`
6. Click **Create Workflow**

The workflow is created and enabled immediately.

### Common HubSpot field API names

| Label           | API name         |
| --------------- | ---------------- |
| Deal Stage      | `dealstage`      |
| Amount          | `amount`         |
| Close Date      | `closedate`      |
| Deal Name       | `dealname`       |
| Lifecycle Stage | `lifecyclestage` |

***

## Step 3 — Deploy Form Snippet

_Skip this step if the client does not use HubSpot-embedded forms._

The Manage Advocate Codes snippet captures the advocate code from the share URL and injects it into HubSpot form submissions so that friend Contacts are attributed to the correct advocate.

> **Prerequisites:** Step 1 (Create Properties) must be completed before Step 3a. The `extole_advocate_code` Contact property must exist before HubSpot will offer it as a field option in the form builder. If the hidden field is not added to the form, the snippet will still run without errors — but the advocate code will be silently dropped at form submission and never land on the Contact record.

### 3a — Add hidden field to each HubSpot form

For every form you want to instrument, add `extole_advocate_code` as a hidden field in HubSpot's form builder.

> **Why this is required:** HubSpot's server only saves fields explicitly defined on the form. Values injected client-side for fields not on the form are silently dropped.

1. Open the form in HubSpot's form builder
2. Add a field → choose **Contact property** → select `Extole Advocate Code`
3. Set it to hidden
4. Save the form

Repeat for each form you want to instrument.

### 3b — Get and deploy the snippet

In the **Manage Advocate Codes** tab:

1. Set the **Advocate Code Property** (default: `extole_advocate_code`) — must match the property name in Step 1
2. Set the **Referral URL Params** (default: `extole_shareable_code`) — the URL parameter name Extole puts on share links
3. Optionally set form targeting (all forms, or specific form IDs)
4. Copy the generated snippet
5. Add the snippet to the client's site — it must load **before** the HubSpot forms script (`js.hsforms.net`)

**Where to place it:** Add it once, site-wide — typically via a tag manager (GTM, etc.) or the site's global `<head>` template, before the `//js.hsforms.net/...` script tag. It does not need to be added per page.

**How it works:**

1. When a friend lands via a share link (URL has `?extole_shareable_code=<code>`), the snippet stores the code in a 30-day cookie and localStorage
2. On that page, and on every subsequent page the friend navigates to, the snippet injects `extole_advocate_code=<code>` as a URL param via `window.history.replaceState` before any HubSpot form loads
3. HubSpot reads URL params at form init time and pre-populates the hidden `extole_advocate_code` field natively
4. The friend can convert on any page — the code persists across the entire visit

***

## Step 4 — Manage Share Links

In the **Manage Share Links** tab:

1. Set the **Share Link Property** (default: `extole_share_link`) — the Contact property that will receive the generated share link URL
2. Enable **Auto-generate Share Links** to create a share link for every new Contact automatically
3. Optionally select a **Campaign Targeting Label** to scope share links to a specific Extole program
4. Click **Save**

### Backfill existing contacts

To generate share links for contacts that existed before the app was installed:

1. Click **Run Backfill**
2. Monitor progress — the UI polls and shows processed / errors counts
3. The operation is idempotent (safe to re-run; contacts that already have a share link are skipped)

***

## Step 5 — Anonymous Advocate Sync (optional)

This step wires the reverse direction: when an anonymous person provides their email in an Extole share experience, Extole calls a HubSpot endpoint that upserts the matching contact and writes their share link. Skip this step if the client doesn't run anonymous share flows.

### 5a — Get the webhook URL and shared secret from HubSpot

In the app's **Manage Share Links** tab → **Anonymous Advocate Sync** section:

1. Click **Enable** to activate the endpoint and generate a shared secret
2. Copy the **Webhook URL** (auto-discovered, format `https://<portalId>.hs-sites-<region>.com/hs/serverless/api/advocate-sync`)
3. Copy the **Shared Secret**

### 5b — Confirm the Extole integration is available

The Extole-side **Hubspot Advocate Sync** integration is provisioned by the Extole platform team for the client's account. Confirm in the client's Extole account at **my.extole.com → Partners → Hubspot Advocate Sync** that the integration is listed.

The integration ships with:

- A Partners-page integration entry with **Configuration** settings (Webhook URL, Shared Secret)
- An RAF companion that listens for `advocate_code_created` (SHAREABLE) events across the client's RAF campaigns and dispatches to the configured HubSpot endpoint

### 5c — Configure the integration

In **my.extole.com → Partners → Hubspot Advocate Sync → Configuration**:

1. Paste the **Webhook URL** from step 5a into the `Webhook URL` setting
2. Paste the **Shared Secret** from step 5a into the `Shared Secret` setting
3. Save

The integration is now live. Any `advocate_code_created` event in any RAF campaign in this Extole account will dispatch to HubSpot's endpoint, which upserts the contact by email and writes the share link.

> **Note:** When this flow creates a brand-new contact, the **Auto Generate Share Link** workflow's enrollment criteria (`extole_share_link IS_UNKNOWN`) prevents it from minting a duplicate share link. No additional configuration needed.

***

## Step 6 — Enable the CRM Card

The Extole app includes a sidebar card on the Contact record that shows the captured advocate code and HubSpot visitor ID.

In HubSpot:

1. Open any Contact record
2. In the right sidebar, click **Customize** (or the settings icon)
3. Find **Extole Activity** in the available cards list and add it
4. Save the layout

The card will show "No referral data captured" for contacts without attribution data, and will display the advocate code once form instrumentation captures it.

***

## Step 7 — Verify End-to-End

### Verify event delivery

After creating the Contact Created workflow, create a test contact in HubSpot. Confirm the event arrives in Extole:

```bash
extole stream --app-type extole-hubspot-app --sandbox
```

Or check a specific person:

```bash
extole person get --email test@example.com
```

### Verify attribution

Full attribution requires a friend to arrive via a share link and submit a form. In a staging or test environment:

1. Get an advocate's share link from Extole (or construct `https://<site>?extole_shareable_code=<code>`)
2. Visit the client's site via that link — confirm the URL param is present
3. Navigate to another page — confirm the snippet injects `extole_advocate_code` into the URL via `replaceState`
4. Submit a HubSpot form
5. Check that the new Contact has `extole_advocate_code` populated with the code
6. Confirm the `hubspot_contact_created` event arrived in Extole

***

## Troubleshooting

| Symptom                                 | Likely cause                                                                                                                                                                                                                   |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Test Connection fails                   | Token wrong or expired — re-run `hs secret add EXTOLE_API_TOKEN` with the correct value                                                                                                                                        |
| Workflow fires but no event in Extole   | The Extole token is embedded in the workflow at creation time. If the token was updated after the workflow was created, use **Update Workflow** (or delete and recreate) to push the new token into the workflow's custom code |
| `extole_advocate_code` empty on Contact | Hidden field not added to form in form builder (Step 3a) — snippet runs silently but code is dropped at submission; or snippet not loading before forms script; or `extole_advocate_code` property not yet created (Step 1)    |
| Form snippet has no effect              | Snippet must load before `//js.hsforms.net/...` — check script order in `<head>`                                                                                                                                               |
| Share link backfill shows errors        | Extole API token lacks shareables scope; or contacts have no email address                                                                                                                                                     |
| CRM card not showing                    | Layout customization not saved per Step 5                                                                                                                                                                                      |

For deeper debugging, check the **Settings Log** tab for recent configuration actions and errors.

***

## Known Limitations

- **Cross-device attribution** — the advocate code cookie is browser-scoped. A friend who clicks on mobile and converts on a different device loses the attribution. Document this gap with the client.
- **HubSpot-native forms only** — Manage Advocate Codes works with HubSpot's JS-embedded forms (v2 classic and v3 new form builder). Typeform, Marketo, and custom HTML forms are not supported.
- **Operations Hub Professional required** — Starter tier clients cannot use this app. Must be confirmed before implementation.
- **Share link label** — A default campaign label (`exhsappd`) is applied to all share links until the Extole shareables API makes the label optional. If the client's program does not have this label, share link creation will fail. Contact Extole support to ensure the label exists on the client's program.
- **Distribution model** — The app is currently deployed via the HubSpot CLI (not a self-serve install link). Each client install requires CLI access to the client's portal. Self-serve distribution via private install link or marketplace would require additional infrastructure investment.

<br />
