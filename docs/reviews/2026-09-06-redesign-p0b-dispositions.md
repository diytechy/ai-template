# P0b review dispositions

Disposition of the [first Opus review](2026-09-05-redesign-p0b-opus.md),
checked against the repository rather than accepted by severity label alone.
The raw review is retained unchanged. This is an intermediate implementation
review, not a replacement decision or an approval of the requirement spine.

| Finding | Disposition and evidence |
|---|---|
| B1, planner-log durability | Accept the missing telemetry commit. Use the existing scoped `commit_telemetry` helper. The claimed missing `mkdir` is incorrect: `write_session_log` already creates the directory. Dual-plan artifacts already require a subsequent handoff/commit; this correction specifically makes the new invocation evidence durable, not the entire round atomic. |
| B2, explicit null tokens | Accept. The legacy display and raw counters must both distinguish unknown from zero. |
| B3, lost cost/cache fields | Reject: `write_session_log` already lists `cost-usd`, `cache-read` and `cache-create` before the added keys. Add a cost-only round-trip regression to demonstrate the existing behavior. |
| B4, unreadable base at another caller | Reject: `stale_terminal_assignment` already has `if not base: return True`, before `train_evidence`. Worker creation also refuses an unreadable base. Falling back to HEAD on an unreadable claim would recreate the defect. |
| B5, wall duration representation | Accept compatibility correction: keep the monotonic measurement and preserve the existing rounded-integer carrier. The unfiltered suite confirmed the integer-header compatibility requirement in `test_done_exit_writes_logs_and_index`. |
| B6, duplicate Git-status parser | Accept. Move the existing parser down beside the shared claim grammar and delegate the integrator's historical name to it. |
| B7, smoke path in adopters | Reject: this is the meta-repo's own `docs/stack.ini`; `scripts/check_smoke_budget.py` exists here. It is not a shipped template step and is not copied to adopters. The current-stage harness selects it correctly. |

The useful nonblocking corrections are removal of the redundant worker-loop
fingerprint check (the session entry checks after blackout), documentation of
the extended provider-session identity field, and handling restart before
work-outcome decisions. Use Git's root-aware diff when reading claim deltas;
a parentless prose commit cannot have moved queued work into an active claim.

Other suggestions do not justify more mechanisms. Lazy fingerprint capture
would miss edits between import and first use. Route selection has already
looked up the same roster row, so another optional lookup would hide an invalid
selection. The restart is deliberately manual: no launcher retry policy was
requested. The smoke step starts at `DevStg-Tests`; full product tests start
at `DevStg-Impl`. It is an additive baseline, not a substitute for full tests.

The review agrees that SR-028/LLR-028's existing session mechanisms remain
intact. Exit 11 is a resumable process outcome; the Drafted IF-015 carrier
amendment suffices. No SN/SR/LLR/TC approval or snapshot is changed.

Verification and the follow-up review are recorded in the
[execution record](../ai-template-redesign-2026-09-05-codex/EXECUTION-RECORD.md).

## Follow-up conditions

The [follow-up review](2026-09-06-redesign-p0b-opus-followup.md) retracted the
unsupported blockers and approved subject to compatibility checks. Those
conditions are discharged as follows:

- **R1:** `test_planner_logs_coexist_with_worker_numbering_and_index` drives
  legacy, worker and planner records through `next_session_number`,
  `phase_draw_ordinal` and `regenerate_index`. Planner filenames use a
  `call_` prefix so even an all-numeric UUID cannot become a legacy ordinal.
  The existing human-readable date format is retained; UTC start/end fields
  carry the more precise attribution. Planning phases remain distinct from
  worker review phases. The date consumer is the index's string rendering.
- **R2:** the shared writer and generated index identify `agent_common.py`;
  the contract/comment now names both worker and planner producers.
- **C2:** both integrator readers pass `--no-renames`. The moved parser used
  `parts[-1]` before and after the move; the review's assertion that its old
  implementation used the first-tab remainder was incorrect. No additional
  parser change is needed.

The existing best-effort telemetry-commit behavior is retained: a hook veto
leaves visible residue for reconciliation. Abrupt coordinator death can leave
usage unavailable. This slice does not add a recovery spool or claim complete
historical provider accounting.

## Final launch-path sweep

The [accounting review](2026-09-06-redesign-p0b-accounting-opus.md) covers the
subsequent probe/interactive completion. These paths and planner calls now use
one `invoke_and_persist` boundary; the worker retains its existing domain-outcome
writer. Its two findings were addressed before the
[bounded closure review](2026-09-06-redesign-p0b-accounting-opus-closure-retry.md):

- **Draw ordinals:** exclude standalone `call_` records in the shared draw
  reader, consistently with worker session numbering. The regression now uses
  exactly `CRITIQUE` for both worker and planner; correctness no longer depends
  on their role spelling being different.
- **Header injection:** encode CR/LF as visible escapes at the shared writer,
  so provider strings occupy one physical metadata line. A regression sends
  forged outcome headers through the actual result parser and writer using LF,
  CR and CRLF; the recorded outcome remains ERROR.

The planner helper also supplies its known `dual-plan` source event when no
more specific attribution was passed. Do not add the suggested broad exception
catch around persistence: a write failure must remain visible, and Python's
exception chaining preserves an underlying launch error. There is no recovery
spool, silent fallback or separate transcript store.

The [first closure attempt](2026-09-06-redesign-p0b-accounting-opus-closure.md)
returned simulated tool markup despite tools being disabled, and no verdict.
It is retained as an unusable provider response, not review evidence. The
retry supplies the complete metadata reader and requires a structured verdict;
neither attempt executed the tool commands appearing in that response.

The structured retry returned **APPROVE**, confirming both regressions would
fail without their fixes. Its remaining suggestions do not change this slice:
current standalone producers do not pass a worker train, and error-class
metadata is not part of the added durable minimum. A future producer that
changes those contracts must extend the mixed-log tests; no speculative carrier
or exception wrapper was added here.
