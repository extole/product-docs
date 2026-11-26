"""Tests for the judge's handling of a reply that is not JSON."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pr_judge import unparsed_reply


def response(stop_reason, output_tokens):
    usage = SimpleNamespace(input_tokens=1200, output_tokens=output_tokens,
                            cache_read_input_tokens=900, cache_creation_input_tokens=None)
    return SimpleNamespace(stop_reason=stop_reason, usage=usage)


class UnparsedReplyTest(unittest.TestCase):

    def test_names_the_stop_reason_and_the_output_tokens(self):
        verdict = unparsed_reply(response("max_tokens", 6000), '{"verdict":"merge-floor","claims":[{"sentence":"cut')

        self.assertEqual(verdict["verdict"], "needs-human")
        self.assertTrue(verdict["failed_closed"])
        self.assertEqual(verdict["reasons"][0],
                         "The reply stopped with stop_reason `max_tokens` after 6000 output tokens, 51 characters.")
        self.assertEqual(verdict["reasons"][1], '{"verdict":"merge-floor","claims":[{"sentence":"cut')

    def test_counts_the_tokens_the_failed_reply_spent(self):
        verdict = unparsed_reply(response("end_turn", 40), "not json")

        self.assertEqual(verdict["usage"], {
            "input_tokens": 1200,
            "output_tokens": 40,
            "cache_read_input_tokens": 900,
            "cache_creation_input_tokens": 0,
        })

    def test_says_when_the_reply_is_empty(self):
        verdict = unparsed_reply(response("refusal", 0), "")

        self.assertEqual(verdict["reasons"][1], "(empty response)")


if __name__ == "__main__":
    unittest.main()
