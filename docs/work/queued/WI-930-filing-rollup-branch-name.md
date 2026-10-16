+++
id = "WI-930"
title = "Filing a review no longer refuses a branch named for the rollup generator's directory"
workstream = "process"
sr_refs = ["SR-235"]
specref = "docs/decisions/coordinator-2026-10-15.toml"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "none"
needs = ["WI-911"]
+++

## Context

The owner ruled (coordinator-2026-10-15 D-011) that WI-852's rollup
branch-name refusal is contrived. The audit of guards built on contrived
findings
(`docs/plans/2026-10-11-review-churn/audit-contrived-guards-2026-10-15.md`)
grades both of its rows CONTRIVED: it needs a hand-chosen branch that
collides with a generated directory, and its letter-case variant cost two
more full-lane gates.

The original rationale, read before drafting: WI-852's third full-lane
review found that filing on a branch named `rollup` writes the round into
`docs/reviews/rollup/`, which the rollup generator owns and prunes. The
coordinator argued it contrived, since the claim mints `wi-NNN` branches and
no supported workflow names a lane `rollup`. The dispute sitting ruled it
FIX under the threat model of the time, which asked only whether the host
was compromised: "an unusual input on a supported path, not a contrived
host". The fourth review then found `Rollup`, and the compare became
case-insensitive (wi-852 D-005 to D-007).

Under PROCESS.md section 6 as the owner extended it on 2026-10-13, a
scenario that needs ordinary tools in an order no supported route produces
is contrived, and a hand-chosen name alias lies outside every promise. No
kit route makes a branch named `rollup` in any letter case: the claim mints
`wi-NNN`, and the coordinator files from the lane's worktree. So removing
the refusal reopens nothing a supported route reaches.

The same function's other branch-name refusal, a branch the round reader
cannot read back as one review scope (such as `feature/x`), is graded
PLAUSIBLE and stays. The rollup directory's one declaration,
`kitlib.verdict.ROLLUP_DIR`, also stays: the generator binds it, and moving
it back would undo a decision (wi-852 D-006) for no gain.

## Deliverables

1. **Delete the refusal.** In `project-trajectory/scripts/review_brief.py`,
   `file_review` loses the casefolded comparison of the round directory with
   `kverdict.ROLLUP_DIR`, its comment and its `BriefError`. Nothing replaces
   it.
2. **Contract text.** In the same module's docstring, IF-288 drops "and
   whose directory is not the rollup generator's own", and IF-289 drops "or
   names the rollup generator's directory". `docs/interface-reference.md` is
   regenerated. IF-175's sentence on `ROLLUP_DIR` in `kitlib/verdict.py` is
   unchanged: it describes the generator's directory, which is still true.
3. **Tests, both deleted, nothing inverted.**
   - `tests/test_review_brief.py`,
     `test_a_filed_coordinator_review_appears_in_the_rollup`: the
     `for lane in ("rollup", "Rollup", "ROLLUP")` block and its comment.
   - `tests/test_review_brief_git.py`,
     `test_filing_a_review_exits_zero_and_writes_only_the_round_file`: the
     three-branch checkout loop and its comment.
   The `feature/wi-900` refusals in both tests are kept.
4. **Spine rows** (Terra authors, on the text WI-911 lands; judged at the
   lane's checkpoint sitting):
   - **LLR-313** (Approved), **amended**: "and the record's directory is not
     the rollup generator's own" is deleted from the `file_review` clause.
   - **TC-333** (Approved), **amended**: Method drops "or whose branch
     names the rollup generator's own directory"; Expected drops "and a lane
     whose scope is the rollup generator's own directory". Its test list is
     unchanged.
   - **SR-235** (Approved), **unchanged**: it promises a recorded verdict
     or a refusal, and names no directory.
5. **`RESYNC_PACK.md` entry**, anchored at a trunk commit: a shipped script
   changes. It says filing no longer refuses a branch named for the rollup's
   directory, and that only a hand-named branch reaches it. Nothing migrates
   and no adopter setting changes.

## Done-when

- `review_brief.file_review` reads no `ROLLUP_DIR` and holds no rollup
  comparison. Fails before the change. No behaviour test is added: the only
  behaviour the deletion changes is a hand-named branch's, and a test for it
  would pin the residue.
- The two rollup test blocks are gone, and both tests still pass with their
  `feature/wi-900` refusals.
- LLR-313 and TC-333 carry the amended text, judged at the lane's
  checkpoint sitting.
- The IF-288 and IF-289 docstring clauses are gone and
  `docs/interface-reference.md` is regenerated.
- `RESYNC_PACK.md` carries the entry.
- The commit bar is green on the lane tip (smoke tier and budget enforce);
  `check_trajectory.py --strict` exits 0.

## Scope answers

- **S1, independently landable deliverables.** One. The deletion, its
  tests, its contract text and its spine amendments land together. WI-852's
  other removal, the duplicated-count refusal, touches different code
  (`kitlib/sitting.py`), a different SR chain (SR-232: LLR-310, TC-327) and
  carries an owner call this row does not, so it is its own row. Their one
  shared surface is `test_a_filed_coordinator_review_appears_in_the_rollup`,
  a trivial rebase. Either may land first; this one waits on WI-911.
- **S2, authority over a hold, an act or a gate.** None given. Filing
  writes a round file that the merge gate reads as today; this row removes
  one refusal before the write. No `## Trust` section.
- **S3, closed coverage.** The promise over branch names stays a
  construction: a branch is filed when the round reader reads its round path
  back as that branch's scope, and refused otherwise. The bound is the
  branches the kit's routes produce (claim-minted `wi-NNN`). A hand-named
  branch that collides with a generated directory, in any letter case, is
  outside it, stated as residue in the RESYNC entry; PROCESS.md section 6
  already places hand-chosen name aliases outside every promise.
- **S4, planning need: `none`.** One script, a deletion, no `## Trust`
  section. IF-288 and IF-289 are the same command's arguments and exit
  codes, edited by one clause each. The tests that change are deletions.
- **S5, architectural delta.** None added. One refusal and one dependency of
  `review_brief` on `kitlib.verdict.ROLLUP_DIR` go away.
- **S6, dependencies.** `needs = ["WI-911"]`, hard: WI-911 amends LLR-313
  and TC-333 (keeping the rollup clause) and edits `review_brief.py`,
  `tests/test_review_brief.py` and `tests/test_review_brief_git.py`, so this
  row's amendments are authored on the text it lands. No new third-party
  package, tool or service.
- **B1.** No deliverable hides in the Context.
- **B2.** No split is minted on a work branch; the sibling row is filed on
  trunk.
- **B3.** No consumer re-derives a past decision.
- **B4.** No owner act or credential in the Done-when.
