# ADJUDICATE — WI-674 — first approval at efa9e3c

The only question: is each row ready to be APPROVED as it stands? `Approved`
blesses the TEXT. It claims no test passed — but a cell that describes a test
the suite does not run, or a mechanism no test drives, is not blessable text,
so every clause was driven against the shipped module and the cited suite
rather than read for plausibility.

Scope: two rows, `LLR-259` (`low-level-requirements.toml`) and `TC-252`
(`test-cases.toml`), both `Drafted`, both Phase 6, under the already-`Approved`
`SR-139`. Everything else shown — SR-139, LLR-155/157/184/185/186,
TC-151/179/180/181, and the off-spine `IF-224` — is chain evidence and was read
as such; no cell of any of them is touched. The brief was rendered by the kit's
own composer (`adjudicate_brief.compose`, 31,624 chars, no refusal) and
followed.

What was verified independently, not taken from the chain:

- **The parent is SR-139, not SR-049.** SR-139's shall is the approval LEVEL —
  "a cumulative level naming the highest spine tier a human still approves" —
  and its rationale's failure that matters is "a machine approving something a
  human meant to hold". LLR-259 is that level's one owner-side consumer: it
  reads the level to decide which chains the owner signs and which an
  adjudicator does, and its two fail-safe clauses (one held row keeps the
  chain; no owing row keeps the chain) point the same way SR-139 demands.
  SR-049's shall is deriving the STAGE from artifact states; the only reason
  to offer it is that LLR-118 (the `gen_open_items` renderer) hangs there as
  "the rendered half of the regime whose gate SR-049 derives" — a legacy join,
  not a reason to add a second renderer row to a row about stage derivation.
  Read sideways under SR-139: LLR-155 owns the config reader and `human_holds`,
  LLR-157 the in-process tier, LLR-184/185/186 the ladder, the stage carrier
  and the effective stage. None renders the brief; LLR-259 overlaps none of
  them. Placement is correct.
- **Every `CodeSymbol` exists and reads as the cell says.** `released_tiers`
  (`trace.py:4186`) iterates `_KIND_IX` once and asks
  `agent_common.human_approves_spine(docs, SPINE_FILES[ix][0])` per tier;
  `grep SPINE_APPROVAL_RUNGS trace.py` finds nothing, so no rung table is
  held there. `dial_releases_chain` (`:4210`) is `bool(owing) and all(kind in
  released)` over rows with `drafted` set or `state` in
  `{changed, added, removed, drafted}` — exactly the cell's three-part rule.
  `reattest_lines` (`:4327`) renders held entries through `_entry_lines`,
  then `_waiting_lines`, which emits a `## Waiting for automated adjudication`
  heading, one `<details>` (no `open`), a `<summary>` carrying the label and
  the chain ids, and each released chain through the SAME `_entry_lines`.
  The title is "Re-attestation brief — spine rows owing an approval" and the
  signing instruction reads "Rule on each section outside the collapsed ...
  block (every section, when none renders)". With `released` empty no block
  renders. Every LLR-259 clause is TRUE of the code.
- **`IF-224` is cited, not allowlisted.** `TC-252.verifies` names it; `grep
  IF-224 tests/` finds only a comment in `test_import_layers.py:356` and the
  size-ratchet note — no allowlist entry. `human_approves_spine`'s three arms
  (mapped-held → True, mapped-released → False, unmapped → True) match
  IF-224's `data` cell. IF-224 itself is off-spine and `Drafted`; it is not in
  this act's scope and its `Status` is untouched.
- **The cited suite is green on this tip and the tier is justified.**
  `python -m pytest -q -n 2 tests/test_trace_briefs.py` → `31 passed in
  45.51s`; the four OI-82 tests by name → `4 passed in 6.85s`
  (`test_a_released_rungs_chain_renders_in_full_collapsed_under_its_label`,
  `test_the_shipped_default_dial_holds_every_chain_and_collapses_none`,
  `test_a_dial_releasing_every_rung_leaves_the_owner_a_stated_empty_ask`,
  `test_a_released_rungs_re_attestation_renders_its_diff_in_the_collapsed_block`).
  `test_trace_briefs` is in `tests/conftest.py` `SLOW_MODULES` (line 168), so
  `-m smoke` deselects it and `Full` is the cheapest tier at which the cited
  module runs; "in a module registered as slow" is true.
- **Every Method arm was opened against the suite**, because a Method that
  describes arms a suite does not contain is the failure mode this rung exists
  to catch. The held/released split at `DevStg-Reqs` with a Drafted-only chain
  inside the block, full text asserted (Requirement, Detail, Method lines), the
  Drafted-SR chain and the Drafted-SR-plus-Drafted-LLR chain outside; the
  title and scoped signing instruction; the amended-after-snapshot arm with
  LLR before/after and the TC removal inside and the SR's before/after
  outside; the no-dial arm with no `<details` and every heading present; the
  every-tier-released arm with the stated empty ask — each is asserted as the
  cell says. ONE arm is not: see the TC-252 finding.
- **No `WI-`/`OI-`/review-round citation** in either cell.

Findings that drive the verdict:

1. **TC-252 Method, last sentence: "The freshness check passes on each written
   brief."** Four briefs are written; `_check` runs on two
   (`test_trace_briefs.py:1072` and `:1181`). The no-dial arm (`:1075-1092`)
   and the every-tier-released arm (`:1094-1104`) write a brief and never read
   it back through `--check`. The sentence overstates the suite by exactly the
   two arms whose rendering differs most from the split brief (no block at
   all; a block with an empty owner's section). This is the class arbitration
   ruling 13 already returned these rows for once — a cell sentence the
   evidence does not support — and the fix is two lines either way: add
   `assert _check(tmp_path).returncode == 0` to both arms (the stronger
   remedy) or narrow the sentence to the two briefs it is true of.
2. **LLR-259 Detail: "with the chains' ids in its summary"** is a clause no
   test verifies. The one summary assertion in the suite
   (`test_trace_briefs.py:1047`) checks the LABEL before `</summary>`; the ids
   are only asserted inside the whole `<details>` body, where the chain
   headings would satisfy the assertion with an empty summary. A design row
   whose test cannot tell the stated summary from a bare label leaves that
   clause unverified — "does anything it says go unverified?" answers yes.
3. **LLR-259 Detail omits a decision TC-252 enforces.** When every owing chain
   is released, `reattest_lines` (`:4432-4437`) writes "_No chain on a rung the
   human-approval dial holds owes an act; every chain in this brief waits for
   automated adjudication._" in the owner's section, and TC-252's Method and
   the every-tier-released test assert it. LLR-259 says only "the held ones in
   the owner's section as before" — a builder implementing the row literally
   emits an empty owner's section above a collapsed block, a brief that reads
   as nothing owed, which is the misreading the code's line exists to prevent
   and the reason the test docstring gives ("rather than reading as an empty
   brief"). The test verifies a decision the design row does not record; the
   row should state it in one clause.

Two observations recorded and deliberately NOT findings: LLR-259's "asks ...
once per spine tier" (once per rendering, not once per row) is true of the
comprehension but no test counts calls — its failure direction is a repeated
migration note, benign; and the `## Waiting for automated adjudication`
heading precedes the block with an italic line explaining the split, which the
row's "a heading and one details block" covers.

Why both rows return rather than LLR-259 alone: nothing in LLR-259 is false of
the code, and on findings 2 and 3 alone an approve-now, amend-later course was
weighed. It was rejected because the lane is owed regardless for finding 1,
and a one-clause amendment to an approved LLR-259 would then drift it and owe
a second adjudication of its own; the design and test halves of this seam are
one gap seen from two sides (finding 2 is fixed in TC-252's suite, finding 3
in LLR-259's cell, and the Method sentence of finding 1 sits between them).
They return together and come back together.

- [RETURN] LLR-259 -> a builder must ship, in `trace.py`, a dial reader that asks `human_approves_spine` once per spine tier through `SPINE_FILES` and holds no rung table, a per-chain predicate that releases a chain only when every owing row (Drafted, or changed/added/removed against the snapshot) sits on a released tier, and a brief renderer that keeps held chains in the owner's section, sets released chains apart in full inside one closed `<details>` block labelled "Waiting for automated adjudication" with the ids in its summary, claims no human act in its title, scopes its signing instruction to the sections outside the block, and renders no block when no tier is released -> parent SR-139 calls for exactly this consumer of the approval level and its fail-safe direction; the five siblings own the reader, the tier axis and the ladder and none renders the brief; IF-224 declares the seam and is cited by TC-252; every named symbol exists and every clause is true of the code; the cited suite is green -> not ready as it stands: the ids-in-summary clause is verified by no assertion (finding 2), and the stated-empty-owner's-section line the code emits and TC-252 asserts is a decision this row does not record (finding 3); both are one-clause fixes and they land with the paired TC-252 return.
- [RETURN] TC-252 -> a test author must drive `trace.py --approve modified` on temporary repositories writing `docs/ratify/CURRENT.md`, in a slow-registered module, through a held-SR/released-LLR-and-TC dial with a Drafted-only chain in the block and two held chains outside, the neutral title and scoped instruction, an amended-after-snapshot pair split by tier, the no-dial rendering with no block, the every-tier-released rendering with the stated empty ask, and the freshness check on each brief written -> it verifies SR-139, LLR-259 and IF-224; `Level`/`Tier`/`Automated`/`Evidence` are unambiguous and the `Full` tier is earned by `SLOW_MODULES` membership; seven of its eight Method arms map onto assertions in the cited module and `31 passed` on this tip -> not ready as it stands: the eighth arm, "The freshness check passes on each written brief", is false for two of the four briefs the suite writes (finding 1) — a cell claiming a check the test does not run is the sentence class this pair was already returned for once.

OUTCOME: RETURN rows=2

## Dispositions

Drafted in the spec of record (`docs/work/queued/WI-674-adjudicate-llr-259-tc-252.md`,
`## Dispositions`), one fenced block, minted at this row's merge.
