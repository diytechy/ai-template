+++
id = "WI-922"
title = "SR-154's single-plan hold reads under its own condition, the plan gate's unreachable cap branch is deleted, and the landing shapes the gate does not judge are stated as residue"
workstream = "process"
sr_refs = ["SR-154"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "none"
needs = ["WI-913", "~WI-921"]
+++

## Deliverable

Closed in its lane on 2026-10-16, after its post-checkpoint gate:

- `plan_gate._cap_problems` no longer has a branch for a second critique
  that neither approves nor names a BLOCKER or MAJOR finding; its docstring
  states why no such critique reaches it. The two premise tests are kept
  and pass, as do `tests/test_plan_gate.py` and `tests/test_plan_filing.py`
  in full.
- IF-295's contract body states the landing shapes the gate does not judge
  (a build commit made on a detached HEAD in a lane worktree, a lane merged
  into trunk by hand, an alias-branch squash, a squash after `git stash`, a
  file-copy landing) as residue, and the interface reference carries it.
  The shipped hook's `plan-gate` entry states that a squash landing on trunk
  is judged by each lane commit it carries, and points at that list.
- SR-154's requirement moves "when unattended work reaches integration"
  inside the routing predicate, so the single-plan hold reads under its own
  condition; sitting 004 ruled it CLARITY, and act seq 122 re-attests it.

No RESYNC entry, as the Done-when rules. LLR-337's rationale, which reads
wider than the stated residue, is left for its next sitting (wi-922 D-005).

## Context

Filed on trunk on 2026-10-15 as WI-913's successor (coordinator-2026-10-15
D-002) and claimed the same day. The owner narrowed it in the re-scope walk
(coordinator-2026-10-15 D-013, under D-010 and the 2026-10-13 plausibility
ruling in PROCESS.md section 6, "Review threat model").

What stays is the two MINORs that wi-913 D-010 routed here, because this
lane re-touches SR-154 and the gate's code:

- SR-154's requirement can be read as if its unattended-integration
  condition scopes the single-plan hold too. The gate holds an attended lane
  at every lane commit and at its landing.
- `_cap_problems` in `project-trajectory/scripts/plan_gate.py` keeps a hold
  that no critique can reach.

What drops is the carried-commit walk, the identity order and the
close-by-content rule. Each landing shape they targeted needs a hand act
that no landing recipe uses:

- a build commit on a detached HEAD in a lane worktree;
- a hand `git merge --no-ff --no-commit` of a lane;
- a squash from an alias branch;
- a squash after `git stash` (recipes section 3 forbids it);
- a file-copy landing.

These shapes are stated as residue instead. So is D-008's item 3: a
Done-when change made on a detached HEAD, with no close, which the
done-when-blessed step judges as nothing; WI-925's lane states it. D-013 supersedes D-008's fold of
item 3 into this row as a fix. The one plausible way a lane commit escapes
its hook, a checkout with no hooks, is WI-926's.

## Deliverables

One lane, one landing.

1. **SR-154's single-plan hold, under its own condition** (spine text, sat
   at the lane's checkpoint). The approved requirement opens "The delivered
   loop content shall, when unattended work reaches integration, obtain ...".
   The single-plan clause comes after that condition, so it reads as scoped
   by it. The amendment moves the condition inside the routing predicate, so
   it scopes only that predicate. The single-plan clause keeps its own
   "where" condition. The row keeps its one `shall` (the owner's ruling of
   2026-10-15, wi-913 D-008), and every approved word is kept. The proposed
   text, for the sitting to judge:

   > The delivered loop content shall obtain, when unattended work reaches
   > integration, each review or critique verdict the declared policy
   > requires from a session that did not author the work — resolved per
   > in-process phase and tier from the delivered agent registry's declared
   > (family x model x tier) rows and only while the declared consent
   > surface that turns managed selection on is present, drawn from a
   > different model family wherever one is configured, degrading only to
   > the documented same-family mode — with every selection logged before
   > launch and a non-converging rework loop escalated through the declared
   > approval level, and, where a claimed work item is marked for an
   > in-lane single plan, refuse build output at its making or landing
   > until a pass record binds its plan and Done-when.

   This moves one phrase and changes no word. The acceptance text changes
   only if the sitting asks.

2. **The cap check's unreachable branch is deleted**
   (`project-trajectory/scripts/plan_gate.py`, `_cap_problems`). The hold
   "the second critique does not approve and has no BLOCKER or MAJOR finding
   to dispute" cannot be reached, from the filing step or from a critique
   file committed by hand. `_critique_problems` is the branch's only caller.
   Before it calls `_cap_problems`, it:
   - runs `kitlib.verdict.filing_refusal` on the critique text read from the
     tree, which refuses a `CHANGES-REQUESTED` that names no finding;
   - reads the word through `kitlib.verdict.effective_verdict`, which turns
     a `CHANGES-REQUESTED` whose findings are all MINOR into an APPROVE.

   A finding's severity is one of BLOCKER, MAJOR or MINOR, read in capitals
   (`score_reviews.SEVERITIES`). So every critique that reaches
   `_cap_problems` names at least one BLOCKER or MAJOR finding. The branch
   goes, and so does the docstring sentence "An empty dispute set authorizes
   nothing". The docstring then states why the blocking set is never empty.
   No other code changes.

3. **The residue, stated once** (shipped text: `plan_gate.py`'s IF-295
   contract body and the shipped hook's comment block,
   `project-trajectory/hooks/pre-commit`). Today:
   - IF-295's body says the gate judges "the commit being made ... and, on a
     squash landing, each lane commit it carries", and names no shape it
     does not judge.
   - The hook's `plan-gate` entry says "Trunk, and a lane with no such row,
     are never judged". That is already inaccurate: on trunk, a
     `git merge --squash` landing is judged by each lane commit it carries.

   The text changes:
   - **IF-295's contract body** gains one paragraph, which is the residue
     list. Proposed:

     > It judges a commit made on a branch named for a claim folder and,
     > on a squash landing, each carried lane commit that such a branch
     > contains. It does not judge a commit made on a detached HEAD, a
     > lane merged into trunk by hand (a merge finished by commit, or one
     > git commits itself, for which git runs no pre-commit hook), a
     > squash whose commits only an alias branch
     > contains, a squash after `git stash` has removed the squash message,
     > or a landing made by copying files. No landing recipe makes any of
     > these; under process.md §6, "Review threat model", they are residue.

   - **The hook's `plan-gate` entry** fixes its trunk sentence and points
     at that list instead of restating it. Proposed: "On trunk, a `git
     merge --squash` landing is judged by each lane commit it carries;
     trunk's own commits, and a lane with no such row, are never judged.
     The shapes no landing recipe makes are listed in IF-295's contract, in
     plan_gate.py."
   - D-008's item 3 belongs in the hook's `done-when-blessed` entry, and
     WI-925's lane carries it there as part of the one residue list it
     rewrites, so this row does not touch that entry.

   `docs/interface-reference.md` is regenerated from the new contract body
   in the same commit.

Unchanged: the gate's behaviour on every input a supported route makes, the
pass record's grammar, the filing step, the merge slot (`landing_refusal`),
`kitlib.done_when`, and `kitlib.git.squash_commits`.

## Spine rows

- **SR-154:** amended (deliverable 1), sat at the lane's checkpoint.
- **LLR-337:** unchanged. "A second-round non-approval additionally requires
  an accepted dispute dismissal of every blocking and major finding" still
  holds for every critique that reaches the check. `_cap_problems` stays in
  its symbol list.
- **TC-367:** unchanged. No test it cites drives the deleted branch.
- **IF-295** (`interfaces.toml`, status Drafted): unchanged. Its contract
  body in the code is text (deliverable 3), and its exit-code contract
  stays the same.

## Done-when

- `_cap_problems` has no branch for a second critique that neither approves
  nor names a BLOCKER or MAJOR finding, and its docstring states why no such
  critique reaches it. No test can fail on the code before the change,
  because the branch is unreachable. The two premises that make it
  unreachable stay pinned, and both tests are kept:
  - the filing refusal:
    `tests/test_plan_filing.py::test_a_critique_outside_the_verdict_format_is_refused_and_nothing_is_written[changes-without-findings]`;
  - the MINOR-only reading:
    `tests/test_plan_filing.py::test_a_minor_only_change_request_passes`.
- `tests/test_plan_gate.py` and `tests/test_plan_filing.py` pass in full.
  Both are in `SLOW_MODULES`, so they are run by name, not left to the
  smoke tier.
- The text changes are in the landing tip:
  - IF-295's contract body in `plan_gate.py` carries the residue list;
  - the hook's `plan-gate` entry carries the corrected trunk sentence and
    the pointer;
  - the `interface-reference` check step is clean.
- SR-154 is amended in the lane and sat at its checkpoint. Its single-plan
  hold reads under its own condition, it has one `shall`, and every
  approved word is kept. LLR-337, TC-367 and IF-295's row are unchanged.
- There is no `RESYNC_PACK.md` entry. The change alters no behaviour a
  supported route reaches and asks nothing of an adopter, and the hook and
  `plan_gate.py` are kit-owned files that a resync overwrites.
- The bar is green on the landing tip: the smoke tier within its budget,
  `check_trajectory.py --strict` clean, and `trace.py --strict` with no
  finding beyond LLR-292's, or none once WI-914 has landed.

## Scope answers

- **S1:** three deliverables could each land alone: the SR-154 amendment
  (it needs a sitting), the branch deletion, and the residue text. They stay
  together:
  - D-010 and D-013 bound 1 and 2 to this claimed row;
  - all three touch SR-154's gate chain, so one lane and one sitting cover
    them.

  If the critique splits them, 2 and 3 land first, since they need no
  sitting.
- **S2:** no. No deliverable gives a file authority over a hold, an act or
  a gate. Deliverable 2 removes a hold that no input reaches. The pass
  record's authority, and WI-913's Trust section for it, are unchanged.
  There is no `## Trust` section.
- **S3:** the row promises no new behaviour over an input space.
  Deliverable 2's unreachability argument covers a closed space:
  - the verdict word is APPROVE or CHANGES-REQUESTED (`kitlib.sitting.REVIEW`);
  - a finding's severity is BLOCKER, MAJOR or MINOR;
  - a CHANGES-REQUESTED with no findings is refused before the branch;
  - one whose findings are all MINOR reads as an APPROVE.

  Deliverable 3 states the gate's bound in section 6's terms: what supported
  routes produce is judged, and the hand shapes are named as residue.
- **S4:** `none`. The row has no Trust section. It changes one script
  family's code, and that is a deletion. The interface seam and the hook
  comment get text only, not behaviour. It promises nothing over an input
  space. Existing tests fully specify the diff. The planmode call under
  `## Calls ruled at filing` covers how the mark takes effect on a claimed
  row.
- **Architectural delta:** none. No state, domain value, input or boundary
  is added. One unreachable branch is removed.
- **B3 and B4:** nothing re-derives a past decision. No Done-when item
  needs an owner act or credential. The SR-154 sitting is the lane's
  in-lane adjudication.
- **Dependencies:**
  - `needs = ["WI-913"]` is met: the gate landed with WI-913 (`b803dd019`).
  - `~WI-921` is met: WI-921 landed (`9d0f1c54b`).
  - WI-926 may edit the same hook file in another region (D-014 item 5).
    Whichever lands second rebases. No edge is added.
  - The residue paragraph cites process.md §6. The plausibility sentence it
    leans on lands with WI-911. The text is true without it, so no edge is
    added.
  - No third-party dependency.

## Calls ruled at filing

- **Q2 still applies** (owner, 2026-10-15, coordinator-2026-10-15 D-002): a
  `git merge` that git commits itself runs no pre-commit hook, so it skips
  every floor step. It stays out of reach, and nothing is built for it. It
  now sits in deliverable 3's residue list.
- Q1 (keep the close rule) and Q3 (leave text-then-act alone) no longer
  apply: D-013 dropped the close rule and the walk change they ruled on.
- **Where the residue list lives** (ruled by the coordinator,
  coordinator-2026-10-15 D-020, for the owner to confirm or overrule): once,
  in IF-295's contract body. The hook's `plan-gate` entry fixes its trunk
  sentence and points there rather than copying the list.
- **Where D-008's item 3 is stated** (ruled by the coordinator,
  coordinator-2026-10-15 D-020, for the owner to confirm or overrule): in
  the hook's `done-when-blessed` entry, the reader it belongs to
  (`kitlib/done_when._staged_base`, SR-156, LLR-307), as part of the one
  residue list WI-925 rewrites there. This row's lane does not touch that
  entry.
- **The planning mark on a claimed row** (ruled by the coordinator,
  coordinator-2026-10-15 D-020, for the owner to confirm or overrule):
  `planmode = "none"` stays in the row. The gate reads a claim copy's mark
  at the lane's base, so an edit made in the lane would not release it. The
  coordinator sets the mark on trunk, in a commit that changes only the
  frontmatter, after the fresh critique of the narrowed copy confirms S4
  and before the lane is cut. Branch `wi-922` has no commits of its own (it
  sits at `769224e01`), so the lane is cut from the trunk tip.

## Critique dispositions

The earlier scope-critique rounds (Codex Sol, medium, 2026-10-15: round 1
CHANGES-REQUESTED with one MAJOR, adopted; round 2 APPROVE in convergence
stance) judged the carried-commit walk, the identity order and the close
rule. D-013 dropped all three, so neither round judged this narrowed copy.
A fresh scope critique of the narrowed copy runs in the lane before any
build.

