#!/usr/bin/env python3
"""Convert Extole product-docs (ReadMe-flavored markdown) + extole-specification
OpenAPI bundles into a Mintlify docs.json v2 site.

One-shot migration tool for the ReadMe -> Mintlify bake-off (ai-tools#346, Phase 1).

Usage:
  python scripts/convert_from_product_docs.py \
      --product-docs /path/to/product-docs \
      --specification /path/to/extole-specification \
      --out .

It writes .mdx pages, copies the OpenAPI specs, and regenerates docs.json.

To update only the generated API navigation from the local OpenAPI bundles:
  python scripts/convert_from_product_docs.py --out . --sync-api-navigation
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen

try:
    import yaml
except ImportError:  # pragma: no cover
    raise SystemExit("PyYAML required: pip install pyyaml")

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

CALLOUT_EMOJI = {
    "📘": "Info",
    "ℹ️": "Info",
    "🚧": "Warning",
    "❗": "Warning",
    "❗️": "Warning",
    "⚠️": "Warning",
    "🛑": "Danger",
    "👍": "Tip",
    "✅": "Check",
    "📖": "Note",
    "📝": "Note",
}


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "page"


def slugify_nav(name: str) -> str:
    """Slugify a navigation label for use as a URL path segment.

    A page's URL is its navigation breadcrumb, so directory names are derived
    from the sidebar label rather than from the upstream folder name. Kept
    separate from slugify() because "&" must survive as "and" here — plain
    slugify() drops it, turning "Programs & Campaigns" into "programs-campaigns"
    — while page filenames still slugify from their upstream stem unchanged.
    """
    return slugify(re.sub(r"\s*&\s*", " and ", name))


# Tab roots are the one segment not taken from a navigation label: the tab is
# labelled "Product Docs" but the URL should read /product/... .
TAB_SLUGS = {
    "Product Docs": "product",
    "Technical Docs": "technical",
    "Guides": "guides",
}

API_TAB_SLUG = "api-reference"


def add_union_titles(spec: dict) -> int:
    """Lift discriminator mapping keys onto oneOf branches as titles.

    Mintlify renders a discriminated union as a tab strip and labels each tab
    from the branch's `title`; with none it falls back to "Option N". ReadMe
    instead labels variants from `discriminator.mapping` keys. This copies those
    keys onto the branches (wrapped in allOf so the title survives the OpenAPI
    3.0 $ref-sibling rule) so Mintlify shows ADMIN_ICON / HS256 / ... instead.
    A dropdown control for large unions is still a Mintlify feature request
    (github.com/orgs/mintlify/discussions/1723); this is the best available.
    """
    schemas = (spec.get("components") or {}).get("schemas") or {}
    titled = 0
    for schema in schemas.values():
        if not isinstance(schema, dict):
            continue
        mapping = (schema.get("discriminator") or {}).get("mapping") or {}
        one_of = schema.get("oneOf")
        if not mapping or not isinstance(one_of, list):
            continue
        key_by_ref = {ref: key for key, ref in mapping.items()}
        rebuilt = []
        for branch in one_of:
            ref = branch.get("$ref") if isinstance(branch, dict) else None
            key = key_by_ref.get(ref)
            if not key:
                rebuilt.append(branch)
                continue
            target = schemas.get(ref.rsplit("/", 1)[-1])
            if isinstance(target, dict) and not target.get("title"):
                target["title"] = key
            rebuilt.append({"title": key, "allOf": [{"$ref": ref}]})
            titled += 1
        schema["oneOf"] = rebuilt
    return titled


def split_frontmatter(text: str):
    if text.startswith("---"):
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
        if m:
            try:
                fm = yaml.safe_load(m.group(1)) or {}
            except Exception:
                fm = {}
            if not isinstance(fm, dict):
                fm = {}
            return fm, m.group(2)
    return {}, text


def yaml_str(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def has_substantive_index_body(body: str) -> bool:
    """Return whether an index contains useful overview content, not just a shell."""
    body_without_headings = re.sub(r"^#{1,6}\s+.*$", "", body, flags=re.MULTILINE)
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'-]*", body_without_headings)
    return len(words) >= 40


# ---- body transforms -------------------------------------------------------

FENCE_RE = re.compile(r"(```.*?```|~~~.*?~~~)", re.DOTALL)
INLINE_CODE_RE = re.compile(r"(`[^`\n]+`)")
MARKDOWN_IMAGE_RE = re.compile(
    r"!\[[^\]]*\]\(\s*(?P<url>https?://[^\s)]+)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)"
)
HTML_IMAGE_RE = re.compile(
    r"<img\b[^>]*?\bsrc\s*=\s*(?P<quote>[\"'])(?P<url>https?://.*?)(?P=quote)",
    re.IGNORECASE | re.DOTALL,
)
LOCAL_MARKDOWN_IMAGE_RE = re.compile(
    r"!\[(?P<alt>[^\]]*)\]\(\s*(?P<path>/images/extole/[^\s)]+)(?P<title>\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)"
)
LOCAL_HTML_IMAGE_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
HTML_LOCAL_SRC_RE = re.compile(r"\bsrc=(?:\"(?P<double>/images/extole/[^\"]*)\"|'(?P<single>/images/extole/[^']*)')", re.IGNORECASE)
HTML_ALT_RE = re.compile(r"\balt=(?:\"(?P<double>[^\"]*)\"|'(?P<single>[^']*)')", re.IGNORECASE)
FILENAME_ALT_RE = re.compile(r"^.+\.(?:png|jpe?g|gif|webp|svg)$", re.IGNORECASE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
FRONTMATTER_TITLE_RE = re.compile(r"^title:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)

MAX_IMAGE_BYTES = 20 * 1024 * 1024
IMAGE_WORKERS = 4
IMAGE_EXTENSION_BY_CONTENT_TYPE = {
    "image/avif": ".avif",
    "image/bmp": ".bmp",
    "image/gif": ".gif",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/svg+xml": ".svg",
    "image/tiff": ".tif",
    "image/webp": ".webp",
    "image/x-icon": ".ico",
}


def _protect(text: str, pattern: re.Pattern, store: list, mark: str = "\x00") -> str:
    def repl(m):
        store.append(m.group(0))
        return f"{mark}{len(store) - 1}{mark}"

    return pattern.sub(repl, text)


def _restore(text: str, store: list, mark: str = "\x00") -> str:
    for i, chunk in enumerate(store):
        text = text.replace(f"{mark}{i}{mark}", chunk)
    return text


def remote_image_urls(text: str) -> set[str]:
    """Return remote URLs used as rendered images, excluding code examples."""
    fences: list = []
    text = _protect(text, FENCE_RE, fences, mark="\x01")
    inlines: list = []
    text = _protect(text, INLINE_CODE_RE, inlines, mark="\x02")
    return {
        m.group("url")
        for pattern in (MARKDOWN_IMAGE_RE, HTML_IMAGE_RE)
        for m in pattern.finditer(text)
    }


def rewrite_remote_images(text: str, local_paths: dict[str, str]) -> str:
    """Replace only rendered remote image URLs with mapped local asset paths."""
    fences: list = []
    text = _protect(text, FENCE_RE, fences, mark="\x01")
    inlines: list = []
    text = _protect(text, INLINE_CODE_RE, inlines, mark="\x02")

    def repl(match):
        url = match.group("url")
        local_path = local_paths.get(url)
        return match.group(0) if not local_path else match.group(0).replace(url, local_path, 1)

    text = MARKDOWN_IMAGE_RE.sub(repl, text)
    text = HTML_IMAGE_RE.sub(repl, text)
    text = _restore(text, inlines, mark="\x02")
    return _restore(text, fences, mark="\x01")


def _plain_image_context(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[`*_~]", "", text)
    text = re.sub(r"^\s*(?:[-*+] |\d+[.)] )", "", text)
    return re.sub(r"\s+", " ", text).strip(" \t:-")


def _short_alt_text(text: str) -> str:
    return text if len(text) <= 180 else text[:177].rsplit(" ", 1)[0] + "..."


def _needs_context_alt(alt: str) -> bool:
    return not alt.strip() or bool(FILENAME_ALT_RE.fullmatch(alt.strip()))


def _html_attr(match: re.Match | None) -> str:
    if not match:
        return ""
    return next((value for value in match.groupdict().values() if value is not None), "")


def _set_html_alt(tag: str, alt: str) -> str:
    escaped = alt.replace('"', "'")
    if HTML_ALT_RE.search(tag):
        return HTML_ALT_RE.sub(f'alt="{escaped}"', tag, count=1)
    suffix = " />" if tag.rstrip().endswith("/>") else ">"
    return tag.rstrip().removesuffix("/>").removesuffix(">") + f' alt="{escaped}"{suffix}'


def add_context_alt_text(text: str, fallback_title: str) -> tuple[str, int]:
    """Fill empty or filename-only local image alt text from nearby MDX prose."""
    title_match = FRONTMATTER_TITLE_RE.search(text)
    title = _plain_image_context(title_match.group(1)) if title_match else fallback_title
    guide_title = title if title.lower().endswith("guide") else f"{title} guide"
    heading = ""
    context = ""
    updated_lines = []
    changed = 0
    frontmatter_delimiters = 2 if text.startswith("---\n") else 0

    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if frontmatter_delimiters:
            updated_lines.append(line)
            if stripped == "---":
                frontmatter_delimiters -= 1
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            heading = _plain_image_context(heading_match.group(1))

        def markdown_repl(match):
            nonlocal changed
            alt = match.group("alt")
            if not _needs_context_alt(alt):
                return match.group(0)
            replacement = (
                f"Screenshot showing {context}"
                if context
                else f"Screenshot for {heading} in the {guide_title}."
                if heading
                else f"Screenshot from the {guide_title}."
            )
            changed += 1
            return f"![{_short_alt_text(replacement)}]({match.group('path')}{match.group('title') or ''})"

        line = LOCAL_MARKDOWN_IMAGE_RE.sub(markdown_repl, line)

        def html_repl(match):
            nonlocal changed
            tag = match.group(0)
            if not _html_attr(HTML_LOCAL_SRC_RE.search(tag)):
                return tag
            alt = _html_attr(HTML_ALT_RE.search(tag))
            if not _needs_context_alt(alt):
                return tag
            replacement = (
                f"Screenshot showing {context}"
                if context
                else f"Screenshot for {heading} in the {guide_title}."
                if heading
                else f"Screenshot from the {guide_title}."
            )
            changed += 1
            return _set_html_alt(tag, _short_alt_text(replacement))

        line = LOCAL_HTML_IMAGE_RE.sub(html_repl, line)
        updated_lines.append(line)

        visible = _plain_image_context(line)
        if not heading_match and visible and "/images/extole/" not in line and not line.lstrip().startswith(("{/*", "[//]:")):
            context = visible

    return "".join(updated_lines), changed


def normalize_local_image_alt_text(out: Path) -> tuple[int, int]:
    """Apply deterministic context alt text to all generated MDX pages."""
    pages = 0
    images = 0
    for page in sorted(out.rglob("*.mdx")):
        original = page.read_text(encoding="utf-8", errors="replace")
        updated, changed = add_context_alt_text(original, page.stem.replace("-", " ").title())
        if changed:
            page.write_text(updated, encoding="utf-8")
            pages += 1
            images += changed
    return pages, images


def image_extension(data: bytes, content_type: str, source_url: str) -> str:
    """Resolve a safe image suffix from the response before writing it locally."""
    content_type = content_type.lower().split(";", 1)[0].strip()
    extension = IMAGE_EXTENSION_BY_CONTENT_TYPE.get(content_type)
    if extension:
        return extension
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return ".gif"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return ".webp"
    if data.lstrip().startswith((b"<svg", b"<?xml")) and b"<svg" in data[:4096].lower():
        return ".svg"
    extension = Path(unquote(urlparse(source_url).path)).suffix.lower()
    if extension in {".avif", ".bmp", ".gif", ".ico", ".jpeg", ".jpg", ".png", ".svg", ".tif", ".tiff", ".webp"}:
        return ".jpg" if extension == ".jpeg" else extension
    raise ValueError(f"response is not a recognized image ({content_type or 'no content type'})")


class ImageMigrator:
    """Download external MDX images and replace them with Mintlify-local paths."""

    def __init__(self, out: Path):
        self.out = out
        self.manifest_path = out / "images" / "extole-manifest.json"

    def _load_manifest(self) -> dict:
        if not self.manifest_path.exists():
            return {}
        try:
            data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except (OSError, json.JSONDecodeError):
            return {}

    def _cached_assets(self, manifest: dict) -> dict[str, dict]:
        cached = {}
        for asset in manifest.get("assets", []):
            path = asset.get("path")
            if not isinstance(path, str) or not (self.out / path.lstrip("/")).is_file():
                continue
            for url in asset.get("sourceUrls", []):
                if isinstance(url, str):
                    cached[url] = asset
        return cached

    def rewrite_cached(self) -> tuple[int, int, int]:
        """Rewrite known remote images using local assets without any network access."""
        cached = self._cached_assets(self._load_manifest())
        local_paths = {url: asset["path"] for url, asset in cached.items()}
        rewritten = 0
        unresolved = 0
        for page in sorted(self.out.rglob("*.mdx")):
            original = page.read_text(encoding="utf-8", errors="replace")
            unresolved += len(remote_image_urls(original) - set(local_paths))
            updated = rewrite_remote_images(original, local_paths)
            if updated != original:
                page.write_text(updated, encoding="utf-8")
                rewritten += 1
        return len({asset["path"] for asset in cached.values()}), rewritten, unresolved

    @staticmethod
    def _fetch(url: str) -> dict:
        for attempt in range(3):
            try:
                request = Request(url, headers={"User-Agent": "Extole-Mintlify-Image-Migration/1.0"})
                with urlopen(request, timeout=30) as response:
                    length = response.headers.get("Content-Length")
                    if length and int(length) > MAX_IMAGE_BYTES:
                        raise ValueError(f"image exceeds Mintlify's 20 MB limit ({length} bytes)")
                    data = response.read(MAX_IMAGE_BYTES + 1)
                    if len(data) > MAX_IMAGE_BYTES:
                        raise ValueError("image exceeds Mintlify's 20 MB limit")
                    content_type = response.headers.get_content_type()
                    extension = image_extension(data, content_type, url)
                    return {
                        "url": url,
                        "data": data,
                        "contentType": content_type,
                        "extension": extension,
                    }
            except (HTTPError, URLError, OSError, ValueError) as exc:
                if attempt == 2:
                    return {"url": url, "error": str(exc)}
                time.sleep(2**attempt)
        raise AssertionError("unreachable")  # pragma: no cover

    def run(self) -> tuple[int, int, int]:
        references: dict[str, set[str]] = {}
        for page in sorted(self.out.rglob("*.mdx")):
            for url in remote_image_urls(page.read_text(encoding="utf-8", errors="replace")):
                references.setdefault(url, set()).add(page.relative_to(self.out).as_posix())

        manifest = self._load_manifest()
        cached = self._cached_assets(manifest)
        resolved: dict[str, dict] = {}
        pending = []
        for url in sorted(references):
            if url in cached:
                resolved[url] = cached[url]
            else:
                pending.append(url)

        downloaded = []
        if pending:
            with ThreadPoolExecutor(max_workers=IMAGE_WORKERS) as pool:
                futures = {pool.submit(self._fetch, url): url for url in pending}
                for future in as_completed(futures):
                    downloaded.append(future.result())

        failures = []
        for result in downloaded:
            url = result["url"]
            if "error" in result:
                failures.append({"url": url, "error": result["error"], "references": sorted(references[url])})
                continue
            digest = hashlib.sha256(result["data"]).hexdigest()
            local_path = f"/images/extole/{digest}{result['extension']}"
            destination = self.out / local_path.lstrip("/")
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists():
                destination.write_bytes(result["data"])
            resolved[url] = {
                "path": local_path,
                "sha256": digest,
                "contentType": result["contentType"],
                "bytes": len(result["data"]),
                "sourceUrls": [url],
            }

        assets_by_digest: dict[str, dict] = {}
        for url, asset in resolved.items():
            digest = asset["sha256"]
            merged = assets_by_digest.setdefault(
                digest,
                {
                    "path": asset["path"],
                    "sha256": digest,
                    "contentType": asset.get("contentType", "application/octet-stream"),
                    "bytes": asset.get("bytes", 0),
                    "sourceUrls": [],
                    "references": [],
                },
            )
            merged["sourceUrls"].append(url)
            merged["references"].extend(references[url])

        local_paths = {url: asset["path"] for url, asset in resolved.items()}
        rewritten = 0
        for page in sorted(self.out.rglob("*.mdx")):
            original = page.read_text(encoding="utf-8", errors="replace")
            updated = rewrite_remote_images(original, local_paths)
            if updated != original:
                page.write_text(updated, encoding="utf-8")
                rewritten += 1

        assets = []
        for asset in assets_by_digest.values():
            asset["sourceUrls"] = sorted(set(asset["sourceUrls"]))
            asset["references"] = sorted(set(asset["references"]))
            assets.append(asset)
        assets.sort(key=lambda asset: asset["path"])
        output = {
            "schemaVersion": 1,
            "assets": assets,
            "failures": sorted(failures, key=lambda failure: failure["url"]),
        }
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        self.manifest_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
        return len(assets), rewritten, len(failures)


def convert_callouts(body: str) -> str:
    """ReadMe emoji blockquote callouts -> Mintlify components."""
    lines = body.split("\n")
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        m = re.match(r"^>\s*([\U0001F000-\U0001FAFF☀-➿️❗⁉]+)\s*(.*)$", line)
        emoji = None
        if m:
            for e in CALLOUT_EMOJI:
                if m.group(1).startswith(e):
                    emoji = e
                    break
        if emoji:
            comp = CALLOUT_EMOJI[emoji]
            title = m.group(2).strip()
            block = []
            i += 1
            while i < n and lines[i].startswith(">"):
                block.append(re.sub(r"^>\s?", "", lines[i]))
                i += 1
            inner = []
            if title:
                inner.append(f"**{title}**")
                inner.append("")
            inner.extend(block)
            content = "\n".join(inner).strip("\n")
            out.append(f"<{comp}>")
            out.append(content)
            out.append(f"</{comp}>")
        else:
            out.append(line)
            i += 1
    return "\n".join(out)


# Raw HTML tags that MDX/JSX renders fine (as strings). Anything else that looks
# like a tag is a ReadMe placeholder/widget and gets escaped to literal text.
KNOWN_HTML = {
    "a", "b", "i", "em", "strong", "u", "s", "del", "ins", "code", "pre", "br",
    "hr", "p", "span", "div", "img", "table", "thead", "tbody", "tfoot", "tr",
    "td", "th", "caption", "colgroup", "col", "ul", "ol", "li", "dl", "dt", "dd",
    "blockquote", "h1", "h2", "h3", "h4", "h5", "h6", "figure", "figcaption",
    "center", "sup", "sub", "small", "details", "summary", "video", "audio",
    "source", "picture", "iframe", "kbd", "mark", "abbr", "article", "section",
    "header", "footer", "nav", "aside", "main",
    # Mintlify / our callout components
    "Info", "Warning", "Tip", "Note", "Check", "Danger", "Card", "CardGroup",
    "Frame", "Steps", "Step", "Tabs", "Tab", "Accordion", "AccordionGroup",
    "Icon", "Tooltip", "Update", "Expandable",
}


def _attr(tag: str, name: str):
    m = re.search(rf'{name}\s*=\s*"([^"]*)"', tag, re.IGNORECASE)
    if not m:
        m = re.search(rf"{name}\s*=\s*'([^']*)'", tag, re.IGNORECASE)
    return m.group(1) if m else None


def convert_readme_image(text: str) -> str:
    """ReadMe <Image ...> widget -> plain markdown-safe <img .../>."""
    def repl(m):
        tag = m.group(0)
        src = _attr(tag, "src") or ""
        alt = _attr(tag, "alt")
        title = _attr(tag, "title") or ""
        width = _attr(tag, "width")
        if not alt or alt.strip().isdigit():
            alt = title
        alt = (alt or "").replace('"', "'").strip()
        parts = [f'src="{src}"', f'alt="{alt}"']
        if width and re.match(r"^[0-9]+%?$", width.strip()):
            parts.append(f'width="{width.strip()}"')
        return "<img " + " ".join(parts) + " />"

    return re.sub(r"<Image\b[^>]*/?>", repl, text, flags=re.IGNORECASE | re.DOTALL)


def convert_html_block(text: str) -> str:
    """ReadMe <HTMLBlock>{`...raw html...`}</HTMLBlock> -> cleaned inline HTML."""
    def repl(m):
        inner = m.group(1)
        inner = re.sub(r'\s+style\s*=\s*"[^"]*"', "", inner)
        inner = re.sub(r"\s+style\s*=\s*'[^']*'", "", inner)
        inner = re.sub(r"\sclass=", " className=", inner)
        inner = re.sub(r"<br\s*>", "<br />", inner, flags=re.IGNORECASE)
        inner = re.sub(r"(<img\b[^>]*?)\s*/?>", lambda x: x.group(1).rstrip() + " />", inner, flags=re.IGNORECASE)
        return "\n" + inner.strip() + "\n"

    return re.sub(
        r"<HTMLBlock>\s*\{`(.*?)`\}\s*</HTMLBlock>", repl, text, flags=re.DOTALL
    )


def convert_readme_anchor(text: str) -> str:
    """ReadMe <Anchor href="URL">text</Anchor> widget -> markdown link."""
    def repl(m):
        tag, inner = m.group(1), m.group(2).strip()
        href = _attr(tag, "href") or ""
        label = inner or _attr(tag, "label") or href
        return f"[{label}]({href})"

    return re.sub(r"(<Anchor\b[^>]*>)(.*?)</Anchor>", repl, text, flags=re.IGNORECASE | re.DOTALL)


def convert_readme_table(text: str) -> str:
    """ReadMe <Table align={[...]}> widget -> plain <table>. The inner markup is
    an HTML table (thead/tr/th with valid JSX style objects) that MDX renders."""
    text = re.sub(r"<Table\b[^>]*>", "<table>", text, flags=re.IGNORECASE)
    text = re.sub(r"</Table>", "</table>", text, flags=re.IGNORECASE)
    return text


TAG_SPAN_RE = re.compile(r"<[^>]+>")


def escape_braces(text: str) -> str:
    """Escape literal braces in prose so MDX doesn't read them as expressions,
    but leave braces inside HTML/JSX tags alone (valid style={{...}} etc.)."""
    tags: list = []
    text = _protect(text, TAG_SPAN_RE, tags, mark="\x02")
    text = re.sub(r"(?<!\\)\{", r"\\{", text)
    text = re.sub(r"(?<!\\)\}", r"\\}", text)
    text = _restore(text, tags, mark="\x02")
    return text


def escape_unknown_tags(text: str) -> str:
    """Escape '<' for any tag whose name is not known HTML/Mintlify, so ReadMe
    placeholders like <REPORT_NAME>, <key>, <CTA> render as literal text."""
    def repl(m):
        name = m.group(1)
        if name.lower() in {k.lower() for k in KNOWN_HTML} or name in KNOWN_HTML:
            return m.group(0)
        return "&lt;" + m.group(0)[1:]

    return re.sub(r"</?([A-Za-z][A-Za-z0-9_]*)", repl, text)


def strip_invalid_jsx_attrs(text: str) -> str:
    """Within surviving HTML tags, drop style="..." and rename class -> className."""
    def repl(m):
        tag = m.group(0)
        tag = re.sub(r'\s+style\s*=\s*"[^"]*"', "", tag)
        tag = re.sub(r"\s+style\s*=\s*'[^']*'", "", tag)
        tag = re.sub(r"\sclass=", " className=", tag)
        return tag

    return re.sub(r"<[A-Za-z][^>]*>", repl, text)


def rewrite_links(text: str, slug_to_path: dict) -> str:
    def doc_repl(m):
        target = m.group(1)
        anchor = ""
        if "#" in target:
            target, anchor = target.split("#", 1)
            anchor = "#" + anchor
        path = slug_to_path.get(target)
        if path:
            return f"](/{path}{anchor})"
        return f"](/{slugify(target)}{anchor})"

    text = re.sub(r"\]\(doc:([^)\s]+)\)", doc_repl, text)
    text = re.sub(r"\]\(ref:([^)\s]+)\)", f"](/{API_TAB_SLUG})", text)
    return text


def sanitize_mdx(text: str) -> str:
    # strip HTML comments (not allowed in MDX v3)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    # ReadMe <Glossary>term</Glossary> widget -> plain text
    text = re.sub(r"</?Glossary>", "", text, flags=re.IGNORECASE)
    # self-close common void elements
    text = re.sub(r"<br\s*>", "<br />", text, flags=re.IGNORECASE)
    text = re.sub(r"<hr\s*>", "<hr />", text, flags=re.IGNORECASE)
    text = re.sub(r"(<img\b[^>]*?)\s*/?>", lambda m: m.group(1).rstrip() + " />", text, flags=re.IGNORECASE)
    # drop style="..." and rename class -> className inside surviving tags
    text = strip_invalid_jsx_attrs(text)
    # escape '<' for tags that are not real HTML/Mintlify components
    text = escape_unknown_tags(text)
    # escape stray '<' that does not begin a tag/closing-tag/comment
    text = re.sub(r"<(?![a-zA-Z/!])", "&lt;", text)
    # escape literal braces in prose (MDX treats { as an expression), but leave
    # braces inside surviving tags (valid JSX style={{...}}) untouched
    text = escape_braces(text)
    return text


def convert_body(body: str, slug_to_path: dict) -> str:
    body = convert_callouts(body)
    fences: list = []
    body = _protect(body, FENCE_RE, fences)
    inlines: list = []
    body = _protect(body, INLINE_CODE_RE, inlines)

    body = convert_html_block(body)
    body = convert_readme_image(body)
    body = convert_readme_anchor(body)
    body = convert_readme_table(body)
    body = rewrite_links(body, slug_to_path)
    body = sanitize_mdx(body)

    body = _restore(body, inlines)
    body = _restore(body, fences)
    return body


# ---------------------------------------------------------------------------
# tree walk
# ---------------------------------------------------------------------------

class Page:
    __slots__ = ("src", "out_path", "title", "description", "slug", "stem")

    def __init__(self, src, out_path, title, description, slug, stem):
        self.src = src
        self.out_path = out_path  # no extension, forward slashes
        self.title = title
        self.description = description
        self.slug = slug
        self.stem = stem


def read_order(d: Path):
    f = d / "_order.yaml"
    if f.exists():
        try:
            data = yaml.safe_load(f.read_text()) or []
            if isinstance(data, list):
                return [str(x) for x in data]
        except Exception:
            pass
    return None


def humanize(name: str) -> str:
    return re.sub(r"[-_]+", " ", name).strip().title()


def child_names(d: Path) -> set[str]:
    """Every name in `d` that could become a page or a group."""
    return {p.stem for p in d.glob("*.md")} | {p.name for p in d.iterdir() if p.is_dir()}


def claimed_slugs(docs_root: Path) -> set[str]:
    """Slugs that the _order.yaml traversal already serves somewhere.

    Used to tell a genuinely dropped page from a deliberate de-duplication:
    upstream keeps shallow copies of a dozen guides that _order.yaml
    intentionally omits because a deeper copy is canonical, and both carry the
    same slug. Restoring those would publish the same content at two URLs.
    """
    claimed: set[str] = set()

    def visit(md: Path):
        fm, body = split_frontmatter(md.read_text(encoding="utf-8", errors="replace"))
        if fm.get("hidden", False):
            return
        if md.name == "index.md" and not has_substantive_index_body(body):
            return
        claimed.add(str(fm.get("slug") or md.stem))

    def walk(d: Path):
        index = d / "index.md"
        if index.exists():
            visit(index)
        order = read_order(d)
        names = order if order is not None else sorted(child_names(d))
        for name in names:
            if name == "index":
                continue
            md = d / f"{name}.md"
            if md.exists():
                visit(md)
            sub = d / name
            if sub.is_dir():
                walk(sub)

    walk(docs_root)
    return claimed


def plan_rescues(docs_root: Path) -> dict[Path, list[str]]:
    """Find pages that _order.yaml drops and nothing else publishes.

    `_order.yaml` is an allowlist, and it used to fail silently in both
    directions: a file it never mentioned disappeared from the site, and an
    entry that matched no file matched nothing quietly. Together those lost 15
    Flow Campaigns guides (whose order file lists 2 of its 17 pages) and the
    Fulfilled Rewards Report, misspelled `fulfilled-reports-report` in its
    order file. All 16 are live URLs on the ReadMe site.

    Anything unlisted whose slug is already served stays dropped -- see
    claimed_slugs. Everything else is appended after the ordered names, and
    every decision is printed so the next omission is visible rather than
    silent.
    """
    def warn(msg: str):
        # stderr, so --dump-slug-map emits clean JSON on stdout.
        print(f"warning: {msg}", file=sys.stderr)

    if not docs_root.is_dir():
        return {}
    claimed = claimed_slugs(docs_root)
    rescues: dict[Path, list[str]] = {}
    for d in [docs_root, *sorted(p for p in docs_root.rglob("*") if p.is_dir())]:
        order = read_order(d)
        if order is None:
            continue
        present = child_names(d)
        for name in order:
            if name not in present:
                warn(f"{d}/_order.yaml lists '{name}', which matches nothing on disk")
        add = []
        for name in sorted(present - set(order) - {"index"}):
            md = d / f"{name}.md"
            if not md.exists():
                warn(f"{d}/{name}/ is unlisted in _order.yaml; left out")
                continue
            fm, _ = split_frontmatter(md.read_text(encoding="utf-8", errors="replace"))
            if fm.get("hidden", False):
                continue
            slug = str(fm.get("slug") or name)
            if slug in claimed:
                warn(f"{d}/{name}.md is unlisted; skipped, '{slug}' is served elsewhere")
                continue
            warn(f"{d}/{name}.md is unlisted in _order.yaml; appending it")
            add.append(name)
        if add:
            rescues[d.resolve()] = add
    return rescues


class Converter:
    def __init__(self, product_docs: Path, out: Path, dry_run: bool = False):
        self.docs_root = product_docs / "docs"
        self.out = out
        self.dry_run = dry_run
        self.pages: list[Page] = []
        self.slug_to_path: dict[str, str] = {}
        # Upstream slug -> URL prefix for a folder whose index.md was too thin to
        # publish. It has no page of its own here, but ReadMe served it as a real
        # category URL, so a redirect still needs somewhere to point.
        self.group_prefixes: dict[str, str] = {}
        self.rescues = plan_rescues(self.docs_root)

    def names_for(self, src_dir: Path, order):
        """Child names for a directory, in navigation order.

        Ordered names lead; pages that _order.yaml dropped without another copy
        to serve them follow, so an omission no longer deletes content.
        """
        if order is None:
            return sorted(child_names(src_dir))
        return [*order, *self.rescues.get(src_dir.resolve(), [])]

    def _page_meta(self, md: Path, out_rel: str):
        fm, _ = split_frontmatter(md.read_text(encoding="utf-8", errors="replace"))
        title = str(fm.get("title") or humanize(md.stem))
        desc = fm.get("excerpt") or fm.get("description") or ""
        desc = re.sub(r"\s+", " ", str(desc)).strip()
        if len(desc) > 300:
            desc = desc[:297].rstrip() + "..."
        slug = str(fm.get("slug") or md.stem)
        return title, desc, slug, fm.get("hidden", False)

    def collect(self, src_dir: Path, out_prefix: str, order, skip_names: set[str] | None = None):
        """Return a Mintlify navigation list for this dir."""
        skip_names = skip_names or set()
        if order is None:
            order = read_order(src_dir)
        names = self.names_for(src_dir, order)
        nav: list = []
        for name in names:
            if name in skip_names:
                continue
            md = src_dir / f"{name}.md"
            sub = src_dir / name
            if md.exists() and sub.is_dir():
                # The sibling page is this group's label and its landing page,
                # so its title names the child directory too.
                page = self._make_page(md, out_prefix)
                label = page.title if page else humanize(name)
                children = self.collect(
                    sub, f"{out_prefix}/{slugify_nav(label)}".strip("/"), read_order(sub)
                )
                if page and children:
                    nav.append({"group": page.title, "pages": children, "root": page.out_path})
                elif page:
                    nav.append(page.out_path)
            elif md.exists():
                page = self._make_page(md, out_prefix)
                if page:
                    nav.append(page.out_path)
            elif sub.is_dir():
                grp = self._make_group(sub, out_prefix)
                if grp:
                    nav.append(grp)
        return nav

    def _make_page(self, md: Path, out_prefix: str):
        title, desc, slug, hidden = self._page_meta(md, "")
        if hidden:
            return None
        out_rel = f"{out_prefix}/{slugify(md.stem)}".strip("/")
        page = Page(md, out_rel, title, desc, slug, md.stem)
        self.pages.append(page)
        self.slug_to_path[slug] = out_rel
        self.slug_to_path.setdefault(md.stem, out_rel)
        return page

    def _make_group(self, sub: Path, out_prefix: str):
        # Resolve the sidebar label first: it, not the upstream folder name,
        # supplies this level's URL segment. Reading index.md used to happen
        # after the prefix was built, which is why a folder called
        # "getting-started" served a group labelled "Extole Overview".
        index = sub / "index.md"
        group_title = humanize(sub.name)
        fm, body = {}, ""
        if index.exists():
            fm, body = split_frontmatter(index.read_text(encoding="utf-8", errors="replace"))
            if fm.get("title"):
                group_title = str(fm["title"])
        out_prefix2 = f"{out_prefix}/{slugify_nav(group_title)}".strip("/")
        pages_list: list = []
        root = None
        if index.exists():
            if has_substantive_index_body(body):
                root = self._make_page_named(index, out_prefix2, "index")
            else:
                if not fm.get("hidden", False):
                    self.group_prefixes[str(fm.get("slug") or sub.name)] = out_prefix2
                    self.group_prefixes.setdefault(sub.name, out_prefix2)
                if not self.dry_run:
                    # Remove a placeholder index emitted by an earlier run. The
                    # only write inside collect(), so --dump-slug-map skips it.
                    (self.out / f"{out_prefix2}/index.mdx").unlink(missing_ok=True)
        order = read_order(sub)
        pages_list.extend(self.collect(sub, out_prefix2, order, skip_names={"index"}))
        if not pages_list:
            # Every child was hidden or skipped. The root page has already been
            # registered by now, so returning None here wrote it to disk and left
            # it out of the navigation — live but unreachable. Keep the overview
            # as the group's only entry when it is real content, and drop the
            # group outright when there is nothing to show.
            if root:
                return {"group": group_title, "pages": [root.out_path]}
            return None
        group = {"group": group_title, "pages": pages_list}
        if root:
            group["root"] = root.out_path
        return group

    def _make_page_named(self, md: Path, out_prefix: str, out_name: str):
        title, desc, slug, hidden = self._page_meta(md, "")
        # `hidden` was read here but never acted on, unlike in _make_page, so a
        # group index marked hidden upstream was still written and served at its
        # URL while absent from the navigation — an unlisted but live page.
        if hidden:
            return None
        out_rel = f"{out_prefix}/{out_name}".strip("/")
        page = Page(md, out_rel, title, desc, slug, md.stem)
        self.pages.append(page)
        self.slug_to_path[slug] = out_rel
        self.slug_to_path.setdefault(md.stem, out_rel)
        # A group index inherits its folder's name as a link target: upstream
        # writes [Offer](doc:offer) for a page living at offer/index.md, whose
        # own stem is the useless "index". Without this the link cannot resolve
        # and falls through to a bare /offer.
        if out_name == "index":
            self.slug_to_path.setdefault(md.parent.name, out_rel)
        return page

    def write_pages(self):
        for page in self.pages:
            raw = page.src.read_text(encoding="utf-8", errors="replace")
            _, body = split_frontmatter(raw)
            body = convert_body(body, self.slug_to_path)
            fm_out = [f"title: {yaml_str(page.title)}"]
            if page.description:
                fm_out.append(f"description: {yaml_str(page.description)}")
            sidebar_title = NAV_SIDEBAR_TITLES.get(page.out_path)
            if sidebar_title:
                fm_out.append(f"sidebarTitle: {yaml_str(sidebar_title)}")
            content = "---\n" + "\n".join(fm_out) + "\n---\n\n" + body.lstrip("\n")
            dest = self.out / (page.out_path + ".mdx")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

SPEC_TABS = [
    ("Consumer to Extole API", "integration-consumer-to-extole.json"),
    ("Server to Extole API", "integration-server-to-extole.json"),
    ("Management API", "management.json"),
    ("Management Expert API", "management-expert.json"),
]

OPENAPI_METHODS = frozenset({"get", "post", "put", "delete", "patch", "head", "options", "trace"})

API_GETTING_STARTED = [
    "api-overview",
    "authentication-overview",
    "common-errors",
]

# Preserve the established ReadMe Technical Docs sidebar during conversion.
# These source directories are not part of that published navigation.
NAV_EXCLUDED_GROUPS = {
    "Technical Docs": {"components", "flow-campaign"},
}

# A root makes Mintlify render a group as a regular navigation link. Render these
# entries as headings and place their overview page first in the group instead.
NAV_GROUPS_WITHOUT_ROOT = {
    "Technical Docs": {"extole-ai"},
}

NAV_SIDEBAR_TITLES = {
    "technical/extole-ai-tools/index": "Overview",
}


def openapi_navigation_groups(spec: dict) -> list[dict]:
    """Generate ReadMe-equivalent tag groups for a Mintlify OpenAPI section.

    Mintlify's automatic OpenAPI navigation follows JSON insertion order. Group
    endpoints alphabetically by tag while preserving the source order of the
    operations within each tag. Explicit page references make that behavior
    stable in both the generated docs and the standalone sync command below.
    """
    operations_by_tag: dict[str, list[tuple[str, str]]] = {}
    for path, path_item in (spec.get("paths") or {}).items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method not in OPENAPI_METHODS or not isinstance(operation, dict):
                continue
            if operation.get("x-hidden") or operation.get("x-excluded"):
                continue
            for tag in operation.get("tags") or ["Endpoints"]:
                operations_by_tag.setdefault(str(tag), []).append((method, path))

    groups = []
    for tag in sorted(operations_by_tag, key=str.casefold):
        operations = operations_by_tag[tag]
        groups.append(
            {
                "group": tag,
                "pages": [f"{method.upper()} {path}" for method, path in operations],
            }
        )
    return groups


def api_reference_group(label: str, filename: str, spec: dict) -> dict:
    return {
        "group": label,
        # Mintlify serves the operation pages it generates from this spec under
        # /api-reference regardless of the tab name or where the bundle lives.
        # That prefix is why API_TAB_SLUG is "api-reference": the hand-written
        # getting-started pages have to share it or the tab splits in two. To
        # move both, set an explicit {"source": ..., "directory": ...} here and
        # change API_TAB_SLUG to match.
        "openapi": f"{API_TAB_SLUG}/{filename}",
        "pages": openapi_navigation_groups(spec),
    }


def sync_api_navigation(out: Path) -> int:
    """Refresh the API Reference tab from the OpenAPI bundles already in ``out``."""
    docs_path = out / "docs.json"
    docs = json.loads(docs_path.read_text(encoding="utf-8"))
    api_tab = next(
        (tab for tab in docs.get("navigation", {}).get("tabs", []) if tab.get("tab") == "API Reference"),
        None,
    )
    if not api_tab:
        raise ValueError("docs.json does not define an API Reference tab")

    getting_started = next(
        (group for group in api_tab.get("groups", []) if group.get("group") == "Getting Started"),
        None,
    )
    groups = [getting_started] if getting_started else []
    for label, filename in SPEC_TABS:
        spec_path = out / API_TAB_SLUG / filename
        if spec_path.exists():
            groups.append(api_reference_group(label, filename, json.loads(spec_path.read_text(encoding="utf-8"))))
    api_tab["groups"] = groups
    docs_path.write_text(json.dumps(docs, indent=2) + "\n", encoding="utf-8")
    return len(groups) - (1 if getting_started else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--product-docs", type=Path)
    ap.add_argument("--specification", type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument(
        "--sync-api-navigation",
        action="store_true",
        help="rewrite the API Reference navigation from local api-reference OpenAPI bundles",
    )
    ap.add_argument(
        "--migrate-images",
        action="store_true",
        help="download uncached remote MDX images into images/extole and rewrite their references",
    )
    ap.add_argument(
        "--dump-slug-map",
        action="store_true",
        help="print the upstream slug -> Mintlify path map as JSON and exit, writing nothing",
    )
    args = ap.parse_args()

    out = args.out.resolve()

    if args.sync_api_navigation:
        print(f"API specs synchronized: {sync_api_navigation(out)}")
        return

    if not args.product_docs and not args.specification:
        if not args.migrate_images:
            ap.error("--product-docs and --specification are required unless --migrate-images is used alone")
        assets, pages, failures = ImageMigrator(out).run()
        print(f"local image assets: {assets}")
        print(f"pages rewritten: {pages}")
        if failures:
            print(f"image failures: {failures}")
            raise SystemExit(1)
        return
    if not args.product_docs or not args.specification:
        ap.error("--product-docs and --specification must be provided together")

    if not args.dump_slug_map:
        removed = clean_generated_pages(out)
        if removed:
            print(f"stale generated pages removed: {removed}")
    conv = Converter(args.product_docs, out, dry_run=args.dump_slug_map)

    # top-level categories become tabs, in docs/_order.yaml order
    top_order = read_order(conv.docs_root) or sorted(
        p.name for p in conv.docs_root.iterdir() if p.is_dir()
    )

    # pass over pages happens lazily during collect; slug map is filled as we go,
    # so run collect first (fills slug map + page list), then write bodies.
    tabs = []
    for cat in top_order:
        cat_dir = conv.docs_root / cat
        if not cat_dir.is_dir():
            continue
        tab_prefix = TAB_SLUGS.get(cat, slugify(cat))
        groups = _as_groups(
            conv,
            cat_dir,
            tab_prefix,
            excluded_groups=NAV_EXCLUDED_GROUPS.get(cat, set()),
            groups_without_root=NAV_GROUPS_WITHOUT_ROOT.get(cat, set()),
        )
        tabs.append({"tab": humanize(cat), "groups": groups})

    # API reference tab combines its written getting-started guides with native OpenAPI specs.
    spec_out = out / API_TAB_SLUG
    if not args.dump_slug_map:
        spec_out.mkdir(parents=True, exist_ok=True)
    api_groups = []
    api_getting_started = []
    api_docs = args.product_docs / "reference" / "Getting Started"
    for name in API_GETTING_STARTED:
        source = api_docs / f"{name}.md"
        if not source.exists():
            continue
        page = conv._make_page_named(source, f"{API_TAB_SLUG}/getting-started", name)
        if page:
            api_getting_started.append(page.out_path)
    if api_getting_started:
        api_groups.append({"group": "Getting Started", "pages": api_getting_started})
    for label, fname in SPEC_TABS:
        src = args.specification / "openapi" / fname
        if not src.exists():
            continue
        spec = json.loads(src.read_text(encoding="utf-8"))
        add_union_titles(spec)
        if not args.dump_slug_map:
            (spec_out / fname).write_text(json.dumps(spec, indent=2), encoding="utf-8")
        api_groups.append(api_reference_group(label, fname, spec))
    tabs.append({"tab": "API Reference", "groups": api_groups})
    tabs.extend(read_extra_tabs(out, {t["tab"] for t in tabs}))

    if args.dump_slug_map:
        print(json.dumps(
            {"pages": conv.slug_to_path, "groups": conv.group_prefixes},
            indent=2, sort_keys=True,
        ))
        return

    conv.write_pages()

    assets, pages, unresolved = ImageMigrator(out).rewrite_cached()
    print(f"cached local image assets: {assets}")
    print(f"pages rewritten from image cache: {pages}")
    if unresolved:
        print(f"uncached remote image references: {unresolved}")

    redirects = read_redirects(out)
    docs_json = build_docs_json(tabs, redirects)
    (out / "docs.json").write_text(json.dumps(docs_json, indent=2) + "\n", encoding="utf-8")
    print(f"redirects carried over from {URL_MAP_FILE}: {len(redirects)}")

    write_home(out)

    if args.migrate_images:
        assets, pages, failures = ImageMigrator(out).run()
        print(f"local image assets: {assets}")
        print(f"pages rewritten: {pages}")
        if failures:
            print(f"image failures: {failures}")
            raise SystemExit(1)

    alt_pages, alt_images = normalize_local_image_alt_text(out)
    print(f"pages with contextual image alt text: {alt_pages}")
    print(f"contextual image alt text updates: {alt_images}")

    print(f"pages written: {len(conv.pages)}")
    print(f"api specs: {len(api_groups)}")
    print(f"tabs: {[t['tab'] for t in tabs]}")


def _as_groups(
    conv: Converter,
    cat_dir: Path,
    tab_prefix: str,
    excluded_groups: set[str] | None = None,
    groups_without_root: set[str] | None = None,
):
    """Build the groups[] for a category tab. Leaf pages directly under the
    category are gathered into an 'Overview' group; subdirs become groups."""
    order = conv.names_for(cat_dir, read_order(cat_dir))
    excluded_groups = excluded_groups or set()
    groups_without_root = groups_without_root or set()
    groups = []
    loose: list = []
    for name in order:
        if name in excluded_groups:
            continue
        md = cat_dir / f"{name}.md"
        sub = cat_dir / name
        if md.exists() and sub.is_dir():
            page = conv._make_page(md, tab_prefix)
            label = page.title if page else humanize(name)
            children = conv.collect(
                sub, f"{tab_prefix}/{slugify_nav(label)}".strip("/"), read_order(sub)
            )
            if page and children:
                groups.append({"group": page.title, "pages": children, "root": page.out_path})
            elif page:
                loose.append(page.out_path)
        elif md.exists():
            page = conv._make_page(md, tab_prefix)
            if page:
                loose.append(page.out_path)
        elif sub.is_dir():
            grp = conv._make_group(sub, tab_prefix)
            if grp:
                if name in groups_without_root:
                    root = grp.pop("root", None)
                    if root:
                        grp["pages"].insert(0, root)
                groups.append(grp)
    if loose:
        groups.insert(0, {"group": "Overview", "pages": loose})
    return groups


URL_MAP_FILE = "url-map.json"


def clean_generated_pages(out: Path) -> int:
    """Delete the .mdx pages under the generated tab roots, then prune empties.

    The converter is overwrite-only, so without this a page that upstream
    renamed or deleted lingers forever: it stays on disk serving its old URL
    while disappearing from the navigation. Renaming a folder used to leave the
    whole old tree behind as a silent duplicate.

    Only `.mdx` under the tab roots is touched. The OpenAPI bundles are left for
    the spec copy to overwrite, so an unreferenced scratch .json in that folder
    survives, and every non-generated file — index.mdx, images/, public/,
    scripts/, docs.json, url-map.json — is outside the tab roots entirely.
    """
    roots = [out / slug for slug in (*TAB_SLUGS.values(), API_TAB_SLUG)]
    removed = 0
    for root in roots:
        if not root.is_dir():
            continue
        for page in root.rglob("*.mdx"):
            page.unlink()
            removed += 1
        for d in sorted(root.rglob("*"), key=lambda p: -len(p.parts)):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
        if not any(root.iterdir()):
            root.rmdir()
    return removed


def read_redirects(out: Path) -> list:
    """Load the checked-in old -> new URL map.

    Redirects used to be a literal in this function, which meant a regeneration
    silently dropped any that had been added to docs.json by hand. Keeping them
    in url-map.json makes them survive, and makes a URL change reviewable as a
    diff to that file.

    Two lists live there. `redirects` is hand-maintained and small.
    `readme_redirects` is the ~800-entry ReadMe map, regenerated wholesale by
    build_readme_redirects.py, kept separate so the curated entries stay
    reviewable and win any collision.
    """
    f = out / URL_MAP_FILE
    if not f.exists():
        return []
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(data, dict):
        data = {"redirects": data}

    def valid(key):
        entries = data.get(key)
        return [
            e for e in entries
            if isinstance(e, dict) and isinstance(e.get("source"), str)
            and isinstance(e.get("destination"), str)
        ] if isinstance(entries, list) else []

    curated = valid("redirects")
    claimed = {e["source"] for e in curated}
    return curated + [e for e in valid("readme_redirects") if e["source"] not in claimed]


def read_extra_tabs(out: Path, generated: set[str]) -> list:
    """Keep tabs in docs.json that this script does not generate.

    The navigation is rebuilt from scratch on every run from the upstream
    categories plus API Reference, so News -- hand-assembled from the ReadMe
    changelog and newsletters, with no upstream source -- disappeared on the
    next conversion. Its .mdx files survive clean_generated_pages, which only
    touches the tab roots, so the pages stayed on disk and served nothing.
    Same failure mode the redirects had before url-map.json.
    """
    f = out / "docs.json"
    if not f.exists():
        return []
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    tabs = (data.get("navigation") or {}).get("tabs")
    if not isinstance(tabs, list):
        return []
    return [t for t in tabs if isinstance(t, dict) and t.get("tab") not in generated]


def build_docs_json(tabs, redirects=None):
    return {
        "$schema": "https://mintlify.com/docs.json",
        "theme": "mint",
        "name": "Extole Documentation",
        "description": "Guides, product documentation, and API reference for the Extole platform.",
        "redirects": redirects or [],
        "colors": {
            "primary": "#ee0049",
            "light": "#ee0049",
            "dark": "#ee0049",
        },
        "logo": {
            "light": "/extole-logo.png",
            "dark": "/extole-logo.png",
            "href": "/",
        },
        "favicon": {
            "light": "/Extole-icon-bug.svg",
            "dark": "/Extole-icon-bug.svg",
        },
        "navigation": {"tabs": tabs},
        "navbar": {
            "links": [
                {"label": "GitHub", "href": "https://github.com/extole"},
                {"label": "My Extole Login", "href": "https://my.extole.com"},
            ],
        },
        "contextual": {"options": ["copy", "view", "chatgpt", "claude", "mcp"]},
        "footer": {"socials": {"github": "https://github.com/extole"}},
    }


def write_home(out: Path):
    # The landing (index.mdx) is a bespoke, hand-authored page that mirrors the
    # docs.extole.com home; it is committed and not derived from source, so
    # preserve it across regenerations. Only write the fallback when absent.
    dest = out / "index.mdx"
    if dest.exists():
        return
    home = """---
title: "Extole Documentation"
description: "Guides, product documentation, and API reference for the Extole platform."
---

<CardGroup cols={2}>
  <Card title="Guides" icon="book-open" href="/guides">
    How-to guides for programs, audiences, rewards, and reporting.
  </Card>
  <Card title="Product Docs" icon="rectangle-list" href="/product">
    Feature and product documentation.
  </Card>
  <Card title="Technical Docs" icon="code" href="/technical">
    Integration, data, and technical reference.
  </Card>
  <Card title="API Reference" icon="terminal" href="/api">
    Consumer, Server, and Management REST APIs.
  </Card>
</CardGroup>
"""
    dest.write_text(home, encoding="utf-8")


if __name__ == "__main__":
    main()
