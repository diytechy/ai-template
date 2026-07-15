# 066-REVIEW-A — WI-149 (lowest-gate-first queue advisory)

Independent review of commit `896f9ed` (WI-149: warn on lower-gate queue order),
built session 065. Reviewed the diff against the spec-of-record
(`docs/specs/owner-intake-2026-07-14.md#gate-first`), AGENTS/PROCESS discipline,
and the registries.

## Harness run (observed, not reported)

- `python project-trajectory/scripts/check_trajectory.py --root .` → `clean (158
  work item(s), 136 done (86%), graph acyclic).` exit 0. `--strict` also clean.
- `python project-trajectory/scripts/trace.py --root .` → `SN=24 SR=56 LLR=57
  TC=57 orphans=0 integrity=0 ... interface-findings=0.` exit 0.
- `python project-trajectory/scripts/check_docs.py --root . --stale` → exit 0
  (only pre-existing staleness hints on historical review docs).
- `python -m pytest tests/test_trajectory.py -q` → 66 passed.
- `python -m pytest -q -n auto -m smoke` → 612 passed, 2 skipped (51 s).

## Assessment

The feature matches its done-when: `gate_first_findings` reads `docs/next-wi`,
is vacuous for a non-anchor/no-SR/no-phase selection, warns naming the open
`[phase]-[g1|g2]` anchor and any Draft SRs in the phase, and is printed as WARN
only — never added to `errors`, even under `--strict` (line 1338), so it can
never fail a gate. Identity skip of anchor WIs, `min`-by-gate anchor selection,
and deterministic `sorted()` iteration are all correct. Both `agent-resume`
prompts carry the lowest-gate-first line. status.md prose (`Next action WI-150`,
run-state RUNNING) matches `docs/next-wi` (WI-150), `docs/run-state` (RUNNING),
and `docs/gate` (G2). No SN/SR/TC rows were added, so no registry sweep applies.

## Findings

- [MINOR] tests/test_trajectory.py:1106 -> the three fixtures cover open-anchor, Draft-SR, and non-phase-WI vacuity, but none asserts the advisory stays SILENT when a phase-development WI is selected and its phase's anchors are all `done` with no Draft SR — the primary "lower gates already cleared, do not nag" path is untested, so a future regression that over-warns on a cleared phase would pass -> add a fixture with a selected WI whose SR names a phase whose `[phase]-[g*]` anchors are all done and no Draft SRs, asserting `gate_first_findings(...) == []` -> @owner

VERDICT: APPROVE findings=1
