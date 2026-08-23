+++
id = "WI-467"
title = "Blind re-derivation validation exercise (owner-approved 2026-08-16): two independent agent teams derive a capability breakdown from the stakeholder needs + depth-0 boundary frame ALONE (no access to SR/LLR/TC/IF registries, scripts, or log — the Parnas & Clements guard against implementation-mirroring), on deliberately different decomposition axes (actor/crossing-driven vs lifecycle/value-flow-driven — N-version diversity per Knight/Leveson); a third pass builds the mechanical alignment map (fresh capability <-> legacy SR/LLR <-> existing TC) with three buckets: matched / orphaned-in-legacy / orphaned-in-fresh; every orphan is a FINDING for the sitting desk, never a silent merge. A validation instrument for the settled re-tier v2 layer, NOT a registry rewrite — no spine cell moves under this WI. Protocol and research basis: docs/plans/2026-08-16-tiering-research-memo.md §2/§3."
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

**The exercise already ran in full, on this branch's own history — this
session's honest deliverable is closing the row, not re-running the work.**
Verified by `git log --all` and `git merge-base --is-ancestor`: commits
`cda29c42` (2026-08-16, "the blind re-derivation validation") and `dea8364e`
(2026-08-16, the hat-aware extension) are both already ancestors of this
branch's `HEAD`, yet the spec stayed in `queued/` — the exercise shipped, its
findings were reviewed and acted on, and the closing act was the one step
skipped.

**What ran, read off the artifacts rather than trusted from the commit
messages.** Two independently-derived, axis-diverse capability breakdowns —
[`plans/2026-08-16-blind-derivation-a.md`](../../../plans/2026-08-16-blind-derivation-a.md)
(actor/crossing axis, 21 top-level + 56 sub-rows) and
[`-b.md`](../../../plans/2026-08-16-blind-derivation-b.md) (lifecycle/value-flow
axis, 24 top-level + 49 sub-rows), each reading only the README vision +
`stakeholder-needs.toml` + `external.toml`, each covering 27/27 SNs — plus a
third, hat-aware variant,
[`-c-hats.md`](../../../plans/2026-08-16-blind-derivation-c-hats.md) (80 rows
across 13 hats), owner-approved as an extension ("might expose some other
items anyways"). The alignment pass,
[`plans/2026-08-16-derivation-alignment.md`](../../../plans/2026-08-16-derivation-alignment.md),
is the mechanical join the spec asks for: 71 distinct obligation clusters
across A∪B, 59 convergent (83%), 0 flat contradictions (5 divergences of
placement/strength), 7 tensions hit by both teams independently; 63 legacy
SRs, 47 MATCHED, 16 ORPHANED-IN-LEGACY (8 implementation-born/derived-requirement
class, 7 needs-understatement, 1 accretion), 11 ORPHANED-IN-FRESH (7 real/partial
holes, 4 over-read-or-covered); §4 adds the hat-aware delta (14 of 16 legacy
orphans gain a naming lens, SR-053 alone stays underivable from any input
tried). Every orphan landed as a finding, never a silent merge — no SR/LLR/TC
cell was touched by this exercise itself, matching the spec's "validation
instrument, not a registry rewrite" constraint exactly.

**The findings were not left on the desk — they were already ruled on and
consumed**, by two already-`complete/` follow-on rows this session verified
rather than assumed: `docs/work/complete/WI-468-hat-exposed-obligation-intake.md`
(the four hat-exposed candidates — C-DPR-2, C-DPR-3, C-PRF-1, C-ACC-2 —
proposed as intake options, ruled at the 2026-08-16l/2026-08-17h sitting-adjacent
exchange into `SR-175`/`SR-176`/`SR-177` plus a match-to-existing-`SR-052`) and
`docs/work/complete/WI-470-open-items-a3-coverage.md` (the C-ACC-2 remainder).
`docs/log.md`'s `2026-08-16j` / `2026-08-16k` / `2026-08-16l` entries carry the
run-time account; nothing in this closing session repeats or re-derives that
record.

**Deviation from a fresh execution of this WI's own instructions:** none of
the "spawn two blind agents" protocol ran this session, deliberately — running
it again would not be a second N-version instance in the Knight/Leveson sense,
it would be re-deriving from the same inputs against a spine the earlier run
already diffed and the sitting already ruled on, which is exactly the
implementation-mirroring failure mode the exercise's own guard exists to
avoid (this time mirroring the *exercise's own prior output* rather than the
legacy registries). The honest act available now is verifying the existing
result held up under downstream use, which it did.

## Context

Owner-approved 2026-08-16 after the re-tier v2 close ("the biggest issue is
that we keep trying to reform requirements that already exist — what if we
try the breakdown from scratch, and then come back and see which TCs /
current implementation ties back in?"). The guards, from the memo: blind
derivation (needs + boundary only), scope capped to the current mission (no
deferred wishlist — the second-system guard), and the standing rule that no
legacy row is deleted or demoted without its original rationale read. The
diff output feeds the ONE sitting beside the ratify brief.
