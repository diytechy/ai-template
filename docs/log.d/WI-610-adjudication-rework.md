## 2026-09-07 — WI-610 adjudication rework, publication pending

Reworked the same bound primary turn in
[the current judgment](../reviews/contract_split/012-ADJUDICATE-4dd61ff.md), committed
as `3ce4422ffb16e78125604c79a7327765c991c075`. Preserved all-row RETURN and frozen
registry/snapshot bindings; recorded LLR-167 retention, LLR-207 responsibility
redistribution and explicit counterpart decisions. The queued spec's typed
continuation carries IF-175 and missing primary-path proofs as dependencies.
Preserved actual design advice and transport evidence byte-identically. No managed
session metadata, ordinary reviewer verdict, successor or publication was authored.

Validation: smoke 1696 passed, 4 skipped in 49.86s; measured wall 50.1s within 90s.
<!-- fig: .venv/bin/python scripts/check_smoke_budget.py --mode enforce; source revision 3ce4422ffb16e78125604c79a7327765c991c075 with only the reviewed queued Approval/Dispositions changes; output out/run-logs/wi-610/rework-012-payload-smoke.txt -->
The real Approval and Dispositions parsers accept the exact returned scope and one
spine continuation. Docs check passed with the existing report.md orphan warning;
unfiltered strict trajectory check is clean with existing advisories. Budgeted
document byte delta: zero. Deviation: no acceptance/publication claimed; the engine
still owes authentic current-session evidence and ordinary independent review
before the exclusive publisher may validate and publish RETURN. Coordinator remains
paused, with no control window, push, main merge or batch-code deletion.

Deferred open items: none — required corrections remain scoped in Dispositions;
this judgment adds no owner decision or first-approval authority.
