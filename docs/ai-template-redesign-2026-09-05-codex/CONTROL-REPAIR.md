# Control repair and retry preparation

The owner requested Claude Fable at medium effort to review the
[incident](CONTROL-OBSERVATIONS.md), then authorized applying valid feedback
and preparing a retry. The preparation described below did not launch a retry or declare WI-605
complete. The owner has now authorized retry; the current launch and stopping
terms are in the [retry record](CONTROL-RETRY.md).

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
- Reopen the rationale-citation finding. The owner challenged the attribution
  of “Rationale names this ruling”; no direct owner message has been verified.
  That phrase comes from the agent-authored ruling record, and F6 repeated it
  as an explicit instruction without establishing its source. Withdraw that
  claimed override of the standing prose convention. Fresh review must judge
  the finding under the ordinary process and assignment scope; if correction
  is owed, use the authorized amendment or successor route, not an invented
  owner instruction. Historical verdicts remain evidence of what was said.
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

## Final preparation checkpoint

Runtime repair: `a7f57c3f`. Lane reconciliation: `b678287c`, followed by the
durable owner-instruction link at `8e6555ec`. The invalid 003 verdict file is
absent, the original commit remains in history, and the original scoped SR/TC
snapshots remain on the unmerged lane. No primary approval snapshot changed.

The first station refresh passed smoke (1687 passed, 8 skipped in 72.60s;
measured 73.0s/90s) but refused on 22 links to consumed log fragments, and
rolled back cleanly to the lane's work commit. This was a real additional
preparation blocker. Compile the 25 already-committed primary fragments through
trunk_step and retarget their incoming links to the permanent compiled headings;
that correction is now applied. It preserves the record text and every ruling,
changes no authority or cap, and avoids putting disposable fragment links back
into the lane. The branch's own new fragment is left for its station compile.

The link-correction commit bars pass: primary 1687 passed/8 skipped in 59.83s,
measured 60.1s/90s; lane 1676 passed/8 skipped in 62.80s, measured 63.0s/90s.
Documentation passes on each. On the actual committed lane, both
review_owed_by_evidence and resume_owed_round select exactly REVIEW-A before any
build/adjudication session, without creating a marker or launching a provider.
<!-- fig: derived="out/run-logs/control-repair/retry-routing-check.json, links-primary-smoke.txt, links-primary-smoke.json, links-lane-smoke.txt, links-lane-smoke.json, compiled-docs.txt, links-lane-docs.txt; out/run-logs/refresh-refused-wi-605-adjudicate-sr-161-llr-183-ow.log" rev=a7f57c3f+durable-log-links; lane=8e6555ec -->

The station refresh is rerun after this record commit. Its resulting
Bar-Green commit on the original lane is the durable verification of the
combined tree; the local command output is retained under
`out/run-logs/control-repair/station-refresh-final.txt`. A successful refresh
is preparation, not WI-605 approval, terminal handback or merge. The next
session still owes its independent REVIEW-A. Keep the global pause until the
owner authorizes the retry; no second control window has been opened.
