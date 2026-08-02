+++
id = "WI-411"
title = "The last unpinned mirror arm: dotted-absolute first-segment semantics (WI-410 REVIEW-A finding 1, minted trunk-side at intake per the R3 invariant). DRIVEN by the reviewer: a whole-name-membership mutation (dropping the split-dot first-segment read inside BOTH absolute arms) left all 61 tests green, so a module whose only internal reference is a DOTTED absolute import (import pkg.mod, or from pkg.mod import x resolved via the first segment) could drift mirror-side station-first. Same WI-406/WI-410 fixtures-only shape, one fixture: a dotted-absolute-import-only module through the full differential lifecycle (real gen_arch_map, lane red untagged, absorption, station parity, tag clears), plus the scratch-mutation drive proving the pin bites when the first-segment read is dropped and nothing else reds. Per the WI-410 arm inventory this exhausts the mirror's arm list - state that in the fixture comment so the pinning series has a recorded terminus. If the fixture exposes a real divergence, the divergence is the deliverable, fixed in the mirror never the generator. Scope: tests/test_trajectory_arch.py only."
workstream = "scripts"
specref = "docs/reviews/WI-410-REVIEW-A.md"
buildtier = "quick"
safety_class = "ordinary"
+++
