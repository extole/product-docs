# docs.extole.com design rubric

The taste test for a docs page or a change to the site's look. It is the documentation member of the
Extole design family indexed in [`extole/design`](https://github.com/extole/design).

| Field | Value |
| --- | --- |
| Source | `.mintlify/AGENTS.md` for criteria 1 to 5 and 8; `docs.json`, `style.css` and `public/style.css` for 6 and 7 |
| Scope | Every page and stylesheet published to docs.extole.com |
| Owner | Unassigned. @ekthayer owns page content in CODEOWNERS; the stylesheets have no owner |
| Version | 0.1.0 |
| Status | Criteria 1 to 5 and 8 are `observed`: they restate written standards. 6 and 7 are `proposed`. So is the pass mark |

Score each criterion 0, 1 or 2 on a rendered preview, light and dark, without knowing who made it.
**Proposed pass mark: 12 of 16, and no criterion at 0.** The owner sets the real one.

| # | Criterion | 0 | 1 | 2 | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | In the right place | A how-to in Product Docs, or a topic covered twice | Right tab, awkward group | The tab and group the question belongs to | `.mintlify/AGENTS.md` » Where a page lives |
| 2 | Scannable | A wall of text | Headings, but long sections | Short sections under headings a reader can scan | » Page structure |
| 3 | Components as written | Bold text standing in for a callout | The wrong callout severity | Callouts, frames and code blocks as the standard names them | » Formatting |
| 4 | Images that help | A remote URL, or an image with no `alt` | Generic `alt`, no frame | Repo images in a `<Frame>`, with real `alt` and a caption where it helps | » Links and images |
| 5 | Literals intact | An event name or field restyled | Formatting drift on one literal | Every literal verbatim, in code font | » Literals |
| 6 | On theme | A color, font or `style` in the page | A new value in a stylesheet with no variable | Only the owning stylesheet's variables | [`SKILL.md`](../SKILL.md) » Know which file styles what |
| 7 | Readable in both themes | Text below 4.5:1, or unreadable in dark | One weak pair | Every text pair at 4.5:1 or better, light and dark | WCAG 2.2 AA |
| 8 | True | A claim nobody checked | Mostly checked | Every behavior, name and number checked against the platform | » Accuracy |

Checked by script, not scored: MDX that does not build and navigation entries with no file
(`npx mint@latest validate`), and pages missing from navigation (`python3 scripts/check_navigation.py`).
