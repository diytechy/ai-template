+++
id = "WI-411"
title = "The last unpinned mirror arm: dotted-absolute first-segment semantics (WI-410 REVIEW-A finding 1, minted trunk-side at intake per the R3 invariant). DRIVEN by the reviewer: a whole-name-membership mutation (dropping the split-dot first-segment read inside BOTH absolute arms) left all 61 tests green, so a module whose only internal reference is a DOTTED absolute import (import pkg.mod, or from pkg.mod import x resolved via the first segment) could drift mirror-side station-first. Same WI-406/WI-410 fixtures-only shape, one fixture: a dotted-absolute-import-only module through the full differential lifecycle (real gen_arch_map, lane red untagged, absorption, station parity, tag clears), plus the scratch-mutation drive proving the pin bites when the first-segment read is dropped and nothing else reds. Per the WI-410 arm inventory this exhausts the mirror's arm list - state that in the fixture comment so the pinning series has a recorded terminus. If the fixture exposes a real divergence, the divergence is the deliverable, fixed in the mirror never the generator. Scope: tests/test_trajectory_arch.py only."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

Shipped 2026-08-02, work commit 91462f79. Fixtures only, as specced — no
production-code change: the first-segment `.split(".")[0]` read inside BOTH
absolute arms of `_has_internal_import` is now driven by the regen_map
differential suite (`tests/test_trajectory_arch.py`, WI-411 section), one
differential lifecycle — lane red on both untagged dotted modules BEFORE
any regeneration (the mirror keeps them), a REAL gen_arch_map regen absorbs
both and the delta empties (a mirror-only keep would be a permanent lane
red), the station rule holding the same red, the Component tags clearing
both. The names-universe geometry is the load-bearing move: a comment-only
`notes` module inside the fixture's scanned `pkg` directory donates `pkg`
to the universe (both sides collect stems +
package directory parts from every scanned file BEFORE the symbol-emptiness
filter) while never itself entering the delta, and the whole dotted name
`pkg.notes` is in the universe on NEITHER side — so only a first-segment
read can keep the two dotted modules. The WI-410 two-module lesson holds
one grain finer: the arms are disjoint syntactic branches, so each arm's
split is pinned by its own one-form module (`import pkg.notes` for the
ast.Import arm, `from pkg.notes import go` for ImportFrom). The fixture was
GREEN on its first watched run — no divergence exposed, so no mirror fix
was owed — and the pin was proven to BITE by scratch mutations (rsync copy,
never the worktree): dropping the ImportFrom split alone, the ast.Import
split alone, and the review's both-dropped probe (previously all-green
across 61 tests) each red EXACTLY this fixture — 1 failed, 61 passed, all
three; two name asserts, one rc assert — with the scratch restored
byte-identical and re-green (62 passed). Per the WI-410 arm inventory the
pinning series' terminus is recorded WITH ONE NAMED RESIDUE — REVIEW-A
finding 2 corrected the original exhausts-the-arms claim (reworked
2026-08-02, next paragraph): every arm is fixture-pinned except the
read-failure branch. Registration judged: none owed — a fixture inside
the already-cited `tests/test_trajectory_arch.py` suite, no module added,
no new LLR/TC rows (the WI-406 REVIEW-A precedent). Budgeted docs
untouched.

Reworked 2026-08-02 on REVIEW-A (CHANGES-REQUESTED findings=2), one rework
commit, still fixtures-only. (1) The masked pair: the reviewer's mutations
dropped the docstring arm alone and the public-symbol arm alone — each
left all 62 tests green, MODULE_BODY satisfying both arms at once — so two
one-form fixtures now pin the pair (a docstring-ONLY and a
public-symbol-ONLY module through the same real-regen lifecycle, both
green on their first watched runs); each single-arm scratch drop reds
EXACTLY its fixture on the rc assert — 1 failed, 64 passed, both. (2) The
honest terminus: every arm of `_would_be_inventoried` and
`_has_internal_import` is fixture-pinned EXCEPT the read-failure branch
(OSError/UnicodeDecodeError -> False), which the green-green differential
cannot drive — gen_arch_map itself CRASHES on a non-UTF-8 .py (probed:
UnicodeDecodeError in scan_module's read_text, rc 1), so there is no
absorb side. Its UnicodeDecodeError half is pinned LANE-SIDE only (a
deterministic invalid-start-byte fixture; either drift direction reds:
flip-to-True 1 failed / 64 passed, except-drop 1 failed / 64 passed); the
OSError half — an unreadable file, not stageable portably — stays the
argued exception, named in the section comment. The original three
first-segment drives re-red exactly the dotted fixture in the enlarged
suite (1 failed, 64 passed, all three); scratch restored byte-identical,
re-green 65 passed.

Watched on 91462f79: tests/test_trajectory_arch.py 62 passed in 1.64s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev=91462f79 -->;
smoke 625 passed / 6 skipped in 10.29s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=91462f79 -->;
full suite 1893 passed / 10 skipped in 0:05:04
<!-- fig: cmd="python -m pytest -q -n auto" rev=91462f79 -->.

Watched on the rework tree (91462f79 + the REVIEW-A rework; tests/
byte-identical to the rework commit): tests/test_trajectory_arch.py
65 passed in 1.84s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev="91462f79 plus the rework diff, tests identical to the rework commit" -->;
smoke 629 passed / 2 skipped in 10.16s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev="91462f79 plus the rework diff, tests identical to the rework commit" -->.
