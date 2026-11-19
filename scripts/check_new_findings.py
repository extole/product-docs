#!/usr/bin/env python3
"""Fail when a change adds a navigation or broken-link finding that its base does not have.

`main` already carries findings of both kinds, so the plain checks fail on every pull request.
This compares the checkout with its base and reports only the findings the change adds.

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


def navigation_findings(checkout: Path) -> set[str]:
    output = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_navigation.py"), str(checkout)],
        capture_output=True, text=True, check=False,
    ).stdout
    return {line for line in output.splitlines() if line.startswith(("UNLISTED", "MISSING", "MISMATCH"))}


def broken_link_findings(checkout: Path) -> set[str]:
    version = os.environ["MINT_VERSION"]
    result = subprocess.run(
        ["npx", "--yes", f"mint@{version}", "broken-links"],
        cwd=checkout, capture_output=True, text=True, check=False,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(f"mint broken-links exited {result.returncode}: {result.stderr.strip()[-400:]}")
    return parse_broken_links(ANSI_ESCAPE.sub("", result.stdout))


def parse_broken_links(output: str) -> set[str]:
    """Pairs of page and link. The CLI wraps a long link onto lines that carry no marker."""
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
    find = CHECKS[args.check]

    with tempfile.TemporaryDirectory() as directory:
        base_checkout = Path(directory) / "base"
        subprocess.run(["git", "-C", str(ROOT), "worktree", "add", "--detach", "--quiet", str(base_checkout), args.base],
                       check=True)
        try:
            base_findings = find(base_checkout)
        finally:
            subprocess.run(["git", "-C", str(ROOT), "worktree", "remove", "--force", str(base_checkout)], check=True)
    added = sorted(find(ROOT) - base_findings)

    for finding in added:
        print(finding)
    print(f"{args.check}: {len(added)} new findings against {args.base} ({len(base_findings)} already there)")
    return 1 if added else 0


if __name__ == "__main__":
    sys.exit(main())
