+++
id = "WI-392"
title = "Filed 2026-08-01 by WI-378 out of WI-386's REVIEW-A, whose reviewer disclosed the bias himself (I am a reviewer arguing for less review of a finding class I raised). A DRIVEN FIGURE IS EVIDENCE ONLY AT THE REVISION IT WAS DRIVEN ON, and this repo's records do not say which revision that was or what command produced it - so a stale figure is indistinguishable from a live one without guessing at a re-run. THREE FALSE FIGURES IN ONE SESSION (2026-08-01), each caught by a reviewer's diligence rather than by machine: WI-380's mutation ledger read `2 failed, 7 passed` - true when measured, false the moment round 1 added a test that also reds under the mutant, and the PASS count coincidentally held at 7 while selection went 9 -> 10 so the stale line still read plausible (cost: a full REVIEW-A round); WI-391's filed title read `109 links`, unreproducible at review and re-measured to 154 occurrences / 101 markdown link targets; WI-384's composed-tree paragraph reported `two false positives` in a sentence that itself falsified the count (cost: a full REVIEW-A round). RUNG 1 IS THE ROW: a declared figure names the COMMAND that produced it and the REVISION it was driven at, and a stdlib check over the declared record surfaces flags a declared figure carrying neither - it checks PRESENCE, never truth, which is cheap and has no false-truth risk, and would have flagged all three. THE HARD PART IS WHAT COUNTS AS A FIGURE (a regex over digits drowns in ids, dates, section numbers and byte budgets), so the likely shape is an opt-in marker rather than detection - the kit's usual declare-don't-infer move - which makes the check's honest claim `declared figures carry provenance`, not `all figures do`. RUNG 2 IS NAMED SO IT IS NOT ASSUMED: actually re-deriving by running the recorded command needs an allow-list (commands read out of documents are an execution surface), is only valid against the recorded revision since most figures are legitimately historical, and cannot run the expensive ones (tests+coverage is 634 s) - decide it separately after rung 1 shows how many figures declare a re-runnable command. docs/stack.ini's re-measure note already asks a HUMAN to re-derive its declared numbers and has no enforcer; this row is that enforcer. A FOURTH CASE, ONE LEVEL UP, FOUND WHILE FILING THIS ROW: WI-378's own census was wrong not in a figure but in its POPULATION - it measured the four branches its session brief named rather than the 20 the predicate had governed, and drew a universal (these are the only two) from a sample; its REVIEW-A round 1 caught it and the corrected figure is 3 of 13. The instructive part is that WI-378 explicitly refused to inherit two FIGURES from the same brief and re-derived both, so scope is the harder half - and a convention recording what command produced a number already carries the fix, since running that command (git log --grep=^integrate: merge filtered by merge-base --is-ancestor) enumerates 20 and exposes a hand-picked four. WHATEVER THIS ROW BUILDS MUST COVER THE POPULATION A FIGURE WAS COMPUTED OVER, NOT JUST ITS VALUE - and a FIFTH case followed immediately, in WI-378's own correction of the fourth: it restated the corrected census as 'twelve staled nothing; these seven' when 12+7=19 against a population of 20 (it is thirteen), so a figure DERIVED from a re-derived figure went underived in the very paragraph explaining the hazard. BOTH constraints are now acceptance bars in this row's Done-when rather than prose, because a constraint stated only in prose does not bind; neither widens the build - rung 1 stays presence-only, and a recorded command that enumerates its population (git log ... | wc -l) already satisfies the first. THE OTHER HALF OF THE REVIEWER'S PROPOSAL - capping a record-only review round - WAS MEASURED AND DELIBERATELY NOT FILED by WI-378: across all 20 merged branches only 3 of 13 staled APPROVEs came from a record-only edit, so capping rounds addresses 23.1% of the cost while weakening a fail-closed gate - and TWO OF THOSE THREE ROUNDS CAUGHT A FALSE CLAIM, which is the argument against capping them at all; this row makes the class cheap instead. SCOPE GUARD: provenance on NUMBERS, not a claims-verifier for prose."
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

Rung 1 exactly as the drain plan scoped it (docs/archive/history/backlog-plan-2026-08-01.md
row 6): the opt-in marker convention plus a presence check. Rung 2
(re-derivation) is deliberately NOT built and is recorded as a declared
absence, not implied as covered.

- **The convention, stated once:** `project-trajectory/PROCESS_OPTIONS.md`
  "Signed measurements" part 3 — a driven figure may opt in by carrying, on
  its own line, `fig: cmd="<command>" rev=<revision>` (the exact producing
  command and the revision driven at), or — for a figure computed from
  declared figures — `fig: derived="<how, from which declared figures>"`;
  a `fig-ok`
  line is prose about the convention. Both acceptance bars are in the
  convention text: the cmd must ENUMERATE the population when the figure is a
  count over one (a hand-picked set names its selection principle), and a
  derived figure is itself declared. Every other surface links here.
  Grammar (REVIEW-A rework): a marker whose values are placeholder-shaped
  is the convention quoting itself and declares nothing; each marker on a
  line owns only the attributes that follow it; rev= takes a bare token
  or a quoted string, and a wordless value counts as missing.
- **The check:** `project-trajectory/scripts/check_figures.py` — presence,
  never truth; warn-first, `--strict` exits 1; honest claim ("declared
  figures carry provenance", never "all figures do") in the docstring. Scans
  root `*.md` + `docs/**/*.md` through `check_doc_refs.doc_files` and the
  lifted `authored_lines` (IF-087, so the two doc checks agree on the walk)
  plus `docs/stack.ini`, with `docs/reviews/` records out of scope (a
  verdict quotes defective markers as evidence); `fig-ok` lines and
  GENERATED blocks exempt. Wired
  opt-in as `[step:figures]` (G3, product layer) in `docs/stack.ini`, whose
  re-measure note now points at the check instead of asking a human.
- **The fixtures:** the three 2026-08-01 false figures drive
  `tests/test_check_figures.py` (13 tests, watched red before the script
  existed) — each flags under a bare marker, warn-first then gating.
- **Rung 2 declined, with its reasons on record** (the enforcement-audit
  signed-measurement row, the module docstring, the stack.ini note): recorded
  commands are an execution surface needing an allow-list; most figures are
  legitimately historical, valid only at the recorded revision; some commands
  are expensive (tests+coverage 634 s) or non-deterministic. Decide it
  separately once declared figures show how many record a re-runnable
  command.
- **Registration:** SR-136 + LLR-146 + TC-140 (Verified, CMP-003); IF-086
  (Provides, the CLI step seam) + IF-087 (Consumes, the shared walk);
  CMP-003 description; bootstrap MAPPING + docstring (size stamp 2257 ->
  2258, reviewed); `tests/test_bootstrap.py` file list; the kit README row;
  dupes census cli class 86 -> 90 (the F5 boilerplate copies; the substance
  walk was lifted, not censused); byte re-stamp + session-protocol link in
  the skill source and both per-agent copy trees; `docs/gate` basis
  regenerated (SR=136 LLR=129 TC=126 — the derive_gate dogfood cache).

**Watched, all measured on the build commit 83ebd450 (clean tree), 2026-08-01
— a reviewer can rerun each command below at that revision:**

- module suite: 13 passed in 0.46s
  <!-- fig: cmd="python -m pytest -q tests/test_check_figures.py" rev=83ebd450 -->
  (first watched RED as 13 failed in 0.23s on the claim tree 3941fee0 with
  only the test file present — historical: that tree no longer exists)
- smoke tier: 607 passed / 6 skipped in 9.45s
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=83ebd450 -->
  (membership 613 within the 640 `[smoke-budget]` ceiling — no re-stamp)
- full suite: 1835 passed / 10 skipped in 0:04:43
  <!-- fig: cmd="python -m pytest -q -n auto" rev=83ebd450 -->
- `check_figures.py --root . --strict` rc=0; `check_doc_refs.py --root .
  --strict` rc=0; `check_trajectory.py --root . --strict` rc=0;
  `check_dupes.py --src project-trajectory/scripts` rc=0. `check_docs.py
  --root . --stale` stays at its pre-existing trunk red — 4 broken links
  <!-- fig: cmd="python project-trajectory/scripts/check_docs.py --root . --stale" rev=83ebd450 -->,
  all in WI-070/WI-173/WI-288 complete-spec records untouched by this branch
  (the same four WI-394's close recorded).
- byte budget: `PROCESS_OPTIONS.md` 166,314 -> 167,884
  <!-- fig: cmd="wc -c project-trajectory/PROCESS_OPTIONS.md" rev=83ebd450 -->,
  a growth of +1,570
  <!-- fig: derived="167,884 minus the 166,314 WI-378 baseline stamp, both wc -c readings" -->
  for the convention text; baseline re-stamped in the byte-budget-guard
  skill copies in the same commit.

**REVIEW-A rework (2026-08-01, findings 1-2), measured on the rework
commit's tree (the one commit after cab612c3):** the parser refuses
placeholder-grammar examples as declarations, judges each marker on its
own attributes, accepts a bare or quoted rev= while a wordless value
counts as missing, and skips `docs/reviews/` records; the convention's
own prose is fig-ok'd at source so a fresh bootstrap scaffold passes the
docstring opt-in end-to-end (the new scaffold-tier test, watched red on
the pre-fix tree at docs/process-options.md:1337 and :1354). The honest
census at this commit: 16 declared figures, rc=0
<!-- fig: cmd="python project-trajectory/scripts/check_figures.py --root . --strict" rev=this-rework-commit -->
— the close commit's 17 included 5 grammar-prose lines (2 in this
Deliverable, 2 in the log fragment, 1 in the enforcement audit) that
were never declarations, and this rework's own record adds 4 markers
<!-- fig: derived="17 minus the 5 placeholder-grammar lines the fixed parser refuses, plus the 4 markers this rework paragraph and the fragment add" -->.
Module suite 19 passed; byte budget 167,884 -> 168,222 (+338 rework,
+1,908 total on the 166,314 baseline), re-stamped.
