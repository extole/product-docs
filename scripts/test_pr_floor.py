#!/usr/bin/env python3
"""Tests for deterministic docs PR floor checks."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from closing_references import armed_references
from pr_floor import preview_host, scan_internal_terms, scan_remote_assets


class PreviewHostTests(unittest.TestCase):
    def test_lowercase_branch(self):
        self.assertEqual(preview_host("ENG-30863"), "extole-eng-30863.mintlify.site")

    def test_rejects_slash(self):
        self.assertIsNone(preview_host("docs/my-feature"))


class InternalTermTests(unittest.TestCase):
    def test_show_expert(self):
        hits = scan_internal_terms("Click **Show Expert** to continue.", "guides/foo.mdx")
        self.assertTrue(any("show-expert" in hit for hit in hits))


class RemoteAssetTests(unittest.TestCase):
    def test_remote_image(self):
        hits = scan_remote_assets("![x](https://example.com/a.png)", "guides/foo.mdx")
        self.assertEqual(len(hits), 1)


class ClosingReferenceTests(unittest.TestCase):
    def test_finds_fix_keyword(self):
        refs = armed_references("fix #12", default_owner="extole", default_repo="product-docs")
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0].number, 12)


if __name__ == "__main__":
    unittest.main()
