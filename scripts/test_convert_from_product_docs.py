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
