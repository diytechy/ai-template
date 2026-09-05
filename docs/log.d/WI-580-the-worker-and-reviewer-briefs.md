## 2026-09-04 — WI-580 the worker and reviewer briefs: batch assignment block, one-turn close bar, rows under review, scratch home

**Session.** Worker lane `wi-580-the-worker-and-reviewer-briefs`, base
`1af07567`. One reviewed diff of two shipped prompt templates plus the two
functions that fill them — the consolidation the row was minted for (three
absorbed rows, WI-559/560/562, each adding a line or a block to
`worker.template.md`, plus the batch finding of plan §0).

**What changed.**

1. **`{assignment_block}`, and an opening sentence that is true for a batch**
   (Done-when 2). `agent_loop.assignment_block` renders EVERY row the lane was
   claimed with — id, title, SpecRef — each tagged `this session's focus` /
   `built` / `not started`, and `worker_prompt` gained an `assigned` parameter
   the `session_body` call site fills from `worker["assigned"]`. The block is
   **empty for a one-row lane**, so the single-row render is what it was except
   for the opening sentence, which now names the branch and this session's
   focus row instead of asserting "ONE work item". The state vocabulary is the
   walk's own evidence (`train_evidence`), not a fourth opinion about doneness.
2. **`{wis}` in the reviewer brief** (Done-when 3). `reviewed_rows_block`
   renders the lane's claimed rows, id + title, so a round can map Done-when
   items to coverage instead of inferring scope from the diff. Filled by
   `str.replace` like the C7 slots, so an operator override without the slot
   renders unchanged; unlike those it renders even with no worker, because a
   literal `{wis}` in a brief that was actually sent is worse than an honest
   "not declared" line.
3. **The one-turn close bar** (Done-when 1, WI-559 item 1 as written). The
   close ritual now states that the close bar IS the commit bar — fast tier +
   wall budget + docs staleness, as `docs/stack.ini` declares them — that the
   full unfiltered suite is the lane REFRESH's job (in the merge slot, outside
   any session's turn, attested by its `Bar-Green:` trailer), and that ending a
   turn to await a suite is the measured stall generator that closed WI-540
   `partial`.
4. **Amended approved cells stale the approval brief too** (Done-when 4,
   WI-560 item 2). The regeneration clause now names an amendment of an
   already-approved cell alongside a mint, with the WI-538/LLR-206 measurement.
5. **The scratch home** (Done-when 5, WI-562 item 2). One rule bullet: scratch
   lives outside the worktree, never under `out/` (the unload refuses an
   undeclared file there by name), never as a stray untracked file.

**LLR-061 amended, and the brief's own new rule exercised on it.** The row's
`detail` enumerated what the worker prompt is assembled from, and that
enumeration became incomplete the moment the assignment block existed — the
stale-clause class this repo keeps finding on `Approved` rows. Amended in-lane
(text + `code_symbol`, no `Status` touched: the re-attest is the trunk-side
adjudication's, and `Modified` retired 2026-08-20), and the approval brief
regenerated at close — which is exactly what Done-when 4's new clause now tells
the next lane to do. LLR-045 was re-read and left alone: `{wis}` adds a fact to
the reviewer brief without falsifying any clause of "constructs redacted
prompt-map briefs", and the C7 slots are not enumerated there either.

**The module-size ratchet: a REVIEWED BUMP, +36 (2572 -> 2608).** Compacted
first (45 -> 36) per the phantom-overage rule, then bumped rather than
decomposed, and the reason is which module the code belongs to: both blocks
read `worker["rows"]`/`worker["assigned"]` and one reads `train_evidence`
against the lane base — the same three facts `worker_prompt`,
`reviewer_prompt` and `current_assignment_wi` already read in `agent_loop`, so
a new sibling module would export the loop's own session state only to import
it straight back. This cuts against the last two entries, which both ratcheted
DOWN by moving outward; the standing reduction of this module is owned by
WI-545, which declares WI-580 among its needs. Full reason in the baseline
comment (`tests/test_module_size_ratchet.py`).

**A note on "byte-identical".** Done-when 2's byte-identity clause is scoped to
the assignment mechanism — items 1, 4 and 5 add prose to the same template by
construction. What the test pins is the mechanism's own claim: for a one-row
lane `assignment_block` contributes nothing.

**Bar — and which one, because this row is about that.** The commit bar ran and
the full unfiltered suite ran too, in one turn (it fit; the new clause says to
run it only then).

<!-- fig: cmd="python -m pytest -q -n auto; python -m pytest -q -n auto -m smoke; python scripts/check_smoke_budget.py --mode enforce (twice); python project-trajectory/scripts/check_docs.py --root . --stale; python -m ruff format/check" rev=e2afbef0 -->

- Full suite: **3429 passed, 25 skipped, 1 failed in 976.8 s**.
- Smoke tier: **1547 passed, 8 skipped in 93.4 s**; `check_smoke_budget.py
  --mode enforce` **FAILS** at 94.0 s and again at 97.5 s against the 60 s
  budget. NOT re-stamped and NOT this row's to re-stamp: this diff adds **zero**
  tests to the tier — both modules it edits (`test_agent_loop_worker`,
  `test_agent_loop_review`) are in `conftest.SLOW_MODULES`, and `pytest -m smoke
  --collect-only` matches none of the new tests — so tier membership did not
  move. The box did: load average 9.3–10.8 with other lanes running, against a
  budget measured at 27–28 s on a quiet 24-core box (WI-496). Re-measure on a
  quiet box before anyone touches the number.
- `check_docs.py --root . --stale`: OK — 1368 docs, 1602 links, 0 broken.
  `ruff format` / `ruff check`: clean.
- The one failure is `test_derive_stage.py::test_this_repo_s_committed_stage_is_current`,
  and it is CAUSED-but-benign: `docs/requirements/low-level-requirements.toml`
  is a declared derivation input, so amending LLR-061 moved the fingerprint.
  Only the fingerprint moved — every derived value in `docs/stage` (`stage`,
  `settled-stage`, `live-stage`, both per-phase maps, `drafted = 9`) is
  byte-identical to the committed copy, so no rung and no draft count changed.
  Left alone deliberately: `docs/stage` is a generated artifact this branch may
  not hand-set, the harness's own `derived-stage` step SKIPS on a work branch
  ("generated freshness is the trunk lane's, concurrency-restructure §5.2"),
  and the trunk step regenerates it after the merge.

**Deferred open items:** none — the two advisory OIs joined to this row (OI-83,
OI-84) are about the coordinator's own launch/base derivation, not about the
briefs it composes, and nothing here touched either path.

