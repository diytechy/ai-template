# WI-853 dispute sitting at 349bb13

## dispute

### ROUNDS

**Scope bound.** PROCESS.md §6's review threat model keeps this sitting to a
normal working environment. Two dispute rounds in one lane directory, written
by the coordinator's own entry point, is a normal configuration: this lane has
two of them (`002-` and `005-DISPUTE-findings.toml`). No compromised or
contrived host is needed, so the finding is in scope.

**What I observed at 9cbf1a59 (code unchanged at 349bb135).**

- I reproduced it in a scratch test outside the repo, using
  `tests/test_plan_coverage.py`'s own fixtures (`write_dispute`,
  `findings_toml`, `REWORK_PLAN`, `REVIEW`):
  - Setup: an accepted dispute verdict rules `F2 DISMISS`. The findings file
    beside it records this review's F2. The plan excludes
    `F2 — dismissed: <verdict>`.
  - With that one findings file, `plan_coverage.py` exits 0.
  - With a second findings file added from an earlier round (it also requests
    exactly `F2`, recording a different finding), the same plan exits 1:
    `Excludes: F2 cites …003-ADJUDICATE-abc1234.md, whose finding F2 is not
    this review's F2`.
- The cause is that `_ruled_texts` (line 477) collects every
  `*.toml` beside the verdict whose id tuple equals the binding's requested
  ids. `_correspondence_problem` (line 494) then refuses if any of them
  disagrees.
  - The binding (`kitlib/sitting.render_requested`) records only brief, kinds
    and outcome. Nothing beside the verdict says which findings file the sitting
    read.
  - The existing test `test_a_dismissal_whose_finding_cannot_be_shown_refuses`
    ("two" case) pins this refusal on purpose.
- In the same scratch run, a plain reasoned exclusion for the same F2 that
  cites no verdict path exits 0. LLR-069: "an exclusion without a verdict
  remains reasoned".

**Weighing.**

- **The defect is real.** In a lane whose dispute rounds reuse the same
  requested ids, it refuses a valid dismissal that cites its verdict. In that
  configuration that falls short of the Done-when's "a resolved dispute
  passes".
- **It fails closed.** No unresolved finding passes because of it.
  - SR-236's acceptance is not breached: it refuses "a finding that cannot be
    shown", and two disagreeing candidate files is exactly that.
  - The Done-when's pass case holds and is tested for the ordinary single
    round.
- **The cost of the defect is one refused gate run**, and either of two
  workarounds clears it:
  - dispute ids unique within the lane (this lane's own disputes use `SR155`
    and `ROUNDS`);
  - an exclusion stating its reason without the verdict path, which the gate
    accepts as reasoned.
- **The fix costs far more.** The coordinator's analysis is right that only
  recording the link is sound; accepting any agreeing file reopens the
  fail-open hole that round 1 found. Recording it means changing the binding
  grammar and its reader (`kitlib/sitting`, SR-232/LLR-310), the composer and
  entry point that know the findings file at reservation (`adjudicate_brief`'s
  single `Adjudicates` findings file, SR-234/LLR-315), and the interface rows
  for both. That reaches two other approved requirement chains outside this
  item's Done-when, and it needs another amendment sitting and another
  full-lane review. CLAUDE.md asks for the smallest change that fixes the
  problem in a foundation others inherit. A fail-closed false refusal does not
  justify widening this lane across two other components' approved contracts.
  The class fix should be its own item.

**Notes that do not change the ruling.**

- **(i) The skill doesn't state the workaround.** The coordinator's position
  says the skill states it (unique finding ids within a lane's disputes). At
  this range `session-protocol` §2 states only the refusal ("…or whose
  findings file beside it records another finding under that id"), not the
  workaround. The follow-up item should name it until the binding records the
  findings file.
- **(ii) A design gap, outside this finding.** A disputed finding can be
  excluded with a reason that never cites its verdict, and the gate cannot tell
  that from any other reasoned exclusion. SR-236 binds only exclusions that
  cite a dispute ruling, so this is outside this finding. It is worth weighing
  in the same follow-up.

**Follow-up for the coordinator to file:** have a dispute sitting's binding
record the findings file it read (written by the entry point at reservation,
read by `plan_coverage`), and treat an older binding without it as fail-closed.
Until then, the skill should tell coordinators to keep dispute ids unique
within a lane.

RULING: ROUNDS DISMISS not-worth-cost Real and in scope but fail-closed: two same-id dispute rounds in one lane refuse a valid cited dismissal (reproduced, exit 1), while nothing unresolved passes and unique ids or an uncited reasoned exclusion clears it; the class fix records the findings file in the sitting binding and reaches two other approved chains (SR-232/LLR-310, SR-234/LLR-315), so it belongs in a follow-up item, not this lane.
