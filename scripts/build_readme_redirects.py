#!/usr/bin/env python3
"""Generate the ReadMe -> Mintlify redirect map.

Mintlify is moving onto docs.extole.com, the domain ReadMe serves today, so
every live ReadMe URL becomes a request against this site the moment DNS
changes. ReadMe URLs are flat (/docs/integrating-with-extole); ours are the
page's navigation breadcrumb (/technical/integration-overview/...), so nothing
lines up without an explicit map.

Three families, each derived rather than hand-written:

  /docs/<slug>      the upstream `slug` frontmatter, or the filename stem --
                    exactly what the converter records in its slug map. Folder
                    landing pages too thin to publish here resolve to the first
                    page of the group they became.
  /reference/<id>   a lowercased operationId. Mintlify generates those pages
                    from the OpenAPI bundles at /api-reference/<tag>/<summary>,
                    so the destination is derived the same way.
  /changelog/...    already covered by the hand-maintained redirects.

Usage:
  python scripts/build_readme_redirects.py --readme-sitemap readme-sitemap.xml \
      --slug-map slug-map.json --out . [--write]

Without --write it only reports coverage. Re-run it immediately before the DNS
cutover: ReadMe stays editable until then, and a page added there afterwards
would not be in this map.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from convert_from_product_docs import SPEC_TABS, slugify  # noqa: E402

URL_MAP_FILE = "url-map.json"
GENERATED_KEY = "readme_redirects"

# Where a ReadMe slug matched more than one candidate page. Chosen by Paul on
# 2026-08-12; the generator asserts it never derives a conflicting destination.
OVERRIDES = {
    "/docs/advocate-tiers": "/guides/audiences-and-segmentation/advocate-tiers",
    "/docs/ada-compliance": "/product/product-overview/security-and-compliance/ada-compliance",
    "/docs/creative-image-asset-guide":
        "/product/product-overview/integration-and-launch/creative-content/creative-image-asset-guide",
    "/docs/webhooks": "/technical/platform-integrations/webhooks",
    "/docs/international-programs": "/product/product-overview/programs/international-programs",
}

# ReadMe appends -1/_2 when two pages want the same slug. The duplicate holds
# the same operation, so it follows the original.
DEDUP_SUFFIX_RE = re.compile(r"[-_]\d+$")


def mintlify_slug(text: str) -> str:
    """Slugify the way Mintlify names a generated operation page.

    It drops apostrophes rather than treating them as separators, so
    "a person's profile" becomes persons-profile, not person-s-profile.
    """
    return slugify(text.replace("'", "").replace("’", ""))


def read_sitemap(path: Path) -> list[str]:
    root = ElementTree.parse(path).getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [el.text.strip() for el in root.iterfind(".//s:loc", ns) if el.text]


def nav_pages(node) -> list[str]:
    """Every page path in docs.json navigation, in sidebar order."""
    out: list[str] = []
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, list):
        for item in node:
            out.extend(nav_pages(item))
    elif isinstance(node, dict):
        if isinstance(node.get("root"), str):
            out.append(node["root"])
        for key in ("tabs", "groups", "pages"):
            if key in node:
                out.extend(nav_pages(node[key]))
    return out


def canonical(path: str) -> str:
    """Mintlify serves a folder's index.mdx at the folder URL itself."""
    return path[: -len("/index")] if path.endswith("/index") else path


def operation_destinations(api_dir: Path):
    """Lowercased operationId -> its generated page, and tag -> first operation.

    The tag map covers ReadMe's own section landing pages (/reference/events-1),
    which are categories rather than operations -- the same case as a /docs
    category, and resolved the same way: the first page inside.

    Only the bundles in SPEC_TABS are read. Globbing the folder instead meant an
    unpublished spec sitting there could supply a destination for a page this
    site does not serve.
    """
    dest: dict[str, str] = {}
    tag_first: dict[str, str] = {}
    for _, filename in SPEC_TABS:
        bundle = api_dir / filename
        if not bundle.exists():
            continue
        try:
            spec = json.loads(bundle.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for methods in (spec.get("paths") or {}).values():
            if not isinstance(methods, dict):
                continue
            for op in methods.values():
                if not isinstance(op, dict):
                    continue
                op_id, tags = op.get("operationId"), op.get("tags")
                summary = op.get("summary")
                if not (op_id and tags and summary):
                    continue
                tag = mintlify_slug(str(tags[0]))
                page = f"/api-reference/{tag}/{mintlify_slug(str(summary))}"
                dest.setdefault(str(op_id).lower(), page)
                tag_first.setdefault(tag, page)
    return dest, tag_first


def build(readme_urls, slug_map, docs_json, api_dir):
    pages, groups = slug_map["pages"], slug_map["groups"]
    ordered = nav_pages(docs_json["navigation"])
    live = {canonical(p) for p in ordered}
    operations, tag_first = operation_destinations(api_dir)

    first_in_group = {}
    for prefix in groups.values():
        for page in ordered:
            if page.startswith(prefix + "/"):
                first_in_group.setdefault(prefix, page)
                break

    redirects, unresolved, stats = {}, [], {}

    def bump(kind):
        stats[kind] = stats.get(kind, 0) + 1

    for url in readme_urls:
        path = "/" + url.split("//", 1)[-1].split("/", 1)[-1] if "//" in url else url
        path = re.sub(r"^https?://[^/]+", "", url).rstrip("/")
        if not path or path.startswith("/changelog"):
            continue  # handled by the hand-maintained redirects
        family, _, slug = path.lstrip("/").partition("/")
        if not slug:
            continue

        if path in OVERRIDES:
            redirects[path] = OVERRIDES[path]
            bump("override")
            continue

        if family == "docs":
            if slug in pages:
                redirects[path] = "/" + pages[slug]
                bump("page")
            elif slug in groups and groups[slug] in first_in_group:
                redirects[path] = "/" + first_in_group[groups[slug]]
                bump("group")
            else:
                unresolved.append(path)
        elif family == "reference":
            key = slug.lower()
            if key in pages:
                redirects[path] = "/" + pages[key]
                bump("api-guide")
            elif key in operations:
                redirects[path] = operations[key]
                bump("operation")
            elif DEDUP_SUFFIX_RE.sub("", key) in operations:
                redirects[path] = operations[DEDUP_SUFFIX_RE.sub("", key)]
                bump("operation-duplicate")
            elif DEDUP_SUFFIX_RE.sub("", key) in tag_first:
                redirects[path] = tag_first[DEDUP_SUFFIX_RE.sub("", key)]
                bump("api-section")
            else:
                unresolved.append(path)

    # An override exists because deriving the destination is ambiguous. If a
    # derivation ever agrees or disagrees, say so rather than silently picking.
    for source, chosen in OVERRIDES.items():
        slug = source.split("/")[-1]
        derived = "/" + pages[slug] if slug in pages else None
        if derived and derived != chosen:
            print(f"note: {source} overrides the derived {derived}", file=sys.stderr)

    dangling = sorted(
        d for d in set(redirects.values())
        if not d.startswith("/api-reference/") and canonical(d).lstrip("/") not in live
    )
    return redirects, unresolved, stats, dangling


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--readme-sitemap", required=True, type=Path)
    ap.add_argument("--slug-map", required=True, type=Path)
    ap.add_argument("--out", type=Path, default=Path("."))
    ap.add_argument("--mintlify-sitemap", type=Path,
                    help="check generated API destinations against a live sitemap")
    ap.add_argument("--write", action="store_true",
                    help=f"write the result into {URL_MAP_FILE}")
    args = ap.parse_args()

    out = args.out.resolve()
    docs_json = json.loads((out / "docs.json").read_text(encoding="utf-8"))
    slug_map = json.loads(args.slug_map.read_text(encoding="utf-8"))
    urls = read_sitemap(args.readme_sitemap)

    redirects, unresolved, stats, dangling = build(
        urls, slug_map, docs_json, out / "api-reference"
    )

    print(f"ReadMe URLs in sitemap: {len(urls)}")
    for kind in sorted(stats):
        print(f"  {kind}: {stats[kind]}")
    print(f"redirects generated: {len(redirects)}")

    if args.mintlify_sitemap:
        live = {canonical(re.sub(r"^https?://[^/]+", "", u).rstrip("/"))
                for u in read_sitemap(args.mintlify_sitemap)}
        missing = sorted(d for d in set(redirects.values()) if canonical(d) not in live)
        print(f"destinations absent from the Mintlify sitemap: {len(missing)}")
        for d in missing[:20]:
            print(f"  MISSING {d}")

    if dangling:
        print(f"destinations with no page in docs.json: {len(dangling)}")
        for d in dangling[:20]:
            print(f"  DANGLING {d}")
    if unresolved:
        print(f"unresolved ReadMe URLs: {len(unresolved)}")
        for u in unresolved[:40]:
            print(f"  UNRESOLVED {u}")

    if args.write:
        f = out / URL_MAP_FILE
        data = json.loads(f.read_text(encoding="utf-8"))
        data[GENERATED_KEY] = [
            {"source": s, "destination": redirects[s]} for s in sorted(redirects)
        ]
        f.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {len(redirects)} entries to {f.name} under '{GENERATED_KEY}'")

    if unresolved or dangling:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
