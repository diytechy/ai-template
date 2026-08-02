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
byte-identical and re-green (62 passed). Per the WI-410 arm inventory this
EXHAUSTS the mirror's arms — the pinning series' recorded terminus, stated
in the section comment. Registration judged: none owed — a fixture inside
the already-cited `tests/test_trajectory_arch.py` suite, no module added,
no new LLR/TC rows (the WI-406 REVIEW-A precedent). Budgeted docs
untouched.

Watched on 91462f79: tests/test_trajectory_arch.py 62 passed in 1.64s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev=91462f79 -->;
smoke 625 passed / 6 skipped in 10.29s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=91462f79 -->;
full suite 1893 passed / 10 skipped in 0:05:04
<!-- fig: cmd="python -m pytest -q -n auto" rev=91462f79 -->.
