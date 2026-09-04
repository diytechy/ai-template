+++
id = "WI-582"
title = "The WI-552 residual sweep: schedule-trace seam declared, needs read from the parsed value, stage-currency test exemption"
workstream = "process"
specref = "docs/archive/work/complete/WI-563-spot-check-the-clean-close-of.md"
buildtier = "medium"
priority = 4
safety_class = "spine"
needs = ["WI-579", "WI-580"]
supersedes = "WI-564;WI-565;WI-576"
+++

## Context

Minted by the owner-directed backlog restructure of 2026-09-02 (plan of record `docs/plans/2026-09-02-backlog-restructure-and-consolidation.md` §2.2; executed out of band as a hand trunk commit series, not by a lane). The absorbed rows are archived under `docs/archive/work/restructured/` with their scope text untouched; their Done-when blocks are QUOTED below under their old ids and remain the spec this row must satisfy — decompose, don't paraphrase.

**Why one row, and why `spine`.** Three one-file fixes minted one-per-finding
by the WI-563 and WI-574 clean-close spot checks. WI-565's own Context argued
for "the same commit range so the residual list from the WI-552 review closes
out whole"; that argument covers WI-564 too, and WI-576 rides along as the
third quick item. `OI-77` is RULED ((a): read the parsed value), so nothing
here waits on a ruling any more. WI-564 was declared `ordinary` but its likely
exit authors a covering TC row, and writing `docs/test/test-cases.toml` is
spine authoring — so this row declares `spine`, runs exclusive, and is batched
with whatever the pending amendment adjudication (WI-578) drafts.

**Standing constraint (owner ruling 2026-09-01, the approval act is the
adjudicator's):** any IF or TC row this lane authors is left `Drafted`; do NOT
flip a `Status`, do NOT run `intake.py snapshot`, do NOT write
`docs/archive/last_approved/` on this lane. The first-approval adjudication
minted at this row's merge performs the act.

## Done-when

1. WI-564's scope below: the schedule→trace seam declared (or the membership
   retagged), `check_trajectory.py --strict` exit 0 on the ERROR line, the
   process finding recorded in this row's Deliverable.
2. WI-565's scope below: the `_SPEC_NEEDS_RE` residual applied per OI-77's
   ruling (read the parsed `needs` value, never re-match the text), plus the
   two cosmetics.
3. WI-576's scope below: the committed-stage currency test gains the
   work-branch exemption its `derive_stage --check` twin has, green on a work
   branch that amends a settled spine row and still red on trunk with a stale
   `docs/stage`.
4. Full suite green.

### From WI-564 (scope, verbatim)

WI-552 arm 5 added `import trace as _trace` inside `schedule.load_oi_status`
(`project-trajectory/scripts/schedule.py:445`), creating a cross-component
import `scripts/schedule` (CMP-008) -> `scripts/trace` (CMP-006) with no <!-- path-ok: CMP module labels quoted from the component registry, not file paths -->
declared IF-### row. `check_trajectory.py --strict` errors on it (exit 1); the
same command at `b6e155d3^1` — trunk immediately before the WI-552 merge — is
ERROR-free, so the red is attributable to that work and not pre-existing.
IN SCOPE: choose ONE of the two exits the checker itself names — declare the
interface row in `docs/requirements/interfaces.toml` (the likely right answer:
the OI readiness gate really is a seam between the scheduler and the registry
reader, and a declared seam wants a covering TC per process.md §8) or retag the
component membership if the two modules genuinely belong to one component. Then
re-run `check_trajectory.py --strict` and show exit 0 on the ERROR line.
EXPLICITLY NOT IN SCOPE: the pre-existing WARN population (undeclared
connectivity, IF-without-TC, LLR CodeSymbol drift) — those long predate WI-552
and are their own burn-down; do not green them here. Also record, in this row's
Deliverable, the process finding this successor exists for: the WI-563
spot-check first passed the WI-552 close as clean because it declared a false
no-toolchain Bar and skipped the mandated `--strict` run. Setting
`[checks] components_check = false` is NOT an acceptable exit — that is
sanctioning the check to green a step.

### From WI-565 (Context, verbatim)

Gated on the owner's ruling by construction: the `open_item` cell above makes
`intake._inject_open_item` mint a `pending` OI at this row's merge and land its
id in THIS row's `needs`, so the successor parks
`waiting:open-item-pending` until the ruling lands (OI-73 exit (B) — there is no
standalone OI exit; the OI is always a dependency of a queued successor).
Riding along, because they are one small pass over the same two files and were
also left on no queue by the first spot-check pass: (i) `intake._OI_ID_RE`
(intake.py:304) is dead — `next_oi_id` reads the watermark and
`trace.live_max_ids`, nothing uses the regex; delete it or use it. (ii)
`check_trajectory.validate`'s docstring disagrees with the shipped
`known_ois=None` coercion at check_trajectory.py:812 (`known_ois = known_ois if
known_ois is not None else frozenset()`); fix the docstring to state what the
code does. Both are cosmetic and neither needs the ruling — but do them in the
same commit range so the residual list from the WI-552 review closes out whole.

(Outside the quote: the `open_item` cell the paragraph describes minted `OI-77`,
which the owner has since RULED (a) — read the value the parser has already
parsed — so nothing here waits on a ruling any more; the fix itself is the
`_SPEC_NEEDS_RE` no-DOTALL residual the OI names.)

### From WI-576 (scope, verbatim)

`tests/test_derive_stage.py:528` (`test_this_repo_s_committed_stage_is_current`)
asserts `recorded["fingerprint"] == kitstage.fingerprint(ROOT, memo=None)` with
no work-branch exemption, while the commit-bar step that makes the same claim
(`derive_stage.py --check`, run through `check.py`) SKIPs on a work branch
because generated freshness is the trunk lane's (concurrency-restructure §5.2).
The mismatch was near-unreachable until WI-572 made lane-side amendment of a
settled `Approved` spine row the normal path; each such amendment moves the
`docs/stage` input digest, so a routine lane now meets a red that the trunk lane
clears one merge later. IN SCOPE: give the test the same branch-awareness its
twin has — reuse whatever `check.py` already consults to decide "work branch"
rather than adding a second notion of it, and pin the exemption with a test so
the skip cannot silently swallow a genuinely stale trunk `docs/stage`. Show the
test green on a work branch that amends a settled spine row, and still RED on
trunk with a stale `docs/stage`; the second half is the point — an exemption that
also disarms trunk would trade a false red for a missed one. EXPLICITLY NOT IN
SCOPE: any change to `derive_stage.py`'s own derivation, or to which artifacts
the work-branch skip covers.
