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

### Rework pass (session 005) — REVIEW-A MAJOR: runtime close-command path

The worker close ritual inherited literal `scripts/trace.py` and
`scripts/spec_move.py` commands, which work in a scaffold but not in this
meta-repo (where the shipped scripts live in `project-trajectory/scripts/`).
The root cause was not either command: `worker_prompt` omitted the runtime
scripts-directory slot that `reviewer_prompt` already resolves at its sole
composition boundary. Added `{scripts}` to the worker template and supplies it
from `scripts_dir(root)` in `worker_prompt`; both close commands now use it.
The regression test composes real prompts for the meta-repo and a scaffold,
and asserts each receives its executable pair of commands. The prompt catalogue
was regenerated.

Focused verification: the new regression passes (`1 passed in 0.09s`) and
formatting passes. A fresh temporary lint tool reports 98 pre-existing
whole-file style findings under its newer default ruleset; none refers to this
change, so it is not a repair target for WI-580. The declared test environment
is absent from this checkout (`python` is unavailable and system `python3`
has no pytest), so the full commit bar cannot be reproduced here; the final
review round will judge this new non-record tree.


### Rework pass (session 003) — REVIEW-A MAJOR: the brief's half-predicate

`assignment_block` derived doneness from the committed `WI:` trailer alone
while `current_assignment_wi` had already been taught the two-part test (the
trailer AND the spec gone from `active/<branch>/`, the WI-589 stranding). Two
derivations of one question, so a batch that committed a trailer and ran out of
budget before its close ritual rendered that row `[built]` to the very session
the walk was sending back to it.

- **The fix is a consolidation, not a patch:** `lane_completion(root, base)`
  returns `(built, done)` and is now the single home of the predicate; the walk
  asks it (two lines shorter than the copy it dropped) and the brief asks the
  same call. A row can no longer be `built` in the brief and unfinished to the
  walk, because there is one set to be in.
- **A third display state, `started, not closed`,** for the trailer-only rows
  the honest predicate now makes visible — labelling them `not started` would
  have replaced a false "done" with a false "untouched" and sent the next
  session to redo committed work.
- **Regression test** `test_the_brief_never_calls_an_unclosed_row_built`
  (tests/test_agent_loop_worker.py): two trailers committed, both specs still
  in `active/`, and the non-focus row must read `started, not closed`; the same
  row reads `built` once its spec is moved out. Carries the mutation note — on
  the trailer-alone predicate the first assertion reads `[built]`.
- **LLR-061's `detail` amended** to state the predicate the brief reads, not
  just the vocabulary it prints (the old cell enumerated three states and said
  nothing about where they came from — the gap that let the defect look
  conformant); `docs/ratify/CURRENT.md` regenerated.
- **Baseline:** `agent_loop.py` 2608 -> 2609 SLOC, a reviewed +1 stamped with
  its reason in `tests/test_module_size_ratchet.py`. Compacted first per the
  phantom-overage rule (the nested-ternary rendering went to a state map).
- **Green:** `test_agent_loop_worker.py`, `test_agent_loop_review.py`,
  `test_module_size_ratchet.py` — 78 passed in 44.5 s; `ruff format` /
  `ruff check` clean; `check_docs.py --root . --stale` OK (1369 docs, 1602
  links, 0 broken). The full smoke bar now PASSES enforcement on a quieter box:
  `pytest -q -n auto -m smoke` 1551 passed / 4 skipped in 61.0 s, and
  `check_smoke_budget.py --mode enforce` timed its own run at **52.9 s vs the
  60 s budget -> within** (load average 2.9, against the 9.3–10.8 that produced
  the 94.0/97.5 s readings above). Same tier membership, quieter box — which is
  the reading that was owed. The `docs/stage` fingerprint red is the same
  CAUSED-but-benign one recorded above (LLR-061 amended again), and for the
  same reason it is the trunk lane's to regenerate.

### Rework pass (session 007) — REVIEW-A blocker and prose reconciliation

The independent round found four record/ritual defects, all in the existing
mechanisms rather than the brief behavior. The line-count row was not
re-stamped after the runtime `{scripts}` composition line landed; the
always-read `CLAUDE.md` still made the full suite a per-WI close obligation
despite the shipped brief and `PROCESS_OPTIONS.md` assigning mid-phase slices
the commit bar; the template note counted eleven of its twelve slots; and the
absorbed WI-559 item 3 had no named discharging row.

The rework re-stamps `agent_loop.py` at 2610 SLOC with a reason covering both
review fixes, aligns `CLAUDE.md` to the existing phase cadence (commit bar for
a mid-phase WI, the stage-declared refresh bar in the merge slot, full suite at
phase close), corrects the slot count, and records that WI-579 discharged
WI-559 item 3. No new check or defensive path was added: the ratchet already
made the unstamped line fail closed, and the prose now has one phase-cadence
rule instead of two contradictory obligations.

Verification: the reviewer's exact focused harness is **79 passed**; the
focused regression/baseline selection is **6 passed**, and the three
byte-budget checks are **3 passed**;
<!-- fig: cmd="python -m pytest tests/test_agent_loop_worker.py tests/test_agent_loop_review.py tests/test_module_size_ratchet.py -q; python -m pytest tests/test_module_size_ratchet.py tests/test_agent_loop_worker.py tests/test_agent_loop_review.py tests/test_bootstrap.py -q -k 'module_sizes_exactly_match or worker_brief_names or reviewer_prompt_names or runtime_scripts_path or byte_caps or size_budget'; python -m pytest tests/test_bootstrap.py -q -k 'byte_caps or size_budget or capped_doc_baselines'; python scripts/check_smoke_budget.py --mode enforce; python project-trajectory/scripts/check.py --jobs 0; python project-trajectory/scripts/trace.py --strict-integrity; python project-trajectory/scripts/check_docs.py --root . --stale" rev=97f0b684 -->
`check.py --jobs 0` is **PASS** (the three work-branch generated-freshness
steps skipped by policy); `trace.py --strict-integrity` reports SN=27, SR=76,
LLR=191, TC=190, orphans=0, integrity=0; `check_docs.py --root . --stale` is
OK (1371 docs, 1602 links, 0 broken); and the prompt catalogue is fresh. The
smoke tests are functionally green (**1551 passed, 4 skipped**). Three loaded
readings were 87.66 s, 81.5 s and 98.9 s against the 60 s wall budget and
correctly failed enforcement while other checkout work was active; after that
work cleared, the authoritative enforced run passed at **52.9 s vs 60 s**. The
budget remained untouched.

Byte deltas: `CLAUDE.md` 7886 -> 7975 (525 bytes headroom under its 8500-byte
cap); `project-trajectory/skills/byte-budget-guard/SKILL.md` and each tracked
copy 4847 -> 4781 (219 bytes headroom under the source's 5000-byte cap).

### Rework pass (session 009) — what the close bar claims, and the one cadence home

REVIEW-A round 008 found five defects, two of them MAJOR and both the same
shape: a sentence asserting a bar that does not run.

**The close bar's claim.** The brief excused the worker from the full suite
because "the lane's own refresh runs the full declared bar for you". Driven,
not read: `integrate._run_bar` calls `check.py --tier all`, and `check.py`'s
step table declares `format` / `lint` / `tests+coverage` relevant from
`_kitladder.STAGE_IMPL`, while `docs/stage` here reads `DevStg-Tests` (one rung
below). `check.py --jobs 0` at this tip returned `RESULT: PASS` over fourteen
steps — registry-integrity, vocabulary, need-form, privacy, doc-navigability,
design-flows, trajectory, skills-index, prompt-catalog, staged-divergence,
approval-immutable, and three work-branch freshness SKIPs — and NOT ONE of them
a test step. So the sentence excused a worker from the only suite that would
have run between the smoke commit bar and phase close. The brief now says the
bar declared for the repo's CURRENT RUNG, names `DevStg-Impl` as where the
product test step arrives, and sends the reader to `check.py`'s step table
rather than restating it — the step table stays the one owner of what the bar
runs. The rung gating is deliberately untouched: ungating `tests+coverage`
would migrate every adopter and is an owner's call.

**The cadence's second home.** Session 007 removed "before claiming a WI/slice
done" from `CLAUDE.md` but left the `session-protocol` skill saying "before
claiming a slice/phase done, at close" — and `CLAUDE.md` points AT that skill
as the authority for commit bar vs gate bar, so the delegated home contradicted
its delegator, the shipped brief, and its own next-but-one sentence ("A per-WI
slice inside a phase ends at the commit bar"). Deleted from all three copies.
`PROCESS_OPTIONS.md` "Phase cadence" is now the only home; the deletion is the
antidote, so nothing new polices it.

**The absorbed item.** The previous round narrowed this row's own acceptance
heading to "items 2 and 3 were discharged by WI-579", but WI-579's heading says
item 3 is SHARED with WI-580 and its Done-when list never claims it. Heading
restored verbatim, and the uncovered half is now covered rather than
reclassified: `test_the_false_partial_class_turns_only_on_the_close_ritual`
drives the WI-540 class on one scaffold — every trailer committed, every spec
still in `active/<branch>/`, so `lane_completion` answers `({WI-201, WI-204},
set())` and `integrate.finished_branches` answers `[]` (the `_lane_close` stall
arm, not the refresh arm); the spec move alone flips both to done and
`["wi-batch"]`. The `== []` is not an empty scan — the same call on the same
scaffold answers `["wi-batch"]` four lines later. Mutation check: restoring the
pre-WI-580 trailer-alone predicate (`return built, built`) fails it at
`assert {'WI-201','WI-204'} == set()`.

Also corrected: the byte-accounting prose said `CLAUDE.md` "holds ~8%" against
a baseline its own edit had moved (7,975 of 8,500 is 6.2%), now `~6%`; and the
worker brief's opening sentence still named the literal `scripts/agent_loop.py`
that the same commit had routed through `{scripts}` everywhere else.
