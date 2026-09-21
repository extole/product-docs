# Docs PR rubric — v1

How a pull request against this repository is sorted into `minor` and `needs-human-review`.
`scripts/pr_judge.py` reads this file and `.mintlify/AGENTS.md` on every run, so a change here
is a change to how every later pull request is labelled.

**The label is a routing hint, not a verdict on quality and not permission to merge.** `main`
still requires a green `validate` and one approving review, and nothing in this repository
merges a pull request automatically.

## What each label claims

**`minor` — one short check settles this.**

The change edits a page that already exists, stays inside that page's existing subject, and
asks the reviewer to confirm at most one thing. A reviewer can finish it in a couple of minutes
without leaving the page it touches.

**Almost every docs change asserts something about the product**, because that is what a docs
change is for. So "it makes a claim" is not by itself a reason to escalate. What separates one
change from another is **how much there is to check, and what it costs to be wrong** — not
whether a claim is present.

**`needs-human-review` — settling this needs more than one short check.**

The reviewer must open the product, the navigation, or other pages, or weigh several separate
claims, to know whether the change is right. Plenty of good work lands here; it is a statement
about the size of the read, not about the quality of the change.

## Any one of these makes it `needs-human-review`

Each is a question a reader of the diff cannot answer on their own.

1. **A new page, a moved page, or a renamed page.** Placement is chosen by *who performs the
   work*, and `.mintlify/AGENTS.md` says plainly that Guides is the largest tab and the wrong
   default. Only a person can confirm the actor test was run. A move also owes a `url-map.json`
   entry.
2. **Any change to `docs.json`.** Navigation is the one error class CI is structurally blind
   to: a valid page absent from `docs.json` ships unreachable with no error and no warning.
3. **More than one separate product claim to check**, or a single claim that is expensive to
   get wrong. A claim is expensive when it **reverses guidance already published** (a
   troubleshooting cause removed, "must" turned into "need not"), when it states a limit, a
   timing, or a monetary or reward consequence, or when acting on it wrongly would leave a
   reader's campaign broken. One ordinary new fact on an existing page is not this.
   Accuracy remains the repository's non-negotiable, and the standard still says to say you
   are unsure rather than write something plausible — this decides how long the check is, not
   whether accuracy matters.
4. **A literal changed** — an event name (`promotion clicked`, `converted`), a schema field
   (`step_name`), an API identifier, or anything inside a code sample. Style rules do not reach
   inside literals, so an edit to one is either a real correction or a real bug.
5. **A rewrite that changes what the page is about**, as opposed to how it reads. Replacing a
   section, re-ordering an argument, or changing whom the page addresses.
6. **An image or link added or repointed**, including a `<Frame>` or an `img` src. Whether the
   target is the right page, and whether the asset is a repo asset rather than a remote URL,
   needs checking against the tree.
7. **A change to the standards or the agent configuration** — `.mintlify/AGENTS.md`,
   `AGENTS.md`, `.agents/`, `.github/`, `scripts/`, `url-map.json`. These govern every later
   change, so they are reviewed as mechanism, not as prose.
8. **A diff too large to read in full.** If the judge's input was truncated, it did not see the
   change, and a label based on part of a diff is a guess.
9. **Anything the judge is unsure about.** Unsure is `needs-human-review`, always. A false
   `needs-human-review` costs one read; a false `minor` sends an unreviewed claim to the live
   customer site.

## What is left, and is `minor`

Two shapes.

**A single fact added to a page that already covers the subject.** One or two sentences, or a
short callout, telling a reader something true about a feature the page is already about. This
is the common shape in this repository and it is `minor` even though a reviewer must confirm
the fact — confirming one fact on one page is the short check this label describes. It stops
being `minor` as soon as it brings a second independent claim, reverses published guidance, or
carries a limit, a timing, or a reward consequence.

**Prose repair** inside an existing page, on its existing subject, conforming to the standards.
In practice:

- Grammar, spelling, and typo fixes.
- De-hedging against the list in `.mintlify/AGENTS.md` (`in order to`, `just`, `simply`,
  `note that`, `please note`, `very`, `keep in mind`, `really`, `essentially`).
- Terminology swaps toward the **Preferred** column of the glossary, in prose only.
- Formatting brought to the standard: bolding a UI element instead of quoting or backticking
  it, `##` headings instead of bold pseudo-headings, Title Case in a title, the number rules,
  a Mintlify callout component in place of a `>` blockquote.
- Tightening a sentence without changing what it asserts.

## The revealed standard

`.mintlify/AGENTS.md` is what this repository *says*. This section is what its reviewers have
actually done, with receipts. It is thin on purpose: the whole repository holds **7** inline
review comments, and the docs owner has left none, so these are the corrections that exist
rather than a representative sample.

Treat each as a `needs-human-review` trigger when the diff introduces the pattern, and as
supporting evidence in `standards_notes` otherwise.

**A procedure must be followable without reverse-engineering it.**
In [#128](https://github.com/extole/product-docs/pull/128) the docs owner rewrote *"Replace the
'MY_ID' from Step #3.2 above, and 'MY_TOKEN' with the Token from Step #2.2 above"* as *"Replace
`MY_ID` with the Bank Identifier from the previous item, and `MY_TOKEN` with the access token
from Step 2"*. A step that names a value the reader has to hunt for is not finished.
On [#127](https://github.com/extole/product-docs/pull/127) `amsuro` left three `suggestion`
blocks, every one of them adding the missing precondition or consequence to a step: which mode
to create the key in, that the token cannot be viewed again, that coupons must exist in Stripe
first.

**Stop justifying that the feature exists.**
`kzeisel` on [#46](https://github.com/extole/product-docs/pull/46): *"I feel like this section
is trying to justify why this exists. We should just say. We support this. Here are some use
cases where you would want to use this. Here is how to do it."*

**A term the reader may not know should link to where it is defined.**
`kwburgess` on [#115](https://github.com/extole/product-docs/pull/115), asking whether someone
is expected to know what a reward bank collectible reward, Flow Builder, or a reward supplier
is without a reference.

**A link to our own docs is a site path, not a `docs.extole.com` URL.**
[#128](https://github.com/extole/product-docs/pull/128) replaced
`https://docs.extole.com/docs/how-to-create-a-promo-link` with
`/guides/platform-overview/implementing-your-referral-program/creating-ctas/how-to-create-a-promo-link`,
and a full URL to an anchor on the same page with `#prerequisites`.

**UI elements are bold, and the label must be the one on the screen today.**
The same pull request turned `` `Security` > `Create Access Token` `` into **Security Center**
and **+ New Access Token** — both a formatting fix and a correction of a label that had moved
on. A UI label in a diff is worth checking against the product.

## Output

The judge returns one object:

- `verdict` — `minor` or `needs-human-review`.
- `one_line` — one sentence a reviewer reads first.
- `triggers` — zero or more of `new-or-moved-page`, `nav-change`, `product-claim`,
  `literal-change`, `scope-change`, `link-or-image`, `standards-or-config`, `diff-truncated`,
  `unsure`. Every `needs-human-review` carries at least one.
- `reasons` — why, each naming what in the diff caused it.
- `standards_notes` — advisory observations against `.mintlify/AGENTS.md`. These never change
  the verdict, and a `minor` pull request may carry several.

## Calibration

**This rubric has not been checked against a person.** It is version 1, and the open queue is
being labelled so the docs owner can say where the labels are wrong. Disagreement is the
evidence that revises this file, and the label exists to collect it.

What is measured so far, on `claude-opus-5`, before any human has seen a verdict:

- **11 open pull requests sampled: 11 `needs-human-review`, 0 `minor`.** Sampled across authors
  and sizes (#99, #105, #109, #111, #130, #137, #143, #146, #161, #162, #164). Two drafts of
  this rubric produced the same 11, so the second draft did not move it.
- **The label does discriminate.** A control on merged work returned `minor` for
  [#134](https://github.com/extole/product-docs/pull/134), a mechanical conversion of 46
  `<Frame>` captions across 16 pages, while [#128](https://github.com/extole/product-docs/pull/128),
  [#135](https://github.com/extole/product-docs/pull/135) and
  [#112](https://github.com/extole/product-docs/pull/112) came back `needs-human-review`. Size
  is not what it keys on: #134 is the largest of the four.
- **So the base rate is a fact about the queue, not a broken rubric.** 48 of the 60 pull
  requests open on 2026-09-21 were opened by Ada, and each exists to add a product fact the
  diff cannot evidence — several of them narrowing or reversing guidance already published.
  That population is genuinely almost all `needs-human-review`.

Two consequences worth knowing before trusting a verdict. A label that is nearly always the
same routes little, so **the `reasons` and `triggers` are doing more work than the label** —
they are a reading route into a specific pull request. And `triggers` are not yet stable: the
same pull request judged twice returned `product-claim` once and `product-claim,
literal-change` the next time, with the verdict unchanged both times.

When this file changes, raise the version at the top and say in the pull request which
disagreement drove it.
