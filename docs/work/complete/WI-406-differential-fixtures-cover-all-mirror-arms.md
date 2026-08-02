+++
id = "WI-406"
title = "Extend WI-399's differential fixtures to the unpinned mirror arms (WI-399 REVIEW-A round-2 finding 4, ADVISORY, minted trunk-side at intake per the R3 invariant). THE GAP, as the reviewer measured it: _would_be_inventoried / _has_internal_import mirror gen_arch_map's emptiness predicate faithfully today (verified arm-by-arm with a 17-case differential harness), but the SHIPPED differential tests (regen_map fixtures in tests/test_trajectory_arch.py) pin only the arms their fixtures contain — the import-only re-exporting __init__, contracts-comment-only, and parse-error arms are consistent yet UNPINNED, so a future edit to either side of the mirror could drift those arms without a red. THE FIX IS FIXTURES ONLY: extend the regen_map differential suite with one fixture per unpinned arm (re-exporting __init__ that imports a sibling; a module whose only content is a first-8-lines Contracts: comment; a module with a syntax error — which per the generator STAYS inventoried), each asserted green-or-red identically in the lane rule and after a REAL gen_arch_map regen. No production-code change is expected; if extending the fixtures EXPOSES a divergence, that divergence is the real deliverable — fix it in the mirror (never in the generator) and say so. Scope: tests/test_trajectory_arch.py fixtures + (only if a divergence surfaces) check_trajectory's mirror helpers."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

Shipped 2026-08-02, work commit 29af0fcb. Fixtures only, as specced — no
production-code change: the three unpinned mirror arms of
`_would_be_inventoried` are now driven by the regen_map differential suite
(`tests/test_trajectory_arch.py`, WI-406 section), each through the full
lifecycle — lane red on the untagged module BEFORE any regeneration (the
mirror keeps it), a REAL gen_arch_map regen absorbs it and the delta empties
(the generator keeps it too — a mirror-only keep would be a permanent lane
red), the station rule holding the same red, the Component tag clearing
both. The re-exporting `__init__` fixture uses `from . import notes`
deliberately: module=None isolates the node.level arm — the
`from .notes import x` shape survived a scratch mutation dropping node.level
via the absolute-segment-in-names arm (the sibling's stem is in the names
universe) — and its comment-only sibling pins the symbol-emptiness skip
inside a package on both sides. The parse-error fixture pins the generator
half too: regen_map's rc==0 assert is the PARSE-ERROR-kept-not-crashed
claim. All three fixtures were GREEN on their first watched run — no
divergence exposed, as the review's 17-case harness predicted, so no mirror
fix was owed — and each pin was then proven to BITE by a scratch mutation of
its mirror arm (drop node.level / delete the first-8-lines Contracts block /
flip SyntaxError to False: each reds exactly its fixture; all reverted).
Registration judged: none owed — fixtures inside the already-cited
`tests/test_trajectory_arch.py` suite, no module added, no new LLR/TC rows.
Budgeted docs untouched.

Watched on 29af0fcb: tests/test_trajectory_arch.py 60 passed in 1.52s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev=29af0fcb -->;
smoke 621 passed / 6 skipped in 11.50s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=29af0fcb -->;
full suite 1883 passed / 10 skipped in 0:04:44
<!-- fig: cmd="python -m pytest -q -n auto" rev=29af0fcb -->.
