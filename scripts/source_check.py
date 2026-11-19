"""Read the private source check's result for a pull request head (RUBRIC v2, "Claim verification").

The check runs in a private repository, because it reads private source: extole/tech's
`docs-claim-verify` workflow polls this repository's open pull requests and posts one comment per
pull request, as the CI GitHub App. The comment carries each claim's sentence, its status and the
repository that settled it, never a path, a symbol or a quote from private source. Only a comment
by that App counts, and only for the head it names.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

VERIFIER_AUTHOR = "extole-github-ci[bot]"
MARKER = re.compile(r"<!-- docs-claim-verifier head=([0-9a-f]{40}) -->")
PAYLOAD = re.compile(r"<!-- docs-claim-verifier-claims\n(.*?)\n-->", re.DOTALL)
STATUSES = ("verified", "contradicted", "partly", "not-in-source", "unreadable")


@dataclass
class SourceCheck:
    claims: list[dict]
    failed: bool


def from_comments(comments: list[dict], head: str) -> SourceCheck | None:
    for comment in reversed(comments):
        if (comment.get("user") or {}).get("login") != VERIFIER_AUTHOR:
            continue
        body = comment.get("body") or ""
        marker = MARKER.search(body)
        payload = PAYLOAD.search(body)
        if not marker or not payload or marker.group(1) != head:
            continue
        try:
            data = json.loads(payload.group(1))
        except json.JSONDecodeError:
            continue
        if data.get("head") != head:
            continue
        claims = [claim for claim in data.get("claims") or [] if claim.get("status") in STATUSES]
        return SourceCheck(claims=claims, failed=bool(data.get("failed")))
    return None


def judge_claims(check: SourceCheck) -> list[dict]:
    rows = []
    for claim in check.claims:
        source = claim.get("repository") or "no repository"
        if claim.get("supported_sentence"):
            source += f"; the source supports: {claim['supported_sentence']}"
        rows.append({
            "sentence": claim.get("sentence") or "(quote withheld by the source check)",
            "status": claim["status"],
            "source": source,
        })
    return rows


def render_context(check: SourceCheck | None) -> str:
    if check is None:
        return "SOURCE CHECK: not run yet for this head. Mark every product claim `unreadable`."
    if check.failed:
        return "SOURCE CHECK: did not finish for this head. Mark every product claim `unreadable`."
    lines = [
        "SOURCE CHECK (trusted: the private verifier read pluribus, showtime, creative and consumed). "
        "These claim statuses are final; use them as your `claims`:",
    ]
    lines += [f"- {row['status']}: {row['sentence']} ({row['source']})" for row in judge_claims(check)]
    return "\n".join(lines)


def reason(check: SourceCheck | None) -> str | None:
    if check is None:
        return "The source check has not run for this commit yet. It runs within about 15 minutes, and the judge runs again."
    if check.failed:
        return "The source check did not finish for this commit, so its claims are unreadable."
    return None
