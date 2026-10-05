# Dispute 1 — ruling (independent, Claude Opus) — WI-806 at `44c9ddfd`

Adjudicator: independent Claude Opus, a fresh session, the adjudicator of
`003-ADJUDICATE-44c9ddf.md` and `004-ADJUDICATE-44c9ddf.md`. I wrote none of the
code, rows or reviews in dispute. My calls are final (OI-103 Q3). Ruled here:

- (B) Sol's retained REVIEW-A MAJOR against the builder's D-004 residue;
- (C) Codex Luna's two REVIEW-B points;
- the SN-029 text for the coordinator to file as a pending open item.

Read: the design note's checkpoint ruling, Q-8 (with the coordinator's reading
the owner confirmed) and change 27; chapter 4 §7 and the landing operation;
`docs/decisions/wi-806.toml` D-003 and D-004; `sol-review-a-r1.md` to `-r3.md`;
`luna-review-b-r1.md`; 001 and 002; the code named in 003.

## Basis (probed, not trusted)

- **The residue, reproduced outside the test file** (`review-tmp/adj806-r2-mut/
  residue.py`, against the lane's own `check.py --text-then-act`):
  - A lane makes a text commit then an act commit, on a trunk it contains. Its
    legitimate `git merge --squash` passes the step (exit 0).
  - Abandoned with `git restore --staged .`, `git restore .` and `git clean
    -fd`, SQUASH_MSG stays.
  - I hand-typed the tip's registry and record bytes, plus an unrelated
    non-spine file. The spine and record are **byte-identical to the legitimate
    squash's**, and the step exits **0**. That is the residue, confirmed.
  - The same index without SQUASH_MSG exits 1. One spine byte off the tip exits
    1 with the rebase hint.
  - Committing deletes SQUASH_MSG, and the new HEAD is no longer an ancestor of
    the tip. The window is one commit, as Sol and D-004 both say.
- **How the message survives.** `git reset`, `git reset --hard`, `git stash`,
  `git checkout <branch>` and `git switch` each delete SQUASH_MSG (probed). Only
  path-level abandons keep it: `git restore`, `git rm --cached`, `git
  read-tree`. The ordinary ways to abandon a squash close the window before it
  opens.
- **The exemption is verified on content.** `_squash_lines` admits the index
  only when two conditions hold:
  - HEAD is an ancestor of the named tip, and the staged approval-act
    registries and record are byte-equal to the tip's;
  - every commit HEAD..tip then passes `commit_text_then_act_lines`.

  Mutants M07 (no ancestor check), M08 (no byte equality) and M09 (folded
  commits not judged) are each killed by a cited test (003). SQUASH_MSG decides
  only WHICH commits are judged, never WHETHER anything is judged.
- **Luna (1).** `git diff --stat cde27048 44c9ddfd -- docs/requirements/
  interfaces.toml` is empty. IF-129's only contract cell is `data =
  "split_changed_cells: the approved and traced changed cells, before and
  after"`, at the anchor and at HEAD. `git grep "re-attest it in this commit"
  cde27048` finds the phrase in no registry. In code it appears only in
  `acceptance_record.staged_spine_findings`' warning text (`:1306` at
  `cde27048`), and in a test and design prose.
  - No IF row names `staged_spine_findings`.
  - The lane rewrote that warning ("re-attest it in the NEXT commit",
    `acceptance_record.py:1314`).
  - `tests/test_trajectory_staged.py:328-330` and
    `test_no_refusal_text_offers_amend_plus_flip` pin it.
  - The design matrix (ch.4 line 630, README line 204) mapped the warning's
    phrase to IF-129 by mistake.
- **Luna (2).** Mutant M05 (a commit judged against its first parent only) turns
  `test_a_refresh_merge_is_judged_by_what_neither_side_carried` red: a lane
  refresh-merging trunk's separate text and act commits is refused. A
  first-parent rule refuses the two-commit form the rule mandates, whenever a
  lane refreshes by merge.
  - What all-parents admits is only content a parent carried.
  - On a lane, the slot's walk (`rev-list HEAD..branch`) judges every commit
    behind the second parent too. Sol r3 confirmed it catches bad commits on
    merged side branches.
  - A merge's own content, a value no parent carried included, is still
    refused (M17 and M20 are killed by
    `test_a_row_only_one_parent_carried_is_judged_by_its_cell_values`).

## Rulings

- **(B) Sol's retained MAJOR (D-004's residue): ACCEPT the residue as recorded,
  and REQUIRE that the rows state it.** No code change.
  - The commit the residue admits gains nothing a sanctioned path does not
    already give. Its spine and record are byte-identical to what `git merge
    --squash <tip>` stages from the same HEAD (probed). Every commit HEAD..tip
    was judged on the way, so the text was committed, and readable, before its
    act, in the lane.
  - Q-8 exempts the landing squash for exactly that reason: "the mechanism to
    mitigate risk is now placed in lane". Anyone holding that tip may land it
    as a squash today. Admitting the same bytes under a hand-typed commit adds
    no capability, and keeps no unjudged text out of anyone's sight that the
    squash would have shown.
  - Sol's point is that Q-8, as the owner confirmed it, keeps "any other commit
    made directly on trunk" to separate text and act. That is true of every
    commit whose spine and record are not a judged tip's. A commit that is
    exactly a judged tip's IS a squash in everything the rule reads, and the
    rule cannot see more than that.
  - Every change that would close the window needs a provenance marker or a
    history walk, and both are forbidden ("enforce at the commit against its
    parent; no marker convention, no history archaeology"):
    - **(c) refusing a hand-typed commit identical to the tip** needs a record
      of whether git or a hand produced the index. Git keeps none beyond
      SQUASH_MSG itself.
    - **Requiring the squash message in the commit message** (a commit-msg
      check for git's "Squashed commit of the following:") is a message marker
      convention. It is forgeable, so it would add a marker without adding
      assurance.
    - **Requiring the whole index to equal the tip**, not just the spine and
      record, needs no marker. But it narrows nothing the rule protects, since
      the extra content is not spine text. It would also refuse a hand landing
      that regenerates views or moves the spec in the landing commit. Rejected
      as cost without benefit.
  - Forging SQUASH_MSG by hand changes nothing either: the content checks still
    decide, so a forged message can only exempt what a real squash of the
    named tip would.
  - **What IS required:** the rows the owner reads must state the residue, so
    the approval blesses the behaviour the code has. LLR-302's squash sentence
    said "During a squash landing", narrower than the code's key. The
    restatements are in 003 (LLR-302 `detail` and `rationale`) and 004
    (LLR-173's pointer phrase; TC-173's squash clause, which also called a
    stale message "judged plainly", contrary to its own cited test).
  - For the coordinator: D-004's `review` field can record "residue ACCEPTED
    by the in-lane adjudicator, dispute-1-ruling.md; stated in LLR-302 and
    TC-173". D-004 stays high-risk for the owner's look, since it keys hook
    behaviour on SQUASH_MSG.

- **(C1) Luna's MAJOR, "IF-129 not amended": REJECTED. The coordinator's
  refutation is upheld.**
  - The obligation behind the matrix line is that the retired advice
    disappears. It lived only in `staged_spine_findings`' warning, and the lane
    changed that warning and pinned it with tests.
  - IF-129's contract never carried the phrase, before or after the lane.
    Amending it would be churn that blesses nothing.
  - WI-806's Done-when lists IF-129 among the rows "amended or added". The close
    note should record "IF-129: nothing to amend; the retired phrase lived in
    `staged_spine_findings`' warning, rewritten at `acceptance_record.py:1314`
    and pinned by `tests/test_trajectory_staged.py:328-330`", so the box is
    closed honestly rather than silently.

- **(C2) Luna's MINOR, "all parents, not the first parent": REJECTED. The
  builder's D-003 is upheld.**
  - The spec's and chapter 4 §7's "against its first parent" describes the
    linear lane commit the rule was drafted for. Applied literally to a merge,
    it refuses every lane that refreshes over trunk's own two-commit act, the
    very form the rule exists to require (M05 is red on that test).
  - All-parents loses no content: every commit behind a lane merge's other
    parent is judged on its own by the slot's walk, and a merge's own text,
    combined values included, is still refused.
  - LLR-302 states the multi-parent rule plainly, so the row and the code
    agree.

## A separate finding (not a dispute point, not a RETURN cause; for the coordinator to file)

- **A hand MERGE on trunk does not judge the merged branch's commits at the
  hook. A hand SQUASH does.** Probed (`mergehook.py`):
  - A side branch holds one `--no-verify` commit mixing text and the act.
  - `git merge --no-ff --no-commit side` on trunk passes the step (exit 0). The
    index matches MERGE_HEAD, and `staged_text_then_act_lines` does not walk
    HEAD..MERGE_HEAD as `_squash_lines` walks HEAD..tip.
  - On a lane the slot catches it.
  - Directly on trunk, landings are squashes (OI-103 Q4), and any direct trunk
    commit can already skip the hook with `--no-verify`. So this widens no
    sanctioned path.
  - LLR-302's own rationale ("a hand landing never meets the merge slot")
    argues for judging a hand merge's incoming commits the same way. That is a
    small, separate WI (one shared walk of HEAD..MERGE_HEAD beside the squash
    walk), not something to fold into this lane.

## SN-029 (the owner's row; held, not edited; for the coordinator to file as a pending open item)

001 recommended deleting the "sanctioned" appositive from `acceptance`. I
**confirm** that. I **update** 001's suggested `why` text: its "which no
sanctioned path now does" is itself untrue at landing, because a landing squash
is sanctioned and carries a lane's amendment and its flip in one trunk commit.
Full replacement cells, byte-exact, each differing from the live cell only in
the one sentence named:

- `acceptance`. This deletes ", the one signal the sanctioned amend-and-flip
  path would otherwise hide":

```text
A cumulative level names the highest tier a human still approves, compared against a separately derived SPINE STAGE (which tier is in process) via a declared, auditable mapping. Every failure direction — an unreadable stage, an out-of-range level, a wrong-typed dial — resolves toward MORE human involvement, because the failure that matters is a machine approving something a human meant to hold. Each acceptance is anchored ON THE ACCEPTED ARTIFACT'S OWN ROW — the commit whose tree carries the accepted text, plus a digest of that row's normative cells — never in a second registry keyed on the same artifact. Text that has moved away from what was accepted surfaces regardless of any Status movement, so an AMENDED requirement drops the derived stage exactly as a newly introduced one does. Each automated approval on a released tier appends a durable record (row, transition, acting reviewer, commit) distinguishable from a human approval by query.
```

- `why`. This replaces "is sound only while every amendment flips its row in the
  same commit — precisely the sanctioned path an amendment detector ignores — so
  the blessed way to amend an attested requirement is invisible to every
  consumer, and" with "returns a commit that already carries the amended text,
  so its diff is empty on exactly the rows an amendment detector exists to
  catch: an amendment to an attested requirement is invisible to every
  consumer, and". This is the argument LLR-173's approved rationale makes:

```text
The unattended layer only pays for itself if a walk-away run actually walks away — so what stops it must be exactly the set of judgements the owner reserved, and nothing else. A three-value gate-authority enum (`attended` / `single-approve` / `autonomous`) cannot express "TCs are human-held but LLRs are not", the distinction an owner actually wants to dial, and leaves each consuming table free to re-interpret the same word with its own fail-safe direction. Answering "has this been approved?" by walking git for the newest commit where a row reads `Verified` returns a commit that already carries the amended text, so its diff is empty on exactly the rows an amendment detector exists to catch: an amendment to an attested requirement is invisible to every consumer, and a stakeholder need has no anchor at all (an SN has no Status cell).
```

- Two older staleness points stay outside WI-806, as 001 said, for the same
  owner sitting:
  - `acceptance`'s "a digest of that row's normative cells" predates the
    whole-file copy;
  - `why`'s "an SN has no Status cell" is untrue now that needs carry `status`.

## Owed

- To the authoring lane: 003's and 004's replacement cells, byte-exact, in
  their own text commit.
- To the builder: 003's owed test
  (`test_a_refresh_merge_combining_two_text_commits_beside_trunks_act_passes`).
- No code change follows from (B), (C1) or (C2).

## Aftermath

No act follows from this ruling. The act comes after the rebase, the landed
restatements and a fresh verdict, as 004's aftermath gives it.

RULING: residue=ACCEPT (rows to state it) luna-major=REJECTED luna-minor=REJECTED
