+++
id = "WI-409"
title = "judge_marker excuses MIXED markers wholesale; the code implements any-value where the ratified Grammar sentence says all-values (WI-404 REVIEW-A finding 1, minted trunk-side at intake per the R3 invariant). DRIVEN by the reviewer: a marker carrying a real cmd beside a wholly-placeholder rev - cmd of wc -c README.md with rev=<revision> - is classified GRAMMAR by the any() in judge_marker and silently neither counted nor flagged, while the amended PROCESS_OPTIONS.md Grammar sentence reads markers whose values are WHOLLY placeholder tokens (all-values). Zero live hits today; the divergence is spec-vs-code and the silent direction. THE FIX aligns code to the ratified sentence: a marker is example grammar only when ALL its attribute values are placeholder-shaped; a mixed marker is a REAL marker judged on completeness (the real cmd with placeholder rev then flags no rev=, the correct loud direction). THE TRAP the reviewer named, do not fall in: the naive all-values flip alone is wrong because an unclosed <revision token carries word characters and would satisfy has_rev's bare capture - the completeness judgment must treat a placeholder-shaped value as ABSENT (placeholder rev == no rev), not as a satisfying value. Tests: the reviewer's mixed fixture both ways (flags after, silent before); the all-placeholder convention-prose lines stay exempt (census stays honest); the WI-404 whole-token cases keep their classification. RIDER, note-2 bound (judge, take only if one line): the unclosed alternative excuses a whitespace-free <-leading QUOTED cmd with a full rev - no runnable command has that shape; either bound the unclosed alternative to unquoted values or record the corner in the module docstring. Scope: check_figures.judge_marker + tests + (if the Grammar sentence needs one clarifying word) the byte-budgeted PROCESS_OPTIONS.md line with the three-copy re-stamp."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

Shipped 2026-08-02, work commit 9895a654. `judge_marker` now implements the
ratified all-values Grammar sentence: a marker is example grammar — excused,
uncounted — only when ALL its attribute values are wholly placeholder tokens
(`values and all(...)`; the empty-values guard keeps a bare marker flagging).
A MIXED marker — one real value beside an unfilled `<token>` — is a real,
half-filled declaration judged on completeness, and the reviewer's named trap
is dodged: in that judgment a placeholder-shaped value counts as ABSENT,
never as satisfying — the bare rev= capture arrives unclosed (`<revision`),
which carries word characters and would otherwise satisfy the wordful-rev
test, silently passing the half-filled template as complete (the naive
all-values flip, convicted by the same assertion that convicts the old
excusal). The reviewer's mixed fixtures now land loud both ways: a real cmd
beside an unfilled rev=<revision> flags its missing rev=, an unfilled
cmd="<command>" beside a real rev flags its missing cmd=. Rider (note 2),
judged: its named shape — a quoted whitespace-free `<`-leading cmd beside a
full rev — now flags via the mixed rule itself, so only the
lone-all-placeholder residual remains, recorded in the module docstring (the
one-line arm); the unclosed alternative was not re-bounded.

Watched red first: the two new mixed-fixture tests on the pre-fix tree
failed exactly as convicted, 2 failed / 21 passed, "OK - no declared
figures" in both silent directions
<!-- fig: cmd="python -m pytest -q tests/test_check_figures.py" rev="f67d6c70 with the two mixed-fixture tests staged, pre-fix" -->;
green after: 23 passed
<!-- fig: cmd="python -m pytest -q tests/test_check_figures.py" rev=9895a654 -->,
the all-placeholder convention prose staying exempt, the WI-404 whole-token
fixtures keeping their classification, the scaffold-tier end-to-end test
green, and the live census unchanged at 45 declared rc=0
<!-- fig: cmd="python project-trajectory/scripts/check_figures.py --root . --strict" rev=9895a654 -->.
Full suite 1891 passed / 10 skipped in 0:05:04
<!-- fig: cmd="python -m pytest -q -n auto" rev=9895a654 -->;
smoke 625 passed / 6 skipped in 11.93s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=9895a654 -->.

PROCESS_OPTIONS.md deliberately untouched — the ratified Grammar sentence
already states all-values, so the code moved to the sentence and no
clarifying word was needed; 169,125 bytes unchanged, no re-stamp owed
<!-- fig: cmd="wc -c project-trajectory/PROCESS_OPTIONS.md" rev=9895a654 -->.

DISCLOSED for the verdict round's adjudication (ratified-cell amendments,
the WI-404/WI-402 precedent, no Modified flip — the requirement did not move
and the owning SR's AcceptanceCriteria already name the class): LLR-146
Detail now states the all-values excusal and the placeholder-counts-as-absent
judgment; TC-140 Method adds the mixed behavior 1:1 with the two new tests;
SR-136 untouched. The staged-spine amend-without-flip warn fired at the work
commit as designed; this disclosure is its answer. Full session record: the
WI-409 entry in docs/log.md (compiled from this branch's fragment).
