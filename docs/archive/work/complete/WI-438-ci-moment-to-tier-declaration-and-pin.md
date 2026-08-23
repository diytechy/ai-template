+++
id = "WI-438"
title = "OI-24 execution, the build half: declare the moment-to-tier table ONCE in a machine-readable home (push=smoke, PR=full, tag=release — the bars the docs already state in prose) and add a stdlib string-search test asserting the reference CI workflow's trigger lines match the declaration, so raising CI scope becomes a reviewed edit to the declaration rather than a quiet workflow change. Also pin that the workflow's harness invocation matches the documented local entry point. The SN-005 text narrowing (per-moment equivalence, one definition of passing per moment, no adopter-copy claim) is NOT this row — it rides the re-attest batch (WI-444)."
workstream = "lock-program"
sr_refs = ["SR-019", "SR-020"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 1
+++

## Deliverable

Completed 2026-08-13. The moment→tier table has one declared home — `[ci-tiers]`
in the stack profile (shipped in `stack.ini.template` with push=smoke,
pull_request=full, tag=release; instanced in `docs/stack.ini` with this repo's
deliberate un-tiered `all`/`all` values and the reason recorded beside them) —
and `tests/test_ci_tier_declaration.py` (19 tests) pins both workflows to their
own tables: entry point at command position, guard→trigger translation, tier
comparison both directions, step labels, the tag trigger's reachability, no
job-level veto above the step guards, and the one-home comment rule on the
workflow file itself. check.yml's comment now points at the declaration instead
of carrying it.

The adversarial round (codex gpt-5.6-sol, medium, hostile brief) found four
real pin defeats, all fixed and each now carried as a bite test: an `echo`-
prefixed mention counted as an invocation (fixed: command-position matching),
`--tier smoke --tier all` read first-match while argparse runs last (fixed:
last wins), a bare `- run:` step gluing onto a guarded neighbour's block
(fixed: step splitting on any step-start key, plus a bite proving the glued
step surfaces unguarded), and nothing refusing a job-level `if:` veto (fixed:
reference workflow refuses one; this repo's known fork-PR dedup guard is the
only recognized job guard, translation-table style). Two doctrine findings
were rejected with reasons: the test's shipped-values assertion and the
step-label rule are deliberate CHECKED pins, not second homes. One wording
over-claim fixed: `push` mirrors the per-commit bar on the pushed tip, not
literally every commit.

Verification: module 19 passed; smoke 1004 passed / 2 skipped; check_docs OK.
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_ci_tier_declaration.py" rev=this-branch -->
Scope note: SN-005's text narrowing stays WI-444's; the pre-existing E741 lint
red at tests/test_id_watermark.py:82 predates this work (confirmed on stashed
HEAD by the builder) and is disposed separately.
