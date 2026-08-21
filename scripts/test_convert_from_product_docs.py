import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("convert_from_product_docs.py")
SPEC = importlib.util.spec_from_file_location("converter", SCRIPT)
converter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(converter)


class RemoteImageRewriteTests(unittest.TestCase):
    def test_rewrites_markdown_and_html_images_only(self):
        markdown_url = "https://files.readme.io/example-image.png"
        html_url = "https://downloads.intercomcdn.com/example-image"
        source = f'''![Diagram]({markdown_url} "Diagram title")
<img src="{html_url}" alt="Screenshot" width="60%" />
[An ordinary link]({markdown_url})
`![Example]({markdown_url})`
```md
![Example]({markdown_url})
```
'''
        local_paths = {
            markdown_url: "/images/extole/diagram.png",
            html_url: "/images/extole/screenshot.png",
        }

        result = converter.rewrite_remote_images(source, local_paths)

        self.assertIn('![Diagram](/images/extole/diagram.png "Diagram title")', result)
        self.assertIn('<img src="/images/extole/screenshot.png" alt="Screenshot" width="60%" />', result)
        self.assertIn(f'[An ordinary link]({markdown_url})', result)
        self.assertIn(f'`![Example]({markdown_url})`', result)
        self.assertIn(f'![Example]({markdown_url})\n```', result)

    def test_discovers_only_rendered_remote_images(self):
        image_url = "https://files.readme.io/example-image.png"
        html_url = "https://downloads.intercomcdn.com/example-image"
        source = f'''![Diagram]({image_url})
<img src="{html_url}" alt="Screenshot" />
[An ordinary link]({image_url})
```
![Example]({image_url})
```
'''

        self.assertEqual(converter.remote_image_urls(source), {image_url, html_url})

    def test_detects_common_image_extensions(self):
        self.assertEqual(converter.image_extension(b"\x89PNG\r\n\x1a\n", "application/octet-stream", "https://example.com/1"), ".png")
        self.assertEqual(converter.image_extension(b"<svg viewBox=\"0 0 1 1\" />", "text/plain", "https://example.com/1"), ".svg")

    def test_rewrites_cached_images_without_downloading(self):
        source_url = "https://files.readme.io/example-image.png"
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            asset = out / "images/extole/example.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"local image")
            (out / "images/extole-manifest.json").write_text(
                json.dumps({"assets": [{"path": "/images/extole/example.png", "sourceUrls": [source_url]}]}),
                encoding="utf-8",
            )
            page = out / "guide.mdx"
            page.write_text(f"![Example]({source_url})\n", encoding="utf-8")

            assets, pages, unresolved = converter.ImageMigrator(out).rewrite_cached()

            self.assertEqual((assets, pages, unresolved), (1, 1, 0))
            self.assertEqual(page.read_text(encoding="utf-8"), "![Example](/images/extole/example.png)\n")

    def test_adds_context_alt_text_for_empty_and_filename_values(self):
        source = '''---
title: "Sample guide"
---

## Create an audience

Click **Add member** to include a person in the audience.

![](/images/extole/empty.png)
![Screen Shot 2024-01-01.png](/images/extole/named.png)
<img src="/images/extole/html.png" alt="" />
'''

        result, changed = converter.add_context_alt_text(source, "Fallback")

        expected = "Screenshot showing Click Add member to include a person in the audience."
        self.assertEqual(changed, 3)
        self.assertIn(f"![{expected}](/images/extole/empty.png)", result)
        self.assertIn(f"![{expected}](/images/extole/named.png)", result)
        self.assertIn(f'<img src="/images/extole/html.png" alt="{expected}" />', result)

    def test_context_alt_uses_section_fallback_without_nearby_prose(self):
        source = '''---
title: "Sample guide"
---

## Create an audience

![Screen Shot 2024-01-01.png](/images/extole/named.png)
'''

        result, changed = converter.add_context_alt_text(source, "Fallback")

        self.assertEqual(changed, 1)
        self.assertIn(
            "![Screenshot for Create an audience in the Sample guide.](/images/extole/named.png)",
            result,
        )


class OpenApiNavigationTests(unittest.TestCase):
    def test_groups_tags_and_operations_in_readme_order(self):
        spec = {
            "paths": {
                "/zebra": {"delete": {"tags": ["Alpha"], "summary": "A title that does not control sorting"}},
                "/aardvark": {"get": {"tags": ["Alpha"], "summary": "Z title that does not control sorting"}},
                "/beta": {
                    "delete": {"tags": ["Beta"]},
                    "post": {"tags": ["Beta"]},
                    "get": {"tags": ["Beta"]},
                    "put": {"tags": ["Beta"]},
                    "patch": {"tags": ["Beta"]},
                },
                "/hidden": {"get": {"tags": ["Alpha"], "x-hidden": True}},
            }
        }

        groups = converter.openapi_navigation_groups(spec)

        self.assertEqual([group["group"] for group in groups], ["Alpha", "Beta"])
        self.assertEqual(groups[0]["pages"], ["DELETE /zebra", "GET /aardvark"])
        self.assertEqual(groups[1]["pages"], [
            "DELETE /beta",
            "POST /beta",
            "GET /beta",
            "PUT /beta",
            "PATCH /beta",
        ])

    def test_sync_api_navigation_replaces_automatic_spec_groups(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            spec_dir = out / "api-reference"
            spec_dir.mkdir()
            (spec_dir / "integration-consumer-to-extole.json").write_text(
                json.dumps(
                    {
                        "paths": {
                            "/profiles/{id}": {"get": {"tags": ["Profiles"]}},
                            "/auth": {"post": {"tags": ["Authentication"]}},
                        }
                    }
                ),
                encoding="utf-8",
            )
            (out / "docs.json").write_text(
                json.dumps(
                    {
                        "navigation": {
                            "tabs": [
                                {
                                    "tab": "API Reference",
                                    "groups": [
                                        {"group": "Getting Started", "pages": ["api-reference/overview"]},
                                        {"group": "Consumer to Extole API", "openapi": "api-reference/old.json", "pages": []},
                                    ],
                                }
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )

            self.assertEqual(converter.sync_api_navigation(out), 1)

            groups = json.loads((out / "docs.json").read_text(encoding="utf-8"))["navigation"]["tabs"][0]["groups"]
            self.assertEqual([group["group"] for group in groups], ["Getting Started", "Consumer to Extole API"])
            self.assertEqual(groups[1]["pages"], [
                {"group": "Authentication", "pages": ["POST /auth"]},
                {"group": "Profiles", "pages": ["GET /profiles/{id}"]},
            ])


if __name__ == "__main__":
    unittest.main()


class NavMirroredPathTests(unittest.TestCase):
    """A page's URL must equal its navigation breadcrumb."""

    def test_slugify_nav_expands_ampersand(self):
        # plain slugify drops "&", collapsing the label to programs-campaigns
        self.assertEqual(converter.slugify("Programs & Campaigns"), "programs-campaigns")
        self.assertEqual(converter.slugify_nav("Programs & Campaigns"), "programs-and-campaigns")
        self.assertEqual(converter.slugify_nav("Audiences & Segmentation"), "audiences-and-segmentation")

    def test_tab_roots_drop_the_docs_suffix(self):
        self.assertEqual(converter.TAB_SLUGS["Product Docs"], "product")
        self.assertEqual(converter.TAB_SLUGS["Technical Docs"], "technical")
        self.assertEqual(converter.API_TAB_SLUG, "api-reference")

    def test_group_directory_comes_from_the_sidebar_label_not_the_folder(self):
        """The regression this restructure fixed: a folder named getting-started
        served a group labelled "Extole Overview" at /…/getting-started/…"""
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory) / "src"
            out = Path(directory) / "out"
            group = src / "getting-started"
            group.mkdir(parents=True)
            (group / "index.md").write_text('---\ntitle: "Extole Overview"\n---\n', encoding="utf-8")
            (group / "what-is-extole.md").write_text(
                '---\ntitle: "What is Extole?"\n---\n\nBody.\n', encoding="utf-8"
            )
            conv = converter.Converter(src, out)
            grp = conv._make_group(group, "product")

            self.assertEqual(grp["group"], "Extole Overview")
            self.assertEqual(grp["pages"], ["product/extole-overview/what-is-extole"])

    def test_openapi_groups_share_the_generated_page_prefix(self):
        """Mintlify serves generated operation pages from /api-reference wherever
        the bundle lives, so the tab root has to match or the tab splits."""
        group = converter.api_reference_group("Management API", "management.json", {"paths": {}})
        self.assertEqual(group["openapi"], "api-reference/management.json")

    def test_redirects_survive_regeneration(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            (out / converter.URL_MAP_FILE).write_text(
                json.dumps({"redirects": [
                    {"source": "/product-docs/getting-started/what-is-extole",
                     "destination": "/product/extole-overview/what-is-extole"},
                    {"source": "/bad"},  # malformed entries are ignored
                ]}),
                encoding="utf-8",
            )
            redirects = converter.read_redirects(out)
            self.assertEqual(len(redirects), 1)
            self.assertEqual(converter.build_docs_json([], redirects)["redirects"], redirects)

    def test_read_redirects_tolerates_a_missing_map(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(converter.read_redirects(Path(directory)), [])


class GroupIndexTests(unittest.TestCase):
    def _group(self, index_frontmatter):
        directory = tempfile.mkdtemp()
        src, out = Path(directory) / "src", Path(directory) / "out"
        group = src / "offer"
        group.mkdir(parents=True)
        body = "\n\n" + ("word " * 60)
        (group / "index.md").write_text(index_frontmatter + body, encoding="utf-8")
        (group / "customer-appreciation.md").write_text(
            '---\ntitle: "Customer Appreciation"\n---\n\nBody.\n', encoding="utf-8"
        )
        conv = converter.Converter(src, out)
        return conv, conv._make_group(group, "product")

    def test_hidden_group_index_is_not_published(self):
        """It was read but never acted on, so an internal page marked hidden
        upstream was still written and served, just missing from the nav."""
        conv, grp = self._group('---\ntitle: "Offer"\nhidden: true\n---\n')
        self.assertNotIn("root", grp)
        self.assertEqual([p.out_path for p in conv.pages if p.out_path.endswith("/index")], [])

    def test_group_index_is_reachable_by_its_folder_name(self):
        """Upstream writes [Offer](doc:offer) for a page at offer/index.md whose
        own stem is the useless "index"; without the alias it cannot resolve."""
        conv, grp = self._group('---\ntitle: "Offer"\n---\n')
        self.assertEqual(grp["root"], "product/offer/index")
        self.assertEqual(conv.slug_to_path.get("offer"), "product/offer/index")
        self.assertEqual(
            converter.rewrite_links("See [Offer](doc:offer).", conv.slug_to_path),
            "See [Offer](/product/offer/index).",
        )


class GroupWithOnlyHiddenChildrenTests(unittest.TestCase):
    def test_overview_survives_when_every_child_is_hidden(self):
        """Returning None here wrote the root page to disk but left it out of
        the navigation — live but unreachable."""
        with tempfile.TemporaryDirectory() as directory:
            src, out = Path(directory) / "src", Path(directory) / "out"
            group = src / "financial-services"
            group.mkdir(parents=True)
            (group / "index.md").write_text(
                '---\ntitle: "Financial Services"\n---\n\n' + ("word " * 60), encoding="utf-8"
            )
            (group / "mastercard.md").write_text(
                '---\ntitle: "Mastercard"\nhidden: true\n---\n\nBody.\n', encoding="utf-8"
            )
            conv = converter.Converter(src, out)
            grp = conv._make_group(group, "technical")

            written = [p.out_path for p in conv.pages]
            self.assertEqual(written, ["technical/financial-services/index"])
            self.assertIsNotNone(grp)
            self.assertEqual(grp["pages"], ["technical/financial-services/index"])
            # nothing written to disk may be absent from the nav
            self.assertEqual(set(written) - set(grp["pages"]), set())

    def test_group_is_dropped_when_there_is_nothing_to_show(self):
        with tempfile.TemporaryDirectory() as directory:
            src, out = Path(directory) / "src", Path(directory) / "out"
            group = src / "empty"
            group.mkdir(parents=True)
            (group / "only.md").write_text(
                '---\ntitle: "Only"\nhidden: true\n---\n\nBody.\n', encoding="utf-8"
            )
            conv = converter.Converter(src, out)
            self.assertIsNone(conv._make_group(group, "technical"))
            self.assertEqual(conv.pages, [])


class OrderYamlOmissionTests(unittest.TestCase):
    """_order.yaml was an allowlist that failed silently in both directions.

    Anything it did not mention vanished from the site, and an entry matching
    no file matched nothing quietly — between them, 15 Flow Campaigns guides
    and the Fulfilled Rewards Report were live on ReadMe and absent here.
    """

    def _tree(self, directory, guides_order, extra=()):
        src = Path(directory) / "src"
        docs = src / "docs"
        guides = docs / "Guides"
        deep = guides / "deep"
        deep.mkdir(parents=True)
        (docs / "_order.yaml").write_text("- Guides\n", encoding="utf-8")
        (guides / "_order.yaml").write_text(guides_order, encoding="utf-8")
        (deep / "_order.yaml").write_text("- dupe\n", encoding="utf-8")
        page = '---\ntitle: "{}"\n---\n\nBody.\n'
        (guides / "listed.md").write_text(page.format("Listed"), encoding="utf-8")
        (guides / "orphan.md").write_text(page.format("Orphan"), encoding="utf-8")
        # the shallow copy of a guide whose canonical version lives in deep/
        (guides / "dupe.md").write_text(page.format("Dupe"), encoding="utf-8")
        (deep / "dupe.md").write_text(page.format("Dupe"), encoding="utf-8")
        for name in extra:
            (guides / f"{name}.md").write_text(page.format(name), encoding="utf-8")
        return src, Path(directory) / "out", guides

    def test_a_page_no_one_else_serves_is_restored_after_the_ordered_ones(self):
        with tempfile.TemporaryDirectory() as directory:
            src, out, guides = self._tree(directory, "- listed\n- deep\n")
            conv = converter.Converter(src, out)
            nav = conv.collect(guides, "guides", converter.read_order(guides))

            self.assertEqual(nav[0], "guides/listed")
            self.assertIn("guides/orphan", nav)
            # restored, never reordered ahead of the curated names
            self.assertGreater(nav.index("guides/orphan"), nav.index("guides/listed"))

    def test_a_deliberate_duplicate_stays_dropped(self):
        """Upstream keeps shallow copies that _order.yaml omits on purpose,
        because a deeper copy is canonical and both carry the same slug."""
        with tempfile.TemporaryDirectory() as directory:
            src, out, guides = self._tree(directory, "- listed\n- deep\n")
            conv = converter.Converter(src, out)
            conv.collect(guides, "guides", converter.read_order(guides))

            written = [p.out_path for p in conv.pages]
            self.assertIn("guides/deep/dupe", written)
            self.assertNotIn("guides/dupe", written)

    def test_an_order_entry_matching_no_file_is_reported(self):
        """The Fulfilled Rewards Report was lost to exactly this: its order
        file says fulfilled-reports-report, the file is fulfilled-rewards."""
        with tempfile.TemporaryDirectory() as directory:
            src, out, guides = self._tree(directory, "- listed\n- deep\n- typoed-name\n")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                converter.Converter(src, out)

            self.assertIn("typoed-name", stderr.getvalue())
            self.assertIn("matches nothing on disk", stderr.getvalue())

    def test_restoring_a_page_is_announced(self):
        with tempfile.TemporaryDirectory() as directory:
            src, out, _ = self._tree(directory, "- listed\n- deep\n")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                converter.Converter(src, out)

            self.assertIn("orphan.md is unlisted", stderr.getvalue())

    def test_a_hidden_unlisted_page_is_left_alone(self):
        with tempfile.TemporaryDirectory() as directory:
            src, out, guides = self._tree(directory, "- listed\n- deep\n")
            (guides / "secret.md").write_text(
                '---\ntitle: "Secret"\nhidden: true\n---\n\nBody.\n', encoding="utf-8"
            )
            conv = converter.Converter(src, out)
            conv.collect(guides, "guides", converter.read_order(guides))

            self.assertNotIn("guides/secret", [p.out_path for p in conv.pages])


class ReadmeWidgetTests(unittest.TestCase):
    """ReadMe components that leaked onto the page as literal text.

    sanitize_mdx escapes the "<" of any tag it does not recognise, so a widget
    the converter missed did not fail loudly -- it rendered as "</Image>" or
    "<Callout icon=...>" in the middle of the prose.
    """

    def test_callout_component_maps_to_a_mintlify_callout(self):
        body = '<Callout icon="\U0001F4D8" theme="info">\n  Read the [docs](doc:x)\n</Callout>'
        out = converter.convert_body(body, {})
        self.assertIn("<Info>", out)
        self.assertIn("</Info>", out)
        self.assertNotIn("Callout", out)

    def test_callout_theme_decides_when_the_icon_is_unknown(self):
        body = '<Callout icon="\U0001F3A8" theme="warn">\n  Careful\n</Callout>'
        self.assertIn("<Warning>", converter.convert_body(body, {}))

    def test_image_caption_and_closing_tag_are_consumed(self):
        body = '<Image src="https://x/y.png" title="Shot">\n  A **caption** here\n</Image>'
        out = converter.convert_body(body, {})
        self.assertIn("<Frame>", out)
        self.assertIn('<img src="https://x/y.png"', out)
        self.assertIn("A **caption** here", out)   # markdown survives
        self.assertNotIn("Image", out)

    def test_an_uncaptioned_image_stays_a_bare_img(self):
        out = converter.convert_body('<Image src="https://x/y.png" alt="Y" />', {})
        self.assertIn('<img src="https://x/y.png"', out)
        self.assertNotIn("<Frame>", out)

    def test_a_self_closing_anchor_does_not_swallow_later_content(self):
        """It has no </Anchor>, so the paired pattern ran forward to the next
        widget's closing tag -- on braze.md that wrapped a heading in a link."""
        body = (
            '<Anchor label="Learn more" target="_blank" href="https://braze.com/" />\n\n'
            '## Integration Model\n\nProse.\n\n'
            'See <Anchor href="https://x/api">the API</Anchor>.\n'
        )
        out = converter.convert_body(body, {})
        self.assertIn("[Learn more](https://braze.com/)", out)
        self.assertIn("\n## Integration Model\n", out)      # still a heading
        self.assertNotIn("[## Integration Model", out)
        self.assertIn("[the API](https://x/api)", out)

    def test_readme_only_widget_is_dropped_not_printed(self):
        out = converter.convert_body("Before\n\n<ImproveOpenRatesCallout />\n\nAfter\n", {})
        self.assertNotIn("ImproveOpenRatesCallout", out)
        self.assertIn("Before", out)
        self.assertIn("After", out)

    def test_placeholders_still_render_as_literal_text(self):
        """<REPORT_NAME> and friends are prose placeholders, not components."""
        out = converter.convert_body('Set **<REPORT_NAME>** and **<FORMAT>**.', {})
        self.assertIn("&lt;REPORT_NAME>", out)
        self.assertIn("&lt;FORMAT>", out)


class CodeBlockSurvivalTests(unittest.TestCase):
    """Fenced code blocks vanished from 81 pages during the ReadMe migration.

    convert_body parks fenced blocks and inline code spans in two stores while
    the widget passes run. Both stores used the same placeholder mark, so the
    Nth fence and the Nth inline span became the same string and the first
    restore claimed both -- the sample JSON on a page was replaced by whatever
    short phrase happened to be the Nth `code` span in its prose.
    """

    def test_a_code_block_survives_an_earlier_inline_span(self):
        body = "Set the `utm_term` value.\n\n```json\n{\"a\": 1}\n```\n"
        out = converter.convert_body(body, {})

        self.assertIn('```json\n{"a": 1}\n```', out)
        self.assertIn("`utm_term`", out)

    def test_every_block_survives_however_many_inline_spans_precede_it(self):
        body = (
            "One `alpha` two `beta` three `gamma`.\n\n"
            "```js\nfirst();\n```\n\n"
            "```js\nsecond();\n```\n"
        )
        out = converter.convert_body(body, {})

        self.assertIn("first();", out)
        self.assertIn("second();", out)
        for span in ("`alpha`", "`beta`", "`gamma`"):
            self.assertIn(span, out)

    def test_a_body_carrying_a_placeholder_mark_is_refused(self):
        with self.assertRaises(ValueError):
            converter._protect(f"a{converter.FENCE_MARK}b", converter.FENCE_RE, [],
                               mark=converter.FENCE_MARK)

    def test_the_three_placeholder_marks_are_distinct(self):
        marks = (converter.FENCE_MARK, converter.TAG_MARK, converter.INLINE_MARK)
        self.assertEqual(len(set(marks)), 3)


class CategoryLinkTargetTests(unittest.TestCase):
    def test_a_link_to_a_category_resolves_to_its_first_page(self):
        """A folder whose index.md is too thin to publish has no page, so
        [Report Types](doc:report-types) fell through to a bare /report-types
        that 404s. Newly fleshed-out upstream indexes started linking to their
        sibling categories, which is how this surfaced."""
        with tempfile.TemporaryDirectory() as directory:
            src, out = Path(directory) / "src", Path(directory) / "out"
            group = src / "report-types"
            group.mkdir(parents=True)
            (group / "index.md").write_text(
                '---\ntitle: "Report Types"\n---\n\nshell\n', encoding="utf-8"
            )
            (group / "audience-reports.md").write_text(
                '---\ntitle: "Audience Reports"\n---\n\nBody.\n', encoding="utf-8"
            )
            conv = converter.Converter(src, out)
            conv._make_group(group, "guides")

            # the thin index is not published, so the slug has no page of its own
            self.assertNotIn("report-types", conv.slug_to_path)
            self.assertEqual(conv.group_prefixes["report-types"], "guides/report-types")
            targets = conv.link_targets()
            self.assertEqual(
                targets["report-types"], "guides/report-types/audience-reports"
            )
            self.assertEqual(
                converter.rewrite_links("See [Report Types](doc:report-types).", targets),
                "See [Report Types](/guides/report-types/audience-reports).",
            )


class PreservedTabTests(unittest.TestCase):
    def test_a_hand_authored_tab_survives_regeneration(self):
        """News is assembled from the ReadMe changelog and newsletters and has
        no upstream source, so rebuilding the navigation used to drop it while
        its .mdx files stayed on disk, serving nothing."""
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            (out / "docs.json").write_text(
                json.dumps({"navigation": {"tabs": [
                    {"tab": "Guides", "groups": [{"group": "stale", "pages": ["x"]}]},
                    {"tab": "News", "pages": ["news/recent-releases"]},
                ]}}),
                encoding="utf-8",
            )
            kept = converter.read_extra_tabs(out, {"Guides", "API Reference"})

            self.assertEqual(kept, [{"tab": "News", "pages": ["news/recent-releases"]}])

    def test_read_extra_tabs_tolerates_a_missing_docs_json(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(converter.read_extra_tabs(Path(directory), set()), [])
