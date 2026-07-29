+++
id = "WI-356"
title = "The census audit guard checks every distribution ROW against its section but never the declared TOTAL, so docs/dupes-allow's header can drift silently. Measured 2026-07-28 during WI-347: the header read 'The distribution (207 blocks)' while the sections held 201 fingerprint lines, and all 13 audit tests passed - because the guard compares each row's count to its own section header, every header did match its own lines, and nothing compares the sum to reality. The 'By disposition' summary line was stale the same way, reading 'extract 35' while the rows summed to 29. One block of the 6-block gap is explained (WI-341 merged two adjacent spine-loader runs); the rest was never tracked down, which is exactly the cost of an unchecked aggregate. Fix: assert the declared total equals the summed section counts AND the emitted census size, and assert the by-disposition line against the sections - or generate the whole header block from the sections, which is the rule this repo already applies to derived numbers. Guard it by mutating the header total and confirming red; a guard that cannot fail is the defect being fixed here."
workstream = "scripts"
specref = "docs/dupes-allow"
buildtier = "quick"
priority = 2
safety_class = "ordinary"
order = 353
+++

## Deliverable

RETIRED 2026-07-29, concurrency-restructure Phase 5 item 7, per the 2026-07-28
audit ruling (handoff-2026-07-28c §3): the header total and "By disposition"
aggregate were third copies of guarded data with no check of their own, so the
fix was to DELETE the numbers, not to build the assert this row proposed. Done
at the Phase 5 item-1 commit's census re-derive: docs/dupes-allow now carries
the per-class distribution table (guarded row-by-row against the sections by
tests/test_dupes_census_audit.py) and no unchecked document-level aggregates.
A number nobody checks is a number that lies; the census now states only the
figures its tests compare.
