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


if __name__ == "__main__":
    unittest.main()
