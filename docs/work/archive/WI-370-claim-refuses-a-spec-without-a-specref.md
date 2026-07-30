+++
id = "WI-370"
title = "The claim protocol accepts a queued spec that reds R-E on every composed tree: integrate.py claim checks the pause, trunk cleanliness, branch shape, safety class, frontier membership and the WI-358 status scan - but not that the spec carries a SpecRef resolving in-repo, so an intake filed against the warn-first floor (as WI-368 and WI-369 were, 2026-07-30) claims cleanly and then reds R-E under --strict in every composed-tree bar that sees it open, from a file the closing branches cannot amend without poisoning their own rename-merges (SpecRef present at open + cleared at terminal means trunk-side repair merges the ref INTO the archived copy, tripping R-F). Add the R-E check as a claim rung: refuse to claim a spec whose SpecRef is empty or does not resolve, naming the field - the debt is payable in one trunk commit before the branch exists, exactly the WI-358 shape. Test in tests/test_integrate.py's claim-refusal section."
workstream = "scripts"
specref = ""
buildtier = "quick"
priority = 2
safety_class = "ordinary"
+++

## Deliverable

DONE 2026-07-30. `integrate.py` gains `_specref_refusal(root, meta, wi_id)`
— the WI-370 claim rung, in the WI-358 helper shape — wired into
`_claim_refusal` after the safety-class check: a queued spec whose
`specref` is empty refuses with the R-E consequence and the payment path
(one trunk commit, then claim); a non-empty ref whose PATH part does not
exist in-repo refuses by name. Anchor (`path#anchor`) resolution stays
check_trajectory's job — the rung checks the path part only, pinned by a
passing-path test. Tests: three rung tests in tests/test_integrate.py's
claim-refusal section (empty ref, unresolving ref, anchor form claiming
clean through the whole ladder); fixtures now state which shape a spec is
in — `spec_text` writes `specref` only when given, `claim_repo` queued
specs resolve to the fixture seed by default, and the e2e closing move
CLEARS the ref the way a real close does (R-F wants a terminal SpecRef
empty on the composed tree). The inline first cut pushed `_claim_refusal`
to C901 complexity 11; extracted rather than baseline-stamped.
