"""GitHub's closing keywords, parsed so Garry can take them back out of what he publishes.

`fix`, `close` or `resolve` in any tense, colon optional, directly before a reference to an issue or
pull request -- `#N`, `owner/repo#N`, a bare URL, an angle-bracket autolink or a markdown link with any
text -- is an instruction GitHub executes when the text reaches the default branch: the referenced
thing is closed, in any repository the merging account can write to, pull requests included. Only a
token between the keyword and the reference, a code span or an HTML comment stops it. GitHub offers no
pre-merge signal for a pull-request target, so the parser has to live here. Every shape was measured
against GitHub on 2026-09-09 (extole/ai-tools,
docs/investigations/engineering/ada_closing_keyword_cross_repo_close_20260909/); the defused form is
a code span, which GitHub does not read and a reviewer can still copy.

Vendored verbatim from `extole/tech` `garry/garry/closing_references.py`, per the product-docs judge
plan (`extole/ai-tools` `docs/plans/product_docs_judge_20260929/BRIEF.md`). This judge's generated
`reasons` can quote a diff line, and a quoted line is exactly the untrusted text this module exists
to defuse before it reaches a posted comment.
"""

import json
import re
import subprocess
from dataclasses import dataclass

CLOSING_KEYWORDS = ("close", "closes", "closed", "fix", "fixes", "fixed", "resolve", "resolves", "resolved")

_GITHUB_ITEM_URL = r"https?://github\.com/(?P<{prefix}owner>[A-Za-z0-9_.-]+)/(?P<{prefix}repo>[A-Za-z0-9_.-]+)/(?:pull|issues)/(?P<{prefix}number>\d+)"

ARMED_REFERENCE = re.compile(
    r"(?<![A-Za-z0-9_])(?P<keyword>close[sd]?|fix(?:e[sd])?|resolve[sd]?)(?![A-Za-z0-9_])"
    r":?[ \t]*"
    r"(?P<reference>"
    r"\[[^\]\n]*\]\(" + _GITHUB_ITEM_URL.format(prefix="link_") + r"[^)\n]*\)"
    r"|<?" + _GITHUB_ITEM_URL.format(prefix="url_") + r">?"
    r"|(?:(?P<slug_owner>[A-Za-z0-9_.-]+)/(?P<slug_repo>[A-Za-z0-9_.-]+))?#(?P<hash_number>\d+)(?![A-Za-z0-9_])"
    r")",
    re.IGNORECASE,
)

_CODE_SPAN = re.compile(r"`+[^`\n]*`+")
_HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


@dataclass(frozen=True)
class ArmedReference:
    keyword: str
    reference: str
    owner: str
    repo: str
    number: int
    start: int
    end: int

    def describe(self):
        target = f"{self.owner}/{self.repo}#{self.number}" if self.owner and self.repo else f"#{self.number}"
        return f"`{self.keyword} {self.reference}` -> {target}"


def _inert_spans(text):
    spans = [match.span() for match in _CODE_SPAN.finditer(text)]
    spans.extend(match.span() for match in _HTML_COMMENT.finditer(text))
    return spans


def armed_references(text, default_owner="", default_repo=""):
    """Every place GitHub would read `text` as an instruction to close something."""
    text = text or ""
    inert = _inert_spans(text)
    found = []
    for match in ARMED_REFERENCE.finditer(text):
        if any(start <= match.start("reference") < end for start, end in inert):
            continue
        owner = match.group("link_owner") or match.group("url_owner") or match.group("slug_owner") or default_owner
        repo = match.group("link_repo") or match.group("url_repo") or match.group("slug_repo") or default_repo
        number = match.group("link_number") or match.group("url_number") or match.group("hash_number")
        found.append(
            ArmedReference(
                keyword=match.group("keyword"),
                reference=match.group("reference"),
                owner=owner or "",
                repo=repo or "",
                number=int(number),
                start=match.start("reference"),
                end=match.end("reference"),
            )
        )
    return found


def _code_span(reference):
    link = re.fullmatch(r"\[(?P<text>[^\]]*)\]\((?P<url>[^)]*)\)", reference)
    if link:
        return f"`{link.group('text')} ({link.group('url')})`"
    return f"`{reference.strip('<>')}`"


def defuse(text, default_owner="", default_repo=""):
    """`text` with every armed reference wrapped in a code span, so GitHub closes nothing."""
    text = text or ""
    pieces = []
    cursor = 0
    for armed in armed_references(text, default_owner, default_repo):
        pieces.append(text[cursor:armed.start])
        pieces.append(_code_span(armed.reference))
        cursor = armed.end
    pieces.append(text[cursor:])
    return "".join(pieces)


def _gh_api(*arguments, payload=None):
    command = ["gh", "api", *arguments]
    if payload is not None:
        command.extend(["--input", "-"])
    completed = subprocess.run(
        command,
        input=json.dumps(payload) if payload is not None else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(f"gh api {' '.join(arguments)} failed: {completed.stderr.strip() or completed.stdout.strip()}")
    return json.loads(completed.stdout) if completed.stdout.strip() else None


def defuse_pull_request(repo, number):
    """Rewrite a pull request's title and body so neither closes anything on merge.

    Returns the list of references it defused, empty when the pull request was already inert.
    A squash merge copies the pull request's title and body into the merge commit message, so
    this has to run immediately before a merge that a person has not read first -- vendored
    from `extole/ada` `closing_references.py` alongside `armed_references`/`defuse`, per the same
    reuse table entry in `docs/plans/catalog_skill_judge_20260924/BRIEF.md`.
    """
    owner, _, name = repo.partition("/")
    pull = _gh_api(f"repos/{repo}/pulls/{number}")
    title = pull.get("title") or ""
    body = pull.get("body") or ""
    armed = armed_references(title, owner, name) + armed_references(body, owner, name)
    if not armed:
        return []
    _gh_api(
        "--method", "PATCH", f"repos/{repo}/pulls/{number}",
        payload={"title": defuse(title, owner, name), "body": defuse(body, owner, name)},
    )
    return armed
