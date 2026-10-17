Reviewed: cba1d96aa4c65e9baac43a73671f04568966e367

Verified: `git rev-parse HEAD` in the lane worktree prints cba1d96aa4c65e9baac43a73671f04568966e367. Read the full-lane diff (f0ff66cc4...cba1d96aa, with the brief's excludes), the WI-922 spec and its specref, the SR-154/LLR-337 rows and the K1-K4/B1 rubric. Failure classes hunted first, in order of severity: (1) fail-open. If the deleted `_cap_problems` branch were reachable, a second critique with an empty blocking set and an accepted dispute would pass through `_dismissals` (an empty loop). (2) Silent wrong content: the SR-154 amendment changes a word or the residue text misstates the gate. (3) An authored change hidden in a generated view. None holds:
- Unreachability, confirmed by reading and by running the code. `parse_verdict` takes severities only from the closed set and uppercases them (score_reviews.py:84-90, `_finding`). `filing_refusal` refuses a CHANGES-REQUESTED with zero findings (kitlib/verdict.py:889). `effective_verdict` turns an all-MINOR CHANGES-REQUESTED into APPROVE (`MINOR = "MINOR"`, verdict.py:210). `_critique_problems` is the only caller (grep). I drove the real gate with a scratch script that builds a second critique committed by hand, an accepted dispute sitting and a forged pass record:
  - an empty CHANGES-REQUESTED gives `the critique is not a filed verdict: it requests changes but names no finding`, held before the cap;
  - a MINOR-only one gives `an approved critique cites no dispute`;
  - an unchanged MAJOR one with a DISMISS gives `[]`.
- Premise pinning. A mutant with the gate's own `filing_refusal` call removed fails `test_a_pass_record_committed_with_its_critique_is_refused_and_the_two_commit_order_passes`. A gate-level test therefore pins that the gate makes the call, and the Done-when's filing-step test pins what the call refuses, so the chain is pinned end to end. A narrower mutant that drops only the gate's "names no finding" refusal survives the two modules. That is not a realistic regression, because both readers share one function.
- SR-154: only the `requirement` cell changed, and status stays Approved. The word multiset is identical before and after. The cell has one `shall`, and it names no implementation carrier (K2). The moved phrase now attaches to "obtain" and no longer to the coordinated "refuse" (K1). LLR-337, TC-367, IF-295's row and every other registry row are unchanged.
- Generated views: the interface-reference text equals the new docstring. `gen_arch_map --contracts-doc docs/interface-reference.md --check` exits 0, and the check.py step skips on a work branch. No authored change hides in a generated view.
- The hook's corrected trunk sentence is true: `test_a_build_without_a_pass_record_is_refused_at_the_hook_and_the_landing` has a squash on trunk judged by each lane commit it carries.
- Residue shapes. I traced each one through `staged_lines`:
  - a hand merge sets MERGE_HEAD on main, and no rows are claimed for main;
  - an alias branch is not a claim folder;
  - with SQUASH_MSG stashed, `squash_commits` is empty;
  - a file copy commits on trunk.
  All four are unjudged as stated. The detached-HEAD clause is the exception (F1).
- K4: no RESYNC_PACK.md entry. The spec's Done-when rules none: the change is a docstring, a hook comment and an unreachable deletion in two kit-owned, overwrite-class files, so a supported route sees no change in behaviour. I accept that ruling under K4.
- D-003: no blank line before the residue paragraph. I accept it, because the generated reference carries the paragraph.

Done-when coverage:
- (1) Branch and docstring: present (plan_gate.py:378-410). The premises are pinned by `test_plan_filing.py::...[changes-without-findings]` and `::test_a_minor_only_change_request_passes` (both pass), plus the gate-level pin above.
- (2) Both modules pass: 68 passed.
- (3) The text is in the tip: IF-295 body plan_gate.py:59-66, hook lines 305-310, and the interface-reference check is clean.
- (4) SR-154 amended as stated. The checkpoint sitting follows the review rounds (D-001/D-004), so it is pending, not uncovered.
- (5) No RESYNC entry: confirmed.
- (6) Landing-tip bar: `check_trajectory --strict` is clean and the trace has no integrity finding. Smoke was not run, per the round facts.

Commands:
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r1/opus/wi-922 tests/test_plan_gate.py tests/test_plan_filing.py` -> `68 passed in 113.44s (0:01:53)`
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (931 work item(s), 808 done (87%), 30 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=3.`
- `python project-trajectory/scripts/gen_arch_map.py --src project-trajectory/scripts --contracts-doc docs/interface-reference.md --check` -> exit 0
- `python project-trajectory/scripts/check.py --run-steps approval-fresh,plan-gate` -> `SKIP approval-fresh` (work branch); `PASS plan-gate`
- mutant probe (scratch plugin, gate's filing_refusal call removed), same two modules -> `1 failed, 67 passed` (the test named above)
- mutant probe (only the "names no finding" refusal dropped at the gate) -> `68 passed`
- scratch drive of the real gate (empty / MINOR-only / MAJOR second critique with an accepted dispute and a forged record) -> outputs quoted above
- scratch drive: on trunk, `git checkout --detach` then `git merge --squash` of an unplanned lane build -> `staged_lines` returns `commit c070c23cbb: WI-950: build output (src/app.py) before a pass record binds its plan: ...`
- `git status --porcelain` in the worktree after all runs -> empty

- [MINOR] project-trajectory/scripts/plan_gate.py:61 -> for clarity (K1): the residue list says the gate "does not judge a commit made on a detached HEAD". `staged_lines` reads a squash landing whatever the branch, and I observed a `git merge --squash` made on a detached HEAD being judged (`staged_lines` returned the lane commit's build hold). The spec's Context names the real residue: "a build commit on a detached HEAD in a lane worktree". The shipped sentence drops that qualifier and overstates the residue. The error runs in the safe direction, so the gate is not fail-open. -> narrow the clause to "a lane commit made on a detached HEAD (a squash landing made there is still judged)", or use the Context's wording, and regenerate docs/interface-reference.md -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:3359 -> for clarity (K1, requirement-row sweep): LLR-337's rationale says the gate is a release boundary "so a skipped hook, rebase, merge or landing cannot turn an unreviewed plan into build output". The IF-295 residue this lane adds says the opposite for the hook-less shapes: a lane merged into trunk by hand, a merge git commits itself, and a file-copy landing are not judged. The two now disagree on what the boundary covers. -> at the SR-154 checkpoint sitting, or in a later row, qualify the rationale to "a skipped hook, rebase, merge or landing through a supported route (the hook or the merge slot)". The spec keeps LLR-337 unchanged, so this is the sitting's call -> @owner

VERDICT: APPROVE findings=2
