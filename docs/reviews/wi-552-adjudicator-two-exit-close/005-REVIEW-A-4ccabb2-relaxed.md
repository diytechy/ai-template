# WI-552 REVIEW-A (independent) — the adjudicator's two exits

Scope: `git diff contract_split...HEAD` (work under review), against AGENTS/PROCESS,
the WI-552 spec-of-record (archived), and the OI-70/OI-73 rulings (docs/log.md).

Harness run by the reviewer (once each, summaries only):
- `trace.py --strict-integrity`: `SN=27 SR=76 LLR=188 TC=186 orphans=2 integrity=0 ... provenance-findings=1 paraphrase-advisories=3` (the LLR-197/provenance advisories are pre-existing trunk state — the diff touches no `docs/requirements` row).
- `check.py --jobs 0`: `RESULT: PASS`.
- `pytest tests/test_intake.py tests/test_handback.py tests/test_schedule.py tests/test_dispatch.py tests/test_trajectory.py`: `190 passed in 48.80s`.

Done-when map: DW1 (mechanical close) covered by test_handback close/merge tests + dispatch wiring; DW2 (OI-mint gates successor) covered; DW3 (refusal invariant) covered for PARTIAL only — **CANCELLED arm UNCOVERED, see MAJOR below**; DW4 (inbound-edge replacement) covered; DW5 (typed OI edges) covered in schedule/trajectory tests; DW6 (dead-dep → partial) covered; DW7 (contract text) — prose updated but overreaches the machinery, see MAJOR.

Drove the real shipped path (`test_handback.adjudication_repo` + `hb.close_adjudication`) to construct the cancelled-close scenario; result quoted in the MAJOR finding.

## Findings

- [MAJOR] project-trajectory/scripts/intake.py:1150 (and handback.py:516) -> the refusal invariant gates on `brief == "disposition"`, but a CANCELLED original close mints a brief-LESS adjudication row (`intake._close_drafts` cancellation arm, ~line 841: "NO `brief`"), so neither the close-side (`close_adjudication`) nor the merge-side (`_disposition_drafts`) guard fires for a cancelled disposition — a cancelled close that queues no successor archives/merges silently, contradicting OI-73 ("Every PARTIAL or CANCELLED disposition must queue at least one successor WI"), Done-when 3 ("a PARTIAL or CANCELLED disposition that queues NO successor is REFUSED ... nothing silent"), and the newly-shipped ADJUDICATE contract text ("A PARTIAL or CANCELLED close MUST queue at least one successor ... REFUSED at that close"). The code comment at intake.py:1145 asserts the false premise ("a PARTIAL or CANCELLED close is judged by a `disposition`-brief adjudication row"). Confirmed empirically: a brief-less adjudication row with `dispositions=""` returns `IDS=['WI-401'] REFUSAL=None` from `close_adjudication` (closed, not refused). -> distinguish the cancelled-close adjudication row (its title/context, or a dedicated marker) from the complete-spot-check row — which legitimately needs no successor — and apply the refusal to the cancelled case at both guards; add a test driving a cancelled disposition with no successor. -> @owner
- [MINOR] project-trajectory/scripts/schedule.py:678 -> Done-when 6 makes `partial` a terminal, will-never-integrate predecessor (validator `dead_dependency_findings` now flags it), but the scheduler's `_waiting_reasons` still emits the "waiting:hard-pred-cancelled" dead-edge reason only for `cancelled`; a WI hard-blocked on a `partial` predecessor shows only the generic "waiting:hard-preds-not-done" in `--explain`, so the two surfaces disagree on whether a partial edge is dead and the owner isn't told it's will-never-happen. -> include `partial` in the `dead` set (or add a partial dead-reason code) so the scheduler and validator agree. -> @owner
- [MINOR] project-trajectory/scripts/schedule.py:434 -> the `_OI_PENDING` comment says "or the row simply gone — is 'left pending' and satisfies the edge", which contradicts both the code and its own next clause ("an OI id absent from the states map is NOT satisfied (fails closed)"); a gone/absent OI fails closed, it does not satisfy. The stray phrase could mislead a maintainer into loosening the gate. -> drop the "or the row simply gone" clause from the comment. -> @owner

VERDICT: CHANGES-REQUESTED findings=3
