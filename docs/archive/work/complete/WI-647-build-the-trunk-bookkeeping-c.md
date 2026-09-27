+++
id = "WI-647"
title = "Build the trunk bookkeeping commit in an isolated worktree from HEAD and install it under a drift check"
workstream = "unattended"
specref = ""
needs = ["WI-636"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Deliverable

- `bookkeeping.commit` builds every trunk bookkeeping commit (the claim, the
  mint) in a scratch worktree cut from HEAD and installs it by
  compare-and-swap under a drift check (IF-186): an owner edit to an
  in-scope path made while the commit is built is refused by name and
  survives byte for byte; an uncommitted generator input outside the scope
  does not shape the committed artifacts.
- The scope is planned over HEAD in the scratch tree and the same plan
  drives the pre-check and the commit, for the claim and the mint alike; an
  uncommitted edit hiding a committed link refuses by name, one adding a
  link widens nothing.
- The drift check runs after the caller's `before_advance`; a refusal after
  the claim's branch cut leaves the branch for the next claim to re-cut.
- The regeneration runs the scratch tree's committed trunk step and reads
  its write scope from the same committed kit; the harness interpreter
  still comes from the checkout, as IF-186 says.
- The claim's held-status check reads the dial committed at the scratch's
  head through WI-636's `authority.dial_at`.
- Amended, status left Approved, for the joint adjudication: TC-145
  `method`. Traced pointer moved: TC-145 `evidence` gains
  `tests/test_bookkeeping.py`.

## Context

Filed on the arbitration of WI-612's review (Fable, ruling B, 2026-09-26).
WI-612's shared helper, `bookkeeping.commit`, runs the claim's and the
mint's writes and the regeneration in the primary checkout. Paths outside the
step's scope are never touched. A path inside it is guarded only at the
pre-check, so an owner edit landing on it while the step runs (for example the
hand-authored part of `docs/status.md`) can be swept into the commit or
overwritten by the regeneration. WI-612 states that window honestly in the
helper's contract (IF-186), and its restore leaves and names any in-scope
path edited after the step wrote it.

IN SCOPE: run the step's writes and `trunk_step --regen` against a temporary
worktree (or index plus tree) cut from HEAD; immediately before installing,
verify that the primary checkout's in-scope paths still equal HEAD, refusing
by name on any drift; then install the result and advance trunk as today.
Update IF-186's contract to the narrower window this leaves: the install
itself.

NOT IN SCOPE: the held-status refusal and loop trailer WI-636 adds to the
same helper (sequenced first, so both land in one place).

## Done-when

- The step's writes and the regeneration run outside the primary checkout.
- A test injects an owner edit to an in-scope path while the regeneration is
  blocked, and shows the edit survives, is absent from the commit, and the step
  refuses naming the path.
- The commit bar passes, and IF-186's contract states the remaining window.
