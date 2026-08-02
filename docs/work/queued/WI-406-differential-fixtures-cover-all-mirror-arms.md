+++
id = "WI-406"
title = "Extend WI-399's differential fixtures to the unpinned mirror arms (WI-399 REVIEW-A round-2 finding 4, ADVISORY, minted trunk-side at intake per the R3 invariant). THE GAP, as the reviewer measured it: _would_be_inventoried / _has_internal_import mirror gen_arch_map's emptiness predicate faithfully today (verified arm-by-arm with a 17-case differential harness), but the SHIPPED differential tests (regen_map fixtures in tests/test_trajectory_arch.py) pin only the arms their fixtures contain — the import-only re-exporting __init__, contracts-comment-only, and parse-error arms are consistent yet UNPINNED, so a future edit to either side of the mirror could drift those arms without a red. THE FIX IS FIXTURES ONLY: extend the regen_map differential suite with one fixture per unpinned arm (re-exporting __init__ that imports a sibling; a module whose only content is a first-8-lines Contracts: comment; a module with a syntax error — which per the generator STAYS inventoried), each asserted green-or-red identically in the lane rule and after a REAL gen_arch_map regen. No production-code change is expected; if extending the fixtures EXPOSES a divergence, that divergence is the real deliverable — fix it in the mirror (never in the generator) and say so. Scope: tests/test_trajectory_arch.py fixtures + (only if a divergence surfaces) check_trajectory's mirror helpers."
workstream = "scripts"
specref = "docs/reviews/WI-399-REVIEW-A.md"
buildtier = "quick"
safety_class = "ordinary"
+++
