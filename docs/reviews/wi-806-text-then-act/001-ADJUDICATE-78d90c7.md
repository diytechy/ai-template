# 001 — ADJUDICATE (independent, Claude Opus) — WI-806 text before the act, first approval at `78d90c70`

Adjudicator: independent Claude Opus. I wrote none of WI-806's code (the Claude
Opus builder, `51122e5a`, `78d90c70`) or its rows (GPT Terra, `1832b889`).
This verdict rules the one row awaiting a first approval, LLR-302. The amended
approved rows are ruled in `002-ADJUDICATE-78d90c7.md`.

Read: the brief, the row `docs/work/active/wi-806/WI-806-text-then-act-in-lane.md`,
the design note's checkpoint ruling, matrix row S788-text-then-act and Q-8's
answer, chapter 4 §7, §10 and §11, `docs/decisions/wi-806.toml`, Terra's
`terra-spine-r1.md`, the spine-authoring skill, and SR-140, SR-179, SR-207,
SR-228 and SN-029. Code read: `acceptance_record.py` (`_commit_parents`,
`_text_changes`, `_row_text_moves`, `text_then_act_lines`,
`commit_text_then_act_lines`, `staged_text_then_act_lines`), `check.py`
(`_text_then_act_refusal`, `_text_then_act_mode`, the step), `integrate.py`
(`_text_then_act_refusal`, `_each_lane_commit`, `_merge_refusal`),
`hooks/pre-commit`, `baseline_snapshot.py` (`_ledger_live_rows`,
`_unattested_rows`, `_refusal_text`), `tests/test_text_then_act.py` and the
changed tests in `tests/test_baseline_snapshot.py`.

## Basis (probed, not trusted)

- **Lane bar.** `pytest tests/test_text_then_act.py tests/test_baseline_snapshot.py`
  in the lane gives **141 passed**. The lane tree stayed clean.
- **Mutation probes.** I ran these on a scratch copy at
  `review-tmp/wave14/adj806/probe` (`mutate.py`): nine single-point mutants,
  each run against the whole `tests/test_text_then_act.py` and against the five
  nodes TC-173's `evidence` cites.
  - **Killed by a cited node:** merge judged against its first parent only
    (M5); the squash's own changes judged against HEAD only (M6); squashed
    commits not judged (M7); `Status` counted as text (M9).
  - **Killed only by an uncited node.** Each one is a clause LLR-302 states:
    - added or removed rows not reported (M1): only
      `test_a_row_added_or_removed_beside_the_act_is_refused` catches it;
    - the hook's `--run-steps` dropping `text-then-act` (M2): only
      `test_the_pre_commit_hook_runs_the_text_then_act_step`;
    - the slot ladder dropping the rung (M3): only
      `test_the_merge_ladder_consults_the_text_then_act_rung`. The cited
      no-verify test calls `integrate._text_then_act_refusal` directly, so it
      never sees the ladder.
  - **Survive all twelve tests:**
    - an unreadable parent skipped instead of refused (M4);
    - the slot walking newest first (M8).
- **The unreadable-parent arm is real code.** In a `--depth 1` clone,
  `commit_text_then_act_lines(tip)` returns "commit 5e15546141's parent
  1821558b28 cannot be read in this repository ... so whether it mixes text and
  the act is unknown". The code refuses an unreadable parent. LLR-302's
  "all of its readable parents" says the opposite.
- **The squash exemption is a base the row never names.**
  `staged_text_then_act_lines` adds the squashed tip
  (`list(squashed[:1])`, read by `check.py` off git's `SQUASH_MSG`) as a second
  base. Only that base lets a lane's text and act land as one squash. LLR-302
  says only "first judges every squashed commit" and "compares ... with its
  parent trees". The staged tree's only parent is HEAD, so a literal reading
  refuses every act-taking squash landing, which is the Q-8 landing the rule
  exists to admit.
- **Replacement text checked.** I applied the cells below on the probe copy.
  `trace.py --strict` then gives integrity 0, with the same counts as the lane
  (form-findings 1, the pre-existing LLR-292; paraphrase advisories 3), and
  `check_vocab` is clean.

## Rulings

- [RETURN] LLR-302 -> obligation: one two-tree comparison judges a commit that writes the approval record and reports any approval-act row whose non-Status cell moved or that was added or removed; a merge counts only what no parent carried; the hook refuses the staged tree, a squash landing on its squashed commits; the merge slot refuses each lane commit; a root commit passes -> chain: SR-140 is a fair parent once the rationale says why. Its record names the author of the copy's commit as the acting reviewer. That attribution is only distinguishable by query from the text's own authorship when the text has an earlier commit of its own, and SR-140 asks for exactly that distinguishability. Sideways, it does not overlap LLR-173 (the record), LLR-178 (the mirror invariant) or LLR-245 (refusing to absorb drift). Down: TC-173 verifies it, amended in 002 -> not ready, for four reasons. (1) "all of its readable parents" contradicts the code, which refuses an unreadable parent by name (shallow-clone probe), so the cell drops a fail-closed clause. (2) The squash landing's second base, the squashed tip, is missing, so the text as written refuses the landing that Q-8 exempts. (3) "oldest first ... the first reported commit" is a claim no test holds (M8 survives), and it is not load-bearing, so it should go. (4) The rationale does not tie the row to anything SR-140 asks for ("identifies the text it blesses only when ..." is true of any copy). Replacement cells:
  - `detail`:
```text
text_then_act_lines judges a tree that writes under the approval record against its parent trees and reports every approval-act row in it whose cell other than Status changed, a traced cell included, or which was added or removed; a tree that writes no record is not judged. A record path, cell or row counts only when it differs from every parent, so a merge, a refresh merge included, reports only what neither parent carried, and a diff git cannot read is reported rather than skipped. commit_text_then_act_lines judges one commit against every parent its commit object names; a parent the repository cannot read is reported by name, and a root commit has no preceding text and passes. staged_text_then_act_lines judges the index against HEAD, and against MERGE_HEAD as well while a merge is in progress; before the first commit nothing is judged. During a squash landing, each commit that git's SQUASH_MSG lists is first judged as a commit, and the index is then judged against both HEAD and the squashed tip, so the squash is admitted only when every commit it folds in passes and it carries no text change differing from both. The pre-commit step refuses any reported line. The merge slot judges each lane commit not yet on trunk and refuses the lane, naming a reported commit, so a commit made without the hook cannot land the mixed change.
```

  - `rationale`:
```text
The record names the author of the commit that writes the copy as the acting reviewer of the text the copy carries. That attribution holds only when the text was committed, and readable for review, before that commit: text riding the act has no commit of its own, so who wrote it and who accepted it cannot be told apart by query. Checking only at the hook would leave a commit made without it unguarded, and checking only at the landing would leave direct commits unguarded, so one comparison over two trees serves both. A merge is judged by what neither parent carried because a refresh that brings in trunk's text commit and act commit together is its parents' work, not the lane's own mixed act. A squash landing is admitted on the commits it folds in rather than on trust, because a hand landing never meets the merge slot.
```

  - Every clause of the new `detail` is true of the code at `78d90c70`.
    TC-173's `method` and `evidence`, as replaced in 002, verify each one. Two
    clauses still need a test the builder adds to `tests/test_text_then_act.py`
    (see "Owed to the builder").
  - Not a RETURN cause, a trace note: `_commit_parents` is the parent reader
    this row's `commit_text_then_act_lines` depends on. D-007 extracted it as
    shared, but it is tagged `Implements: SR-148, LLR-298` only, while
    `_each_lane_commit` carries both rows. Tagging it `SR-140, LLR-302` too and
    adding it to `code_symbol` would make the two shared helpers consistent.

## Owed to the builder (test gaps; code review's, not row truth)

- A test that a commit whose parent the repository cannot read is reported by
  name (`commit_text_then_act_lines` in a `--depth 1` clone). M4 survives the
  whole file today.
- A test that a diff git cannot read is reported, not skipped
  (`text_then_act_lines(root, ["0" * 40])` returns a line).
- Neither is needed for the code to be correct. Both are needed for TC-173 to
  verify what LLR-302 now says.

## Dispositions

I am writing no `## Dispositions` block into the WI-806 spec, by the
coordinator's direction for this in-lane sitting: the replacement cells above
are the whole corrective work. The authoring lane applies them byte-exact
(text first, its own commit). A fresh ruling on the landed text then precedes
any act.

## Aftermath (not taken; the coordinator gates the act on the code review)

LLR sits on a rung that the declared gate authority releases. Once the
replacement cells land byte-exact in a text commit and a fresh verdict approves
them, LLR-302's `Status` flips in the act commit together with the re-attest
of the 002 rows. The command is in 002's aftermath.

OUTCOME: RETURN rows=1
