# Supervised control retry

**Stopped before integration; pause restored.** The owner clarified that
worktrees must never write snapshots. The revised resolution below moves
snapshot writing to the mechanical approval path; the withdrawal failure
remains evidence of the incorrect ownership and timing in the existing flow.
No work item completed or merged in this segment.

**Next session:** follow [handoff-2026-09-07.md](../handoff-2026-09-07.md).
Implement and verify the revised repair before retrying. The envelope/launch
sections below describe the previous segment; do not use their launch sequence
or remaining-time figure as a fresh preflight.

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

### Owner clarification and revised resolution

After this report, the owner stated: “a worktree should absolutely never touch
a snapshot” and “Snapshots are only updated mechanically after the adjudicator
or human approves the actual spine change.” This is the current owner boundary,
including adjudicator worktrees. An exclusive spine-authoring worker may edit
in-scope spine content; an implementation worker needing that change returns
a handback. Judgment is the adjudicator's or human's act; the trunk approval
step mechanically updates the approved snapshot. A model invoking a copy
command itself from its worktree does not satisfy that separation.

The owner's subsequent clarification also corrects the earlier “stale approval
evidence” framing: changed text calls for a meaning comparison against the
snapshot; confirmed unchanged meaning preserves existing implementation
judgments. The [work-type diagrams and runtime audit](WORK-FLOWS.md) separate
implementation, exclusive spine authoring, trunk approval and retained
adjudicator context. They are the sequencing detail for this repair.
The owner further clarified that an ID's meaning must remain stable or every
use and reference needs an impact review. Adjudication itself runs in the
primary checkout on the active integration branch, with no adjudication
worktree; see [location and publication](WORK-FLOWS.md#where-adjudication-runs).

The shipped amendment prompt currently directs exactly the wrong ownership:
`project-trajectory/prompts/adjudicate-amendment.template.md:91` tells the
adjudicator “the re-attestation is YOURS and this session performs it” and
supplies `intake.py snapshot --approves`. The first-approval prompt similarly
tells the session to take the snapshot. `adjudicate_brief._aftermath` reinforces
that direction; its comment explains that the old mechanical flip path was
retired, then treats the session as responsible for the aftermath. The copy
command mechanically copies files, but the model chooses when to invoke it
and the reference it supplies names an act without validating its completed
approval evidence. In this incident the copy entered the lane before the
required independent review had settled acceptance.

This supersedes the earlier withdrawal-first repair plan. The primary defect
is assigning snapshot writes to a worker before approval is complete. Adding
another allowed worker rollback path would leave that defect in place.

Resolution before another launch:

1. Remove snapshot-writing and snapshot-repair instructions from adjudication
   and authoring briefs, generated assignments and their supporting guidance.
   The adjudicator records the exact accepted/returned changes and evidence;
   a MEANING classification alone is not approval. Keep human-held approvals
   at the human boundary. No worker edits, copies or restores snapshot files
   or writes approval exceptions into their ledger.
2. Move the whole approval operation to an exclusive coordinator turn in the
   primary checkout on the integration branch. Connect the mechanical copier
   there, after the applicable judgment and required reviews are accepted.
   Publish the approval, any approval Status change and its snapshot in the
   same trunk commit, before releasing the exclusive spine window. A confirmed
   equivalent amendment preserves its approval and implementation judgments;
   publish its equivalence decision and mechanical snapshot update together.
   Uncertain equivalence holds the baseline, and changed meaning requires
   impact review of every use and reference to the ID. Identify the approved
   content and scope so the copier writes that content; a free-form reference alone
   does not establish an approval. Textual change alone does not invalidate
   an implementation judgment when the meaning comparison confirms equivalence.
   Whole-registry copying must not absorb other unapproved changes — that
   clause is [WI-596](../work/queued/WI-596-the-anchoring-copy-s-absorb-le.md)'s
   declared scope, so depend on that row and cite its ledger rather than
   restating it here; two homes for one rule is what this repair exists to
   remove. This is an approval-triggered write, never ordinary freshness
   regeneration.
3. Enforce snapshot ownership at the existing worker-change and integration
   boundaries. **Close the adjudication-actor exception first**: today
   `integrate._approval_act_refusal` -> `_adjudication_lane` ->
   `acceptance_record.merge_approval_refusal` stands the `SNAPSHOT_DIR`
   prohibition down for any branch whose claimed specs are all
   `safety_class = "adjudication"`, so a rule phrased against
   "worker-originated" changes is a no-op against exactly the path that failed.
   Refuse snapshot writes from all WI branches regardless of actor class.
   Remove adjudication worktree dispatch and move its approval effects to the
   trunk operation in step 2. Preserve the `Adjudicates` scope restriction
   there, together with the requirement for an approval and its snapshot in
   one commit. Do not retain the current demand for that pair in a worker's
   delta: it would refuse a legitimate first approval after worker snapshot
   permission is removed. Cover the amendment/no-Status-flip bypass as well
   as first approvals. Reject worker-originated snapshot/approval-ledger changes;
   ordinary synchronization of accepted primary artifacts is not a worker
   approval act. Add explicit read-only/generated guidance in the snapshot
   directory and the briefs that consume it. Preserve byte-for-byte copies:
   a snapshot-only banner inside each mirrored registry would itself violate
   that format, so put the instruction in its directory guidance and prompt
   framing unless the format is deliberately changed.
4. Verify accepted approval produces the intended mechanical snapshot;
   returned or missing approval, or content outside its scope, produces no
   write; worker snapshot edits are refused; mixed accepted/returned registry content is
   not silently absorbed. Exercise both human approval and adjudication paths
   with their actual stage authority and required review sequence. Verify
   meaning-preserving prose changes retain implementation judgments, and
   update the snapshot only with the accepted equivalence decision. Verify
   meaning changes cannot bypass the ID-use impact review, and implementation
   work hands back any needed spine change. Check exclusivity
   through approval and snapshot publication, including restart recovery.
5. Reconcile the existing unmerged lane against the authoritative primary
   snapshots, preserving its evidence and valid corrective successor work.
   Remove the premature approval copy and prose-exception workaround through
   an explicit supervisor repair, not a new worker permission. Complete the
   counterpart decisions and successor prerequisites, then pass fresh review
   and the station bar under the corrected ownership. Do not weaken the
   owner-tier ordinary-round coverage obligation to fit current code.

6. Scope the migration the trunk-turn decision implies, before step 3 removes
   worktree dispatch. Six rows are shaped for it today: `WI-605` in its active
   lane, which step 5 already covers, and `WI-601`, `WI-602`, `WI-603`,
   `WI-604` and `WI-606` queued with `safety_class = "adjudication"`. Removing
   adjudication worktree dispatch changes how all six run, and `WI-606`
   depends on `WI-605`. Migrate their records and scopes to trunk execution;
   do not preserve an adjudication-worktree compatibility route. Settle the three mechanical
   consequences the [boundary table](WORK-FLOWS.md#what-the-runtime-does-today)
   now records: preserve exclusive ownership across entry points and restarts,
   replace the branch-keyed adjudication close, and carry scope-based checks
   and evidence onto trunk approval publication. Existing exclusive admission
   already drains the station, and scoped adjudication already has an explicit
   no-product-bar arm; neither a new concurrent writer nor a new full bar
   follows from moving the turn. None of these is a new requirement; each is an existing mechanism
   whose key or holder the move invalidates.

Separately, reconcile the queued retention restoration with the
[continuity and concurrent-use findings](WORK-FLOWS.md#retained-adjudicator-context)
before admitting that work. Retention is still wanted but is not implemented
in the current runtime; it must not be reported as surviving between WIs today.

The staged/committed mirror checks must be assessed within this corrected
flow; their observed inability to express the existing incident's rollback
remains a recovery concern, not the central product design. Keep the pause
and coordinator stop through repair. The September 7 handoff records the
owner's intended new-session execution and subsequent supervised retry;
this plan does not itself approve disputed spine cells.

The sample remains insufficient to select a runner replacement. It demonstrates
that the scope/interpreter repairs functioned in this retry and that snapshot
write ownership and approval sequencing need a focused contract repair. Ordinary review/rework rounds are
not counted as manual interventions; the supervisor's stop is one correctness
intervention. The log-conflict resolution was prelaunch preparation.
