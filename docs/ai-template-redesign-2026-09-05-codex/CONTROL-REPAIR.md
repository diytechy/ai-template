# Control repair and retry preparation

The owner requested Claude Fable at medium effort to review the
[incident](CONTROL-OBSERVATIONS.md), then authorized applying valid feedback
and preparing a retry. The tracked pause remains. This repair does not start
another control window or declare WI-605 complete.

## Independent feedback and disposition

The [unaltered Fable review](CONTROL-REPAIR-FABLE-REVIEW.md) records the CLI
session and recommendations. The call completed without a provider error on
Claude Fable 5.1 with `CLAUDE_CODE_EFFORT_LEVEL=medium`; raw reported cost USD
5.5218265 is preparation cost, not control-window spend.

- Accept the smoke failure and lost scope/rework findings. Tests reproduced
  both against the original code before implementation.
- Accept the mechanical-close diagnosis. The close-order MAJOR was false:
  adjudication review precedes worker DONE and the coordinator's close. The
  reviewer now sees that role on the adjudication row it is reviewing. The
  lifecycle and its strict review identity checks remain intact.
- Reject the proposed rationale-removal successor. The explicit
  [owner instruction](../log.d/2026-09-06-sn036-owner-ruling.md) says “Rationale
  names this ruling.” [F6 was already dispositioned](../reviews/2026-09-06-sn036-review-dispositions.md)
  on that basis. A general process convention does not override it; retain
  the citation and the visible advisory, with no suppression.
- Resolve the duplicate-title warning as a false positive. WI-601 judges
  LLR-061; WI-603 judges LLR-167. Both distinct dependencies remain.
- Accept the approved/traced distinction. Only LLR-061/167/183's approved
  Detail cells carry the LLR snapshot's amendment authority. Traced
  Module/CodeSymbol changes are non-attesting under §A5.1 and remain part of
  the whole-copy inventory. The snapshot tool's reference is a naming gate,
  not a machine verification of the named judgment's semantic authority.
- Correct the partial-close explanation further than Fable did: the helper
  refuses an adjudication lane in `_no_recursion_refusal` before committing
  residue. This lane owes a reconciled judgment and normal mechanical close,
  not a recursive partial-close adjudication.
- Accept voiding `ceab73e1`. Its provider was Astra despite its copied Fable
  co-author trailer. Reverting the verdict file preserves that commit in
  history while removing the invalid verdict from the current record set.

## Implemented repair

The smoke wrapper reports both outcomes and propagates a failing child in
warn and enforce modes. The elapsed-only timing interface is unchanged.
`harness_python` resolves a local virtual environment first, then the primary
worktree's environment, then the existing ambient fallback. The review prompt
uses that resolved interpreter in its actual commands.

Specialized adjudication composition reads the authoritative assignment spec's
Context verbatim and without truncation, separately labelled as governing
constraints. Deliverable and Dispositions self-assessment are not injected as
cell evidence. A missing governing spec holds the session. Independent rework
findings carry the prior verdict path and explicitly address the existing
judgment rather than authorizing a new delegation. Every specialized brief
receives these inputs; templates may place the slots, but overrides cannot
omit the inputs. The amendment template distinguishes governing scope from
the registry-derived evidence and tier authority from row reservations.

The module-size baseline grows by 19 SLOC in agent_loop for the existing
composition boundary's forwarding, interpreter rendering and reviewer role
label. This implements the independently reviewed repair at the owning
boundary; it does not add another router. New context assembly stays in
adjudicate_brief. No dependency, policy dial, requirement cell or approval
snapshot is changed by these repairs.

## Interrupted lane and retry sequence

The original claimed branch remains
`wi-605-adjudicate-sr-161-llr-183-ow`. Reconciliation reverts only the invalid
003 verdict, records the two declined review findings and preserves the
legitimate SR/TC copies and withheld LLR result. Its successor disposition is
corrected to require judgments accepting the exact live approved cells:
merely recording a verdict or drafting corrective work is insufficient to
permit copying. Returned cells must finish their correction and judgment
first. This is a substantive successor correction for fresh review, not a
record-only reroll of the same disputed tree.

Preparation sequence: commit and verify the repair on primary; commit the
lane reconciliation; use the station's `refresh` to bring the repaired primary
into the lane and run its bar. Do not hand-merge trunk, fabricate a review
marker, write a legacy rollup or treat the Fable plan review as WI-605 approval.
Probe the real `review_owed_by_evidence` and `resume_owed_round` against the
prepared lane. A later authorized retry should begin with its missing
REVIEW-A, then reach DONE, mechanical close and integration only after a valid
round. The merge then mints the existing LLR successor. No terminal close or
merge is claimed before those conditions hold.

## Verification

Before repair: the existing focused smoke/interpreter tests passed 24 tests;
the lifecycle baseline passed 197. New regressions failed in five smoke cases,
one linked-interpreter case, both initial/rework scope cases, and the rendered
review-command case. After the first implementation, 164 focused tests passed.
Additional override, untruncated-feedback and missing-spec tests cover the
composition boundary. Final full-suite, smoke timing, documentation and
prepared-lane results are recorded below when completed.
<!-- fig: derived="out/run-logs/control-repair/{baseline-tests,lifecycle-baseline,smoke-regression-before,interpreter-regression-before,scope-regression-before,review-regression-before,focused-after}.txt" rev=2137230e+control-repair -->

The unfiltered run finished with 3671 passed, 26 skipped and two failures in
726.11s. One read the review record before its linked repair record had been
written; the completed documentation graph fixes it. The other found the
pre-existing CLAUDE.md baseline stamp left at 7975 bytes by the owner-ruled
90-second budget update (`c559a403`), while the actual file is 8009 bytes.
The file and its 8500-byte cap are unchanged; the skill's baseline is corrected
in its source and both tracked copies. That skill shrinks from 4613 to 4594
bytes (406 bytes under its 5000-byte cap). The three cap checks and the one
orphan/link check pass on targeted rerun. No cap or test threshold was raised.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto; .venv/bin/python -m pytest -q tests/test_bootstrap.py -k 'byte_caps or size_budget or capped_doc_baselines'; .venv/bin/python -m pytest -q tests/test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans" rev=2137230e+control-repair; out/run-logs/control-repair/full-suite.txt; full-suite-failures-rerun.txt; docs-failure-rerun.txt; byte-stamp.json -->

The actual check.py smoke step, driven in an isolated fixture with a child
exiting 7, now reports FAIL and returns harness exit 1 even at 0.0 seconds
within budget. Actual WI-605 prompt composition carries its full reserved
scope, Sol's complete findings, the prior 001 verdict path, the primary .venv
command and the mechanical-close reviewer role. These are executed local
checks; no provider or coordinator retry was launched.
<!-- fig: derived="out/run-logs/control-repair/smoke-end-to-end.txt and prepared-prompt-check.json" rev=2137230e+control-repair -->

An extra complexity-baseline audit remains red on inherited drift, including
moved rendering modules and earlier agent_session/intake/plan_briefs changes.
For the two flagged agent_loop functions, route_session and run_iteration,
AST comparison against 2137230e is identical (cognitive 38 and 16 respectively).
No new over-threshold function remains from this repair. This is not a claim
of a clean DevStg-Impl complexity gate; the current declared stage is
DevStg-Tests. The baseline was not broadly restamped to hide those findings.

Primary commit bar: 1687 passed, 8 skipped in 78.12s; the repaired wrapper
measured 78.3s against the unchanged 90s ceiling and returned success.
Documentation passes with zero broken links and the existing generated-report
orphan warning; strict trajectory passes with warnings. Ruff passes.
<!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce; .venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale; .venv/bin/python project-trajectory/scripts/check_trajectory.py --root . --strict" rev=2137230e+control-repair; out/run-logs/control-repair/commit-smoke.txt; docs-final.txt; trajectory.txt -->
