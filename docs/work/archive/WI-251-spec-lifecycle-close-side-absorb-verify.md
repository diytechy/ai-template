+++
id = "WI-251"
title = "Spec-lifecycle close side: absorb-verify sweep (archive done-WI specs after confirming a spine/architecture home, clear the 137 stale done-row SpecRefs) + fail-closed R-F in check_trajectory (done WI => empty SpecRef; a live docs/specs file needs an open citing WI; WARN commit bar / ERROR --strict per WI-243) + dogfood the scaffold boilerplate this repo predates (specs+rubrics README/-000 exemplars, .githooks/commit-msg; fix the WI-000 delete-banner template-side first) + test_dogfood_sync walks bootstrap.MAPPING against a declared-omissions list (2026-07-20 owner directive, scope re-affirmed same day)"
workstream = "quality"
sr_refs = ["SR-109"]
buildtier = "strong"
safety_class = "high-risk"
order = 248
+++

## Deliverable

Close-side spec lifecycle SHIPPED + fail-closed. R-F in check_trajectory (spec_lifecycle_findings: done WI => empty SpecRef; live docs/specs file needs >=1 open citer; scaffold README/-000 excluded; shared doc lives while any open citer remains) rides the warn-plain/ERROR-under---strict tier - WARN at the commit bar, gate-blocking at G2/G3, vacuous on a fresh scaffold, opt-out docs/trajectory-check. Spine: SR-109/LLR-097/TC-100 Verified via 4 new test_trajectory R-F cases. The absorb-verify sweep: 4 independent verifier agents checked all 61 archivable specs against the permanent homes - 61/61 ABSORBED zero gaps (per-spec dispositions in log 2026-07-20) - then archived each to docs/archive/specs/<stem>.2026-07-20.md (ARCHIVED banner, WI-attributed) and cleared all 137 stale done-row SpecRefs; links re-resolved, check_docs 0 broken. Dogfood: WI-000.template delete-banner contradiction fixed (permanent exemplar), specs+rubrics README/-000 backfilled (root cause: docs/specs predated WI-053; 0/58 live specs had carried the close-ritual boxes), .githooks/commit-msg installed as a delegating wrapper (verbatim-copy attempt failed live - shipped hook assumes scripts/ layout). Standing invariants: test_dogfood_sync walks bootstrap.MAPPING vs SCAFFOLD_OMISSIONS (each with reason, currency + bite-proof tests) + byte-identity pins on the 4 boilerplate copies (109-REVIEW-A MINOR consumed). PROCESS_OPTIONS R-F prose +492B flagged/re-stamped. 109-REVIEW-A APPROVE f=2 all MINOR, both consumed (byte-identity test; status trim).
