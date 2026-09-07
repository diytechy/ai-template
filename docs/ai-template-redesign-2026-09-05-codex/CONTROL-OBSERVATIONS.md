# Short control observations

Operating envelope: [owner ruling](CONTROL-DECISION.md#owner-ruling-2026-09-06).
Preparation and live route probes: [preflight](CONTROL-PREFLIGHT.md).

## Launch

The hooks-enabled pause-deletion baseline is
`de9a2bfa7febe32ae16099cc09008f43a2240165` on `contract_split`. The queue and
route registry were revalidated at that commit. The following record-only
commit names this baseline; no runtime bytes differ. Coordinator UTC start,
process id and output are captured locally under `out/run-logs/control-window/`
at invocation, then folded into this record at a safe stopped boundary.
WI-551 remained deferred through the window. No coordinator observation had
occurred at the initial identity-record commit.

## Recording and stopping

The supervisor follows the launcher output and existing invocation, review,
integration and Git records. For each completed WI record its accepted
obligations, attempts, review rounds, interventions by reason, reported cost
or unavailable coverage, integration time and queue wait. Preserve incomplete,
partial and abandoned attempts as well. Required approvals and sampled reviews
are separate from defect-repair interventions. Do not sum ambiguous counters.

Count across launcher restarts, never reset the window at exit 11. Stop new
admission at the first ruled WI/day/coordinator-hour bound, recreate the
tracked pause and drain under current policy. The reported spend watch is not
an admission gate. A required runtime repair closes its measured segment;
record the old and new revisions before any later observation. A correctness
failure stops the affected path. Do not widen the window or silently substitute
another one if the sample is insufficient.

## Events

- Started `2026-09-07T01:11:34.757486+00:00` from record-only boot commit
  `dc848687858fc871b8d38dd0748d88672716b475`, launcher PID 73853. The frozen
  runtime baseline remains the pause-deletion commit above. The launcher
  claimed WI-605 exclusively at `46d010f4da82149e1929073f0d8f258cdf8c8529`.
- Session 001, Fable 5.1 / medium effort / strong route: ADJUDICATE committed
  its verdict, scoped SR/TC snapshots, and an LLR successor disposition.
  The LLR snapshot was withheld. Invocation
  `52a22b1d6ba64e2ea5989d8ff22fbaab`, reported wall 377s, raw reported
  cost USD 3.9353014999999996, usage scope `unknown`; not an aggregate cost.
- Session 002, Sol / medium: independent REVIEW-A returned
  CHANGES-REQUESTED with one major close-order finding and one minor rationale
  citation finding, reported wall 324s. Its record explicitly discloses that
  the smoke step printed PASS despite `/usr/local/bin/python3: No module named
  pytest`; it claims no pytest green. The coordinator started session 003,
  Astra / medium effort / strong route, for ordinary adjudication rework.
<!-- fig: derived="WI-605 session 001/002 metadata and review verdicts in its claimed branch; out/run-logs/control-window/launcher.log and launch.json; exact source paths below" rev=8956f053 -->

## Stop-admission finding

The supervisor re-created the tracked pause at
`2026-09-07T01:27:17.711514+00:00` after confirming the reviewer's false-green
report, initially allowing the existing lane to drain. A second correctness
finding below required interrupting that drain. No runtime code changed
within the segment.

Root cause: `scripts/check_smoke_budget.py:main` prints a note for a nonzero
test child but returns only `evaluate(elapsed, budget, mode)`. The registered
`[step:smoke]` runs that wrapper alone, so an under-budget failure reports PASS
to `check.py`. This covers assertion failures as well as missing pytest.
The linked-worktree review’s ambient Python selection exposed it; installing
pytest there alone would leave the false-green mechanism intact.

An isolated reproduction loaded the actual script with `runpy.run_path`,
stubbed `subprocess.run` to `CompletedProcess(['pytest'], 1)` and the two
monotonic readings to 0.0/1.0, then called `main(['--mode', 'enforce'])`:

```text
note: smoke tier exited 1 (test failures are not a budget breach; fix them separately)
smoke wall-clock budget: 1.0s vs 90s budget -> within
REPRODUCTION: child exit=1; enforcing wrapper exit=0
```

This is a control finding, not a passing control or justification for a
replacement runner. The targeted repair is to propagate test failure and
cover the failing-child/under-budget case, then verify the real interpreter
path for linked-worktree reviews. No second observation window is implied.

Evidence remains on the claimed lane until integration:
`docs/iteration/wi-605-adjudicate-sr-161-llr-183-ow-001-20260906-201146.log`,
`docs/reviews/wi-605-adjudicate-sr-161-llr-183-ow/002-REVIEW-A-efb0fcd.md`,
and the local launcher log.

## Interrupted rework: scope lost before a snapshot act

Session 003 committed `ceab73e1107b64e9f238df30b4edeffb982d5c1d`, a new
meaning verdict on LLR-061/167/183. It then staged a whole LLR snapshot and its
approval stamp, explicitly claiming authority over LLR-061 and LLR-167 while
WI-601 and WI-603 remained queued. This contradicts the WI-605 spec's reserved
scopes and required prior judgments; the first session had correctly withheld
that copy. The attempt had not been committed or promoted when interrupted.

The supervisor suspended coordinator polling, sent SIGINT to the worker and
coordinator, and verified that both and the provider/test children exited.
The launcher exited 130 at `2026-09-07T01:31:13.103265+00:00`; its measured
elapsed time was 1178.3461733749718s (about 19m38s). No WI completed, no branch
merged, and the primary checkout's approval snapshots did not change.
There were three started provider sessions and one recorded independent review;
the third session was interrupted, so its final usage/cost is unavailable.
The two supervisor interventions were the admission pause and the interruption
of the unsafe snapshot path. No relaunch or second window occurred.
<!-- fig: derived="out/run-logs/control-window/launch.json, launcher.log and interruption.json; primary git range de9a2bfa..46d010f4; lane HEAD ceab73e1" rev=46d010f4 -->

Preservation: the lane remains on its original claimed branch at `ceab73e1`,
with all committed work intact. The attempted uncommitted snapshot is retained
as [a forensic patch](../work/handback/wi-605-control-interruption-llr-snapshot.patch),
SHA-256 `d1db313c6db674f3204693e881492e930c138a99cff463d88a3c1e263c1f9646`.
Only its two uncommitted paths (`docs/archive/last_approved/README.md` and the
LLR snapshot) were restored to the lane's committed HEAD; the lane is clean.
This is an interrupted assignment, not a complete/partial acceptance or a
renamed parked ref. Do not run the existing as-is partial-close helper on the
unsafe staged state: it would commit that state. Reconcile the lane under the
corrected scope before deciding its terminal outcome. The tracked pause stops
new claims but the dispatcher can resume a parked claim before testing pause,
so do not relaunch merely because the pause exists.

The code explains the lost context: `agent_loop.session_body` returns the
specialized `adjudicate_brief.compose` result without including
`worker['rework']`; only the generic worker path includes review feedback.
`adjudicate_brief.amendment_values` enumerates the whole current drift model
without using the WI's scope, and the amendment template says to judge the
shown cells only. After the SR/TC copy, the regenerated brief therefore showed
the remaining LLR drift and authorized its snapshot without conveying the
WI-605 exclusions or Sol's requested rework. The repair must carry governing
assignment constraints and review findings into the specialized judge path,
while preserving independent judgment of the evidence.

The close-order finding also needs reconciliation: Sol asked the agent to
close the active row before review, while `dispatch._close_done_adjudication`
and `handback.close_adjudication` own a mechanical adjudication close after
worker completion. Do not patch around that disagreement by deleting a
legitimate close or weakening review.

## Result and verification

Outcome: correctness failures found; insufficient completed-work evidence for
a throughput comparison or replacement decision. Targeted repair is the next
step. PC remains unconditional after the window under its own contract-change
sequence; these findings do not authorize a replacement or a second window.
WI-551 was re-queued at close as the handoff instructed, after remaining
excluded throughout the window; the global pause remains in effect.

Stop-record verification initially overlapped the worker's tests: 1676 passed,
8 skipped in 96.72s, measured 97.2s, exceeding the 90s ceiling. The worker's
concurrent timed run also exceeded it (92.9s); this contention includes
supervisor-induced load and is not clean comparative timing. After the
processes stopped, the isolated supervisor run passed 1676 tests, skipped 8
in 58.63s; measured wall 58.846227500005625s, enforced within the unchanged
90s budget. The supervisor checked pytest's exit separately before evaluating
the timing, so this evidence does not rely on the defective failure propagation.
<!-- fig: cmd=".venv/bin/python -m pytest -q -n auto -m smoke; .venv/bin/python scripts/check_smoke_budget.py --elapsed 58.846227500005625 --mode enforce" rev=46d010f4+control-stop; out/run-logs/control-stop-smoke.txt; control-stop-smoke.json; control-stop-smoke-isolated.txt; control-stop-smoke-isolated.json -->
