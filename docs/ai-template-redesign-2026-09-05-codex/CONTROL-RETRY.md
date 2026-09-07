# Supervised control retry

**Stopped before integration; pause restored.** The snapshot withdrawal/check
conflict below requires repair and lane reconciliation before another launch.
No work item completed or merged in this segment.

The owner authorized retry with “Okay, you can retry”, after challenging the
unsupported attribution of “Rationale names this ruling”. That attribution is
withdrawn in the [repair disposition](CONTROL-REPAIR.md) and F6; ordinary review
must reconsider the citation finding. This is not new approval of a registry
cell, snapshot or rejected finding.

## Envelope and launch

Resume the original claimed adjudication lane after its corrected Dispositions
and the station refresh pass the declared bar. Launch from the primary checkout
with `./agent-resume.sh`, using the existing routes and policy dials. The first
owed phase is REVIEW-A. The coordinator then owns review, rework, mechanical
close and integration under the existing process. Do not substitute a manual
approval, terminal handback or snapshot copy.

The [control ruling](CONTROL-DECISION.md#owner-ruling-2026-09-06) continues to
apply: first eight completed WIs, two active days or twelve active coordinator
hours, whichever arrives first. The previous segment completed no WIs and ran
1178.346 seconds; carry that time forward, leaving 42021.654 active seconds.
Reported spend is watched against USD1000 with missing figures disclosed.
The retained-adjudicator patch stays deferred until this segment ends.
<!-- fig: derived="out/run-logs/control-window/launch.json; 43200 - 1178.3461733749718 seconds; previous completions in CONTROL-OBSERVATIONS.md" rev=c00cfe57 -->

No runtime change is allowed inside a measured segment. A correctness failure
stops the affected path and closes the segment for repair. At a normal bound,
restore the tracked pause to stop admission and let admitted work drain under
current policy. Re-queue the retained-adjudicator patch after the window closes.
Count across launcher restarts; exit 11 does not renew any budget. Record any
other exit or manual intervention and preserve all incomplete attempts.

## Evidence

Launch identity, UTC times, process id and output will be captured under
`out/run-logs/control-retry/`. The supervisor records actual review, invocation,
integration and Git evidence below after a safe stopping boundary. Preparation
checks are not control observations, and retry authorization is not a passing
review. The preceding [incident](CONTROL-OBSERVATIONS.md) remains in the sample.

## Launch and preparation results

Frozen launch commit: `2081427466297efbac989645f33cabf199378905`.
Runtime repair remains `a7f57c3f`; no runtime, test, routing or policy bytes
changed between preparation and this segment. The original lane's correction
is `39c75d22`. The first station refresh refused an appended-log conflict;
following its conflict-resolution instructions, `f1811071` preserved both
records and regenerated the conflicting generated surface. The final station
refresh passed all 15 steps at `820d567fe727b7a6201c9f3e952a60a526d2a190`.
Actual committed-evidence routing selected REVIEW-A before any build.

Primary launch smoke: 1687 passed, 8 skipped in 60.48s; enforced wall 60.8s/90s.
Conflict-resolution smoke: 1687 passed, 8 skipped in 62.01s; wall 62.3s/90s.
Documentation and strict trajectory passed with existing advisories. The first
launch commit hook requested regeneration after the deferred-row/pause changes;
the generated surfaces were refreshed and the enabled hook then passed.
<!-- fig: derived="out/run-logs/control-retry/{prepared.json,prelaunch-smoke.txt,conflict-smoke.txt,station-refresh-final.txt,launch-commit.txt,prelaunch-docs.txt,prelaunch-trajectory.txt}" rev=20814274; lane=820d567f -->

## Measured segment

Launched `./agent-resume.sh` at `2026-09-07T03:04:07.520926+00:00`, launcher
PID 84987. Admission was paused at `2026-09-07T03:35:05.209074+00:00`; the
supervisor interrupted the owned coordinator/provider process groups at
`03:35:19.481007+00:00`. The launcher ended at
`2026-09-07T03:35:19.510539+00:00`, return code -2 (SIGINT), after 1871.909
seconds (31m12s). Across both segments, active coordinator time is 3050.255
seconds (50m50s), with zero completed or integrated WIs. No successor was
minted; integration time is not applicable, and the lane never reached its
merge queue turn. There was no coordinator restart in this segment.
<!-- fig: derived="out/run-logs/control-retry/launch.json + out/run-logs/control-window/launch.json; 1871.9090379999834 + 1178.3461733749718; primary HEAD remained 20814274" rev=20814274 -->

| Session | Provider | Outcome | Reported wall / cost |
|---|---|---|---|
| 003 | Sol, medium CLI effort | REVIEW-A CHANGES-REQUESTED: correct the rationale and re-attest it; verdict `bf418cd3` | 306s / not reported |
| 004 | Astra, medium CLI effort | Adjudication rework, telemetry role DESIGN-CHECK: preserved reserved scopes and drafted the rationale successor; `d522ef25`, `d69550ef` | 295s / not reported |
| 005 | Opus 5, medium | REVIEW-A CHANGES-REQUESTED: five findings; verdict `588f3c9d` | 537s / raw reported USD3.820941499999999 |
| 006 | Fable 5.1, medium | Adjudication rework interrupted: verdict committed at `668edaf4`; aftermath not committed | incomplete / no final reported cost |

Those records live on the original `wi-605-adjudicate-sr-161-llr-183-ow`
branch, under `docs/reviews/wi-605-adjudicate-sr-161-llr-183-ow/` and its
`docs/iteration/wi-605-...-003/004/005-20260906-22*.log` files. Invocation ids
are `32b5f62074fb4b6b9532659f3161ec42`,
`4bc2a93aa9c0445f836a757761b09710`, and
`c7c94f909ad1498ea95d4f87c1081f73`, respectively. The interrupted Fable CLI
session is `ede0dd0c-5266-416d-a6c9-badf327a36bd`. Missing cost is not zero;
no token counters or ambiguous cumulative context percentages are summed.
<!-- fig: derived="lane docs/iteration/wi-605-adjudicate-sr-161-llr-183-ow-{003-20260906-220408,004-20260906-220937,005-20260906-221448}.log; local Fable session metadata" rev=668edaf4 -->

The scope/rework repair worked on the observed path: both adjudicators received
and retained the WI-601/WI-603 reservations and no LLR snapshot was copied.
The repaired harness ran actual pytest; Sol's check printed 1687 passed/8
skipped, enforced wall 66.4s/90s. Opus's full current-stage bar passed
(15 steps: 12 PASS, 3 SKIP; smoke 68.1s). These greens establish the checks ran, not the
semantic adequacy of the proposed approval.
<!-- fig: derived="out/run-logs/control-retry/launcher.log; lane 005-REVIEW-A-d69550e.md" rev=588f3c9d -->

## Stop and root cause

Opus correctly challenged more than the citation frame. Its five findings
covered the unconditional perspective-discharge claim (the shipped injection
currently runs only through dual-plan), missing counterpart decisions in the
SR-161 chain, prose attached to the wrong successor by the real parser, the
SR snapshot retained after its approval was withdrawn, and the unargued direct
TC-178 -> SR-161 verification link. Fable accepted these and attempted to
withdraw the SR snapshot while drafting corrective work. Those are review
findings and proposed dispositions, not owner rulings or approved cell edits.

The withdrawal hit a different defect: `acceptance_record.staged_snapshot_findings`
requires every changed snapshot to equal its live counterpart in the same
commit. Restoring the pre-copy approved snapshot necessarily differs from
live while that live amendment remains pending. The strict integrity floor
therefore rejected the withdrawal. The committed-history counterpart
`committed_snapshot_findings` imposes the same new-copy invariant at the last
writing commit. Neither represents an explicit withdrawal to a previously
accepted snapshot; both treat it as a malformed new approval copy.

At `03:32:52.916Z`, Fable's real `trace.py --strict-integrity` returned:

> FINDING (approval record): docs/archive/last_approved/docs/requirements/system-requirements.toml is NOT byte-identical to docs/requirements/system-requirements.toml in this commit

The associated current-stage bar returned FAIL (two failed steps); passing
smoke did not hide that failure. Fable restored the disputed snapshot and
staged a ledger exception stating that SR-161 Rationale was not endorsed.
Opus had offered that ledger alternative, so this was not unilateral disregard
of its feedback. It still leaves the mechanical anchor equal to the rejected
live cell: the README is explicitly prose, parsed by nothing and excluded from
the snapshot check. A prose exception cannot restore the missing drift signal
or supply the approval the WI withdrew. The supervisor rejected that route
and stopped before a later review, close or merge could accept it.

The supervisor reproduced the refusal through the actual reader using an
isolated Git index: restore exactly the primary's snapshot blob
`435d8ce708795a5e3f9451ff0d171824b2b3c452` from `20814274` at lane `668edaf4`;
the reader returns the same single NOT-byte-identical finding. The real index
and worktree were untouched by this reproduction. Evidence is
`out/run-logs/control-retry/withdrawal-reproduction.json` and
`fable-verification-extract.json`. No runtime fix was made inside the segment.

## Preserved state and resolution plan

The primary never advanced from its launch commit during paid operation and
no primary approval snapshot changed. The original lane remains at
`668edaf49896608e48bc6ff3cec014840312476a`, clean after preserving and restoring
only its three interrupted paths. Its committed round-006 verdict contains
intended aftermath described as done; the interruption means that aftermath
was not committed and must not be read as an executed act. The original SR/TC
snapshot proposal still exists on this unmerged lane; it is not accepted.

All interrupted staged bytes are preserved in the
[forensic patch](../work/handback/wi-605-control-retry-interruption.patch),
SHA256 `995df79351faa234f99054a5a947b892613edffae03c2d1d747c2b24b50238f3`.
This is evidence, not a terminal handback or a patch approved for application.
It includes valid successor work together with the rejected ledger exception;
reconcile it selectively. No branch was renamed, deleted or reset, and no
accepted review or terminal result was fabricated. The retained-adjudicator
patch is re-queued after the stop, under the restored global pause.

Resolution before another launch:

1. Reconcile the approval-copy contract and its staged/committed readers around
   a reviewed withdrawal to an exact previously accepted snapshot. Determine
   the authoritative rollback target and its approval provenance at that
   boundary; do not add a generic old-blob allowance or a README exception.
   Preserve the prohibition on tampered snapshots, partial copies/deletions
   and copying an unaccepted live cell. Apply the applicable SR-179/LLR-178
   amendment/review route if their declared contract needs changing.
2. Exercise both staged and committed withdrawal, later live amendment,
   unauthorized historical-target selection, and existing invalid-copy cases.
   Keep this failing real-lane reproduction as the acceptance case. Obtain
   independent review of the contract and smallest implementation change.
3. Reconcile the preserved lane: withdraw the unendorsed SR snapshot, retain
   only justified TC evidence, remove the prose-exception workaround, complete
   the parsed successor scopes/counterpart decisions and their acceptance
   prerequisites, and correct premature aftermath claims. Honor the owner-tier
   need; do not weaken ordinary-round coverage merely to match today's code.
4. Pass the station refresh and fresh REVIEW-A, then use the normal adjudication
   close and integration route. This report does not authorize another control
   launch. The pause alone does not prevent resuming an existing claim, so keep
   the coordinator stopped until reconciliation and a later authorized retry.

The sample remains insufficient to select a runner replacement. It demonstrates
that the scope/interpreter repairs functioned in this retry and that approval
withdrawal needs a focused contract repair. Ordinary review/rework rounds are
not counted as manual interventions; the supervisor's stop is one correctness
intervention. The log-conflict resolution was prelaunch preparation.
