+++
id = "WI-510"
title = "Decompose the two stray orphan SRs no queued row owns: SR-160 (front-door launchers) and SR-164 (declared SN scope)"
specref = ""
workstream = "requirements"
sr_refs = ["SR-160", "SR-164"]
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 2
+++

## Deliverable

Both strays decomposed, both mints `Drafted` per this row's own Context.

**SR-160** (front-door launchers). Investigation found the obligation
SPLIT: the loop-resume half — `agent-resume.{sh,cmd,command}` at the
repository root — is built and driven by real, already-passing tests
(WI-475's interpreter-selection module); the environment-preparation half
has no root launcher at all (`onboard.sh`/`dev-setup.sh` materialize under
`scripts/`, not the root SR-160's acceptance names — the gap README.md's
own "Still owed" ledger already states). Decomposed rather than
reclassified: the behaviour that exists IS testable, so `Verification`
stays `Test`. Minted `LLR-193` (module `agent-resume.sh`, symbol
`pick_py`, mirrored by `agent-resume.cmd`'s `:pickpy` and inherited by
`agent-resume.command`'s delegation) and `TC-188`, evidence 11 real
`tests/test_launcher_interpreter.py::*[live]` node ids. The
environment-preparation residual is stated on the row as NOT DISCHARGED
(the debt-stating pattern) rather than covered by a citation to a module
that does not exist.

**SR-164** (declared SN scope). Investigation found the obligation
entirely unbuilt: no field, checker branch, or test anywhere in the
shipped scripts reads or validates a stakeholder-need `scope` value — the
`**Scope: ...**` prefix in each need's prose is pure convention, and `SN`
carries no entry in `trace.py`'s `REQUIRED_FIELDS`/`ENUM_FIELDS` schema
tables at all. Minted `LLR-194`, citing the real, already-delivered
generic seam this obligation is scheduled to extend — `trace.py`'s
`schema_findings`/`REQUIRED_FIELDS`/`ENUM_FIELDS`, which already reports
a missing required field or an out-of-vocabulary closed value by name for
six other tables — with the row stating plainly that SN's own entry does
not exist yet. `TC-189` cites two real existing tests
(`tests/test_trace.py::test_missing_required_if_field_is_a_warn`,
`::test_out_of_vocabulary_aspect_is_a_schema_finding`) exercising that
same generic mechanism's two behaviours over the one table that has them
today (`IF`), honestly framed as verifying the seam rather than a
scope-specific checker that has no code to cite.

**Orphan count:** 11 -> 7 (SR-160 and SR-164 each cleared 2 findings — no
LLR, no test).
<!-- fig: cmd="python project-trajectory/scripts/trace.py" rev=25428fee -->

**Stage:** unmoved at `DevStg-LLReqs` — both mints land `Drafted`, and
drafts are excluded from the effective stage, exactly as the Context
predicted.

`docs/status.md`'s hand-authored orphan-debt sentence corrected: "five
undecomposed SRs" -> "three", and the "the two strays have their own
decomposition row" clause replaced with "the two strays are decomposed"
(forward-only; no closed WI id named per the R-D guard).

Surfaces regenerated: `trace.py --bump-ids` (LLR 192->194, TC 187->189),
`gen_open_items.py`, `derive_stage.py`, `gen_trajectory.py`
(`PROJECT_STATE.html` + `docs/status.md`'s generated block).

## Context

Owner-directed 2026-08-22: the orphan-debt mapping placed five of the
seven undecomposed SRs (plus LLR-164's missing TC) with queued rows that
already own their subjects (SR-151/152 → the test-evidence carrier row,
SR-162 → the wi455 lane, SR-163 → the remap program, SR-177 + LLR-164 →
the session-continuity row — each carries a fold-in note and the sr_ref).
This row takes the two strays:

- **SR-160** — front-door launchers for the two universal contributor
  actions (`run_menu` / the `agent-resume.*` surface). Read the row and
  the live launchers; decompose into LLR/TC, or — if the obligation is
  genuinely a launch-surface inspection rather than a testable behavior —
  re-class its Verification to Analysis/Inspection with the reasoning on
  the row (the orphan rule accepts that honestly; do not re-class just to
  clear the finding — the WI-475 launcher tests suggest the behavior IS
  testable, which is the default expectation here).
- **SR-164** — stakeholder-need scope is a declared, checked value. The
  declared-surface + checker pattern is well-worn (the SN scope
  declaration and whatever validates it); decompose to the LLR naming the
  checker seam and the TC driving it.

Both mints land Drafted (no selection movement — the effective stage
excludes drafts) and ride the ordinary approval machinery under the
DevStg-Needs dial. Closing this row plus the four fold-ins zeroes the
orphan debt, which is what currently holds the ladder at DevStg-LLReqs.
