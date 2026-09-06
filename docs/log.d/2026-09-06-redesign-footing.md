## 2026-09-06 — Begin the redesign with current-runner repairs

Owner-authorized supervised implementation on `contract_split`, based on
`5645798c`. The [execution record](../ai-template-redesign-2026-09-05-codex/EXECUTION-RECORD.md)
defines the slice and links the refreshed census, adversarial reviews and
dispositions. Sol and Terra implemented the coordinator repairs; Luna refreshed
the baseline and tested the accounting boundary.

The worker now reconstructs its evidence base from the existing verified Git
claim. Loaded Python changes stop the coordinator with exit 11 at a safe
boundary; the dispatcher drains running children and preserves their branches
for an operator restart. Invocation accounting extends the existing log carrier
with identities, route attribution, timing and raw usage without treating
missing counters as zero. The local smoke harness step enforces the existing
budget. OI-83/OI-84 record the accepted implementation choices; no requirement
approval, snapshot, queue assignment or pause changed.

The broad repair passed the unfiltered suite: `3556 passed, 20 skipped in
713.82s`. An earlier run exposed an integer-header compatibility failure and
an unlinked inventory; both were corrected before this passing run. A run
overlapping source edits was invalidated by the new drift detector and is not
stable-tree evidence. <!-- fig: cmd=".venv/bin/python -m pytest -q -n auto" rev=5645798c+P0b-before-final-accounting-sweep; out/run-logs/redesign-full-final.txt -->

The subsequent launch-path completion passed routing/stdin/accounting/dual-plan
and ratchet checks: `93 passed in 9.72s`; selected worker checks passed
`4 passed, 67 deselected in 4.16s`. Final review fixes passed
`29 passed in 1.80s`. The shared writer now keeps provider metadata on one
physical header line, and standalone calls cannot increment worker draw
ordinals even with an identical role name. <!-- fig: derived="pytest outputs in out/run-logs/redesign-accounting-final.txt, redesign-accounting-worker.txt and redesign-accounting-review-fixes.txt; base 5645798c plus final accounting completion" -->

The final enforced smoke run passed tests (`1654 passed, 4 skipped in 60.81s`)
but failed timing: `61.0s vs 60s budget -> OVER`, exit 1. Commit proceeds under
the owner's explicit standing authorization for this machine's smoke timing;
the budget and tier membership are unchanged. Documentation has no broken
links; strict trajectory and trace integrity pass with existing advisories.
Ruff and the module/function ratchets pass. <!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=5645798c+P0b-final; out/run-logs/redesign-smoke-commit.txt -->

The commit hook caught the generated approval brief's stale interface-change
count. Regenerated `docs/ratify/CURRENT.md`; no approval was granted and no
approved snapshot changed. Hooks remain enabled.

Deviation: this is the plan's repaired-baseline slice, not replacement-runner
enablement or completed P0a/P0c. The control workload, paid-run budget and
observation window remain unestablished. Full obligation/scenario mapping,
populated adopter evidence and H1's explicit need-context bridge remain next
work. No live pilot was started. Capped/watched document byte delta: zero.
The intentional module-size changes are explained in the execution record;
no function-complexity ceiling was raised.

Deferred open items: none created by this slice. Existing OI-82 remains pending;
the control prerequisites and remaining implementation scope are retained in
the execution record rather than represented as completed work.

### Commit and adopter instructions

Implementation landed as `22b21b06` with hooks enabled. A follow-on
[resync entry](../../project-trajectory/RESYNC_PACK.md) names that exact source
commit, the coherent script update, manual restart behavior, preserved claim
history and metadata compatibility. Corrected the three final review-log
headers to put the requested `high` in `effort`, leaving their undeclared
routing tier blank; provider transcripts and usage values are unchanged.

Documentation-only follow-on validation: smoke `1654 passed, 4 skipped in
60.08s`, enforced wall `60.3s vs 60s budget -> OVER`, exit 1; the same owner
timing authorization applies. Documentation check: no broken links, with the
existing report orphan warning. No source or test membership changed after
the implementation commit. <!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=22b21b06+resync-docs; out/run-logs/redesign-resync-smoke.txt -->
