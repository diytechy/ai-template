+++
id = "WI-098"
title = "Thin history-provenance comments in kit masters (H4)"
workstream = "scripts"
needs = ["~WI-079"]
order = 97
+++

## Deliverable

WI-098 (2026-07-14, OI-5 ruling log.md 2026-07-13): the review's H4 - shipped kit scripts narrate meta-repo history inline. WI-079 strips REVIEW_*/THREAD_* anchors at SCAFFOLD; this thins them IN THE MASTERS. Owner-ruled `thin` (over `keep`/`strip entirely`): keep the rule prose + the retained pointers, drop the dangling archive-doc archaeology. Dropped ~40 citations across 15 kit scripts: the REVIEW_GRIND_*/THREAD_*_REVIEW finding codes, the AGENT_ROLES Rn / IMPROVEMENT_PLAN.md Thread-n / capability-expansion.md C3 / `the S8 rulings` / `owner-ruled <date>` design-doc citations (the class the scaffold-strip left in scope per the OI-5 ruling). KEPT as the pointers (so provenance isn't `stripped entirely`): the named-convention shorthand `the F5 rule` (20+ live uses - a term of art, out of the owner's named scope; SURFACED as a candidate naming cleanup follow-on), the live cross-refs (process.md SS7, process-options.md "Unattended operation"), and the meaningful glosses ("verbatim across the kit", "pairs now, factor later"). The 6 identical `_utf8_console` cp1252 docstrings edited byte-identically to stay verbatim. UNTOUCHED: bootstrap.py's strip_provenance machinery documentation (lines ~1203-1266 name the anchor patterns to explain the regexes - load-bearing, not archaeology) - which also keeps WI-079's test_scaffolded_scripts_carry_no_archive_review_anchors kit_hits>0 valid (verified: 2 provenance tests pass; scaffolded copies still anchor-free). No script logic changed (comments/docstrings only); syntax OK on all 17 *.py; generated artifacts unaffected (comments aren't symbols). Commit bar: smoke 563 passed/2 skipped, check_docs --stale EXIT=0. No SN/SR/LLR/TC (G3), no byte-budgeted file touched.
