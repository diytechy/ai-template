# Approval-repair control preflight — 2026-09-07

Preparation for the supervised retry authorized in the
[September 7 handoff](../handoff-2026-09-07.md). This record and pause removal
belong to the launch commit; its exact SHA is captured in the ignored segment
launch record after the hooks-enabled commit succeeds. There is no new budget
or artifact approval in this launch act.

## Frozen revision and verification

- Repair revision: `0f106ce9c1e13a5f86b744311d649a4f69df32f2` on `contract_split`.
- Launch revision: the commit containing this preflight and the pause deletion; capture
  its exact SHA in `out/run-logs/control-retry-approval/launch.json` before launch.
- Full repair suite: 3,735 passed, 22 skipped; retained log
  `out/run-logs/approval-repair-full-catalog-final.txt`.
- Final owner-only mover guard: independently reviewed; 39 targeted checks
  passed.
- The repair and its checks are preparation. They count as zero control-window
  WI completions and zero control-window coordinator seconds.

At the committed repair, strict trajectory is clean (604 WIs, 549 done,
21 cancelled; standing warnings retained). Normal trunk regeneration passed;
its four changed generated lines update provenance only. Snapshot registry
bytes remain unchanged; the snapshot-directory last-write label now reflects
its README guidance edit and must not be read as a fresh registry approval.
The scheduler still lists 17 ready rows; the existing adjudication-first
admission selects WI-605. Route listing resolves the same eight entries and
strong selection returns ANTHROPIC-FABLE. Actual policy, stack and enabled
route files are unchanged. Exact outputs are under
`out/run-logs/approval-preflight-committed-*`.
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/check_trajectory.py --root . --strict" rev=0f106ce9; out/run-logs/approval-preflight-committed-trajectory.txt -->
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/schedule.py --root . ready --format json" rev=0f106ce9; out/run-logs/approval-preflight-committed-ready.json -->

The formatted repair commit bar passed: smoke 1694 passed/4 skipped;
enforcing smoke 55.3 seconds against 90 seconds; docs zero broken links.
[The repair log](../log.d/2026-09-07-approval-repair.md) retains exact test
scope, failed-first evidence and independent reviews. Repeat the per-commit
bar for this launch documentation/pause-removal commit. Remove `docs/work/pause` only in the separate
hooks-enabled launch commit, verify that commit is clean, and freeze its exact
SHA before invoking the normal root `./agent-resume.sh` launcher.

## First admission and immutable primary binding

The supported launch is the ordinary dispatcher launch. Do not call
`primary_adjudication.begin` by hand and do not premint `turn.toml` in the
repair or pause-removal commit. On the clean pause-removal launch base, the
dispatcher applies its adjudication-first admission rule and selects the same
queued WI-605 as the first exclusive primary turn. That supported admission,
while holding the coordinator and integration locks, creates
`docs/reviews/primary/WI-605-<launch-base>/turn.toml`. Its `base` must equal
the frozen pause-removal launch commit; its proposal blob must equal that
commit's queued WI-605 blob; and its scope must be exactly SR-161, LLR-183 and
TC-178. It creates no claim branch or adjudication worktree.

A read-only prospective setup against the prepared working tree already
resolved the launcher command, `opus` model map, queued adjudication row,
`brief=amendment`, and exact three-row scope, and composed the primary prompt
without refusal. The final read-only setup check uses the committed repair revision; its exact
result is retained in `out/run-logs/approval-preflight-committed-setup.json`.
After the normal dispatcher commits selection, the runtime invokes its
normal immutable-binding validator before the session callback. The supervisor
will inspect the resulting turn record against the frozen launch base. No
manual preselection or inserted provider-start barrier is part of this launch.

## Preserved WI-605 incident evidence

- Original branch remains `wi-605-adjudicate-sr-161-llr-183-ow`; it is evidence,
  not an executable approval or a branch to rename, merge, reset, or delete.
- Preserved clean lane HEAD:
  `668edaf49896608e48bc6ff3cec014840312476a`.
- Preserved forensic patch:
  `docs/work/handback/wi-605-control-retry-interruption.patch`, SHA-256
  `995df79351faa234f99054a5a947b892613edffae03c2d1d747c2b24b50238f3`.
- The supervisor migration retains the branch, rounds, report and patch while
  transferring the same open WI-605 to queued primary ownership. The patch is
  not applied wholesale and no duplicate terminal WI-605 exists.

## Carried control accounting

- Completed/integrated WIs carried from the two earlier measured segments: 0.
- Active coordinator time carried: 3,050.255 seconds.
- Remaining twelve-hour allowance: 40,149.745 seconds.
- Earlier segments used local 2026-09-06. A launch on local 2026-09-07
  uses the second active date; preparation itself does not consume an active
  control date. Stop by the end of that date if no earlier bound has arrived.
- Existing stops remain the first of eight completed WIs, two active days, or
  twelve active coordinator hours. US$1,000 remains a watch over reported
  spend; missing spend is disclosed rather than treated as zero.

## Routes and evidence limits

The root launcher supplies the declared managed-routing configuration and the
fallback command `claude -p --model {model} --output-format stream-json
--verbose --dangerously-skip-permissions`; empty launcher model/map overrides
leave `docs/stack.ini` authoritative. The prospective reader resolved `opus`
and the declared phase map without registry or prompt-map refusal.

Historical live evidence remains limited to the recorded Fable 5.1 medium and
Astra medium probes, plus the authorized Claude Code update and recorded Opus
review invocations. Registry listing or collaboration-agent execution is not a
provider authentication probe. Re-probe only a changed route whose live
evidence is absent or stale, and record actual provider identity, session,
result and reported cost. Do not infer billing or availability from selection.

## Queue exclusions and retained debt

- WI-551 remains deferred and excluded from this measured configuration. Its
  retention restoration is outside this retry.
- WI-596 remains queued. The repair supplies much of its absorption machinery,
  but its stated brief verdict/`UNJUDGED` rendering and rollup/intake history
  reader obligations are not silently counted complete.
- WI-601, WI-603 and the other queued adjudications retain their own scopes and
  dependencies. WI-605 may cite their later judgments but does not absorb them.

## Clean checkout and recovery constraint

Selection requires a clean primary checkout. Once a pending turn exists, no
unrelated primary write, preflight edit, pause edit, manual staging, or second
turn may proceed. Publication independently replays the reviewed candidate in
a disposable checkout and mutates primary only for the verified atomic commit.
Ordinary publication refusal or failed hook retains the candidate and
pending selection. An external kill between tree installation and commit can
leave dirty staged residue; the reviewed operational limit requires supervisor
reconciliation before any resume. A crash after the publication commit is recovered by verifying the
terminal spec and exact publication carrier; it must not mint or commit again.
Any dirty residue that cannot be proved to be the publisher's reversible stage
is a stop condition for supervisor reconciliation, not material to commit or
discard opportunistically.

## Final read-only checks after commit

Record exact outputs and hashes for: clean status and current branch; pause
presence before removal and absence at the frozen launch commit; full generated
freshness and required check tiers; queue/frontier plus adjudication-first
selection of WI-605; managed route registry and enabled order; launcher Python
and command resolution; absence of any premature pending record; preserved
lane ref/HEAD and patch SHA-256; WI-551 deferred; WI-596 queued; and carried
time/completion counters. The runtime validates the committed selection before invoking the provider;
the supervisor checks the resulting selection record as described above.
