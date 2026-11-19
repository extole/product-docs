#!/usr/bin/env python3
"""Fail when a change adds a navigation or broken-link finding that its base does not have.

`main` already carries findings of both kinds, so the plain checks fail on every pull request.
This compares the checkout with its base and reports only the findings the change adds.

Exit status: 0 when the change adds no finding, 1 when it adds one, 2 when the check could not run.

Usage:
  python3 scripts/check_new_findings.py --base <ref> navigation
  python3 scripts/check_new_findings.py --base <ref> broken-links      # needs MINT_VERSION
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
LINK_MARKER = "⎿"
BROKEN_LINK_COUNT = re.compile(r"found (\d+) broken links?")
NO_BROKEN_LINKS = "no broken links found"
NEW_FINDINGS, DID_NOT_RUN = 1, 2


class CheckDidNotRun(RuntimeError):
    pass


def navigation_findings(checkout: Path) -> set[str]:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_navigation.py"), str(checkout)],
        capture_output=True, text=True, check=False,
    )
    if result.returncode not in (0, 1):
        raise CheckDidNotRun(f"check_navigation.py exited {result.returncode}: {result.stderr.strip()[-400:]}")
    output = result.stdout
    return {line for line in output.splitlines() if line.startswith(("UNLISTED", "MISSING", "MISMATCH"))}


def broken_link_findings(checkout: Path) -> set[str]:
    version = os.environ["MINT_VERSION"]
    result = subprocess.run(
        ["npx", "--yes", f"mint@{version}", "broken-links"],
        cwd=checkout, capture_output=True, text=True, check=False,
    )
    if result.returncode not in (0, 1):
        raise CheckDidNotRun(f"mint broken-links exited {result.returncode}: {result.stderr.strip()[-400:]}")
    return parse_broken_links(ANSI_ESCAPE.sub("", result.stdout))


def parse_broken_links(output: str) -> set[str]:
    """Pairs of page and link. The CLI wraps a long link onto lines that carry no marker.

    Raises CheckDidNotRun when the output carries neither of the CLI's result lines, or reports
    broken links that the parse cannot find. Either means the run failed or the format changed.
    """
    findings = pairs_from_broken_link_output(output)
    reported = BROKEN_LINK_COUNT.search(output)
    if not reported and NO_BROKEN_LINKS not in output:
        raise CheckDidNotRun(f"mint broken-links printed no result line: {output.strip()[-300:]!r}")
    if reported and int(reported.group(1)) > 0 and not findings:
        raise CheckDidNotRun(
            f"mint broken-links reported {reported.group(1)} broken links, and none could be read. "
            "The CLI's output format may have changed: update parse_broken_links."
        )
    return findings


def pairs_from_broken_link_output(output: str) -> set[str]:
    findings: set[str] = set()
    page = ""
    link: str | None = None
    for line in output.splitlines():
        stripped = line.strip()
        if stripped.startswith(LINK_MARKER):
            if link is not None:
                findings.add(f"{page}  {link}")
            link = stripped.removeprefix(LINK_MARKER).strip()
        elif re.fullmatch(r"\S+\.mdx?", stripped):
            if link is not None:
                findings.add(f"{page}  {link}")
            page, link = stripped, None
        elif link is not None and stripped:
            link += stripped
    if link is not None:
        findings.add(f"{page}  {link}")
    return findings


CHECKS = {"navigation": navigation_findings, "broken-links": broken_link_findings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--base", required=True, help="the commit the change is compared with")
    parser.add_argument("check", choices=sorted(CHECKS))
    args = parser.parse_args()
    try:
        base_findings, added = compare_with_base(CHECKS[args.check], args.base)
    except (CheckDidNotRun, subprocess.CalledProcessError) as error:
        reason = (getattr(error, "stderr", None) or str(error)).strip()
        annotate("error", f"{args.check} check did not run", reason)
        print(f"{args.check}: the check did not run, so it says nothing about this change: {reason}")
        return DID_NOT_RUN

    for finding in added:
        annotate("error", f"New {args.check} finding", finding)
        print(finding)
    print(f"{args.check}: {len(added)} new findings against {args.base} ({len(base_findings)} already there)")
    return NEW_FINDINGS if added else 0


def compare_with_base(find, base: str) -> tuple[set[str], list[str]]:
    with tempfile.TemporaryDirectory() as directory:
        base_checkout = Path(directory) / "base"
        subprocess.run(["git", "-C", str(ROOT), "worktree", "add", "--detach", "--quiet", str(base_checkout), base],
                       check=True, capture_output=True, text=True)
        try:
            base_findings = find(base_checkout)
        finally:
            subprocess.run(["git", "-C", str(ROOT), "worktree", "remove", "--force", str(base_checkout)],
                           check=True, capture_output=True, text=True)
    return base_findings, sorted(find(ROOT) - base_findings)


def annotate(level: str, title: str, message: str) -> None:
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::{level} title={title}::{message}")


if __name__ == "__main__":
    sys.exit(main())
