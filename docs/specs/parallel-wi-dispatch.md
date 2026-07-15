# Design spec — Parallel WI dispatch across coordinator lanes

**Status: PROPOSED for autonomous ratification.** Registered as **WI-162**
(`BuildTier=strong`). The owner requested that every dependency-ready,
non-overlapping work item start without waiting behind unrelated work. This
design adds a dispatcher over the existing WI DAG and `--track` worktree lanes;
it does not weaken the lowest-gate-first rule or make spine work concurrent.

## 1. Problem and boundary

The kit already supports independently locked lanes: `agent_loop.py --track x`
runs on branch `llm/x`, in its own worktree, with coordination files under
`docs/tracks/x/`. Nothing assigns work to those lanes. The root coordinator
therefore consumes one `docs/next-wi` pin at a time even when several queued WIs
are independently actionable.

Parallel dispatch is opt-in and concerns **WI execution**, not parallel writes
to the requirement spine or parallel integration into the iteration branch.
Absent the opt-in, today's single-lane bytes and behavior remain unchanged.

## 2. Declared control and ownership

`docs/parallel` is the consent surface. Its first non-comment line is an integer
maximum lane count. Absent, empty, `0`, or `1` means the existing serial mode;
values above `1` enable dispatch. Invalid or unreasonably large values fail
preflight rather than silently selecting a different concurrency level. The
scaffold does not create the file.

One **dispatcher/integrator** runs in the primary iteration worktree and is the
only process allowed to:

- scan the root WI registry and choose candidates;
- create/reuse lane worktrees and `llm/<lane>` branches;
- write root `docs/status.md`, `docs/next-wi`, `docs/run-state`, or spine rows;
- integrate an approved lane result into the iteration branch; and
- publish the next root actionability snapshot.

The dispatcher holds one repo-level dispatch lock. Existing per-worktree
`out/agent-loop.lock` files continue to prevent duplicate coordinators inside a
lane. An assignment is durable in a dispatcher-owned manifest under `out/`
(runtime state, not a source of truth) and mirrored for humans in the lane's
tracked `docs/tracks/<lane>/next-wi`. Assignment is atomic: reserve the WI in the
manifest before starting its process. On restart the dispatcher reconciles the
manifest against live processes, lane HEADs, and recorded verdicts before making
new assignments. Thus a crash cannot cause two lanes to own one WI.

## 3. Actionability scan

The root `work-items.csv` is the authoritative snapshot. A WI is eligible only
when all of these hold:

1. `Status=queued`; `active`, `blocked`, `deferred`, and `done` are ineligible.
2. Every **hard** predecessor is `done`. A `~WI-n` soft predecessor is ordering
   advice, not an actionability edge, but it remains an overlap/order signal.
3. It is not already reserved, running, awaiting review, or awaiting integration
   in any lane or the root session.
4. It passes the lowest-gate-first filter: an open `[phase]-[g1|g2]` anchor or a
   Draft SR suppresses later development for that phase unless an explicit owner
   order recorded in status selects otherwise.
5. It is safe for a lane under the overlap rules in §4.

Selection is deterministic: first the explicit owner/root `docs/next-wi` order,
then registry order. The scanner fills at most the declared free lane count and
records every accepted and rejected candidate with its reason. It rescans only
from an integrated root snapshot—not from mutually stale lane registries.

## 4. Conservative overlap guard

Parallelism is an accelerator, never a correctness bet. Two candidates may share
a wave only when **all** known conflict keys are disjoint:

- neither has non-empty `SR-Refs`, touches a spine registry, is a `[phase]-[g*]`
  anchor, advances a gate, or otherwise declares spine scope;
- neither is a hard or soft predecessor of the other;
- their non-empty `Campaign` values differ;
- their non-empty `Workstream` values differ;
- their normalized `SpecRef` file surfaces (fragment removed) differ; and
- their declared deliverable/path surfaces do not overlap.

The same comparison is made against every root-active and lane-reserved WI, not
only candidates in the new wave. Missing path metadata is **unknown**, not
disjoint: the WI stays serial unless its spec names bounded files or an owner
explicitly records a parallel-safe exception. A runtime lane diff that escapes
its declared surfaces is quarantined before review/integration and returned for
re-plan; it never teaches the dispatcher a looser rule automatically.

These rules intentionally leave performance on the table. Same-campaign and
same-workstream work often shares concepts even when current file lists differ;
spine edits carry semantic conflicts that git cannot detect. Later evidence may
justify a narrower rule through a new WI.

## 5. Lane lifecycle

For each accepted WI the dispatcher:

1. creates or resets an idle worktree from the current integration HEAD on its
   stable `llm/<lane>` branch;
2. materializes lane-local `status.md`, `next-wi`, `run-phase`, and `run-state`
   naming exactly that WI and its existing `BuildTier` (never downgraded);
3. launches `agent_loop.py --track <lane>` with the normal policy, routing,
   pause/blackout, stall, and iteration-budget controls;
4. moves the lane through BUILD and its own required review round(s);
5. marks an approved result `ready-to-integrate`, or preserves a precise
   blocked/needs-human/rework state without occupying another WI; and
6. integrates ready lanes **one at a time**, in deterministic assignment order.

Lane work does not directly close root registry rows. The integrator verifies
the reviewed diff is within the assignment, applies it without auto-committing,
updates the root WI/log/status surfaces, runs the real commit bar on the combined
root state, and only then commits. If a lane represents a slice/campaign close,
the full suite/gate obligations still apply. After each integration it refreshes
the remaining lanes against the new root HEAD: a newly introduced conflict or
failed rebase quarantines that lane for re-plan instead of guessing through it.

Worktrees and branches are retained while assigned or diagnostically useful.
An idle, fully integrated lane may be cleaned/reused; cleanup never deletes an
unintegrated commit. `docs/pause` stops new dispatch at the next boundary while
in-flight lanes finish normally. Blackout likewise starts no new lane session.

## 6. Review and failure semantics

Review rounds are **per lane assignment**, not pooled across concurrent WIs.
Each reviewer receives that lane's WI, diff, TCs, and commit range; the existing
review-policy count, family heterogeneity, score merge, tripwires, critique loop,
and escalation rules apply unchanged. A verdict for WI-A cannot approve WI-B.

The integrator is not a substitute reviewer. It checks scope, root composition,
and the commit bar. Contested or changed-after-review lane output returns to that
lane for another normal review round. A lane failure affects only its assignment:
other disjoint lanes may continue. Root `run-state` is:

- `RUNNING` while any eligible, running, reviewing, or integrable work remains;
- `NEEDS-HUMAN` only when the next global action needs a human act (with the
  required `Needs <human>` status item and `ask:` line);
- `BLOCKED` only when every remaining WI is blocked; and
- `DONE` only at the declared end state.

If the dispatcher itself cannot prove ownership, overlap safety, or integration
correctness, it starts no new work and pages rather than falling back silently.

## 7. Telemetry and durable evidence

Lane iteration logs and indexes remain namespaced under
`docs/tracks/<lane>/iteration*`. Each row gains/retains stable lane and WI keys.
The dispatcher emits one generated root aggregate ordered by start time and
keyed by `(lane, session)`, so simultaneous session numbers cannot collide.
Aggregation is a projection over lane logs, never a second editable history.

The root `docs/log.md` receives the durable WI close/integration record and real
gate outputs. Dispatcher events record candidate decisions, conflict keys,
assignment/release, review verdict, integration commit, and failure reason. This
supports utilization and false-serialization analysis without treating the
runtime manifest as project memory.

## 8. Never-breaking and safety properties

- No `docs/parallel` means the current one-coordinator path exactly.
- The dispatcher launches only rows already allowed by `docs/agents-enabled` and
  honors `docs/push-policy`; it never pushes under `human`.
- Lane count controls concurrency, not model tier, review depth, gate authority,
  or test strength.
- At most one owner exists per WI; at most one integrator mutates the root; spine
  and gate work remain serial; every integrated commit meets the root commit bar.
- The engine and dispatcher remain stdlib-only, Python 3.8+, Windows/POSIX.

## 9. Ratification decisions

Ratification accepts these design-shaping choices as one contract:

1. opt-in integer `docs/parallel`, absent/≤1 = serial;
2. a central dispatcher plus separate worktrees, with serialized integration;
3. strict off-spine overlap keys and unknown-surface-means-serial;
4. per-lane review rounds before integration; and
5. lane-local telemetry with one generated root projection.

The principal trade-off is conservative utilization versus trustworthy merges.
The design chooses trust: parallelize only what can be proven independent, then
use recorded rejection reasons to motivate future, narrower improvements.

## 10. Implementation WI breakdown (file on ratification)

1. **Actionability + overlap library** — parse the registry/DAG, lowest-gate
   filter, conflict keys, deterministic selection, reason-coded fixture tests.
2. **Dispatcher + worktree lifecycle** — `docs/parallel`, dispatch lock,
   manifest/recovery, lane creation/reuse, process supervision, pause/blackout.
3. **Lane review/integration state machine** — per-WI review rounds, quarantine,
   serialized no-auto-commit application, root gate/close handling.
4. **Telemetry projection** — collision-safe lane/WI identity, generated root
   aggregate, candidate/assignment/integration events.
5. **Docs/scaffold/dogfood** — canonical PROCESS_OPTIONS text, launcher/control
   exposure, optional scaffold wiring if ratified, end-to-end parallel fixtures,
   and a two-independent-WI meta-repo trial.

## 11. Done-when for the implementation campaign

- Two independent dependency-ready off-spine WIs execute concurrently in
  separate worktrees, receive separate review verdicts, and integrate serially.
- Shared campaign/workstream/spec/path, dependency-related, unknown-surface, and
  spine candidates are demonstrably serialized with reason-coded evidence.
- Crash/restart never double-assigns a WI or loses an unintegrated commit.
- One lane may block or fail while another disjoint lane completes; root
  `run-state` remains honest.
- Absent `docs/parallel`, existing single-lane tests and behavior are unchanged.
- Windows and POSIX end-to-end fixtures pass, and the complete campaign closes at
  the full gate bar.
