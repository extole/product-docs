#!/usr/bin/env python3
"""Tests for deterministic docs PR floor checks."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from closing_references import armed_references
from pr_floor import (
    MAXIMUM_PAGES_PER_SUBJECT,
    FloorResult,
    added_subjects,
    deleted_sentences,
    grep_matches,
    preview_host,
    preview_host_from_comments,
    scan_internal_terms,
    scan_remote_assets,
    send_back_reasons,
    subjects_on_other_pages,
)
from pr_judge import apply_verdict_steps, before_review


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
    def test_show_expert_and_expert_setting_are_not_internal_terms(self):
        added = "This is an expert setting. To see it, turn on **Show Expert**."
        self.assertEqual(scan_internal_terms(added, "guides/foo.mdx"), [])

    def test_account_link_with_client_id(self):
        added = "Open the [report](https://my.extole.com/reports?client_id=1063468100#/)."
        hits = scan_internal_terms(added, "guides/foo.mdx")
        self.assertTrue(any("client-id" in hit for hit in hits))

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


class SubjectOnOtherPageTests(unittest.TestCase):
    SECTION_ADDED_TO_EXISTING_PAGE = "\n".join([
        "+## Standard Rules in Flow Builder Campaigns",
        "+| Quality Rule | Description |",
        "+| :--- | :--- |",
        "+| Share Email Limit | Limits the share emails a person can receive. |",
        "+The **Business Event Quality** reward rule stops it.",
        " | Untouched Row | stays as it was |",
        "-| Removed Row | is not a subject |",
    ])

    def test_added_section_names_its_heading_bold_terms_and_table_rows(self):
        self.assertEqual(
            added_subjects(self.SECTION_ADDED_TO_EXISTING_PAGE),
            {
                "Standard Rules in Flow Builder Campaigns",
                "Quality Rule",
                "Share Email Limit",
                "Business Event Quality",
            },
        )

    def test_short_and_numeric_cells_are_not_subjects(self):
        self.assertEqual(added_subjects("+| On | 30 |\n+| 2026 | yes |"), set())

    def test_subject_on_another_page_is_found_and_the_page_itself_is_not(self):
        lines = {
            "Share Email Limit": [
                ("guides/flow-campaigns/default-business-event-quality-rules.mdx", "| > Share Email Limit | > Shared |"),
                ("product/rules-quality.mdx", "| Share Email Limit | Limits |"),
            ],
        }
        found, too_common = subjects_on_other_pages(
            {"product/rules-quality.mdx": {"Share Email Limit"}},
            lambda subject: lines.get(subject, []),
        )
        self.assertEqual(
            found,
            {"guides/flow-campaigns/default-business-event-quality-rules.mdx": {
                "subjects": ["Share Email Limit"],
                "lines": ["| > Share Email Limit | > Shared |"],
            }},
        )
        self.assertEqual(too_common, [])

    def test_grep_match_keeps_a_line_that_holds_a_unicode_line_separator(self):
        output = "abc123:product/a.mdx:promote advocacy,\u2028and limit shares\nabc123:guides/b.mdx:Program\n"
        self.assertEqual(
            grep_matches(output),
            [
                ("product/a.mdx", "promote advocacy,\u2028and limit shares"),
                ("guides/b.mdx", "Program"),
            ],
        )

    def test_subject_on_many_pages_is_reported_as_too_common(self):
        many = [(f"guides/page-{index}.mdx", "Reward Rule") for index in range(MAXIMUM_PAGES_PER_SUBJECT + 1)]
        found, too_common = subjects_on_other_pages({"product/a.mdx": {"Reward Rule"}}, lambda subject: many)
        self.assertEqual(found, {})
        self.assertEqual(too_common, [f"Reward Rule ({MAXIMUM_PAGES_PER_SUBJECT + 1} pages)"])

    def test_review_note_names_the_page_and_its_subjects(self):
        floor = FloorResult(subjects_on_other_pages={
            "guides/a.mdx": {"subjects": ["Mass Share Limit", "Share Email Limit"], "lines": []},
        })
        self.assertIn(
            "`guides/a.mdx` already names **Mass Share Limit**, **Share Email Limit**.",
            before_review(floor),
        )


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
