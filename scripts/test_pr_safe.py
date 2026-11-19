#!/usr/bin/env python3
"""Tests for the safe class that the docs PR judge records in shadow."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pr_floor import FloorResult
from pr_safe import classify, site_path_resolver, term_swaps

STANDARDS = (Path(__file__).resolve().parent.parent / ".mintlify" / "AGENTS.md").read_text(encoding="utf-8")
HEAD_FILES = {"guides/rewards/how-to-set-up-a-reward.mdx", "technical/partners/index.mdx"}


def clean_floor() -> FloorResult:
    return FloorResult(validate_conclusion="success")


def edit(patch: str, filename: str = "guides/rewards/page.mdx") -> dict:
    lines = patch.splitlines()
    return {
        "filename": filename,
        "status": "modified",
        "patch": patch,
        "additions": sum(line.startswith("+") for line in lines),
        "deletions": sum(line.startswith("-") for line in lines),
    }


def safe(files: list[dict], floor: FloorResult | None = None):
    return classify(files, floor or clean_floor(), STANDARDS, site_path_resolver(HEAD_FILES))


class TermTableTests(unittest.TestCase):
    def test_reads_the_real_terminology_table(self):
        swaps = term_swaps(STANDARDS)
        self.assertIn(("referrer", "advocate"), swaps)
        self.assertIn(("fraud rules", "quality rules"), swaps)
        self.assertIn(("v8", "legacy campaign"), swaps)

    def test_a_qualified_avoid_term_needs_judgment(self):
        swaps = term_swaps(STANDARDS)
        self.assertNotIn(("campaign", "program"), swaps)
        self.assertNotIn(("step", "business event"), swaps)
        self.assertNotIn(("user", "person"), swaps)
        self.assertNotIn(("fraud rules", "quality engine"), swaps)


class SafeClassTests(unittest.TestCase):
    def test_term_swap_is_safe(self):
        result = safe([edit("-Each referrer gets a share link.\n+Each advocate gets a share link.")])
        self.assertTrue(result.would_merge, result.reasons)
        self.assertEqual(result.kinds, ["term-swap"])

    def test_bolding_a_ui_label_is_formatting(self):
        result = safe([edit("-Click Save to finish.\n+Click **Save** to finish.")])
        self.assertEqual(result.kinds, ["formatting"])

    def test_link_fix_to_a_page_that_exists(self):
        result = safe([edit(
            "-See [rewards](/guides/old/reward).\n+See [rewards](/guides/rewards/how-to-set-up-a-reward).",
        )])
        self.assertEqual(result.kinds, ["link-fix"])

    def test_link_to_a_page_that_does_not_exist_is_not_safe(self):
        result = safe([edit("-See [rewards](/guides/old/reward).\n+See [rewards](/guides/nowhere).")])
        self.assertFalse(result.would_merge)

    def test_typo(self):
        result = safe([edit("-You will recieve the reward.\n+You will receive the reward.")])
        self.assertEqual(result.kinds, ["typo"])

    def test_changed_number_is_never_safe(self):
        result = safe([edit("-Rules count the 50 most recent rewards.\n+Rules count the 100 most recent rewards.")])
        self.assertFalse(result.would_merge)

    def test_new_sentence_is_not_safe(self):
        result = safe([edit("+A reward expires after a year.")])
        self.assertFalse(result.would_merge)

    def test_rewording_is_not_safe(self):
        result = safe([edit("-The reward is issued at once.\n+The reward is issued after the friend converts.")])
        self.assertFalse(result.would_merge)

    def test_new_page_is_not_safe(self):
        added = edit("+# A Page", filename="guides/rewards/new.mdx") | {"status": "added"}
        self.assertFalse(safe([added]).would_merge)

    def test_floor_finding_blocks(self):
        floor = clean_floor()
        floor.pages_changed_on_main = ["guides/rewards/page.mdx"]
        result = safe([edit("-Each referrer gets one.\n+Each advocate gets one.")], floor)
        self.assertFalse(result.would_merge)

    def test_failed_validate_blocks(self):
        floor = FloorResult(validate_conclusion="failure", validate_failed=True)
        result = safe([edit("-Each referrer gets one.\n+Each advocate gets one.")], floor)
        self.assertFalse(result.would_merge)

    def test_pending_validate_does_not_block(self):
        result = safe([edit("-Each referrer gets one.\n+Each advocate gets one.")], FloorResult())
        self.assertTrue(result.would_merge, result.reasons)


if __name__ == "__main__":
    unittest.main()
