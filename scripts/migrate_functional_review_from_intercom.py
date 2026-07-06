#!/usr/bin/env python3
"""Export the six Functional Review Intercom runbooks into product-docs markdown."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

INTERCOM_VERSION = "2.14"
TARGET_DIR = "docs/Guides/functional-review"

# Slug -> Intercom article id (from Help Center; Overview ~18427874)
FUNCTIONAL_REVIEW_ARTICLES: list[tuple[str, str]] = [
    ("functional-review-overview", "18427874"),
    ("functional-review-input-runtime-event-validation", "18427875"),
    ("functional-review-conversion-reward-validation", "18427876"),
    ("functional-review-email-webhook-side-effect-validation", "18427877"),
    ("functional-review-report-execution-runtime-checks", "18427878"),
    ("functional-review-terms-rewards-and-configuration-alignment", "18427879"),
]


def slugify(text: str) -> str:
    value = text.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def load_dotenv() -> None:
    for candidate in (
        Path.home() / "src/tech/code/ai/.env",
        Path.home() / "Documents/work repos/ai-tools/ai-tools.env",
        Path("ai-tools.env"),
    ):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.removeprefix("export ").strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


def http_json(url: str, token: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Intercom-Version": INTERCOM_VERSION,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, context=ssl.create_default_context(), timeout=60) as response:
        payload = json.load(response)
    if not isinstance(payload, dict):
        raise RuntimeError(f"Unexpected payload from {url}")
    return payload


class IntercomHtmlToMarkdown(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.list_depth = 0
        self._link_href = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key: value or "" for key, value in attrs}
        if tag in {"h1", "h2", "h3", "h4"}:
            level = int(tag[1])
            self.parts.append("\n" + ("#" * level) + " ")
        elif tag == "p":
            self.parts.append("\n\n")
        elif tag == "br":
            self.parts.append("\n")
        elif tag in {"ol", "ul"}:
            self.list_depth += 1
            self.parts.append("\n")
        elif tag == "li":
            prefix = "  " * max(self.list_depth - 1, 0)
            self.parts.append(f"\n{prefix}- ")
        elif tag == "a":
            self._link_href = attrs_dict.get("href", "")
            self.parts.append("[")
        elif tag == "img":
            alt = attrs_dict.get("alt", "image")
            src = attrs_dict.get("src", "")
            if src:
                self.parts.append(f"![{alt}]({src})")
        elif tag in {"b", "strong"}:
            self.parts.append("**")
        elif tag in {"i", "em"}:
            self.parts.append("*")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"h1", "h2", "h3", "h4"}:
            self.parts.append("\n")
        elif tag == "a":
            self.parts.append(f"]({self._link_href})")
        elif tag in {"b", "strong", "i", "em"}:
            self.parts.append("**" if tag in {"b", "strong"} else "*")
        elif tag in {"ol", "ul"}:
            self.list_depth = max(0, self.list_depth - 1)
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def markdown(self) -> str:
        text = "".join(self.parts)
        text = html.unescape(text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip() + "\n"


def article_markdown(full_article: dict) -> str:
    markdown = full_article.get("body_markdown")
    if isinstance(markdown, str) and markdown.strip():
        return markdown.strip() + "\n"
    body = full_article.get("body")
    if isinstance(body, str) and body.strip():
        parser = IntercomHtmlToMarkdown()
        parser.feed(body)
        return parser.markdown()
    raise RuntimeError(f"No body for article {full_article.get('title')}")


def write_page(repo_root: Path, slug: str, title: str, markdown: str, intercom_id: str) -> Path:
    target_dir = repo_root / TARGET_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{slug}.md"
    excerpt_source = re.sub(r"\s+", " ", markdown.split("\n", 1)[0]).strip()
    excerpt = excerpt_source[:240] if excerpt_source else title
    front_matter = (
        "---\n"
        f"title: {json.dumps(title)}\n"
        f"slug: {slug}\n"
        f"excerpt: {json.dumps(excerpt)}\n"
        "hidden: true\n"
        f"intercom_source_id: {intercom_id}\n"
        "---\n\n"
    )
    target.write_text(front_matter + markdown, encoding="utf-8")
    return target


def fetch_by_slug(token: str) -> dict[str, dict]:
    by_slug: dict[str, dict] = {}
    page = 1
    while True:
        query = urllib.parse.urlencode({"per_page": 50, "page": page})
        payload = http_json(f"https://api.intercom.io/articles?{query}", token)
        for item in payload.get("data", []):
            title = str(item.get("title", "")).strip()
            by_slug[slugify(title)] = item
        total_pages = payload.get("pages", {}).get("total_pages", page)
        if page >= total_pages:
            break
        page += 1
    return by_slug


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--product-docs-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    token = os.environ.get("INTERCOM_ACCESS_TOKEN", "")
    if not token:
        print("INTERCOM_ACCESS_TOKEN is required", file=sys.stderr)
        return 1
    if not args.product_docs_root.is_dir():
        print(f"product-docs root not found: {args.product_docs_root}", file=sys.stderr)
        return 1

    articles_by_slug = fetch_by_slug(token)
    written: list[str] = []
    missing: list[str] = []

    for slug, article_id in FUNCTIONAL_REVIEW_ARTICLES:
        summary = articles_by_slug.get(slug)
        if summary is None:
            summary = {"id": article_id}
        full = http_json(f"https://api.intercom.io/articles/{summary['id']}", token)
        title = str(full.get("title", slug))
        markdown = article_markdown(full)
        if args.dry_run:
            written.append(f"{slug} ({title}) id={summary['id']}")
            continue
        path = write_page(args.product_docs_root, slug, title, markdown, str(summary["id"]))
        written.append(str(path.relative_to(args.product_docs_root)))

    if missing:
        print("Missing Intercom articles:", ", ".join(missing), file=sys.stderr)
    print(json.dumps({"written": written, "missing": missing}, indent=2))
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
