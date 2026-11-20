#!/usr/bin/env python3
"""Tests for the comparison of findings against a base."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_new_findings import CheckDidNotRun, parse_broken_links

OUTPUT = """found 3 broken links in 2 files
api-reference/getting-started/authentication-overview.mdx
 ⎿  ./getting-started.md
guides/a/advocate-invite-email-asset-guide.mdx
 ⎿  <https://success.extole.com/en/articles/11932190-add-a-promotion-onsite-call
-to-action-or-marketing-email?q=add+a+cta>
 ⎿  <https://my.extole.com/programs>
"""


class BrokenLinkParseTests(unittest.TestCase):
    def test_pairs_each_link_with_its_page_and_joins_wrapped_lines(self):
        self.assertEqual(parse_broken_links(OUTPUT), {
            "api-reference/getting-started/authentication-overview.mdx  ./getting-started.md",
            "guides/a/advocate-invite-email-asset-guide.mdx  <https://success.extole.com/en/articles/"
            "11932190-add-a-promotion-onsite-call-to-action-or-marketing-email?q=add+a+cta>",
            "guides/a/advocate-invite-email-asset-guide.mdx  <https://my.extole.com/programs>",
        })

    def test_reported_links_that_cannot_be_read_mean_the_check_did_not_run(self):
        changed_format = "found 2 broken links in 1 file\n- guides/a.mdx -> /nowhere\n- guides/a.mdx -> /gone\n"
        with self.assertRaises(CheckDidNotRun):
            parse_broken_links(changed_format)

    def test_no_findings(self):
        self.assertEqual(parse_broken_links("success no broken links found\n"), set())

    def test_output_with_no_result_line_means_the_check_did_not_run(self):
        with self.assertRaises(CheckDidNotRun):
            parse_broken_links("npm error code ETARGET\nnpm error notarget No matching version found\n")


if __name__ == "__main__":
    unittest.main()
