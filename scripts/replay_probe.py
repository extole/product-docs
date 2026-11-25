#!/usr/bin/env python3
"""Ask Mintlify's `/mcp` on docs.extole.com and on a branch preview the same things, and print what comes back.

Two probes, both with no credentials:

- search: `search_extole_documentation` for each query. The response carries one content part for
  each returned section. For each query this prints the ranked section titles, and the ranks of the
  sections whose text contains each expected or unwanted string.
- filesystem: `query_docs_filesystem_extole_documentation` with `rg -il <string> /`, which lists
  the pages that contain a string. This is exact, so it is what a gate can rely on.

    python3 replay_probe.py --branch eng-31874 \
        --query "when does the extole platform invite expire" --query "invitation link expired" \
        --present "7 days" --absent "within the hour"

`--branch` is the preview name Mintlify derives from the Git branch: lower case, `[a-z0-9-]+`.
"""
from __future__ import annotations

import argparse
import datetime
import json
import shlex
import urllib.request

SEARCH_TOOL = "search_extole_documentation"
FILESYSTEM_TOOL = "query_docs_filesystem_extole_documentation"


def call(host: str, name: str, arguments: dict) -> list[str]:
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": arguments}}
    request = urllib.request.Request(
        f"https://{host}/mcp", method="POST", data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
    )
    body = urllib.request.urlopen(request, timeout=60).read().decode()
    message = next((json.loads(line[5:]) for line in body.splitlines() if line.startswith("data:")), None) or json.loads(body)
    return [part.get("text", "") for part in message["result"]["content"]]


def title_of(section: str) -> str:
    return next((line[len("Title:"):].strip() for line in section.splitlines() if line.startswith("Title:")), "?")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--branch", required=True)
    parser.add_argument("--query", action="append", default=[])
    parser.add_argument("--present", action="append", default=[])
    parser.add_argument("--absent", action="append", default=[])
    args = parser.parse_args()

    hosts = ("docs.extole.com", f"extole-{args.branch}.mintlify.site")
    print(f"read {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')}")
    for host in hosts:
        print(f"== {host}")
        for query in args.query:
            sections = call(host, SEARCH_TOOL, {"query": query})
            print(f"  search {query!r}: {len(sections)} sections")
            print("    ranked: " + " | ".join(f"{rank}. {title_of(s)}" for rank, s in enumerate(sections, 1)))
            for string in args.present + args.absent:
                ranks = [rank for rank, s in enumerate(sections, 1) if string.lower() in s.lower()]
                print(f"    {string!r} in sections ranked: {ranks or 'none'}")
        for string in args.present + args.absent:
            listing = call(host, FILESYSTEM_TOOL, {"command": f"rg -il {shlex.quote(string)} /"})
            pages = [line.strip() for text in listing for line in text.splitlines() if line.strip().startswith("/")]
            print(f"  filesystem rg {string!r}: {len(pages)} page(s) {pages[:6]}")


if __name__ == "__main__":
    main()
