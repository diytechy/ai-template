## 2026-09-07 — Repaired control stopped, pause restored

The root launcher ran the repaired configuration from `b830f202` and stopped
at `79115aab` after its own abbreviated candidate metadata caused the primary
verifier to reject the completed judgment. The independent read-only follow-up
also confirmed that `when-minting` review routing misses a draft's later
high-risk classification. The
[observation record](../ai-template-redesign-2026-09-05-codex/CONTROL-APPROVAL-OBSERVATIONS.md)
retains exact evidence, independent audits and the pending writer boundary.

The segment lasted 616.129 seconds and completed zero WIs. Cumulative active
control time is 3666.384 seconds; reported cost for the first invocation is
USD5.948853000000001 with unknown usage scope. The second invocation was
interrupted, with no final coordinator usage record. No usage gap is treated
as zero. No code changed inside the measured segment, no independent review
round ran, and no approval/snapshot/terminal/mint effect was published.
<!-- fig: derived="out/run-logs/control-retry-approval/launch.json, stop-state-proof.json and committed docs/iteration/contract_split-001-20260907-040924.log" rev=79115aab -->

Owned coordinator/provider process groups were verified absent before pause
recreation. The same retention WI is re-queued as the handoff requires, with
its separate authoring and ownership prerequisites; the patch was not applied.
The original legacy worktree/branch and forensic patch remain unchanged.
The new primary turn, verdict, carrier and abbreviated invocation metadata
remain intact as incident evidence. No further window, source fix, artifact
approval or PC completion is claimed. PC remains the next authorized package,
with its authoring/judgment prerequisite and the preserved writer state to
reconcile before new claims.

Stop-commit verification: smoke 1694 passed, 4 skipped in 49.42 seconds;
enforcing smoke 1694 passed, 4 skipped in 49.19 seconds, 49.5-second wall
against the unchanged 90-second budget. Docs: 1501 documents, 2401 links,
zero broken and one pre-existing orphan warning. Strict trajectory is clean;
it correctly warns that the queued adjudication has a reachable WI trailer,
which is a reconciliation prompt and not completion evidence. This is a
post-segment documentation/pause/requeue check, not a retest or repair of the
two runtime defects.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke" rev=79115aab+control-stop; out/run-logs/approval-control-stop-smoke.txt -->
<!-- fig: cmd=".venv/bin/python scripts/check_smoke_budget.py --mode enforce" rev=79115aab+control-stop; out/run-logs/approval-control-stop-smoke-budget.txt -->
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale" rev=79115aab+control-stop; out/run-logs/approval-control-stop-docs-final.txt -->
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/check_trajectory.py --root . --strict" rev=79115aab+control-stop; out/run-logs/approval-control-stop-trajectory.txt -->

Deferred open items: none — the two findings are recorded technical defects;
no new owner ruling is requested in this stop record.
