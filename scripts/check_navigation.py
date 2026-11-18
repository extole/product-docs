#!/usr/bin/env python3
"""Check that every page is reachable and that file paths mirror navigation.

Mintlify serves a page at its file path whether or not docs.json lists it, and
`mint validate` only reports a navigation entry whose file is missing. This
reports the other two defects:

  UNLISTED   an .mdx page under a content directory that no navigation entry
             names, so it serves at its URL but appears in no sidebar or search
  MISMATCH   a listed page whose directory is not the tab directory followed by
             the slugified group chain it sits under

and, for completeness, MISSING for a navigation entry with no file.

Hidden groups are exempt from the mirroring check: they have no sidebar
position to mirror, which is how the runbooks are served.

Usage:
  python3 scripts/check_navigation.py            # from the repository root
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

CONTENT_DIRECTORIES = ("guides", "product", "technical", "news", "runbooks", "api-reference")
TAB_DIRECTORIES = {
    "Guides": "guides",
    "Product Docs": "product",
    "Technical Docs": "technical",
    "News": "news",
    "API Reference": "api-reference",
}
HTTP_METHODS = ("GET ", "POST ", "PUT ", "DELETE ", "PATCH ")


def slugify(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower().replace("&", "and")).strip("-")


def listed_pages(navigation: dict) -> list[tuple[str, list[str], str, bool]]:
    pages: list[tuple[str, list[str], str, bool]] = []

    def walk(items, tab: str, chain: list[str], hidden: bool) -> None:
        for item in items:
            if isinstance(item, str):
                if not item.startswith(HTTP_METHODS):
                    pages.append((tab, chain, item, hidden))
            elif isinstance(item, dict) and "group" in item:
                group_hidden = hidden or bool(item.get("hidden"))
                group_chain = chain + [item["group"]]
                if "root" in item:
                    pages.append((tab, group_chain, item["root"], group_hidden))
                walk(item.get("pages", []), tab, group_chain, group_hidden)
            elif isinstance(item, dict) and "pages" in item:
                walk(item["pages"], tab, chain, hidden)

    for tab in navigation["tabs"]:
        walk(tab.get("groups", tab.get("pages", [])), tab["tab"], [], False)
    return pages


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    navigation = json.loads((root / "docs.json").read_text())["navigation"]
    pages = listed_pages(navigation)

    listed = {page for _, _, page, _ in pages}
    on_disk = {
        str(path.relative_to(root))[: -len(".mdx")]
        for directory in CONTENT_DIRECTORIES
        for path in (root / directory).rglob("*.mdx")
    }

    findings: list[str] = []
    for page in sorted(on_disk - listed):
        findings.append(f"UNLISTED  {page}")
    for page in sorted(listed - on_disk):
        findings.append(f"MISSING   {page}")
    for tab, chain, page, hidden in pages:
        if hidden or page not in on_disk:
            continue
        tab_directory = TAB_DIRECTORIES.get(tab)
        if tab_directory is None:
            continue
        expected = "/".join([tab_directory, *(slugify(group) for group in chain)])
        parent = "/".join([tab_directory, *(slugify(group) for group in chain[:-1])])
        directory = str(Path(page).parent)
        if directory not in (expected, parent):
            findings.append(f"MISMATCH  {page}  (nav: {tab} > {' > '.join(chain)})")

    for finding in findings:
        print(finding)
    print(f"{len(on_disk)} pages on disk, {len(listed)} listed, {len(findings)} findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
