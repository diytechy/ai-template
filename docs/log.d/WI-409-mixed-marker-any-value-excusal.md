## 2026-08-02 — WI-409: mixed markers judged — the grammar excusal needs ALL values placeholder

**Summary.** WI-404 REVIEW-A finding 1 (the recorded MINOR that rode the
APPROVE): `judge_marker` excused the whole marker when ANY attribute value
fullmatched `PLACEHOLDER_VALUE`, so a half-filled template — a real command
typed, an unfilled `rev=<revision>` beside it — was classified GRAMMAR and
silently neither counted nor flagged, while the ratified PROCESS_OPTIONS.md
Grammar sentence reads all-values ("a marker whose values are wholly
placeholder tokens"). Spec-vs-code divergence in the silent direction, zero
live hits. The code now implements the ratified sentence: excusal only when
ALL values are placeholder-shaped; a mixed marker is a real declaration
judged on completeness, its placeholder value counting as ABSENT — the
reviewer's named trap, dodged: the bare rev= capture arrives unclosed
(`<revision`), carries word characters, and would otherwise satisfy the
wordful-rev test, passing the half-filled template as complete (the naive
all-values flip, convicted by the same assertion that convicts the old
excusal).

**Deliverables.**

- `project-trajectory/scripts/check_figures.py`: the excusal is now
  `values and all(_placeholder(v) ...)` (the empty-values guard keeps a bare
  marker flagging); `_placeholder` factored out and applied in the
  completeness judgment so an unfilled field never satisfies cmd=, rev= or
  derived=; the module docstring and `judge_marker` state the all-values
  rule, the absent-not-satisfying judgment, and the recorded note-2 corner.
- `tests/test_check_figures.py`: the reviewer's mixed fixtures both ways — a
  real cmd beside a placeholder rev flags its missing rev= (strict rc=1), a
  placeholder cmd beside a real rev flags its missing cmd=; the
  all-placeholder prose exemptions, the WI-404 whole-token fixtures and the
  scaffold-tier end-to-end test stay green untouched.

**Judgment calls / deviations.** (1) PROCESS_OPTIONS.md deliberately NOT
touched: the ratified Grammar sentence already states all-values — the code
moved to the sentence, so the spec's "one clarifying word" arm was not
needed and the byte budget is unmoved. (2) The note-2 rider taken on its
one-line arm: the rider's named shape (a quoted whitespace-free `<`-leading
cmd beside a full rev) now flags via the mixed rule itself, so only the
lone-all-placeholder residual remains and is recorded in the module
docstring; re-bounding the unclosed alternative to bare captures would have
threaded quoted-ness through the judge for a corner no runnable command
occupies. (3) LLR-146 `Detail` and TC-140 `Method` amended to the built
truth, DISCLOSED for the verdict round's adjudication (the WI-404/WI-402
precedent; no `Modified` flip — the requirement did not move, SR-136
untouched); the staged-spine amend-without-flip warn fired at the work
commit as designed, and the disclosure in the work-commit body and the
Deliverable is its answer.

**Byte deltas:** AGENTS.template.md 9,991, PROCESS.md 64,460 and
PROCESS_OPTIONS.md 169,125 all untouched
<!-- fig: cmd="wc -c project-trajectory/AGENTS.template.md project-trajectory/PROCESS.md project-trajectory/PROCESS_OPTIONS.md" rev=9895a654 -->
— no re-stamp owed.

**Watched, measured on the work commit 9895a654 (clean tree):** red first —
2 failed / 21 passed on the pre-fix tree, both mixed fixtures erring silent
exactly as convicted ("OK - no declared figures" both ways)
<!-- fig: cmd="python -m pytest -q tests/test_check_figures.py" rev="f67d6c70 with the two mixed-fixture tests staged, pre-fix" -->;
then green — 23 passed in 1.24s
<!-- fig: cmd="python -m pytest -q tests/test_check_figures.py" rev=9895a654 -->.
Smoke 625 passed / 6 skipped in 11.93s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=9895a654 -->;
full suite 1891 passed / 10 skipped in 0:05:04
<!-- fig: cmd="python -m pytest -q -n auto" rev=9895a654 -->;
live census unchanged at 45 declared, rc=0 under --strict — the three
all-placeholder grammar-prose lines stay exempt under the all-values rule
<!-- fig: cmd="python project-trajectory/scripts/check_figures.py --root . --strict" rev=9895a654 -->.
`check_trajectory --strict` and `check_doc_refs --strict` rc=0 (the LLR-146/
TC-140 amend-without-flip warns fired on the staged-spine surface at the
work commit — the disclosed adjudication ask; the remaining trajectory warns
are the pre-existing WI-389/WI-390 and connectivity set); `check_docs
--stale` stays at the pre-existing trunk red of 4 broken links (the same
WI-070/WI-173/WI-288 record lines, none added by this branch).
