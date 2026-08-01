+++
id = "WI-197"
title = "Coverage step adapter - headless plan_coverage.py invocation after generation and revision; report injection; exit-1 bounce-once-then-page dispositions (DP-001 selected plan P4)"
workstream = "unattended"
needs = ["WI-194"]
buildtier = "medium"
order = 193
+++

## Deliverable

WI-197 (2026-07-16, opus build / fable integrate): scripts/plan_coverage_step.py - the thin seam between plan_coverage (IF-057) and plan_round (IF-058): run_coverage() invokes the checker as a subprocess (sibling script, sys.executable, --out), returns the typed {exit, findings, malformed, implicated, report}; FAIL-line prefixes parse to implicated TRUE plan keys via caller-supplied plan_key_of (unmapped basenames dropped); exit 2 preserved as malformed=True (fail-closed: bounces BOTH plans via empty implicated); to_record_kwargs() projects onto record(STEP_COVERAGE,...); side-effect-free - the coordinator records. Report returned never printed (the critic/arbiter brief payload). 6 tests driving the REAL plan_round + REAL plan_coverage subprocess through clean / bounce-then-clean / bounce-then-page. Spine LLR-073/TC-073 under SR-061 (provisional); Proposed IF-060 (source), CMP-004; scaffolded.
