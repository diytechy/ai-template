+++
id = "WI-410"
title = "One more differential fixture: the absolute-import arms of _has_internal_import are unpinned (WI-406 REVIEW-A finding 1, minted trunk-side at intake per the R3 invariant). DRIVEN by the reviewer: dropping BOTH absolute arms (the ImportFrom names-membership check and the whole ast.Import branch) leaves all 60 tests green - an absolute-import-only module (import scripts.sibling / from scripts import sibling with no relative form) can drift mirror-side without a red. Same fixtures-only shape as WI-406, one fixture: a module whose only internal reference is an absolute import, driven through the full differential lifecycle (lane red untagged before regen, real gen_arch_map absorbs, station parity, tag clears both), plus the scratch-mutation drive proving the new pin bites when either absolute arm is dropped and nothing else reds. If the fixture EXPOSES a real divergence, the divergence is the deliverable, fixed in the mirror never the generator. Scope: tests/test_trajectory_arch.py only."
workstream = "scripts"
specref = "docs/reviews/WI-406-REVIEW-A.md"
buildtier = "quick"
safety_class = "ordinary"
+++
