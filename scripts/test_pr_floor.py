#!/usr/bin/env python3
"""Tests for deterministic docs PR floor checks."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from closing_references import armed_references
from pr_floor import (
    FloorResult,
    deleted_sentences,
    preview_host,
    preview_host_from_comments,
    scan_internal_terms,
    scan_remote_assets,
    send_back_reasons,
)
from pr_judge import apply_verdict_steps


class PreviewHostTests(unittest.TestCase):
    def test_lowercase_branch(self):
        self.assertEqual(preview_host("ENG-30863"), "extole-eng-30863.mintlify.site")

    def test_slash_becomes_dash_as_mintlify_names_it(self):
        self.assertEqual(
            preview_host("docs/trigger-events-overview"),
            "extole-docs-trigger-events-overview.mintlify.site",
        )

    def test_rejects_other_characters(self):
        self.assertIsNone(preview_host("docs/my_feature"))

    def test_mintlify_comment_names_the_host(self):
        body = (
            "| [extole](https://app.mintlify.com/extole/extole/activity) | Ready | "
            "[View Preview](https://extole-claude-upbeat-curie-gek2mn.mintlify.site/guides/a) |"
        )
        self.assertEqual(
            preview_host_from_comments(["unrelated", body]),
            "extole-claude-upbeat-curie-gek2mn.mintlify.site",
        )


class InternalTermTests(unittest.TestCase):
    def test_show_expert(self):
        hits = scan_internal_terms("Click **Show Expert** to continue.", "guides/foo.mdx")
        self.assertTrue(any("show-expert" in hit for hit in hits))

    def test_image_path_is_not_an_internal_repository(self):
        added = '<img src="/images/extole/1099e785cae5de9d.png" alt="Offer" />'
        self.assertEqual(scan_internal_terms(added, "guides/foo.mdx"), [])

    def test_term_already_on_main_is_not_new(self):
        added = "Email support@extole.com, or ask jane.doe@extole.com."
        hits = scan_internal_terms(added, "guides/foo.mdx", lambda token: token == "support@extole.com")
        self.assertEqual(len(hits), 1)
        self.assertIn("jane.doe@extole.com", hits[0])
        self.assertNotIn("support@extole.com", hits[0])


class DeletedSentenceTests(unittest.TestCase):
    def test_moved_sentence_is_not_absent(self):
        files = [{
            "filename": "guides/a.mdx",
            "patch": "-This sentence moves further down the page.\n+This sentence moves further down the page.",
        }]
        self.assertEqual(deleted_sentences(files), [])

    def test_deleted_table_row_is_kept_as_written(self):
        row = "| Views | The socket that carries the tabs |"
        files = [{"filename": "guides/a.mdx", "patch": f"-{row}\n+| Other | row |"}]
        self.assertEqual(deleted_sentences(files), [row])


class VerdictStepTests(unittest.TestCase):
    def test_change_already_on_main_closes(self):
        verdict = apply_verdict_steps(
            {"verdict": "needs-human", "reasons": []}, FloorResult(already_on_main=True),
        )
        self.assertEqual(verdict["verdict"], "close")

    def test_validate_failure_inherited_from_main_is_not_sent_back(self):
        floor = FloorResult(validate_failed=True, validate_conclusion="failure", validate_failed_on_main=True)
        self.assertEqual(send_back_reasons(floor), [])

    def test_behind_main_on_other_pages_is_not_sent_back(self):
        self.assertEqual(send_back_reasons(FloorResult(commits_behind_main=12)), [])

    def test_main_changed_the_same_page_is_sent_back(self):
        reasons = send_back_reasons(FloorResult(pages_changed_on_main=["guides/a.mdx"]))
        self.assertEqual(len(reasons), 1)
        self.assertIn("F9", reasons[0])


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
