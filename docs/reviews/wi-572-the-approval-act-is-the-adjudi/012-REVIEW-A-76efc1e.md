## 2026-09-02 — WI-572 REVIEW-A (independent, round 3)

Scope: `git diff contract_split...HEAD` minus telemetry/verdicts/generated. Requirement
surface read: the archived spec `docs/archive/work/complete/WI-572-the-approval-act-is-the-adjudi.md`,
PROCESS.md §4, PROCESS_OPTIONS.md "Who performs the approval act", and the cited rows
(IF-091, LLR-158, OI-45, SR-178).

Instruments, run here, once each:

- `python project-trajectory/scripts/check.py --jobs 0` — `RESULT: PASS`
  (registry-integrity / vocabulary / need-form / privacy / doc-navigability /
  skills-index / prompt-catalog / staged-divergence / approval-immutable PASS;
  derived-stage + approval-fresh SKIP, work branch).
- `python project-trajectory/scripts/trace.py --strict-integrity` —
  `Traceability: SN=27 SR=76 LLR=188 TC=187 orphans=2 integrity=0 ... provenance-findings=1`
  (the one provenance finding is LLR-197/WI-448, untouched by this diff).
- `python -m pytest -q -n auto -m smoke` — **`1 failed, 1455 passed, 8 skipped in 21.47s`**
  (see finding 2); `scripts/check_smoke_budget.py --mode enforce` —
  `smoke wall-clock budget: 21.9s vs 60s budget -> within`.
- Targeted: `pytest -q tests/test_adjudicate_brief.py tests/test_integrate_admission.py
  tests/test_intake.py tests/test_approval_level.py` — `213 passed`.

Drove the shipped paths, not probes: called `adjudicate_brief.first_approval_values`,
`acceptance_record.{staged_approval_acts,staged_drafted_rows,lane_approval_refusal}` and
`intake._released_drafted_rows` against this repo and against the recorded census commit.
The spec's census claim reproduces exactly — `staged_approval_acts('.', '580df781~1',
'580df781')` returns the four flips (LLR-203, LLR-204, TC-199, TC-200), no more.
Both round-2 regression tests were confirmed to fail on the pre-fix behaviour: reverting the
`entered_drafted` arm in `staged_drafted_rows` reds
`test_a_status_only_withdrawal_mints_first_approval_adjudication` and
`test_born_and_withdrawn_drafted_rows_reach_first_approval_not_refusal`.

Done-when map: Deliverable 1 covered (5 merge-slot + 4 reader tests); 2 covered at the
trigger (4) and the brief (6) EXCEPT the mint/brief scope equality, which is UNCOVERED
(finding 1); 3 covered by `test_the_MEANING_aftermath_is_DERIVED_...`; 4 is prose; 5 counts
check out.

- [MAJOR] project-trajectory/scripts/adjudicate_brief.py:610 -> `first_approval_values` re-resolves the population from `trace.reattest_model`, which walks EVERY SR in the repo, so the brief's scope is the whole repo's `Drafted` backlog rather than the rows the merge handed over — the function never receives the merge delta, so it structurally cannot ask the mint's question. Driven here with a synthetic row and no merge context at all, it returned 4 SR chains / 11 `[AWAITING FIRST APPROVAL]` rows / 40,658 chars and `registries = docs/requirements/low-level-requirements.toml=… system-requirements.toml=… docs/test/test-cases.toml=…` — all three registries. This contradicts the doctrine this same diff writes: PROCESS_OPTIONS.md mechanism 2 says the merge "MINTS a first-approval adjudication over the `Drafted` rows the lane handed over", and the ruling's own concurrency reason is that "the approval snapshot must not move across a workstream". Failure scenario: merge A stages one `Drafted` LLR and mints adj-1 whose title/`## Context` name that one row; the template then tells the claiming session "You hold the approval authority for every row below marked `[AWAITING FIRST APPROVAL]`" and "`APPROVE` only when EVERY row you were shown is approved", so adj-1 flips 11 rows across 4 unrelated SRs and re-anchors all three registries under one WI. Second-order: a merge B minted adj-2 before adj-1 ran now composes to `(None, reason)` ("no spine row awaits a first approval any more"), which `compose` turns into a rule-3 HELD-for-a-human stop — the widening manufactures owner interrupts. This repo is live for it: `human_approval_through = "DevStg-Needs"` releases all three spine rungs. -> Pass the mint's row-id set into the assembler as a typed input (the intersection of that set with the live `reattest_model` re-resolution is both the mint's question and a live one), so the wider population is never constructible rather than filtered out afterwards. -> @owner
- [MAJOR] tests/test_wi_convert.py:195 -> the declared per-commit bar is RED at this tip: `pytest -q -n auto -m smoke` gives `1 failed, 1455 passed` on `test_the_live_registry_round_trips_in_whichever_home_is_authoritative`, with `ConvertError('docs/work/cancelled/README.md: does not start with a +++ frontmatter fence')`. The same test PASSES in the `contract_split` worktree — because trunk still holds `docs/work/active/wi-572-…/WI-572-….md`, so `wi_convert` stops at `drained-stop` before reaching the README. This lane's close drains `active/` (it is now the only claim on trunk), which uncovers `wi_convert.py:601`'s `work_dir.rglob("*.md")` picking up the tracked, legitimate `docs/work/cancelled/README.md`. The defect is `wi_convert`'s and pre-dates the diff, but it is reachable only after a close, so merging this branch turns trunk's smoke tier red. -> Narrow the folder-home walk to the `WI-*.md` shape the folder home actually defines (`_claimed_specs` already treats a non-`WI-<n>-<slug>.md` glob hit as residue), which deletes the bad state rather than excluding one filename; note the fix is `wi_convert`'s scope, so it may belong in a follow-up row rather than in this diff, but the red tip cannot ship as green. -> @owner
- [MINOR] project-trajectory/scripts/acceptance_record.py:540 -> `lane_approval_refusal` builds its snapshot arm from `git diff --name-only --no-renames base head -- SNAPSHOT_DIR`, which lists DELETIONS as well as writes, and then renders every name as `"  wrote {}"`. A branch that removes a stale `docs/archive/last_approved/` file is refused with a refusal record stating it wrote a file it deleted — a false sentence in the one artifact a human reads to understand why the merge stopped. -> Read the status letter (`--name-status` / `--diff-filter`) and word the line from it, so the record names the act it observed; this corrects the message rather than adding a guard, so no unrepresentable-form clause is owed. -> @owner
- [MINOR] docs/requirements/interfaces.toml:1210 -> for clarity: IF-091's `data` now reads "staged_approval_acts records and the lane_approval_refusal text (integrate)", but `integrate` consumes only the refusal text — `grep` over all of `project-trajectory/scripts` and `scripts` shows `staged_approval_acts` has no caller outside `acceptance_record` itself, so the seam declares a record that never crosses it. -> Drop `staged_approval_acts records` from the integrate clause and leave the seam naming `lane_approval_refusal` alone. -> @owner
- [MINOR] project-trajectory/scripts/acceptance_record.py:439 -> for clarity: `staged_approval_acts`' docstring says it reports "exactly the set `staged_spine_amendments` exempts" (and the spec Deliverable §1 and registry-machinery-reference repeat it), then four paragraphs later carves out the de-approval — `Approved` → `Drafted` moves Status, so the amendment reader exempts it, but this reader does not report it. Two statements in one docstring disagree about the mirror's completeness. -> State the mirror as "the exempted set MINUS the de-approvals, which bless nothing" in the docstring and the LLR-158 Detail cell that quotes it. -> @owner

VERDICT: CHANGES-REQUESTED findings=5
