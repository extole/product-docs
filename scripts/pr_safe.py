"""The safe class for docs pull requests: changes that add no product claim (RUBRIC v2, "The safe class").

A change is safe when every changed line is a line-for-line edit of one of these kinds, and the
floor is clean:

- `formatting`: the same words, with emphasis or whitespace changed.
- `link-fix`: the same text, with internal link targets changed to pages that exist on the head.
- `term-swap`: each replaced word is an **Avoid** term replaced by its **Preferred** term from the
  terminology table in `.mintlify/AGENTS.md`.
- `typo`: at most two words changed, each a near spelling of the word it replaces.

Numbers and backtick literals never change in a safe change. The classification is deterministic:
no model reads the diff. Today it runs in shadow, which records what it would merge and merges
nothing.
"""

from __future__ import annotations

import difflib
import re
from dataclasses import asdict, dataclass, field
from typing import Callable

from pr_floor import MDX_PATH, FloorResult

MAX_CHANGED_LINES = 40
TYPO_MAX_WORDS = 2
TYPO_MIN_SIMILARITY = 0.75

LINK_TARGET = re.compile(r"\]\(([^)\s]*)\)")
EMPHASIS = re.compile(r"[*_]")
WORD = re.compile(r"[\w'-]+")
FACT_TOKEN = re.compile(r"`[^`]+`|\d+(?:[.,]\d+)*")
TERMINOLOGY_ROW = re.compile(r"^\|\s*\*\*(?P<preferred>[^|]+?)\*\*[^|]*\|\s*(?P<avoid>[^|]+?)\s*\|", re.MULTILINE)


@dataclass
class SafeClass:
    would_merge: bool
    kinds: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def term_swaps(standards: str) -> set[tuple[str, str]]:
    """(avoid, preferred) pairs from the Terminology table, lowercased.

    A row whose Avoid cell carries a qualifier, such as "campaign *(when you mean the use case)*"
    or "user, consumer *(in data prose)*", needs judgment to apply, so none of its terms is a safe
    swap.
    """
    section = standards.split("## Terminology", 1)[-1].split("\n## ", 1)[0]
    swaps: set[tuple[str, str]] = set()
    for row in TERMINOLOGY_ROW.finditer(section):
        if "(" in row.group("avoid"):
            continue
        preferred_alternatives = [term.strip().lower() for term in row.group("preferred").split(",")]
        for avoid in row.group("avoid").split(","):
            avoid = avoid.strip().strip('"').lower()
            if not avoid or avoid.startswith(("—", "and ")):
                continue
            for preferred in preferred_alternatives:
                swaps.update(paired_variants(avoid, preferred))
    return swaps


def paired_variants(avoid: str, preferred: str) -> set[tuple[str, str]]:
    avoid_variants = [term.strip() for term in avoid.split("/")]
    preferred_variants = [term.strip() for term in preferred.split("/")]
    if len(avoid_variants) == len(preferred_variants):
        return set(zip(avoid_variants, preferred_variants))
    return {(variant, preferred_variants[0]) for variant in avoid_variants}


def change_blocks(patch: str) -> list[tuple[list[str], list[str]]]:
    blocks: list[tuple[list[str], list[str]]] = []
    removed: list[str] = []
    added: list[str] = []
    for line in patch.splitlines():
        if line.startswith("-") and not line.startswith("---"):
            if added:
                blocks.append((removed, added))
                removed, added = [], []
            removed.append(line[1:])
        elif line.startswith("+") and not line.startswith("+++"):
            added.append(line[1:])
        elif removed or added:
            blocks.append((removed, added))
            removed, added = [], []
    if removed or added:
        blocks.append((removed, added))
    return blocks


def fact_tokens(line: str) -> list[str]:
    return sorted(FACT_TOKEN.findall(LINK_TARGET.sub("]()", line)))


def without_link_targets(line: str) -> str:
    return LINK_TARGET.sub("]()", line)


def without_formatting(line: str) -> str:
    return re.sub(r"\s+", " ", EMPHASIS.sub("", line)).strip()


def classify_line(
    old: str,
    new: str,
    swaps: set[tuple[str, str]],
    link_resolves: Callable[[str], bool],
) -> str | None:
    if fact_tokens(old) != fact_tokens(new):
        return None
    if without_formatting(old) == without_formatting(new):
        return "formatting"
    if without_link_targets(old) == without_link_targets(new):
        new_targets = set(LINK_TARGET.findall(new)) - set(LINK_TARGET.findall(old))
        return "link-fix" if all(link_resolves(target) for target in new_targets) else None
    old_words = WORD.findall(without_formatting(old))
    new_words = WORD.findall(without_formatting(new))
    replaced = [
        (" ".join(old_words[i1:i2]).lower(), " ".join(new_words[j1:j2]).lower())
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=old_words, b=new_words).get_opcodes()
        if tag != "equal"
    ]
    if replaced and all(is_term_swap(before, after, swaps) for before, after in replaced):
        return "term-swap"
    if len(replaced) <= TYPO_MAX_WORDS and all(
        before and after and " " not in before and " " not in after
        and difflib.SequenceMatcher(a=before, b=after).ratio() >= TYPO_MIN_SIMILARITY
        for before, after in replaced
    ):
        return "typo"
    return None


def is_term_swap(before: str, after: str, swaps: set[tuple[str, str]]) -> bool:
    if (before, after) in swaps:
        return True
    singular = (before.removesuffix("s"), after.removesuffix("s"))
    return before.endswith("s") and after.endswith("s") and singular in swaps


def site_path_resolver(head_files: set[str]) -> Callable[[str], bool]:
    def resolves(target: str) -> bool:
        path = target.split("#", 1)[0].split("?", 1)[0]
        if not path.startswith("/") or path.startswith("//"):
            return False
        relative = path.strip("/")
        return any(candidate in head_files for candidate in (relative, f"{relative}.mdx", f"{relative}/index.mdx"))
    return resolves


def floor_blockers(floor: FloorResult) -> list[str]:
    checks = [
        (floor.fork, "fork pull request"),
        (floor.diff_truncated, "diff truncated"),
        (floor.validate_failed, f"`validate` is {floor.validate_conclusion!r}"),
        (bool(floor.navigation_send_back), "navigation finding (F2)"),
        (bool(floor.internal_terms), "internal term (F4)"),
        (bool(floor.remote_image_or_link), "remote image or absolute link (F5)"),
        (bool(floor.closing_keyword_hits), "closing keyword (F6)"),
        (floor.merge_conflicts, "conflicts with `main`"),
        (bool(floor.pages_changed_on_main), "`main` changed the same page (F9)"),
        (bool(floor.reach_exact_failures), "deleted text still on the preview (F12)"),
        (bool(floor.mechanism_paths), "mechanism path (R4)"),
        (bool(floor.contention_same_page), "another open pull request changes the same page (F8)"),
        (floor.already_on_main, "the change is already on `main`"),
        (bool(floor.tool_failures), "a floor check failed to run"),
    ]
    return [reason for failed, reason in checks if failed]


def classify(
    files: list[dict],
    floor: FloorResult,
    standards: str,
    link_resolves: Callable[[str], bool],
) -> SafeClass:
    reasons = floor_blockers(floor)
    if not files:
        reasons.append("no files changed")
    for entry in files:
        if entry.get("status") != "modified" or not MDX_PATH.match(entry["filename"]):
            reasons.append(f"{entry['filename']}: {entry.get('status')}, not an edit to an existing page")
    changed_lines = sum(entry.get("additions", 0) + entry.get("deletions", 0) for entry in files)
    if changed_lines > MAX_CHANGED_LINES:
        reasons.append(f"{changed_lines} changed lines, more than {MAX_CHANGED_LINES}")
    if reasons:
        return SafeClass(would_merge=False, reasons=reasons)

    swaps = term_swaps(standards)
    kinds: set[str] = set()
    for entry in files:
        for removed, added in change_blocks(entry.get("patch") or ""):
            if len(removed) != len(added):
                reasons.append(f"{entry['filename']}: adds or removes lines")
                continue
            for old, new in zip(removed, added):
                kind = classify_line(old, new, swaps, link_resolves)
                if kind:
                    kinds.add(kind)
                else:
                    reasons.append(f"{entry['filename']}: changes content: {new.strip()[:80]!r}")
    return SafeClass(would_merge=not reasons, kinds=sorted(kinds), reasons=reasons)

