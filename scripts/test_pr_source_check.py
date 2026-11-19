"""Tests for reading the private source check's comment."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import source_check
from pr_floor import FloorResult
from pr_judge import apply_verdict_steps

HEAD = "a" * 40
OTHER_HEAD = "b" * 40


def comment(head=HEAD, claims=None, author=source_check.VERIFIER_AUTHOR, failed=False, payload_head=None):
    payload = {"head": payload_head or head, "claims": claims or [], **({"failed": True} if failed else {})}
    body = f"<!-- docs-claim-verifier head={head} -->\nSource check.\n<!-- docs-claim-verifier-claims\n{json.dumps(payload)}\n-->"
    return {"user": {"login": author}, "body": body}


CONTRADICTED = {
    "sentence": "The job's page runs two reports for that job:",
    "status": "contradicted",
    "repository": "showtime",
    "supported_sentence": "The job's page runs three reports for that job.",
}


class FromCommentsTests(unittest.TestCase):
    def test_reads_the_check_for_the_head(self):
        check = source_check.from_comments([comment(claims=[CONTRADICTED])], HEAD)
        self.assertEqual(check.claims[0]["status"], "contradicted")
        self.assertFalse(check.failed)

    def test_ignores_a_comment_by_anyone_else(self):
        self.assertIsNone(source_check.from_comments([comment(claims=[CONTRADICTED], author="ekthayer")], HEAD))

    def test_ignores_a_check_of_an_older_head(self):
        self.assertIsNone(source_check.from_comments([comment(head=OTHER_HEAD)], HEAD))

    def test_ignores_a_payload_naming_a_different_head(self):
        self.assertIsNone(source_check.from_comments([comment(payload_head=OTHER_HEAD)], HEAD))

    def test_reports_a_check_that_did_not_finish(self):
        self.assertTrue(source_check.from_comments([comment(failed=True)], HEAD).failed)

    def test_drops_a_claim_with_an_unknown_status(self):
        check = source_check.from_comments([comment(claims=[{**CONTRADICTED, "status": "approved"}])], HEAD)
        self.assertEqual(check.claims, [])


class JudgeClaimsTests(unittest.TestCase):
    def test_names_the_repository_and_the_supported_sentence(self):
        rows = source_check.judge_claims(source_check.SourceCheck(claims=[CONTRADICTED], failed=False))
        self.assertEqual(rows[0]["source"], "showtime; the source supports: The job's page runs three reports for that job.")

    def test_a_contradicted_claim_sends_the_pull_request_back(self):
        rows = source_check.judge_claims(source_check.SourceCheck(claims=[CONTRADICTED], failed=False))
        verdict = apply_verdict_steps({"verdict": "merge-floor", "claims": rows, "reasons": []}, FloorResult())
        self.assertEqual(verdict["verdict"], "send-back")
        self.assertIn("three reports", " ".join(verdict["send_back"]))

    def test_verified_claims_do_not_hold_the_pull_request(self):
        rows = source_check.judge_claims(source_check.SourceCheck(claims=[{**CONTRADICTED, "status": "verified", "supported_sentence": ""}], failed=False))
        verdict = apply_verdict_steps({"verdict": "merge-floor", "claims": rows, "reasons": []}, FloorResult())
        self.assertEqual(verdict["verdict"], "merge-floor")


if __name__ == "__main__":
    unittest.main()
