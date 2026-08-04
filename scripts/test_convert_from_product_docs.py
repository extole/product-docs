import importlib.util
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


if __name__ == "__main__":
    unittest.main()
