+++
id = "WI-410"
title = "One more differential fixture: the absolute-import arms of _has_internal_import are unpinned (WI-406 REVIEW-A finding 1, minted trunk-side at intake per the R3 invariant). DRIVEN by the reviewer: dropping BOTH absolute arms (the ImportFrom names-membership check and the whole ast.Import branch) leaves all 60 tests green - an absolute-import-only module (import scripts.sibling / from scripts import sibling with no relative form) can drift mirror-side without a red. Same fixtures-only shape as WI-406, one fixture: a module whose only internal reference is an absolute import, driven through the full differential lifecycle (lane red untagged before regen, real gen_arch_map absorbs, station parity, tag clears both), plus the scratch-mutation drive proving the new pin bites when either absolute arm is dropped and nothing else reds. If the fixture EXPOSES a real divergence, the divergence is the deliverable, fixed in the mirror never the generator. Scope: tests/test_trajectory_arch.py only."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

Shipped 2026-08-02, work commit 34894b48. Fixtures only, as specced — no
production-code change: the absolute-import arms of `_has_internal_import`
are now driven by the regen_map differential suite
(`tests/test_trajectory_arch.py`, WI-410 section), one differential
lifecycle — lane red on the untagged modules BEFORE any regeneration (the
mirror keeps them), a REAL gen_arch_map regen absorbs both and the delta
empties (a mirror-only keep would be a permanent lane red), the station
rule holding the same red, the Component tags clearing both. One lifecycle,
TWO driftable modules, by necessity: the two absolute arms are disjoint
syntactic branches — one import statement trips exactly one — so no single
module can pin both, and the fixture tree ships both flat-layout shapes
(`import mod_0` for the ast.Import branch, `from mod_0 import run` for the
ImportFrom names-membership arm), each with no other inventoried content.
The names universe both sides build is module stems + package directory
parts — the scan root's own name is in neither, so the flat stem is the
internal shape and `from scripts import mod_0` would be external on both
sides alike (the fixture comment records the why). The fixture was GREEN on
its first watched run — no divergence exposed, so no mirror fix was owed —
and the pin was then proven to BITE by scratch mutations: dropping the
names-membership arm alone (`if node.level:`), deleting the whole
ast.Import branch alone, and the review's both-dropped probe (previously
all-green across 60 tests) each red EXACTLY this fixture — 1 failed,
60 passed, all three — with the scratch restored byte-identical and
re-green (61 passed). Registration judged: none owed — a fixture inside the
already-cited `tests/test_trajectory_arch.py` suite, no module added, no
new LLR/TC rows (the WI-406 REVIEW-A precedent). Budgeted docs untouched.

Watched on 34894b48: tests/test_trajectory_arch.py 61 passed in 1.58s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev=34894b48 -->;
smoke 625 passed / 6 skipped in 12.11s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=34894b48 -->;
full suite 1892 passed / 10 skipped in 0:05:04
<!-- fig: cmd="python -m pytest -q -n auto" rev=34894b48 -->.
