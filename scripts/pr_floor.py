"""Deterministic floor checks F1–F15 for the docs pull request judge (RUBRIC v2).

Runs before the model. Needs no secrets except optional preview host calls (F12/F13).
Output is JSON the judge reads and may override the model's proposed verdict.
"""

from __future__ import annotations

import json
import re
import subprocess
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

from closing_references import armed_references

REQUIRED_CHECK = "validate"
MECHANISM_PREFIXES = (
    ".mintlify/AGENTS.md",
    "AGENTS.md",
    ".agents/",
    ".github/",
    "scripts/",
    "url-map.json",
)
CONTENT_PREFIXES = ("guides/", "product/", "technical/", "news/", "runbooks/")
GENERATED_PATH = re.compile(r"^api-reference/.*\.json$")
MDX_PATH = re.compile(r"^(guides|product|technical|news|runbooks)/.+\.mdx$")

# Draft internal-only term list (README §11.4); the docs owner edits via rubric changes.
INTERNAL_TERM_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("show-expert", re.compile(r"\bShow Expert\b", re.I)),
    ("expert-setting", re.compile(r"\bExpert setting\b", re.I)),
    ("version-label", re.compile(r"(?<![/\w])\bv\d+(?:\.\d+)?\b(?![/\w])")),
    ("ticket-key", re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b")),
    ("slack-link", re.compile(r"https?://[^\s]*slack\.com/", re.I)),
    ("internal-repo", re.compile(r"\bextole/[a-z0-9_-]+\b", re.I)),
    ("client-id", re.compile(r"client_id=\d{6,}")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
]

BODY_LINE_PATTERNS = {
    "question": re.compile(r"^Question:\s*\S", re.MULTILINE),
    "claims": re.compile(r"^Claims:\s*$", re.MULTILINE),
    "changes_live": re.compile(r"^Changes live text:", re.MULTILINE),
    "replay": re.compile(r"^Replay:", re.MULTILINE),
    "placement": re.compile(r"^Placement:", re.MULTILINE),
}
# M1 adds the template; until then F11 only informs.
BODY_TEMPLATE_SINCE = "2099-01-01T00:00:00Z"

IMAGE_PATH = re.compile(r"/images/\S+")
MINTLIFY_PREVIEW_HOST = re.compile(r"https://(extole-[a-z0-9-]+\.mintlify\.site)")
FRONTMATTER_TITLE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)

REMOTE_IMAGE = re.compile(r"!\[[^\]]*\]\(\s*https?://", re.I)
EXPIRES_PARAM = re.compile(r"expires=", re.I)
ABSOLUTE_DOCS_LINK = re.compile(r"https?://docs\.extole\.com/", re.I)

SECTION_HEADING = re.compile(r"^\+#{1,6}\s+(.+)$", re.MULTILINE)
ADDED_LINE = re.compile(r"^\+(?!\+\+\+)(.*)$", re.MULTILINE)


@dataclass
class FloorResult:
    validate_conclusion: str | None = None
    validate_failed: bool = False
    validate_failed_on_main: bool = False
    already_on_main: bool = False
    navigation_send_back: list[str] = field(default_factory=list)
    broken_links_send_back: list[str] = field(default_factory=list)
    internal_terms: list[str] = field(default_factory=list)
    remote_image_or_link: list[str] = field(default_factory=list)
    closing_keyword_hits: list[str] = field(default_factory=list)
    literals_changed: list[str] = field(default_factory=list)
    contention_same_section: dict[str, list[int]] = field(default_factory=dict)
    contention_same_page: dict[str, list[int]] = field(default_factory=dict)
    merge_conflicts: bool = False
    commits_behind_main: int = 0
    pages_changed_on_main: list[str] = field(default_factory=list)
    corpus_duplicates: list[str] = field(default_factory=list)
    body_lines_missing: list[str] = field(default_factory=list)
    body_lines_required: bool = False
    reach_exact_failures: list[str] = field(default_factory=list)
    reach_search: list[dict[str, Any]] = field(default_factory=list)
    mechanism_paths: list[str] = field(default_factory=list)
    fork: bool = False
    diff_truncated: bool = False
    preview_unreachable: bool = False
    tool_failures: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run(argv: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, capture_output=True, text=True, encoding="utf-8", errors="replace", check=check,
    )


def gh_json(args: list[str]) -> Any:
    return json.loads(run(["gh"] + args).stdout or "null")


def added_text_from_patch(patch: str) -> str:
    return "\n".join(match.group(1) for match in ADDED_LINE.finditer(patch or ""))


def section_headings_from_patch(patch: str) -> set[str]:
    return {match.group(1).strip() for match in SECTION_HEADING.finditer(patch or "")}


def validate_check(repo: str, sha: str) -> tuple[str | None, bool]:
    try:
        runs = gh_json([
            "api", f"repos/{repo}/commits/{sha}/check-runs", "--paginate",
            "--jq", f'[.check_runs[] | select(.name == "{REQUIRED_CHECK}")]',
        ])
    except Exception as error:  # noqa: BLE001
        return None, False
    if not runs:
        return None, False
    latest = max(runs, key=lambda row: row.get("started_at") or "")
    conclusion = latest.get("conclusion")
    failed = conclusion not in (None, "success", "skipped", "neutral")
    return conclusion, failed


def navigation_delta(root: Path, base_sha: str, head_sha: str) -> list[str]:
    """New UNLISTED pages introduced on the head relative to base docs.json + tree."""
    findings: list[str] = []

    def listed_at(ref: str) -> set[str]:
        text = run(["git", "show", f"{ref}:docs.json"], check=False).stdout
        if not text.strip():
            return set()
        navigation = json.loads(text)["navigation"]
        return _listed_pages_from_navigation(navigation)

    def on_disk_at(ref: str) -> set[str]:
        paths: set[str] = set()
        for prefix in CONTENT_PREFIXES:
            listing = run(["git", "ls-tree", "-r", "--name-only", ref, "--", prefix], check=False).stdout
            for line in listing.splitlines():
                if line.endswith(".mdx"):
                    paths.add(line[: -len(".mdx")])
        return paths

    base_listed, head_listed = listed_at(base_sha), listed_at(head_sha)
    base_disk, head_disk = on_disk_at(base_sha), on_disk_at(head_sha)
    for page in sorted((head_disk - head_listed) - (base_disk - base_listed)):
        findings.append(f"UNLISTED (new on head) {page}")
    for page in sorted(head_listed - base_listed):
        if page in head_disk - head_listed:
            findings.append(f"UNLISTED (listed path missing file) {page}")
    return findings


def _listed_pages_from_navigation(navigation: dict) -> set[str]:
    pages: set[str] = set()

    def walk(items: list) -> None:
        for item in items:
            if isinstance(item, str) and not item.startswith(("GET ", "POST ", "PUT ", "DELETE ", "PATCH ")):
                pages.add(item)
            elif isinstance(item, dict) and "group" in item:
                if "root" in item:
                    pages.add(item["root"])
                walk(item.get("pages", []))
            elif isinstance(item, dict) and "pages" in item:
                walk(item["pages"])

    for tab in navigation["tabs"]:
        walk(tab.get("groups", tab.get("pages", [])))
    return pages


def scan_internal_terms(
    added: str,
    filename: str,
    already_published: Callable[[str], bool] = lambda token: False,
) -> list[str]:
    prose = IMAGE_PATH.sub("", added)
    hits: list[str] = []
    for name, pattern in INTERNAL_TERM_PATTERNS:
        new_tokens = sorted({
            match.group(0) for match in pattern.finditer(prose)
            if not already_published(match.group(0))
        })
        if new_tokens:
            hits.append(f"{filename}: internal term `{name}` ({', '.join(new_tokens[:3])})")
    return hits


def published_on(base_sha: str) -> Callable[[str], bool]:
    def already_published(token: str) -> bool:
        found = run(["git", "grep", "-q", "-F", token, base_sha, "--", *CONTENT_PREFIXES])
        return found.returncode == 0
    return already_published


def scan_remote_assets(added: str, filename: str) -> list[str]:
    hits: list[str] = []
    if REMOTE_IMAGE.search(added):
        hits.append(f"{filename}: remote image URL in added lines")
    if EXPIRES_PARAM.search(added):
        hits.append(f"{filename}: `expires=` in added lines")
    if ABSOLUTE_DOCS_LINK.search(added):
        hits.append(f"{filename}: absolute docs.extole.com link (use root-relative paths)")
    return hits


def scan_closing_keywords(pull: dict, repo: str) -> list[str]:
    owner, name = repo.split("/", 1)
    texts = [
        pull.get("title") or "",
        pull.get("body") or "",
    ]
    commits = gh_json(["api", f"repos/{repo}/pulls/{pull['number']}/commits", "--paginate"])
    texts.extend(commit.get("commit", {}).get("message", "") for commit in commits or [])
    hits: list[str] = []
    for label, text in zip(["title", "body", *["commit"] * len(commits or [])], texts, strict=False):
        for ref in armed_references(text, default_owner=owner, default_repo=name):
            hits.append(f"{label}: {ref.describe()}")
    return hits


def other_open_on_paths(repo: str, number: int, paths: set[str]) -> dict[str, list[dict]]:
    by_path: dict[str, list[dict]] = {path: [] for path in paths}
    open_prs = gh_json([
        "pr", "list", "--repo", repo, "--state", "open", "--limit", "200",
        "--json", "number,title,files",
    ])
    for row in open_prs or []:
        if row["number"] == number:
            continue
        detail = gh_json([
            "api", f"repos/{repo}/pulls/{row['number']}/files", "--paginate",
            "--jq", "[.[].filename]",
        ])
        for path in paths:
            if path in detail:
                by_path[path].append({"number": row["number"], "title": row.get("title", "")})
    return by_path


def preview_host(branch: str) -> str | None:
    slug = branch.lower().replace("/", "-")
    if not re.fullmatch(r"[a-z0-9-]+", slug):
        return None
    return f"extole-{slug}.mintlify.site"


def preview_host_from_comments(comment_bodies: list[str]) -> str | None:
    for body in reversed(comment_bodies):
        match = MINTLIFY_PREVIEW_HOST.search(body)
        if match:
            return match.group(1)
    return None


def mintlify_preview_host(repo: str, number: int, branch: str) -> str | None:
    bodies = gh_json([
        "api", f"repos/{repo}/issues/{number}/comments", "--paginate",
        "--jq", '[.[] | select(.user.login == "mintlify[bot]") | .body]',
    ]) or []
    return preview_host_from_comments(bodies) or preview_host(branch)


def deleted_sentences(files: list[dict]) -> list[str]:
    """Deleted content lines that the diff does not add back anywhere (F12's absent strings)."""
    added_text = "\n".join(
        added_text_from_patch(entry.get("patch") or "")
        for entry in files if MDX_PATH.match(entry["filename"])
    )
    sentences: list[str] = []
    for entry in files:
        if not MDX_PATH.match(entry["filename"]):
            continue
        for line in (entry.get("patch") or "").splitlines():
            if not line.startswith("-") or line.startswith("---"):
                continue
            text = line[1:].strip()
            if len(text) > 20 and text not in sentences and text not in added_text:
                sentences.append(text)
    return sentences


def new_page_titles(files: list[dict], head_sha: str) -> dict[str, str]:
    titles: dict[str, str] = {}
    for entry in files:
        if entry.get("status") != "added" or not MDX_PATH.match(entry["filename"]):
            continue
        text = run(["git", "show", f"{head_sha}:{entry['filename']}"]).stdout
        match = FRONTMATTER_TITLE.search(text)
        if match:
            titles[entry["filename"]] = match.group(1)
    return titles


def pages_with_same_title(titles: dict[str, str], base_sha: str) -> list[str]:
    listing = run(["git", "grep", "-i", "-E", r"^title:", base_sha, "--", *CONTENT_PREFIXES]).stdout
    existing: dict[str, str] = {}
    for line in listing.splitlines():
        _, path, rest = line.split(":", 2)
        match = FRONTMATTER_TITLE.search(rest)
        if match:
            existing.setdefault(normalized_title(match.group(1)), path)
    return [
        f"{path} has the same title as existing {existing[normalized_title(title)]}: {title!r}"
        for path, title in titles.items()
        if normalized_title(title) in existing and existing[normalized_title(title)] != path
    ]


def normalized_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip().strip("\"'")).lower()


def changed_files_identical_on_main(files: list[dict], base_sha: str, head_sha: str) -> bool:
    paths = [entry["filename"] for entry in files]
    if not paths:
        return False
    return run(["git", "diff", "--quiet", base_sha, head_sha, "--", *paths]).returncode == 0


def paths_changed_on_main_since_branch(files: list[dict], base_sha: str, head_sha: str) -> tuple[int, list[str]]:
    merge_base = run(["git", "merge-base", base_sha, head_sha], check=True).stdout.strip()
    behind = int(run(["git", "rev-list", "--count", f"{merge_base}..{base_sha}"], check=True).stdout.strip())
    paths = [entry["filename"] for entry in files]
    if not paths:
        return behind, []
    changed = run(["git", "diff", "--name-only", merge_base, base_sha, "--", *paths], check=True).stdout
    return behind, sorted(set(changed.split()))


def mcp_rg_pages(host: str, string: str) -> list[str]:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "query_docs_filesystem_extole_documentation",
            "arguments": {"command": f"rg -ilF {json.dumps(string)} /"},
        },
    }
    request = urllib.request.Request(
        f"https://{host}/mcp",
        method="POST",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
    )
    try:
        body = urllib.request.urlopen(request, timeout=60).read().decode()
    except urllib.error.URLError as error:
        raise OSError(str(error)) from error
    message = next(
        (json.loads(line[5:]) for line in body.splitlines() if line.startswith("data:")), None,
    ) or json.loads(body)
    pages: list[str] = []
    for part in message.get("result", {}).get("content", []):
        for line in (part.get("text") or "").splitlines():
            if line.strip().startswith("/"):
                pages.append(line.strip())
    return pages


def compute_floor(
    pull: dict,
    *,
    repo: str,
    root: Path,
    base_sha: str,
    head_sha: str,
    diff_truncated: bool,
    skip_preview: bool = False,
) -> FloorResult:
    floor = FloorResult(diff_truncated=diff_truncated)
    head = pull.get("headRefName") or ""
    is_fork = ((pull.get("headRepository") or {}).get("nameWithOwner") or "").lower() != repo.lower()
    floor.fork = is_fork

    conclusion, failed = validate_check(repo, head_sha)
    floor.validate_conclusion = conclusion
    floor.validate_failed = failed
    if failed:
        _, floor.validate_failed_on_main = validate_check(repo, base_sha)

    try:
        floor.navigation_send_back = navigation_delta(root, base_sha, head_sha)
    except Exception as error:  # noqa: BLE001
        floor.tool_failures.append(f"navigation delta: {error}")

    already_published = published_on(base_sha)
    for entry in pull.get("files") or []:
        filename = entry["filename"]
        patch = entry.get("patch") or ""
        added = added_text_from_patch(patch)
        if not added:
            continue
        floor.internal_terms.extend(scan_internal_terms(added, filename, already_published))
        floor.remote_image_or_link.extend(scan_remote_assets(added, filename))
        if any(filename.startswith(prefix) for prefix in MECHANISM_PREFIXES) or filename in MECHANISM_PREFIXES:
            floor.mechanism_paths.append(filename)

    floor.closing_keyword_hits = scan_closing_keywords(pull, repo)

    content_paths = {
        entry["filename"]
        for entry in pull.get("files") or []
        if MDX_PATH.match(entry["filename"])
    }
    if content_paths:
        by_path = other_open_on_paths(repo, pull["number"], content_paths)
        for path, others in by_path.items():
            if not others:
                continue
            floor.contention_same_page[path] = [row["number"] for row in others]
            my_headings = section_headings_from_patch(
                next(e.get("patch") or "" for e in pull["files"] if e["filename"] == path),
            )
            for other in others:
                other_files = gh_json([
                    "api", f"repos/{repo}/pulls/{other['number']}/files", "--paginate",
                ])
                other_patch = next(
                    (f.get("patch") or "" for f in other_files if f["filename"] == path), "",
                )
                if my_headings & section_headings_from_patch(other_patch):
                    floor.contention_same_section.setdefault(path, []).append(other["number"])

    merge_state = gh_json([
        "pr", "view", str(pull["number"]), "--repo", repo, "--json", "mergeStateStatus,createdAt",
    ])
    floor.merge_conflicts = merge_state.get("mergeStateStatus") == "DIRTY"
    files = pull.get("files") or []
    try:
        floor.already_on_main = changed_files_identical_on_main(files, base_sha, head_sha)
        floor.commits_behind_main, floor.pages_changed_on_main = paths_changed_on_main_since_branch(
            files, base_sha, head_sha,
        )
        floor.corpus_duplicates = pages_with_same_title(new_page_titles(files, head_sha), base_sha)
    except subprocess.CalledProcessError as error:
        floor.tool_failures.append(f"git against main: {str(error.stderr or error).strip()[:200]}")
    created = pull.get("createdAt") or merge_state.get("createdAt") or ""
    floor.body_lines_required = created >= BODY_TEMPLATE_SINCE
    body = pull.get("body") or ""
    for key, pattern in BODY_LINE_PATTERNS.items():
        if not pattern.search(body):
            floor.body_lines_missing.append(key)

    if skip_preview or is_fork:
        return floor

    host = mintlify_preview_host(repo, pull["number"], head)
    if not host:
        floor.preview_unreachable = True
        floor.tool_failures.append(f"no Mintlify preview host for branch {head!r}")
        return floor

    absent_strings = deleted_sentences(pull.get("files") or [])
    try:
        for string in absent_strings[:8]:
            pages = mcp_rg_pages(host, string)
            if pages:
                floor.reach_exact_failures.append(
                    f"F12: deleted sentence still on preview {host}: {string[:80]!r} -> {pages[:3]}",
                )
    except OSError as error:
        floor.preview_unreachable = True
        floor.tool_failures.append(f"F12 preview {host}: {error}")

    return floor


def render_floor_context(floor: FloorResult) -> str:
    return (
        "<<<FLOOR (deterministic)>>>\n"
        + json.dumps(floor.to_dict(), indent=2)
        + "\n<<<END FLOOR>>>"
    )


def send_back_reasons(floor: FloorResult) -> list[str]:
    reasons: list[str] = []
    if floor.validate_failed and not floor.validate_failed_on_main:
        reasons.append(f"F1: `{REQUIRED_CHECK}` is not green ({floor.validate_conclusion!r}).")
    reasons.extend(f"F2: {item}" for item in floor.navigation_send_back)
    reasons.extend(f"F3: {item}" for item in floor.broken_links_send_back)
    reasons.extend(f"F4: {item}" for item in floor.internal_terms)
    reasons.extend(f"F5: {item}" for item in floor.remote_image_or_link)
    reasons.extend(f"F6: {item}" for item in floor.closing_keyword_hits)
    if floor.merge_conflicts:
        reasons.append("F9: the branch conflicts with `main`; merge `main` in and resolve the conflicts.")
    if floor.pages_changed_on_main:
        reasons.append(
            f"F9: `main` changed {floor.pages_changed_on_main} after this branch started; "
            "merge `main` in and check the change still reads right."
        )
    if floor.body_lines_required and floor.body_lines_missing:
        reasons.append(f"F11: body missing {floor.body_lines_missing}.")
    reasons.extend(floor.reach_exact_failures)
    return reasons
