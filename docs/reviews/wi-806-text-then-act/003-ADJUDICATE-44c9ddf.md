# 003 — ADJUDICATE (independent, Claude Opus) — WI-806 text before the act, first approval at `44c9ddfd`

Adjudicator: independent Claude Opus, a fresh session. I wrote none of WI-806's
code (Claude Opus builders: `51122e5a`, `78d90c70`, `61f14843`, `2d7f3d39`), none
of its rows (GPT Terra: `1832b889`, `98142025`, `a4d6f7d4`, `44c9ddfd`), and none
of the earlier verdicts. This verdict rules the one row awaiting a first
approval, LLR-302, from the brief
`review-tmp/wave15/brief-wi806-first-r2.md`. The amended approved rows are ruled
in `004-ADJUDICATE-44c9ddf.md`; the builder-reviewer dispute (D-004's residue),
Luna's REVIEW-B points and the SN-029 text are in `dispute-1-ruling.md`.

Read: the brief; the spec; the design note's checkpoint ruling, Q-8 and change
27, and chapter 4 §7; PROCESS.md §3, §4, §7; the spine-authoring skill;
`docs/decisions/wi-806.toml`; 001 and 002; Sol's REVIEW-A rounds 1-3, Luna's
REVIEW-B round 1, Terra's round reports 2-4 and the builder's round-2 spine
list. Code read at `44c9ddfd`: `acceptance_record.py` (`_commit_parents`,
`_text_changes`, `_row_text_moves`, `text_then_act_lines`,
`commit_text_then_act_lines`, `_squash_lines`, `staged_text_then_act_lines`,
`staged_spine_findings`), `check.py` (`_text_then_act_refusal`,
`_text_then_act_mode`), `integrate.py` (`_text_then_act_refusal`,
`_each_lane_commit`), `hooks/pre-commit`, and `tests/test_text_then_act.py` in
full.

## Basis (probed, not trusted)

- **Lane bar.** In the lane, with a fixed basetemp:
  `pytest -p no:cacheprovider -n 4 tests/test_text_then_act.py
  tests/test_baseline_snapshot.py tests/test_acceptance_record.py
  tests/test_trajectory_staged.py` gives **207 passed in 80.69s**. The
  shallow-clone test passed here too. The lane stayed clean.
- **Every evidence node exists.** I checked all 24 nodes TC-173 cites against a
  `def` in their files. All exist. The one text-then-act test not cited,
  `test_no_refusal_text_offers_amend_plus_flip`, pins no LLR-302 clause.
- **Mutation probes.** I ran 21 single-point mutants on a `git archive` export at
  `review-tmp/adj806-r2-mut/base` (`mutate.py`), each against the whole
  `tests/test_text_then_act.py`. **20 killed, each by a cited node:**
  - add or remove ignored (M01);
  - the hook drops the step (M02);
  - the slot ladder drops the rung (M03);
  - an unreadable parent skipped (M04);
  - a merge judged against its first parent only (M05);
  - MERGE_HEAD dropped at the hook (M06);
  - the squash ancestor check dropped (M07);
  - the squash byte-equality check dropped (M08);
  - the squashed commits not judged (M09);
  - the rebase hint dropped (M10);
  - `Status` counted as text (M11);
  - a traced cell excluded (M12);
  - an unreadable diff skipped (M13);
  - a root commit judged against the empty tree (M14);
  - a commit that writes no record judged anyway (M16);
  - a cell counted when it differs from ANY parent (M17);
  - the index judged even when the exemption holds (M18);
  - check.py reading no SQUASH_MSG (M19);
  - presence compared against the first parent only (M20);
  - the index judged against the empty tree before the first commit (M21).
- **One mutant survives every test: M15.** It counts a record path written
  when the path differs from ANY parent, not from every parent. The clause
  "A record path ... counts only when it differs from every parent" is real
  behaviour, but no test holds it. I built the case that tells them apart
  (`m15probe.py`):
  - The lane commits text only to LLR-001's multiline Detail (line 1). Trunk
    commits text only to the same cell (line 9), then takes an act on the SR
    registry.
  - The lane refresh-merges trunk. Git combines the two text commits into a
    third LLR-001 value, and the merge brings in trunk's SR copy.
  - At HEAD that merge passes (`[]`), which is right: the record is trunk's,
    not the merge's. Under M15 it is refused as "LLR-001: Detail in a commit
    that writes docs/archive/last_approved".
  - This is a legitimate refresh shape the mutant would block. The test is owed
    (below).
- **The squash exemption keys on SQUASH_MSG alone, and the row says otherwise.**
  I reproduced the residue myself (`residue.py`, outside the test file):
  - A two-commit lane is squashed onto the trunk it contains. The legitimate
    squash passes the actual `check.py --text-then-act` step (exit 0).
  - I abandoned it with `git restore --staged . && git restore . && git clean
    -fd`. SQUASH_MSG stays.
  - I then hand-typed the tip's registry and record bytes plus an unrelated
    file. Its spine and record are byte-identical to the legitimate squash's.
    **The step exits 0.** The same index with SQUASH_MSG removed exits 1. One
    byte off the tip exits 1 with the rebase hint.
  - git deleted SQUASH_MSG at that commit, and HEAD then no longer lies inside
    the tip. `git reset`, `git reset --hard`, `git stash`, `git checkout` and
    `git switch` all delete SQUASH_MSG as well. Only path-level abandons
    (`restore`, `rm --cached`, `read-tree`) leave it.
  - LLR-302's squash sentence opens "During a squash landing", but the code has
    no notion of a landing beyond the message. An abandoned squash's commit
    gets the exemption, and under the row's literal scope that is a commit the
    general clause ("judges the index against HEAD") should judge plainly.
  - `dispute-1-ruling.md` ACCEPTS this residue. An accepted, deliberate
    behaviour must be in the row the owner reads, not only in a decisions file.
    Otherwise the approval blesses a narrower rule than the code has, and the
    residue reads as a defect against the row.
- **Deviations from 001's bytes.** Two are forced by the code:
  - The squash sentence was restated for builder rounds 1-2. The merge-tree
    equality was dropped, and the exemption now holds on HEAD-in-tip plus byte
    equality.
  - `code_symbol` gained `_commit_parents` and `_squash_lines`, both tagged
    `Implements: ... LLR-302`. This closes 001's trace note.
  - `rationale` is 001's text byte for byte.
  - Sol's round-3 MINOR is answered by round 4's wording: the conditions are
    the exemption's, and a non-ancestor squash is refused only when ordinary
    judging finds mixed text and act.
- **Replacement text checked.** I applied the cells below, and 004's, on a
  detached scratch worktree at `44c9ddfd` (`review-tmp/adj806-r2-mut/rowswt`).
  - `trace.py --strict`: integrity 0, with counts unchanged from the lane
    (form-findings 1, the pre-existing LLR-292; paraphrase-advisories 3).
  - `check_vocab` is clean, and `check_trajectory.py --strict` is clean.

## Rulings

- [RETURN] LLR-302 -> obligation: one two-tree comparison judges any commit that writes the approval record and reports each approval-act row whose non-Status cell moved, or that was added or removed, as that commit's own (what no parent carried); the hook judges the index (against MERGE_HEAD too in a merge), exempting it only while SQUASH_MSG names a tip containing HEAD whose spine and record the index stages byte for byte, and then judging each commit HEAD..tip; the slot judges every lane commit; an unreadable parent or diff is refused; a root commit passes -> chain:
  - Up: SR-140 is a fair parent. Its acting-reviewer field, the copy-writing commit's author, is query-distinguishable from the text's authorship only when the text has an earlier commit of its own. The rationale says exactly that.
  - Sideways: no overlap with LLR-173 (the record), LLR-178 (the mirror invariant) or LLR-245 (refusing absorbed drift).
  - Down: TC-173 cites a node that kills every mutant except M15.

  -> not ready, for one cause:
  - The squash sentence scopes the exemption to "a squash landing". The code grants it to any commit made while SQUASH_MSG names a qualifying tip, an abandoned squash's next commit included (reproduced above).
  - The residue is accepted on its merits (`dispute-1-ruling.md`), so the fix is to state it, not to change the code.
  - The rationale gains the reason content verification suffices: what the exemption admits could equally have landed as the squash.

  Every other clause is true of the code and held by a cited test, M15's clause excepted, and that test is owed below. Replacement cells (`detail`: only the squash sentences change; `rationale`: one sentence appended):
  - `detail`:
```text
text_then_act_lines judges a tree that writes under the approval record against its parent trees and reports every approval-act row in it whose cell other than Status changed, a traced cell included, or which was added or removed; a tree that writes no record is not judged. A record path, cell or row counts only when it differs from every parent, so a merge, a refresh merge included, reports only what neither parent carried, and a diff git cannot read is reported rather than skipped. commit_text_then_act_lines judges one commit against every parent its commit object names; a parent the repository cannot read is reported by name, and a root commit has no preceding text and passes. staged_text_then_act_lines judges the index against HEAD, and against MERGE_HEAD as well while a merge is in progress; before the first commit nothing is judged. While git's SQUASH_MSG names a squashed tip, the index is exempt only when HEAD is an ancestor of that tip and the approval-act registries and record in the index are byte-equal to the tip's; then each commit HEAD..tip is judged against its parents and the index is not. Otherwise the index is judged like any commit, and a refusal tells the operator to rebase the lane onto trunk first. Git keeps no other squash state, so a SQUASH_MSG that an abandoned squash left behind grants the same exemption, on the same conditions, to at most the next commit, since git deletes the message when that commit is made. The pre-commit step refuses any reported line. The merge slot judges each lane commit not yet on trunk and refuses the lane, naming a reported commit, so a commit made without the hook cannot land the mixed change.
```

  - `rationale`:
```text
The record names the author of the commit that writes the copy as the acting reviewer of the text the copy carries. That attribution holds only when the text was committed, and readable for review, before that commit: text riding the act has no commit of its own, so who wrote it and who accepted it cannot be told apart by query. Checking only at the hook would leave a commit made without it unguarded, and checking only at the landing would leave direct commits unguarded, so one comparison over two trees serves both. A merge is judged by what neither parent carried because a refresh that brings in trunk's text commit and act commit together is its parents' work, not the lane's own mixed act. A squash landing is admitted on the commits it folds in rather than on trust, because a hand landing never meets the merge slot. The exemption is verified on content rather than on the message: the spine and record a commit it admits stages are a lane tip's own, byte for byte, and every commit HEAD..tip was judged, so it could equally have landed as that tip's squash; telling a hand-made commit from the squash would need a provenance marker, which enforcing at the commit against its parents rules out.
```

  - The other cells stand: `title`, `sr_refs` (SR-140), `test_refs` (TC-173), `module`, `component` (CMP-006), `phase`. `code_symbol` matches the ten functions tagged `Implements: ... LLR-302`, both `_text_then_act_refusal` homes included.

## Owed to the builder (a test gap, not row truth)

- **One test in `tests/test_text_then_act.py`, named exactly
  `test_a_refresh_merge_combining_two_text_commits_beside_trunks_act_passes`.**
  The scenario is M15's:
  - A lane text-only commit changes one line of a multiline LLR cell.
  - A trunk text-only commit changes another line of the same cell, then trunk
    takes an act on the SR registry.
  - The lane refresh-merges trunk.
  - Assert that `commit_text_then_act_lines` on the merge returns `[]`, and that
    `integrate._text_then_act_refusal` passes the lane.

  It must be red under M15 (`writes & paths` -> `writes | paths` in
  `text_then_act_lines`). `review-tmp/adj806-r2-mut/m15probe.py` is a working
  sketch of the scenario. 004's TC-173 `evidence` replacement cites this exact
  name, so the test lands before or with that text, never after it.

## Dispositions

Per the coordinator's direction for this in-lane sitting, I am writing no
`## Dispositions` block into the spec. The replacement cells above, 004's, and
the owed test are the whole corrective work. The authoring lane applies the
cells byte-exact in their own text commit, the builder adds the test, and a
fresh ruling on the landed text comes before any act.

## Aftermath (not taken; the coordinator resumes this adjudication after rebasing the lane)

LLR sits on a rung that the declared gate authority releases. Once the
replacement cells and the owed test have landed and a fresh verdict approves
them, LLR-302's `Status` flips `Drafted` -> `Approved` in one act commit that
changes nothing else. The same commit re-attests 004's rows. The command is in
004's aftermath.

OUTCOME: RETURN rows=1
