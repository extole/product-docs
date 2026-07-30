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
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

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


def _protect(text: str, pattern: re.Pattern, store: list, mark: str = "\x00") -> str:
    def repl(m):
        store.append(m.group(0))
        return f"{mark}{len(store) - 1}{mark}"

    return pattern.sub(repl, text)


def _restore(text: str, store: list, mark: str = "\x00") -> str:
    for i, chunk in enumerate(store):
        text = text.replace(f"{mark}{i}{mark}", chunk)
    return text


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
    text = re.sub(r"\]\(ref:([^)\s]+)\)", "](/api-reference)", text)
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


class Converter:
    def __init__(self, product_docs: Path, out: Path):
        self.docs_root = product_docs / "docs"
        self.out = out
        self.pages: list[Page] = []
        self.slug_to_path: dict[str, str] = {}

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
        if order is None:
            names = sorted(
                [p.stem for p in src_dir.glob("*.md")]
                + [p.name for p in src_dir.iterdir() if p.is_dir()]
            )
        else:
            names = order
        nav: list = []
        for name in names:
            if name in skip_names:
                continue
            md = src_dir / f"{name}.md"
            sub = src_dir / name
            if md.exists() and sub.is_dir():
                page = self._make_page(md, out_prefix)
                children = self.collect(sub, f"{out_prefix}/{slugify(name)}", read_order(sub))
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
        out_prefix2 = f"{out_prefix}/{slugify(sub.name)}".strip("/")
        index = sub / "index.md"
        group_title = humanize(sub.name)
        pages_list: list = []
        root = None
        if index.exists():
            fm, body = split_frontmatter(index.read_text(encoding="utf-8", errors="replace"))
            if fm.get("title"):
                group_title = str(fm["title"])
            if has_substantive_index_body(body):
                root = self._make_page_named(index, out_prefix2, "index")
            else:
                # Remove a placeholder index emitted by an earlier conversion run.
                (self.out / f"{out_prefix2}/index.mdx").unlink(missing_ok=True)
        order = read_order(sub)
        pages_list.extend(self.collect(sub, out_prefix2, order, skip_names={"index"}))
        if not pages_list:
            return None
        group = {"group": group_title, "pages": pages_list}
        if root:
            group["root"] = root.out_path
        return group

    def _make_page_named(self, md: Path, out_prefix: str, out_name: str):
        title, desc, slug, hidden = self._page_meta(md, "")
        out_rel = f"{out_prefix}/{out_name}".strip("/")
        page = Page(md, out_rel, title, desc, slug, md.stem)
        self.pages.append(page)
        self.slug_to_path[slug] = out_rel
        self.slug_to_path.setdefault(md.stem, out_rel)
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
    "technical-docs/extole-ai/index": "Overview",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--product-docs", required=True, type=Path)
    ap.add_argument("--specification", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    out = args.out.resolve()

    # clean previously generated content dirs (keep repo scaffolding)
    conv = Converter(args.product_docs, out)

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
        tab_prefix = slugify(cat)
        groups = _as_groups(
            conv,
            cat_dir,
            tab_prefix,
            excluded_groups=NAV_EXCLUDED_GROUPS.get(cat, set()),
            groups_without_root=NAV_GROUPS_WITHOUT_ROOT.get(cat, set()),
        )
        tabs.append({"tab": humanize(cat), "groups": groups})

    # API reference tab combines its written getting-started guides with native OpenAPI specs.
    spec_out = out / "api-reference"
    spec_out.mkdir(parents=True, exist_ok=True)
    api_groups = []
    api_getting_started = []
    api_docs = args.product_docs / "reference" / "Getting Started"
    for name in API_GETTING_STARTED:
        source = api_docs / f"{name}.md"
        if not source.exists():
            continue
        page = conv._make_page_named(source, "api-reference/getting-started", name)
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
        (spec_out / fname).write_text(json.dumps(spec, indent=2), encoding="utf-8")
        api_groups.append({"group": label, "openapi": f"api-reference/{fname}"})
    tabs.append({"tab": "API Reference", "groups": api_groups})

    conv.write_pages()

    docs_json = build_docs_json(tabs)
    (out / "docs.json").write_text(json.dumps(docs_json, indent=2) + "\n", encoding="utf-8")

    write_home(out)

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
    order = read_order(cat_dir)
    if order is None:
        order = sorted(
            [p.stem for p in cat_dir.glob("*.md")]
            + [p.name for p in cat_dir.iterdir() if p.is_dir()]
        )
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
            children = conv.collect(sub, f"{tab_prefix}/{slugify(name)}", read_order(sub))
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


def build_docs_json(tabs):
    return {
        "$schema": "https://mintlify.com/docs.json",
        "theme": "mint",
        "name": "Extole Documentation",
        "description": "Guides, product documentation, and API reference for the Extole platform.",
        "redirects": [
            {
                "source": "/technical-docs/extole-ai/extole-mcp",
                "destination": "/technical-docs/extole-ai/extole-mcp/index",
            },
            {
                "source": "/technical-docs/extole-mcp",
                "destination": "/technical-docs/extole-ai/extole-mcp/index",
            },
            {
                "source": "/technical-docs/extole-ai/extole-cli",
                "destination": "/technical-docs/extole-ai/extole-cli/index",
            },
            {
                "source": "/technical-docs/extole-cli",
                "destination": "/technical-docs/extole-ai/extole-cli/index",
            },
        ],
        "colors": {"primary": "#ee0049"},
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
  <Card title="Product Docs" icon="rectangle-list" href="/product-docs">
    Feature and product documentation.
  </Card>
  <Card title="Technical Docs" icon="code" href="/technical-docs">
    Integration, data, and technical reference.
  </Card>
  <Card title="API Reference" icon="terminal" href="/api-reference">
    Consumer, Server, and Management REST APIs.
  </Card>
</CardGroup>
"""
    dest.write_text(home, encoding="utf-8")


if __name__ == "__main__":
    main()
