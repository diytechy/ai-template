# Supervisor review — the approval repair, its proportionality and its lock

Read-only review of `0f106ce9` (the repair), `b830f202`..`79115aab` (the
stopped segment) and `70a17cab` (the stop), against the live source. It adds
four findings to the two the [observations](../ai-template-redesign-2026-09-05-codex/CONTROL-APPROVAL-OBSERVATIONS.md)
already confirm. It changes no code, policy or approval.

## The two recorded findings are real

Both were re-derived independently before this review accepted them.

- **Candidate identity.** `agent_common.head_sha` is `rev-parse --short` and
  its docstring says "Short HEAD sha". `primary_adjudication.session_binding`
  records that value unchanged as `candidate`. `primary_approval._HEX40`
  gates on `^[0-9a-f]{40}$`, so the eight-character `fa90a5b7` excludes the
  real judgment record. The sibling `agent_common.head_sha_full` exists and
  its docstring says bases "are exact, never abbreviated"; the wrong one of
  the two is wired in. This is a one-value defect, not a design fault.
- **Derived successor class.** `intake.parse_dispositions` sets
  `draft["kind"] = safety_class or ("" if planmode == "dual" else "ordinary")`,
  so a `dual` draft with no declared class yields `""`.
  `agent_common.adjudication_review_owed` matches only `spine` or `high-risk`,
  so no round is owed for a successor that later mints high-risk. Zero
  independent rounds ran in the segment.

## Finding 1 — the volume follows the owner's ruling, not overreach

The 8,298 figure is gross insertions. The split is scripts `+2828 -1016`,
tests `+2529 -812`, and docs/prompts/registries `+2941 -226`; existing modules
lost 716 lines as work moved out of them (`handback` -397, `integrate` -189,
`kitlib/verdict` -130). The genuinely new machinery is roughly 1,100 lines
across `primary_turn`, `primary_adjudication`, `primary_approval`,
`primary_publication`, `primary_close`, `publication_verify` and
`kitlib/adjudication`.

Adjudication was NOT previously working on trunk. Pre-repair it ran as a
claimed lane in a worktree, and `handback._lane` treated a primary checkout
holding that branch as an error: "the MAIN checkout at {} has {} checked out,
so there is no trunk checked out to close the lane INTO". What worked was the
adjudicator producing verdicts, from the wrong place and with an ungated
snapshot write. The owner's 2026-09-07 ruling — the turn runs in the primary
checkout with no branch — removed the key three downstream mechanisms were
built on: the close was branch-keyed, the bar was the merge slot's branch
attestation, and publication was a merge. Each needed a new home. The volume
is consequence.

The smaller alternative that was on the table (leave adjudication in its lane,
record a verdict only, let the merge slot copy after the merge, reusing its
existing lock, bar and serialization) was not chosen. That is a settled owner
decision and is not reopened here.

## Finding 2 — the absorption census now has two homes

`primary_approval.absorption_census(root, turn, candidate, accepted)` is the
whole-registry absorb ledger. That is
[WI-596](../archive/work/cancelled/WI-596-the-anchoring-copy-s-absorb-le.md)'s declared
scope, still queued. The overlap was flagged twice before implementation
(`55ad0402`, resolution step 2) and the dependency was not taken. Decide one
home: either WI-596 is superseded by this implementation and closed with that
disposition recorded, or the census defers to it. Two homes for one rule is
the defect class this repair exists to remove.

## Finding 3 — what the lock actually excludes, and for how long

`integrate._slot` takes `out/integrate.lock`. Exactly two callers contend for
it: `integrate.integrate()` (the merge-queue drain) and, since the repair,
`primary_adjudication.run`. Nothing else — not claims, lane spawns, intake,
regeneration or the checks, which sit behind the separate
`agent_common.dispatch_lock_path` coordinator lock the loop holds for its whole
run. So holding `integrate.lock` blocks the merge drain in that checkout and
nothing else.

`agent_common._take_os_lock` is non-blocking on both platforms (`LOCK_NB` /
`LK_NBLCK`). A contender does not queue; `integrate()` returns `fail(lock_err)`
immediately. Holding the slot across several model turns therefore cannot
deadlock, back up or hang anything. It can only make a concurrent merge attempt
fail fast.

`primary_adjudication.run` takes the slot before `session(...)` and releases it
in `finally`, so it is held across the provider call — minutes, not the
sub-second the design assumes. In the single-coordinator case that exclusion is
doing no work: `dispatch._admission`'s exclusive arm admits "only into an idle
station, as the sole toucher of trunk", so no lane is out and no branch is
waiting to merge. What the lock genuinely catches is cross-process: a second or
stale coordinator, a double launch, or a hand-run integrator. Those are real and
the in-process exclusivity reasoning cannot see them.

Crash safety is sound: it is a kernel advisory lock released by the OS on exit
or crash, so the SIGINT could not wedge the next run.

**The durable blocker is not the lock.** `primary_publication.writer_refusal`
reads the on-disk pending turn, and `_slot` consults it for every caller except
the primary turn itself. A merge refuses while an unfinished selection exists
whether or not any process holds the lock. That record, not the lock, is what
survived the interruption and is why the launcher must not be run.

## Finding 4 — a load-bearing docstring is now false

`integrate._slot` still states: "the slot is held for well under a second and
extra lanes buy throughput instead of queueing behind one bar", and describes
the design as speculative rather than pessimistic. That is false on the primary
path. Either correct the docstring, or drop the slot around the provider
session and retake it for publication — which restores the stated invariant
while keeping the cross-process guard where it earns its place. Do not leave a
comment a later reader will trust.
