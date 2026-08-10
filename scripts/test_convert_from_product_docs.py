import importlib.util
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
